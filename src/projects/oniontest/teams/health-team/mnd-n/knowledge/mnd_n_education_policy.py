EXPLICIT_KNOWLEDGE_CUES = [
    "심리학 용어",
    "심리 용어",
    "무슨 뜻",
    "개념을 설명",
    "개념 알려",
    "연구 사례",
    "근거가 있",
    "내담자에게 권",
    "어떤 말을",
    "호흡법",
    "회복탄력성",
    "긍정심리학",
    "psychology term",
    "define ",
    "what does ",
]


def should_retrieve_psychology_knowledge(user_sentence: str) -> bool:
    normalized = " ".join(user_sentence.lower().split())
    return any(cue in normalized for cue in EXPLICIT_KNOWLEDGE_CUES)


def educational_answer_instruction(retrieved_context: str | None = None) -> str:
    instruction = (
        "Use the retrieved glossary only for optional education. "
        "Do not diagnose, label, or infer a user's personality. "
        "Clearly distinguish a general concept from a judgment about the user. "
        "Answer concisely in natural Korean without mixing in other languages, "
        "retain the English term in parentheses, and include "
        "the source document and page. If translation_status is machine_draft, "
        "say that the Korean translation is provisional."
    )
    if retrieved_context:
        instruction += f"\n\nRetrieved context:\n{retrieved_context}"
    return instruction
