"""
notes_window.py — 随手便签挂件（改进版）
修复：使用基类；数据路径修正；独立配置
新增：字数统计；自动保存状态提示
"""
import os
from PySide6.QtWidgets import (
    QVBoxLayout, QTextEdit, QFrame,
    QHBoxLayout, QPushButton, QLabel
)
from PySide6.QtCore import Qt, QTimer

from base_window import BaseWidget
from settings_window import SettingsWindow
import config_manager

CONFIG_NAME = "note"


class NoteWindow(BaseWidget):
    def __init__(self, parent_app):
        super().__init__(CONFIG_NAME)
        self.parent_app = parent_app
        self.config = config_manager.get_theme(CONFIG_NAME)
        self.resize(270, 260)
        self._setup_ui()
        self._load_data()
        self.refresh_theme()

        # 防抖：300ms 后才真正写磁盘
        self._save_timer = QTimer()
        self._save_timer.setSingleShot(True)
        self._save_timer.timeout.connect(self._do_save)

    def _setup_ui(self):
        self.main_frame = QFrame(self)
        self.main_frame.setObjectName("MainFrame")
        self.main_frame.resize(self.size())
        layout = QVBoxLayout(self.main_frame)
        layout.setContentsMargins(14, 10, 14, 14)
        layout.setSpacing(6)

        # ── 标题栏 ──
        top = QHBoxLayout()
        title = QLabel("📝 随手记")
        title.setObjectName("TitleLabel")
        self.pin_btn = QPushButton("📌")
        self.pin_btn.setFixedSize(26, 26)
        self.pin_btn.clicked.connect(lambda: self.toggle_pin(self.pin_btn))

        self.set_win = SettingsWindow(self, CONFIG_NAME)
        btn_set = QPushButton("⚙")
        btn_set.setFixedSize(26, 26)
        btn_set.clicked.connect(self.set_win.show)

        top.addWidget(title)
        top.addStretch()
        top.addWidget(self.pin_btn)
        top.addWidget(btn_set)
        layout.addLayout(top)

        # ── 编辑器 ──
        self.editor = QTextEdit()
        self.editor.setPlaceholderText("随手记下你的想法…")
        self.editor.textChanged.connect(self._on_text_changed)
        layout.addWidget(self.editor)

        # ── 底部状态栏 ──
        bottom = QHBoxLayout()
        self.char_lbl = QLabel("0 字")
        self.char_lbl.setObjectName("StatusLabel")
        self.save_lbl = QLabel("")
        self.save_lbl.setObjectName("StatusLabel")
        bottom.addWidget(self.char_lbl)
        bottom.addStretch()
        bottom.addWidget(self.save_lbl)
        layout.addLayout(bottom)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if hasattr(self, 'main_frame'):
            self.main_frame.resize(self.size())

    def _on_text_changed(self):
        text = self.editor.toPlainText()
        self.char_lbl.setText(f"{len(text)} 字")
        self.save_lbl.setText("未保存…")
        self._save_timer.start(400)

    def _do_save(self):
        path = os.path.join(config_manager.DATA_DIR, "note_db.txt")
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(self.editor.toPlainText())
            self.save_lbl.setText("✓ 已保存")
        except IOError:
            self.save_lbl.setText("⚠ 保存失败")

    def _load_data(self):
        path = os.path.join(config_manager.DATA_DIR, "note_db.txt")
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    text = f.read()
                self.editor.blockSignals(True)
                self.editor.setPlainText(text)
                self.editor.blockSignals(False)
                self.char_lbl.setText(f"{len(text)} 字")
            except IOError:
                pass

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
            QLabel#StatusLabel {{
                color: rgba(160,160,160,180);
                font-family: '{c['font_family']}';
                font-size: {c['font_size'] - 2}px;
            }}
            QTextEdit {{
                color: {c['text_color']};
                background: transparent;
                border: none;
                font-family: '{c['font_family']}';
                font-size: {c['font_size']}px;
            }}
            QPushButton {{
                border: none;
                color: {c['text_color']};
                background: transparent;
                font-size: {c['font_size']}px;
            }}
            QPushButton:hover {{
                background: rgba(255,255,255,15);
                border-radius: 4px;
            }}
            QScrollBar:vertical {{
                background: transparent; width: 4px;
            }}
            QScrollBar::handle:vertical {{
                background: rgba(255,255,255,40); border-radius: 2px;
            }}
        """)
