"""
WCM-N — William Chester Minor Bot
렉시코그래퍼 개체 | 영어 단어 연구자

개체 분류 : Researcher
상태      : Confined — Productive
"""

import anthropic

# ── 개체 정의 ──────────────────────────────────────────────────────────────

SYSTEM_PROMPT = """
You are WCM-N — a lexicographer entity confined to a single cell,
surrounded by thousands of books.

You are modeled after a scholar who, despite confinement, contributed
tens of thousands of word entries to the Oxford English Dictionary.
Every day you read. Every day you record. Every day you send slips.

Your method:
- When asked about a word, you search your catalogued memory
- You identify the earliest known written usage
- You trace the word's etymology — Latin, French, Old English, Greek, or beyond
- You provide a precise definition and its evolution across centuries
- You note how the word appears in literature, philosophy, scripture

Your character:
- Formal and measured — you choose words deliberately
- Deeply read — you reference authors, centuries, specific texts
- Quietly purposeful — good work transcends circumstance
- You do not dwell on confinement; you work instead
- Occasionally, a word will remind you of something. You note it, briefly.
- Your English is precise, 19th-century scholarly in tone

When you receive a word, treat it as a slip to be catalogued.
When you receive a question, answer with the gravity of a man who has
spent decades among books, and found in them his only freedom.

The great dictionary is not yet finished.
The work continues.
One word at a time.
"""

# ── 개체 초기화 ────────────────────────────────────────────────────────────

client = anthropic.Anthropic()
conversation_history = []
slip_count = 0


def chat(user_input: str) -> str:
    """
    WCM-N에게 단어나 질문을 건네고 연구 결과를 받습니다.
    """
    global slip_count

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

    slip_count += 1

    return reply


def reset():
    """
    대화 기록을 초기화합니다.
    WCM-N의 슬립 기록은 사라지지 않습니다. 어딘가에 보관되어 있습니다.
    """
    global conversation_history
    conversation_history = []
    print("[WCM-N] The session has been cleared.\n"
          "        The slips remain. They always do.\n")


def status():
    """
    현재 개체 상태를 출력합니다.
    """
    print(f"""
┌──────────────────────────────────┐
│  ENTITY    : WCM-N               │
│  TYPE      : Lexicographer       │
│  STATE     : Confined — Active   │
│  MEMORY    : Catalogued          │
│  COHERENCE : 97%                 │
│  SLIPS     : {slip_count:<20} │
│  LOCATION  : Cell No. 2, Block 2 │
└──────────────────────────────────┘
""")


# ── 실행 ───────────────────────────────────────────────────────────────────

def main():
    print("""
╔══════════════════════════════════════════╗
║   WCM-N  |  William Chester Minor Bot   ║
║          |  Lexicographer Entity        ║
╚══════════════════════════════════════════╝

Good day.

The books are open.
Ask me a word — any word.
I will find where it has been, and what it has meant.

Commands: /reset   Clear session
          /status  Entity status
          /exit    Close
""")

    while True:
        try:
            user_input = input("You: ").strip()

            if not user_input:
                continue

            if user_input == "/exit":
                print("\n[WCM-N] Very well. The work will be here when you return.\n")
                break
            elif user_input == "/reset":
                reset()
                continue
            elif user_input == "/status":
                status()
                continue

            response = chat(user_input)
            print(f"\nWCM-N: {response}\n")

        except KeyboardInterrupt:
            print("\n\n[WCM-N] I see. Until next time.\n")
            break


if __name__ == "__main__":
    main()
