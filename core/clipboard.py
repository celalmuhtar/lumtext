import subprocess
import time
import sys

from PyQt6.QtCore import QMimeData
from PyQt6.QtWidgets import QApplication


def get_selected_text() -> str:
    """Get currently selected text using xclip (PRIMARY selection on Linux)."""
    if sys.platform.startswith("linux"):
        return _linux_get_selected()
    elif sys.platform == "darwin":
        return _mac_get_selected()
    elif sys.platform == "win32":
        return _windows_get_selected()
    return ""


def set_clipboard(text: str):
    app = QApplication.instance()
    if app is None:
        return
    cb = app.clipboard()
    cb.setText(text)


def set_clipboard_html(html_text: str, plain_text: str = ""):
    app = QApplication.instance()
    if app is None:
        return
    cb = app.clipboard()
    mime = QMimeData()
    mime.setHtml(html_text)
    mime.setText(plain_text or html_text)
    cb.setMimeData(mime)


def _linux_get_selected() -> str:
    try:
        result = subprocess.run(
            ["xclip", "-selection", "primary", "-o"],
            capture_output=True, text=True, timeout=2
        )
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass

    try:
        subprocess.run(["xdotool", "key", "ctrl+c"], timeout=1)
        time.sleep(0.15)
        result = subprocess.run(
            ["xclip", "-selection", "clipboard", "-o"],
            capture_output=True, text=True, timeout=2
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass

    try:
        result = subprocess.run(
            ["xsel", "--primary", "--output"],
            capture_output=True, text=True, timeout=2
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass

    return ""


def _mac_get_selected() -> str:
    try:
        script = 'tell application "System Events" to keystroke "c" using command down'
        subprocess.run(["osascript", "-e", script], timeout=1)
        time.sleep(0.15)
        result = subprocess.run(["pbpaste"], capture_output=True, text=True, timeout=2)
        return result.stdout.strip()
    except Exception:
        return ""


def _mac_set_clipboard(text: str):
    try:
        proc = subprocess.Popen(["pbcopy"], stdin=subprocess.PIPE)
        proc.communicate(text.encode())
    except Exception:
        pass


def _windows_get_selected() -> str:
    try:
        import ctypes
        import ctypes.wintypes
        VK_CONTROL = 0x11
        VK_C = 0x43
        KEYEVENTF_KEYUP = 0x0002
        ctypes.windll.user32.keybd_event(VK_CONTROL, 0, 0, 0)
        ctypes.windll.user32.keybd_event(VK_C, 0, 0, 0)
        time.sleep(0.05)
        ctypes.windll.user32.keybd_event(VK_C, 0, KEYEVENTF_KEYUP, 0)
        ctypes.windll.user32.keybd_event(VK_CONTROL, 0, KEYEVENTF_KEYUP, 0)
        time.sleep(0.15)
        ctypes.windll.user32.OpenClipboard(0)
        CF_UNICODETEXT = 13
        handle = ctypes.windll.user32.GetClipboardData(CF_UNICODETEXT)
        text = ctypes.c_wchar_p(handle).value or ""
        ctypes.windll.user32.CloseClipboard()
        return text.strip()
    except Exception:
        return ""


def _windows_set_clipboard(text: str):
    try:
        import ctypes
        CF_UNICODETEXT = 13
        GMEM_MOVEABLE = 0x0002
        ctypes.windll.user32.OpenClipboard(0)
        ctypes.windll.user32.EmptyClipboard()
        encoded = text.encode("utf-16-le") + b"\x00\x00"
        handle = ctypes.windll.kernel32.GlobalAlloc(GMEM_MOVEABLE, len(encoded))
        ptr = ctypes.windll.kernel32.GlobalLock(handle)
        ctypes.memmove(ptr, encoded, len(encoded))
        ctypes.windll.kernel32.GlobalUnlock(handle)
        ctypes.windll.user32.SetClipboardData(CF_UNICODETEXT, handle)
        ctypes.windll.user32.CloseClipboard()
    except Exception:
        pass
