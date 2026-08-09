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
        "happiness",
        "great",
        "fun",
        "joy",
        "joyful",
        "excited",
        "thanks",
        "thank",
        "love",
        "glad",
        "win",
        "good",
        "nice",
        "嬉しい",
        "楽しい",
        "ありがとう",
        "好き",
        "开心",
        "高兴",
        "谢谢",
        "喜欢",
        "feliz",
        "gracias",
        "amor",
        "contento",
        "heureux",
        "merci",
        "aime",
        "기뻐",
        "기쁘",
        "행복",
        "좋아",
        "좋다",
        "좋은",
        "좋았",
        "재밌",
        "재미",
        "신나",
        "고마워",
        "고맙",
        "감사",
        "사랑",
        "반가워",
        "반갑",
        "이겼",
    ],
    "anger": [
        "angry",
        "anger",
        "hate",
        "attack",
        "annoyed",
        "furious",
        "threat",
        "betray",
        "mad",
        "irritated",
        "shut up",
        "嫌い",
        "怒",
        "攻撃",
        "讨厌",
        "生气",
        "攻击",
        "odio",
        "enojado",
        "attaque",
        "déteste",
        "화나",
        "화났",
        "화남",
        "싫어",
        "싫다",
        "싫은",
        "공격",
        "짜증",
        "분노",
        "위협",
        "배신",
        "꺼져",
        "닥쳐",
    ],
    "trust": [
        "trust",
        "help",
        "friend",
        "please",
        "safe",
        "promise",
        "support",
        "together",
        "with you",
        "believe",
        "安心",
        "信じ",
        "友達",
        "帮",
        "朋友",
        "相信",
        "seguro",
        "ayuda",
        "amigo",
        "confiar",
        "aide",
        "ami",
        "confiance",
        "믿",
        "도와",
        "친구",
        "부탁",
        "안전",
        "약속",
        "지원",
        "함께",
        "같이",
        "괜찮",
    ],
    "sadness": [
        "sad",
        "sadness",
        "lost",
        "lonely",
        "sorry",
        "cry",
        "hurt",
        "miss",
        "depressed",
        "tired",
        "exhausted",
        "alone",
        "悲しい",
        "寂しい",
        "ごめん",
        "痛い",
        "伤心",
        "孤独",
        "对不起",
        "痛",
        "triste",
        "solo",
        "perdón",
        "fatigué",
        "triste",
        "désolé",
        "슬퍼",
        "슬프",
        "잃어",
        "잃었",
        "외로",
        "미안",
        "울",
        "눈물",
        "다쳤",
        "아파",
        "아프",
        "그리워",
        "지쳐",
        "힘들",
        "우울",
    ],
}


def _normalize(sentence: str) -> str:
    """Normalize simple punctuation so keyword matching stays readable."""
    cleaned = sentence.lower()
    for mark in "?!.,;:()[]{}\"'“”‘’…~":
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
