"""Get answers from local models through Ollama (used by "Generate it for me" mode).

Runs fully offline. Pull each model once before use, for example:
    ollama pull llama3.1:8b
    ollama pull mistral
    ollama pull gemma2:9b
"""
import ollama

# Dropdown name -> Ollama model tag. Remove any you haven't pulled.
LOCAL_MODELS = {
    "Llama 3.1 8B": "llama3.1:8b",
    "Mistral 7B": "mistral",
    "Gemma 2 9B": "gemma2:9b",
}


def installed_tags() -> set[str]:
    """Ollama model tags already downloaded on this machine."""
    try:
        data = ollama.list()
        models = data.get("models", []) if isinstance(data, dict) else getattr(data, "models", [])
        tags = set()
        for m in models:
            if isinstance(m, dict):
                name = m.get("model") or m.get("name")
            else:
                name = getattr(m, "model", None) or getattr(m, "name", None)
            if name:
                tags.add(name)
                tags.add(name.split(":")[0])
        return tags
    except Exception:
        return set()


def available_models() -> dict[str, str]:
    """Only the local models that are actually downloaded."""
    tags = installed_tags()
    return {k: v for k, v in LOCAL_MODELS.items() if v in tags or v.split(":")[0] in tags}


def ask_model(name: str, prompt: str) -> str:
    """Send one prompt to a local model and return its reply as text."""
    r = ollama.chat(model=LOCAL_MODELS[name],
                    messages=[{"role": "user", "content": prompt}])
    return r["message"]["content"]


if __name__ == "__main__":
    print("Downloaded local models:", list(available_models()) or "none - run `ollama pull llama3.1:8b`")
