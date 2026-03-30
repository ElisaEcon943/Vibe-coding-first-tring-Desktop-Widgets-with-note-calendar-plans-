"""
settings_window.py — 挂件个性化设置面板（改进版）
修复：透明度滑条与当前颜色同步；颜色选择器支持 alpha
新增：实时预览标签；保存配置按钮
"""
import re
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QColorDialog, QSlider, QFontDialog, QFrame
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
import config_manager


class SettingsWindow(QWidget):
    def __init__(self, target_win, config_name: str):
        super().__init__()
        self.target_win = target_win
        self.config_name = config_name

        self.setWindowTitle("个性化设置")
        self.setFixedSize(280, 420)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.Window)

        self._build_ui()
        self._sync_slider()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(18, 18, 18, 18)

        # ── 颜色区域 ──
        layout.addWidget(self._section_label("🎨 颜色设置"))

        btn_bg = QPushButton("修改背景颜色")
        btn_bg.clicked.connect(self._pick_bg)
        layout.addWidget(btn_bg)

        btn_text = QPushButton("修改文字颜色")
        btn_text.clicked.connect(self._pick_text)
        layout.addWidget(btn_text)

        # ── 透明度 ──
        layout.addWidget(self._section_label("🌓 背景透明度"))

        slider_row = QHBoxLayout()
        self.op_slider = QSlider(Qt.Horizontal)
        self.op_slider.setRange(20, 255)   # 最低 20，防止完全透明
        self.op_slider.valueChanged.connect(self._on_opacity_changed)
        self.op_label = QLabel("180")
        self.op_label.setFixedWidth(30)
        slider_row.addWidget(self.op_slider)
        slider_row.addWidget(self.op_label)
        layout.addLayout(slider_row)

        # ── 字体 ──
        layout.addWidget(self._section_label("🔤 字体样式"))
        btn_font = QPushButton("选择字体与大小")
        btn_font.clicked.connect(self._pick_font)
        layout.addWidget(btn_font)

        # ── 预览 ──
        layout.addWidget(self._section_label("👁 预览"))
        self.preview = QLabel("桌面挂件效果预览 Preview 123")
        self.preview.setAlignment(Qt.AlignCenter)
        self.preview.setFixedHeight(50)
        self.preview.setFrameShape(QFrame.StyledPanel)
        layout.addWidget(self.preview)
        self._update_preview()

        layout.addStretch()

        # ── 保存 ──
        btn_save = QPushButton("💾 保存配置")
        btn_save.clicked.connect(self._save)
        layout.addWidget(btn_save)

    def _section_label(self, text):
        lbl = QLabel(text)
        lbl.setStyleSheet("font-weight: bold; margin-top: 4px;")
        return lbl

    def _sync_slider(self):
        """将滑条同步到当前配置的透明度值"""
        try:
            alpha = int(
                re.search(r'rgba\(\d+,\s*\d+,\s*\d+,\s*(\d+)\)',
                          self.target_win.config.get("bg_color", "")).group(1)
            )
        except (AttributeError, TypeError):
            alpha = 180
        self.op_slider.setValue(alpha)
        self.op_label.setText(str(alpha))

    def _on_opacity_changed(self, value):
        self.op_label.setText(str(value))
        self._apply_opacity(value)
        self._update_preview()

    def _apply_opacity(self, value):
        """仅更新透明度，保留颜色 RGB"""
        bg = self.target_win.config.get("bg_color", "rgba(30,30,35,200)")
        match = re.search(r'rgba\((\d+),\s*(\d+),\s*(\d+)', bg)
        if match:
            r, g, b = match.group(1), match.group(2), match.group(3)
            self.target_win.config["bg_color"] = f"rgba({r}, {g}, {b}, {value})"
        self.target_win.refresh_theme()

    def _pick_bg(self):
        color = QColorDialog.getColor()
        if color.isValid():
            alpha = self.op_slider.value()
            self.target_win.config["bg_color"] = (
                f"rgba({color.red()}, {color.green()}, {color.blue()}, {alpha})"
            )
            self.target_win.refresh_theme()
            self._update_preview()

    def _pick_text(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.target_win.config["text_color"] = color.name()
            self.target_win.refresh_theme()
            self._update_preview()

    def _pick_font(self):
        conf = self.target_win.config
        ok, font = QFontDialog.getFont(
            QFont(conf.get("font_family", "微软雅黑"), conf.get("font_size", 13)), self
        )
        if ok:
            conf["font_family"] = font.family()
            conf["font_size"] = font.pointSize()
            self.target_win.refresh_theme()
            self._update_preview()

    def _update_preview(self):
        c = self.target_win.config
        self.preview.setStyleSheet(
            f"background-color: {c.get('bg_color', 'rgba(30,30,35,200)')};"
            f"color: {c.get('text_color', '#e8e8e8')};"
            f"font-family: '{c.get('font_family', '微软雅黑')}';"
            f"font-size: {c.get('font_size', 13)}px;"
            f"border-radius: 8px; padding: 4px;"
        )

    def _save(self):
        config_manager.save_theme(self.target_win.config, self.config_name)
        self.close()
