REPAIR_KEYWORDS = [
    "sorry",
    "apologize",
    "apology",
    "forgive me",
    "미안",
    "사과",
    "용서해",
]

APPRECIATION_KEYWORDS = [
    "thank",
    "thanks",
    "grateful",
    "appreciate",
    "고마워",
    "고맙",
    "감사",
]


def _normalize(sentence: str) -> str:
    cleaned = sentence.lower()
    for mark in "?!.,;:()[]{}\"'“”‘’…~":
        cleaned = cleaned.replace(mark, " ")
    return " ".join(cleaned.split())


def detect_recovery_signal(sentence: str) -> dict:
    """Detect explicit attempts to repair or affirm the relationship."""
    normalized = _normalize(sentence)
    repair_matches = [word for word in REPAIR_KEYWORDS if word in normalized]
    appreciation_matches = [
        word for word in APPRECIATION_KEYWORDS if word in normalized
    ]
    matched_keywords = repair_matches + appreciation_matches

    if repair_matches:
        kind = "repair"
    elif appreciation_matches:
        kind = "appreciation"
    else:
        kind = "none"

    strength = min(1.0, 0.5 + max(0, len(matched_keywords) - 1) * 0.15)
    if not matched_keywords:
        strength = 0.0

    return {
        "detected": bool(matched_keywords),
        "kind": kind,
        "strength": round(strength, 3),
        "matched_keywords": matched_keywords,
    }
