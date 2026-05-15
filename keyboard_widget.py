"""
Main keyboard widget — QWERTY and Grouped layouts, rebuilt correctly.
"""
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QFrame, QScrollArea, QSizePolicy, QMenu, QAction
)
from PyQt5.QtCore import Qt, pyqtSignal, QTimer, QPoint, QSize
from PyQt5.QtGui import QFont, QPixmap, QIcon
import os

from symbol_data import (
    HANDSHAPE_SYMBOLS, LOCATION_SYMBOLS, MOVEMENT_SYMBOLS,
    ORIENTATION_SYMBOLS, HAND_ARRANGEMENT_SYMBOLS, HAND_PARTS_SYMBOLS,
    HANDSHAPE_KEY_MAP, LOCATION_KEY_MAP, MOVEMENT_KEY_MAP,
    QWERTY_ROWS, get_symbol_by_id, get_symbols, get_key_map
)
from config import load_custom_symbols


# ─────────────────────── helpers ───────────────────────

def _clear_layout(layout):
    """Recursively remove all items from a layout."""
    if layout is None:
        return
    while layout.count():
        item = layout.takeAt(0)
        child_layout = item.layout()
        if child_layout:
            _clear_layout(child_layout)
        widget = item.widget()
        if widget:
            widget.setParent(None)
            widget.deleteLater()


# ─────────────────────── Key button ───────────────────────

class KeyButton(QPushButton):
    symbol_clicked = pyqtSignal(dict)

    def __init__(self, sym_data, phys_key="", parent=None):
        super().__init__(parent)
        self.sym_data = sym_data
        self.phys_key = phys_key
        self.setCursor(Qt.PointingHandCursor)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self._setup()
        self.clicked.connect(self._click)

    def _setup(self):
        if not self.sym_data:
            self.setText(self.phys_key)
            self.setProperty("class", "keyBtnEmpty")
            self.setEnabled(False)
            self.setToolTip(f"[{self.phys_key}] — нет символа")
            return

        label = self.sym_data.get("label", "?")
        vis = self.sym_data.get("visual_hint", "")

        glyph = self.sym_data.get("custom_glyph")
        if glyph and os.path.exists(str(glyph)):
            pix = QPixmap(str(glyph)).scaled(28, 28, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.setIcon(QIcon(pix))
            self.setIconSize(QSize(28, 28))
            self.setText("")
        else:
            if vis:
                self.setText(f"{vis}\n{label}")
            else:
                self.setText(label)

        self.setFont(QFont("Segoe UI Symbol", 11))
        self.setProperty("class", "keyBtn")

        desc = self.sym_data.get("description_ru", "")
        desc_en = self.sym_data.get("description_en", "")
        key_hint = f"Клавиша: [{self.phys_key}]" if self.phys_key else ""
        tip_parts = [desc, desc_en, f"ID: {self.sym_data.get('id','')}", key_hint]
        self.setToolTip("\n".join(p for p in tip_parts if p))

    def _click(self):
        if self.sym_data:
            self.symbol_clicked.emit(self.sym_data)

    def flash(self):
        self.setProperty("class", "keyBtnHighlight")
        self.style().unpolish(self)
        self.style().polish(self)
        self.update()
        QTimer.singleShot(250, self._unflash)

    def _unflash(self):
        self.setProperty("class", "keyBtn")
        self.style().unpolish(self)
        self.style().polish(self)
        self.update()


# ─────────────────────── Keyboard Widget ───────────────────────

class KeyboardWidget(QWidget):
    symbol_clicked = pyqtSignal(dict)
    theme_change_requested = pyqtSignal()
    help_requested = pyqtSignal()
    custom_symbols_requested = pyqtSignal()

    LAYER_NAMES = {
        "handshape": "✊ Кистежесты (DEZ)",
        "location": "📍 Расположение (TAB)",
        "movement": "➡ Движения (SIG)",
    }

    def __init__(self, theme_mgr, parent=None):
        super().__init__(parent)
        self.theme_mgr = theme_mgr
        self.current_layer = "handshape"
        self.layout_mode = "qwerty"
        self._key_buttons = {}   # phys_key -> KeyButton (only in qwerty)

        self._main_lo = QVBoxLayout(self)
        self._main_lo.setSpacing(6)
        self._main_lo.setContentsMargins(6, 4, 6, 4)

        self._build_toolbar()
        self._build_keyboard_area()
        self._build_status()
        self._populate_keyboard()

    # ─── toolbar ───
    def _build_toolbar(self):
        bar = QFrame()
        bar.setObjectName("toolbar")
        lo = QHBoxLayout(bar)
        lo.setContentsMargins(10, 6, 10, 6)
        lo.setSpacing(8)

        # Layer buttons
        self._layer_btns = {}
        for layer_id, label in self.LAYER_NAMES.items():
            b = QPushButton(label)
            b.setProperty("class", "layerBtnActive" if layer_id == self.current_layer else "layerBtn")
            b.clicked.connect(lambda checked, lid=layer_id: self.set_layer(lid))
            lo.addWidget(b)
            self._layer_btns[layer_id] = b

        lo.addStretch(1)

        # Tool buttons
        for text, tip, slot in [
            ("⊕ Ещё", "Ориентация, руки, части кисти", self._show_extras),
            ("⌨", "Раскладка: QWERTY / По группам (F6)", self.toggle_layout),
            ("🎨", "Сменить тему (F5)", self.theme_change_requested.emit),
            ("✏", "Пользовательские символы (F7)", self.custom_symbols_requested.emit),
            ("?", "Справка (F1)", self.help_requested.emit),
        ]:
            b = QPushButton(text)
            b.setProperty("class", "toolBtn")
            b.setToolTip(tip)
            b.clicked.connect(slot)
            lo.addWidget(b)

        self._main_lo.addWidget(bar)

    # ─── keyboard area ───
    def _build_keyboard_area(self):
        self._kb_frame = QFrame()
        self._kb_frame.setObjectName("keyboardFrame")
        self._kb_lo = QVBoxLayout(self._kb_frame)
        self._kb_lo.setContentsMargins(8, 8, 8, 8)
        self._kb_lo.setSpacing(4)
        self._main_lo.addWidget(self._kb_frame, 1)

    # ─── status ───
    def _build_status(self):
        self._status = QLabel()
        self._status.setObjectName("statusLabel")
        self._status.setAlignment(Qt.AlignCenter)
        self._main_lo.addWidget(self._status)
        self._update_status()

    def _update_status(self):
        ln = self.LAYER_NAMES.get(self.current_layer, self.current_layer)
        mode = "QWERTY" if self.layout_mode == "qwerty" else "По группам"
        tn = self.theme_mgr.colors.get("name", "")
        self._status.setText(f"Слой: {ln}  ·  Раскладка: {mode}  ·  Тема: {tn}")

    # ─── populate ───
    def _populate_keyboard(self):
        _clear_layout(self._kb_lo)
        self._key_buttons.clear()

        if self.layout_mode == "qwerty":
            self._build_qwerty()
        else:
            self._build_grouped()

        self._update_status()

    def _build_qwerty(self):
        km = get_key_map(self.current_layer)
        syms = get_symbols(self.current_layer)
        lookup = {s["id"]: s for s in syms}

        for row_keys in QWERTY_ROWS:
            row_lo = QHBoxLayout()
            row_lo.setSpacing(3)
            for key in row_keys:
                sid = km.get(key)
                sd = lookup.get(sid) if sid else None
                btn = KeyButton(sd, key, self._kb_frame)
                btn.setMinimumSize(46, 50)
                btn.setMaximumHeight(66)
                btn.symbol_clicked.connect(self.symbol_clicked.emit)
                row_lo.addWidget(btn)
                self._key_buttons[key] = btn
            self._kb_lo.addLayout(row_lo)

        # Space bar
        space_lo = QHBoxLayout()
        space_lo.addStretch(2)
        sp = QPushButton("Пробел")
        sp.setObjectName("spaceBar")
        sp.setMinimumHeight(36)
        sp.clicked.connect(lambda: self.symbol_clicked.emit({
            "id": "space", "unicode_char": " ", "label": " ",
            "description_ru": "Пробел", "description_en": "Space"
        }))
        space_lo.addWidget(sp, 5)
        space_lo.addStretch(2)
        self._kb_lo.addLayout(space_lo)

    def _build_grouped(self):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        content = QWidget()
        clo = QVBoxLayout(content)
        clo.setSpacing(6)
        clo.setContentsMargins(6, 6, 6, 6)

        syms = list(get_symbols(self.current_layer))
        # add custom
        custom = load_custom_symbols()
        for sid, sd in custom.items():
            if sd.get("category") == self.current_layer:
                sd["id"] = sid
                syms.append(sd)

        groups = {}
        for s in syms:
            g = s.get("group", "Другое")
            groups.setdefault(g, []).append(s)

        for gname, gsyms in groups.items():
            header = QLabel(f"  {gname}")
            header.setProperty("class", "groupHeader")
            clo.addWidget(header)

            row = QHBoxLayout()
            row.setSpacing(4)
            for s in gsyms:
                btn = KeyButton(s, "", self)
                btn.setMinimumSize(56, 56)
                btn.setMaximumSize(80, 72)
                btn.symbol_clicked.connect(self.symbol_clicked.emit)
                row.addWidget(btn)
            row.addStretch()
            clo.addLayout(row)

        clo.addStretch()
        scroll.setWidget(content)
        self._kb_lo.addWidget(scroll)

    # ─── public API ───
    def set_layer(self, layer):
        self.current_layer = layer
        for lid, b in self._layer_btns.items():
            b.setProperty("class", "layerBtnActive" if lid == layer else "layerBtn")
            b.style().unpolish(b)
            b.style().polish(b)
            b.update()
        self._populate_keyboard()

    def toggle_layout(self):
        self.layout_mode = "grouped" if self.layout_mode == "qwerty" else "qwerty"
        self._populate_keyboard()

    def handle_physical_key(self, key_char, shift=False):
        km = get_key_map(self.current_layer)
        sid = km.get(key_char) or km.get(key_char.lower())
        if sid:
            sd = get_symbol_by_id(sid)
            if sd:
                btn = self._key_buttons.get(key_char) or self._key_buttons.get(key_char.lower())
                if btn:
                    btn.flash()
                self.symbol_clicked.emit(sd)
                return True
        return False

    def _show_extras(self):
        menu = QMenu(self)

        sub_ori = menu.addMenu("Ориентация ладони")
        for s in ORIENTATION_SYMBOLS:
            a = QAction(f"{s['label']}  {s['description_ru']}", self)
            a.triggered.connect(lambda ch, ss=s: self.symbol_clicked.emit(ss))
            sub_ori.addAction(a)

        sub_ha = menu.addMenu("Расположение рук")
        for s in HAND_ARRANGEMENT_SYMBOLS:
            a = QAction(f"{s['label']}  {s['description_ru']}", self)
            a.triggered.connect(lambda ch, ss=s: self.symbol_clicked.emit(ss))
            sub_ha.addAction(a)

        sub_hp = menu.addMenu("Части кисти")
        for s in HAND_PARTS_SYMBOLS:
            a = QAction(f"{s['label']}  {s['description_ru']}", self)
            a.triggered.connect(lambda ch, ss=s: self.symbol_clicked.emit(ss))
            sub_hp.addAction(a)

        sub_sep = menu.addMenu("Разделители")
        for lab, ch, desc in [(",", ",", "Запятая"), ("(", "(", "Скобка ("), (")", ")", "Скобка )"),
                               ("/", "/", "Слэш"), ("◌̄", "\u0304", "Черта сверху")]:
            s = {"id": f"sep_{lab}", "label": lab, "unicode_char": ch, "description_ru": desc}
            a = QAction(f"{lab}  {desc}", self)
            a.triggered.connect(lambda ch2, ss=s: self.symbol_clicked.emit(ss))
            sub_sep.addAction(a)

        sender = self.sender()
        if sender:
            menu.exec_(sender.mapToGlobal(QPoint(0, sender.height())))
        else:
            menu.exec_(self.mapToGlobal(QPoint(100, 50)))