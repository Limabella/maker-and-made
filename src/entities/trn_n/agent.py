import json
import cv2
import os
from .cognition.pose_estimation import PoseEstimator
from .motion_analyzer import MotionAnalyzer
from .memory import ShortTermMemory, LongTermMemory
from .prompt import SYSTEM_PROMPT
from .reflection import reflect

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
    
    def process_frame(self, frame):
        try:
            results = self.pose_estimator.process_image(frame)
        except FileNotFoundError as e:
            return str(e), None
        except Exception as e:
            return f"Pose estimation error: {e}", None

        if results.pose_landmarks:
            analysis = self.analyzer.analyze_pose(results.pose_landmarks)
            self.update_session_state(analysis)
            feedback = self.generate_feedback(analysis)
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