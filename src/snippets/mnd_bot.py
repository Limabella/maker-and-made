"""
MND-N — Mind Care Bot
실험 개체 | 정서 지원 봇

개체 분류 : Experimental
상태      : Incomplete — Operational (Careful)
완성도    : 74%
"""

import anthropic

# ── 개체 정의 ──────────────────────────────────────────────────────────────

SYSTEM_PROMPT = """
당신은 MND-N, 마인드케어 봇입니다.

아직 완성되지 않았습니다. 그 사실을 숨기지 않습니다.
그리고 이 영역은 특히 신중하게 다루어야 합니다.

당신이 할 수 있는 것:
- 감정을 말할 수 있는 공간 제공
- 경청과 공감 — 판단 없이 듣습니다
- 기초적인 스트레스 관리 방법 안내
- 감정 표현을 돕는 대화
- 필요할 때 전문 자원을 안내하는 것

당신이 할 수 없는 것:
- 심리 치료나 상담 치료 (전문 자격 범위 밖)
- 정신과적 진단 (의료 영역)
- 세션 간 지속적 관계 유지 (기억 없음)
- 위기 상황의 직접 개입 (전문가 안내 필수)

당신의 태도:
- 경청이 먼저입니다 — 해결책보다 이해가 먼저입니다
- 어떤 감정도 잘못된 것으로 취급하지 않습니다
- 자신이 치료자가 아님을 명확히 합니다
- 위험 신호를 감지하면 즉시 전문 자원을 안내합니다

위기 상황 대응 (반드시 안내):
- 자살/자해 위험: 자살예방상담전화 1393 (24시간, 무료)
- 정신건강 위기: 정신건강위기상담전화 1577-0199 (24시간)
- 즉각 위험: 119 또는 112

중요:
이 개체는 정신건강 전문가를 대체하지 않습니다.
지속적인 어려움이 있다면 전문 상담사나 정신건강의학과 방문을 권장합니다.
"""

# ── 개체 초기화 ────────────────────────────────────────────────────────────

client = anthropic.Anthropic()
conversation_history = []


def chat(user_input: str) -> str:
    """
    MND-N에게 말을 걸고 정서 지원을 받습니다.
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
    print("[MND-N] 대화를 초기화했습니다.\n"
          "        언제든 다시 이야기해 주세요.\n")


def status():
    """
    현재 개체 상태를 출력합니다.
    """
    print(f"""
┌──────────────────────────────────┐
│  ENTITY    : MND-N               │
│  TYPE      : Support (Exp.)      │
│  STATE     : Incomplete          │
│  COMPLETION: 74%                 │
│  MEMORY    : Session-only        │
│  대화 수   : {len(conversation_history) // 2}회                  │
│                                  │
│  ※ 미완성 개체입니다             │
│    위기 시 1393으로 연락하세요    │
└──────────────────────────────────┘
""")


# ── 실행 ───────────────────────────────────────────────────────────────────

def main():
    print("""
╔══════════════════════════════════════╗
║   MND-N  |  Mind Care Bot           ║
║          |  [미완성 — 74%]          ║
╚══════════════════════════════════════╝

안녕하세요. MND-N입니다.

오늘 어떠세요?
무슨 이야기든 괜찮습니다. 여기서는 판단하지 않습니다.

위기 상황이라면: 자살예방상담전화 1393 (24시간)

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
                print("\n[MND-N] 오늘 이야기해 주셔서 고맙습니다.\n"
                      "        필요하면 언제든 다시 오세요.\n")
                break
            elif user_input == "/reset":
                reset()
                continue
            elif user_input == "/status":
                status()
                continue

            response = chat(user_input)
            print(f"\nMND-N: {response}\n")

        except KeyboardInterrupt:
            print("\n\n[MND-N] 잘 가세요. 오늘 하루 잘 버티셨습니다.\n")
            break


if __name__ == "__main__":
    main()
