"""
Text editor with notation mode — intercepts physical keys.
"""
from PyQt5.QtWidgets import QTextEdit, QFileDialog, QMessageBox
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QKeyEvent


class NotationTextEditor(QTextEdit):
    physical_key_pressed = pyqtSignal(str, bool)  # char, shift

    NOTATION_CHARS = set("`1234567890-=qwertyuiop[]\\asdfghjkl;'zxcvbnm,./")

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("editor")
        self.setFont(QFont("Consolas", 17))
        self.setPlaceholderText(
            "Нажимайте клавиши или кнопки экранной клавиатуры для ввода символов нотации.\n"
            "F2 — Кистежесты  |  F3 — Расположение  |  F4 — Движения"
        )
        self.setAcceptRichText(False)
        self.setMinimumHeight(80)
        self._notation_mode = True

    @property
    def notation_mode(self):
        return self._notation_mode

    @notation_mode.setter
    def notation_mode(self, v):
        self._notation_mode = v

    def keyPressEvent(self, event: QKeyEvent):
        key = event.key()
        mod = event.modifiers()
        text = event.text()

        # Ctrl combos — pass through
        if mod & Qt.ControlModifier:
            if key == Qt.Key_S:
                self.save_to_file()
                return
            super().keyPressEvent(event)
            return

        # Function keys — ignore (handled by main window shortcuts)
        if Qt.Key_F1 <= key <= Qt.Key_F12:
            event.ignore()
            return

        # Navigation / editing keys — pass through
        if key in (Qt.Key_Left, Qt.Key_Right, Qt.Key_Up, Qt.Key_Down,
                   Qt.Key_Home, Qt.Key_End, Qt.Key_PageUp, Qt.Key_PageDown,
                   Qt.Key_Backspace, Qt.Key_Delete, Qt.Key_Return, Qt.Key_Enter):
            super().keyPressEvent(event)
            return

        if key == Qt.Key_Space:
            super().keyPressEvent(event)
            return

        if key == Qt.Key_Tab:
            self.insertPlainText("  ")
            return

        if key == Qt.Key_Escape:
            c = self.textCursor()
            c.clearSelection()
            self.setTextCursor(c)
            return

        # Notation mode — intercept
        if self._notation_mode and text:
            lower = text.lower() if text else ""
            if lower in self.NOTATION_CHARS:
                shift = bool(mod & Qt.ShiftModifier)
                self.physical_key_pressed.emit(lower, shift)
                return

        super().keyPressEvent(event)

    def insert_notation_symbol(self, sym_text):
        c = self.textCursor()
        c.insertText(sym_text)
        self.setTextCursor(c)

    def save_to_file(self):
        path, _ = QFileDialog.getSaveFileName(self, "Сохранить", "", "Text (*.txt);;All (*)")
        if path:
            try:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(self.toPlainText())
                QMessageBox.information(self, "Готово", f"Сохранено: {path}")
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", str(e))