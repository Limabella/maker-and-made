AGGRESSIVE_KEYWORDS = [
    "hate",
    "attack",
    "threat",
    "angry",
    "kill",
    "mad",
    "shut up",
    "嫌い",
    "怒",
    "攻撃",
    "讨厌",
    "生气",
    "攻击",
    "odio",
    "enojado",
    "déteste",
    "싫어",
    "싫다",
    "공격",
    "협박",
    "죽일",
    "화나",
    "꺼져",
    "닥쳐",
]

DISTRESS_KEYWORDS = [
    "sad",
    "lonely",
    "hurt",
    "panic",
    "anxious",
    "tired",
    "depressed",
    "exhausted",
    "alone",
    "悲しい",
    "寂しい",
    "伤心",
    "孤独",
    "triste",
    "solo",
    "슬퍼",
    "슬프",
    "외로",
    "아파",
    "아프",
    "불안",
    "지쳐",
    "힘들",
    "우울",
]


def _normalize(sentence: str) -> str:
    cleaned = sentence.lower()
    for mark in "?!.,;:()[]{}\"'“”‘’…~":
        cleaned = cleaned.replace(mark, " ")
    return " ".join(cleaned.split())


def monitor_context(
    sentence: str,
    emotion: dict,
    memory_summary: dict,
    safety: dict,
) -> dict:
    """Observe dialogue context without diagnosing the player or character."""
    normalized_sentence = _normalize(sentence)

    aggressive_matches = [
        keyword for keyword in AGGRESSIVE_KEYWORDS if keyword in normalized_sentence
    ]
    distress_matches = [
        keyword for keyword in DISTRESS_KEYWORDS if keyword in normalized_sentence
    ]

    recent_negative_streak = memory_summary.get("recent_negative_streak", 0)
    trust_level = memory_summary.get("trust_level", 0.5)
    negative_emotion = emotion.get("anger", 0.0) + emotion.get("sadness", 0.0)

    repeated_negative_signal = recent_negative_streak >= 2
    trust_drop_signal = trust_level <= 0.3
    elevated_negative_emotion = negative_emotion >= 0.75

    return {
        "aggressive_matches": aggressive_matches,
        "distress_matches": distress_matches,
        "repeated_negative_signal": repeated_negative_signal,
        "trust_drop_signal": trust_drop_signal,
        "elevated_negative_emotion": elevated_negative_emotion,
        "safety_triggered": safety.get("triggered", False),
        "signal_count": sum(
            [
                bool(aggressive_matches),
                bool(distress_matches),
                repeated_negative_signal,
                trust_drop_signal,
                elevated_negative_emotion,
                safety.get("triggered", False),
            ]
        ),
    }
