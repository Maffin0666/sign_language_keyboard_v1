# -*- coding: utf-8 -*-
"""
Генерация и рендеринг кастомных символов нотации жестового языка.
Некоторые символы не существуют в стандартных шрифтах,
поэтому рисуются программно.
"""

from PyQt5.QtGui import (QPainter, QPixmap, QFont, QPen, QColor,
                         QFontMetrics, QPainterPath, QBrush, QIcon)
from PyQt5.QtCore import Qt, QRectF, QPointF


class SymbolRenderer:
    """Рендерит кастомные символы, которых нет в стандартных шрифтах."""

    CACHE = {}  # кэш отрендеренных символов

    @classmethod
    def render_symbol(cls, symbol_id: str, size: int = 40,
                      color: str = "#000000", bg_color: str = None) -> QPixmap:
        """
        Рендерит символ в QPixmap.

        symbol_id: идентификатор символа
        size: размер в пикселях
        color: цвет символа
        bg_color: цвет фона (None = прозрачный)
        """
        cache_key = f"{symbol_id}_{size}_{color}_{bg_color}"
        if cache_key in cls.CACHE:
            return cls.CACHE[cache_key]

        pixmap = QPixmap(size, size)
        if bg_color:
            pixmap.fill(QColor(bg_color))
        else:
            pixmap.fill(Qt.transparent)

        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.TextAntialiasing)

        pen = QPen(QColor(color))
        pen.setWidth(max(1, size // 20))
        painter.setPen(pen)

        # Проверяем кастомные символы
        if symbol_id in cls.CUSTOM_RENDERERS:
            cls.CUSTOM_RENDERERS[symbol_id](painter, size, color)
        else:
            # Рендерим как текст
            cls._render_text(painter, symbol_id, size, color)

        painter.end()

        cls.CACHE[cache_key] = pixmap
        return pixmap

    @classmethod
    def _render_text(cls, painter: QPainter, text: str, size: int, color: str):
        """Рендерит текстовый символ."""
        font = QFont("Segoe UI Symbol", int(size * 0.55))
        font.setStyleStrategy(QFont.PreferAntialias)
        painter.setFont(font)
        painter.setPen(QColor(color))

        rect = QRectF(0, 0, size, size)
        painter.drawText(rect, Qt.AlignCenter, text)

    # === Кастомные отрисовки для специальных символов ===

    @staticmethod
    def _draw_neutral_space(painter: QPainter, size: int, color: str):
        """Ø — нейтральное место перед телом (перечёркнутый круг)."""
        margin = size * 0.15
        r = QRectF(margin, margin, size - 2 * margin, size - 2 * margin)
        pen = QPen(QColor(color), max(2, size // 18))
        painter.setPen(pen)
        painter.drawEllipse(r)
        # Диагональная линия
        painter.drawLine(
            QPointF(margin + (size - 2 * margin) * 0.15, margin + (size - 2 * margin) * 0.85),
            QPointF(margin + (size - 2 * margin) * 0.85, margin + (size - 2 * margin) * 0.15)
        )

    @staticmethod
    def _draw_top_head(painter: QPainter, size: int, color: str):
        """Ξ — верх головы (три горизонтальные линии)."""
        pen = QPen(QColor(color), max(2, size // 16))
        painter.setPen(pen)
        cx = size / 2
        w = size * 0.6
        for i, y_frac in enumerate([0.3, 0.5, 0.7]):
            y = size * y_frac
            painter.drawLine(QPointF(cx - w / 2, y), QPointF(cx + w / 2, y))

    @staticmethod
    def _draw_chest(painter: QPainter, size: int, color: str):
        """[] — грудь (квадратные скобки)."""
        pen = QPen(QColor(color), max(2, size // 16))
        painter.setPen(pen)
        m = size * 0.2
        h = size * 0.6
        # Левая скобка
        painter.drawLine(QPointF(m + size * 0.05, m), QPointF(m, m))
        painter.drawLine(QPointF(m, m), QPointF(m, m + h))
        painter.drawLine(QPointF(m, m + h), QPointF(m + size * 0.05, m + h))
        # Правая скобка
        r = size - m
        painter.drawLine(QPointF(r - size * 0.05, m), QPointF(r, m))
        painter.drawLine(QPointF(r, m), QPointF(r, m + h))
        painter.drawLine(QPointF(r, m + h), QPointF(r - size * 0.05, m + h))

    @staticmethod
    def _draw_no_movement(painter: QPainter, size: int, color: str):
        """ø — нет движения (маленький перечёркнутый круг)."""
        cx, cy = size / 2, size / 2
        r = size * 0.2
        pen = QPen(QColor(color), max(1, size // 22))
        painter.setPen(pen)
        painter.drawEllipse(QPointF(cx, cy), r, r)
        painter.drawLine(
            QPointF(cx - r * 0.7, cy + r * 0.7),
            QPointF(cx + r * 0.7, cy - r * 0.7)
        )

    @staticmethod
    def _draw_up_arrow(painter: QPainter, size: int, color: str):
        """^ — вверх (стрелка вверх)."""
        pen = QPen(QColor(color), max(2, size // 16))
        painter.setPen(pen)
        cx = size / 2
        top = size * 0.2
        bottom = size * 0.8
        painter.drawLine(QPointF(cx, bottom), QPointF(cx, top))
        # Наконечник
        arr = size * 0.12
        painter.drawLine(QPointF(cx, top), QPointF(cx - arr, top + arr))
        painter.drawLine(QPointF(cx, top), QPointF(cx + arr, top + arr))

    @staticmethod
    def _draw_down_arrow(painter: QPainter, size: int, color: str):
        """v — вниз (стрелка вниз)."""
        pen = QPen(QColor(color), max(2, size // 16))
        painter.setPen(pen)
        cx = size / 2
        top = size * 0.2
        bottom = size * 0.8
        painter.drawLine(QPointF(cx, top), QPointF(cx, bottom))
        arr = size * 0.12
        painter.drawLine(QPointF(cx, bottom), QPointF(cx - arr, bottom - arr))
        painter.drawLine(QPointF(cx, bottom), QPointF(cx + arr, bottom - arr))

    @staticmethod
    def _draw_towards(painter: QPainter, size: int, color: str):
        """τ — к говорящему."""
        pen = QPen(QColor(color), max(2, size // 16))
        painter.setPen(pen)
        # T-образный символ
        cx = size / 2
        top = size * 0.25
        bottom = size * 0.75
        w = size * 0.35
        painter.drawLine(QPointF(cx - w, top), QPointF(cx + w, top))
        painter.drawLine(QPointF(cx, top), QPointF(cx, bottom))

    @staticmethod
    def _draw_away(painter: QPainter, size: int, color: str):
        """⊥ — от говорящего."""
        pen = QPen(QColor(color), max(2, size // 16))
        painter.setPen(pen)
        cx = size / 2
        top = size * 0.25
        bottom = size * 0.75
        w = size * 0.35
        painter.drawLine(QPointF(cx, top), QPointF(cx, bottom))
        painter.drawLine(QPointF(cx - w, bottom), QPointF(cx + w, bottom))

    @staticmethod
    def _draw_circle_movement(painter: QPainter, size: int, color: str):
        """● — по кругу."""
        pen = QPen(QColor(color), max(2, size // 16))
        painter.setPen(pen)
        cx, cy = size / 2, size / 2
        r = size * 0.25
        painter.drawEllipse(QPointF(cx, cy), r, r)
        # Стрелка на круге
        arr = size * 0.08
        ax = cx + r
        ay = cy
        painter.drawLine(QPointF(ax, ay), QPointF(ax - arr, ay - arr))
        painter.drawLine(QPointF(ax, ay), QPointF(ax + arr * 0.5, ay - arr))

    @staticmethod
    def _draw_touch(painter: QPainter, size: int, color: str):
        """✕ — касание (x)."""
        pen = QPen(QColor(color), max(2, size // 14))
        painter.setPen(pen)
        m = size * 0.25
        painter.drawLine(QPointF(m, m), QPointF(size - m, size - m))
        painter.drawLine(QPointF(size - m, m), QPointF(m, size - m))

    @staticmethod
    def _draw_wiggle(painter: QPainter, size: int, color: str):
        """φ — шевеление (волнистая линия)."""
        pen = QPen(QColor(color), max(2, size // 16))
        painter.setPen(pen)
        path = QPainterPath()
        cy = size / 2
        start_x = size * 0.15
        end_x = size * 0.85
        amplitude = size * 0.12
        path.moveTo(start_x, cy)
        segments = 3
        seg_w = (end_x - start_x) / segments
        for s in range(segments):
            x1 = start_x + s * seg_w + seg_w / 4
            y1 = cy - amplitude
            x2 = start_x + s * seg_w + seg_w * 3 / 4
            y2 = cy + amplitude
            x3 = start_x + (s + 1) * seg_w
            y3 = cy
            path.cubicTo(x1, y1, x2, y2, x3, y3)
        painter.drawPath(path)

    @staticmethod
    def _draw_open(painter: QPainter, size: int, color: str):
        """□ — открыть (пустой квадрат)."""
        pen = QPen(QColor(color), max(2, size // 16))
        painter.setPen(pen)
        m = size * 0.25
        painter.drawRect(QRectF(m, m, size - 2 * m, size - 2 * m))

    @staticmethod
    def _draw_close(painter: QPainter, size: int, color: str):
        """# — закрыть (решётка)."""
        pen = QPen(QColor(color), max(2, size // 16))
        painter.setPen(pen)
        m = size * 0.2
        third = (size - 2 * m) / 3
        # Вертикальные
        for i in [1, 2]:
            x = m + third * i
            painter.drawLine(QPointF(x, m), QPointF(x, size - m))
        # Горизонтальные
        for i in [1, 2]:
            y = m + third * i
            painter.drawLine(QPointF(m, y), QPointF(size - m, y))

    @staticmethod
    def _draw_repeated(painter: QPainter, size: int, color: str):
        """•• — повторяющееся движение (две точки)."""
        pen = QPen(QColor(color))
        painter.setPen(pen)
        painter.setBrush(QBrush(QColor(color)))
        r = size * 0.06
        cy = size / 2
        painter.drawEllipse(QPointF(size * 0.35, cy), r, r)
        painter.drawEllipse(QPointF(size * 0.65, cy), r, r)

    @staticmethod
    def _draw_side_by_side(painter: QPainter, size: int, color: str):
        """‖ — рядом (две вертикальные линии)."""
        pen = QPen(QColor(color), max(2, size // 16))
        painter.setPen(pen)
        top = size * 0.2
        bottom = size * 0.8
        painter.drawLine(QPointF(size * 0.4, top), QPointF(size * 0.4, bottom))
        painter.drawLine(QPointF(size * 0.6, top), QPointF(size * 0.6, bottom))

    @staticmethod
    def _draw_interlinking(painter: QPainter, size: int, color: str):
        """ꭓ — сцепление (два сцепленных кольца)."""
        pen = QPen(QColor(color), max(2, size // 18))
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)
        r = size * 0.18
        painter.drawEllipse(QPointF(size * 0.38, size / 2), r, r)
        painter.drawEllipse(QPointF(size * 0.62, size / 2), r, r)

    @staticmethod
    def _draw_one_inside(painter: QPainter, size: int, color: str):
        """⊚ — одна внутри другой (концентрические круги)."""
        pen = QPen(QColor(color), max(1, size // 20))
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)
        cx, cy = size / 2, size / 2
        painter.drawEllipse(QPointF(cx, cy), size * 0.3, size * 0.3)
        painter.drawEllipse(QPointF(cx, cy), size * 0.15, size * 0.15)

    @staticmethod
    def _draw_crossed_over(painter: QPainter, size: int, color: str):
        """⊗ — скрещены (круг с крестом)."""
        pen = QPen(QColor(color), max(2, size // 18))
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)
        cx, cy = size / 2, size / 2
        r = size * 0.28
        painter.drawEllipse(QPointF(cx, cy), r, r)
        painter.drawLine(QPointF(cx - r * 0.7, cy - r * 0.7), QPointF(cx + r * 0.7, cy + r * 0.7))
        painter.drawLine(QPointF(cx + r * 0.7, cy - r * 0.7), QPointF(cx - r * 0.7, cy + r * 0.7))

    @staticmethod
    def _draw_fist_A(painter: QPainter, size: int, color: str):
        """A — кулак (стилизованное изображение)."""
        font = QFont("Segoe UI", int(size * 0.5), QFont.Bold)
        painter.setFont(font)
        painter.setPen(QColor(color))
        rect = QRectF(0, 0, size, size)
        painter.drawText(rect, Qt.AlignCenter, "A")
        # Маленькая линия снизу для обозначения кулака
        pen = QPen(QColor(color), max(1, size // 24))
        painter.setPen(pen)
        painter.drawLine(QPointF(size * 0.3, size * 0.82), QPointF(size * 0.7, size * 0.82))


# Регистрация кастомных рендереров
SymbolRenderer.CUSTOM_RENDERERS = {
    "Ø": SymbolRenderer._draw_neutral_space,
    "Ξ": SymbolRenderer._draw_top_head,
    "[]": SymbolRenderer._draw_chest,
    "ø": SymbolRenderer._draw_no_movement,
    "^": SymbolRenderer._draw_up_arrow,
    "v_sig": SymbolRenderer._draw_down_arrow,
    "τ": SymbolRenderer._draw_towards,
    "⊥": SymbolRenderer._draw_away,
    "●": SymbolRenderer._draw_circle_movement,
    "✕": SymbolRenderer._draw_touch,
    "φ": SymbolRenderer._draw_wiggle,
    "□": SymbolRenderer._draw_open,
    "#": SymbolRenderer._draw_close,
    "••": SymbolRenderer._draw_repeated,
    "‖": SymbolRenderer._draw_side_by_side,
    "ꭓ": SymbolRenderer._draw_interlinking,
    "⊚": SymbolRenderer._draw_one_inside,
    "⊗": SymbolRenderer._draw_crossed_over,
}


def get_symbol_pixmap(symbol: str, size: int = 40,
                      color: str = "#000000", bg: str = None) -> QPixmap:
    """Удобная функция для получения QPixmap символа."""
    return SymbolRenderer.render_symbol(symbol, size, color, bg)


def get_symbol_icon(symbol: str, size: int = 40, color: str = "#000000") -> QIcon:
    """Получить QIcon для символа."""
    pixmap = get_symbol_pixmap(symbol, size, color)
    return QIcon(pixmap)