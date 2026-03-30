# Vibe-coding-first-tring-Desktop-Widgets-with-note-calendar-plans-
 我的第一个 vibe coding 作品 · 透明玻璃桌面挂件 · 待办+日历+便签 · 可锁定置顶
<div align="center">

# 🪟 Desktop Widgets · 桌面效率挂件

**透明玻璃质感 · 三合一 · 零依赖一键运行**
**Frosted Glass UI · All-in-One · Zero Setup**

<br/>

[![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![PySide6](https://img.shields.io/badge/PySide6-Qt6-41CD52?style=for-the-badge&logo=qt&logoColor=white)](https://doc.qt.io/qtforpython/)
[![Platform](https://img.shields.io/badge/Platform-Win%20%7C%20Mac%20%7C%20Linux-lightgrey?style=for-the-badge)]()
[![License](https://img.shields.io/badge/License-MIT-blueviolet?style=for-the-badge)](LICENSE)

<br/>


</div>

---

## 📖 项目简介

**Desktop Widgets** 是一套常驻桌面的轻量效率挂件，由三个独立浮窗组成：

> 📌 **待办事项** · 📅 **日历日程** · 📝 **随手便签**

采用透明无边框设计，磨砂玻璃质感，悬浮于桌面之上而不喧宾夺主。  
无需配置，开箱即用，支持一键打包为无需 Python 环境的独立程序。

## 📖 Introduction

**Desktop Widgets** is a lightweight always-on-top productivity suite with three independent floating panels:

> 📌 **Todo** · 📅 **Calendar** · 📝 **Quick Notes**

Designed with a frosted-glass, borderless aesthetic — it stays on your desktop without getting in the way.  
No configuration needed. Works out of the box. Ships as a single executable with zero dependencies.

---

## ✨ 核心亮点 / Highlights

<table>
<tr>
<td width="33%" align="center">

### 🎨 透明玻璃风
**Frosted Glass UI**

无边框半透明设计  
背景色、透明度、字体  
全部实时可调

Borderless & translucent.  
Customize colors, opacity  
and fonts in real time.

</td>
<td width="33%" align="center">

### ⚡ 轻量零负担
**Truly Lightweight**

无需安装，双击即用  
数据存于本地  
不联网、不收集任何信息

No install needed.  
Data stored locally.  
No network, no tracking.

</td>
<td width="33%" align="center">

### 🗂 三合一整合
**All-in-One**

待办 + 日历 + 便签  
三窗口独立浮动  
告别 App 切换

Todo + Calendar + Notes.  
Three panels, one tool.  
Stay in your flow.

</td>
</tr>
</table>

---

## 🚀 快速开始 / Quick Start

### 方式一 · 免安装版/ Pre-built Binary (Recommended)

前往 [Releases 页面](../../releases) 下载对应系统的可执行文件，**双击直接运行**，无需安装 Python。

Go to the [Releases page](../../releases) and download the binary for your OS. **Double-click to run** — no Python needed.

| 系统 / OS | 文件 / File |
|-----------|-------------|
| Windows | `桌面挂件.exe` |

> 💾 数据保存在 `~/.desktop_widgets/`，重装不丢失。  
> Data is saved to `~/.desktop_widgets/` and persists across reinstalls.

---

### 方式二 · 源码运行（开发者）/ Run from Source (Developers)

```bash
# 克隆仓库 / Clone
git clone https://github.com/your-username/desktop-widgets.git
cd desktop-widgets

# 安装依赖 / Install dependency
pip install PySide6

# 启动 / Run
python main.py
```

---

## 📋 功能列表 / Features

| | 功能 / Feature | 说明 / Description |
|---|---|---|
| ✅ | 待办事项 Todo | 添加、勾选、删除任务；进度计数；一键清空 / Add, check, delete; progress counter; bulk-clear |
| 📅 | 日历日程 Calendar | 翻月导航；星期表头；今日高亮；有日程标记 / Month nav; weekday header; today highlight; event dots |
| 📝 | 随手便签 Notes | 自由文本；字数统计；防抖自动保存 / Free text; word count; debounced auto-save |
| 🎨 | 独立主题 Per-widget Theme | 每个挂件独立配色、字体、透明度，含实时预览 / Per-widget color, font, opacity with live preview |
| 📌 | 窗口置顶 Always on Top | 每个挂件独立置顶开关 / Per-widget toggle |
| 💾 | 位置记忆 Position Memory | 退出保存坐标，下次自动还原 / Saves and restores window positions |
| 🖥 | 系统托盘 System Tray | 最小化到托盘；双击还原；单独控制各挂件 / Minimize to tray; double-click to restore |
| 🔒 | 锁定移动 Lock Position | 一键锁定所有挂件 / Lock all widgets at once |

---

## 📁 项目结构 / Project Structure

```
desktop-widgets/
├── main.py              # 入口 & 托盘管理 / Entry point & tray
├── base_window.py       # 基类：拖拽、置顶、主题 / Base class: drag, pin, theme
├── config_manager.py    # 配置 & 数据路径 / Config & data path management
├── settings_window.py   # 个性化设置面板 / Per-widget settings panel
├── todo_window.py       # 待办事项挂件 / Todo widget
├── calendar_window.py   # 日历日程挂件 / Calendar widget
└── notes_window.py      # 随手便签挂件 / Notes widget
```

---

## 📦 自行打包 / Build Your Own Binary

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name "桌面挂件" main.py
# 输出在 dist/ / Output in dist/
```

> ⚠️ Windows 下部分杀软可能误报，添加信任即可。  
> Some antivirus may flag the .exe as a false positive — add it to your allowlist.

---

## 🤝 贡献 / Contributing

欢迎 Issue 和 PR！/ Issues and PRs are welcome!

- 🐛 Bug 报告请附操作系统版本和截图 / Include OS version and screenshot for bugs  
- 💡 功能建议请描述使用场景 / Describe your use case for feature requests  
- 🔧 PR 请保持 `_snake_case` 命名风格 / Follow `_snake_case` naming in PRs  

---

## 📄 License

[MIT](LICENSE) © 2025 [Elisa](https://github.com/your-username)

<div align="center">
<br/>
<sub>Made with ❤️ and Python · 用 Python 和热爱做的</sub>
</div>
