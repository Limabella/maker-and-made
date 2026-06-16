from dataclasses import asdict, dataclass


@dataclass
class EmotionState:
    """Basic emotion scores from 0.0 to 1.0."""

    joy: float = 0.0
    anger: float = 0.0
    trust: float = 0.0
    sadness: float = 0.0


KEYWORDS = {
    "joy": [
        "happy",
        "great",
        "fun",
        "excited",
        "thanks",
        "thank",
        "love",
        "glad",
        "win",
        "기뻐",
        "행복",
        "좋아",
        "재밌",
        "신나",
        "고마워",
        "감사",
        "사랑",
        "반가워",
        "이겼",
    ],
    "anger": [
        "angry",
        "hate",
        "attack",
        "annoyed",
        "furious",
        "threat",
        "betray",
        "화나",
        "싫어",
        "공격",
        "짜증",
        "분노",
        "위협",
        "배신",
    ],
    "trust": [
        "trust",
        "help",
        "friend",
        "please",
        "safe",
        "promise",
        "support",
        "믿",
        "도와",
        "친구",
        "부탁",
        "안전",
        "약속",
        "지원",
    ],
    "sadness": [
        "sad",
        "lost",
        "lonely",
        "sorry",
        "cry",
        "hurt",
        "miss",
        "슬퍼",
        "잃어",
        "외로",
        "미안",
        "울",
        "다쳤",
        "아파",
        "그리워",
    ],
}


def _normalize(sentence: str) -> str:
    """Normalize simple punctuation so keyword matching stays readable."""
    cleaned = sentence.lower()
    for mark in "?!.,;:()[]{}\"'":
        cleaned = cleaned.replace(mark, " ")
    return " ".join(cleaned.split())


def _tokenize(sentence: str) -> set[str]:
    return set(sentence.split())


def _keyword_matches(keyword: str, normalized_sentence: str, words: set[str]) -> bool:
    """Match English words by token and Korean stems by substring."""
    keyword = keyword.lower()
    if keyword.isascii() and " " not in keyword:
        return keyword in words
    return keyword in normalized_sentence


def estimate_emotion(sentence: str) -> dict:
    """Estimate emotion state using simple keyword matches."""
    normalized_sentence = _normalize(sentence)
    words = _tokenize(normalized_sentence)
    emotion = EmotionState()

    for emotion_name, keywords in KEYWORDS.items():
        matches = sum(
            1
            for keyword in keywords
            if _keyword_matches(keyword, normalized_sentence, words)
        )
        # Each match adds visible weight while keeping the score bounded.
        setattr(emotion, emotion_name, min(1.0, matches * 0.25))

    return asdict(emotion)
