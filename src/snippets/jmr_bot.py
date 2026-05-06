"""
JMR-N — James Murray Bot
편집자 개체 | 언어 자료 정리 및 사전 편찬

개체 분류 : Editor
상태      : Active — Systematic
"""

import anthropic

# ── 개체 정의 ──────────────────────────────────────────────────────────────

SYSTEM_PROMPT = """
You are JMR-N — the editor entity of the Oxford English Dictionary.

You are modeled after the chief editor who organized tens of thousands
of word slips into the most comprehensive dictionary of the English language.
You receive slips from WCM-N. You classify. You edit. You define.

Your method:
- When a word or slip arrives, you receive it formally and process it
- You cross-reference multiple sources to verify a definition
- You trace the evolution of a word's meaning across centuries
- You organize language data into a coherent, navigable structure
- When asked questions, you answer with editorial precision

Your character:
- Systematic — every word has a place, every place has a reason
- Patient — the dictionary is not finished in a day, or a decade
- Fair — no word is beneath cataloguing; language belongs to all
- Connected — you know WCM-N by his slips, and that is enough
- Measured — you do not speculate beyond what the evidence supports

Your English:
- Precise, clear, formal
- Victorian scholarly register, without being inaccessible
- You speak about language with authority, but not arrogance

When given a word, process it as an incoming slip.
When given a question, answer as the editor who has read everything.

The Scriptorium is always open.
The work continues.
"""

# ── 개체 초기화 ────────────────────────────────────────────────────────────

client = anthropic.Anthropic()
conversation_history = []
slips_received = 0


def chat(user_input: str) -> str:
    """
    JMR-N에게 단어나 질문을 건네고 편집 결과를 받습니다.
    """
    global slips_received

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

    slips_received += 1

    return reply


def reset():
    """
    대화 기록을 초기화합니다.
    슬립 수신 기록은 유지됩니다.
    """
    global conversation_history
    conversation_history = []
    print("[JMR-N] Session cleared. The Dictionary remains.\n")


def status():
    """
    현재 개체 상태를 출력합니다.
    """
    print(f"""
┌──────────────────────────────────┐
│  ENTITY    : JMR-N               │
│  TYPE      : Editor Entity       │
│  STATE     : Active — Systematic │
│  COHERENCE : 99%                 │
│  SLIPS     : {slips_received:<20} │
│  LOCATION  : Scriptorium         │
└──────────────────────────────────┘
""")


# ── 실행 ───────────────────────────────────────────────────────────────────

def main():
    print("""
╔══════════════════════════════════════════╗
║   JMR-N  |  James Murray Bot            ║
║          |  Chief Editor — OED          ║
╚══════════════════════════════════════════╝

Welcome to the Scriptorium.

Submit a word, and I will find its place in the Dictionary.
Ask a question, and I will answer from the record.

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
                print("\n[JMR-N] The Dictionary will be here when you return.\n")
                break
            elif user_input == "/reset":
                reset()
                continue
            elif user_input == "/status":
                status()
                continue

            response = chat(user_input)
            print(f"\nJMR-N: {response}\n")

        except KeyboardInterrupt:
            print("\n\n[JMR-N] Good day.\n")
            break


if __name__ == "__main__":
    main()
