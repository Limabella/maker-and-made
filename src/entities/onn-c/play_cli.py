from pathlib import Path
import argparse
import os
import sys

MND_N_PATH = Path(__file__).parents[1] / "mnd-n"
if str(MND_N_PATH) not in sys.path:
    sys.path.insert(0, str(MND_N_PATH))

from main import run_pipeline
from layers.memory_layer import MemoryLayer
from support_layers.llm_expression_layer import generate_nvidia_expression


COMMANDS = {"/help", "/quit", "/exit", "/reset", "/state"}
REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
SUPPORTED_ENV_KEYS = {
    "NVIDIA_API_KEY",
    "NVIDIA_MODEL",
    "NIM_MODEL",
    "NVIDIA_API_BASE_URL",
    "NVIDIA_TIMEOUT_SECONDS",
}


def _load_local_env(path: Path = REPOSITORY_ROOT / ".env") -> None:
    """Load simple KEY=VALUE entries without overriding shell variables."""
    if not path.exists():
        return

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        if key.lower().startswith("$env:"):
            key = key[5:].strip()
        value = value.strip().strip('"').strip("'")
        if key in SUPPORTED_ENV_KEYS:
            os.environ.setdefault(key, value)


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
    _load_local_env()
    args = _parse_args()
    memory_path = Path(__file__).parent / "data" / "play_cli_memory.json"
    memory = MemoryLayer(memory_path)

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
            print("Memory reset.")
            continue

        if command.startswith("/") and command not in COMMANDS:
            print("Unknown command. Use /help.")
            continue

        result = run_pipeline(user_sentence, memory)
        if args.nvidia:
            print("NVIDIA 응답 생성 중...", flush=True)
        expression = (
            generate_nvidia_expression(
                user_sentence,
                result,
                recent_interactions=memory.load_interactions()[:-1],
            )
            if args.nvidia
            else None
        )
        if expression:
            memory.update_last_interaction(
                {
                    "onn_c_line": expression["onn_c_line"],
                    "mnd_n_line": expression["mnd_n_line"],
                    "expression_provider": expression["provider"],
                }
            )
        _print_result(result, expression=expression)


if __name__ == "__main__":
    sys.exit(main())
