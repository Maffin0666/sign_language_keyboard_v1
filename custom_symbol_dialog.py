"""
Dialog for custom symbols management.
"""
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QFileDialog, QListWidget, QListWidgetItem,
    QGroupBox, QFormLayout, QMessageBox, QComboBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
import os
from config import load_custom_symbols, save_custom_symbols


class CustomSymbolDialog(QDialog):
    def __init__(self, parent=None, theme_mgr=None):
        super().__init__(parent)
        self.theme_mgr = theme_mgr
        self.custom_symbols = load_custom_symbols()
        self.setWindowTitle("Пользовательские символы")
        self.setMinimumSize(650, 500)
        if theme_mgr:
            self.setStyleSheet(theme_mgr.stylesheet())
        self._build()
        self._load_list()

    def _build(self):
        lo = QVBoxLayout(self)
        lo.addWidget(QLabel("Добавляйте свои символы или заменяйте существующие изображениями."))

        content = QHBoxLayout()

        # Left: list
        left = QGroupBox("Символы")
        ll = QVBoxLayout(left)
        self.sym_list = QListWidget()
        self.sym_list.currentItemChanged.connect(self._on_select)
        ll.addWidget(self.sym_list)
        btns = QHBoxLayout()
        b1 = QPushButton("➕ Новый")
        b1.clicked.connect(self._new)
        b2 = QPushButton("🗑 Удалить")
        b2.clicked.connect(self._delete)
        btns.addWidget(b1)
        btns.addWidget(b2)
        ll.addLayout(btns)
        content.addWidget(left, 1)

        # Right: editor
        right = QGroupBox("Редактор")
        rl = QFormLayout(right)
        self.f_id = QLineEdit()
        self.f_id.setPlaceholderText("unique_id")
        rl.addRow("ID:", self.f_id)
        self.f_label = QLineEdit()
        self.f_label.setPlaceholderText("Символ на кнопке")
        rl.addRow("Символ:", self.f_label)
        self.f_unicode = QLineEdit()
        self.f_unicode.setPlaceholderText("Вставляемый символ")
        rl.addRow("Unicode:", self.f_unicode)
        self.f_desc = QLineEdit()
        rl.addRow("Описание:", self.f_desc)
        self.f_cat = QComboBox()
        self.f_cat.addItems(["handshape", "location", "movement"])
        rl.addRow("Категория:", self.f_cat)
        self.f_key = QLineEdit()
        self.f_key.setPlaceholderText("(необязательно)")
        rl.addRow("Клавиша:", self.f_key)

        img_lo = QHBoxLayout()
        self.f_glyph = QLineEdit()
        self.f_glyph.setReadOnly(True)
        img_lo.addWidget(self.f_glyph)
        browse = QPushButton("📁")
        browse.setFixedWidth(36)
        browse.clicked.connect(self._browse)
        img_lo.addWidget(browse)
        rl.addRow("Изображение:", img_lo)

        self.preview = QLabel("—")
        self.preview.setFixedSize(72, 72)
        self.preview.setAlignment(Qt.AlignCenter)
        rl.addRow("Превью:", self.preview)

        save = QPushButton("💾 Сохранить")
        save.clicked.connect(self._save)
        rl.addRow(save)
        content.addWidget(right, 1)

        lo.addLayout(content)
        close = QPushButton("Закрыть")
        close.clicked.connect(self.accept)
        lo.addWidget(close)

    def _load_list(self):
        self.sym_list.clear()
        for sid, sd in self.custom_symbols.items():
            item = QListWidgetItem(f"{sd.get('label','?')} — {sid}")
            item.setData(Qt.UserRole, sid)
            self.sym_list.addItem(item)

    def _on_select(self, cur, prev):
        if not cur:
            return
        sid = cur.data(Qt.UserRole)
        s = self.custom_symbols.get(sid, {})
        self.f_id.setText(sid)
        self.f_label.setText(s.get("label", ""))
        self.f_unicode.setText(s.get("unicode_char", ""))
        self.f_desc.setText(s.get("description_ru", ""))
        idx = self.f_cat.findText(s.get("category", "handshape"))
        if idx >= 0: self.f_cat.setCurrentIndex(idx)
        self.f_key.setText(s.get("key_binding", "") or "")
        g = s.get("custom_glyph", "") or ""
        self.f_glyph.setText(g)
        if g and os.path.exists(g):
            self.preview.setPixmap(QPixmap(g).scaled(72, 72, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else:
            self.preview.setText("—")

    def _new(self):
        self.sym_list.clearSelection()
        for f in (self.f_id, self.f_label, self.f_unicode, self.f_desc, self.f_key, self.f_glyph):
            f.setText("")
        self.preview.setText("—")
        self.f_id.setFocus()

    def _delete(self):
        cur = self.sym_list.currentItem()
        if not cur: return
        sid = cur.data(Qt.UserRole)
        if QMessageBox.question(self, "Удалить?", f"Удалить «{sid}»?") == QMessageBox.Yes:
            self.custom_symbols.pop(sid, None)
            save_custom_symbols(self.custom_symbols)
            self._load_list()

    def _save(self):
        sid = self.f_id.text().strip()
        if not sid:
            QMessageBox.warning(self, "Ошибка", "Укажите ID!")
            return
        self.custom_symbols[sid] = {
            "label": self.f_label.text().strip() or sid,
            "unicode_char": self.f_unicode.text().strip() or self.f_label.text().strip(),
            "description_ru": self.f_desc.text().strip(),
            "description_en": "",
            "category": self.f_cat.currentText(),
            "key_binding": self.f_key.text().strip() or None,
            "custom_glyph": self.f_glyph.text().strip() or None,
            "group": "custom", "accent": "none",
        }
        save_custom_symbols(self.custom_symbols)
        self._load_list()
        QMessageBox.information(self, "OK", f"Символ «{sid}» сохранён.")

    def _browse(self):
        p, _ = QFileDialog.getOpenFileName(self, "Изображение", "", "Images (*.png *.svg *.jpg *.bmp)")
        if p:
            self.f_glyph.setText(p)
            if os.path.exists(p):
                self.preview.setPixmap(QPixmap(p).scaled(72, 72, Qt.KeepAspectRatio, Qt.SmoothTransformation))