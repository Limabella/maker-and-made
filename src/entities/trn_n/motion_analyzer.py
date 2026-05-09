import math

class MotionAnalyzer:
    def __init__(self):
        self.rep_count = 0
        self.in_rep = False
        self.exercise_type = None
    
    def analyze_pose(self, landmarks):
        # Extract key joint positions
        left_shoulder = self.get_landmark(landmarks, 11)
        right_shoulder = self.get_landmark(landmarks, 12)
        left_hip = self.get_landmark(landmarks, 23)
        right_hip = self.get_landmark(landmarks, 24)
        left_knee = self.get_landmark(landmarks, 25)
        right_knee = self.get_landmark(landmarks, 26)
        left_ankle = self.get_landmark(landmarks, 27)
        right_ankle = self.get_landmark(landmarks, 28)
        
        # Calculate angles
        left_knee_angle = self.calculate_angle(left_hip, left_knee, left_ankle)
        right_knee_angle = self.calculate_angle(right_hip, right_knee, right_ankle)
        
        # Detect exercise (simple heuristic for squat)
        if left_knee_angle < 120 and right_knee_angle < 120:
            exercise = "squat"
            if not self.in_rep and left_knee_angle < 90:
                self.in_rep = True
            elif self.in_rep and left_knee_angle > 150:
                self.rep_count += 1
                self.in_rep = False
        else:
            exercise = None
        
        # Form checks
        errors = []
        if abs(left_knee_angle - right_knee_angle) > 20:
            errors.append("Uneven knee bend")
        if left_knee.x < left_ankle.x or right_knee.x < right_ankle.x:
            errors.append("Knees caving in")
        
        return {
            'exercise_type': exercise,
            'rep_count': self.rep_count,
            'angles': {
                'left_knee': left_knee_angle,
                'right_knee': right_knee_angle
            },
            'errors': errors
        }
    
    def get_landmark(self, landmarks, idx):
        return landmarks.landmark[idx]
    
    def calculate_angle(self, a, b, c):
        # Calculate angle at b between points a, b, c
        ab = math.sqrt((b.x - a.x)**2 + (b.y - a.y)**2)
        bc = math.sqrt((b.x - c.x)**2 + (b.y - c.y)**2)
        ac = math.sqrt((c.x - a.x)**2 + (c.y - a.y)**2)
        
        cos_angle = (ab**2 + bc**2 - ac**2) / (2 * ab * bc)
        angle = math.acos(cos_angle)
        return math.degrees(angle)