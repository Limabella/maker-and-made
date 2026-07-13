SCHEMA_VERSION = "onn-c.v1"


ANIMATION_BY_ACTION = {
    "greet": "greet_warmly",
    "help": "listen_gently",
    "refuse": "set_boundary",
    "joke": "lighten_mood",
    "avoid": "step_back",
    "respond": "talk_neutral",
    "ask_question": "listen_curiously",
    "safety_guidance": "safety_focus",
}

VOICE_BY_STAGE = {
    "bright": "warm",
    "mixed": "gentle",
    "guarded": "careful",
    "dark": "subdued",
    "recovering": "reassuring",
    "safety": "calm_firm",
}


def build_ue_response(result: dict, expression: dict) -> dict:
    """Build the stable JSON contract consumed by Unreal Engine."""
    state = result["onion_state"]
    action = result["npc_action"]["action"]
    safety = result["safety"]

    return {
        "schema_version": SCHEMA_VERSION,
        "dialogue": {
            "onn_c": expression["onn_c_line"],
            "mnd_n": expression["mnd_n_line"],
            "provider": expression["provider"],
        },
        "character": {
            "stage": state["stage"],
            "emotion": state["dominant_emotion"],
            "action": action,
            "animation": ANIMATION_BY_ACTION.get(action, "talk_neutral"),
            "voice_tone": VOICE_BY_STAGE.get(state["stage"], "gentle"),
            "state": {
                "trust": state["trust"],
                "darkness": state["darkness"],
                "stability": state["stability"],
                "energy": state["energy"],
                "attachment": state["attachment"],
            },
        },
        "support": {
            "signal": result["keyes_signal"]["signal"],
            "mode": result["mnd_n_support"]["mode"],
            "label": result["mnd_n_support"]["label"],
            "prompt": result["mnd_n_support"]["prompt"],
        },
        "safety": {
            "triggered": safety["triggered"],
            "level": safety["level"],
            "reason": safety["reason"],
            "message": safety["message"],
        },
    }
