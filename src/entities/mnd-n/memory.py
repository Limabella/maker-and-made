from datetime import datetime
import json
import os


class ShortTermMemory:

    def __init__(self, limit=20):

        self.limit = limit
        self.memories = []

    def add_memory(self, text, emotion):

        memory = {
            "timestamp": datetime.utcnow().isoformat(),
            "summary": text[:120],
            "emotion": emotion,
        }

        self.memories.append(memory)

        # 메모리 제한 유지
        if len(self.memories) > self.limit:
            self.memories.pop(0)

    def get_recent(self, limit=5):

        return self.memories[-limit:]


class LongTermMemory:

    def __init__(self, path="memory.json"):

        self.path = path

        self.data = {
            "emotion_patterns": {},
            "relationship": {
                "trust": 0.5,
                "attachment": 0.0
            }
        }

        self.load()

    def load(self):

        if not os.path.exists(self.path):
            self.save()
            return

        with open(self.path, "r", encoding="utf-8") as f:
            self.data = json.load(f)

    def save(self):

        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(
                self.data,
                f,
                ensure_ascii=False,
                indent=2
            )

    def update_emotion(self, emotion):

        patterns = self.data["emotion_patterns"]

        patterns[emotion] = (
            patterns.get(emotion, 0) + 1
        )

        self.save()

    def update_relationship(self, trust_delta=0.0):

        self.data["relationship"]["trust"] += trust_delta

        self.save()

    def get_emotion_patterns(self):

        return self.data["emotion_patterns"]

    def get_relationship(self):

        return self.data["relationship"]