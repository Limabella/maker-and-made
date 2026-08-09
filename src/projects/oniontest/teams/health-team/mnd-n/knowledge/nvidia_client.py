import json
import os
import urllib.error
import urllib.request
from pathlib import Path


REPOSITORY_ROOT = next(
    parent for parent in Path(__file__).resolve().parents if (parent / ".git").exists()
)
DEFAULT_CHAT_URL = "https://integrate.api.nvidia.com/v1/chat/completions"


def load_repository_env(path: Path = REPOSITORY_ROOT / ".env") -> None:
    if not path.exists():
        return
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        if key.lower().startswith("$env:"):
            key = key[5:].strip()
        if key.startswith(("NVIDIA_", "NIM_", "PSYCH_RAG_", "OLLAMA_")):
            os.environ.setdefault(key, value.strip().strip('"').strip("'"))


def _post_json(url: str, payload: dict, headers: dict, timeout: int) -> dict:
    request = urllib.request.Request(
        url,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers=headers,
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return json.loads(response.read().decode("utf-8"))
    except (urllib.error.URLError, json.JSONDecodeError, TimeoutError) as error:
        raise RuntimeError(f"Model request failed: {error}") from error


def chat_completion(
    messages: list[dict],
    model: str | None = None,
    temperature: float = 0.1,
) -> str:
    load_repository_env()
    api_key = os.getenv("NVIDIA_API_KEY")
    if not api_key:
        raise RuntimeError("NVIDIA_API_KEY is required")
    model = (
        model
        or os.getenv("PSYCH_RAG_INDEX_MODEL")
        or os.getenv("NVIDIA_MODEL")
        or os.getenv("NIM_MODEL")
        or "nvidia/nvidia-nemotron-nano-9b-v2"
    )
    if "nemotron-nano-9b-v2" in model.lower() and messages:
        messages = [dict(message) for message in messages]
        first = messages[0]
        first["content"] = "/no_think\n" + str(first.get("content", ""))

    data = _post_json(
        os.getenv("PSYCH_RAG_LLM_BASE_URL")
        or os.getenv("NVIDIA_API_BASE_URL")
        or DEFAULT_CHAT_URL,
        {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": 4096,
        },
        {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
        int(os.getenv("NVIDIA_TIMEOUT_SECONDS", "90")),
    )
    try:
        return str(data["choices"][0]["message"]["content"]).strip()
    except (KeyError, IndexError, TypeError) as error:
        raise RuntimeError("Unexpected chat completion response") from error


def ollama_embeddings(texts: list[str]) -> list[list[float]]:
    load_repository_env()
    base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434").rstrip("/")
    data = _post_json(
        f"{base_url}/api/embed",
        {
            "model": os.getenv("PSYCH_RAG_EMBED_MODEL", "bge-m3"),
            "input": texts,
        },
        {"Content-Type": "application/json"},
        int(os.getenv("PSYCH_RAG_EMBED_TIMEOUT", "120")),
    )
    embeddings = data.get("embeddings")
    if not isinstance(embeddings, list):
        raise RuntimeError("Unexpected Ollama embedding response")
    return embeddings
