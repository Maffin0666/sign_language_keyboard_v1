# -*- coding: utf-8 -*-
"""
Экранная клавиатура нотаций русского жестового языка (РЖЯ).

Главный файл приложения.
Запуск: python main.py
Сборка: pyinstaller --onefile --windowed --name SignKeyboard main.py

Поддержка:
- Ввод мышью (клик по клавише)
- Ввод с физической клавиатуры
- Переключение категорий: Ctrl+1..6 или кнопки
- Переключение темы: Ctrl+T
- Копирование: Ctrl+C
- Очистка: Ctrl+Delete
"""

import sys
import os
import ctypes

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QGridLayout, QPushButton, QTextEdit, QLabel, QScrollArea,
    QFrame, QStatusBar, QToolTip, QSizePolicy, QAction, QMenuBar,
    QMenu, QMessageBox, QShortcut, QButtonGroup, QSplitter,
    QGraphicsDropShadowEffect
)
from PyQt5.QtCore import (
    Qt, QSize, QTimer, QEvent, pyqtSignal, QPropertyAnimation,
    QEasingCurve, QRect
)
from PyQt5.QtGui import (
    QFont, QIcon, QPixmap, QPainter, QColor, QKeySequence,
    QFontDatabase, QPalette, QCursor, QTextCursor
)

from keyboard_data import (
    ALL_CATEGORIES, CATEGORY_ORDER, TAB_SYMBOLS, DEZ_SYMBOLS,
    SIG_SYMBOLS, ORI_SYMBOLS, HA_SYMBOLS, FINGER_SYMBOLS,
    NOTATION_FORMULAS, EXAMPLES
)
from theme_manager import ThemeManager, ThemeMode
from custom_font import SymbolRenderer, get_symbol_pixmap

# Для корректного DPI на Windows
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    pass


class KeyButton(QPushButton):
    """Кнопка-клавиша экранной клавиатуры."""

    symbol_clicked = pyqtSignal(str, str)  # symbol, description

    def __init__(self, symbol: str, description: str = "",
                 hotkey: str = "", parent=None):
        super().__init__(parent)
        self.symbol = symbol
        self.description = description
        self.hotkey = hotkey
        self._setup_ui()

    def _setup_ui(self):
        self.setObjectName("keyBtn")
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setMinimumSize(52, 56)
        self.setMaximumSize(120, 100)
        self.setCursor(QCursor(Qt.PointingHandCursor))

        # Тултип с описанием
        tooltip_text = f"<b>{self.symbol}</b>"
        if self.description:
            tooltip_text += f"<br>{self.description}"
        if self.hotkey:
            tooltip_text += f"<br><i>Клавиша: {self.hotkey}</i>"
        self.setToolTip(tooltip_text)

        # Текст кнопки
        self.setText(self.symbol)

        # Подключение клика
        self.clicked.connect(self._on_clicked)

    def _on_clicked(self):
        self.symbol_clicked.emit(self.symbol, self.description)
        # Анимация нажатия (визуальная обратная связь)
        self._flash()

    def _flash(self):
        """Визуальная обратная связь при нажатии."""
        original_style = self.styleSheet()
        self.setStyleSheet(original_style + "background-color: rgba(0,120,212,0.3);")
        QTimer.singleShot(150, lambda: self.setStyleSheet(original_style))

    def update_symbol_display(self, theme_colors: dict):
        """Обновляет отображение символа с учётом темы."""
        color = theme_colors.get('key_text', '#000000')

        # Проверяем, нужен ли кастомный рендеринг
        if self.symbol in SymbolRenderer.CUSTOM_RENDERERS:
            pixmap = get_symbol_pixmap(self.symbol, 32, color)
            icon = QIcon(pixmap)
            self.setIcon(icon)
            self.setIconSize(QSize(32, 32))
            self.setText("")
        else:
            self.setIcon(QIcon())
            self.setText(self.symbol)


class SpecialKeyButton(QPushButton):
    """Специальная кнопка (управление, модификаторы и т.д.)."""

    def __init__(self, text: str, tooltip: str = "", parent=None):
        super().__init__(text, parent)
        self.setObjectName("specialKeyBtn")
        self.setCursor(QCursor(Qt.PointingHandCursor))
        if tooltip:
            self.setToolTip(tooltip)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setMinimumHeight(45)


class CategoryButton(QPushButton):
    """Кнопка переключения категории символов."""

    def __init__(self, text: str, category_id: str, parent=None):
        super().__init__(text, parent)
        self.category_id = category_id
        self.setObjectName("categoryBtn")
        self.setCheckable(True)
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.setMinimumHeight(36)


class TextOutputArea(QTextEdit):
    """Область вывода текста нотаций."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(80)
        self.setMaximumHeight(150)
        self.setPlaceholderText(
            "Здесь отображается запись нотации жестов... "
            "Кликайте по клавишам или нажимайте на физической клавиатуре."
        )
        font = QFont("Segoe UI Symbol", 16)
        font.setStyleStrategy(QFont.PreferAntialias)
        self.setFont(font)
        self.setAcceptRichText(False)


class SignLanguageKeyboard(QMainWindow):
    """Главное окно экранной клавиатуры."""

    def __init__(self):
        super().__init__()
        self.theme_manager = ThemeManager()
        self.current_category = "TAB"
        self.key_buttons = []  # все кнопки текущей категории
        self.hotkey_map = {}  # маппинг физических клавиш на символы

        self._init_ui()
        self._apply_theme()
        self._setup_shortcuts()

        # Таймер для отслеживания смены системной темы
        self.theme_check_timer = QTimer()
        self.theme_check_timer.timeout.connect(self._check_system_theme)
        self.theme_check_timer.start(5000)  # проверяем каждые 5 секунд
        self._last_system_dark = None

    def _init_ui(self):
        """Инициализация интерфейса."""
        self.setWindowTitle("Клавиатура нотаций РЖЯ — Sign Language Notation Keyboard")
        self.setMinimumSize(900, 600)
        self.resize(1100, 720)

        # Устанавливаем иконку (простой значок руки)
        self._set_window_icon()

        # Центральный виджет
        central = QWidget()
        central.setObjectName("centralWidget")
        self.setCentralWidget(central)

        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(12, 8, 12, 8)
        main_layout.setSpacing(8)

        # === 1. Меню ===
        self._create_menu_bar()

        # === 2. Текстовая область вывода ===
        self.text_output = TextOutputArea()
        main_layout.addWidget(self.text_output)

        # === 3. Панель информации о текущей категории ===
        info_layout = QHBoxLayout()
        self.category_info_label = QLabel()
        self.category_info_label.setObjectName("sectionLabel")
        info_layout.addWidget(self.category_info_label)
        info_layout.addStretch()

        self.theme_label = QLabel()
        self.theme_label.setObjectName("sectionLabel")
        info_layout.addWidget(self.theme_label)
        main_layout.addLayout(info_layout)

        # === 4. Панель категорий ===
        category_panel = QWidget()
        category_panel.setObjectName("categoryPanel")
        cat_layout = QHBoxLayout(category_panel)
        cat_layout.setContentsMargins(4, 4, 4, 4)
        cat_layout.setSpacing(4)

        self.category_group = QButtonGroup(self)
        self.category_group.setExclusive(True)
        self.category_buttons = {}

        category_names = {
            "TAB": "TAB\nМесто",
            "DEZ": "DEZ\nФорма кисти",
            "SIG": "SIG\nДвижение",
            "ORI": "ORI\nОриентация",
            "HA": "HA\nРасположение",
            "FINGER": "Части\nкисти",
        }

        for i, cat_id in enumerate(CATEGORY_ORDER):
            btn = CategoryButton(category_names.get(cat_id, cat_id), cat_id)
            btn.setToolTip(f"Переключить на {ALL_CATEGORIES[cat_id]['label']} (Ctrl+{i + 1})")
            btn.clicked.connect(lambda checked, cid=cat_id: self._switch_category(cid))
            self.category_group.addButton(btn)
            self.category_buttons[cat_id] = btn
            cat_layout.addWidget(btn)

        # Кнопка темы
        self.theme_btn = SpecialKeyButton("🎨", "Переключить тему (Ctrl+T)")
        self.theme_btn.setMaximumWidth(60)
        self.theme_btn.clicked.connect(self._cycle_theme)
        cat_layout.addWidget(self.theme_btn)

        main_layout.addWidget(category_panel)

        # === 5. Область клавиатуры (со скроллом) ===
        self.keyboard_scroll = QScrollArea()
        self.keyboard_scroll.setWidgetResizable(True)
        self.keyboard_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.keyboard_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        self.keyboard_container = QWidget()
        self.keyboard_layout = QVBoxLayout(self.keyboard_container)
        self.keyboard_layout.setContentsMargins(4, 4, 4, 4)
        self.keyboard_layout.setSpacing(6)

        self.keyboard_scroll.setWidget(self.keyboard_container)
        main_layout.addWidget(self.keyboard_scroll, stretch=1)

        # === 6. Панель управления внизу ===
        control_layout = QHBoxLayout()
        control_layout.setSpacing(6)

        # Кнопка Пробел
        space_btn = SpecialKeyButton("Пробел", "Вставить пробел (Space)")
        space_btn.clicked.connect(lambda: self._insert_symbol(" ", "Пробел"))
        control_layout.addWidget(space_btn, stretch=3)

        # Разделитель нотации
        sep_btn = SpecialKeyButton(" , ", "Разделитель записи (запятая)")
        sep_btn.clicked.connect(lambda: self._insert_symbol(" , ", "Разделитель"))
        control_layout.addWidget(sep_btn, stretch=1)

        # Backspace
        back_btn = SpecialKeyButton("⌫ Удалить", "Удалить последний символ (Backspace)")
        back_btn.clicked.connect(self._backspace)
        control_layout.addWidget(back_btn, stretch=1)

        # Очистить
        clear_btn = SpecialKeyButton("Очистить", "Очистить всё (Ctrl+Delete)")
        clear_btn.clicked.connect(self._clear_all)
        control_layout.addWidget(clear_btn, stretch=1)

        # Копировать
        copy_btn = SpecialKeyButton("📋 Копировать", "Копировать в буфер обмена (Ctrl+C)")
        copy_btn.clicked.connect(self._copy_to_clipboard)
        control_layout.addWidget(copy_btn, stretch=1)

        # Новая строка
        newline_btn = SpecialKeyButton("↵", "Новая строка (Enter)")
        newline_btn.clicked.connect(lambda: self._insert_symbol("\n", "Новая строка"))
        newline_btn.setMaximumWidth(60)
        control_layout.addWidget(newline_btn)

        main_layout.addLayout(control_layout)

        # === 7. Статус бар ===
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Готово. Выберите категорию и нажимайте символы.")

        # Инициализация первой категории
        self.category_buttons["TAB"].setChecked(True)
        self._switch_category("TAB")

    def _set_window_icon(self):
        """Создаёт программную иконку окна."""
        pixmap = QPixmap(64, 64)
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)

        # Рисуем стилизованную руку
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor("#0078D4"))
        painter.drawRoundedRect(4, 4, 56, 56, 12, 12)

        painter.setPen(QColor("white"))
        font = QFont("Segoe UI", 28, QFont.Bold)
        painter.setFont(font)
        painter.drawText(QRect(4, 4, 56, 56), Qt.AlignCenter, "✋")

        painter.end()
        self.setWindowIcon(QIcon(pixmap))

    def _create_menu_bar(self):
        """Создаёт строку меню."""
        menubar = self.menuBar()

        # Файл
        file_menu = menubar.addMenu("Файл")

        copy_action = QAction("Копировать текст", self)
        copy_action.setShortcut("Ctrl+C")
        copy_action.triggered.connect(self._copy_to_clipboard)
        file_menu.addAction(copy_action)

        clear_action = QAction("Очистить", self)
        clear_action.setShortcut("Ctrl+Delete")
        clear_action.triggered.connect(self._clear_all)
        file_menu.addAction(clear_action)

        file_menu.addSeparator()

        exit_action = QAction("Выход", self)
        exit_action.setShortcut("Alt+F4")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Вид
        view_menu = menubar.addMenu("Вид")

        theme_action = QAction("Сменить тему (Ctrl+T)", self)
        theme_action.triggered.connect(self._cycle_theme)
        view_menu.addAction(theme_action)

        view_menu.addSeparator()

        for mode in [ThemeMode.SYSTEM, ThemeMode.LIGHT, ThemeMode.DARK, ThemeMode.HIGH_CONTRAST]:
            names = {
                ThemeMode.SYSTEM: "Системная тема",
                ThemeMode.LIGHT: "Светлая тема",
                ThemeMode.DARK: "Тёмная тема",
                ThemeMode.HIGH_CONTRAST: "Контрастная тема",
            }
            action = QAction(names[mode], self)
            action.triggered.connect(lambda checked, m=mode: self._set_specific_theme(m))
            view_menu.addAction(action)

        # Категории
        cat_menu = menubar.addMenu("Категории")

        cat_names = {
            "TAB": "TAB — Место (Ctrl+1)",
            "DEZ": "DEZ — Форма кисти (Ctrl+2)",
            "SIG": "SIG — Движение (Ctrl+3)",
            "ORI": "ORI — Ориентация (Ctrl+4)",
            "HA": "HA — Расположение (Ctrl+5)",
            "FINGER": "Части кисти (Ctrl+6)",
        }

        for cat_id in CATEGORY_ORDER:
            action = QAction(cat_names.get(cat_id, cat_id), self)
            action.triggered.connect(lambda checked, c=cat_id: self._switch_category(c))
            cat_menu.addAction(action)

        # Справка
        help_menu = menubar.addMenu("Справка")

        notation_help = QAction("О нотации жестов", self)
        notation_help.triggered.connect(self._show_notation_help)
        help_menu.addAction(notation_help)

        examples_action = QAction("Примеры записей", self)
        examples_action.triggered.connect(self._show_examples)
        help_menu.addAction(examples_action)

        help_menu.addSeparator()

        about_action = QAction("О программе", self)
        about_action.triggered.connect(self._show_about)
        help_menu.addAction(about_action)

    def _setup_shortcuts(self):
        """Настраивает горячие клавиши."""
        # Переключение категорий: Ctrl+1..6
        for i, cat_id in enumerate(CATEGORY_ORDER):
            shortcut = QShortcut(QKeySequence(f"Ctrl+{i + 1}"), self)
            shortcut.activated.connect(lambda c=cat_id: self._switch_category(c))

        # Переключение темы
        theme_shortcut = QShortcut(QKeySequence("Ctrl+T"), self)
        theme_shortcut.activated.connect(self._cycle_theme)

        # Предыдущая/следующая категория
        prev_cat = QShortcut(QKeySequence("Ctrl+Left"), self)
        prev_cat.activated.connect(self._prev_category)

        next_cat = QShortcut(QKeySequence("Ctrl+Right"), self)
        next_cat.activated.connect(self._next_category)

    def _switch_category(self, category_id: str):
        """Переключает отображаемую категорию символов."""
        if category_id not in ALL_CATEGORIES:
            return

        self.current_category = category_id

        # Обновляем кнопки категорий
        for cid, btn in self.category_buttons.items():
            btn.setChecked(cid == category_id)

        # Обновляем информацию
        cat_data = ALL_CATEGORIES[category_id]
        self.category_info_label.setText(
            f"📌 {cat_data['label']} — {cat_data['description']}"
        )

        # Перестраиваем клавиатуру
        self._build_keyboard(category_id)

        # Обновляем маппинг клавиш
        self._update_hotkey_map(category_id)

        self.status_bar.showMessage(
            f"Категория: {cat_data['label']}. "
            f"Нажимайте клавиши или кликайте мышью."
        )

    def _prev_category(self):
        """Предыдущая категория."""
        idx = CATEGORY_ORDER.index(self.current_category)
        new_idx = (idx - 1) % len(CATEGORY_ORDER)
        self._switch_category(CATEGORY_ORDER[new_idx])

    def _next_category(self):
        """Следующая категория."""
        idx = CATEGORY_ORDER.index(self.current_category)
        new_idx = (idx + 1) % len(CATEGORY_ORDER)
        self._switch_category(CATEGORY_ORDER[new_idx])

    def _build_keyboard(self, category_id: str):
        """Строит раскладку клавиатуры для данной категории."""
        # Очищаем старые кнопки
        self.key_buttons.clear()

        # Удаляем все виджеты из layout
        while self.keyboard_layout.count():
            item = self.keyboard_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                self._clear_layout(item.layout())

        cat_data = ALL_CATEGORIES[category_id]
        groups = cat_data.get("groups", {})
        theme = self.theme_manager.get_current_theme()

        if category_id == "DEZ":
            # DEZ имеет вложенную структуру с вариантами
            self._build_dez_keyboard(groups, theme)
        else:
            # Стандартная структура: группы с символами
            self._build_standard_keyboard(groups, theme)

        # Добавляем растяжение в конец
        self.keyboard_layout.addStretch()

    def _build_standard_keyboard(self, groups: dict, theme: dict):
        """Строит стандартную раскладку клавиатуры (TAB, SIG, ORI, HA, FINGER)."""
        for group_name, symbols in groups.items():
            # Метка группы
            group_label = QLabel(f"  {group_name}")
            group_label.setObjectName("sectionLabel")
            group_label.setFont(QFont("Segoe UI", 11, QFont.Bold))
            self.keyboard_layout.addWidget(group_label)

            # Сетка кнопок
            grid = QGridLayout()
            grid.setSpacing(4)

            col = 0
            row = 0
            max_cols = 10  # максимум кнопок в ряду

            for symbol, sym_data in symbols.items():
                desc = sym_data.get("desc", "")
                key = sym_data.get("key", "")

                btn = KeyButton(symbol, desc, key)
                btn.symbol_clicked.connect(self._on_symbol_clicked)
                btn.update_symbol_display(theme)

                grid.addWidget(btn, row, col)
                self.key_buttons.append(btn)

                col += 1
                if col >= max_cols:
                    col = 0
                    row += 1

            self.keyboard_layout.addLayout(grid)

            # Разделитель
            sep = QFrame()
            sep.setObjectName("separator")
            sep.setFrameShape(QFrame.HLine)
            sep.setFixedHeight(1)
            self.keyboard_layout.addWidget(sep)

    def _build_dez_keyboard(self, groups: dict, theme: dict):
        """Строит раскладку для DEZ (формы кисти) с группами и вариантами."""
        # Сначала показываем акценты/модификаторы
        acc_data = DEZ_SYMBOLS.get("accents", {})
        if acc_data:
            acc_label = QLabel("  Акценты (модификаторы формы кисти)")
            acc_label.setObjectName("sectionLabel")
            acc_label.setFont(QFont("Segoe UI", 11, QFont.Bold))
            self.keyboard_layout.addWidget(acc_label)

            acc_grid = QGridLayout()
            acc_grid.setSpacing(4)
            col = 0
            for acc_id, acc_info in acc_data.items():
                sym = acc_info.get("symbol", "")
                desc = acc_info.get("desc", "")
                display = f"◌{sym}" if sym else "—"

                btn = KeyButton(display, f"Акцент: {desc}")
                btn.symbol_clicked.connect(self._on_accent_clicked)
                btn.update_symbol_display(theme)
                acc_grid.addWidget(btn, 0, col)
                self.key_buttons.append(btn)
                col += 1

            self.keyboard_layout.addLayout(acc_grid)

            sep = QFrame()
            sep.setObjectName("separator")
            sep.setFrameShape(QFrame.HLine)
            sep.setFixedHeight(1)
            self.keyboard_layout.addWidget(sep)

        # Группы кистежестов
        for group_name, group_data in groups.items():
            desc = group_data.get("desc", "")
            variants = group_data.get("variants", {})

            group_label = QLabel(f"  {group_name} — {desc}")
            group_label.setObjectName("sectionLabel")
            group_label.setFont(QFont("Segoe UI", 11, QFont.Bold))
            self.keyboard_layout.addWidget(group_label)

            grid = QGridLayout()
            grid.setSpacing(4)

            col = 0
            row = 0
            max_cols = 10

            for symbol, var_data in variants.items():
                var_desc = var_data.get("desc", "")
                key = var_data.get("key", "")

                btn = KeyButton(symbol, var_desc, key)
                btn.symbol_clicked.connect(self._on_symbol_clicked)
                btn.update_symbol_display(theme)

                grid.addWidget(btn, row, col)
                self.key_buttons.append(btn)

                col += 1
                if col >= max_cols:
                    col = 0
                    row += 1

            self.keyboard_layout.addLayout(grid)

            sep = QFrame()
            sep.setObjectName("separator")
            sep.setFrameShape(QFrame.HLine)
            sep.setFixedHeight(1)
            self.keyboard_layout.addWidget(sep)

    def _update_hotkey_map(self, category_id: str):
        """Обновляет маппинг физических клавиш на символы текущей категории."""
        self.hotkey_map.clear()

        cat_data = ALL_CATEGORIES[category_id]
        groups = cat_data.get("groups", {})

        if category_id == "DEZ":
            for group_name, group_data in groups.items():
                variants = group_data.get("variants", {})
                for symbol, var_data in variants.items():
                    key = var_data.get("key", "")
                    if key:
                        self.hotkey_map[key.lower()] = (symbol, var_data.get("desc", ""))
        else:
            for group_name, symbols in groups.items():
                for symbol, sym_data in symbols.items():
                    key = sym_data.get("key", "")
                    if key:
                        self.hotkey_map[key.lower()] = (symbol, sym_data.get("desc", ""))

    def _on_symbol_clicked(self, symbol: str, description: str):
        """Обработчик клика по символу."""
        self._insert_symbol(symbol, description)

    def _on_accent_clicked(self, symbol: str, description: str):
        """Обработчик клика по акценту — добавляет к последнему символу."""
        # Убираем маркер "◌"
        accent = symbol.replace("◌", "").strip()
        if accent == "—":
            return

        cursor = self.text_output.textCursor()
        # Вставляем акцент (комбинирующий символ)
        cursor.insertText(accent)
        self.text_output.setTextCursor(cursor)
        self.status_bar.showMessage(f"Добавлен акцент: {description}", 3000)

    def _insert_symbol(self, symbol: str, description: str = ""):
        """Вставляет символ в текстовую область."""
        cursor = self.text_output.textCursor()
        cursor.insertText(symbol)
        self.text_output.setTextCursor(cursor)
        self.text_output.ensureCursorVisible()

        if description:
            self.status_bar.showMessage(f"Вставлен: {symbol} — {description}", 3000)

    def _backspace(self):
        """Удаляет последний символ."""
        cursor = self.text_output.textCursor()
        if not cursor.atStart():
            cursor.deletePreviousChar()
            self.text_output.setTextCursor(cursor)

    def _clear_all(self):
        """Очищает текстовое поле."""
        self.text_output.clear()
        self.status_bar.showMessage("Текст очищен.", 2000)

    def _copy_to_clipboard(self):
        """Копирует текст в буфер обмена."""
        text = self.text_output.toPlainText()
        if text:
            clipboard = QApplication.clipboard()
            clipboard.setText(text)
            self.status_bar.showMessage("Текст скопирован в буфер обмена!", 3000)
        else:
            self.status_bar.showMessage("Нечего копировать.", 2000)

    def _cycle_theme(self):
        """Переключает тему по кругу."""
        self.theme_manager.cycle_theme()
        self._apply_theme()
        mode_name = self.theme_manager.get_mode_name()
        self.status_bar.showMessage(f"Тема: {mode_name}", 3000)

    def _set_specific_theme(self, mode: ThemeMode):
        """Устанавливает конкретную тему."""
        self.theme_manager.set_theme(mode)
        self._apply_theme()
        mode_name = self.theme_manager.get_mode_name()
        self.status_bar.showMessage(f"Тема: {mode_name}", 3000)

    def _apply_theme(self):
        """Применяет текущую тему ко всему приложению."""
        stylesheet = self.theme_manager.generate_stylesheet()
        self.setStyleSheet(stylesheet)

        # Обновляем метку темы
        mode_name = self.theme_manager.get_mode_name()
        theme = self.theme_manager.get_current_theme()
        theme_display_name = theme.get("name", mode_name)
        self.theme_label.setText(f"🎨 Тема: {mode_name} ({theme_display_name})")

        # Обновляем символы на кнопках
        for btn in self.key_buttons:
            btn.update_symbol_display(theme)

    def _check_system_theme(self):
        """Проверяет, изменилась ли системная тема Windows."""
        if self.theme_manager.current_mode != ThemeMode.SYSTEM:
            return

        from theme_manager import is_windows_dark_mode
        current_dark = is_windows_dark_mode()

        if self._last_system_dark is not None and current_dark != self._last_system_dark:
            self._apply_theme()

        self._last_system_dark = current_dark

    def _clear_layout(self, layout):
        """Рекурсивно очищает layout."""
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                self._clear_layout(item.layout())

    def keyPressEvent(self, event):
        """Обработка нажатий с физической клавиатуры."""
        # Получаем текст нажатой клавиши
        key_text = event.text().lower()
        key_code = event.key()
        modifiers = event.modifiers()

        # Пропускаем, если нажаты модификаторы (Ctrl, Alt и т.д.)
        if modifiers & Qt.ControlModifier:
            super().keyPressEvent(event)
            return

        if modifiers & Qt.AltModifier:
            super().keyPressEvent(event)
            return

        # Обработка специальных клавиш
        if key_code == Qt.Key_Space:
            self._insert_symbol(" ", "Пробел")
            return
        elif key_code == Qt.Key_Return or key_code == Qt.Key_Enter:
            self._insert_symbol("\n", "Новая строка")
            return
        elif key_code == Qt.Key_Backspace:
            self._backspace()
            return
        elif key_code == Qt.Key_Delete:
            self._backspace()
            return

        # Функциональные клавиши
        fkey_map = {
            Qt.Key_F1: "f1", Qt.Key_F2: "f2", Qt.Key_F3: "f3",
            Qt.Key_F4: "f4", Qt.Key_F5: "f5", Qt.Key_F6: "f6",
            Qt.Key_F7: "f7", Qt.Key_F8: "f8", Qt.Key_F9: "f9",
            Qt.Key_F10: "f10", Qt.Key_F11: "f11", Qt.Key_F12: "f12",
        }

        if key_code in fkey_map:
            key_text = fkey_map[key_code]

        # Ищем в маппинге
        if key_text in self.hotkey_map:
            symbol, desc = self.hotkey_map[key_text]
            self._insert_symbol(symbol, desc)

            # Подсвечиваем соответствующую кнопку
            for btn in self.key_buttons:
                if btn.symbol == symbol:
                    btn._flash()
                    break
            return

        # Если не нашли в маппинге, передаём дальше
        super().keyPressEvent(event)

    def _show_notation_help(self):
        """Показывает справку о системе нотации."""
        help_text = """
<h2>Система нотации русского жестового языка</h2>

<p>Нотация использует символы для записи жестов по нескольким параметрам:</p>

<h3>Основные компоненты записи:</h3>
<ul>
<li><b>TAB</b> (место) — где на теле производится жест</li>
<li><b>DEZ</b> (форма кисти) — какую форму принимает рука (57 кистежестов в 22 группах)</li>
<li><b>ORI</b> (ориентация) — куда направлена ладонь и пальцы</li>
<li><b>SIG</b> (движение) — какое движение производится</li>
<li><b>HA</b> (расположение) — как кисти расположены друг относительно друга</li>
</ul>

<h3>Формулы записи:</h3>
<ol>
<li><b>Одноручные жесты:</b> tab — dez — ori — sig</li>
<li><b>Двуручные tab-жесты:</b> tab — dez — ori — (ha) — dez — ori — sig</li>
<li><b>Сдвоенные dez-жесты:</b> tab — dez — ori — (ha) — dez — ori — sig (обе руки двигаются)</li>
</ol>

<h3>Модификаторы DEZ:</h3>
<p>Каждая группа кистежестов может иметь модификаторы:</p>
<ul>
<li>Без акцента — базовая форма</li>
<li>Точка (·) — 1-я модификация</li>
<li>Крышечка (^) — 2-я модификация</li>
<li>Черта (=) — 3-я модификация</li>
<li>И т.д.</li>
</ul>

<h3>Горячие клавиши:</h3>
<ul>
<li><b>Ctrl+1..6</b> — переключение категорий</li>
<li><b>Ctrl+←/→</b> — предыдущая/следующая категория</li>
<li><b>Ctrl+T</b> — сменить тему</li>
<li><b>Ctrl+C</b> — копировать текст</li>
<li><b>Ctrl+Delete</b> — очистить</li>
</ul>
"""
        msg = QMessageBox(self)
        msg.setWindowTitle("Справка: Нотация жестового языка")
        msg.setTextFormat(Qt.RichText)
        msg.setText(help_text)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    def _show_examples(self):
        """Показывает примеры записей жестов."""
        examples_text = "<h2>Примеры записей жестов</h2><table border='1' cellpadding='8'>"
        examples_text += "<tr><th>Нотация</th><th>Описание</th></tr>"

        for ex in EXAMPLES:
            examples_text += f"<tr><td><code style='font-size:16px'>{ex['notation']}</code></td>"
            examples_text += f"<td>{ex['desc']}</td></tr>"

        examples_text += "</table>"
        examples_text += """
<p><br><b>Правила расположения:</b></p>
<ul>
<li>Символы sig в столбик → движения одновременно</li>
<li>Символы sig в строку → движения последовательно (слева направо)</li>
<li>Ориентация ладони всегда записывается перед символами движения</li>
</ul>
"""

        msg = QMessageBox(self)
        msg.setWindowTitle("Примеры записей жестов")
        msg.setTextFormat(Qt.RichText)
        msg.setText(examples_text)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    def _show_about(self):
        """Показывает информацию о программе."""
        about_text = """
<h2>Клавиатура нотаций РЖЯ</h2>
<p><b>Версия:</b> 1.0</p>
<p>Экранная клавиатура для ввода символов нотации 
русского жестового языка.</p>

<p><b>Возможности:</b></p>
<ul>
<li>6 категорий символов нотации</li>
<li>Ввод мышью и с физической клавиатуры</li>
<li>Автоопределение системной темы Windows</li>
<li>4 цветовые темы (системная, светлая, тёмная, контрастная)</li>
<li>Кастомные символы, отсутствующие в стандартных шрифтах</li>
</ul>

<p><b>Система нотации</b> основана на работе Stokoe, 
адаптированной для BSL и русского жестового языка.</p>
"""
        QMessageBox.about(self, "О программе", about_text)


def main():
    """Точка входа приложения."""
    # Включаем High DPI масштабирование
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    app = QApplication(sys.argv)

    # Устанавливаем шрифт приложения
    app_font = QFont("Segoe UI", 10)
    app.setFont(app_font)

    # Устанавливаем имя приложения
    app.setApplicationName("SignLanguageKeyboard")
    app.setApplicationDisplayName("Клавиатура нотаций РЖЯ")
    app.setOrganizationName("RJY Notation")

    # Создаём и показываем окно
    window = SignLanguageKeyboard()
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()