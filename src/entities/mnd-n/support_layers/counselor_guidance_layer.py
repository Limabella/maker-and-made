from copy import deepcopy

from knowledge.evidence_catalog import get_evidence


GUIDANCE_CUES = {
    "five_to_one_feedback": (
        "5긍정",
        "5 긍정",
        "5:1",
        "칭찬",
        "피드백",
        "positive feedback",
    ),
    "slow_breathing": (
        "호흡",
        "숨쉬",
        "숨 쉬",
        "4-7-8",
        "478 호흡",
        "breathing",
        "breathwork",
    ),
    "resilience": (
        "회복탄력",
        "회복 탄력",
        "스트레스 회복",
        "다시 일어",
        "resilience",
    ),
    "positive_psychology": (
        "긍정심리",
        "긍정 심리",
        "perma",
        "강점",
        "감사",
        "flourish",
    ),
    "psychology_concept": (
        "심리학 용어",
        "심리 용어",
        "무슨 뜻",
        "개념을 설명",
        "개념 알려",
        "psychology term",
    ),
}


GUIDANCE_CARDS = {
    "five_to_one_feedback": {
        "topic": "positive_first_feedback",
        "kind": "practice_heuristic",
        "principle": (
            "관찰 가능한 긍정적 행동을 충분히 인정한 뒤, 바꾸면 좋을 행동 한 가지만 "
            "구체적으로 제안합니다. 5:1은 연습용 구조이며 숫자를 억지로 채우지 않습니다."
        ),
        "practice_steps": [
            "진실하고 구체적인 긍정적 행동이나 노력을 최대 다섯 가지 찾습니다.",
            "성격이 아니라 관찰한 행동과 그 영향을 말합니다.",
            "한 번에 바꿀 행동은 한 가지만, 선택 가능한 부탁으로 제시합니다.",
            "내담자가 받아들일 준비가 되었는지 확인합니다.",
        ],
        "suggested_message": (
            "계속 이야기해 준 점과 작은 시도를 소중하게 보고 있어요. 괜찮다면 한 가지, "
            "힘들어질 때 잠시 멈추겠다고 알려주는 연습을 함께 해볼까요?"
        ),
        "research_note": (
            "긍정·부정 상호작용의 균형은 부부 갈등 연구에서 다뤄졌습니다. 이를 상담 전반의 "
            "보편적인 5:1 처방으로 일반화하기보다 긍정적 관찰을 충분히 표현하는 연습 규칙으로 사용합니다."
        ),
        "evidence": get_evidence("interaction_balance"),
        "caution": "과장된 칭찬, 거짓 칭찬, 중요한 문제의 축소에는 사용하지 않습니다.",
    },
    "slow_breathing": {
        "topic": "consent_based_slow_breathing",
        "kind": "evidence_informed_option",
        "principle": (
            "호흡을 통제하라고 지시하기 전에 동의를 구하고, 숨 참기를 강요하지 않는 편안한 "
            "느린 호흡을 짧게 제안한 뒤 느낌을 다시 확인합니다."
        ),
        "practice_steps": [
            "지금 호흡 연습을 해볼 의향이 있는지 묻습니다.",
            "편안한 범위에서 천천히 들이쉬고 내쉬도록 안내합니다.",
            "30~60초 뒤 불편함, 어지러움, 숨 가쁨을 확인합니다.",
            "불편하면 즉시 평소 호흡으로 돌아가고 다른 방법을 선택합니다.",
        ],
        "suggested_message": (
            "괜찮다면 숨을 참지 말고 편안한 속도로 조금 천천히 호흡해볼까요? "
            "불편하거나 어지러우면 바로 평소 호흡으로 돌아가도 됩니다."
        ),
        "research_note": (
            "느린 자발 호흡이 세션 중과 이후의 미주신경성 HRV 증가와 관련된다는 메타분석이 있습니다. "
            "웨어러블 연구에서는 고정 안내보다 심박·호흡 반응에 맞춘 적응형 안내도 시험되었습니다."
        ),
        "evidence": get_evidence(
            "slow_breathing_meta_analysis",
            "adaptive_wearable_biofeedback",
        ),
        "caution": (
            "4-7-8 같은 특정 패턴을 기본 정답으로 강요하지 않습니다. 호흡곤란, 흉통, 심한 어지러움이 "
            "있으면 중단하고 적절한 의료 도움을 우선합니다."
        ),
    },
    "resilience": {
        "topic": "resilience_as_recovery_process",
        "kind": "research_translation",
        "principle": (
            "회복탄력성을 즉시 괜찮아지는 성격으로 보지 않고, 스트레스 이후 시간이 지나며 나타나는 "
            "회복 과정과 사용할 수 있는 자원을 함께 살핍니다."
        ),
        "practice_steps": [
            "지금 당장의 감정을 먼저 인정합니다.",
            "이전에 버텨낸 방법이나 도움받을 수 있는 사람을 한 가지 찾습니다.",
            "즉시 해결보다 다음 확인 시점을 정합니다.",
            "나중의 변화도 현재 상태와 함께 기록합니다.",
        ],
        "suggested_message": (
            "지금 바로 괜찮아져야 한다고 재촉하지 않을게요. 이전에 조금이라도 버티는 데 도움이 된 것과, "
            "한 시간쯤 뒤 다시 확인해볼 작은 신호를 함께 정해볼까요?"
        ),
        "research_note": (
            "2026년 급성 스트레스 연구에서는 회복탄력성과 관련된 신경생리 차이가 스트레스 직후보다 "
            "약 1시간 뒤의 변화에서 두드러졌습니다. 이는 개인을 뇌 신호로 판정하라는 뜻이 아니라 "
            "회복의 시간 경과를 관찰할 근거입니다."
        ),
        "evidence": get_evidence("resilience_neural_signatures"),
        "caution": "연구의 집단 수준 뇌영상 결과를 개별 내담자의 상태나 회복탄력성 점수로 추론하지 않습니다.",
    },
    "positive_psychology": {
        "topic": "perma_micro_intervention",
        "kind": "evidence_informed_option",
        "principle": (
            "부정 감정을 지우지 않은 채 PERMA 영역 중 지금 가능한 한 가지 자원을 골라 작은 행동으로 연결합니다."
        ),
        "practice_steps": [
            "현재 어려움과 감정을 먼저 인정합니다.",
            "긍정 정서·몰입·관계·의미·성취 중 도움이 될 한 영역을 고릅니다.",
            "내담자가 선택할 수 있는 아주 작은 행동 하나를 제안합니다.",
            "도움이 되었는지 자기보고로 다시 확인합니다.",
        ],
        "suggested_message": (
            "힘든 감정을 없애려 하지 않고 그대로 두어도 괜찮아요. 그 옆에 오늘 해낸 작은 일이나 "
            "도움을 청할 수 있는 사람 한 가지를 함께 찾아볼까요?"
        ),
        "research_note": (
            "PERMA는 웰빙을 여러 영역으로 보는 측정 틀이며 치료 처방은 아닙니다. 긍정심리 중재 메타분석은 "
            "평균적으로 작은 효과를 보고했지만 연구 간 차이와 연구 품질의 한계도 함께 보고했습니다."
        ),
        "evidence": get_evidence("perma_profiler", "positive_psychology_meta_analysis"),
        "caution": "감사나 긍정 표현을 강요하거나 고통의 원인과 현실적 문제를 덮는 데 사용하지 않습니다.",
    },
    "psychology_concept": {
        "topic": "psychology_concept_education",
        "kind": "grounded_education",
        "principle": (
            "용어의 일반적 정의와 내담자에 대한 판단을 분리하고, 출처가 있는 설명을 실제 대화에 적용할지 함께 검토합니다."
        ),
        "practice_steps": [
            "용어의 출처와 정의를 확인합니다.",
            "번역이 검토본인지 기계 번역 초안인지 표시합니다.",
            "용어를 내담자의 성격이나 진단명으로 붙이지 않습니다.",
            "적용 전 내담자의 경험과 맞는지 열린 질문으로 확인합니다.",
        ],
        "suggested_message": (
            "이 용어는 사람을 규정하는 이름이 아니라 경험을 이해하기 위한 하나의 관점이에요. "
            "이 설명이 지금 경험과 맞는 부분이 있는지 함께 살펴볼까요?"
        ),
        "research_note": "활성화된 LightRAG가 있으면 검토된 심리학 용어집의 출처와 페이지를 함께 제시합니다.",
        "evidence": [],
        "caution": "검색 결과만으로 진단하거나 성격을 추론하지 않습니다.",
    },
}


PERMA_TO_CARD = {
    "positive_emotion": "positive_psychology",
    "engagement": "positive_psychology",
    "relationships": "five_to_one_feedback",
    "meaning": "resilience",
    "accomplishment": "positive_psychology",
}


def recommend_counselor_guidance(
    user_sentence: str,
    mnd_n_support: dict,
    safety: dict,
) -> dict:
    """Build guidance for the player acting as a counselor in the simulation."""
    if safety.get("triggered"):
        return {
            "active": False,
            "mode": "safety",
            "audience": "player_as_virtual_counselor",
            "topic": None,
            "kind": None,
            "principle": "일반 상담 연습 안내를 멈추고 안전 절차를 우선합니다.",
            "practice_steps": [],
            "suggested_message": None,
            "research_note": None,
            "evidence": [],
            "caution": safety.get("message"),
        }

    normalized = " ".join(user_sentence.lower().split())
    card_name = next(
        (
            name
            for name, cues in GUIDANCE_CUES.items()
            if any(cue in normalized for cue in cues)
        ),
        None,
    )
    if card_name is None:
        card_name = PERMA_TO_CARD.get(
            mnd_n_support.get("perma_axis"),
            "positive_psychology",
        )

    guidance = deepcopy(GUIDANCE_CARDS[card_name])
    guidance.update(
        {
            "active": True,
            "mode": "counselor_support",
            "audience": "player_as_virtual_counselor",
            "card": card_name,
        }
    )
    return guidance


def format_counselor_guidance(guidance: dict) -> str:
    """Render a concise MND-N line without losing research boundaries."""
    if not guidance.get("active"):
        return guidance["principle"]

    return (
        f"상담자 안내: {guidance['principle']} "
        f"예시: “{guidance['suggested_message']}” "
        f"연구 메모: {guidance['research_note']}"
    )
