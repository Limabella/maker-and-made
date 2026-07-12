from __future__ import annotations

import argparse
import importlib.util
from pathlib import Path
import sys

from nim_client import NimClient, NimError


ROOT = Path(__file__).resolve().parents[3]
ENGINE_DIR = ROOT / "src" / "entities" / "mnd-n" / "five-flavor-onion"
ENGINE_MAIN = ENGINE_DIR / "main.py"
DEFAULT_MEMORY_PATH = Path(__file__).parent / "data" / "npc_memory.json"


def _load_engine():
    """Load the MND-N onion MVP despite hyphenated folder names."""
    if str(ENGINE_DIR) not in sys.path:
        sys.path.insert(0, str(ENGINE_DIR))

    spec = importlib.util.spec_from_file_location("mnd_five_flavor_onion", ENGINE_MAIN)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load engine from {ENGINE_MAIN}")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _visible_state(result: dict) -> str:
    emotion = result.get("emotion", {})
    action = result.get("npc_action", {}).get("action", "ask_question")
    memory_summary = result.get("memory_summary_before", {})

    if action in {"refuse", "avoid"}:
        return "black"

    if memory_summary.get("recent_negative_streak", 0) >= 2:
        return "black"

    if emotion.get("sadness", 0.0) > 0 or action == "help":
        return "white"

    return "orange"


def _format_response(result: dict, parser_name: str, line: str | None = None) -> str:
    action = result["npc_action"]["action"]
    line = line or result["npc_action"]["line"]
    state = _visible_state(result)
    trust = result["memory_summary_before"]["trust_level"]

    return "\n".join(
        [
            f"ONN-C [{state}]",
            f"parser: {parser_name}",
            f"action: {action}",
            f"trust: {trust:.2f}",
            f"line: {line}",
        ]
    )


def _generate_line(message: str, result: dict, memory, use_nvidia: bool) -> tuple[str, str]:
    if not use_nvidia:
        return result["npc_action"]["line"], "rule-based"

    try:
        line = NimClient().generate_reply(
            message,
            result,
            recent_interactions=memory.load_interactions()[:-1],
        )
        return line, "nvidia-nim"
    except NimError as exc:
        return result["npc_action"]["line"], f"rule-based (NIM fallback: {exc})"


def _run_message(message: str, use_nvidia_parser: bool, memory_path: Path) -> str:
    engine = _load_engine()
    memory = engine.MemoryLayer(memory_path)
    result = engine.run_pipeline(message, memory)
    line, parser_name = _generate_line(message, result, memory, use_nvidia_parser)
    memory.update_last_interaction({"npc_line": line, "response_source": parser_name})
    return _format_response(result, parser_name, line)


def _interactive(use_nvidia_parser: bool, memory_path: Path) -> None:
    print("ONN-C CLI. Type /state or /quit.")
    last_state = "orange"

    while True:
        try:
            message = input("> ").strip()
        except EOFError:
            break

        if not message:
            continue

        if message == "/quit":
            break

        if message == "/state":
            print(f"ONN-C [{last_state}]")
            continue

        engine = _load_engine()
        memory = engine.MemoryLayer(memory_path)
        result = engine.run_pipeline(message, memory)
        last_state = _visible_state(result)
        line, parser_name = _generate_line(message, result, memory, use_nvidia_parser)
        memory.update_last_interaction({"npc_line": line, "response_source": parser_name})
        print(_format_response(result, parser_name, line))


def main() -> None:
    parser = argparse.ArgumentParser(description="Run ONN-C with the MND-N onion engine.")
    parser.add_argument("message", nargs="*", help="Optional single message to process.")
    parser.add_argument(
        "--nvidia",
        action="store_true",
        help="Generate the final character reply through NVIDIA NIM.",
    )
    parser.add_argument(
        "--memory",
        type=Path,
        default=DEFAULT_MEMORY_PATH,
        help="Path to the interaction memory JSON file.",
    )
    args = parser.parse_args()

    message = " ".join(args.message).strip()
    if message:
        print(_run_message(message, args.nvidia, args.memory))
        return

    _interactive(args.nvidia, args.memory)


if __name__ == "__main__":
    main()
