ALLOWED_ACTIONS = {"greet", "help", "refuse", "joke", "avoid", "ask_question"}


def _clamp(value: float) -> float:
    return max(0.0, min(1.0, value))


def _normalize(sentence: str) -> str:
    cleaned = sentence.lower()
    for mark in "?!.,;:()[]{}\"'":
        cleaned = cleaned.replace(mark, " ")
    return " ".join(cleaned.split())


def _tokenize(sentence: str) -> set[str]:
    return set(sentence.split())


def _keyword_matches(keyword: str, normalized_sentence: str, words: set[str]) -> bool:
    keyword = keyword.lower()
    if keyword.isascii() and " " not in keyword:
        return keyword in words
    return keyword in normalized_sentence


def _has_any(
    keywords: list[str],
    normalized_sentence: str,
    words: set[str],
) -> bool:
    return any(
        _keyword_matches(keyword, normalized_sentence, words)
        for keyword in keywords
    )


def _dominant_emotion(emotion: dict) -> str:
    """Return the strongest emotion, or neutral if all scores are zero."""
    if not emotion:
        return "neutral"

    name, score = max(emotion.items(), key=lambda item: item[1])
    return name if score > 0 else "neutral"


def decide_action(
    user_sentence: str,
    big_five: dict,
    emotion: dict,
    memory: list[dict],
    memory_summary: dict | None = None,
) -> str:
    """Choose one NPC action based on personality, emotion, and memory."""
    is_question = user_sentence.strip().endswith(("?", "？"))
    sentence = _normalize(user_sentence)
    words = _tokenize(sentence)
    dominant_emotion = _dominant_emotion(emotion)
    memory_summary = memory_summary or {}
    memory_count = memory_summary.get("total_interactions", len(memory))
    memory_trust = memory_summary.get("trust_level", 0.5)
    familiarity = memory_summary.get("familiarity", 0.0)
    recent_negative_streak = memory_summary.get("recent_negative_streak", 0)

    agreeableness = big_five.get("agreeableness", 0.5)
    extraversion = big_five.get("extraversion", 0.5)
    openness = big_five.get("openness", 0.5)
    neuroticism = big_five.get("neuroticism", 0.5)

    # Past memory shifts the NPC attitude before the final decision.
    effective_agreeableness = _clamp(agreeableness + (memory_trust - 0.5) * 0.4)
    effective_extraversion = _clamp(extraversion + familiarity * 0.1)
    effective_neuroticism = _clamp(neuroticism + (0.5 - memory_trust) * 0.3)

    is_greeting = _has_any(["hello", "hi", "hey", "안녕", "반가워"], sentence, words)
    asks_for_help = _has_any(["help", "support", "도와", "지원"], sentence, words)

    if recent_negative_streak >= 2 and dominant_emotion in {"anger", "sadness"}:
        return "avoid"

    if memory_trust <= 0.25 and dominant_emotion == "anger":
        return "refuse"

    if is_greeting:
        return "greet"

    if dominant_emotion == "anger" and effective_agreeableness < 0.5:
        return "refuse"

    if dominant_emotion == "sadness" and effective_agreeableness >= 0.5:
        return "help"

    if asks_for_help and memory_trust >= 0.25:
        return "help"

    if effective_agreeableness >= 0.75 and memory_trust >= 0.45:
        return "help"

    if effective_neuroticism >= 0.7 and dominant_emotion in {"anger", "sadness"}:
        return "avoid"

    if openness >= 0.7 and effective_extraversion >= 0.6 and memory_trust >= 0.4:
        return "joke"

    if memory_count == 0 or is_question:
        return "ask_question"

    if memory_trust >= 0.7 and effective_extraversion >= 0.6:
        return "help"

    if effective_extraversion >= 0.7:
        return "greet"

    return "ask_question"
