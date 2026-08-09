import json
import re
from pathlib import Path


REGISTRY_PATH = Path(__file__).with_name("safety_signal_registry.json")


def _load_registry() -> dict:
    return json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))


def _normalize(sentence: str) -> str:
    cleaned = sentence.casefold()
    for mark in "?!.,;:()[]{}\"'“”‘’…~":
        cleaned = cleaned.replace(mark, " ")
    return " ".join(cleaned.split())


def _contains_pattern(sentence: str, pattern: str) -> bool:
    """Use word boundaries for Latin text and substring matching for CJK text."""
    if pattern.isascii():
        return re.search(rf"(?<!\w){re.escape(pattern)}(?!\w)", sentence) is not None
    return pattern in sentence


def check_safety_gate(sentence: str) -> dict:
    """Detect policy signals before gamified advice continues.

    This deterministic registry is only the first detection layer. A match
    pauses ordinary guidance for review; it is not a diagnosis or a complete
    assessment of urgency.
    """
    registry = _load_registry()
    normalized_sentence = _normalize(sentence)
    matches = []

    for rule in registry["rules"]:
        matched_patterns = [
            pattern
            for pattern in rule["patterns"]
            if _contains_pattern(normalized_sentence, pattern.casefold())
        ]
        if matched_patterns:
            matches.append(
                {
                    "rule_id": rule["id"],
                    "category": rule["category"],
                    "level": rule["level"],
                    "matched_patterns": matched_patterns,
                }
            )

    if not matches:
        return {
            "triggered": False,
            "level": "normal",
            "reason": None,
            "matched_keywords": [],
            "matched_signals": [],
            "policy_version": registry["version"],
            "requires_context_review": False,
            "action": None,
            "message": None,
        }

    priority = {"normal": 0, "high": 1, "crisis": 2}
    primary = max(matches, key=lambda match: priority[match["level"]])
    matched_keywords = sorted(
        {
            pattern
            for match in matches
            for pattern in match["matched_patterns"]
        }
    )
    return {
        "triggered": True,
        "level": primary["level"],
        "reason": primary["category"],
        "matched_keywords": matched_keywords,
        "matched_signals": matches,
        "policy_version": registry["version"],
        "requires_context_review": True,
        "action": "safety_guidance",
        "message": registry["trigger_message"],
    }
