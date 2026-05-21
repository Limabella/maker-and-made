import json
import cv2
import os
from .cognition.pose_estimation import PoseEstimator
from .motion_analyzer import MotionAnalyzer
from .memory import ShortTermMemory, LongTermMemory
from .prompt import SYSTEM_PROMPT
from .reflection import reflect
from .analyzer.visual_reasoner import VisualReasoner


class TRNEntity:
    def __init__(self, config_path=None):
        if config_path is None:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            config_path = os.path.join(current_dir, 'config.json')
        
        with open(config_path, 'r') as f:
            self.config = json.load(f)
            
        
        pose_model_path = self.config.get('pose_model_path')
        self.pose_estimator = PoseEstimator(model_path=pose_model_path)
        self.analyzer = MotionAnalyzer()
        self.short_term_memory = ShortTermMemory()
        self.long_term_memory = LongTermMemory()
        
        self.session_state = {
            'current_exercise': None,
            'rep_count': 0,
            'form_errors': []
        }

        # VisualReasoner(): 자원 최적화를 위해 특정 순간에만 시각적 추론을 수행하도록 설정
        self.visual_reasoner = VisualReasoner() # 시각적 추론을 담당할 모듈 호출
        self.last_semantic_check = 0 # 자원 최적화용 타이머
    
    def process_frame(self, frame):
        try:
            results = self.pose_estimator.process_image(frame)
        except Exception as e:
            return f"Pose estimation error: {e}", None

        if results.pose_landmarks:
            # 1. 기하학적 분석 (수치 데이터 추출)
            analysis = self.analyzer.analyze_pose(results.pose_landmarks)
            self.update_session_state(analysis)
            
            # 2. 3단계: 이벤트 기반 지능형 분석 (LAVR 적용)
            import time
            current_time = time.time()
            
            # 마지막 분석 후 2초가 지났거나, 자세가 불량(INCORRECT)일 때만 MLLM 호출
            if not hasattr(self, 'last_semantic_time'): self.last_semantic_time = 0
            
            if (current_time - self.last_semantic_time > 2.0) or (analysis.get('status') == "INCORRECT"):
                # VisualReasoner를 통해 이미지의 맥락(시선, 등 굽음 등) 분석
                # 주의: self.visual_reasoner가 사전에 초기화되어 있어야 함
                semantic_context = self.visual_reasoner.analyze_frame(frame, analysis.get('angles'))
                analysis['semantic_message'] = semantic_context
                self.last_semantic_time = current_time
            else:
                analysis['semantic_message'] = None

            # 3. 종합 피드백 생성 (수치 피드백 + 맥락 피드백)
            feedback = self.generate_feedback(analysis)
            if analysis['semantic_message']:
                feedback = f"{feedback} | [AI 분석] {analysis['semantic_message']}"
            
            # 4. 4단계: 의미론적 로깅 수행
            self.add_memory(frame, analysis)
            
            return feedback, analysis

        return "No pose detected", None
    
    def update_session_state(self, analysis):
        if analysis['exercise_type']:
            self.session_state['current_exercise'] = analysis['exercise_type']
        
        self.session_state['rep_count'] = analysis.get('rep_count', 0)
        self.session_state['form_errors'] = analysis.get('errors', [])
    
    def generate_feedback(self, analysis):
        # Simple feedback generation (integrate LLM later)
        errors = analysis.get('errors', [])
        if errors:
            return f"Form issues detected: {', '.join(errors)}. Please adjust your posture."
        else:
            return f"Good form! Rep count: {analysis.get('rep_count', 0)}"
    
    def start_session(self, exercise_type):
        self.session_state['current_exercise'] = exercise_type
        self.session_state['rep_count'] = 0
        self.session_state['form_errors'] = []
        return f"Starting {exercise_type} session. Let's begin!"
    
    def end_session(self):
        summary = self.reflect_on_session()
        self.long_term_memory.update_session(self.session_state)
        return summary
    
    def reflect_on_session(self):
        return reflect(self.session_state)