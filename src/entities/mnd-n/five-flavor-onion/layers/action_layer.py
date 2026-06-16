ACTION_LINES = {
    "greet": "The NPC greets the player warmly.",
    "help": "The NPC offers practical help.",
    "refuse": "The NPC refuses to cooperate.",
    "joke": "The NPC makes a light joke to ease the moment.",
    "avoid": "The NPC backs away and avoids deeper contact.",
    "ask_question": "The NPC asks a follow-up question.",
}


def build_npc_action(action: str) -> dict:
    """Return the final NPC action payload."""
    if action not in ACTION_LINES:
        action = "ask_question"

    return {
        "action": action,
        "line": ACTION_LINES[action],
    }
