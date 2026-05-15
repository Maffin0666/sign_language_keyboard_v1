"""
Help dialog with reference info.
"""
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QTabWidget, QScrollArea,
                             QTextBrowser, QPushButton)


class HelpDialog(QDialog):
    def __init__(self, parent=None, theme_mgr=None):
        super().__init__(parent)
        self.setWindowTitle("Справка — Нотация жестового языка")
        self.setMinimumSize(820, 600)
        if theme_mgr:
            self.setStyleSheet(theme_mgr.stylesheet())
        self._build()

    def _build(self):
        lo = QVBoxLayout(self)
        tabs = QTabWidget()
        tabs.addTab(self._tab(self._overview_html()), "Обзор")
        tabs.addTab(self._tab(self._dez_html()), "Кистежесты (DEZ)")
        tabs.addTab(self._tab(self._tab_html()), "Расположение (TAB)")
        tabs.addTab(self._tab(self._sig_html()), "Движения (SIG)")
        tabs.addTab(self._tab(self._ori_html()), "Ориентация / Руки")
        tabs.addTab(self._tab(self._examples_html()), "Примеры записей")
        tabs.addTab(self._tab(self._hotkeys_html()), "Горячие клавиши")
        lo.addWidget(tabs)
        btn = QPushButton("Закрыть")
        btn.clicked.connect(self.accept)
        lo.addWidget(btn)

    def _tab(self, html):
        sa = QScrollArea()
        sa.setWidgetResizable(True)
        tb = QTextBrowser()
        tb.setOpenExternalLinks(True)
        tb.setHtml(html)
        sa.setWidget(tb)
        return sa

    def _overview_html(self):
        return """<h2>Система нотации жестового языка</h2>
<p>Каждый жест описывается компонентами:</p>
<ul>
<li><b>DEZ</b> — форма кисти (57 кистежестов, 22 группы)</li>
<li><b>TAB</b> — место расположения относительно тела</li>
<li><b>SIG</b> — движение руки</li>
<li><b>ORI</b> — ориентация ладони</li>
<li><b>HA</b> — расположение рук друг относительно друга</li>
</ul>
<h3>Формула записи</h3>
<ol>
<li><b>Одноручные:</b> TAB → DEZ → ORI → SIG</li>
<li><b>Двуручные (одна рука движется):</b> TAB → DEZ → ORI → ORI → (HA) → DEZ → ORI → SIG</li>
<li><b>Двуручные (обе движутся):</b> TAB → DEZ → ORI → ORI → (HA) → DEZ → ORI → ORI → SIG</li>
</ol>
<h3>Диакритические знаки</h3>
<table border='1' cellpadding='5'>
<tr><td>(нет)</td><td>Базовая форма</td></tr>
<tr><td>· точка</td><td>Вариант 1</td></tr>
<tr><td>^ крышечка</td><td>Вариант 2</td></tr>
<tr><td>— черта</td><td>Вариант 3</td></tr>
<tr><td>¨ две точки</td><td>Вариант 4</td></tr>
<tr><td>⌢ дуга</td><td>Вариант 5</td></tr>
</table>"""

    def _dez_html(self):
        return """<h2>Кистежесты (DEZ)</h2>
<table border='1' cellpadding='5' width='100%'>
<tr><th>Символ</th><th>Описание</th><th>Emoji</th></tr>
<tr><td>A</td><td>Кулак</td><td>✊</td></tr>
<tr><td>Ȧ</td><td>Кулак, большой палец</td><td>👍</td></tr>
<tr><td>G</td><td>Указательный палец</td><td>☝</td></tr>
<tr><td>R</td><td>Скрещенные пальцы</td><td>🤞</td></tr>
<tr><td>H</td><td>Два пальца вместе</td><td>🤚</td></tr>
<tr><td>V</td><td>V-форма</td><td>✌</td></tr>
<tr><td>K</td><td>K-форма</td><td>🤙</td></tr>
<tr><td>W</td><td>Три пальца</td><td>🖖</td></tr>
<tr><td>④</td><td>Четыре пальца</td><td>🖐</td></tr>
<tr><td>F</td><td>Кольцо</td><td>👌</td></tr>
<tr><td>⑦</td><td>Семёрка</td><td>🤟</td></tr>
<tr><td>I</td><td>Мизинец</td><td>🤙</td></tr>
<tr><td>Y</td><td>Большой+мизинец</td><td>🤙</td></tr>
<tr><td>Ч</td><td>Рога</td><td>🤘</td></tr>
<tr><td>⑤</td><td>Пять растопырены</td><td>🖐</td></tr>
<tr><td>B</td><td>Плоская ладонь</td><td>✋</td></tr>
<tr><td>C</td><td>C-форма</td><td>🤏</td></tr>
<tr><td>O</td><td>O-кольцо</td><td>👌</td></tr>
<tr><td>E</td><td>Полусогнутые</td><td>✊</td></tr>
</table>"""

    def _tab_html(self):
        return """<h2>Расположение (TAB)</h2>
<table border='1' cellpadding='5' width='100%'>
<tr><th>Символ</th><th>Место</th></tr>
<tr><td>Ø</td><td>Нейтральное (перед телом)</td></tr>
<tr><td>ʞ</td><td>Верх головы</td></tr>
<tr><td>∩</td><td>Верхняя часть лица</td></tr>
<tr><td>◯</td><td>Всё лицо</td></tr>
<tr><td>Ш</td><td>Глаз</td></tr>
<tr><td>Д</td><td>Нос</td></tr>
<tr><td>Э</td><td>Щека</td></tr>
<tr><td>⊃</td><td>Ухо</td></tr>
<tr><td>U</td><td>Подбородок</td></tr>
<tr><td>Π</td><td>Горло / шея</td></tr>
<tr><td>[]</td><td>Грудь</td></tr>
<tr><td>α</td><td>Запястье (внутри)</td></tr>
<tr><td>ο</td><td>Запястье (тыл)</td></tr>
<tr><td>Н</td><td>Бедро</td></tr>
</table>"""

    def _sig_html(self):
        return """<h2>Движения (SIG)</h2>
<table border='1' cellpadding='5' width='100%'>
<tr><th>Символ</th><th>Движение</th></tr>
<tr><td>●</td><td>Нет движения</td></tr>
<tr><td>∧</td><td>Вверх</td></tr>
<tr><td>∨</td><td>Вниз</td></tr>
<tr><td>τ</td><td>К говорящему</td></tr>
<tr><td>⊥</td><td>От говорящего</td></tr>
<tr><td>&lt;</td><td>Влево</td></tr>
<tr><td>&gt;</td><td>Вправо</td></tr>
<tr><td>×</td><td>Касание</td></tr>
<tr><td>ω</td><td>Поворот запястья</td></tr>
<tr><td>≋</td><td>Шевеление</td></tr>
<tr><td>□</td><td>Раскрыть</td></tr>
<tr><td>■</td><td>Закрыть</td></tr>
<tr><td>˜</td><td>Повторение</td></tr>
</table>"""

    def _ori_html(self):
        return """<h2>Ориентация (ORI) и расположение рук (HA)</h2>
<h3>Ориентация ладони</h3>
<table border='1' cellpadding='5'>
<tr><td>∧</td><td>Вверх</td></tr>
<tr><td>∨</td><td>Вниз</td></tr>
<tr><td>τ</td><td>К говорящему</td></tr>
<tr><td>⊥</td><td>От говорящего</td></tr>
<tr><td>&lt;</td><td>Влево</td></tr>
<tr><td>&gt;</td><td>Вправо</td></tr>
</table>
<h3>Расположение рук</h3>
<table border='1' cellpadding='5'>
<tr><td>A̅</td><td>Правая выше</td></tr>
<tr><td>A̲</td><td>Левая выше</td></tr>
<tr><td>‖</td><td>Рядом</td></tr>
<tr><td>×</td><td>Контакт</td></tr>
<tr><td>⊗</td><td>Сцепление</td></tr>
<tr><td>⊘</td><td>Перекрещены</td></tr>
</table>
<h3>Части кисти</h3>
<table border='1' cellpadding='5'>
<tr><td>a</td><td>Большой палец</td></tr>
<tr><td>e</td><td>Указательный</td></tr>
<tr><td>i</td><td>Средний</td></tr>
<tr><td>o</td><td>Безымянный</td></tr>
<tr><td>u</td><td>Мизинец</td></tr>
</table>"""

    def _examples_html(self):
        return """<h2>Примеры записей жестов</h2>
<table border='1' cellpadding='8' width='100%'>
<tr><th>Запись</th><th>Описание</th></tr>
<tr><td style='font-size:18px;font-family:monospace;'>U A τ∧ ×˜</td>
<td>Гнездо 30: подбородок, кулак, к себе+вверх, касание повторяется</td></tr>
<tr><td style='font-size:18px;font-family:monospace;'>B̄ >⊥ , B̄ ο⊥ &lt;⊙</td>
<td>Гнездо 1658: двуручный tab-жест</td></tr>
<tr><td style='font-size:18px;font-family:monospace;'>Ø F >⊥ , F >⊥ ∧˜</td>
<td>Гнездо 885</td></tr>
<tr><td style='font-size:18px;font-family:monospace;'>[] ⑧τ&lt; ×˜</td>
<td>Гнездо 964</td></tr>
<tr><td style='font-size:18px;font-family:monospace;'>B̄ α> G &lt;⊥ ⊥</td>
<td>Гнездо 403</td></tr>
</table>"""

    def _hotkeys_html(self):
        return """<h2>Горячие клавиши</h2>
<table border='1' cellpadding='5' width='100%'>
<tr><th>Клавиша</th><th>Действие</th></tr>
<tr><td><b>F1</b></td><td>Справка</td></tr>
<tr><td><b>F2</b></td><td>Слой: Кистежесты (DEZ)</td></tr>
<tr><td><b>F3</b></td><td>Слой: Расположение (TAB)</td></tr>
<tr><td><b>F4</b></td><td>Слой: Движения (SIG)</td></tr>
<tr><td><b>F5</b></td><td>Переключить тему</td></tr>
<tr><td><b>F6</b></td><td>Переключить раскладку</td></tr>
<tr><td><b>F7</b></td><td>Пользовательские символы</td></tr>
<tr><td><b>Ctrl+S</b></td><td>Сохранить текст</td></tr>
<tr><td><b>Ctrl+C/V/A/Z</b></td><td>Копировать / Вставить / Выделить / Отменить</td></tr>
<tr><td><b>Backspace / Delete</b></td><td>Удалить символ</td></tr>
<tr><td><b>Space</b></td><td>Пробел (разделитель)</td></tr>
<tr><td><b>Enter</b></td><td>Новая строка</td></tr>
</table>
<p><b>Ввод символов:</b> нажимайте клавиши 1–0, Q–P, A–;, Z–/ — 
вставится символ текущего слоя.</p>"""