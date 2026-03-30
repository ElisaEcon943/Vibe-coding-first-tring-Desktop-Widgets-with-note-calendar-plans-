import json
import os
import sys


def get_data_dir():
    """获取数据文件存放目录（打包后也能正确找到）"""
    if getattr(sys, 'frozen', False):
        # PyInstaller 打包后，使用用户数据目录
        base = os.path.join(os.path.expanduser("~"), ".desktop_widgets")
    else:
        base = os.path.dirname(os.path.abspath(__file__))
    os.makedirs(base, exist_ok=True)
    return base


DATA_DIR = get_data_dir()


def get_default_config():
    return {
        "bg_color": "rgba(30, 30, 35, 200)",
        "text_color": "#e8e8e8",
        "font_size": 13,
        "font_family": "微软雅黑"
    }


def get_theme(name="shared"):
    """读取指定名称的配置（每个挂件可独立配置）"""
    default = get_default_config()
    path = os.path.join(DATA_DIR, f"config_{name}.json")
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                conf = json.load(f)
            for k, v in default.items():
                if k not in conf:
                    conf[k] = v
            return conf
        except (json.JSONDecodeError, IOError):
            pass
    return default.copy()


def save_theme(config, name="shared"):
    """保存指定挂件的配置"""
    path = os.path.join(DATA_DIR, f"config_{name}.json")
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
    except IOError as e:
        print(f"保存配置失败: {e}")


def get_window_positions():
    """读取窗口上次的位置"""
    path = os.path.join(DATA_DIR, "window_positions.json")
    default = {
        "todo": [60, 100],
        "calendar": [370, 100],
        "note": [700, 100]
    }
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
    return default


def save_window_positions(positions: dict):
    """保存窗口位置"""
    path = os.path.join(DATA_DIR, "window_positions.json")
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(positions, f)
    except IOError as e:
        print(f"保存窗口位置失败: {e}")
