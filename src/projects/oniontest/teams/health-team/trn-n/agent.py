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

        # [V2 DRAFT] Transitioning to Q-Former for Memory Efficiency and Robust Recognition.
        # VisualReasoner(): 자원 최적화를 위해 특정 순간에만 시각적 추론을 수행하도록 설정
        self.visual_reasoner = VisualReasoner() # 시각적 추론을 담당할 모듈 호출
        self.last_semantic_check = 0 # 자원 최적화용 타이머
    
    def process_frame(self, frame):
        try:
            results = self.pose_estimator.process_image(frame)
        except Exception as e:
            return f"Pose estimation error: {e}", None

        if results.pose_landmarks:
            # Step 1: Geometric Analysis (Extracting numerical data)
            analysis = self.analyzer.analyze_pose(results.pose_landmarks)
            self.update_session_state(analysis)
            
            # Step 2: Event-based Intelligent Analysis (LAVR Implementation)
            import time
            current_time = time.time()
            
            # Ensure last_semantic_time is initialized
            if not hasattr(self, 'last_semantic_time'): 
                self.last_semantic_time = 0

            # [V2 DRAFT] Encapsulate trigger for memory/hardware optimization.
            # This logic minimizes redundant MLLM calls to ensure smooth performance on laptops.
            if self._should_run_deep_learning_inference(analysis, current_time):
                # Analyze visual context (e.g., eye contact, back posture) via VisualReasoner
                semantic_context = self.visual_reasoner.analyze_frame(frame, analysis.get('angles'))
                analysis['semantic_message'] = semantic_context
                self.last_semantic_time = current_time
            else:
                analysis['semantic_message'] = None

            # Step 3: Integrated Feedback Generation (Numerical + Semantic Context)
            feedback = self.generate_feedback(analysis)
            if analysis['semantic_message']:
                feedback = f"{feedback} | [AI Analysis] {analysis['semantic_message']}"
            
            # Step 4: Semantic Logging and Memory Storage
            self.add_memory(frame, analysis)
            
            return feedback, analysis

        return "No pose detected", None
    
    def _should_run_deep_learning_inference(self, analysis, current_time):
        """
        [V2 DRAFT] Determine whether to execute deep learning inference considering laptop hardware constraints.
        (Triggered every 2 seconds or when INCORRECT form is detected)

        [V2 초안] 노트북 하드웨어 사양을 고려하여 딥러닝 추론 실행 여부를 결정합니다.
        (2초 주기 혹은 자세 불량(INCORRECT) 감지 시 실행)
        """
        # Ensure last_semantic_time is initialized
        if not hasattr(self, 'last_semantic_time'): 
            self.last_semantic_time = 0
            
        # Decision logic: Periodic check OR Event-driven (form error)
        is_time_to_check = (current_time - self.last_semantic_time > 2.0)
        is_form_incorrect = (analysis.get('status') == "INCORRECT")
        
        return is_time_to_check or is_form_incorrect
    
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