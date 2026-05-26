import json
import os
import sys
from pathlib import Path

try:
    from platformdirs import user_config_dir
except ImportError:
    def user_config_dir(appname: str, roaming: bool = False) -> str:
        if sys.platform == "win32":
            base = os.environ.get("APPDATA", str(Path.home() / "AppData" / "Roaming"))
        elif sys.platform == "darwin":
            base = str(Path.home() / "Library" / "Application Support")
        else:
            base = os.environ.get("XDG_CONFIG_HOME", str(Path.home() / ".config"))
        return str(Path(base) / appname)

CONFIG_DIR = Path(user_config_dir("lumtext"))
CONFIG_FILE = CONFIG_DIR / "settings.json"

DEFAULT_CONFIG = {
    "provider": "Anthropic",
    "model": "claude-sonnet-4-5",
    "api_keys": {},
    "hotkey": "<ctrl>+<shift>+space",
    "languages": ["Azerbaijani", "English", "Russian", "Turkish"],
    "language": "English",
    "theme": "dark",
    "window_position": None,
}


def load_config() -> dict:
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            for key, value in DEFAULT_CONFIG.items():
                if key not in data:
                    data[key] = value
            return data
        except (json.JSONDecodeError, IOError):
            pass
    return dict(DEFAULT_CONFIG)


def save_config(config: dict):
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    if os.name == "posix":
        os.chmod(CONFIG_FILE, 0o600)


def get_api_key(config: dict, provider: str) -> str:
    return config.get("api_keys", {}).get(provider, "")


def set_api_key(config: dict, provider: str, key: str):
    if "api_keys" not in config:
        config["api_keys"] = {}
    config["api_keys"][provider] = key
