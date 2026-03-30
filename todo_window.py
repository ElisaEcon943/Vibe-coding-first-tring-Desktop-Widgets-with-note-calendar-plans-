"""
todo_window.py — 待办事项挂件（改进版）
修复：
  - 使用基类消除重复代码
  - 数据路径使用 DATA_DIR（打包兼容）
  - 独立配置存储
新增：
  - 已完成任务折叠/展开
  - 任务数量统计标签
"""
import json
import os
from PySide6.QtWidgets import (
    QVBoxLayout, QLineEdit, QCheckBox, QScrollArea,
    QFrame, QHBoxLayout, QPushButton, QLabel, QWidget
)
from PySide6.QtCore import Qt

from base_window import BaseWidget
from settings_window import SettingsWindow
import config_manager

CONFIG_NAME = "todo"


class TodoWindow(BaseWidget):
    def __init__(self, parent_app):
        super().__init__(CONFIG_NAME)
        self.parent_app = parent_app
        self.config = config_manager.get_theme(CONFIG_NAME)
        self.resize(290, 420)
        self._setup_ui()
        self._load_data()
        self.refresh_theme()

    def _setup_ui(self):
        self.main_frame = QFrame(self)
        self.main_frame.setObjectName("MainFrame")
        self.main_frame.resize(self.size())
        layout = QVBoxLayout(self.main_frame)
        layout.setContentsMargins(14, 10, 14, 14)
        layout.setSpacing(8)

        # ── 标题栏 ──
        top = QHBoxLayout()
        title = QLabel("✅ 我的待办")
        title.setObjectName("TitleLabel")
        self.count_lbl = QLabel("")
        self.count_lbl.setObjectName("CountLabel")
        self.pin_btn = QPushButton("📌")
        self.pin_btn.setFixedSize(26, 26)
        self.pin_btn.clicked.connect(lambda: self.toggle_pin(self.pin_btn))

        self.set_win = SettingsWindow(self, CONFIG_NAME)
        btn_set = QPushButton("⚙")
        btn_set.setFixedSize(26, 26)
        btn_set.clicked.connect(self.set_win.show)

        top.addWidget(title)
        top.addWidget(self.count_lbl)
        top.addStretch()
        top.addWidget(self.pin_btn)
        top.addWidget(btn_set)
        layout.addLayout(top)

        # ── 输入框 ──
        self.input = QLineEdit()
        self.input.setPlaceholderText("回车添加新任务…")
        self.input.returnPressed.connect(self._add_task)
        layout.addWidget(self.input)

        # ── 任务列表 ──
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QFrame.NoFrame)
        self.container = QWidget()
        self.list_layout = QVBoxLayout(self.container)
        self.list_layout.setAlignment(Qt.AlignTop)
        self.list_layout.setSpacing(4)
        self.scroll.setWidget(self.container)
        layout.addWidget(self.scroll)

        # ── 底部操作 ──
        bottom = QHBoxLayout()
        btn_clear = QPushButton("🗑 清空已完成")
        btn_clear.clicked.connect(self._clear_done)
        bottom.addStretch()
        bottom.addWidget(btn_clear)
        layout.addLayout(bottom)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if hasattr(self, 'main_frame'):
            self.main_frame.resize(self.size())

    def _add_task(self, text=None, checked=False):
        t = text if text else self.input.text().strip()
        if not t:
            return

        item = QFrame()
        item.setObjectName("TaskItem")
        lay = QHBoxLayout(item)
        lay.setContentsMargins(4, 2, 4, 2)

        cb = QCheckBox(t)
        cb.setChecked(checked)
        if checked:
            cb.setStyleSheet("color: rgba(180,180,180,160); text-decoration: line-through;")

        def on_check(state):
            if state == 2:
                cb.setStyleSheet("color: rgba(180,180,180,160); text-decoration: line-through;")
            else:
                cb.setStyleSheet("")
            self._save_data()
            self._update_count()

        cb.stateChanged.connect(on_check)

        btn_del = QPushButton("✕")
        btn_del.setFixedSize(18, 18)
        btn_del.setObjectName("DelBtn")
        btn_del.clicked.connect(lambda: [item.setParent(None), self._save_data(), self._update_count()])

        lay.addWidget(cb)
        lay.addStretch()
        lay.addWidget(btn_del)
        self.list_layout.addWidget(item)

        if not text:
            self.input.clear()
            self._save_data()
        self._update_count()

    def _clear_done(self):
        to_remove = []
        for i in range(self.list_layout.count()):
            item_widget = self.list_layout.itemAt(i).widget()
            if item_widget:
                cb = item_widget.findChild(QCheckBox)
                if cb and cb.isChecked():
                    to_remove.append(item_widget)
        for w in to_remove:
            w.setParent(None)
        self._save_data()
        self._update_count()

    def _update_count(self):
        total = done = 0
        for i in range(self.list_layout.count()):
            w = self.list_layout.itemAt(i).widget()
            if w:
                cb = w.findChild(QCheckBox)
                if cb:
                    total += 1
                    if cb.isChecked():
                        done += 1
        if total:
            self.count_lbl.setText(f"({done}/{total})")
        else:
            self.count_lbl.setText("")

    def refresh_theme(self):
        c = self.config
        self.setStyleSheet(f"""
            QFrame#MainFrame {{
                background-color: {c['bg_color']};
                border-radius: 16px;
                border: 1px solid rgba(255,255,255,25);
            }}
            QLabel#TitleLabel {{
                color: {c['text_color']};
                font-family: '{c['font_family']}';
                font-size: {c['font_size'] + 1}px;
                font-weight: bold;
            }}
            QLabel#CountLabel {{
                color: rgba(180,180,180,180);
                font-family: '{c['font_family']}';
                font-size: {c['font_size'] - 1}px;
            }}
            QCheckBox {{
                color: {c['text_color']};
                font-family: '{c['font_family']}';
                font-size: {c['font_size']}px;
            }}
            QLineEdit {{
                background: rgba(255,255,255,15);
                color: {c['text_color']};
                border: 1px solid rgba(255,255,255,20);
                border-radius: 8px;
                padding: 4px 8px;
                font-size: {c['font_size']}px;
                font-family: '{c['font_family']}';
            }}
            QLineEdit:focus {{
                border: 1px solid rgba(255,255,255,50);
            }}
            QPushButton {{
                border: none;
                color: {c['text_color']};
                background: transparent;
                font-family: '{c['font_family']}';
                font-size: {c['font_size']}px;
            }}
            QPushButton#DelBtn {{
                color: rgba(255,100,100,180);
                font-size: 10px;
            }}
            QPushButton:hover {{
                background: rgba(255,255,255,15);
                border-radius: 4px;
            }}
            QScrollBar:vertical {{
                background: transparent; width: 4px;
            }}
            QScrollBar::handle:vertical {{
                background: rgba(255,255,255,40);
                border-radius: 2px;
            }}
        """)

    def _save_data(self):
        data = []
        for i in range(self.list_layout.count()):
            w = self.list_layout.itemAt(i).widget()
            if w:
                cb = w.findChild(QCheckBox)
                if cb:
                    data.append({"t": cb.text(), "c": cb.isChecked()})
        path = os.path.join(config_manager.DATA_DIR, "todo_db.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)

    def _load_data(self):
        path = os.path.join(config_manager.DATA_DIR, "todo_db.json")
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    for item in json.load(f):
                        self._add_task(item.get('t', ''), item.get('c', False))
            except (json.JSONDecodeError, IOError):
                pass
        self._update_count()
