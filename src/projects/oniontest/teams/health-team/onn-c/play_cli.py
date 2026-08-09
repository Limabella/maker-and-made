import argparse
import os
import sys
from pathlib import Path

MND_N_PATH = Path(__file__).parent.parent / "mnd-n"
if str(MND_N_PATH) not in sys.path:
    sys.path.insert(0, str(MND_N_PATH))

from config import load_local_env
from conversation_service import ConversationService
from layers.memory_layer import MemoryLayer


COMMANDS = {"/help", "/quit", "/exit", "/reset", "/state"}
def _print_help(use_nvidia: bool) -> None:
    print(
        "\nCommands:\n"
        "  /help   show commands\n"
        "  /state  show current memory summary\n"
        "  /reset  clear this CLI play memory\n"
        "  /quit   exit\n"
        f"\nNVIDIA expression mode: {'on' if use_nvidia else 'off'}\n"
    )


def _print_result(result: dict, expression: dict | None = None) -> None:
    onion_state = result["onion_state"]
    keyes_signal = result["keyes_signal"]
    support = result["mnd_n_support"]
    guidance = result["counselor_guidance"]
    action = result["npc_action"]

    print("\nONN-C")
    print(f"  stage      : {onion_state['stage']}")
    print(f"  action     : {action['action']}")
    print(f"  line       : {action['line']}")
    print(
        "  state      : "
        f"trust={onion_state['trust']:.2f}, "
        f"darkness={onion_state['darkness']:.2f}, "
        f"stability={onion_state['stability']:.2f}, "
        f"energy={onion_state['energy']:.2f}, "
        f"attachment={onion_state['attachment']:.2f}"
    )
    print(f"  emotion    : {onion_state['dominant_emotion']}")
    if expression:
        print(f"  says       : {expression['onn_c_line']}")

    print("\nMND-N")
    print(f"  signal     : {keyes_signal['signal']} ({keyes_signal['reason']})")
    print(f"  mode       : {support['mode']}")
    print(f"  guide      : {support['label']} - {support['prompt']}")
    print(f"  topic      : {guidance['topic'] or 'safety'}")
    print(f"  principle  : {guidance['principle']}")
    if guidance.get("suggested_message"):
        print(f"  try saying : {guidance['suggested_message']}")
    if guidance.get("research_note"):
        print(f"  evidence   : {guidance['research_note']}")
    if guidance.get("caution"):
        print(f"  caution    : {guidance['caution']}")
    if expression:
        print(f"  says       : {expression['mnd_n_line']}")
        print(f"  expression : {expression['provider']}")
        if expression.get("error"):
            print(f"  error      : {expression['error']}")

    if result["safety"]["triggered"]:
        print(f"  safety     : {result['safety']['message']}")


def _print_state(memory: MemoryLayer) -> None:
    summary = memory.summarize_interactions()
    print("\nMemory Summary")
    print(f"  total_interactions      : {summary['total_interactions']}")
    print(f"  positive_interactions   : {summary['positive_interactions']}")
    print(f"  negative_interactions   : {summary['negative_interactions']}")
    print(f"  recent_negative_streak  : {summary['recent_negative_streak']}")
    print(f"  trust_level             : {summary['trust_level']:.2f}")
    print(f"  familiarity             : {summary['familiarity']:.2f}")


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Playable ONN-C CLI MVP.")
    parser.add_argument(
        "--nvidia",
        action="store_true",
        help="Use NVIDIA-compatible chat endpoint as expression layer.",
    )
    return parser.parse_args()


def main() -> None:
    load_local_env()
    args = _parse_args()
    memory_path = Path(__file__).parent / "data" / "play_cli_memory.json"
    memory = MemoryLayer(memory_path)
    service = ConversationService(memory, use_nvidia=args.nvidia)

    print("Five Flavor Onion CLI MVP")
    print("Type as the player. Use /help for commands.\n")
    if args.nvidia:
        print("NVIDIA expression mode is on. State and safety decisions remain rule-based.\n")
        print(
            "NVIDIA model: "
            f"{os.getenv('NVIDIA_MODEL') or os.getenv('NIM_MODEL') or 'nvidia/nvidia-nemotron-nano-9b-v2'}\n"
        )

    while True:
        try:
            user_sentence = input("Player > ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBye.")
            return

        if not user_sentence:
            continue

        command = user_sentence.lower()
        if command in {"/quit", "/exit"}:
            print("Bye.")
            return

        if command == "/help":
            _print_help(args.nvidia)
            continue

        if command == "/state":
            _print_state(memory)
            continue

        if command == "/reset":
            memory_path.unlink(missing_ok=True)
            memory = MemoryLayer(memory_path)
            service = ConversationService(memory, use_nvidia=args.nvidia)
            print("Memory reset.")
            continue

        if command.startswith("/") and command not in COMMANDS:
            print("Unknown command. Use /help.")
            continue

        if args.nvidia:
            print("NVIDIA 응답 생성 중...", flush=True)
        turn = service.respond(user_sentence)
        _print_result(turn.result, expression=turn.expression)


if __name__ == "__main__":
    sys.exit(main())
