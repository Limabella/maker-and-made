def assign_keyes_signal(context: dict, safety: dict) -> dict:
    """Convert observed signals into a Green/Yellow/Red operating signal.

    This is not a diagnosis. It is an operational caution signal for MND-N's
    support policy.
    """
    if safety.get("triggered"):
        return {
            "signal": "red",
            "reason": safety.get("reason") or "safety_gate_triggered",
            "allow_gamified_guidance": False,
        }

    if (
        context.get("repeated_negative_signal")
        or context.get("trust_drop_signal")
        or context.get("elevated_negative_emotion")
        or context.get("aggressive_matches")
    ):
        return {
            "signal": "yellow",
            "reason": "repeated_or_elevated_context_signal",
            "allow_gamified_guidance": True,
        }

    return {
        "signal": "green",
        "reason": "ordinary_interaction",
        "allow_gamified_guidance": True,
    }
