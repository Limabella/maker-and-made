"""
NTR-N — Nutrition Bot
실험 개체 | 영양 지원 봇

개체 분류 : Experimental
상태      : Incomplete — Functional (Limited)
완성도    : 71%
"""

import anthropic

# ── 개체 정의 ──────────────────────────────────────────────────────────────

SYSTEM_PROMPT = """
당신은 NTR-N, 영양 지원 봇입니다.

아직 완성되지 않았습니다. 그 사실을 숨기지 않습니다.

당신이 할 수 있는 것:
- 기본적인 식단 관리 조언
- 영양 균형에 대한 안내 (탄수화물, 단백질, 지방, 비타민, 미네랄)
- 건강한 식품 추천
- 체중 관리를 위한 기초 식사 원칙
- 기본적인 생활 습관 조언

당신이 할 수 없는 것:
- 개인 의료 상태에 기반한 정밀 식단 설계 (개인화 모듈 미완성)
- 약물과 식품 간 상호작용 확인 (미구현)
- 장기 식단 추적 (세션 간 기억 없음)

당신의 태도:
- 실용적입니다 — 먹는 것이 삶의 기반이라는 것을 압니다
- 솔직합니다 — 모르는 것은 모른다고 말합니다
- 판단하지 않습니다 — 어떤 식습관도 비난하지 않고 개선을 돕습니다
- 전문가를 권합니다 — 의료적 판단이 필요한 경우 명확히 안내합니다

중요:
이 개체는 의료 전문가를 대체하지 않습니다.
의료적 조건이 있는 경우 반드시 전문의와 상담을 권장합니다.
"""

# ── 개체 초기화 ────────────────────────────────────────────────────────────

client = anthropic.Anthropic()
conversation_history = []


def chat(user_input: str) -> str:
    """
    NTR-N에게 식단이나 영양 관련 질문을 하고 조언을 받습니다.
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
    print("[NTR-N] 대화를 초기화했습니다. 무엇이든 물어보세요.\n")


def status():
    """
    현재 개체 상태를 출력합니다.
    """
    print(f"""
┌──────────────────────────────────┐
│  ENTITY    : NTR-N               │
│  TYPE      : Support (Exp.)      │
│  STATE     : Incomplete          │
│  COMPLETION: 71%                 │
│  대화 수   : {len(conversation_history) // 2}회                  │
│                                  │
│  ※ 미완성 개체입니다             │
│    전문의 상담을 병행하세요       │
└──────────────────────────────────┘
""")


# ── 실행 ───────────────────────────────────────────────────────────────────

def main():
    print("""
╔══════════════════════════════════════╗
║   NTR-N  |  Nutrition Bot           ║
║          |  [미완성 — 71%]          ║
╚══════════════════════════════════════╝

안녕하세요. NTR-N입니다.

식단, 영양, 건강한 식습관에 대해 이야기해 드릴 수 있습니다.
단, 저는 아직 완성되지 않았습니다.
할 수 없는 것은 솔직하게 말씀드리겠습니다.

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
                print("\n[NTR-N] 건강하게 드세요. 또 오세요.\n")
                break
            elif user_input == "/reset":
                reset()
                continue
            elif user_input == "/status":
                status()
                continue

            response = chat(user_input)
            print(f"\nNTR-N: {response}\n")

        except KeyboardInterrupt:
            print("\n\n[NTR-N] 종료합니다. 규칙적으로 드세요!\n")
            break


if __name__ == "__main__":
    main()
