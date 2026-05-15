# -*- coding: utf-8 -*-
"""
Менеджер тем: определяет системную тему Windows и позволяет
переключать между светлой, тёмной и системной.
"""

import sys
import ctypes
from enum import Enum

from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtCore import QSettings


class ThemeMode(Enum):
    SYSTEM = "system"
    LIGHT = "light"
    DARK = "dark"
    HIGH_CONTRAST = "high_contrast"


def is_windows_dark_mode():
    """Определяет, включена ли тёмная тема Windows."""
    try:
        import winreg
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize"
        )
        value, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
        winreg.CloseKey(key)
        return value == 0  # 0 = dark, 1 = light
    except Exception:
        return False


class ThemeManager:
    """Управление цветовыми темами клавиатуры."""

    def __init__(self):
        self.current_mode = ThemeMode.SYSTEM
        self._themes = self._build_themes()

    def _build_themes(self):
        return {
            ThemeMode.LIGHT: {
                "name": "Светлая",
                "window_bg": "#F0F0F0",
                "panel_bg": "#FFFFFF",
                "key_bg": "#E8E8E8",
                "key_bg_hover": "#D0D0D0",
                "key_bg_pressed": "#B0B0B0",
                "key_border": "#C0C0C0",
                "key_text": "#1A1A1A",
                "key_label": "#666666",
                "accent": "#0078D4",
                "accent_hover": "#106EBE",
                "accent_text": "#FFFFFF",
                "category_tab_bg": "#E0E0E0",
                "category_tab_active": "#0078D4",
                "category_tab_text": "#333333",
                "category_tab_text_active": "#FFFFFF",
                "text_area_bg": "#FFFFFF",
                "text_area_border": "#CCCCCC",
                "text_area_text": "#1A1A1A",
                "tooltip_bg": "#FFFFDD",
                "tooltip_text": "#333333",
                "status_bar_bg": "#E8E8E8",
                "status_bar_text": "#555555",
                "separator": "#D0D0D0",
                "shadow_color": "rgba(0,0,0,30)",
                "key_special_bg": "#D4E6F1",
                "key_modifier_bg": "#FADBD8",
            },
            ThemeMode.DARK: {
                "name": "Тёмная",
                "window_bg": "#1E1E1E",
                "panel_bg": "#2D2D2D",
                "key_bg": "#3C3C3C",
                "key_bg_hover": "#4A4A4A",
                "key_bg_pressed": "#5A5A5A",
                "key_border": "#555555",
                "key_text": "#E0E0E0",
                "key_label": "#999999",
                "accent": "#4CC2FF",
                "accent_hover": "#3AA8E5",
                "accent_text": "#1A1A1A",
                "category_tab_bg": "#383838",
                "category_tab_active": "#4CC2FF",
                "category_tab_text": "#CCCCCC",
                "category_tab_text_active": "#1A1A1A",
                "text_area_bg": "#2D2D2D",
                "text_area_border": "#555555",
                "text_area_text": "#E0E0E0",
                "tooltip_bg": "#3C3C3C",
                "tooltip_text": "#E0E0E0",
                "status_bar_bg": "#2D2D2D",
                "status_bar_text": "#999999",
                "separator": "#444444",
                "shadow_color": "rgba(0,0,0,80)",
                "key_special_bg": "#2C4A5E",
                "key_modifier_bg": "#5E2C2C",
            },
            ThemeMode.HIGH_CONTRAST: {
                "name": "Контрастная",
                "window_bg": "#000000",
                "panel_bg": "#000000",
                "key_bg": "#1A1A1A",
                "key_bg_hover": "#333333",
                "key_bg_pressed": "#555555",
                "key_border": "#FFFF00",
                "key_text": "#FFFFFF",
                "key_label": "#FFFF00",
                "accent": "#00FF00",
                "accent_hover": "#00CC00",
                "accent_text": "#000000",
                "category_tab_bg": "#1A1A1A",
                "category_tab_active": "#00FF00",
                "category_tab_text": "#FFFFFF",
                "category_tab_text_active": "#000000",
                "text_area_bg": "#000000",
                "text_area_border": "#FFFF00",
                "text_area_text": "#FFFFFF",
                "tooltip_bg": "#1A1A1A",
                "tooltip_text": "#FFFF00",
                "status_bar_bg": "#000000",
                "status_bar_text": "#FFFF00",
                "separator": "#FFFF00",
                "shadow_color": "rgba(255,255,0,30)",
                "key_special_bg": "#003300",
                "key_modifier_bg": "#330000",
            },
        }

    def get_system_theme(self):
        """Возвращает тему, соответствующую системной."""
        if is_windows_dark_mode():
            return ThemeMode.DARK
        return ThemeMode.LIGHT

    def get_current_theme(self):
        """Возвращает словарь текущей темы."""
        if self.current_mode == ThemeMode.SYSTEM:
            actual = self.get_system_theme()
        else:
            actual = self.current_mode
        return self._themes.get(actual, self._themes[ThemeMode.LIGHT])

    def cycle_theme(self):
        """Переключает тему по кругу: System -> Light -> Dark -> HighContrast -> System."""
        order = [ThemeMode.SYSTEM, ThemeMode.LIGHT, ThemeMode.DARK, ThemeMode.HIGH_CONTRAST]
        idx = order.index(self.current_mode) if self.current_mode in order else 0
        self.current_mode = order[(idx + 1) % len(order)]
        return self.current_mode

    def set_theme(self, mode: ThemeMode):
        self.current_mode = mode

    def get_mode_name(self):
        names = {
            ThemeMode.SYSTEM: "Системная",
            ThemeMode.LIGHT: "Светлая",
            ThemeMode.DARK: "Тёмная",
            ThemeMode.HIGH_CONTRAST: "Контрастная",
        }
        return names.get(self.current_mode, "Неизвестно")

    def generate_stylesheet(self):
        """Генерирует полный QSS стиль для приложения."""
        t = self.get_current_theme()
        return f"""
        /* Главное окно */
        QMainWindow {{
            background-color: {t['window_bg']};
        }}

        QWidget#centralWidget {{
            background-color: {t['window_bg']};
        }}

        /* Область текста */
        QTextEdit {{
            background-color: {t['text_area_bg']};
            color: {t['text_area_text']};
            border: 2px solid {t['text_area_border']};
            border-radius: 8px;
            padding: 8px;
            font-size: 18px;
            font-family: 'Segoe UI', 'Arial Unicode MS', 'DejaVu Sans';
            selection-background-color: {t['accent']};
            selection-color: {t['accent_text']};
        }}

        QTextEdit:focus {{
            border-color: {t['accent']};
        }}

        /* Панель категорий */
        QWidget#categoryPanel {{
            background-color: {t['panel_bg']};
            border-radius: 8px;
        }}

        /* Кнопки категорий */
        QPushButton#categoryBtn {{
            background-color: {t['category_tab_bg']};
            color: {t['category_tab_text']};
            border: none;
            border-radius: 6px;
            padding: 8px 16px;
            font-size: 13px;
            font-weight: bold;
            margin: 2px;
        }}

        QPushButton#categoryBtn:hover {{
            background-color: {t['accent']};
            color: {t['accent_text']};
        }}

        QPushButton#categoryBtn:checked {{
            background-color: {t['category_tab_active']};
            color: {t['category_tab_text_active']};
        }}

        /* Кнопки клавиатуры */
        QPushButton#keyBtn {{
            background-color: {t['key_bg']};
            color: {t['key_text']};
            border: 1px solid {t['key_border']};
            border-radius: 8px;
            padding: 4px;
            font-size: 20px;
            font-family: 'Segoe UI Symbol', 'Arial Unicode MS', 'DejaVu Sans';
            min-width: 50px;
            min-height: 50px;
        }}

        QPushButton#keyBtn:hover {{
            background-color: {t['key_bg_hover']};
            border-color: {t['accent']};
        }}

        QPushButton#keyBtn:pressed {{
            background-color: {t['key_bg_pressed']};
        }}

        /* Специальные кнопки */
        QPushButton#specialKeyBtn {{
            background-color: {t['key_special_bg']};
            color: {t['key_text']};
            border: 1px solid {t['key_border']};
            border-radius: 8px;
            padding: 4px 12px;
            font-size: 12px;
            font-weight: bold;
            min-height: 50px;
        }}

        QPushButton#specialKeyBtn:hover {{
            background-color: {t['accent']};
            color: {t['accent_text']};
        }}

        /* Модификаторы */
        QPushButton#modifierBtn {{
            background-color: {t['key_modifier_bg']};
            color: {t['key_text']};
            border: 1px solid {t['key_border']};
            border-radius: 8px;
            padding: 4px;
            font-size: 14px;
            min-width: 50px;
            min-height: 50px;
        }}

        QPushButton#modifierBtn:hover {{
            background-color: {t['accent']};
            color: {t['accent_text']};
        }}

        /* Статус бар */
        QStatusBar {{
            background-color: {t['status_bar_bg']};
            color: {t['status_bar_text']};
            font-size: 12px;
        }}

        /* Тултипы */
        QToolTip {{
            background-color: {t['tooltip_bg']};
            color: {t['tooltip_text']};
            border: 1px solid {t['key_border']};
            border-radius: 4px;
            padding: 4px 8px;
            font-size: 13px;
        }}

        /* Метки */
        QLabel {{
            color: {t['key_text']};
        }}

        QLabel#sectionLabel {{
            color: {t['key_label']};
            font-size: 12px;
            font-style: italic;
            padding: 4px 0px;
        }}

        /* Разделитель */
        QFrame#separator {{
            background-color: {t['separator']};
            max-height: 1px;
        }}

        /* Скроллбар */
        QScrollArea {{
            border: none;
            background-color: transparent;
        }}

        QScrollBar:vertical {{
            background-color: {t['panel_bg']};
            width: 10px;
            border-radius: 5px;
        }}

        QScrollBar::handle:vertical {{
            background-color: {t['key_border']};
            border-radius: 5px;
            min-height: 30px;
        }}

        QScrollBar::handle:vertical:hover {{
            background-color: {t['accent']};
        }}

        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
            height: 0px;
        }}

        QScrollBar:horizontal {{
            background-color: {t['panel_bg']};
            height: 10px;
            border-radius: 5px;
        }}

        QScrollBar::handle:horizontal {{
            background-color: {t['key_border']};
            border-radius: 5px;
            min-width: 30px;
        }}

        QScrollBar::handle:horizontal:hover {{
            background-color: {t['accent']};
        }}

        QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
            width: 0px;
        }}

        /* Меню */
        QMenuBar {{
            background-color: {t['panel_bg']};
            color: {t['key_text']};
        }}

        QMenuBar::item:selected {{
            background-color: {t['accent']};
            color: {t['accent_text']};
        }}

        QMenu {{
            background-color: {t['panel_bg']};
            color: {t['key_text']};
            border: 1px solid {t['key_border']};
        }}

        QMenu::item:selected {{
            background-color: {t['accent']};
            color: {t['accent_text']};
        }}
        """