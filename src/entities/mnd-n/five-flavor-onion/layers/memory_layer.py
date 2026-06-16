import json
from pathlib import Path


POSITIVE_ACTIONS = {"greet", "help", "joke"}
NEGATIVE_ACTIONS = {"refuse", "avoid"}


def _clamp(value: float) -> float:
    return max(0.0, min(1.0, value))


class MemoryLayer:
    """Stores and retrieves previous NPC interactions from a JSON file."""

    def __init__(self, memory_path: Path):
        self.memory_path = memory_path
        self.memory_path.parent.mkdir(parents=True, exist_ok=True)
        self._ensure_memory_file()

    def _ensure_memory_file(self) -> None:
        if not self.memory_path.exists():
            self.memory_path.write_text('{"interactions": []}\n', encoding="utf-8")

    def load_interactions(self) -> list[dict]:
        """Load previous interactions, returning an empty list if the file is invalid."""
        try:
            data = json.loads(self.memory_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            data = {"interactions": []}

        interactions = data.get("interactions", [])
        if not isinstance(interactions, list):
            return []

        return interactions

    def add_interaction(self, interaction: dict) -> None:
        """Append a new interaction and save it back to disk."""
        interactions = self.load_interactions()
        interactions.append(interaction)

        self.memory_path.write_text(
            json.dumps({"interactions": interactions}, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

    def summarize_interactions(self, interactions: list[dict] | None = None) -> dict:
        """Summarize past interactions into a small attitude state."""
        if interactions is None:
            interactions = self.load_interactions()

        total_score = 0.0
        positive_count = 0
        negative_count = 0
        recent_negative_streak = 0

        for interaction in interactions:
            score = self._score_interaction(interaction)
            total_score += score

            if score > 0:
                positive_count += 1
            elif score < 0:
                negative_count += 1

        for interaction in reversed(interactions):
            if self._score_interaction(interaction) < 0:
                recent_negative_streak += 1
            else:
                break

        # Trust moves slowly but accumulates across repeated interactions.
        trust_level = _clamp(0.5 + total_score * 0.08)
        familiarity = _clamp(len(interactions) / 5)

        return {
            "total_interactions": len(interactions),
            "positive_interactions": positive_count,
            "negative_interactions": negative_count,
            "recent_negative_streak": recent_negative_streak,
            "trust_level": trust_level,
            "familiarity": familiarity,
        }

    def _score_interaction(self, interaction: dict) -> float:
        """Score one memory item as positive or negative for future decisions."""
        emotion = interaction.get("emotion", {})
        action = interaction.get("npc_action")

        positive_emotion = emotion.get("joy", 0.0) + emotion.get("trust", 0.0)
        negative_emotion = emotion.get("anger", 0.0) + emotion.get("sadness", 0.0)
        score = positive_emotion - negative_emotion

        if action in POSITIVE_ACTIONS:
            score += 0.2
        elif action in NEGATIVE_ACTIONS:
            score -= 0.2

        return score
