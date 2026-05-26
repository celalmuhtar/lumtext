<div align="center">

<img src="ui/app_icon.png" width="64" alt="Lumtext Logo">

# ◈ Lumtext

**AI-Powered Text Processing — Instantly, Anywhere**

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://python.org)
[![PyQt6](https://img.shields.io/badge/PyQt-6.6%2B-41CD52?logo=qt&logoColor=white)](https://www.riverbankcomputing.com/software/pyqt/)
[![Platform](https://img.shields.io/badge/Platform-Linux%20|%20macOS%20|%20Windows-8A2BE2)](#-cross-platform)
[![License](https://img.shields.io/badge/License-MIT-yellow)](#)

</div>

---

## ✨ Key Features

| # | Feature | Description |
|---|---------|-------------|
| 🌐 | **Global Hotkey** | Select text in *any* app, press `Ctrl+Shift+Space` — Lumtext pops up instantly |
| 🤖 | **8 AI Providers** | OpenAI, Anthropic, Google, Groq, DeepSeek, MiniMax, Kimi, OpenRouter (300+ models) |
| ✏️ | **7 Smart Operations** | Fix grammar, translate, summarize, adapt for email, change tone, convert to bullet points |
| 🖥️ | **System Tray** | Runs silently in the background — accessible from your tray at all times |
| 🔄 | **Live Model List** | OpenRouter fetches real-time available models — 300+ at your fingertips |
| 🔍 | **Conflict Detection** | Scans GNOME/KDE for occupied shortcuts so you never pick a conflicting one |
| 🚀 | **Autostart** | Optional system boot autostart — always ready when you need it |
| 🌍 | **Multi-language UI** | English, Azerbaijani, Turkish, Russian — switch on the fly |
| 📋 | **Copy & Replace** | Copy result formatted or plain; replace selected text with one click |

---

## 💡 Why Lumtext?

- **Zero complex setup** — install dependencies, run, done. No framework, no account (just an API key).
- **No AI SDKs** — Everything uses Python's built-in `urllib`. No bloated dependencies.
- **Works everywhere** — system tray on Linux, macOS, and Windows. Fits any workflow.
- **Privacy-first** — your API keys stay in `~/.config/lumtext/settings.json`. No telemetry.
- **Dark theme** — easy on the eyes for long work sessions.
- **Drag & drop popup** — reposition the floating action window anywhere on screen.

---

## 📦 Requirements

| Dependency | Minimum Version | Notes |
|-----------|----------------|-------|
| Python | 3.10+ | |
| PyQt6 | 6.6.0+ | GUI framework |
| pynput | 1.7.6+ | Global hotkey listener (macOS/Windows) |
| platformdirs | 4.0.0+ | Config file path resolution |
| xclip | *system* | Linux PRIMARY selection (install via `apt install xclip`) |

> **Zero AI SDKs required** — all provider APIs are called via Python's standard library `urllib`.

---

## 🚀 Quick Start

### 🐧 Linux

```bash
git clone <repo-url> lumtext
cd lumtext
chmod +x install.sh
./install.sh
```

The installer automatically:
- Checks for Python 3, pip, and installs `xclip`
- Installs PyQt6 system dependencies (`libxcb-cursor0`, etc.)
- Creates a Python virtual environment
- Installs required Python packages
- Creates a `.desktop` launcher
- Optionally enables autostart

**Manual install:**

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 main.py
```

### 🍎 macOS

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
# Grant Accessibility permissions when prompted
python3 main.py
```

Or run the helper script:

```bash
chmod +x install_mac.sh
./install_mac.sh
```

### 🪟 Windows

```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

Or double-click `install_windows.ps1` (run as Administrator if needed).

---

## 📖 Usage Guide

### First Run

1. Launch Lumtext — you'll see a blue **AI** icon in your system tray
2. Right-click the tray icon → **Open Settings**
3. Go to the **Model & API** tab
4. Select your AI provider (e.g., Anthropic, OpenAI)
5. Enter your API key for the chosen provider
6. Pick a model from the dropdown
7. Click **Save**

### Everyday Use

```
1. Highlight text in any application (browser, editor, terminal, etc.)
2. Press Ctrl+Shift+Space (default shortcut)
3. A sleek floating popup appears with your selected text
4. Choose an operation:
   ✎   Fix & simplify sentence
   ⇄   Translate to another language
   ✉   Adapt for email
   ⚡  Summarize
   ⬆  Convert to formal tone
   ⬇  Convert to casual tone
   ⊟  Convert to bullet points
5. Click ▶  Run
6. AI processes your text — result appears in the popup
7. Copy formatted or plain text, or click "Replace" to swap the original
```

### Customizing the Hotkey

If `Ctrl+Shift+Space` conflicts with your system:

1. Right-click tray icon → **Open Settings**
2. Go to the **Shortcuts** tab
3. View currently occupied system shortcuts (auto-scanned from GNOME/KDE)
4. Enter your new shortcut (format: `<ctrl>+<shift>+a`)
5. Click **Set**
6. Click **Save**

### Using OpenRouter (300+ Models)

1. Select **OpenRouter** as your provider
2. Enter your [OpenRouter API key](https://openrouter.ai/keys)
3. Click **⟳ Load models** — fetches an up-to-date model list
4. Start typing to filter 300+ models, or pick from defaults
5. You can also type any model ID manually (e.g., `nousresearch/hermes-3-llama-3.1-405b:free`)

### External Trigger Script

If the global hotkey doesn't work in your environment, you can bind `scripts/trigger.py` to your own keyboard shortcut:

```bash
python3 scripts/trigger.py
```

This sends a signal via the UNIX socket (`/tmp/lumtext.sock`) to trigger the popup with the currently selected text.

---

## 🖼️ Screenshots

| | |
|---|---|
| **Settings Window** — configure providers, API keys, hotkey & language | <img src="screenshots/settings.png" width="320" alt="Settings"> |
| **Action Popup** — press the hotkey to open action selector | <img src="screenshots/popup.png" width="320" alt="Action Popup"> |
| **AI Result** — processed output with copy/replace buttons | <img src="screenshots/result.png" width="320" alt="Result"> |

---

## 🤖 Supported AI Providers

| Provider | Auth Method | Example Models | Config URL |
|----------|------------|----------------|------------|
| **OpenAI** | Bearer Token | GPT-4o, GPT-4-turbo, GPT-3.5-turbo | [API Keys](https://platform.openai.com/api-keys) |
| **Anthropic** | x-api-key | Claude Opus 4.5, Sonnet 4.5, Haiku 4.5 | [Console](https://console.anthropic.com/settings/keys) |
| **Google** | API Key (query) | Gemini 2.0 Flash, 1.5 Pro, 1.5 Flash | [AI Studio](https://aistudio.google.com/apikey) |
| **Groq** | Bearer Token | Llama 3.3-70B, Llama 3.1-8B, Mixtral | [Console](https://console.groq.com/keys) |
| **DeepSeek** | Bearer Token | DeepSeek Chat, DeepSeek Reasoner | — |
| **MiniMax** | Bearer Token | MiniMax-Text-01, abab6.5s-chat | — |
| **Kimi** | Bearer Token | Moonshot v1 (8k/32k/128k) | — |
| **OpenRouter** | Bearer Token | 300+ models (live list) | [Keys](https://openrouter.ai/keys) |

---

## ⚙️ Configuration

**Config file:** `~/.config/lumtext/settings.json`

```json
{
  "provider": "Anthropic",
  "model": "claude-sonnet-4-5",
  "hotkey": "<ctrl>+<shift>+<space>",
  "language": "English",
  "languages": ["Azerbaijani", "English", "Russian", "Turkish"],
  "theme": "dark",
  "window_position": [100, 100],
  "api_keys": {
    "openai": "sk-...",
    "anthropic": "sk-ant-..."
  }
}
```

**Settings window layout:**

| Tab | Settings |
|-----|----------|
| ⚙ **Model & API** | Provider selection, model picker, API keys (masked, with reveal toggle) |
| ⌨ **Shortcuts** | Current hotkey display, new hotkey input, occupied shortcuts list |
| 🌐 **Languages** | UI language selector, translation language checkboxes (max 6) |

---

## 🏗️ Architecture

```
main.py
 ├── ConfigManager          ← ~/.config/lumtext/settings.json
 ├── HotkeyManager
 │    ├── SelectionWatcher  ← PRIMARY selection (xclip) 250ms poll
 │    └── TriggerListener   ← UNIX socket /tmp/lumtext.sock
 ├── ActionPopup (PyQt6)
 │    ├── AIWorker (QThread) → call_ai() → 8 providers via urllib
 │    └── Clipboard         ← xclip / pbcopy / win32clipboard
 └── SettingsWindow
      └── OpenRouterFetchWorker (QThread)
```

**Execution flow:**

```
1. main.py starts in the system tray
2. SelectionWatcher continuously polls PRIMARY selection (Linux) or
   listens for global hotkey (macOS/Windows via pynput)
3. User presses hotkey → TriggerListener activates
4. Popup appears with the selected text and action chooser
5. User selects an action and clicks Run
6. AIWorker sends the request to the selected AI provider in a background thread
7. Result appears in the popup — copy formatted, plain, or replace original text
```

**Cross-platform clipboard handling:**

| Platform | Get Selection | Set Clipboard |
|----------|--------------|---------------|
| Linux | `xclip` (PRIMARY), fallback `xdotool`+`xclip`, `xsel` | PyQt6 `QClipboard` |
| macOS | `osascript` (Cmd+C) + `pbpaste` | `pbcopy` / PyQt6 |
| Windows | Win32 API (`keybd_event` + `GetClipboardData`) | Win32 API / PyQt6 |

---

## 🛠️ Development

```bash
git clone <repo-url>
cd lumtext
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 main.py
```

**Project structure:**

```
lumtext/
├── main.py                  # Entry point — app init, tray, hotkey
├── requirements.txt         # Python dependencies
├── install.sh               # Linux installer
├── install_mac.sh           # macOS installer
├── install_windows.ps1      # Windows installer
├── ui/
│   ├── action_popup.py      # Floating popup UI (QDialog)
│   ├── settings_window.py   # Settings window (QMainWindow)
│   ├── app_icon.png         # Application icon (1024×1024)
│   ├── arrow.png            # Dropdown arrow (PNG)
│   └── arrow.svg            # Dropdown arrow (SVG)
├── core/
│   ├── ai_handler.py        # AI provider integrations (8 providers)
│   ├── clipboard.py         # Cross-platform clipboard (xclip/pbcopy/win32)
│   ├── config_manager.py    # JSON config load/save (~/.config/lumtext)
│   ├── hotkey_manager.py    # Global hotkey + selection watcher
│   └── localization.py      # i18n (EN, AZ, TR, RU)
└── scripts/
    └── trigger.py           # External trigger via UNIX socket
```

---

## 🌐 Read this in other languages

| Language | README |
|----------|--------|
| 🇦🇿 Azərbaycan dili | [README.az.md](README.az.md) |
| 🇹🇷 Türkçe | [README.tr.md](README.tr.md) |
| 🇷🇺 Русский | [README.ru.md](README.ru.md) |

---

<div align="center">

**Lumtext** — Select. Press. Transform.

</div>
