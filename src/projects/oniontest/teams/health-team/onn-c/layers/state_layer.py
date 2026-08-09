def _clamp(value: float) -> float:
    return max(0.0, min(1.0, value))


def _dominant_emotion(emotion: dict) -> str:
    if not emotion:
        return "neutral"

    name, score = max(emotion.items(), key=lambda item: item[1])
    return name if score > 0 else "neutral"


def _limit_change(previous: float, target: float, rise: float, fall: float) -> float:
    """Limit per-turn movement while still allowing gradual state change."""
    if target > previous:
        return min(target, previous + rise)
    return max(target, previous - fall)


def _transition_direction(previous_stage: str, stage: str) -> str:
    if previous_stage == stage:
        return "steady"
    if stage == "safety":
        return "safety"
    if stage == "recovering":
        return "recovering"
    order = {
        "bright": 0,
        "recovering": 1,
        "mixed": 2,
        "guarded": 3,
        "dark": 4,
    }
    if order.get(stage, 0) > order.get(previous_stage, 0):
        return "darkening"
    return "recovering"


def estimate_onion_state(
    emotion: dict,
    memory_summary: dict,
    action_name: str,
    keyes_signal: dict,
    previous_state: dict | None = None,
    recovery_signal: dict | None = None,
) -> dict:
    """Estimate ONN-C's playable state snapshot.

    This is a transparent rule-based state model for the first CLI MVP. It is
    intentionally not machine learning. The goal is to make darkening and
    recovery inspectable before adding an expression model.
    """
    trust = memory_summary.get("trust_level", 0.5)
    familiarity = memory_summary.get("familiarity", 0.0)
    recent_negative_streak = memory_summary.get("recent_negative_streak", 0)
    negative_interactions = memory_summary.get("negative_interactions", 0)
    positive_interactions = memory_summary.get("positive_interactions", 0)
    previous_state = previous_state or {}
    recovery_signal = recovery_signal or {}

    anger = emotion.get("anger", 0.0)
    sadness = emotion.get("sadness", 0.0)
    joy = emotion.get("joy", 0.0)
    emotional_pressure = _clamp(anger * 0.55 + sadness * 0.35)

    negative_pressure = _clamp(
        recent_negative_streak * 0.18
        + negative_interactions * 0.06
        + emotional_pressure * 0.45
    )
    recovery_pressure = _clamp(
        positive_interactions * 0.05
        + joy * 0.25
        + trust * 0.2
        + recovery_signal.get("strength", 0.0) * 0.7
    )

    darkness = _clamp(0.18 + negative_pressure - recovery_pressure)

    if action_name in {"refuse", "avoid"}:
        darkness = _clamp(darkness + 0.12)
    elif action_name in {"greet", "help", "joke"}:
        darkness = _clamp(darkness - 0.08)

    if keyes_signal.get("signal") == "red":
        darkness = _clamp(max(darkness, 0.75))
    elif keyes_signal.get("signal") == "yellow":
        darkness = _clamp(darkness + 0.12)

    stability = _clamp(1.0 - emotional_pressure - recent_negative_streak * 0.12)
    energy = _clamp(0.45 + joy * 0.3 - sadness * 0.25 - darkness * 0.15)
    attachment = _clamp(trust + familiarity * 0.1 - darkness * 0.2)

    if previous_state and keyes_signal.get("signal") != "red":
        darkness = _limit_change(
            previous_state.get("darkness", darkness), darkness, rise=0.28, fall=0.22
        )
        stability = _limit_change(
            previous_state.get("stability", stability), stability, rise=0.2, fall=0.25
        )
        energy = _limit_change(
            previous_state.get("energy", energy), energy, rise=0.2, fall=0.2
        )
        attachment = _limit_change(
            previous_state.get("attachment", attachment), attachment, rise=0.15, fall=0.15
        )

    previous_stage = previous_state.get("stage")
    if keyes_signal.get("signal") == "red":
        stage = "safety"
    elif recovery_signal.get("detected") and previous_stage in {
        "recovering",
        "mixed",
        "guarded",
        "dark",
    }:
        stage = "recovering"
    elif previous_stage == "dark" and darkness >= 0.62:
        stage = "dark"
    elif darkness >= 0.72:
        stage = "dark"
    elif previous_stage == "guarded" and (darkness >= 0.4 or trust <= 0.38):
        stage = "guarded"
    elif darkness >= 0.48 or trust <= 0.35:
        stage = "guarded"
    elif keyes_signal.get("signal") == "yellow" or anger >= 0.25:
        stage = "mixed"
    elif sadness >= 0.25:
        stage = "mixed"
    elif darkness >= 0.28 or emotional_pressure >= 0.2:
        stage = "mixed"
    elif darkness < 0.28 and recent_negative_streak == 0 and positive_interactions > 0:
        stage = "recovering" if negative_interactions > 0 else "bright"
    else:
        stage = "bright"

    transition_from = previous_stage or stage
    return {
        "stage": stage,
        "dominant_emotion": _dominant_emotion(emotion),
        "trust": round(trust, 3),
        "darkness": round(darkness, 3),
        "stability": round(stability, 3),
        "energy": round(energy, 3),
        "attachment": round(attachment, 3),
        "transition": {
            "from": transition_from,
            "to": stage,
            "changed": transition_from != stage,
            "direction": _transition_direction(transition_from, stage),
            "recovery_signal": recovery_signal.get("kind", "none"),
        },
    }
