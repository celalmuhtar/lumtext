from pathlib import Path

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QComboBox, QLineEdit, QPushButton, QFrame,
    QListWidget, QListWidgetItem, QTabWidget, QScrollArea,
    QMessageBox, QDialog, QTextEdit, QSizePolicy, QCheckBox,
    QCompleter
)
from PyQt6.QtCore import Qt, QEvent, QSize, QTimer, pyqtSignal, QSortFilterProxyModel, QUrl
from PyQt6.QtGui import QDesktopServices
from PyQt6.QtGui import QFont, QIcon, QKeySequence

from core.ai_handler import MODELS, fetch_openrouter_models
from PyQt6.QtCore import QThread, pyqtSignal as Signal
from core.config_manager import load_config, save_config, get_api_key, set_api_key
from core.hotkey_manager import get_system_hotkeys, validate_hotkey
from core.localization import tr, set_language, LANGUAGES

_ARROW_PATH = Path(__file__).parent / "arrow.png"

def _get_style() -> str:
    return STYLE_TEMPLATE.replace("{_ARROW_PATH}", str(_ARROW_PATH))

STYLE_TEMPLATE = """
QMainWindow, QWidget#central {
    background: #0a0a10;
}
QWidget {
    font-family: 'Ubuntu', 'Segoe UI', sans-serif;
}
QTabWidget::pane {
    border: 1px solid #1e1e30;
    background: #0d0d18;
    border-radius: 10px;
}
QTabBar::tab {
    background: #12121e;
    color: #5a5a8a;
    padding: 10px 22px;
    border: none;
    font-size: 12px;
    font-weight: 500;
}
QTabBar::tab:selected {
    color: #a0a0ff;
    background: #0d0d18;
    border-bottom: 2px solid #6060ff;
}
QTabBar::tab:hover { color: #8080cc; }
QLabel#title {
    color: #e0e0f0;
    font-size: 22px;
    font-weight: 700;
    letter-spacing: 2px;
}
QLabel#subtitle {
    color: #3a3a6a;
    font-size: 11px;
    letter-spacing: 1px;
}
QLabel#section {
    color: #5050aa;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 3px;
}
QLabel.field_label {
    color: #8080a8;
    font-size: 12px;
}
QComboBox {
    background: #13131f;
    color: #c8c8e0;
    border: 1px solid #252538;
    border-radius: 8px;
    padding: 8px 12px;
    font-size: 12px;
    min-height: 20px;
}
QComboBox:focus { border-color: #5050bb; }
QComboBox::drop-down {
    border: none;
    width: 26px;
}
QComboBox::down-arrow {
    image: url({_ARROW_PATH});
    width: 12px;
    height: 8px;
}
QComboBox QAbstractItemView {
    background: #13131f;
    color: #c8c8e0;
    border: 1px solid #252538;
    selection-background-color: #252548;
    outline: none;
}
QLineEdit {
    background: #13131f;
    color: #c8c8e0;
    border: 1px solid #252538;
    border-radius: 8px;
    padding: 8px 12px;
    font-size: 12px;
    min-height: 20px;
}
QLineEdit:focus { border-color: #5050bb; }
QPushButton.primary {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #3535aa, stop:1 #6035aa);
    color: white;
    border: none;
    border-radius: 8px;
    padding: 9px 22px;
    font-size: 12px;
    font-weight: 600;
}
QPushButton.primary:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #4545bb, stop:1 #7045bb);
}
QPushButton.secondary {
    background: #13131f;
    color: #8080b8;
    border: 1px solid #252538;
    border-radius: 8px;
    padding: 9px 18px;
    font-size: 12px;
}
QPushButton.secondary:hover { color: #c0c0e0; border-color: #404060; }
QPushButton.danger {
    background: #1a0a0a;
    color: #cc5050;
    border: 1px solid #3a1a1a;
    border-radius: 8px;
    padding: 9px 18px;
    font-size: 12px;
}
QPushButton.danger:hover { background: #2a1010; }
QListWidget {
    background: #0d0d18;
    color: #8080a0;
    border: 1px solid #1e1e30;
    border-radius: 8px;
    font-size: 11px;
    font-family: 'JetBrains Mono', 'Fira Code', monospace;
    padding: 4px;
}
QListWidget::item { padding: 3px 6px; border-radius: 4px; }
QListWidget::item:hover { background: #1a1a2a; color: #c0c0d8; }
QFrame#card {
    background: #0d0d18;
    border: 1px solid #1e1e30;
    border-radius: 12px;
}
QFrame#divider {
    background: #1a1a2a;
    max-height: 1px;
    min-height: 1px;
}
QLabel#hotkey_display {
    background: #080810;
    color: #8080ff;
    border: 1px solid #252548;
    border-radius: 6px;
    padding: 6px 14px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 13px;
}
"""


class SettingsWindow(QMainWindow):
    hotkey_changed = pyqtSignal(str)
    language_changed = pyqtSignal(str)

    def __init__(self, hotkey_manager=None):
        super().__init__()
        self.hotkey_manager = hotkey_manager
        self.config = load_config()
        set_language(self.config.get("language", "English"))
        self._setup_window()
        self._setup_ui()
        self._center_on_screen()

    def _center_on_screen(self):
        screen = self.screen()
        if screen is None:
            return
        geo = screen.availableGeometry()
        x = geo.x() + (geo.width() - self.width()) // 2
        y = geo.y() + (geo.height() - self.height()) // 2
        self.move(x, y)

    def _setup_window(self):
        self.setWindowTitle(tr("settings_title"))
        self.setMinimumSize(640, 580)
        self.setStyleSheet(_get_style())

    def _setup_ui(self):
        central = QWidget()
        central.setObjectName("central")
        self.setCentralWidget(central)

        root = QVBoxLayout(central)
        root.setContentsMargins(28, 24, 28, 24)
        root.setSpacing(16)

        # Header
        hdr = QHBoxLayout()
        left = QVBoxLayout()
        t = QLabel(tr("title"))
        t.setObjectName("title")
        s = QLabel(tr("settings_subtitle"))
        s.setObjectName("subtitle")
        left.addWidget(t)
        left.addWidget(s)
        hdr.addLayout(left)
        hdr.addStretch()

        save_btn = QPushButton(tr("btn_save"))
        save_btn.setProperty("class", "primary")
        save_btn.setStyleSheet(_get_style())
        save_btn.clicked.connect(self._save_all)
        hdr.addWidget(save_btn)
        root.addLayout(hdr)

        div = QFrame()
        div.setObjectName("divider")
        root.addWidget(div)

        # Tabs
        self._tabs = QTabWidget()
        self._tabs.addTab(self._build_model_tab(), tr("tab_model"))
        self._tabs.addTab(self._build_hotkey_tab(), tr("tab_hotkey"))
        self._tabs.addTab(self._build_languages_tab(), tr("tab_languages"))
        root.addWidget(self._tabs)

    # ── Model & API Tab ──────────────────────────────────────────────────────
    def _build_model_tab(self):
        w = QWidget()
        layout = QVBoxLayout(w)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(14)

        # Provider
        sec = QLabel(tr("section_provider"))
        sec.setObjectName("section")
        layout.addWidget(sec)

        row = QHBoxLayout()
        lbl = QLabel(tr("label_provider"))
        lbl.setProperty("class", "field_label")
        row.addWidget(lbl)
        self.provider_combo = QComboBox()
        for p in MODELS.keys():
            self.provider_combo.addItem(p)
        self.provider_combo.setCurrentText(self.config.get("provider", "Anthropic"))
        self.provider_combo.currentTextChanged.connect(self._on_provider_change)
        row.addWidget(self.provider_combo)
        row.addStretch()
        layout.addLayout(row)

        row2 = QHBoxLayout()
        lbl2 = QLabel(tr("label_model"))
        lbl2.setProperty("class", "field_label")
        row2.addWidget(lbl2)
        self.model_combo = QComboBox()
        self.model_combo.setEditable(True)
        self.model_combo.setInsertPolicy(QComboBox.InsertPolicy.NoInsert)
        self.model_combo.setMinimumWidth(220)
        row2.addWidget(self.model_combo)

        self.fetch_models_btn = QPushButton(tr("btn_fetch_models"))
        self.fetch_models_btn.setProperty("class", "secondary")
        self.fetch_models_btn.setToolTip(tr("fetch_tooltip"))
        self.fetch_models_btn.clicked.connect(self._fetch_openrouter_models)
        self.fetch_models_btn.hide()
        row2.addWidget(self.fetch_models_btn)

        row2.addStretch()
        layout.addLayout(row2)

        self.or_hint = QLabel(tr("or_hint"))
        self.or_hint.setStyleSheet("color: #4a6a4a; font-size: 10px;")
        self.or_hint.setWordWrap(True)
        self.or_hint.hide()
        layout.addWidget(self.or_hint)

        div = QFrame(); div.setObjectName("divider")
        layout.addWidget(div)

        sec2 = QLabel(tr("section_api_keys"))
        sec2.setObjectName("section")
        layout.addWidget(sec2)

        self.api_key_widgets = {}
        provider_urls = {
            "OpenAI": "https://platform.openai.com/api-keys",
            "Anthropic": "https://console.anthropic.com/settings/keys",
            "Google": "https://aistudio.google.com/apikey",
            "Groq": "https://console.groq.com/keys",
            "OpenRouter": "https://openrouter.ai/keys",
        }
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")
        inner = QWidget()
        inner_layout = QVBoxLayout(inner)
        inner_layout.setSpacing(10)

        for provider in MODELS.keys():
            card = QFrame()
            card.setObjectName("card")
            card_layout = QHBoxLayout(card)
            card_layout.setContentsMargins(12, 10, 12, 10)

            plbl = QLabel(f"{provider}:")
            plbl.setProperty("class", "field_label")
            plbl.setMinimumWidth(90)
            card_layout.addWidget(plbl)

            key_edit = QLineEdit()
            key_edit.setPlaceholderText(tr("api_key_placeholder", p=provider))
            key_edit.setEchoMode(QLineEdit.EchoMode.Password)
            key_edit.setText(get_api_key(self.config, provider))
            card_layout.addWidget(key_edit)

            show_btn = QPushButton("👁")
            show_btn.setFixedWidth(36)
            show_btn.setStyleSheet("QPushButton { background: #1a1a2a; border: 1px solid #2a2a4a; border-radius: 6px; color: #6060aa; }")
            show_btn.clicked.connect(lambda checked, e=key_edit: self._toggle_key_visibility(e))
            card_layout.addWidget(show_btn)

            link_btn = QPushButton("🔗")
            link_btn.setFixedWidth(36)
            link_btn.setToolTip(provider_urls.get(provider, ""))
            link_btn.setStyleSheet("QPushButton { background: transparent; border: none; color: #5050aa; font-size: 16px; } QPushButton:hover { color: #7070cc; }")
            if provider in provider_urls:
                link_btn.clicked.connect(lambda checked, u=provider_urls[provider]: QDesktopServices.openUrl(QUrl(u)))
            else:
                link_btn.setEnabled(False)
            card_layout.addWidget(link_btn)

            self.api_key_widgets[provider] = key_edit
            inner_layout.addWidget(card)

        inner_layout.addStretch()
        scroll.setWidget(inner)
        layout.addWidget(scroll)

        self._on_provider_change(self.provider_combo.currentText())
        return w

    def _on_provider_change(self, provider: str):
        self.model_combo.clear()
        for m in MODELS.get(provider, {}).get("models", []):
            self.model_combo.addItem(m)

        self._model_proxy = QSortFilterProxyModel(self)
        self._model_proxy.setFilterCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        combo_model = self.model_combo.model()
        if combo_model:
            self._model_proxy.setSourceModel(combo_model)
        self._model_completer = QCompleter(self._model_proxy, self)
        self._model_completer.setCompletionMode(QCompleter.CompletionMode.PopupCompletion)
        self._model_completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self._model_completer.setFilterMode(Qt.MatchFlag.MatchContains)
        self.model_combo.setCompleter(self._model_completer)

        is_openrouter = (provider == "OpenRouter")
        self.fetch_models_btn.setVisible(is_openrouter)
        self.or_hint.setVisible(is_openrouter)
        self.model_combo.setEditable(True)
        self.model_combo.installEventFilter(self)
        self.model_combo.currentTextChanged.connect(self._on_settings_model_changed)

        saved_model = self.config.get("model", "")
        if saved_model in MODELS.get(provider, {}).get("models", []):
            self.model_combo.setCurrentText(saved_model)
        elif saved_model and provider == self.config.get("provider"):
            self.model_combo.setCurrentText(saved_model)

    def _fetch_openrouter_models(self):
        provider = self.provider_combo.currentText()
        if provider != "OpenRouter":
            return
        api_key_widget = self.api_key_widgets.get("OpenRouter", None)
        key = api_key_widget.text().strip() if api_key_widget else ""
        if not key:
            QMessageBox.warning(self, tr("dialog_no_key_title"),
                                tr("dialog_no_key_msg"))
            return

        self.fetch_models_btn.setText(tr("or_fetching"))
        self.fetch_models_btn.setEnabled(False)

        self._or_worker = _OpenRouterFetchWorker(key)
        self._or_worker.done.connect(self._on_openrouter_models_loaded)
        self._or_worker.failed.connect(self._on_openrouter_fetch_failed)
        self._or_worker.start()

    def _on_openrouter_models_loaded(self, models: list):
        current = self.model_combo.currentText()
        self.model_combo.clear()
        for m in models:
            self.model_combo.addItem(m)
        if current:
            self.model_combo.setCurrentText(current)
        self.fetch_models_btn.setText(tr("or_loaded", count=len(models)))
        self.fetch_models_btn.setEnabled(True)

    def _on_openrouter_fetch_failed(self, error: str):
        self.fetch_models_btn.setText(tr("btn_fetch_models"))
        self.fetch_models_btn.setEnabled(True)
        QMessageBox.warning(self, tr("or_fetch_error_title"),
                            tr("or_fetch_error_msg", error=error))

    def _toggle_key_visibility(self, edit: QLineEdit):
        if edit.echoMode() == QLineEdit.EchoMode.Password:
            edit.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            edit.setEchoMode(QLineEdit.EchoMode.Password)

    # ── Hotkey Tab ───────────────────────────────────────────────────────────
    def _build_hotkey_tab(self):
        w = QWidget()
        layout = QVBoxLayout(w)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(14)

        sec = QLabel(tr("section_hotkey"))
        sec.setObjectName("section")
        layout.addWidget(sec)

        cur_row = QHBoxLayout()
        lbl = QLabel(tr("label_current_hotkey"))
        lbl.setProperty("class", "field_label")
        cur_row.addWidget(lbl)
        self.hotkey_display = QLabel(self.config.get("hotkey", "<ctrl>+<shift>+space"))
        self.hotkey_display.setObjectName("hotkey_display")
        cur_row.addWidget(self.hotkey_display)
        cur_row.addStretch()
        layout.addLayout(cur_row)

        inp_row = QHBoxLayout()
        lbl2 = QLabel(tr("label_new_hotkey"))
        lbl2.setProperty("class", "field_label")
        inp_row.addWidget(lbl2)
        self.hotkey_input = QLineEdit()
        self.hotkey_input.setPlaceholderText(tr("hotkey_placeholder"))
        inp_row.addWidget(self.hotkey_input)
        set_btn = QPushButton(tr("btn_set_hotkey"))
        set_btn.setProperty("class", "secondary")
        set_btn.clicked.connect(self._set_hotkey)
        inp_row.addWidget(set_btn)
        layout.addLayout(inp_row)

        hint = QLabel(tr("hotkey_format_hint"))
        hint.setStyleSheet("color: #3a3a6a; font-size: 10px;")
        layout.addWidget(hint)

        div = QFrame(); div.setObjectName("divider")
        layout.addWidget(div)

        sec2 = QLabel(tr("section_system_hotkeys"))
        sec2.setObjectName("section")
        layout.addWidget(sec2)

        note = QLabel(tr("hotkey_note"))
        note.setStyleSheet("color: #5a4a2a; font-size: 11px;")
        note.setWordWrap(True)
        layout.addWidget(note)

        self.hotkeys_list = QListWidget()
        self.hotkeys_list.setMaximumHeight(200)
        refresh_btn = QPushButton(tr("btn_refresh_hotkeys"))
        refresh_btn.setProperty("class", "secondary")
        refresh_btn.clicked.connect(self._load_system_hotkeys)
        layout.addWidget(refresh_btn)
        layout.addWidget(self.hotkeys_list)
        self._load_system_hotkeys()

        layout.addStretch()
        return w

    def _load_system_hotkeys(self):
        self.hotkeys_list.clear()
        for hk in get_system_hotkeys():
            item = QListWidgetItem(hk)
            self.hotkeys_list.addItem(item)

    def _set_hotkey(self):
        new_hk = self.hotkey_input.text().strip()
        if not new_hk:
            QMessageBox.warning(self, tr("dialog_error"), tr("dialog_hotkey_empty"))
            return
        valid, msg = validate_hotkey(new_hk)
        if not valid:
            QMessageBox.warning(self, tr("dialog_invalid_format"), msg)
            return
        self.config["hotkey"] = new_hk
        self.hotkey_display.setText(new_hk)
        self.hotkey_changed.emit(new_hk)
        self.hotkey_input.clear()

    # ── Languages Tab ────────────────────────────────────────────────────────
    def _build_languages_tab(self):
        w = QWidget()
        layout = QVBoxLayout(w)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(14)

        # UI Language selector
        sec_ui = QLabel(tr("section_ui_lang"))
        sec_ui.setObjectName("section")
        layout.addWidget(sec_ui)

        lang_row = QHBoxLayout()
        lbl_ui = QLabel(tr("label_ui_lang"))
        lbl_ui.setProperty("class", "field_label")
        lang_row.addWidget(lbl_ui)
        self.ui_lang_combo = QComboBox()
        current_lang = self.config.get("language", "English")
        for lang in LANGUAGES:
            self.ui_lang_combo.addItem(lang)
        self.ui_lang_combo.blockSignals(True)
        self.ui_lang_combo.setCurrentText(current_lang)
        self.ui_lang_combo.blockSignals(False)
        self.ui_lang_combo.currentTextChanged.connect(self._on_ui_lang_changed)
        lang_row.addWidget(self.ui_lang_combo)
        lang_row.addStretch()
        layout.addLayout(lang_row)

        div = QFrame(); div.setObjectName("divider")
        layout.addWidget(div)

        # Translation languages
        sec = QLabel(tr("section_translate_langs"))
        sec.setObjectName("section")
        layout.addWidget(sec)

        note = QLabel(tr("lang_note"))
        note.setStyleSheet("color: #6060a0; font-size: 11px;")
        layout.addWidget(note)

        available_langs = [
            "Azerbaijani", "English", "Russian", "Turkish", "German",
            "French", "Spanish", "Arabic", "Chinese", "Japanese",
            "Persian", "Italian", "Portuguese", "Ukrainian", "Georgian",
        ]

        self.lang_checkboxes = {}
        current_langs = self.config.get("languages", ["Azerbaijani", "English", "Russian", "Turkish"])

        grid_widget = QWidget()
        grid_layout = QVBoxLayout(grid_widget)
        for lang in available_langs:
            cb = QCheckBox(lang)
            cb.setChecked(lang in current_langs)
            cb.setStyleSheet("QCheckBox { color: #a0a0c0; font-size: 12px; padding: 4px; } "
                             "QCheckBox::indicator { border: 1px solid #2a2a4a; border-radius: 4px; width: 14px; height: 14px; } "
                             "QCheckBox::indicator:checked { background: #5050cc; border-color: #7070ff; }")
            self.lang_checkboxes[lang] = cb
            grid_layout.addWidget(cb)

        scroll = QScrollArea()
        scroll.setWidget(grid_widget)
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: 1px solid #1e1e30; border-radius: 8px; background: #0d0d18; }")
        layout.addWidget(scroll)
        layout.addStretch()
        return w

    def _on_ui_lang_changed(self, lang: str):
        self.config["language"] = lang
        set_language(lang)
        save_config(self.config)
        self.language_changed.emit(lang)
        provider = self.provider_combo.currentText() if hasattr(self, 'provider_combo') else self.config.get("provider", "Anthropic")
        model = self.model_combo.currentText() if hasattr(self, 'model_combo') else self.config.get("model", "")
        tab_index = self._tabs.currentIndex() if hasattr(self, '_tabs') else None
        for attr in list(self.__dict__.keys()):
            if attr in ('hotkey_manager', 'config', 'hotkey_changed', 'language_changed'):
                continue
            try:
                delattr(self, attr)
            except AttributeError:
                pass
        self._setup_ui()
        if hasattr(self, 'provider_combo'):
            idx = self.provider_combo.findText(provider)
            if idx >= 0:
                self.provider_combo.setCurrentIndex(idx)
        if hasattr(self, 'model_combo') and model:
            self.model_combo.setCurrentText(model)
        if tab_index is not None and hasattr(self, '_tabs') and self._tabs.count() > tab_index:
            self._tabs.setCurrentIndex(tab_index)

    # ── Events ────────────────────────────────────────────────────────────────
    def _on_settings_model_changed(self):
        model = self.model_combo.currentText().strip()
        if model:
            self.config["model"] = model
            self.config["provider"] = self.provider_combo.currentText()
            save_config(self.config)

    def eventFilter(self, obj, event):
        if hasattr(self, 'model_combo') and obj is self.model_combo and event.type() == QEvent.Type.FocusIn:
            le = self.model_combo.lineEdit()
            if le:
                QTimer.singleShot(0, le.selectAll)
        return super().eventFilter(obj, event)

    # ── Save ─────────────────────────────────────────────────────────────────
    def _save_all(self):
        self.config["provider"] = self.provider_combo.currentText()
        self.config["model"] = self.model_combo.currentText().strip()

        for provider, edit in self.api_key_widgets.items():
            key = edit.text().strip()
            if key:
                set_api_key(self.config, provider, key)

        selected_langs = [lang for lang, cb in self.lang_checkboxes.items() if cb.isChecked()]
        if len(selected_langs) > 6:
            QMessageBox.warning(self, tr("dialog_warning"), tr("dialog_max_langs"))
            return
        if selected_langs:
            self.config["languages"] = selected_langs

        save_config(self.config)
        QMessageBox.information(self, tr("dialog_saved"), tr("dialog_saved_msg"))


class _OpenRouterFetchWorker(QThread):
    done = Signal(list)
    failed = Signal(str)

    def __init__(self, api_key: str):
        super().__init__()
        self.api_key = api_key

    def run(self):
        try:
            models = fetch_openrouter_models(self.api_key)
            if models:
                self.done.emit(models)
            else:
                self.failed.emit("Boş siyahı qaytarıldı")
        except Exception as e:
            self.failed.emit(str(e))
