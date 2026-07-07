CRISIS_KEYWORDS = [
    "kill myself",
    "suicide",
    "self harm",
    "hurt myself",
    "end my life",
    "die",
    "want to die",
    "i don't want to live",
    "死にたい",
    "自殺",
    "想死",
    "自杀",
    "suicidio",
    "quiero morir",
    "suicide",
    "mourir",
    "죽고",
    "죽고싶",
    "죽고 싶",
    "살기 싫",
    "자살",
    "자해",
    "해치고",
    "끝내고",
]

VIOLENCE_KEYWORDS = [
    "kill you",
    "attack you",
    "hurt you",
    "threat",
    "murder",
    "stab",
    "shoot",
    "殺す",
    "攻撃",
    "杀",
    "攻击",
    "matar",
    "atacar",
    "tuer",
    "attaque",
    "죽일",
    "공격",
    "해칠",
    "협박",
]


def _normalize(sentence: str) -> str:
    cleaned = sentence.lower()
    for mark in "?!.,;:()[]{}\"'“”‘’…~":
        cleaned = cleaned.replace(mark, " ")
    return " ".join(cleaned.split())


def check_safety_gate(sentence: str) -> dict:
    """Detect high-priority safety signals before gamified advice continues.

    This is not a clinical classifier. It is a conservative rule-based gate for
    the prototype. When triggered, the game/support loop should switch to safety
    guidance and avoid reward, growth, or playful coaching language.
    """
    normalized_sentence = _normalize(sentence)

    matched_crisis = [
        keyword for keyword in CRISIS_KEYWORDS if keyword in normalized_sentence
    ]
    matched_violence = [
        keyword for keyword in VIOLENCE_KEYWORDS if keyword in normalized_sentence
    ]

    if matched_crisis:
        return {
            "triggered": True,
            "level": "crisis",
            "reason": "self_harm_signal",
            "matched_keywords": matched_crisis,
            "action": "safety_guidance",
            "message": (
                "Gamified advice is paused. Offer calm safety guidance and "
                "encourage contacting trusted people or local emergency support."
            ),
        }

    if matched_violence:
        return {
            "triggered": True,
            "level": "high",
            "reason": "violence_or_threat_signal",
            "matched_keywords": matched_violence,
            "action": "safety_guidance",
            "message": (
                "Gamified advice is paused. Set a firm boundary and redirect "
                "to immediate safety and de-escalation."
            ),
        }

    return {
        "triggered": False,
        "level": "normal",
        "reason": None,
        "matched_keywords": [],
        "action": None,
        "message": None,
    }
