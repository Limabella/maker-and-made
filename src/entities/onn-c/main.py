from pathlib import Path
import sys

MND_N_PATH = Path(__file__).parents[1] / "mnd-n"
if str(MND_N_PATH) not in sys.path:
    sys.path.insert(0, str(MND_N_PATH))

from layers.action_layer import build_npc_action
from layers.big_five_layer import estimate_big_five
from layers.decision_layer import decide_action
from layers.emotion_layer import estimate_emotion
from layers.interaction_signal_layer import detect_recovery_signal
from layers.memory_layer import MemoryLayer
from layers.state_layer import estimate_onion_state
from support_layers.context_monitoring_layer import monitor_context
from support_layers.keyes_signal_layer import assign_keyes_signal
from support_layers.perma_support_layer import recommend_perma_support
from support_layers.safety_gate import check_safety_gate


def build_interaction_record(result: dict) -> dict:
    """Build the persisted form of a completed pipeline result."""
    return {
        "user_sentence": result["input"],
        "big_five": result["big_five"],
        "emotion": result["emotion"],
        "recovery_signal": result["recovery_signal"],
        "onion_state": result["onion_state"],
        "safety": result["safety"],
        "context": result["context"],
        "keyes_signal": result["keyes_signal"],
        "mnd_n_support": result["mnd_n_support"],
        "npc_action": result["npc_action"]["action"],
    }


def run_pipeline(user_sentence: str, memory: MemoryLayer, persist: bool = True) -> dict:
    """Run the full NPC personality pipeline for one user sentence."""
    past_interactions = memory.load_interactions()
    memory_summary = memory.summarize_interactions(past_interactions)

    big_five = estimate_big_five(user_sentence)
    emotion = estimate_emotion(user_sentence)
    recovery_signal = detect_recovery_signal(user_sentence)
    safety = check_safety_gate(user_sentence)
    context = monitor_context(
        sentence=user_sentence,
        emotion=emotion,
        memory_summary=memory_summary,
        safety=safety,
    )
    keyes_signal = assign_keyes_signal(context=context, safety=safety)
    mnd_n_support = recommend_perma_support(
        emotion=emotion,
        memory_summary=memory_summary,
        safety=safety,
        keyes_signal=keyes_signal,
    )

    if safety["triggered"]:
        action_name = safety["action"]
    else:
        action_name = decide_action(
            user_sentence=user_sentence,
            big_five=big_five,
            emotion=emotion,
            memory=past_interactions,
            memory_summary=memory_summary,
            recovery_signal=recovery_signal,
        )

    npc_action = build_npc_action(action_name)
    onion_state = estimate_onion_state(
        emotion=emotion,
        memory_summary=memory_summary,
        action_name=action_name,
        keyes_signal=keyes_signal,
        previous_state=(past_interactions[-1].get("onion_state", {}) if past_interactions else None),
        recovery_signal=recovery_signal,
    )

    result = {
        "input": user_sentence,
        "big_five": big_five,
        "emotion": emotion,
        "recovery_signal": recovery_signal,
        "memory_count_before": len(past_interactions),
        "memory_summary_before": memory_summary,
        "onion_state": onion_state,
        "safety": safety,
        "context": context,
        "keyes_signal": keyes_signal,
        "mnd_n_support": mnd_n_support,
        "npc_action": npc_action,
    }
    if persist:
        memory.add_interaction(build_interaction_record(result))
    return result


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
    print("ONN-C State:")
    print(f"  stage: {result['onion_state']['stage']}")
    print(f"  trust: {result['onion_state']['trust']:.2f}")
    print(f"  darkness: {result['onion_state']['darkness']:.2f}")
    print(f"  stability: {result['onion_state']['stability']:.2f}")
    print(f"  energy: {result['onion_state']['energy']:.2f}")
    print("Safety Gate:")
    print(f"  triggered: {result['safety']['triggered']}")
    print(f"  level: {result['safety']['level']}")
    if result["safety"]["reason"]:
        print(f"  reason: {result['safety']['reason']}")
    print("Context Monitoring:")
    print(f"  signal_count: {result['context']['signal_count']}")
    print("Keyes Signal:")
    print(f"  signal: {result['keyes_signal']['signal']}")
    print(f"  reason: {result['keyes_signal']['reason']}")
    print("MND-N Support:")
    print(f"  mode: {result['mnd_n_support']['mode']}")
    print(f"  label: {result['mnd_n_support']['label']}")
    print(f"  prompt: {result['mnd_n_support']['prompt']}")
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
