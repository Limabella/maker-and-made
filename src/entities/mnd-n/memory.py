from datetime import datetime


class MemoryStore:

    def __init__(self):
        self.memories = []

    def add_memory(self, text, emotion):

        memory = {
            "timestamp": datetime.utcnow().isoformat(),
            "summary": text[:120],
            "emotion": emotion,
        }

        self.memories.append(memory)

    def recent_memories(self, limit=5):
        return self.memories[-limit:]