"""
base_window.py — 所有挂件窗口的基类
提取公共逻辑：拖拽移动、置顶切换、主题刷新接口
"""
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt


class BaseWidget(QWidget):
    """
    挂件基类，子类只需：
    1. 调用 super().__init__(config_name)
    2. 实现 refresh_theme()
    """

    def __init__(self, config_name: str):
        super().__init__()
        self._config_name = config_name
        self._old_pos = None
        self.can_move = True

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)

    # ── 拖拽移动 ──────────────────────────────────────────
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._old_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if self.can_move and event.buttons() == Qt.LeftButton and self._old_pos is not None:
            delta = event.globalPosition().toPoint() - self._old_pos
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self._old_pos = event.globalPosition().toPoint()

    def mouseReleaseEvent(self, event):
        self._old_pos = None

    # ── 置顶切换 ──────────────────────────────────────────
    def toggle_pin(self, pin_btn=None):
        pinned = bool(self.windowFlags() & Qt.WindowStaysOnTopHint)
        if pinned:
            self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool)
            if pin_btn:
                pin_btn.setStyleSheet("")
        else:
            self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool | Qt.WindowStaysOnTopHint)
            if pin_btn:
                pin_btn.setStyleSheet("color: #FFD700; background: rgba(255,215,0,25);")
        self.show()

    # ── 子类必须实现 ──────────────────────────────────────
    def refresh_theme(self):
        raise NotImplementedError
