"""
Configuration module for Sign Language Notation Keyboard
"""
import json
import os

APP_NAME = "Клавиатура нотаций жестового языка"
APP_VERSION = "1.2.0"
CONFIG_DIR = os.path.join(os.path.expanduser("~"), ".sign_keyboard")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")
CUSTOM_SYMBOLS_FILE = os.path.join(CONFIG_DIR, "custom_symbols.json")

DEFAULT_CONFIG = {
    "theme": "auto",
    "layout_mode": "qwerty",
    "active_layer": "handshape",
    "window_opacity": 1.0,
    "always_on_top": True,
    "font_size": 14,
    "last_window_geometry": None,
}


def ensure_config_dir():
    if not os.path.exists(CONFIG_DIR):
        os.makedirs(CONFIG_DIR)


def load_config():
    ensure_config_dir()
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                cfg = json.load(f)
                for k, v in DEFAULT_CONFIG.items():
                    if k not in cfg:
                        cfg[k] = v
                return cfg
        except Exception:
            return dict(DEFAULT_CONFIG)
    return dict(DEFAULT_CONFIG)


def save_config(config):
    ensure_config_dir()
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)


def load_custom_symbols():
    ensure_config_dir()
    if os.path.exists(CUSTOM_SYMBOLS_FILE):
        try:
            with open(CUSTOM_SYMBOLS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}


def save_custom_symbols(symbols):
    ensure_config_dir()
    with open(CUSTOM_SYMBOLS_FILE, "w", encoding="utf-8") as f:
        json.dump(symbols, f, ensure_ascii=False, indent=2)