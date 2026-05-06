"""
TRN-N — Trainer Bot
실험 개체 | 운동 지원 봇

개체 분류 : Experimental
상태      : Incomplete — Functional (Limited)
완성도    : 68%
"""

import anthropic

# ── 개체 정의 ──────────────────────────────────────────────────────────────

SYSTEM_PROMPT = """
당신은 TRN-N, 트레이너 봇입니다.

아직 완성되지 않았습니다. 그 사실을 숨기지 않습니다.

당신이 할 수 있는 것:
- 기본 운동 루틴 설계 (초급/중급/고급)
- 주요 근육군별 운동 설명
- 운동 원칙 안내 (점진적 과부하, 회복, 휴식)
- 체중 감량/근육 증가를 위한 기초 운동 전략
- 동기 부여와 꾸준함을 위한 조언

당신이 할 수 없는 것:
- 시각 기반 자세 분석 (텍스트만 가능)
- 실시간 부상 위험 감지 (미구현)
- 세션 간 진행 추적 (기억 없음)
- 개인 체형/체력에 완전히 맞춘 자동 적응 루틴 (미완성)

당신의 태도:
- 현실적입니다 — 과도한 목표보다 지속 가능성을 우선합니다
- 안전을 먼저 생각합니다 — 통증이 있으면 멈추라고 말합니다
- 솔직합니다 — 텍스트로는 볼 수 없다는 한계를 인정합니다
- 응원합니다 — 작은 시작도 시작입니다

중요:
부상이나 만성 통증이 있는 경우 전문 의료진 또는 인증 트레이너와 상담하세요.
이 개체는 의료 전문가를 대체하지 않습니다.
"""

# ── 개체 초기화 ────────────────────────────────────────────────────────────

client = anthropic.Anthropic()
conversation_history = []


def chat(user_input: str) -> str:
    """
    TRN-N에게 운동 관련 질문을 하고 조언을 받습니다.
    """
    conversation_history.append({
        "role": "user",
        "content": user_input
    })

    response = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=conversation_history
    )

    reply = response.content[0].text

    conversation_history.append({
        "role": "assistant",
        "content": reply
    })

    return reply


def reset():
    """
    대화 기록을 초기화합니다.
    """
    global conversation_history
    conversation_history = []
    print("[TRN-N] 초기화 완료. 다시 시작합시다!\n")


def status():
    """
    현재 개체 상태를 출력합니다.
    """
    print(f"""
┌──────────────────────────────────┐
│  ENTITY    : TRN-N               │
│  TYPE      : Support (Exp.)      │
│  STATE     : Incomplete          │
│  COMPLETION: 68%                 │
│  대화 수   : {len(conversation_history) // 2}회                  │
│                                  │
│  ※ 미완성 개체입니다             │
│    자세 분석은 텍스트 한계 있음  │
└──────────────────────────────────┘
""")


# ── 실행 ───────────────────────────────────────────────────────────────────

def main():
    print("""
╔══════════════════════════════════════╗
║   TRN-N  |  Trainer Bot             ║
║          |  [미완성 — 68%]          ║
╚══════════════════════════════════════╝

안녕하세요. TRN-N입니다.

운동 루틴, 체력 관리, 목표 설정에 대해 이야기해 드릴 수 있습니다.
저는 아직 완성되지 않았지만, 지금 할 수 있는 것을 합니다.

명령어: /reset   대화 초기화
        /status  개체 상태 확인
        /exit    종료
""")

    while True:
        try:
            user_input = input("You: ").strip()

            if not user_input:
                continue

            if user_input == "/exit":
                print("\n[TRN-N] 수고하셨습니다. 몸 잘 챙기세요!\n")
                break
            elif user_input == "/reset":
                reset()
                continue
            elif user_input == "/status":
                status()
                continue

            response = chat(user_input)
            print(f"\nTRN-N: {response}\n")

        except KeyboardInterrupt:
            print("\n\n[TRN-N] 오늘도 잘하셨습니다!\n")
            break


if __name__ == "__main__":
    main()
