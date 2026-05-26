<div align="center">

<img src="ui/app_icon.png" width="64" alt="Логотип Lumtext">

# ◈ Lumtext

🇬🇧 [English](README.md) · 🇦🇿 [Azərbaycan](README.az.md) · 🇹🇷 [Türkçe](README.tr.md)

**Обработка текста с ИИ — Мгновенно, Везде**

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://python.org)
[![PyQt6](https://img.shields.io/badge/PyQt-6.6%2B-41CD52?logo=qt&logoColor=white)](https://www.riverbankcomputing.com/software/pyqt/)
[![Platform](https://img.shields.io/badge/Platform-Linux%20|%20macOS%20|%20Windows-8A2BE2)](#-кроссплатформенность)
[![Лицензия](https://img.shields.io/badge/Лицензия-MIT-желтый)](#)

</div>

---

## ✨ Ключевые возможности

| # | Возможность | Описание |
|---|-------------|----------|
| 🌐 | **Глобальная горячая клавиша** | Выделите текст в *любом* приложении, нажмите `Ctrl+Shift+Space` — Lumtext появится мгновенно |
| 🤖 | **8 AI-провайдеров** | OpenAI, Anthropic, Google, Groq, DeepSeek, MiniMax, Kimi, OpenRouter (300+ моделей) |
| ✏️ | **7 умных операций** | Исправить грамматику, перевести, резюмировать, адаптировать для письма, изменить тон, преобразовать в список |
| 🖥️ | **Системный трей** | Работает незаметно в фоне — доступен из трея в любой момент |
| 🔄 | **Живой список моделей** | OpenRouter загружает актуальный список моделей в реальном времени — 300+ моделей |
| 🔍 | **Обнаружение конфликтов** | Сканирует GNOME/KDE на занятые горячие клавиши |
| 🚀 | **Автозапуск** | Опциональный запуск при загрузке системы — всегда готов |
| 🌍 | **Многоязычный интерфейс** | Английский, Азербайджанский, Турецкий, Русский — переключение на лету |
| 📋 | **Копировать и заменить** | Копируйте результат с форматированием или без; замените выделенный текст одним кликом |

---

## 💡 Почему Lumtext?

- **Простая настройка** — установите зависимости, запустите, готово. Никаких фреймворков, только API-ключ.
- **Нет AI SDK** — Все запросы через встроенный Python `urllib`. Никаких лишних зависимостей.
- **Работает везде** — системный трей на Linux, macOS и Windows. Подходит для любого рабочего процесса.
- **Конфиденциальность** — ваши API-ключи хранятся в `~/.config/lumtext/settings.json`. Никакой телеметрии.
- **Темная тема** — удобна для длительных сессий работы.
- **Перемещаемый попап** — перетащите плавающее окно в любое место на экране.

---

## 📦 Требования

| Зависимость | Мин. версия | Примечания |
|------------|-------------|------------|
| Python | 3.10+ | |
| PyQt6 | 6.6.0+ | Графический фреймворк |
| pynput | 1.7.6+ | Глобальные клавиши (macOS/Windows) |
| platformdirs | 4.0.0+ | Определение пути конфигурации |
| xclip | *системная* | Linux PRIMARY выделение (`apt install xclip`) |

> **AI SDK не требуются** — все провайдеры вызываются через стандартную библиотеку Python `urllib`.

---

## 🚀 Быстрый старт

### 🐧 Linux

```bash
git clone <repo-url> lumtext
cd lumtext
chmod +x install.sh
./install.sh
```

Установщик автоматически:
- Проверяет Python 3 и pip, устанавливает `xclip`
- Устанавливает системные зависимости PyQt6 (`libxcb-cursor0` и т.д.)
- Создает виртуальное окружение Python
- Устанавливает требуемые пакеты Python
- Создает `.desktop` ярлык
- Опционально включает автозапуск

**Ручная установка:**

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
# При запросе разрешите доступ к специальным возможностям
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

## 📖 Руководство по использованию

### Первый запуск

1. Запустите Lumtext — в системном трее появится синяя иконка **AI**
2. Кликните правой кнопкой по иконке в трее → **Открыть настройки**
3. Перейдите на вкладку **Модель & API**
4. Выберите AI-провайдера (например, Anthropic, OpenAI)
5. Введите ваш API-ключ для выбранного провайдера
6. Выберите модель из списка
7. Нажмите **Сохранить**

### Повседневное использование

```
1. Выделите текст в любом приложении (браузер, редактор, терминал и т.д.)
2. Нажмите Ctrl+Shift+Space (горячая клавиша по умолчанию)
3. Появится плавающее окно с выделенным текстом
4. Выберите операцию:
   ✎   Исправить и упростить
   ⇄   Перевести на другой язык
   ✉   Адаптировать для письма
   ⚡  Резюмировать
   ⬆  Перевести в официальный стиль
   ⬇  Перевести в повседневный стиль
   ⊟  Преобразовать в маркированный список
5. Нажмите ▶  Выполнить
6. ИИ обрабатывает текст — результат появляется в окне
7. Скопируйте с форматированием или без, или нажмите "Заменить"
```

### Изменение горячей клавиши

1. Кликните правой кнопкой по иконке в трее → **Открыть настройки**
2. Перейдите на вкладку **Горячие клавиши**
3. Просмотрите занятые системные клавиши (автосканирование GNOME/KDE)
4. Введите новую клавишу (формат: `<ctrl>+<shift>+a`)
5. Нажмите **Установить**
6. Нажмите **Сохранить**

### OpenRouter (300+ моделей)

1. Выберите **OpenRouter** в качестве провайдера
2. Введите ваш [API-ключ OpenRouter](https://openrouter.ai/keys)
3. Нажмите **⟳ Загрузить модели** — загружается актуальный список моделей
4. Начните ввод для фильтрации 300+ моделей
5. Вы также можете ввести ID любой модели вручную

### Внешний скрипт триггера

Если глобальная клавиша не работает, добавьте `scripts/trigger.py` в вашу собственную привязку клавиш:

```bash
python3 scripts/trigger.py
```

Это отправляет сигнал через UNIX-сокет (`/tmp/lumtext.sock`) для вызова окна с выделенным текстом.

---

## 🖼️ Скриншоты

| | |
|---|---|
| **Окно настроек** — провайдеры, API-ключи, горячая клавиша и язык | <img src="screenshots/settings.png" width="320" alt="Настройки"> |
| **Окно действий** — открывается по горячей клавише | <img src="screenshots/popup.png" width="320" alt="Окно действий"> |
| **Результат AI** — обработанный вывод с кнопками копирования/замены | <img src="screenshots/result.png" width="320" alt="Результат"> |

---

## 🤖 Поддерживаемые AI-провайдеры

| Провайдер | Метод аутентификации | Примеры моделей | URL настройки |
|-----------|---------------------|----------------|---------------|
| **OpenAI** | Bearer Token | GPT-4o, GPT-4-turbo, GPT-3.5-turbo | [API ключи](https://platform.openai.com/api-keys) |
| **Anthropic** | x-api-key | Claude Opus 4.5, Sonnet 4.5, Haiku 4.5 | [Консоль](https://console.anthropic.com/settings/keys) |
| **Google** | API ключ | Gemini 2.0 Flash, 1.5 Pro, 1.5 Flash | [AI Studio](https://aistudio.google.com/apikey) |
| **Groq** | Bearer Token | Llama 3.3-70B, Llama 3.1-8B, Mixtral | [Консоль](https://console.groq.com/keys) |
| **DeepSeek** | Bearer Token | DeepSeek Chat, DeepSeek Reasoner | — |
| **MiniMax** | Bearer Token | MiniMax-Text-01, abab6.5s-chat | — |
| **Kimi** | Bearer Token | Moonshot v1 (8k/32k/128k) | — |
| **OpenRouter** | Bearer Token | 300+ моделей (живой список) | [Ключи](https://openrouter.ai/keys) |

---

## ⚙️ Конфигурация

**Файл:** `~/.config/lumtext/settings.json`

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

**Окно настроек:**

| Вкладка | Настройки |
|---------|-----------|
| ⚙ **Модель & API** | Выбор провайдера, выбор модели, API-ключи (скрыты, с кнопкой показать/скрыть) |
| ⌨ **Горячие клавиши** | Текущая клавиша, ввод новой клавиши, занятые системные клавиши |
| 🌐 **Языки** | Выбор языка интерфейса, языки перевода (макс. 6) |

---

## 🏗️ Архитектура

```
main.py
 ├── ConfigManager          ← ~/.config/lumtext/settings.json
 ├── HotkeyManager
 │    ├── SelectionWatcher  ← PRIMARY выделение (xclip) 250мс
 │    └── TriggerListener   ← UNIX socket /tmp/lumtext.sock
 ├── ActionPopup (PyQt6)
 │    ├── AIWorker (QThread) → call_ai() → 8 провайдеров (urllib)
 │    └── Clipboard         ← xclip / pbcopy / win32
 └── SettingsWindow
      └── OpenRouterFetchWorker (QThread)
```

**Поток выполнения:**

```
1. main.py запускается в системном трее
2. SelectionWatcher отслеживает PRIMARY выделение (Linux) или
   слушает глобальную клавишу (macOS/Windows через pynput)
3. Пользователь нажимает клавишу → TriggerListener активируется
4. Появляется окно с выделенным текстом и выбором операции
5. Пользователь выбирает операцию и нажимает "Выполнить"
6. AIWorker отправляет запрос выбранному провайдеру в фоновом потоке
7. Результат отображается в окне — копирование с/без форматирования, замена
```

---

## 🛠️ Разработка

```bash
git clone <repo-url>
cd lumtext
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 main.py
```

**Структура проекта:**

```
lumtext/
├── main.py                  # Точка входа
├── requirements.txt         # Python зависимости
├── install.sh               # Установщик для Linux
├── install_mac.sh           # Установщик для macOS
├── install_windows.ps1      # Установщик для Windows
├── ui/
│   ├── action_popup.py      # Всплывающее окно (QDialog)
│   ├── settings_window.py   # Окно настроек (QMainWindow)
│   ├── app_icon.png         # Иконка приложения (1024×1024)
│   ├── arrow.png            # Стрелка раскрывающегося списка (PNG)
│   └── arrow.svg            # Стрелка раскрывающегося списка (SVG)
├── core/
│   ├── ai_handler.py        # Интеграция AI-провайдеров (8 провайдеров)
│   ├── clipboard.py         # Кроссплатформенный буфер обмена (xclip/pbcopy/win32)
│   ├── config_manager.py    # Загрузка/сохранение JSON конфига (~/.config/lumtext)
│   ├── hotkey_manager.py    # Глобальная клавиша + отслеживание выделения
│   └── localization.py      # i18n (AZ, EN, TR, RU)
└── scripts/
    └── trigger.py           # Внешний триггер (UNIX socket)
```

---

---

<div align="center">

**Lumtext** — Выдели. Нажми. Преобразуй.

</div>
