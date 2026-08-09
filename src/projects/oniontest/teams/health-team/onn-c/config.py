import os
from pathlib import Path


REPOSITORY_ROOT = next(
    parent for parent in Path(__file__).resolve().parents if (parent / ".git").exists()
)
SUPPORTED_ENV_KEYS = {
    "NVIDIA_API_KEY",
    "NVIDIA_MODEL",
    "NIM_MODEL",
    "NVIDIA_API_BASE_URL",
    "NVIDIA_TIMEOUT_SECONDS",
}


def load_local_env(path: Path = REPOSITORY_ROOT / ".env") -> None:
    """Load supported KEY=VALUE entries without overriding the shell."""
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
        value = value.strip().strip('"').strip("'")
        if key in SUPPORTED_ENV_KEYS:
            os.environ.setdefault(key, value)
