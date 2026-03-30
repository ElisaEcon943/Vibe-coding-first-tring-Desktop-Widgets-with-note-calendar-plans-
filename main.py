"""
main.py — 程序入口与托盘管理（改进版）
修复：窗口位置持久化；退出时保存位置
新增：关闭所有窗口时不退出（仅最小化到托盘）
"""
import sys
from PySide6.QtWidgets import QApplication, QSystemTrayIcon, QMenu
from PySide6.QtGui import QAction, QIcon, QPixmap, QPainter, QColor, QFont
from PySide6.QtCore import Qt

from todo_window import TodoWindow
from calendar_window import CalendarWindow
from notes_window import NoteWindow
import config_manager


def _make_tray_icon():
    """生成一个简单的彩色托盘图标（无需图片文件）"""
    px = QPixmap(32, 32)
    px.fill(Qt.transparent)
    painter = QPainter(px)
    painter.setRenderHint(QPainter.Antialiasing)
    painter.setBrush(QColor(80, 140, 255, 220))
    painter.setPen(Qt.NoPen)
    painter.drawRoundedRect(2, 2, 28, 28, 7, 7)
    painter.setPen(QColor(255, 255, 255))
    font = QFont()
    font.setPixelSize(16)
    font.setBold(True)
    painter.setFont(font)
    painter.drawText(px.rect(), Qt.AlignCenter, "W")
    painter.end()
    return QIcon(px)


class MainApp:
    def __init__(self):
        positions = config_manager.get_window_positions()

        self.todo = TodoWindow(self)
        self.cal = CalendarWindow(self)
        self.note = NoteWindow(self)
        self.wins = [
            ("todo", self.todo),
            ("calendar", self.cal),
            ("note", self.note),
        ]

        # 恢复上次窗口位置
        self.todo.move(*positions.get("todo", [60, 100]))
        self.cal.move(*positions.get("calendar", [370, 100]))
        self.note.move(*positions.get("note", [700, 100]))

        for _, w in self.wins:
            w.show()

        # ── 系统托盘 ──
        self.tray = QSystemTrayIcon()
        self.tray.setIcon(_make_tray_icon())
        self.tray.setToolTip("桌面效率挂件")

        menu = QMenu()

        # 显示/隐藏切换
        self.show_act = QAction("👁 隐藏所有挂件", menu, checkable=True)
        self.show_act.triggered.connect(self._toggle_visibility)
        menu.addAction(self.show_act)

        # 锁定位置
        self.lock_act = QAction("🔒 锁定窗口位置", menu, checkable=True)
        self.lock_act.triggered.connect(self._toggle_lock)
        menu.addAction(self.lock_act)

        menu.addSeparator()

        # 单独显示/隐藏
        for name, win in self.wins:
            label = {"todo": "待办事项", "calendar": "日历日程", "note": "随手记"}[name]
            act = QAction(f"  {label}", menu, checkable=True)
            act.setChecked(True)
            act.triggered.connect(lambda checked, w=win: w.show() if checked else w.hide())
            menu.addAction(act)

        menu.addSeparator()
        exit_act = QAction("❌ 退出", menu)
        exit_act.triggered.connect(self._quit)
        menu.addAction(exit_act)

        self.tray.setContextMenu(menu)
        self.tray.activated.connect(self._on_tray_activated)
        self.tray.show()

    def _toggle_visibility(self, hidden):
        for _, w in self.wins:
            w.hide() if hidden else w.show()

    def _toggle_lock(self, locked):
        for _, w in self.wins:
            w.can_move = not locked

    def _on_tray_activated(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.DoubleClick:
            for _, w in self.wins:
                w.show()
                w.raise_()

    def _quit(self):
        """退出前保存窗口位置"""
        positions = {
            name: [win.x(), win.y()] for name, win in self.wins
        }
        config_manager.save_window_positions(positions)
        QApplication.instance().quit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)  # 关闭窗口不退出，保留托盘
    main = MainApp()
    sys.exit(app.exec())
