"""
Theme manager — auto-detect + Light/Dark/HighContrast
"""
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QPalette
from PyQt5.QtCore import QObject, pyqtSignal

try:
    import darkdetect
    HAS_DARKDETECT = True
except ImportError:
    HAS_DARKDETECT = False


class ThemeManager(QObject):
    theme_changed = pyqtSignal(str)

    THEMES = {
        "light": {
            "name": "☀ Светлая",
            "window_bg": "#F0F0F0",
            "panel_bg": "#FFFFFF",
            "key_bg": "#E6E6E6",
            "key_hover": "#D0D0D0",
            "key_pressed": "#B8B8B8",
            "key_active_bg": "#3C8DBC",
            "key_active_text": "#FFFFFF",
            "text": "#1A1A1A",
            "text_dim": "#777777",
            "border": "#C0C0C0",
            "accent": "#2196F3",
            "editor_bg": "#FFFFFF",
            "editor_text": "#1A1A1A",
            "tooltip_bg": "#FFFDE7",
            "tooltip_text": "#333333",
            "tooltip_border": "#E0D860",
            "status_bg": "#E8E8E8",
            "status_text": "#444444",
            "layer_hs": "#DBEAFE",
            "layer_loc": "#D1FAE5",
            "layer_mov": "#FEF3C7",
            "group_header_bg": "#F5F5F5",
            "separator": "#D5D5D5",
        },
        "dark": {
            "name": "🌙 Тёмная",
            "window_bg": "#1E1E1E",
            "panel_bg": "#2B2B2B",
            "key_bg": "#3A3A3A",
            "key_hover": "#4D4D4D",
            "key_pressed": "#606060",
            "key_active_bg": "#1565C0",
            "key_active_text": "#FFFFFF",
            "text": "#E0E0E0",
            "text_dim": "#999999",
            "border": "#555555",
            "accent": "#64B5F6",
            "editor_bg": "#2B2B2B",
            "editor_text": "#E0E0E0",
            "tooltip_bg": "#3A3A3A",
            "tooltip_text": "#E0E0E0",
            "tooltip_border": "#666666",
            "status_bg": "#2B2B2B",
            "status_text": "#BBBBBB",
            "layer_hs": "#1E3A5F",
            "layer_loc": "#1B4332",
            "layer_mov": "#5C3D00",
            "group_header_bg": "#333333",
            "separator": "#444444",
        },
        "high_contrast": {
            "name": "◐ Контрастная",
            "window_bg": "#000000",
            "panel_bg": "#0A0A0A",
            "key_bg": "#1A1A1A",
            "key_hover": "#333333",
            "key_pressed": "#555555",
            "key_active_bg": "#FFD600",
            "key_active_text": "#000000",
            "text": "#FFFFFF",
            "text_dim": "#FFFF00",
            "border": "#FFFF00",
            "accent": "#00FF00",
            "editor_bg": "#0A0A0A",
            "editor_text": "#FFFFFF",
            "tooltip_bg": "#1A1A1A",
            "tooltip_text": "#FFFFFF",
            "tooltip_border": "#FFFF00",
            "status_bg": "#1A1A1A",
            "status_text": "#FFFF00",
            "layer_hs": "#001155",
            "layer_loc": "#004400",
            "layer_mov": "#553300",
            "group_header_bg": "#111111",
            "separator": "#FFFF00",
        },
    }

    def __init__(self, initial="auto"):
        super().__init__()
        self._mode = initial
        self._resolved = self._resolve(initial)

    def _resolve(self, mode):
        if mode == "auto":
            if HAS_DARKDETECT:
                try:
                    t = darkdetect.theme()
                    if t and t.lower() == "dark":
                        return "dark"
                except Exception:
                    pass
            try:
                app = QApplication.instance()
                if app and app.palette().color(QPalette.Window).lightness() < 128:
                    return "dark"
            except Exception:
                pass
            return "light"
        return mode

    @property
    def colors(self):
        return self.THEMES.get(self._resolved, self.THEMES["light"])

    @property
    def current(self):
        return self._resolved

    def set_theme(self, mode):
        self._mode = mode
        old = self._resolved
        self._resolved = self._resolve(mode)
        if old != self._resolved:
            self.theme_changed.emit(self._resolved)

    def cycle(self):
        order = ["light", "dark", "high_contrast"]
        try:
            idx = order.index(self._resolved)
        except ValueError:
            idx = -1
        nxt = order[(idx + 1) % len(order)]
        self.set_theme(nxt)
        return nxt

    def stylesheet(self):
        c = self.colors
        return f"""
        * {{ font-family: "Segoe UI", "Arial", sans-serif; }}

        QMainWindow, QWidget#centralWidget {{
            background-color: {c['window_bg']};
            color: {c['text']};
        }}

        QTextEdit#editor {{
            background-color: {c['editor_bg']};
            color: {c['editor_text']};
            border: 2px solid {c['border']};
            border-radius: 8px;
            padding: 10px;
            font-size: 17px;
            font-family: "Consolas", "Courier New", monospace;
            selection-background-color: {c['accent']};
        }}

        /* --- Toolbar --- */
        QFrame#toolbar {{
            background-color: {c['panel_bg']};
            border: 1px solid {c['border']};
            border-radius: 8px;
        }}

        /* --- Layer buttons --- */
        QPushButton.layerBtn {{
            background-color: {c['key_bg']};
            color: {c['text']};
            border: 2px solid {c['border']};
            border-radius: 6px;
            padding: 6px 14px;
            font-size: 13px;
            font-weight: bold;
            min-height: 32px;
        }}
        QPushButton.layerBtn:hover {{
            background-color: {c['key_hover']};
            border-color: {c['accent']};
        }}
        QPushButton.layerBtnActive {{
            background-color: {c['key_active_bg']};
            color: {c['key_active_text']};
            border: 2px solid {c['accent']};
            border-radius: 6px;
            padding: 6px 14px;
            font-size: 13px;
            font-weight: bold;
            min-height: 32px;
        }}

        /* --- Small toolbar buttons --- */
        QPushButton.toolBtn {{
            background-color: {c['key_bg']};
            color: {c['text']};
            border: 1px solid {c['border']};
            border-radius: 5px;
            padding: 4px 10px;
            font-size: 12px;
            min-height: 28px;
        }}
        QPushButton.toolBtn:hover {{
            background-color: {c['key_hover']};
            border-color: {c['accent']};
        }}

        /* --- Keyboard keys --- */
        QPushButton.keyBtn {{
            background-color: {c['key_bg']};
            color: {c['text']};
            border: 1px solid {c['border']};
            border-radius: 6px;
            font-size: 13px;
            padding: 2px;
        }}
        QPushButton.keyBtn:hover {{
            background-color: {c['key_hover']};
            border-color: {c['accent']};
        }}
        QPushButton.keyBtn:pressed {{
            background-color: {c['key_pressed']};
        }}
        QPushButton.keyBtnEmpty {{
            background-color: {c['panel_bg']};
            color: {c['text_dim']};
            border: 1px dashed {c['border']};
            border-radius: 6px;
            font-size: 11px;
            padding: 2px;
        }}
        QPushButton.keyBtnHighlight {{
            background-color: {c['key_active_bg']};
            color: {c['key_active_text']};
            border: 2px solid {c['accent']};
            border-radius: 6px;
            font-size: 13px;
            font-weight: bold;
            padding: 2px;
        }}

        /* --- Keyboard frame --- */
        QFrame#keyboardFrame {{
            background-color: {c['panel_bg']};
            border: 1px solid {c['border']};
            border-radius: 10px;
        }}

        /* --- Space bar --- */
        QPushButton#spaceBar {{
            background-color: {c['key_bg']};
            color: {c['text']};
            border: 1px solid {c['border']};
            border-radius: 6px;
            font-size: 12px;
            min-height: 34px;
        }}
        QPushButton#spaceBar:hover {{
            background-color: {c['key_hover']};
        }}

        /* --- Status bar --- */
        QLabel#statusLabel {{
            background-color: {c['status_bg']};
            color: {c['status_text']};
            padding: 5px 12px;
            border-radius: 6px;
            font-size: 12px;
        }}

        /* --- Tooltips --- */
        QToolTip {{
            background-color: {c['tooltip_bg']};
            color: {c['tooltip_text']};
            border: 1px solid {c['tooltip_border']};
            padding: 6px 10px;
            font-size: 13px;
            border-radius: 4px;
        }}

        /* --- Scroll areas in grouped view --- */
        QScrollArea {{
            background-color: {c['panel_bg']};
            border: none;
        }}
        QScrollArea > QWidget > QWidget {{
            background-color: {c['panel_bg']};
        }}
        QScrollBar:vertical {{
            background-color: {c['panel_bg']};
            width: 8px;
        }}
        QScrollBar::handle:vertical {{
            background-color: {c['border']};
            border-radius: 4px;
            min-height: 30px;
        }}

        /* --- Group headers --- */
        QLabel.groupHeader {{
            color: {c['text']};
            background-color: {c['group_header_bg']};
            padding: 4px 10px;
            border-radius: 4px;
            font-weight: bold;
            font-size: 12px;
        }}

        /* --- Dialogs --- */
        QDialog {{
            background-color: {c['window_bg']};
            color: {c['text']};
        }}
        QTextBrowser {{
            background-color: {c['editor_bg']};
            color: {c['editor_text']};
            border: 1px solid {c['border']};
            border-radius: 6px;
            padding: 8px;
        }}
        QTabWidget::pane {{
            background-color: {c['panel_bg']};
            border: 1px solid {c['border']};
            border-radius: 4px;
        }}
        QTabBar::tab {{
            background-color: {c['key_bg']};
            color: {c['text']};
            padding: 6px 14px;
            border: 1px solid {c['border']};
            border-bottom: none;
            border-top-left-radius: 4px;
            border-top-right-radius: 4px;
            margin-right: 2px;
        }}
        QTabBar::tab:selected {{
            background-color: {c['key_active_bg']};
            color: {c['key_active_text']};
        }}
        QTabBar::tab:hover {{
            background-color: {c['key_hover']};
        }}
        QGroupBox {{
            color: {c['text']};
            border: 1px solid {c['border']};
            border-radius: 6px;
            margin-top: 14px;
            padding-top: 14px;
            font-weight: bold;
        }}
        QGroupBox::title {{
            color: {c['text']};
            subcontrol-origin: margin;
            left: 10px;
        }}
        QLineEdit, QComboBox {{
            background-color: {c['editor_bg']};
            color: {c['editor_text']};
            border: 1px solid {c['border']};
            border-radius: 4px;
            padding: 5px 8px;
        }}
        QListWidget {{
            background-color: {c['editor_bg']};
            color: {c['editor_text']};
            border: 1px solid {c['border']};
            border-radius: 4px;
        }}
        QListWidget::item:selected {{
            background-color: {c['accent']};
            color: {c['key_active_text']};
        }}
        QPushButton {{
            background-color: {c['key_bg']};
            color: {c['text']};
            border: 1px solid {c['border']};
            border-radius: 5px;
            padding: 6px 14px;
            font-size: 13px;
        }}
        QPushButton:hover {{
            background-color: {c['key_hover']};
        }}
        QMenu {{
            background-color: {c['panel_bg']};
            color: {c['text']};
            border: 1px solid {c['border']};
        }}
        QMenu::item:selected {{
            background-color: {c['accent']};
            color: {c['key_active_text']};
        }}
        QMenuBar {{
            background-color: {c['panel_bg']};
            color: {c['text']};
        }}
        QMenuBar::item:selected {{
            background-color: {c['accent']};
            color: {c['key_active_text']};
        }}
        """