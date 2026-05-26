import subprocess
import threading
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QRadioButton,
    QComboBox, QLabel, QPushButton, QFrame, QButtonGroup,
    QProgressBar, QScrollArea, QWidget, QTextEdit, QSizePolicy, QCompleter
)
from PyQt6.QtCore import Qt, QEvent, QThread, pyqtSignal, QPoint, QTimer, QSortFilterProxyModel
from PyQt6.QtGui import QFont, QColor, QPalette, QKeySequence, QShortcut, QCursor

from pathlib import Path

from core.ai_handler import call_ai, build_prompt, MODELS, fetch_openrouter_models
from core.clipboard import get_selected_text, set_clipboard, set_clipboard_html
from core.config_manager import load_config, save_config, get_api_key
from core.localization import tr, set_language

_ARROW_PATH = str(Path(__file__).parent / "arrow.png")


class AIWorker(QThread):
    finished = pyqtSignal(str)
    error = pyqtSignal(str)

    def __init__(self, provider, model, api_key, action, text, language=""):
        super().__init__()
        self.provider = provider
        self.model = model
        self.api_key = api_key
        self.action = action
        self.text = text
        self.language = language

    def run(self):
        try:
            prompt = build_prompt(self.action, self.text, self.language)
            result = call_ai(self.provider, self.model, self.api_key, prompt)
            self.finished.emit(result)
        except Exception as e:
            self.error.emit(str(e))


def _md_to_html(text: str) -> str:
    import re
    text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
    text = re.sub(r'(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)', r'<i>\1</i>', text)
    text = re.sub(r'__(.+?)__', r'<u>\1</u>', text)
    text = re.sub(r'~~(.+?)~~', r'<s>\1</s>', text)
    text = re.sub(r'`(.+?)`', r'<code>\1</code>', text)
    text = re.sub(r'\n{2,}', '</p><p>', text.strip())
    text = re.sub(r'\n', '<br>', text)
    return f'<p>{text}</p>'


class ActionPopup(QDialog):
    def __init__(self, selected_text: str = "", parent=None):
        super().__init__(parent)
        self.config = load_config()
        set_language(self.config.get("language", "English"))
        self.selected_text = selected_text or get_selected_text()
        self.result_text = ""
        self.worker = None
        self._drag_pos = None

        self._setup_window()
        self._setup_ui()
        self._center_on_screen()

    def _setup_window(self):
        self.setWindowTitle(tr("title"))
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setMinimumWidth(380)
        ss = """
            QDialog {
                background: transparent;
            }
            #main_frame {
                background: #0f0f13;
                border: 1px solid #2a2a3a;
                border-radius: 16px;
            }
            QLabel#title_label {
                color: #e0e0f0;
                font-size: 13px;
                font-weight: 600;
                font-family: 'JetBrains Mono', 'Fira Code', monospace;
                letter-spacing: 1px;
            }
            QLabel#subtitle {
                color: #5a5a7a;
                font-size: 10px;
                font-family: 'JetBrains Mono', monospace;
            }
            QLabel#section_label {
                color: #6060aa;
                font-size: 10px;
                font-weight: 600;
                font-family: 'JetBrains Mono', monospace;
                letter-spacing: 2px;
                text-transform: uppercase;
            }
            QRadioButton {
                color: #b0b0d0;
                font-size: 12px;
                font-family: 'Segoe UI', 'Inter', 'Ubuntu', sans-serif;
                padding: 6px 12px 6px 4px;
                border-radius: 8px;
                spacing: 6px;
                border: 1px solid transparent;
            }
            QRadioButton:hover {
                background: #14142a;
                color: #e0e0f8;
                border: 1px solid #2a2a5a;
            }
            QRadioButton:checked {
                color: #c0c0ff;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #181840, stop:1 #12122e);
                border: 1px solid #3a3a8a;
                font-weight: 500;
            }
            QRadioButton::indicator {
                width: 14px;
                height: 14px;
                border-radius: 7px;
                border: 2px solid #3a3a6a;
                background: transparent;
            }
            QRadioButton::indicator:hover {
                border-color: #6060cc;
            }
            QRadioButton::indicator:checked {
                background: qradialgradient(cx:0.5, cy:0.5, radius:0.4,
                    fx:0.5, fy:0.5, stop:0 #8080ff, stop:1 #4040cc);
                border-color: #7070ee;
            }
            QComboBox {
                background: #12122a;
                color: #c0c0d8;
                border: 1px solid #2a2a5a;
                border-radius: 8px;
                padding: 4px 10px;
                font-size: 11px;
                font-family: 'Segoe UI', 'Inter', sans-serif;
            }
            QComboBox:focus, QComboBox:hover { border-color: #5050aa; }
            QComboBox::drop-down {
                border: none;
                width: 26px;
            }
            QComboBox::down-arrow {
                image: url(_ARROW_PLACEHOLDER_);
                width: 12px;
                height: 8px;
            }
            QComboBox QAbstractItemView {
                background: #0f0f1e;
                color: #b0b0d0;
                border: 1px solid #2a2a5a;
                border-radius: 6px;
                selection-background-color: #1a1a4a;
                padding: 4px;
                outline: none;
            }
            QComboBox QAbstractItemView::item {
                padding: 6px 10px;
                border-radius: 4px;
                min-height: 20px;
            }
            QComboBox QAbstractItemView::item:hover {
                background: #1a1a3a;
                color: #d0d0f0;
            }
            QComboBox#provider_combo { min-width: 120px; }
            QComboBox#model_combo { min-width: 170px; }
            QPushButton#fetch_btn {
                background: #12122a;
                color: #8080dd;
                border: 1px solid #2a2a5a;
                border-radius: 8px;
                padding: 4px 10px;
                font-size: 13px;
                min-width: 32px;
            }
            QPushButton#fetch_btn:hover { border-color: #5050aa; color: #a0a0ff; }
            QPushButton#replace_btn {
                background: #1a2a1a;
                color: #50c050;
                border: 1px solid #2a5a2a;
                border-radius: 8px;
                padding: 6px 14px;
                font-size: 11px;
            }
            QPushButton#replace_btn:hover { background: #2a3a2a; }
            QProgressBar#progress_bar {
                background: #0a0a14;
                border: none;
                border-radius: 2px;
                text-align: center;
            }
            QProgressBar#progress_bar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #20c060, stop:0.5 #40e080, stop:1 #20c060);
                border-radius: 2px;
            }
            QPushButton#run_btn {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #4040cc, stop:1 #7040cc);
                color: white;
                border: none;
                border-radius: 10px;
                padding: 10px 24px;
                font-size: 13px;
                font-weight: 600;
            }
            QPushButton#run_btn:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #5050dd, stop:1 #8050dd);
            }
            QPushButton#run_btn:disabled { background: #2a2a4a; color: #505070; }
            QPushButton#cancel_btn {
                background: transparent;
                color: #5a5a8a;
                border: 1px solid #2a2a4a;
                border-radius: 10px;
                padding: 10px 18px;
                font-size: 12px;
            }
            QPushButton#cancel_btn:hover { color: #c0c0d8; border-color: #4a4a6a; }
            QPushButton#copy_btn {
                background: #1a3a1a;
                color: #60c060;
                border: 1px solid #2a5a2a;
                border-radius: 8px;
                padding: 6px 14px;
                font-size: 11px;
            }
            QPushButton#copy_btn:hover { background: #2a4a2a; }
            QTextEdit#result_box {
                background: #080810;
                color: #d0d0e8;
                border: 1px solid #2a2a4a;
                border-radius: 8px;
                font-size: 12px;
                font-family: 'Ubuntu', sans-serif;
                padding: 8px;
            }
            QTextEdit#result_box code {
                background: #1a1a2a;
                color: #80c080;
                border-radius: 3px;
                padding: 1px 4px;
                font-family: 'JetBrains Mono', monospace;
                font-size: 11px;
            }
            QTextEdit#preview_box {
                background: #0a0a14;
                color: #6a6a8a;
                border: 1px solid #1a1a2a;
                border-radius: 6px;
                font-size: 11px;
                padding: 6px;
            }
            QTextEdit#preview_box code {
                background: #12121e;
                border-radius: 2px;
                padding: 1px 3px;
                font-family: 'JetBrains Mono', monospace;
            }
            QLabel#status_label {
                color: #6060aa;
                font-size: 11px;
                font-family: 'JetBrains Mono', monospace;
            }
        """
        ss = ss.replace("_ARROW_PLACEHOLDER_", _ARROW_PATH)
        self.setStyleSheet(ss)

    def _setup_ui(self):
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)

        frame = QFrame()
        frame.setObjectName("main_frame")
        self.frame = frame
        outer.addWidget(frame)

        frame.installEventFilter(self)
        for child in frame.findChildren(QWidget):
            child.installEventFilter(self)

        layout = QVBoxLayout(frame)
        layout.setContentsMargins(20, 18, 20, 18)
        layout.setSpacing(12)

        # Header
        header = QHBoxLayout()
        self._title_label = QLabel(tr("title"))
        self._title_label.setObjectName("title_label")
        header.addWidget(self._title_label)
        header.addStretch()

        self.provider_combo = QComboBox()
        self.provider_combo.setObjectName("provider_combo")
        self.provider_combo.setMinimumWidth(110)
        self.model_combo = QComboBox()
        self.model_combo.setObjectName("model_combo")
        self.model_combo.setMinimumWidth(170)

        self.fetch_btn = QPushButton("⟳")
        self.fetch_btn.setObjectName("fetch_btn")
        self.fetch_btn.setToolTip(tr("fetch_tooltip"))
        self.fetch_btn.clicked.connect(self._fetch_openrouter_models)
        self.fetch_btn.hide()

        current_provider = self.config.get("provider", "")
        current_model = self.config.get("model", "")

        for p in sorted(MODELS.keys()):
            label = tr("provider_no_key", p=p) if not get_api_key(self.config, p) else p
            self.provider_combo.addItem(label, p)

        idx = self.provider_combo.findData(current_provider)
        if idx >= 0:
            self.provider_combo.setCurrentIndex(idx)

        self._populate_models()
        self._setup_model_completer()
        self._update_model_ui(current_provider)

        midx = self.model_combo.findText(current_model)
        if midx >= 0:
            self.model_combo.setCurrentIndex(midx)
        elif current_model:
            self.model_combo.setEditText(current_model)

        self.provider_combo.currentIndexChanged.connect(self._on_provider_changed)
        self.model_combo.currentTextChanged.connect(self._on_model_changed)

        header.addWidget(self.provider_combo)
        header.addWidget(self.model_combo)
        header.addWidget(self.fetch_btn)
        layout.addLayout(header)

        # Divider
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setStyleSheet("color: #1a1a2a;")
        layout.addWidget(line)

        # Selected text preview
        if self.selected_text:
            sec = QLabel(tr("section_selected"))
            sec.setObjectName("section_label")
            self._sec_selected = sec
            layout.addWidget(sec)
            preview = QTextEdit()
            preview.setObjectName("preview_box")
            preview.setHtml(_md_to_html(self.selected_text[:300] + ("…" if len(self.selected_text) > 300 else "")))
            preview.setReadOnly(True)
            preview.setMaximumHeight(80)
            layout.addWidget(preview)
        else:
            warn = QLabel(tr("no_text_warning"))
            warn.setStyleSheet("color: #cc8030; font-size: 11px;")
            self._warn_label = warn
            layout.addWidget(warn)

        # Actions panel (collapsible)
        self.actions_panel = QWidget()
        self.actions_panel.setObjectName("actions_panel")
        actions_layout = QVBoxLayout(self.actions_panel)
        actions_layout.setContentsMargins(0, 0, 0, 0)
        actions_layout.setSpacing(8)

        sec2 = QLabel(tr("section_action"))
        sec2.setObjectName("section_label")
        self._sec_action = sec2
        actions_layout.addWidget(sec2)

        self.btn_group = QButtonGroup(self)
        self.translate_combo = None

        actions = [
            ("format",      "✎", "action_format"),
            ("translate",   "⇄", "action_translate"),
            ("email",       "✉", "action_email"),
            ("summarize",   "⚡", "action_summarize"),
            ("tone_formal", "⬆", "action_tone_formal"),
            ("tone_casual", "⬇", "action_tone_casual"),
            ("bulletpoints","⊟", "action_bulletpoints"),
        ]

        self._radio_actions = {}
        for key, icon_char, tr_key in actions:
            row = QHBoxLayout()
            row.setContentsMargins(0, 0, 0, 0)
            row.setSpacing(10)

            icon_label = QLabel(icon_char)
            icon_label.setFixedWidth(28)
            icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            icon_label.setStyleSheet("""
                font-size: 18px;
                color: #30cc70;
                font-weight: 500;
            """)

            rb = QRadioButton(tr(tr_key))
            self.btn_group.addButton(rb)
            rb.setProperty("action_key", key)
            rb.setProperty("tr_key", tr_key)
            row.addWidget(icon_label)
            row.addWidget(rb, 1)
            actions_layout.addLayout(row)
            self._radio_actions[key] = rb

            if key == "translate":
                langs_row = QHBoxLayout()
                langs_row.setContentsMargins(38, 0, 0, 0)
                lbl = QLabel(tr("translate_lang_label"))
                lbl.setStyleSheet("color: #5a5a8a; font-size: 11px;")
                self._translate_lbl = lbl
                langs_row.addWidget(lbl)
                self.translate_combo = QComboBox()
                for lang in self.config.get("languages", ["English", "Russian", "Turkish", "Azerbaijani"]):
                    self.translate_combo.addItem(lang)
                langs_row.addWidget(self.translate_combo)
                langs_row.addStretch()
                actions_layout.addLayout(langs_row)

        # Select first by default
        list(self._radio_actions.values())[0].setChecked(True)

        layout.addWidget(self.actions_panel)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setObjectName("progress_bar")
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(0)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setFixedHeight(4)
        self.progress_bar.hide()
        layout.addWidget(self.progress_bar)

        # Result area
        self.result_box = QTextEdit()
        self.result_box.setObjectName("result_box")
        self.result_box.setPlaceholderText(tr("result_placeholder"))
        self.result_box.setMinimumHeight(60)
        self.result_box.setMaximumHeight(400)
        self.result_box.hide()
        layout.addWidget(self.result_box)

        # Status
        self.status_label = QLabel("")
        self.status_label.setObjectName("status_label")
        layout.addWidget(self.status_label)

        # Buttons
        btn_row = QHBoxLayout()
        self.run_btn = QPushButton(tr("btn_run"))
        self.run_btn.setObjectName("run_btn")
        self.run_btn.clicked.connect(self._run_action)
        if not self.selected_text:
            self.run_btn.setEnabled(False)

        self.cancel_btn = QPushButton(tr("btn_cancel"))
        self.cancel_btn.setObjectName("cancel_btn")
        self.cancel_btn.clicked.connect(self.close)

        self.copy_btn = QPushButton(tr("btn_copy_fmt"))
        self.copy_btn.setObjectName("copy_btn")
        self.copy_btn.clicked.connect(self._copy_result)
        self.copy_btn.hide()

        self.copy_plain_btn = QPushButton(tr("btn_copy_plain"))
        self.copy_plain_btn.setObjectName("copy_btn")
        self.copy_plain_btn.clicked.connect(self._copy_plain)
        self.copy_plain_btn.hide()

        self.replace_btn = QPushButton(tr("btn_replace"))
        self.replace_btn.setObjectName("replace_btn")
        self.replace_btn.setToolTip(tr("replace_tooltip"))
        self.replace_btn.clicked.connect(self._replace_text)
        self.replace_btn.hide()

        self.toggle_actions_btn = QPushButton(tr("btn_actions"))
        self.toggle_actions_btn.setObjectName("cancel_btn")
        self.toggle_actions_btn.clicked.connect(self._toggle_actions)
        self.toggle_actions_btn.hide()

        btn_row.addWidget(self.cancel_btn)
        btn_row.addWidget(self.toggle_actions_btn)
        btn_row.addStretch()
        btn_row.addWidget(self.replace_btn)
        btn_row.addWidget(self.copy_plain_btn)
        btn_row.addWidget(self.copy_btn)
        btn_row.addWidget(self.run_btn)
        layout.addLayout(btn_row)

        # ESC to close
        esc = QShortcut(QKeySequence("Escape"), self)
        esc.activated.connect(self.close)

    def _retranslate_ui(self):
        self._title_label.setText(tr("title"))
        self.run_btn.setText(tr("btn_rerun") if self.result_text else tr("btn_run"))
        self.cancel_btn.setText(tr("btn_cancel"))
        self.copy_btn.setText(tr("btn_copy_fmt"))
        self.copy_plain_btn.setText(tr("btn_copy_plain"))
        self.replace_btn.setText(tr("btn_replace"))
        self.fetch_btn.setToolTip(tr("fetch_tooltip"))
        self.result_box.setPlaceholderText(tr("result_placeholder"))
        if hasattr(self, '_toggle_actions_btn'):
            self.toggle_actions_btn.setText(tr("btn_actions"))
        if hasattr(self, '_sec_selected'):
            self._sec_selected.setText(tr("section_selected"))
        if hasattr(self, '_sec_action'):
            self._sec_action.setText(tr("section_action"))
        if hasattr(self, '_warn_label'):
            self._warn_label.setText(tr("no_text_warning"))
        if hasattr(self, '_translate_lbl'):
            self._translate_lbl.setText(tr("translate_lang_label"))
        for rb in self._radio_actions.values():
            tr_key = rb.property("tr_key")
            if tr_key:
                rb.setText(tr(tr_key))

    def eventFilter(self, obj, event):
        if hasattr(self, 'model_combo') and obj is self.model_combo and event.type() == QEvent.Type.FocusIn:
            le = self.model_combo.lineEdit()
            if le:
                QTimer.singleShot(0, le.selectAll)
        elif obj is self.frame and event.type() == event.Type.MouseButtonPress and event.button() == Qt.MouseButton.LeftButton:
            self._drag_pos = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            return True
        elif obj is self.frame and event.type() == event.Type.MouseMove and self._drag_pos is not None:
            self.move(event.globalPosition().toPoint() - self._drag_pos)
            return True
        elif obj is self.frame and event.type() == event.Type.MouseButtonRelease and event.button() == Qt.MouseButton.LeftButton:
            self._drag_pos = None
            return False
        return super().eventFilter(obj, event)

    def _center_on_screen(self):
        self.adjustSize()
        screen = self.screen()
        if screen is None:
            return
        geo = screen.availableGeometry()
        x = geo.x() + (geo.width() - self.width()) // 2
        y = geo.y() + (geo.height() - self.height()) // 2
        self.move(x, y)

    def _populate_models(self):
        self.model_combo.setEditable(True)
        self.model_combo.blockSignals(True)
        self.model_combo.clear()
        provider = self.provider_combo.currentData()
        if provider and provider in MODELS:
            for m in MODELS[provider]["models"]:
                self.model_combo.addItem(m)
        self.model_combo.blockSignals(False)

    def _setup_model_completer(self):
        combo_model = self.model_combo.model()
        if combo_model is None:
            return
        self._model_proxy = QSortFilterProxyModel(self)
        self._model_proxy.setFilterCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self._model_proxy.setSourceModel(combo_model)
        completer = QCompleter(self._model_proxy, self)
        completer.setCompletionMode(QCompleter.CompletionMode.PopupCompletion)
        completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        completer.setFilterMode(Qt.MatchFlag.MatchContains)
        self.model_combo.setCompleter(completer)

    def _update_model_ui(self, provider: str):
        is_openrouter = (provider == "OpenRouter")
        self.model_combo.setEditable(True)
        self.model_combo.installEventFilter(self)
        self.fetch_btn.setVisible(is_openrouter)

    def _on_provider_changed(self):
        self._populate_models()
        self._setup_model_completer()
        provider = self.provider_combo.currentData()
        self._update_model_ui(provider)
        if provider:
            self.config["provider"] = provider
            model = self.model_combo.currentText()
            if model:
                self.config["model"] = model
            save_config(self.config)

    def _on_model_changed(self):
        model = self.model_combo.currentText()
        if model:
            self.config["model"] = model
            provider = self.provider_combo.currentData()
            if provider:
                self.config["provider"] = provider
            save_config(self.config)

    def _fetch_openrouter_models(self):
        provider = self.provider_combo.currentData()
        if provider != "OpenRouter":
            return
        api_key = get_api_key(self.config, "OpenRouter")
        if not api_key:
            self.status_label.setText(tr("fetch_status_no_key"))
            return
        self.fetch_btn.setText("⏳")
        self.fetch_btn.setEnabled(False)
        self._or_worker = _OpenRouterFetchWorker(api_key)
        self._or_worker.done.connect(self._on_openrouter_models_loaded)
        self._or_worker.failed.connect(self._on_openrouter_fetch_failed)
        self._or_worker.start()

    def _on_openrouter_models_loaded(self, models: list):
        current = self.model_combo.currentText()
        self.model_combo.blockSignals(True)
        self.model_combo.clear()
        for m in models:
            self.model_combo.addItem(m)
        if current and current not in models:
            self.model_combo.setEditText(current)
        elif current:
            self.model_combo.setCurrentText(current)
        self.model_combo.blockSignals(False)
        self._setup_model_completer()
        self.fetch_btn.setText("✓")
        self.fetch_btn.setEnabled(True)

    def _on_openrouter_fetch_failed(self, error: str):
        self.fetch_btn.setText("⟳")
        self.fetch_btn.setEnabled(True)
        self.status_label.setText(tr("fetch_status_error", error=error[:40]))

    def _get_selected_action(self):
        checked = self.btn_group.checkedButton()
        if checked:
            return checked.property("action_key")
        return "format"

    def _run_action(self):
        if not self.selected_text:
            return

        action = self._get_selected_action()
        language = ""
        if action == "translate" and self.translate_combo:
            language = self.translate_combo.currentText()

        provider = self.config.get("provider", "Anthropic")
        model = self.config.get("model", "claude-sonnet-4-5")
        api_key = get_api_key(self.config, provider)

        if not api_key:
            self.status_label.setText(tr("status_api_missing"))
            return

        self.result_text = ""
        self.result_box.clear()
        self.result_box.setMinimumHeight(60)

        self.run_btn.setEnabled(False)
        self.run_btn.setText(tr("btn_waiting"))
        self.status_label.setText(tr("status_processing"))
        self.progress_bar.show()
        self.result_box.hide()
        self.copy_btn.hide()
        self.copy_plain_btn.hide()
        self.replace_btn.hide()
        self.toggle_actions_btn.hide()
        self.actions_panel.show()

        self.adjustSize()

        self.worker = AIWorker(provider, model, api_key, action, self.selected_text, language)
        self.worker.finished.connect(self._on_result)
        self.worker.error.connect(self._on_error)
        self.worker.start()

    def _on_result(self, text: str):
        self.result_text = text
        self.progress_bar.hide()
        self.result_box.setHtml(_md_to_html(text))
        self.result_box.show()
        self.result_box.setMinimumHeight(120)
        self.copy_btn.show()
        self.copy_plain_btn.show()
        self.replace_btn.show()
        self.toggle_actions_btn.show()
        self.run_btn.setEnabled(True)
        self.run_btn.setText(tr("btn_rerun"))
        self.status_label.setText(tr("status_ready"))
        self.actions_panel.hide()
        self.adjustSize()
        h = self.sizeHint().height()
        self.resize(self.width(), min(h, 520))

    def _toggle_actions(self):
        if self.actions_panel.isVisible():
            self.actions_panel.hide()
            self.toggle_actions_btn.setText(tr("btn_actions"))
        else:
            self.actions_panel.show()
            self.toggle_actions_btn.setText(tr("btn_actions_hide"))
        self.adjustSize()

    def _on_error(self, error: str):
        self.progress_bar.hide()
        self.status_label.setText(tr("status_error", error=error[:80]))
        self.run_btn.setEnabled(True)
        self.run_btn.setText(tr("btn_run"))

    def _copy_result(self):
        if self.result_text:
            html = self.result_box.toHtml()
            plain = self.result_box.toPlainText()
            set_clipboard_html(html, plain)
            self.copy_btn.setText(tr("copy_success_fmt"))
            QTimer.singleShot(2000, lambda: self.copy_btn.setText(tr("btn_copy_fmt")))

    def _copy_plain(self):
        if self.result_text:
            set_clipboard(self.result_box.toPlainText())
            self.copy_plain_btn.setText(tr("copy_success_plain"))
            QTimer.singleShot(2000, lambda: self.copy_plain_btn.setText(tr("btn_copy_plain")))

    def _replace_text(self):
        if not self.result_text:
            return
        html = self.result_box.toHtml()
        plain = self.result_box.toPlainText()
        set_clipboard_html(html, plain)
        self.hide()
        QTimer.singleShot(250, self._send_ctrl_v)

    def _send_ctrl_v(self):
        try:
            from pynput.keyboard import Key, Controller
            kb = Controller()
            kb.press(Key.ctrl)
            kb.press('v')
            kb.release('v')
            kb.release(Key.ctrl)
        except Exception:
            pass
        self.close()


class _OpenRouterFetchWorker(QThread):
    done = pyqtSignal(list)
    failed = pyqtSignal(str)

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
