ACTION_LINES = {
    "greet": "The NPC greets the player warmly.",
    "help": "The NPC offers practical help.",
    "refuse": "The NPC refuses to cooperate.",
    "joke": "The NPC makes a light joke to ease the moment.",
    "avoid": "The NPC backs away and avoids deeper contact.",
    "respond": "The NPC responds directly to the player.",
    "ask_question": "The NPC asks a follow-up question.",
    "safety_guidance": "MND-N pauses gamified advice and switches to safety guidance.",
}


def build_npc_action(action: str) -> dict:
    """Return the final NPC action payload."""
    if action not in ACTION_LINES:
        action = "respond"

    return {
        "action": action,
        "line": ACTION_LINES[action],
    }
