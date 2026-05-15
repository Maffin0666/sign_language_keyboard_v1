"""
Sign Language Notation Keyboard — main entry point.
Run: python main.py
Build: pyinstaller --onefile --windowed --name SignLanguageKeyboard main.py
"""
import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QSplitter,
    QShortcut, QAction, QFileDialog, QMessageBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeySequence, QFont

from theme_manager import ThemeManager
from keyboard_widget import KeyboardWidget
from text_editor import NotationTextEditor
from help_dialog import HelpDialog
from custom_symbol_dialog import CustomSymbolDialog
from config import load_config, save_config, APP_NAME, APP_VERSION


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.cfg = load_config()
        self.theme = ThemeManager(self.cfg.get("theme", "auto"))

        self.setWindowTitle(f"{APP_NAME}  v{APP_VERSION}")
        self.setMinimumSize(920, 640)

        if self.cfg.get("always_on_top", True):
            self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)

        self._build_ui()
        self._build_menu()
        self._build_shortcuts()
        self._apply_theme()

        self.theme.theme_changed.connect(lambda _: self._apply_theme())

        # restore geometry
        g = self.cfg.get("last_window_geometry")
        if g:
            try:
                self.restoreGeometry(bytes.fromhex(g))
            except Exception:
                self.resize(1050, 720)
        else:
            self.resize(1050, 720)

        self.keyboard.set_layer(self.cfg.get("active_layer", "handshape"))
        if self.cfg.get("layout_mode") == "grouped":
            self.keyboard.toggle_layout()

    # ─── UI ───
    def _build_ui(self):
        central = QWidget()
        central.setObjectName("centralWidget")
        self.setCentralWidget(central)

        lo = QVBoxLayout(central)
        lo.setContentsMargins(8, 8, 8, 8)
        lo.setSpacing(6)

        splitter = QSplitter(Qt.Vertical)

        self.editor = NotationTextEditor()
        self.editor.physical_key_pressed.connect(self._on_phys_key)
        splitter.addWidget(self.editor)

        self.keyboard = KeyboardWidget(self.theme)
        self.keyboard.symbol_clicked.connect(self._on_symbol)
        self.keyboard.theme_change_requested.connect(self._cycle_theme)
        self.keyboard.help_requested.connect(self._help)
        self.keyboard.custom_symbols_requested.connect(self._custom)
        splitter.addWidget(self.keyboard)

        splitter.setSizes([180, 460])
        lo.addWidget(splitter)

    def _build_menu(self):
        mb = self.menuBar()

        fm = mb.addMenu("Файл")
        fm.addAction("Сохранить (Ctrl+S)", self.editor.save_to_file, "Ctrl+S")
        fm.addAction("Загрузить…", self._load_file)
        fm.addSeparator()
        fm.addAction("Выход", self.close, "Alt+F4")

        lm = mb.addMenu("Слой")
        lm.addAction("✊ Кистежесты (F2)", lambda: self.keyboard.set_layer("handshape"))
        lm.addAction("📍 Расположение (F3)", lambda: self.keyboard.set_layer("location"))
        lm.addAction("➡ Движения (F4)", lambda: self.keyboard.set_layer("movement"))

        vm = mb.addMenu("Вид")
        vm.addAction("🎨 Тема (F5)", self._cycle_theme)
        vm.addAction("⌨ Раскладка (F6)", self.keyboard.toggle_layout)
        vm.addSeparator()
        self._ontop = QAction("Поверх всех окон", self)
        self._ontop.setCheckable(True)
        self._ontop.setChecked(self.cfg.get("always_on_top", True))
        self._ontop.triggered.connect(self._toggle_ontop)
        vm.addAction(self._ontop)

        tm = mb.addMenu("Инструменты")
        tm.addAction("✏ Пользовательские символы (F7)", self._custom)

        hm = mb.addMenu("Справка")
        hm.addAction("📖 Справка (F1)", self._help)
        hm.addAction("О программе", self._about)

    def _build_shortcuts(self):
        QShortcut(QKeySequence("F1"), self).activated.connect(self._help)
        QShortcut(QKeySequence("F2"), self).activated.connect(lambda: self.keyboard.set_layer("handshape"))
        QShortcut(QKeySequence("F3"), self).activated.connect(lambda: self.keyboard.set_layer("location"))
        QShortcut(QKeySequence("F4"), self).activated.connect(lambda: self.keyboard.set_layer("movement"))
        QShortcut(QKeySequence("F5"), self).activated.connect(self._cycle_theme)
        QShortcut(QKeySequence("F6"), self).activated.connect(self.keyboard.toggle_layout)
        QShortcut(QKeySequence("F7"), self).activated.connect(self._custom)

    # ─── slots ───
    def _on_symbol(self, sd):
        ch = sd.get("unicode_char", sd.get("label", "?"))
        self.editor.insert_notation_symbol(ch)
        self.editor.setFocus()

    def _on_phys_key(self, key, shift):
        self.keyboard.handle_physical_key(key, shift)

    def _cycle_theme(self):
        t = self.theme.cycle()
        self.cfg["theme"] = t
        save_config(self.cfg)
        self._apply_theme()

    def _apply_theme(self):
        self.setStyleSheet(self.theme.stylesheet())

    def _help(self):
        HelpDialog(self, self.theme).exec_()

    def _custom(self):
        CustomSymbolDialog(self, self.theme).exec_()

    def _about(self):
        QMessageBox.about(self, "О программе",
            f"<h2>{APP_NAME}</h2><p>v{APP_VERSION}</p>"
            "<p>Экранная клавиатура нотаций русского жестового языка.</p>"
            "<p>DEZ — форма кисти · TAB — расположение · SIG — движение</p>"
            "<p>Также: ориентация, расположение рук, части кисти, свои символы.</p>"
            "<hr><p>F1–F7 — горячие клавиши</p>")

    def _toggle_ontop(self, checked):
        self.cfg["always_on_top"] = checked
        save_config(self.cfg)
        flags = self.windowFlags()
        if checked:
            flags |= Qt.WindowStaysOnTopHint
        else:
            flags &= ~Qt.WindowStaysOnTopHint
        self.setWindowFlags(flags)
        self.show()

    def _load_file(self):
        p, _ = QFileDialog.getOpenFileName(self, "Загрузить", "", "Text (*.txt);;All (*)")
        if p:
            try:
                with open(p, "r", encoding="utf-8") as f:
                    self.editor.setPlainText(f.read())
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", str(e))

    def closeEvent(self, ev):
        self.cfg["active_layer"] = self.keyboard.current_layer
        self.cfg["layout_mode"] = self.keyboard.layout_mode
        self.cfg["last_window_geometry"] = self.saveGeometry().toHex().data().decode()
        save_config(self.cfg)
        ev.accept()


def main():
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    app.setFont(QFont("Segoe UI", 10))
    app.setStyle("Fusion")

    w = MainWindow()
    w.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()