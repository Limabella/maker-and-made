class ShortTermMemory:
    def __init__(self):
        self.memories = []
    
    def add_memory(self, input_data, analysis):
        self.memories.append({
            'input': input_data,
            'analysis': analysis,
            'timestamp': None  # Add timestamp if needed
        })
        if len(self.memories) > 10:  # Limit to last 10
            self.memories.pop(0)
    
    def get_recent_memories(self):
        return self.memories[-5:]  # Last 5

class LongTermMemory:
    def __init__(self):
        self.sessions = []
    
    def update_session(self, session_data):
        self.sessions.append(session_data)
    
    def get_past_sessions(self):
        return self.sessions