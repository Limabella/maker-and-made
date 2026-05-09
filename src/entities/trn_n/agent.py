import json
import cv2
import os
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
        
        # MediaPipe will be integrated later
        # For now, using basic OpenCV
        self.pose = None
        self.analyzer = MotionAnalyzer()
        self.short_term_memory = ShortTermMemory()
        self.long_term_memory = LongTermMemory()
        
        self.session_state = {
            'current_exercise': None,
            'rep_count': 0,
            'form_errors': []
        }
    
    def process_frame(self, frame):
        # Convert to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # TODO: Integrate MediaPipe for pose detection
        # For now, return placeholder response
        if self.pose is None:
            return "Pose detection not yet integrated", None
        
        # Process pose
        results = self.pose.process(rgb_frame)
        
        if results.pose_landmarks:
            # Analyze motion
            analysis = self.analyzer.analyze_pose(results.pose_landmarks)
            
            # Update session state
            self.update_session_state(analysis)
            
            # Generate feedback
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