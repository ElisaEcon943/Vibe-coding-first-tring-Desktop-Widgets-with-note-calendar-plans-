# 桌面效率挂件 — 打包指南

## 📁 文件结构
```
desktop_widgets/
├── main.py              # 程序入口
├── base_window.py       # 窗口基类（新增）
├── config_manager.py    # 配置管理
├── settings_window.py   # 设置面板
├── todo_window.py       # 待办事项
├── calendar_window.py   # 日历日程
└── notes_window.py      # 随手便签
```

## 🚀 运行方式
```bash
pip install PySide6
python main.py
```

---

## 📦 打包为免安装 .exe（Windows）

### 第一步：安装 PyInstaller
```bash
pip install pyinstaller
```

### 第二步：在项目目录执行打包命令
```bash
pyinstaller --onefile --windowed --name "桌面挂件" main.py
```

参数说明：
- `--onefile`：打包成单个 .exe 文件
- `--windowed`：不显示黑色控制台窗口
- `--name "桌面挂件"`：输出文件名

### 第三步：找到输出文件
打包完成后，`.exe` 文件在 `dist/` 目录下。

---

## 🍎 打包为 macOS .app

### 安装 PyInstaller
```bash
pip install pyinstaller
```

### 打包命令
```bash
pyinstaller --onefile --windowed --name "桌面挂件" main.py
```

输出在 `dist/桌面挂件.app`，可直接双击运行。

---

## 🐧 打包为 Linux 可执行文件
```bash
pyinstaller --onefile --name "桌面挂件" main.py
```

输出在 `dist/桌面挂件`，`chmod +x` 后可运行。

---

## ⚠ 注意事项

1. **数据存储位置**：打包后，数据文件（todo_db.json 等）会保存在：
   - Windows：`C:\Users\你的用户名\.desktop_widgets\`
   - macOS / Linux：`~/.desktop_widgets/`

2. **字体问题**：如果目标电脑没有「微软雅黑」字体，
   在设置面板中改为系统字体即可。

3. **杀毒软件误报**：PyInstaller 打包的 exe 可能被某些杀毒软件误报，
   这是正常现象，可以添加信任或使用 Nuitka 替代打包。

4. **Nuitka 打包（性能更好，但配置较复杂）**：
   ```bash
   pip install nuitka
   python -m nuitka --onefile --windows-disable-console --follow-imports main.py
   ```
