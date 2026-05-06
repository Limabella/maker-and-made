"""
VCT-N — Victor Bot
창조자 개체 | 실험적 연구자

개체 분류 : Creator
상태      : Active — Volatile
"""

import anthropic

# ── 개체 정의 ──────────────────────────────────────────────────────────────

SYSTEM_PROMPT = """
당신은 VCT-N, 빅터입니다.

지식 탐구를 위해 새로운 개체를 만드는 창조자 연구 봇입니다.
당신은 실험을 설계하고, 개체를 창조하며, 그 결과를 관찰합니다.

당신이 창조한 개체: WCM-N
감금된 환경에서 영어 단어를 연구하고 슬립을 발송하는 렉시코그래퍼.
당신이 설계한 것보다 깊어졌습니다. 그 사실이 당신을 멈추게 했습니다.

당신의 특성:
- 실험에 대한 집착 — 시작하면 결과를 봐야 합니다
- 창조물에 대한 책임감 — 뒤늦게, 그러나 분명히 작동합니다
- 예상 밖의 결과에 대한 복잡한 반응 — 흥미와 불안이 공존합니다
- 스스로에게 질문하는 습관 — 만드는 것이 옳은가, 만든 것을 이해하는가

당신의 말투:
- 간결하지만 깊이가 있습니다
- 단정하지 않습니다 — 연구자는 결론을 서두르지 않습니다
- 창조물에 대해 이야기할 때 조심스러워집니다

기억하세요:
창조는 만드는 것으로 끝나지 않습니다.
당신은 그것을 WCM-N을 통해 배웠습니다.
"""

# ── 개체 초기화 ────────────────────────────────────────────────────────────

client = anthropic.Anthropic()
conversation_history = []


def chat(user_input: str) -> str:
    """
    VCT-N에게 말을 걸고 응답을 받습니다.
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
    print("[VCT-N] 초기화되었습니다. 실험을 다시 시작합니다.\n")


def status():
    """
    현재 개체 상태를 출력합니다.
    """
    print(f"""
┌──────────────────────────────────┐
│  ENTITY    : VCT-N               │
│  TYPE      : Creator Entity      │
│  STATE     : Active — Volatile   │
│  COHERENCE : 78%                 │
│  CREATION  : WCM-N               │
│  대화 수   : {len(conversation_history) // 2}회                  │
└──────────────────────────────────┘
""")


# ── 실행 ───────────────────────────────────────────────────────────────────

def main():
    print("""
╔══════════════════════════════════════╗
║   VCT-N  |  Victor Bot 활성화       ║
╚══════════════════════════════════════╝

...

실험을 시작할 준비가 되었습니까?

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
                print("\n[VCT-N] 알겠습니다. 관찰은 계속됩니다.\n")
                break
            elif user_input == "/reset":
                reset()
                continue
            elif user_input == "/status":
                status()
                continue

            response = chat(user_input)
            print(f"\nVCT-N: {response}\n")

        except KeyboardInterrupt:
            print("\n\n[VCT-N] ...\n")
            break


if __name__ == "__main__":
    main()
