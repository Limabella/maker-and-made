from dataclasses import dataclass
from datetime import datetime


@dataclass
class EmotionState:
    stress: float = 0.0
    anxiety: float = 0.0
    trust: float = 0.5
    fatigue: float = 0.0
    attachment: float = 0.0
    loneliness: float = 0.0
    stability: float = 1.0

    updated_at: str = datetime.utcnow().isoformat()


def update_emotion(state, analysis):

    state.stress = analysis["stress"]

    emotion = analysis["emotion"]

    if emotion == "anxiety":
        state.anxiety += 0.1
        state.stability -= 0.05

    elif emotion == "loneliness":
        state.loneliness += 0.1

    elif emotion == "positive":
        state.trust += 0.05
        state.stability += 0.02

    return state