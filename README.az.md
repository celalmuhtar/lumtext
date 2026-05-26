<div align="center">

<img src="ui/app_icon.png" width="64" alt="Lumtext Loqosu">

# ◈ Lumtext

🇬🇧 [English](README.md) · 🇹🇷 [Türkçe](README.tr.md) · 🇷🇺 [Русский](README.ru.md)

**AI ilə Mətn Emalı — Dərhal, İstənilən Yerdə**

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://python.org)
[![PyQt6](https://img.shields.io/badge/PyQt-6.6%2B-41CD52?logo=qt&logoColor=white)](https://www.riverbankcomputing.com/software/pyqt/)
[![Platform](https://img.shields.io/badge/Platform-Linux%20|%20macOS%20|%20Windows-8A2BE2)](#-çarpaz-platforma)
[![Lisenziya](https://img.shields.io/badge/Lisenziya-MIT-sarı)](#)

</div>

---

## ✨ Əsas Xüsusiyyətlər

| # | Xüsusiyyət | Təsvir |
|---|-----------|--------|
| 🌐 | **Qlobal Qısayol** | İstənilən proqramda mətni seçin, `Ctrl+Shift+Space` basın — Lumtext dərhal açılır |
| 🤖 | **8 AI Provayder** | OpenAI, Anthropic, Google, Groq, DeepSeek, MiniMax, Kimi, OpenRouter (300+ model) |
| ✏️ | **7 Ağıllı Əməliyyat** | Qrammatikanı düzəlt, tərcümə et, xülasə et, email üçün uyğunlaşdır, üslubu dəyiş, siyahıya çevir |
| 🖥️ | **Sistem Tray** | Arxa planda səssizcə işləyir — hər an tray-dan əlçatandır |
| 🔄 | **Canlı Model Siyahısı** | OpenRouter real-time model siyahısı yükləyir — 300+ model barmaqlarınızın ucunda |
| 🔍 | **Konflikt Aşkarlama** | GNOME/KDE sistem qısayollarını skan edərək məşğul düymələri göstərir |
| 🚀 | **Avtostart** | Sistemlə birlikdə avtomatik başlanğıc — hər an hazır |
| 🌍 | **Çoxdilli İnterfeys** | Azərbaycan, İngilis, Türk, Rus dilləri — anında keçid |
| 📋 | **Kopyala & Əvəz et** | Nəticəni formatlı və ya düz kopyalayın; bir kliklə seçilmiş mətni əvəz edin |

---

## 💡 Niyə Lumtext?

- **Sadə quraşdırma** — asılılıqları yüklə, işə sal, hazır. Heç bir framework, yalnız API açarı.
- **AI SDK-ları yoxdur** — Bütün API sorğuları Python `urllib` ilə. Artıq yük yoxdur.
- **Hər yerdə işləyir** — Linux, macOS, Windows sistem tray. İstənilən iş axınına uyğundur.
- **Məxfilik ön planda** — API açarları `~/.config/lumtext/settings.json`-da qalır. Heç bir telemetriya.
- **Tünd tema** — uzun iş saatları üçün gözəl dizayn.
- **Popup daşına bilər** — üzən pəncərəni istənilən yerə sürükləyin.

---

## 📦 Tələblər

| Asılılıq | Minimum Versiya | Qeydlər |
|-----------|----------------|--------|
| Python | 3.10+ | |
| PyQt6 | 6.6.0+ | GUI framework |
| pynput | 1.7.6+ | Qlobal qısayol (macOS/Windows) |
| platformdirs | 4.0.0+ | Konfiq yolu təyini |
| xclip | *sistem* | Linux PRIMARY seçimi (`apt install xclip`) |

> **AI SDK-ları tələb olunmur** — bütün provayderlər Python `urllib` ilə çağırılır.

---

## 🚀 Qısa Başlanğıc

### 🐧 Linux

```bash
git clone <repo-url> lumtext
cd lumtext
chmod +x install.sh
./install.sh
```

Quraşdırma skripti avtomatik:
- Python 3, pip yoxlayır və `xclip` quraşdırır
- PyQt6 sistem asılılıqlarını yükləyir (`libxcb-cursor0` və s.)
- Python virtual mühiti yaradır
- Tələb olunan paketləri quraşdırır
- `.desktop` qısayolu yaradır
- İstəyə bağlı avtostart aktiv edir

**Əl ilə quraşdırma:**

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
# İcazə soruşulduqda Giriş imkanlarına icazə verin
python3 main.py
```

### 🪟 Windows

```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

---

## 📖 İstifadə Təlimatı

### İlk İşə Salma

1. Lumtext-i işə salın — sistem tray-da mavi **AI** ikonu görünəcək
2. Tray ikonasına sağ klik → **Ayarları Aç**
3. **Model & API** sekmesine keçin
4. AI provayder seçin (məsələn, Anthropic, OpenAI)
5. API açarınızı daxil edin
6. Model seçin
7. **Yadda saxla** düyməsinə basın

### Gündəlik İstifadə

```
1. İstənilən proqramda mətni seçin (brauzer, redaktor, terminal)
2. Ctrl+Shift+Space basın (standart qısayol)
3. Seçilmiş mətn ilə üzən popup pəncərəsi açılır
4. Əməliyyat seçin:
   ✎   Cümləni düzəlt & sadələşdir
   ⇄   Tərcümə et
   ✉   Email üçün uyğunlaşdır
   ⚡  Xülasə et
   ⬆  Rəsmi (formal) üsluba çevir
   ⬇  Gündəlik (informal) üsluba çevir
   ⊟  Bullet point siyahısına çevir
5. ▶  İcra et düyməsinə basın
6. AI mətni emal edir — nəticə popup-da görünür
7. Formatlı və ya düz kopyalayın, yaxud "Əvəz et" ilə orijinalı dəyişin
```

### Qısayolu Dəyişmək

1. Tray ikonasına sağ klik → **Ayarları Aç**
2. **Qısayollar** sekmesine keçin
3. Sistemdə məşğul qısayolları görün (GNOME/KDE avtomatik skan)
4. Yeni qısayol daxil edin (format: `<ctrl>+<shift>+a`)
5. **Təyin et** düyməsinə basın
6. **Yadda saxla** düyməsinə basın

### OpenRouter (300+ Model)

1. Provayder olaraq **OpenRouter** seçin
2. [OpenRouter API açarınızı](https://openrouter.ai/keys) daxil edin
3. **⟳ Modelləri yüklə** vurun — ən son model siyahısı yüklənir
4. 300+ model arasında axtarış edin
5. İstənilən model ID-sini əl ilə yaza bilərsiniz

### Xarici Trigger Skripti

Qısayol işləmirsə, `scripts/trigger.py` skriptini öz qısayol bağlamanıza əlavə edin:

```bash
python3 scripts/trigger.py
```

Bu, UNIX socket (`/tmp/lumtext.sock`) vasitəsilə Lumtext-ə siqnal göndərir.

---

## 🖼️ Ekran Görüntüləri

| | |
|---|---|
| **Ayarlar Pəncərəsi** — provayder, API açarları, qısayol və dil konfiqurasiyası | <img src="screenshots/settings.png" width="320" alt="Ayarlar"> |
| **Action Popup** — qısayolu basdıqdan sonra açılan əməliyyat seçici | <img src="screenshots/popup.png" width="320" alt="Popup"> |
| **AI Nəticəsi** — işlənmiş nəticə kopyala/əvəz et düymələri ilə | <img src="screenshots/result.png" width="320" alt="Nəticə"> |

---

## 🤖 Dəstəklənən AI Provayderləri

| Provayder | Auth metodu | Nümunə Modellər | Konfiq URL |
|----------|------------|----------------|------------|
| **OpenAI** | Bearer Token | GPT-4o, GPT-4-turbo, GPT-3.5-turbo | [API Keys](https://platform.openai.com/api-keys) |
| **Anthropic** | x-api-key | Claude Opus 4.5, Sonnet 4.5, Haiku 4.5 | [Console](https://console.anthropic.com/settings/keys) |
| **Google** | API Key | Gemini 2.0 Flash, 1.5 Pro, 1.5 Flash | [AI Studio](https://aistudio.google.com/apikey) |
| **Groq** | Bearer Token | Llama 3.3-70B, Llama 3.1-8B, Mixtral | [Console](https://console.groq.com/keys) |
| **DeepSeek** | Bearer Token | DeepSeek Chat, DeepSeek Reasoner | — |
| **MiniMax** | Bearer Token | MiniMax-Text-01, abab6.5s-chat | — |
| **Kimi** | Bearer Token | Moonshot v1 (8k/32k/128k) | — |
| **OpenRouter** | Bearer Token | 300+ model (canlı siyahı) | [Keys](https://openrouter.ai/keys) |

---

## ⚙️ Konfiqurasiya

**Fayl:** `~/.config/lumtext/settings.json`

```json
{
  "provider": "Anthropic",
  "model": "claude-sonnet-4-5",
  "hotkey": "<ctrl>+<shift>+<space>",
  "language": "English",
  "languages": ["Azərbaycan dili", "English", "Russian", "Turkish"],
  "theme": "dark",
  "window_position": [100, 100],
  "api_keys": {
    "openai": "sk-...",
    "anthropic": "sk-ant-..."
  }
}
```

**Ayarlar pəncərəsi:**

| Tab | Ayarlar |
|-----|---------|
| ⚙ **Model & API** | Provayder seçimi, model seçimi, API açarları (gizli, göstər/gizlə düyməsi ilə) |
| ⌨ **Qısayollar** | Cari qısayol, yeni qısayol girişi, sistemdə məşğul qısayollar |
| 🌐 **Dillər** | İnterfeys dili seçimi, tərcümə dilləri (max 6) |

---

## 🏗️ Arxitektura

```
main.py
 ├── ConfigManager          ← ~/.config/lumtext/settings.json
 ├── HotkeyManager
 │    ├── SelectionWatcher  ← PRIMARY seçim (xclip) 250ms
 │    └── TriggerListener   ← UNIX socket /tmp/lumtext.sock
 ├── ActionPopup (PyQt6)
 │    ├── AIWorker (QThread) → call_ai() → 8 provayder (urllib)
 │    └── Clipboard         ← xclip / pbcopy / win32
 └── SettingsWindow
      └── OpenRouterFetchWorker (QThread)
```

**İşləmə ardıcıllığı:**

```
1. main.py sistem tepsisinde işə düşür
2. SelectionWatcher PRIMARY seçimi izləyir (Linux) və ya
   qlobal qısayol dinləyir (macOS/Windows pynput ilə)
3. İstifadəçi qısayola basır → TriggerListener aktivləşir
4. Popup seçilmiş mətn və əməliyyat seçimi ilə açılır
5. İstifadəçi əməliyyat seçib "İcra et" basır
6. AIWorker arxa plan thread-də AI sorğusunu göndərir
7. Nəticə popup-da göstərilir — formatlı/düz kopyala, əvəz et
```

---

## 🛠️ Tərtibat

```bash
git clone <repo-url>
cd lumtext
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 main.py
```

**Layihə strukturu:**

```
lumtext/
├── main.py                  # Giriş nöqtəsi
├── requirements.txt         # Python asılılıqları
├── install.sh               # Linux quraşdırma skripti
├── install_mac.sh           # macOS quraşdırma skripti
├── install_windows.ps1      # Windows quraşdırma skripti
├── ui/
│   ├── action_popup.py      # Üzən popup UI (QDialog)
│   ├── settings_window.py   # Ayarlar pəncərəsi (QMainWindow)
│   ├── app_icon.png         # Tətbiq ikonu (1024×1024)
│   ├── arrow.png            # Açılan ox (PNG)
│   └── arrow.svg            # Açılan ox (SVG)
├── core/
│   ├── ai_handler.py        # AI provayder inteqrasiyası (8 provayder)
│   ├── clipboard.py         # Çarpaz platforma bufer (xclip/pbcopy/win32)
│   ├── config_manager.py    # JSON konfiq yüklə/saxla (~/.config/lumtext)
│   ├── hotkey_manager.py    # Qlobal qısayol + seçim izləyici
│   └── localization.py      # i18n (AZ, EN, TR, RU)
└── scripts/
    └── trigger.py           # Xarici trigger (UNIX socket)
```

---

---

<div align="center">

**Lumtext** — Seç. Bas. Çevir.

</div>
