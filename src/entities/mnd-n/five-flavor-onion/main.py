from pathlib import Path
import sys

from layers.action_layer import build_npc_action
from layers.big_five_layer import estimate_big_five
from layers.decision_layer import decide_action
from layers.emotion_layer import estimate_emotion
from layers.memory_layer import MemoryLayer


def run_pipeline(user_sentence: str, memory: MemoryLayer) -> dict:
    """Run the full NPC personality pipeline for one user sentence."""
    past_interactions = memory.load_interactions()
    memory_summary = memory.summarize_interactions(past_interactions)

    big_five = estimate_big_five(user_sentence)
    emotion = estimate_emotion(user_sentence)
    action_name = decide_action(
        user_sentence=user_sentence,
        big_five=big_five,
        emotion=emotion,
        memory=past_interactions,
        memory_summary=memory_summary,
    )
    npc_action = build_npc_action(action_name)

    memory.add_interaction(
        {
            "user_sentence": user_sentence,
            "big_five": big_five,
            "emotion": emotion,
            "npc_action": npc_action["action"],
        }
    )

    return {
        "input": user_sentence,
        "big_five": big_five,
        "emotion": emotion,
        "memory_count_before": len(past_interactions),
        "memory_summary_before": memory_summary,
        "npc_action": npc_action,
    }


def print_result(result: dict) -> None:
    """Print a compact view of the pipeline output."""
    print("\nInput:")
    print(f"  {result['input']}")

    print("Big Five:")
    for trait, score in result["big_five"].items():
        print(f"  {trait}: {score:.2f}")

    print("Emotion:")
    for emotion, score in result["emotion"].items():
        print(f"  {emotion}: {score:.2f}")

    memory_summary = result["memory_summary_before"]
    print(f"Previous interactions: {result['memory_count_before']}")
    print("Memory:")
    print(f"  trust_level: {memory_summary['trust_level']:.2f}")
    print(f"  familiarity: {memory_summary['familiarity']:.2f}")
    print(f"  recent_negative_streak: {memory_summary['recent_negative_streak']}")
    print("NPC Action:")
    print(f"  action: {result['npc_action']['action']}")
    print(f"  line: {result['npc_action']['line']}")


def main() -> None:
    memory_path = Path(__file__).parent / "data" / "npc_memory.json"
    memory = MemoryLayer(memory_path)

    # Simple test scenario. You can also pass a sentence from the command line.
    user_sentence = " ".join(sys.argv[1:]) or "안녕 친구야, 새로운 장소를 탐험하게 도와줄래?"
    result = run_pipeline(user_sentence, memory)
    print_result(result)


if __name__ == "__main__":
    main()
