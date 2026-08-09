from dataclasses import asdict, dataclass


@dataclass
class BigFiveScores:
    """Simple OCEAN personality scores from 0.0 to 1.0."""

    openness: float = 0.5
    conscientiousness: float = 0.5
    extraversion: float = 0.5
    agreeableness: float = 0.5
    neuroticism: float = 0.5


KEYWORDS = {
    "openness": {
        "positive": [
            "new",
            "explore",
            "adventure",
            "creative",
            "imagine",
            "mystery",
            "learn",
            "art",
            "strange",
            "curious",
            "experiment",
            "새로운",
            "탐험",
            "모험",
            "창의",
            "상상",
            "미스터리",
            "배우",
            "예술",
            "낯선",
            "호기심",
            "실험",
        ],
        "negative": [
            "routine",
            "normal",
            "same",
            "traditional",
            "familiar",
            "반복",
            "평범",
            "똑같",
            "전통",
            "익숙",
        ],
    },
    "conscientiousness": {
        "positive": [
            "plan",
            "careful",
            "promise",
            "goal",
            "duty",
            "work",
            "finish",
            "prepare",
            "responsible",
            "organize",
            "계획",
            "조심",
            "약속",
            "목표",
            "책임",
            "일",
            "완료",
            "끝내",
            "준비",
            "정리",
        ],
        "negative": [
            "later",
            "random",
            "messy",
            "ignore",
            "reckless",
            "lazy",
            "나중",
            "무작위",
            "엉망",
            "무시",
            "무모",
            "게으",
        ],
    },
    "extraversion": {
        "positive": [
            "hello",
            "hi",
            "hey",
            "party",
            "friend",
            "talk",
            "together",
            "excited",
            "team",
            "join",
            "안녕",
            "반가워",
            "파티",
            "친구",
            "대화",
            "함께",
            "같이",
            "신나",
            "팀",
            "합류",
        ],
        "negative": [
            "alone",
            "quiet",
            "hide",
            "silent",
            "혼자",
            "조용",
            "숨",
            "침묵",
        ],
    },
    "agreeableness": {
        "positive": [
            "help",
            "please",
            "thanks",
            "thank",
            "kind",
            "trust",
            "share",
            "friend",
            "support",
            "sorry",
            "도와",
            "부탁",
            "고마워",
            "감사",
            "친절",
            "믿",
            "공유",
            "나눠",
            "친구",
            "지원",
            "미안",
        ],
        "negative": [
            "attack",
            "hate",
            "steal",
            "threat",
            "enemy",
            "betray",
            "공격",
            "싫어",
            "훔쳐",
            "위협",
            "적",
            "배신",
        ],
    },
    "neuroticism": {
        "positive": [
            "afraid",
            "fear",
            "worry",
            "angry",
            "sad",
            "danger",
            "stress",
            "panic",
            "anxious",
            "hurt",
            "무서",
            "두려",
            "걱정",
            "화나",
            "슬퍼",
            "위험",
            "스트레스",
            "패닉",
            "불안",
            "아파",
        ],
        "negative": [
            "calm",
            "safe",
            "stable",
            "relax",
            "okay",
            "침착",
            "안전",
            "안정",
            "편안",
            "괜찮",
        ],
    },
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


def _score_trait(
    normalized_sentence: str,
    words: set[str],
    positive_words: list[str],
    negative_words: list[str],
) -> float:
    """Move a neutral 0.5 score up or down based on matched keywords."""
    score = 0.5

    for keyword in positive_words:
        if _keyword_matches(keyword, normalized_sentence, words):
            score += 0.1

    for keyword in negative_words:
        if _keyword_matches(keyword, normalized_sentence, words):
            score -= 0.1

    return max(0.0, min(1.0, score))


def estimate_big_five(sentence: str) -> dict:
    """Estimate simple OCEAN scores from keywords in the user sentence."""
    normalized_sentence = _normalize(sentence)
    words = _tokenize(normalized_sentence)
    scores = BigFiveScores()

    for trait, keyword_groups in KEYWORDS.items():
        setattr(
            scores,
            trait,
            _score_trait(
                normalized_sentence=normalized_sentence,
                words=words,
                positive_words=keyword_groups["positive"],
                negative_words=keyword_groups["negative"],
            ),
        )

    return asdict(scores)
