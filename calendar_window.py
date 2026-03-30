"""
calendar_window.py — 日历日程挂件（改进版）
修复：使用基类；数据路径修正；独立配置
新增：
  - 上/下月翻页导航
  - 星期表头（一 二 三 四 五 六 日）
  - 今日高亮
  - 有日程的日期显示小圆点提示
"""
import calendar
import json
import os
from datetime import datetime, date

from PySide6.QtWidgets import (
    QVBoxLayout, QLabel, QGridLayout, QFrame,
    QPushButton, QTextEdit, QHBoxLayout, QWidget
)
from PySide6.QtCore import Qt

from base_window import BaseWidget
from settings_window import SettingsWindow
import config_manager

CONFIG_NAME = "calendar"
WEEKDAYS = ["一", "二", "三", "四", "五", "六", "日"]


class CalendarWindow(BaseWidget):
    def __init__(self, parent_app):
        super().__init__(CONFIG_NAME)
        self.parent_app = parent_app
        self.config = config_manager.get_theme(CONFIG_NAME)
        self.resize(310, 500)

        today = date.today()
        self._view_year = today.year
        self._view_month = today.month
        self.selected_date = today.strftime("%Y-%m-%d")
        self.events = {}

        self._setup_ui()
        self._load_data()
        self.refresh_theme()

    def _setup_ui(self):
        self.main_frame = QFrame(self)
        self.main_frame.setObjectName("MainFrame")
        self.main_frame.resize(self.size())
        layout = QVBoxLayout(self.main_frame)
        layout.setContentsMargins(14, 10, 14, 14)
        layout.setSpacing(6)

        # ── 标题栏 ──
        top = QHBoxLayout()
        self.pin_btn = QPushButton("📌")
        self.pin_btn.setFixedSize(26, 26)
        self.pin_btn.clicked.connect(lambda: self.toggle_pin(self.pin_btn))

        self.set_win = SettingsWindow(self, CONFIG_NAME)
        btn_set = QPushButton("⚙")
        btn_set.setFixedSize(26, 26)
        btn_set.clicked.connect(self.set_win.show)

        title_lbl = QLabel("📅 日历日程")
        title_lbl.setObjectName("TitleLabel")
        top.addWidget(title_lbl)
        top.addStretch()
        top.addWidget(self.pin_btn)
        top.addWidget(btn_set)
        layout.addLayout(top)

        # ── 月份导航 ──
        nav = QHBoxLayout()
        btn_prev = QPushButton("‹")
        btn_prev.setFixedSize(28, 28)
        btn_prev.setObjectName("NavBtn")
        btn_prev.clicked.connect(self._prev_month)

        self.month_label = QLabel()
        self.month_label.setObjectName("MonthLabel")
        self.month_label.setAlignment(Qt.AlignCenter)

        btn_next = QPushButton("›")
        btn_next.setFixedSize(28, 28)
        btn_next.setObjectName("NavBtn")
        btn_next.clicked.connect(self._next_month)

        btn_today = QPushButton("今天")
        btn_today.setObjectName("TodayBtn")
        btn_today.clicked.connect(self._go_today)

        nav.addWidget(btn_prev)
        nav.addStretch()
        nav.addWidget(self.month_label)
        nav.addStretch()
        nav.addWidget(btn_today)
        nav.addWidget(btn_next)
        layout.addLayout(nav)

        # ── 日历格子 ──
        self.grid_widget = QWidget()
        self.grid = QGridLayout(self.grid_widget)
        self.grid.setSpacing(3)
        layout.addWidget(self.grid_widget)

        # ── 日程编辑 ──
        layout.addWidget(QLabel("📝 当日日程："))
        self.event_editor = QTextEdit()
        self.event_editor.setPlaceholderText("点击日期后在此记录日程…")
        self.event_editor.textChanged.connect(self._save_event)
        layout.addWidget(self.event_editor)

        self._update_cal()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if hasattr(self, 'main_frame'):
            self.main_frame.resize(self.size())

    # ── 月份翻页 ──
    def _prev_month(self):
        if self._view_month == 1:
            self._view_month = 12
            self._view_year -= 1
        else:
            self._view_month -= 1
        self._update_cal()

    def _next_month(self):
        if self._view_month == 12:
            self._view_month = 1
            self._view_year += 1
        else:
            self._view_month += 1
        self._update_cal()

    def _go_today(self):
        today = date.today()
        self._view_year = today.year
        self._view_month = today.month
        self.selected_date = today.strftime("%Y-%m-%d")
        self._update_cal()
        self.event_editor.setPlainText(self.events.get(self.selected_date, ""))

    def _update_cal(self):
        self.month_label.setText(f"{self._view_year}年 {self._view_month}月")

        # 清空格子
        for i in reversed(range(self.grid.count())):
            w = self.grid.itemAt(i).widget()
            if w:
                w.setParent(None)

        # 星期表头
        for col, wd in enumerate(WEEKDAYS):
            lbl = QLabel(wd)
            lbl.setAlignment(Qt.AlignCenter)
            lbl.setObjectName("WeekdayLabel")
            self.grid.addWidget(lbl, 0, col)

        today_str = date.today().strftime("%Y-%m-%d")
        first_wd, n_days = calendar.monthrange(self._view_year, self._view_month)
        # calendar 以周一=0，我们也是周一=0，一致

        for d in range(1, n_days + 1):
            ds = f"{self._view_year}-{self._view_month:02d}-{d:02d}"
            cell_col = (first_wd + d - 1) % 7
            cell_row = (first_wd + d - 1) // 7 + 1  # +1 留给表头

            btn = QPushButton(str(d))
            btn.setFixedSize(34, 34)
            btn.clicked.connect(lambda _, s=ds: self._switch_date(s))

            # 样式优先级：选中 > 今天 > 有日程 > 普通
            if ds == self.selected_date:
                btn.setObjectName("DaySelected")
            elif ds == today_str:
                btn.setObjectName("DayToday")
            elif ds in self.events and self.events[ds].strip():
                btn.setObjectName("DayHasEvent")
            else:
                btn.setObjectName("DayNormal")

            self.grid.addWidget(btn, cell_row, cell_col)

        self.refresh_theme()

    def _switch_date(self, ds):
        self.selected_date = ds
        self.event_editor.blockSignals(True)
        self.event_editor.setPlainText(self.events.get(ds, ""))
        self.event_editor.blockSignals(False)
        self._update_cal()

    def _save_event(self):
        text = self.event_editor.toPlainText()
        if text.strip():
            self.events[self.selected_date] = text
        else:
            self.events.pop(self.selected_date, None)
        path = os.path.join(config_manager.DATA_DIR, "calendar_db.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.events, f, ensure_ascii=False)

    def _load_data(self):
        path = os.path.join(config_manager.DATA_DIR, "calendar_db.json")
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    self.events = json.load(f)
            except (json.JSONDecodeError, IOError):
                self.events = {}
        self.event_editor.blockSignals(True)
        self.event_editor.setPlainText(self.events.get(self.selected_date, ""))
        self.event_editor.blockSignals(False)

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
            QLabel#MonthLabel {{
                color: {c['text_color']};
                font-family: '{c['font_family']}';
                font-size: {c['font_size']}px;
                font-weight: bold;
            }}
            QLabel#WeekdayLabel {{
                color: rgba(180,180,180,200);
                font-family: '{c['font_family']}';
                font-size: {c['font_size'] - 1}px;
            }}
            QLabel {{
                color: {c['text_color']};
                font-family: '{c['font_family']}';
                font-size: {c['font_size']}px;
            }}
            QPushButton {{
                border: none;
                color: {c['text_color']};
                background: transparent;
                font-family: '{c['font_family']}';
                font-size: {c['font_size']}px;
                border-radius: 17px;
            }}
            QPushButton#NavBtn {{
                font-size: 18px;
                font-weight: bold;
                color: {c['text_color']};
            }}
            QPushButton#TodayBtn {{
                background: rgba(255,255,255,15);
                border-radius: 8px;
                padding: 0 6px;
                font-size: {c['font_size'] - 1}px;
            }}
            QPushButton#DayNormal:hover {{
                background: rgba(255,255,255,15);
            }}
            QPushButton#DayToday {{
                color: #FFD700;
                font-weight: bold;
                border: 1px solid rgba(255,215,0,120);
            }}
            QPushButton#DaySelected {{
                background: rgba(255,255,255,40);
                font-weight: bold;
            }}
            QPushButton#DayHasEvent {{
                color: #7EC8E3;
            }}
            QTextEdit {{
                background: rgba(0,0,0,35);
                color: {c['text_color']};
                border: 1px solid rgba(255,255,255,20);
                border-radius: 8px;
                font-family: '{c['font_family']}';
                font-size: {c['font_size']}px;
                padding: 4px;
            }}
            QScrollBar:vertical {{
                background: transparent; width: 4px;
            }}
            QScrollBar::handle:vertical {{
                background: rgba(255,255,255,40); border-radius: 2px;
            }}
        """)
