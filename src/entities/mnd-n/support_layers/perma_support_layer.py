PERMA_GUIDES = {
    "positive_emotion": {
        "label": "Positive Emotion",
        "prompt": "Notice one small safe or pleasant signal before continuing.",
    },
    "engagement": {
        "label": "Engagement",
        "prompt": "Choose one small activity that fits the onion's current energy.",
    },
    "relationships": {
        "label": "Relationships",
        "prompt": "Repair the interaction with one respectful, low-pressure step.",
    },
    "meaning": {
        "label": "Meaning",
        "prompt": "Connect the next action to a small reason that matters.",
    },
    "accomplishment": {
        "label": "Accomplishment",
        "prompt": "Make the next step small enough to finish now.",
    },
}


def recommend_perma_support(
    emotion: dict,
    memory_summary: dict,
    safety: dict,
    keyes_signal: dict | None = None,
) -> dict:
    """Return MND-N's bounded PERMA/Flourish support recommendation.

    MND-N is a third helper, not a therapist. The recommendation should guide
    dialogue and action selection without diagnosing the user or the character.
    """
    if safety.get("triggered"):
        return {
            "active": False,
            "mode": "safety",
            "perma_axis": None,
            "label": "Safety",
            "prompt": "Pause PERMA guidance and switch to safety guidance.",
        }

    keyes_signal = keyes_signal or {"signal": "green"}
    caution_signal = keyes_signal.get("signal") == "yellow"

    anger = emotion.get("anger", 0.0)
    sadness = emotion.get("sadness", 0.0)
    joy = emotion.get("joy", 0.0)
    trust = emotion.get("trust", 0.0)
    memory_trust = memory_summary.get("trust_level", 0.5)
    recent_negative_streak = memory_summary.get("recent_negative_streak", 0)

    if anger >= 0.5 or recent_negative_streak >= 2 or caution_signal:
        axis = "relationships"
    elif sadness >= 0.5:
        axis = "meaning"
    elif trust >= 0.5 and memory_trust >= 0.5:
        axis = "engagement"
    elif joy >= 0.5:
        axis = "positive_emotion"
    else:
        axis = "accomplishment"

    guide = PERMA_GUIDES[axis]
    return {
        "active": True,
        "mode": "support",
        "keyes_signal": keyes_signal.get("signal"),
        "perma_axis": axis,
        "label": guide["label"],
        "prompt": guide["prompt"],
    }
