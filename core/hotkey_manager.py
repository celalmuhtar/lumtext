import sys
import threading
import time
from typing import Callable, Optional

from core.clipboard import get_selected_text


# ── Linux: UNIX socket trigger + xclip selection watcher ─────────────────

class _LinuxSelectionWatcher:
    def __init__(self, interval: float = 0.25):
        self.interval = interval
        self._running = False
        self._thread: Optional[threading.Thread] = None
        self._last_text = ""
        self.current_text = ""

    def start(self):
        self._running = True
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def _run(self):
        while self._running:
            try:
                text = get_selected_text()
                if text:
                    self.current_text = text
                    self._last_text = text
            except Exception:
                pass
            time.sleep(self.interval)

    def stop(self):
        self._running = False
        if self._thread:
            self._thread.join(timeout=1)


class _LinuxTriggerListener:
    def __init__(self, callback: Callable):
        self.callback = callback
        self._running = False
        self._thread: Optional[threading.Thread] = None
        self._server: Optional[any] = None

    def start(self):
        import os, socket
        SOCKET_PATH = "/tmp/lumtext.sock"
        try:
            os.unlink(SOCKET_PATH)
        except OSError:
            pass
        self._server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self._server.bind(SOCKET_PATH)
        self._server.listen(1)
        self._server.settimeout(1)
        self._running = True
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def _run(self):
        import socket
        while self._running:
            try:
                conn, _ = self._server.accept()
                data = conn.recv(1024)
                if data:
                    self.callback()
                conn.close()
            except socket.timeout:
                pass
            except OSError:
                pass

    def stop(self):
        import os
        self._running = False
        if self._server:
            try:
                self._server.close()
            except OSError:
                pass
        try:
            os.unlink("/tmp/lumtext.sock")
        except OSError:
            pass


# ── Windows/Mac: pynput global hotkey listener ──────────────────────────

class _PynputHotkeyListener:
    def __init__(self, hotkey_str: str, callback: Callable):
        self.hotkey_str = hotkey_str
        self.callback = callback
        self._listener: Optional[any] = None
        self._running = False

    def start(self):
        from pynput import keyboard
        # Convert "<ctrl>+<shift>+space" → pynput format
        parts = self.hotkey_str.replace("<", "").replace(">", "").lower().split("+")
        key_map = {
            "ctrl": "<ctrl>", "shift": "<shift>", "alt": "<alt>",
            "super": "<cmd>" if sys.platform == "darwin" else "<win>",
            "space": "<space>", "tab": "<tab>", "enter": "<enter>",
            "escape": "<esc>", "backspace": "<backspace>",
            "delete": "<delete>", "home": "<home>", "end": "<end>",
            "pageup": "<page_up>", "pagedown": "<page_down>",
        }
        combo = set()
        for p in parts:
            if p in key_map:
                combo.add(keyboard.HotKey.parse(key_map[p])[0])
            elif len(p) == 1:
                combo.add(p)
        hotkey = keyboard.HotKey(combo, self._on_activate)
        self._listener = keyboard.Listener(on_press=hotkey.press, on_release=hotkey.release)
        self._running = True
        self._listener.start()

    def _on_activate(self):
        text = get_selected_text()
        if text:
            self.callback(text)

    def stop(self):
        self._running = False
        if self._listener:
            self._listener.stop()


# ── Unified HotkeyManager ───────────────────────────────────────────────

class HotkeyManager:
    def __init__(self, hotkey_str: str, callback: Callable):
        self.hotkey_str = hotkey_str
        self.callback = callback
        if sys.platform == "linux":
            self._selection = _LinuxSelectionWatcher()
            self._trigger = _LinuxTriggerListener(self._on_linux_trigger)
            self._pynput = None
        else:
            self._selection = None
            self._trigger = None
            self._pynput = _PynputHotkeyListener(hotkey_str, callback)

    def _on_linux_trigger(self):
        if self._selection and self._selection.current_text:
            self.callback(self._selection.current_text)

    def start(self):
        if self._selection:
            self._selection.start()
        if self._trigger:
            self._trigger.start()
        if self._pynput:
            self._pynput.start()

    def stop(self):
        if self._selection:
            self._selection.stop()
        if self._trigger:
            self._trigger.stop()
        if self._pynput:
            self._pynput.stop()

    def update_hotkey(self, new_hotkey: str, callback: Callable):
        self.hotkey_str = new_hotkey
        self.callback = callback
        if self._pynput:
            self._pynput.stop()
            self._pynput = _PynputHotkeyListener(new_hotkey, callback)
            self._pynput.start()


# ── System hotkey helpers (Linux only, rest are stubs) ──────────────────

def get_system_hotkeys_linux() -> list[str]:
    import subprocess
    hotkeys = []
    try:
        schemas = [
            "org.gnome.settings-daemon.plugins.media-keys",
            "org.gnome.desktop.wm.keybindings",
        ]
        for schema in schemas:
            result = subprocess.run(
                ["gsettings", "list-recursively", schema],
                capture_output=True, text=True, timeout=3
            )
            if result.returncode == 0:
                for line in result.stdout.splitlines():
                    parts = line.split(None, 2)
                    if len(parts) == 3 and parts[2] not in ("@as []", "['disabled']", "['']"):
                        hotkeys.append(f"[GNOME] {parts[1]}: {parts[2]}")
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass
    common = [
        "<ctrl>+c  — Copy", "<ctrl>+v  — Paste",
        "<ctrl>+x  — Cut", "<ctrl>+z  — Undo",
        "<ctrl>+a  — Select all", "<ctrl>+s  — Save",
        "<alt>+Tab  — Switch windows", "<alt>+F4  — Close window",
    ]
    return common + hotkeys


def get_system_hotkeys() -> list[str]:
    if sys.platform.startswith("linux"):
        return get_system_hotkeys_linux()
    elif sys.platform == "darwin":
        return [
            "⌘+C — Copy", "⌘+V — Paste", "⌘+X — Cut",
            "⌘+Space — Spotlight", "⌘+Tab — App switcher",
            "⌘+Q — Quit app", "⌘+W — Close window",
        ]
    else:
        return [
            "Ctrl+C — Copy", "Ctrl+V — Paste", "Ctrl+X — Cut",
            "Ctrl+Z — Undo", "Ctrl+A — Select all",
            "Ctrl+Alt+Delete — System menu",
            "Win — Start menu",
        ]


def validate_hotkey(hotkey_str: str) -> tuple[bool, str]:
    if not hotkey_str.strip():
        return False, "Shortcut cannot be empty"
    return True, "OK"
