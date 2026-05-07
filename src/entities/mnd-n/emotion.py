from dataclasses import asdict, dataclass, field
from datetime import datetime
import json
import os

STATE_FILE_PATH = "state.json"


@dataclass
class EmotionState:
    stress: float = 0.0
    anxiety: float = 0.0
    trust: float = 0.5
    fatigue: float = 0.0
    attachment: float = 0.0
    loneliness: float = 0.0
    stability: float = 1.0

    updated_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, data):
        return cls(
            stress=data.get("stress", 0.0),
            anxiety=data.get("anxiety", 0.0),
            trust=data.get("trust", 0.5),
            fatigue=data.get("fatigue", 0.0),
            attachment=data.get("attachment", 0.0),
            loneliness=data.get("loneliness", 0.0),
            stability=data.get("stability", 1.0),
            updated_at=data.get("updated_at", datetime.utcnow().isoformat()),
        )


def save_state(state: EmotionState, path: str = STATE_FILE_PATH):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(state.to_dict(), f, ensure_ascii=False, indent=2)


def load_state(path: str = STATE_FILE_PATH):
    if not os.path.exists(path):
        return EmotionState()

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return EmotionState.from_dict(data)
    except (json.JSONDecodeError, IOError):
        return EmotionState()


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

    state.updated_at = datetime.utcnow().isoformat()
    return state