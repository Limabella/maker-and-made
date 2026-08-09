class ShortTermMemory:
    def __init__(self):
        self.memories = []
    
    def add_memory(self, frame, analysis):
        from datetime import datetime
        
        # 4단계: 의미론적 로깅 (Semantic Logging)
        # 단순 수치 외에 AI가 판단한 '이유'를 함께 저장합니다.
        log_entry = {
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'exercise_status': analysis.get('status'),
            'reps': analysis.get('count'),
            'angles': analysis.get('angles'),
            'geometric_feedback': analysis.get('message'),
            'semantic_analysis': analysis.get('semantic_message'), # AI의 맥락 분석 결과
        }
        
        self.memories.append(log_entry)
        
        # 메모리 최적화 (최근 10개 유지)
        if len(self.memories) > 10:
            self.memories.pop(0)
            
        # (선택 사항) 로컬 파일이나 DB에 의미론적 로그 저장
        # self.save_to_persistent_storage(log_entry)
    
    def get_recent_memories(self):
        return self.memories[-5:]  # Last 5

class LongTermMemory:
    def __init__(self):
        self.sessions = []
    
    def update_session(self, session_data):
        self.sessions.append(session_data)
    
    def get_past_sessions(self):
        return self.sessions