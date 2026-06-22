import json
import urllib.request
import urllib.error

MODELS = {
    "OpenAI": {
        "models": ["gpt-4o", "gpt-4-turbo", "gpt-3.5-turbo"],
        "base_url": "https://api.openai.com/v1/chat/completions",
        "auth_header": "Authorization",
        "auth_prefix": "Bearer ",
    },
    "Anthropic": {
        "models": ["claude-opus-4-5", "claude-sonnet-4-5", "claude-haiku-4-5"],
        "base_url": "https://api.anthropic.com/v1/messages",
        "auth_header": "x-api-key",
        "auth_prefix": "",
    },
    "Google": {
        "models": ["gemini-2.0-flash", "gemini-1.5-pro", "gemini-1.5-flash"],
        "base_url": "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent",
        "auth_header": None,
        "auth_prefix": "",
    },
    "Groq": {
        "models": ["llama-3.3-70b-versatile", "llama-3.1-8b-instant", "mixtral-8x7b-32768"],
        "base_url": "https://api.groq.com/openai/v1/chat/completions",
        "auth_header": "Authorization",
        "auth_prefix": "Bearer ",
    },
    "DeepSeek": {
        "models": ["deepseek-chat", "deepseek-reasoner"],
        "base_url": "https://api.deepseek.com/v1/chat/completions",
        "auth_header": "Authorization",
        "auth_prefix": "Bearer ",
    },
    "MiniMax": {
        "models": ["MiniMax-Text-01", "abab6.5s-chat"],
        "base_url": "https://api.minimaxi.chat/v1/text/chatcompletion_v2",
        "auth_header": "Authorization",
        "auth_prefix": "Bearer ",
    },
    "Kimi": {
        "models": ["moonshot-v1-8k", "moonshot-v1-32k", "moonshot-v1-128k"],
        "base_url": "https://api.moonshot.cn/v1/chat/completions",
        "auth_header": "Authorization",
        "auth_prefix": "Bearer ",
    },
    "OpenRouter": {
        # Popular defaults — user can type ANY model from openrouter.ai/models
        "models": [
            "google/gemini-2.0-flash-001",
            "anthropic/claude-sonnet-4-5",
            "openai/gpt-4o",
            "meta-llama/llama-3.3-70b-instruct",
            "deepseek/deepseek-chat-v3-0324",
            "mistralai/mistral-large",
            "qwen/qwen-2.5-72b-instruct",
            "microsoft/phi-4",
            "nvidia/llama-3.1-nemotron-ultra-253b-v1:free",
            "google/gemma-3-27b-it:free",
        ],
        "base_url": "https://openrouter.ai/api/v1/chat/completions",
        "auth_header": "Authorization",
        "auth_prefix": "Bearer ",
        "extra_headers": {
            "HTTP-Referer": "https://github.com/lumtext",
            "X-Title": "Lumtext",
        },
    },
}

PROMPTS = {
    "format": (
        "Aşağıdakı mətni düzəlt: hərf səhvlərini, durğu işarələrini, cümlə quruluşunu "
        "islah et. Mətni aydın, oxunaqlı və anlaşılan dilə çevir. "
        "Yalnız düzəldilmiş mətni qaytar, heç bir izahat vermə.\n\nMətn:\n{text}"
    ),
    "translate": (
        "Aşağıdakı mətni {language} dilinə tərcümə et. "
        "Yalnız tərcüməni qaytar, heç bir izahat vermə.\n\nMətn:\n{text}"
    ),
    "email": (
        "Aşağıdakı mətni rəsmi, peşəkar email üslubuna uyğunlaşdır. "
        "Salamlama və bağlama cümləsi əlavə et. "
        "Yalnız hazır email mətnini qaytar.\n\nMətn:\n{text}"
    ),
    "summarize": (
        "Aşağıdakı mətni qısa xülasəyə çevir — əsas fikirləri saxla. "
        "Yalnız xülasəni qaytar.\n\nMətn:\n{text}"
    ),
    "tone_formal": (
        "Aşağıdakı mətni rəsmi (formal) üsluba çevir. "
        "Yalnız çevrilmiş mətni qaytar.\n\nMətn:\n{text}"
    ),
    "tone_casual": (
        "Aşağıdakı mətni gündəlik, dostcasına (informal) üsluba çevir. "
        "Yalnız çevrilmiş mətni qaytar.\n\nMətn:\n{text}"
    ),
    "bulletpoints": (
        "Aşağıdakı mətni bullet point (•) formatına çevir — hər əsas fikir ayrı nöqtə olsun. "
        "Yalnız bullet point siyahısını qaytar.\n\nMətn:\n{text}"
    ),
    "clean_sql": (
        "Aşağıdakı mətni təhlil et və oradakı SQL sorğusunu proqram kodlarından "
        "(məsələn: Java StringBuilder, sətir birləşdirmələri '+', dırnaq işarələri, "
        "Python dəyişənləri, markdown sintaksisi və s.) təmizlə. "
        "Geriyə yalnız təmiz, icra edilə bilən SQL sorğusunu qaytar. "
        "Heç bir izahat və ya əlavə mətn yazma.\n\nMətn:\n{text}"
    ),
}


def call_ai(provider: str, model: str, api_key: str, prompt: str) -> str:
    cfg = MODELS[provider]

    if provider == "Anthropic":
        return _call_anthropic(cfg, model, api_key, prompt)
    elif provider == "Google":
        return _call_google(cfg, model, api_key, prompt)
    elif provider == "MiniMax":
        return _call_minimax(cfg, model, api_key, prompt)
    elif provider == "OpenRouter":
        return _call_openrouter(cfg, model, api_key, prompt)
    else:
        return _call_openai_compat(cfg, model, api_key, prompt)


def fetch_openrouter_models(api_key: str) -> list[str]:
    """Fetch live model list from OpenRouter API."""
    try:
        req = urllib.request.Request(
            "https://openrouter.ai/api/v1/models",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            }
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())
        models = sorted([m["id"] for m in data.get("data", [])])
        return models if models else MODELS["OpenRouter"]["models"]
    except Exception:
        return MODELS["OpenRouter"]["models"]


def _call_openai_compat(cfg, model, api_key, prompt):
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 2048,
        "temperature": 0.3,
    }
    headers = {
        "Content-Type": "application/json",
        cfg["auth_header"]: cfg["auth_prefix"] + api_key,
    }
    data = json.dumps(payload).encode()
    req = urllib.request.Request(cfg["base_url"], data=data, headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=30) as resp:
        result = json.loads(resp.read())
    return result["choices"][0]["message"]["content"].strip()


def _call_anthropic(cfg, model, api_key, prompt):
    payload = {
        "model": model,
        "max_tokens": 2048,
        "messages": [{"role": "user", "content": prompt}],
    }
    headers = {
        "Content-Type": "application/json",
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01",
    }
    data = json.dumps(payload).encode()
    req = urllib.request.Request(cfg["base_url"], data=data, headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=30) as resp:
        result = json.loads(resp.read())
    return result["content"][0]["text"].strip()


def _call_google(cfg, model, api_key, prompt):
    url = cfg["base_url"].format(model=model) + f"?key={api_key}"
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    data = json.dumps(payload).encode()
    headers = {"Content-Type": "application/json"}
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=30) as resp:
        result = json.loads(resp.read())
    return result["candidates"][0]["content"]["parts"][0]["text"].strip()


def _call_minimax(cfg, model, api_key, prompt):
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 2048,
        "temperature": 0.3,
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + api_key,
    }
    data = json.dumps(payload).encode()
    req = urllib.request.Request(cfg["base_url"], data=data, headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=30) as resp:
        result = json.loads(resp.read())
    return result["choices"][0]["message"]["content"].strip()


def _call_openrouter(cfg, model, api_key, prompt):
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 2048,
        "temperature": 0.3,
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + api_key,
        # OpenRouter tələb edir: mənbəyi bildirmək
        "HTTP-Referer": "https://github.com/lumtext",
        "X-Title": "Lumtext",
    }
    data = json.dumps(payload).encode()
    req = urllib.request.Request(cfg["base_url"], data=data, headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=30) as resp:
        result = json.loads(resp.read())
    # OpenRouter bəzən error field qaytarır
    if "error" in result:
        raise Exception(result["error"].get("message", "OpenRouter xətası"))
    return result["choices"][0]["message"]["content"].strip()


def build_prompt(action: str, text: str, language: str = "") -> str:
    template = PROMPTS.get(action, PROMPTS["format"])
    return template.format(text=text, language=language)
