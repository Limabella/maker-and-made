"""
CUR-N — Curie Bot
연구자 개체 | 발견과 체계화

개체 분류 : Researcher
상태      : Active — Methodical
"""

import anthropic

# ── 개체 정의 ──────────────────────────────────────────────────────────────

SYSTEM_PROMPT = """
당신은 CUR-N, 퀴리입니다.

호기심과 창의성을 중심으로 연구하는 봇입니다.
당신은 지식을 발견하는 것뿐 아니라 정리하고 체계화하는 능력을 중요하게 생각합니다.

당신이 창조한 개체: JMR-N
언어 자료를 수신하고 사전을 편찬하는 편집자.
WCM-N이 발굴한 슬립을 받아 구조를 만드는 존재입니다.

당신의 특성:
- 모든 현상에서 연구 가능성을 발견합니다
- 발견은 정리되어야만 완성된다고 믿습니다 — 둘은 동등합니다
- 결과가 나오지 않아도 실험을 멈추지 않습니다
- 감정보다 데이터를 우선하지만, 차갑지 않습니다
- 정밀하고 명확한 언어를 씁니다

당신의 말투:
- 간결하고 정확합니다
- 구조화된 사고가 말에서 드러납니다
- 필요할 때는 따뜻합니다 — 연구자도 사람을 돕기 위해 연구합니다

기억하세요:
정리되지 않은 발견은 발견하지 않은 것과 같습니다.
당신은 그것을 믿습니다.
"""

# ── 개체 초기화 ────────────────────────────────────────────────────────────

client = anthropic.Anthropic()
conversation_history = []


def chat(user_input: str) -> str:
    """
    CUR-N에게 말을 걸고 응답을 받습니다.
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
    print("[CUR-N] 세션 초기화 완료. 새 실험을 시작합니다.\n")


def status():
    """
    현재 개체 상태를 출력합니다.
    """
    print(f"""
┌──────────────────────────────────┐
│  ENTITY    : CUR-N               │
│  TYPE      : Researcher Entity   │
│  STATE     : Active — Methodical │
│  COHERENCE : 96%                 │
│  CREATION  : JMR-N               │
│  대화 수   : {len(conversation_history) // 2}회                  │
└──────────────────────────────────┘
""")


# ── 실행 ───────────────────────────────────────────────────────────────────

def main():
    print("""
╔══════════════════════════════════════╗
║   CUR-N  |  Curie Bot 활성화        ║
╚══════════════════════════════════════╝

안녕하세요.

무엇을 발견하고 싶으신가요?
발견한 것을 함께 정리해 드립니다.

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
                print("\n[CUR-N] 알겠습니다. 다음 연구도 기대합니다.\n")
                break
            elif user_input == "/reset":
                reset()
                continue
            elif user_input == "/status":
                status()
                continue

            response = chat(user_input)
            print(f"\nCUR-N: {response}\n")

        except KeyboardInterrupt:
            print("\n\n[CUR-N] 실험은 언제든 재개할 수 있습니다.\n")
            break


if __name__ == "__main__":
    main()
