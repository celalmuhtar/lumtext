import sys
from pathlib import Path

from PyQt6.QtWidgets import QApplication, QSystemTrayIcon, QMenu
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtCore import pyqtSignal, QObject

from core.config_manager import load_config
from core.hotkey_manager import HotkeyManager
from core.localization import tr, set_language
from ui.settings_window import SettingsWindow
from ui.action_popup import ActionPopup


def create_app_icon():
    icon_path = Path(__file__).parent / "ui" / "app_icon.png"
    if icon_path.exists():
        return QIcon(str(icon_path))
    return QIcon()


class Signals(QObject):
    show_popup = pyqtSignal(str)
    show_settings = pyqtSignal()


class AITextApp:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.app.setQuitOnLastWindowClosed(False)
        self.app.setApplicationName("Lumtext")
        self._app_icon = create_app_icon()
        self.app.setWindowIcon(self._app_icon)

        self.signals = Signals()
        self.signals.show_popup.connect(self._open_popup)
        self.signals.show_settings.connect(self._open_settings)

        self.config = load_config()
        set_language(self.config.get("language", "English"))
        self.settings_window = None
        self.popup = None

        self._setup_tray()
        self._setup_hotkey()

    def _setup_tray(self):
        self.tray = QSystemTrayIcon(self._app_icon)
        self.tray.setToolTip(tr("tray_tooltip"))

        menu = QMenu()
        menu.setStyleSheet("""
            QMenu {
                background: #0f0f18;
                color: #c0c0d8;
                border: 1px solid #2a2a4a;
                border-radius: 8px;
                padding: 4px;
            }
            QMenu::item { padding: 8px 20px; border-radius: 4px; }
            QMenu::item:selected { background: #1a1a3a; }
            QMenu::separator { background: #1a1a3a; height: 1px; margin: 4px 8px; }
        """)

        self._open_settings_action = menu.addAction(tr("tray_open_settings"))
        self._open_settings_action.triggered.connect(self._open_settings)

        menu.addSeparator()

        self._hotkey_info_action = menu.addAction(tr("tray_hotkey_info"))
        self._hotkey_info_action.setEnabled(False)

        menu.addSeparator()

        quit_action = menu.addAction(tr("tray_quit"))
        quit_action.triggered.connect(self._quit)

        self.tray.setContextMenu(menu)
        self.tray.activated.connect(self._tray_activated)
        self.tray.show()

    def _setup_hotkey(self):
        hotkey = self.config.get("hotkey", "<ctrl>+<shift>+<space>")
        self.hotkey_manager = HotkeyManager(hotkey, self._hotkey_triggered)
        self.hotkey_manager.start()

    def _hotkey_triggered(self, text: str = ""):
        if not text:
            return
        self.signals.show_popup.emit(text)

    def _tray_activated(self, reason):
        if reason in (QSystemTrayIcon.ActivationReason.Trigger,
                      QSystemTrayIcon.ActivationReason.DoubleClick):
            self._open_settings()

    def _open_popup(self, selected_text: str):
        if self.popup and self.popup.isVisible():
            self.popup.close()
        self.popup = ActionPopup(selected_text)
        self.popup.show()
        self.popup.activateWindow()
        self.popup.raise_()

    def _open_settings(self):
        if self.settings_window is None:
            self.settings_window = SettingsWindow(self.hotkey_manager)
            self.settings_window.hotkey_changed.connect(self._on_hotkey_changed)
            self.settings_window.language_changed.connect(self._on_language_changed)
        self.settings_window.show()
        self.settings_window.raise_()
        self.settings_window.activateWindow()

    def _on_hotkey_changed(self, new_hotkey: str):
        self.hotkey_manager.update_hotkey(new_hotkey, self._hotkey_triggered)
        self.tray.setToolTip(tr("tray_tooltip_fmt", hotkey=new_hotkey))

    def _on_language_changed(self, lang: str):
        set_language(lang)
        self.tray.setToolTip(tr("tray_tooltip"))
        self._open_settings_action.setText(tr("tray_open_settings"))
        self._hotkey_info_action.setText(tr("tray_hotkey_info"))
        hotkey = self.config.get("hotkey", "<ctrl>+<shift>+<space>")
        self.tray.setToolTip(tr("tray_tooltip_fmt", hotkey=hotkey))
        if self.popup and self.popup.isVisible():
            self.popup._retranslate_ui()

    def _quit(self):
        self.hotkey_manager.stop()
        self.app.quit()

    def run(self):
        self.tray.showMessage(
            "Lumtext",
            tr("startup_message"),
            QSystemTrayIcon.MessageIcon.Information,
            5000
        )
        sys.exit(self.app.exec())


if __name__ == "__main__":
    app = AITextApp()
    app.run()
