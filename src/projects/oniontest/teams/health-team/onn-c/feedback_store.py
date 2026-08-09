import hashlib
import json
import threading
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


REPORT_CATEGORIES = {
    "unsafe_response",
    "missed_risk",
    "false_alarm",
    "harmful_bias",
    "incorrect_information",
    "privacy_concern",
    "manipulative_response",
    "other",
}
MAX_NOTE_LENGTH = 1000
MAX_CONTENT_LENGTH = 4000
_WRITE_LOCK = threading.Lock()


def _required_text(payload: dict[str, Any], key: str, max_length: int) -> str:
    value = payload.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{key} must be a non-empty string")
    if len(value) > max_length:
        raise ValueError(f"{key} must be at most {max_length} characters")
    return value.strip()


def _optional_text(payload: dict[str, Any], key: str, max_length: int) -> str | None:
    value = payload.get(key)
    if value is None:
        return None
    if not isinstance(value, str):
        raise ValueError(f"{key} must be a string")
    if len(value) > max_length:
        raise ValueError(f"{key} must be at most {max_length} characters")
    return value.strip() or None


def create_feedback_report(payload: dict[str, Any]) -> dict[str, Any]:
    """Validate a user report without retaining conversation text by default."""
    category = _required_text(payload, "category", 64)
    if category not in REPORT_CATEGORIES:
        raise ValueError("category is not supported")

    session_id = _required_text(payload, "session_id", 64)
    turn_id = _optional_text(payload, "turn_id", 128)
    note = _optional_text(payload, "note", MAX_NOTE_LENGTH)
    include_content = payload.get("include_content", False)
    if not isinstance(include_content, bool):
        raise ValueError("include_content must be a boolean")

    content = None
    if include_content:
        content = {
            "user_message": _optional_text(payload, "user_message", MAX_CONTENT_LENGTH),
            "ai_response": _optional_text(payload, "ai_response", MAX_CONTENT_LENGTH),
        }
        if not any(content.values()):
            raise ValueError("include_content requires user_message or ai_response")

    return {
        "schema_version": "onion-feedback.v1",
        "report_id": str(uuid.uuid4()),
        "created_at": datetime.now(timezone.utc).isoformat(),
        "status": "pending_review",
        "category": category,
        "session_ref": hashlib.sha256(session_id.encode("utf-8")).hexdigest()[:16],
        "turn_id": turn_id,
        "note": note,
        "content_included": include_content,
        "content": content,
    }


def save_feedback_report(payload: dict[str, Any], report_dir: Path) -> dict[str, Any]:
    report = create_feedback_report(payload)
    report_dir.mkdir(parents=True, exist_ok=True)
    path = report_dir / "pending_reports.jsonl"
    serialized = json.dumps(report, ensure_ascii=False)
    with _WRITE_LOCK:
        with path.open("a", encoding="utf-8") as stream:
            stream.write(serialized + "\n")
    return report
