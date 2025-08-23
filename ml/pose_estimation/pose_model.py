import cv2
import mediapipe as mp
import numpy as np
import json
import math
from typing import Dict, List, Tuple, Optional
import time

class PoseEstimationModel:
    def __init__(self):
        """Initialize the pose estimation model using MediaPipe"""
        self.mp_pose = mp.solutions.pose
        self.mp_drawing = mp.solutions.drawing_utils
        self.pose = self.mp_pose.Pose(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        
        # Comprehensive exercise database with form requirements
        self.exercise_database = {
            'squat': {
                'key_angles': ['knee_angle', 'hip_angle', 'back_angle'],
                'thresholds': {
                    'knee_angle': {'min': 70, 'max': 110, 'optimal': 90},
                    'hip_angle': {'min': 45, 'max': 90, 'optimal': 70},
                    'back_angle': {'min': 160, 'max': 180, 'optimal': 170}
                },
                'alignment_checks': ['knee_alignment', 'back_straight'],
                'movement_pattern': 'vertical',
                'primary_muscles': ['quadriceps', 'glutes', 'hamstrings']
            },
            'pushup': {
                'key_angles': ['elbow_angle', 'shoulder_angle', 'back_angle'],
                'thresholds': {
                    'elbow_angle': {'min': 80, 'max': 100, 'optimal': 90},
                    'shoulder_angle': {'min': 160, 'max': 180, 'optimal': 170},
                    'back_angle': {'min': 160, 'max': 180, 'optimal': 175}
                },
                'alignment_checks': ['body_straight', 'elbow_position'],
                'movement_pattern': 'horizontal',
                'primary_muscles': ['chest', 'triceps', 'shoulders']
            },
            'lunge': {
                'key_angles': ['front_knee_angle', 'back_knee_angle', 'hip_angle'],
                'thresholds': {
                    'front_knee_angle': {'min': 80, 'max': 110, 'optimal': 90},
                    'back_knee_angle': {'min': 80, 'max': 110, 'optimal': 90},
                    'hip_angle': {'min': 45, 'max': 90, 'optimal': 70}
                },
                'alignment_checks': ['knee_alignment', 'hip_level'],
                'movement_pattern': 'forward',
                'primary_muscles': ['quadriceps', 'glutes', 'hamstrings']
            },
            'bicep_curl': {
                'key_angles': ['elbow_angle', 'shoulder_angle', 'wrist_angle'],
                'thresholds': {
                    'elbow_angle': {'min': 30, 'max': 90, 'optimal': 60},
                    'shoulder_angle': {'min': 160, 'max': 180, 'optimal': 170},
                    'wrist_angle': {'min': 160, 'max': 180, 'optimal': 170}
                },
                'alignment_checks': ['elbow_fixed', 'wrist_straight'],
                'movement_pattern': 'isolated',
                'primary_muscles': ['biceps', 'forearms']
            },
            'plank': {
                'key_angles': ['shoulder_angle', 'hip_angle', 'ankle_angle'],
                'thresholds': {
                    'shoulder_angle': {'min': 160, 'max': 180, 'optimal': 170},
                    'hip_angle': {'min': 160, 'max': 180, 'optimal': 170},
                    'ankle_angle': {'min': 160, 'max': 180, 'optimal': 170}
                },
                'alignment_checks': ['body_straight', 'core_engaged'],
                'movement_pattern': 'static',
                'primary_muscles': ['core', 'shoulders', 'glutes']
            },
            'deadlift': {
                'key_angles': ['hip_angle', 'knee_angle', 'back_angle'],
                'thresholds': {
                    'hip_angle': {'min': 30, 'max': 60, 'optimal': 45},
                    'knee_angle': {'min': 100, 'max': 140, 'optimal': 120},
                    'back_angle': {'min': 160, 'max': 180, 'optimal': 170}
                },
                'alignment_checks': ['back_straight', 'bar_path'],
                'movement_pattern': 'hinge',
                'primary_muscles': ['hamstrings', 'glutes', 'lower_back']
            },
            'overhead_press': {
                'key_angles': ['shoulder_angle', 'elbow_angle', 'wrist_angle'],
                'thresholds': {
                    'shoulder_angle': {'min': 160, 'max': 180, 'optimal': 170},
                    'elbow_angle': {'min': 80, 'max': 100, 'optimal': 90},
                    'wrist_angle': {'min': 160, 'max': 180, 'optimal': 170}
                },
                'alignment_checks': ['shoulder_alignment', 'wrist_straight'],
                'movement_pattern': 'vertical',
                'primary_muscles': ['shoulders', 'triceps']
            },
            'row': {
                'key_angles': ['shoulder_angle', 'elbow_angle', 'back_angle'],
                'thresholds': {
                    'shoulder_angle': {'min': 45, 'max': 90, 'optimal': 70},
                    'elbow_angle': {'min': 80, 'max': 120, 'optimal': 100},
                    'back_angle': {'min': 160, 'max': 180, 'optimal': 170}
                },
                'alignment_checks': ['back_straight', 'shoulder_blades'],
                'movement_pattern': 'horizontal',
                'primary_muscles': ['back', 'biceps', 'rear_deltoids']
            },
            'burpee': {
                'key_angles': ['knee_angle', 'hip_angle', 'shoulder_angle'],
                'thresholds': {
                    'knee_angle': {'min': 70, 'max': 110, 'optimal': 90},
                    'hip_angle': {'min': 45, 'max': 90, 'optimal': 70},
                    'shoulder_angle': {'min': 160, 'max': 180, 'optimal': 170}
                },
                'alignment_checks': ['full_range', 'explosive_movement'],
                'movement_pattern': 'compound',
                'primary_muscles': ['full_body']
            },
            'mountain_climber': {
                'key_angles': ['shoulder_angle', 'hip_angle', 'knee_angle'],
                'thresholds': {
                    'shoulder_angle': {'min': 160, 'max': 180, 'optimal': 170},
                    'hip_angle': {'min': 160, 'max': 180, 'optimal': 170},
                    'knee_angle': {'min': 80, 'max': 120, 'optimal': 100}
                },
                'alignment_checks': ['core_stable', 'alternating_legs'],
                'movement_pattern': 'dynamic',
                'primary_muscles': ['core', 'shoulders', 'hip_flexors']
            }
        }
        
        # Exercise detection patterns
        self.exercise_patterns = {
            'squat': {
                'primary_indicators': ['knee_bend', 'hip_drop'],
                'secondary_indicators': ['vertical_movement', 'feet_shoulder_width']
            },
            'pushup': {
                'primary_indicators': ['horizontal_position', 'arm_bend'],
                'secondary_indicators': ['body_straight', 'elbow_tuck']
            },
            'lunge': {
                'primary_indicators': ['forward_step', 'knee_bend'],
                'secondary_indicators': ['hip_drop', 'back_knee_low']
            },
            'bicep_curl': {
                'primary_indicators': ['arm_curl', 'elbow_fixed'],
                'secondary_indicators': ['wrist_straight', 'shoulder_stable']
            },
            'plank': {
                'primary_indicators': ['static_position', 'body_straight'],
                'secondary_indicators': ['core_engaged', 'shoulder_stable']
            },
            'deadlift': {
                'primary_indicators': ['hip_hinge', 'back_straight'],
                'secondary_indicators': ['knee_bend', 'bar_path']
            },
            'overhead_press': {
                'primary_indicators': ['arm_extension', 'shoulder_press'],
                'secondary_indicators': ['wrist_straight', 'core_stable']
            },
            'row': {
                'primary_indicators': ['arm_pull', 'shoulder_blade_squeeze'],
                'secondary_indicators': ['back_straight', 'elbow_bend']
            },
            'burpee': {
                'primary_indicators': ['squat_drop', 'pushup', 'jump'],
                'secondary_indicators': ['full_range', 'explosive']
            },
            'mountain_climber': {
                'primary_indicators': ['alternating_legs', 'core_stable'],
                'secondary_indicators': ['shoulder_stable', 'hip_movement']
            }
        }
    
    def calculate_angle(self, a: Tuple[float, float], b: Tuple[float, float], c: Tuple[float, float]) -> float:
        """Calculate angle between three points"""
        a = np.array([a[0], a[1]])
        b = np.array([b[0], b[1]])
        c = np.array([c[0], c[1]])
        
        radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
        angle = np.abs(radians * 180.0 / np.pi)
        
        if angle > 180.0:
            angle = 360 - angle
            
        return angle
    
    def get_landmark_coordinates(self, landmarks, landmark_idx: int) -> Optional[Tuple[float, float]]:
        """Get coordinates of a specific landmark"""
        if landmarks and landmarks.landmark:
            landmark = landmarks.landmark[landmark_idx]
            return (landmark.x, landmark.y)
        return None
    
    def calculate_all_angles(self, landmarks) -> Dict[str, float]:
        """Calculate all relevant angles for exercise analysis"""
        angles = {}
        
        # Get all landmarks
        landmarks_dict = {
            'nose': self.get_landmark_coordinates(landmarks, self.mp_pose.PoseLandmark.NOSE),
            'left_shoulder': self.get_landmark_coordinates(landmarks, self.mp_pose.PoseLandmark.LEFT_SHOULDER),
            'right_shoulder': self.get_landmark_coordinates(landmarks, self.mp_pose.PoseLandmark.RIGHT_SHOULDER),
            'left_elbow': self.get_landmark_coordinates(landmarks, self.mp_pose.PoseLandmark.LEFT_ELBOW),
            'right_elbow': self.get_landmark_coordinates(landmarks, self.mp_pose.PoseLandmark.RIGHT_ELBOW),
            'left_wrist': self.get_landmark_coordinates(landmarks, self.mp_pose.PoseLandmark.LEFT_WRIST),
            'right_wrist': self.get_landmark_coordinates(landmarks, self.mp_pose.PoseLandmark.RIGHT_WRIST),
            'left_hip': self.get_landmark_coordinates(landmarks, self.mp_pose.PoseLandmark.LEFT_HIP),
            'right_hip': self.get_landmark_coordinates(landmarks, self.mp_pose.PoseLandmark.RIGHT_HIP),
            'left_knee': self.get_landmark_coordinates(landmarks, self.mp_pose.PoseLandmark.LEFT_KNEE),
            'right_knee': self.get_landmark_coordinates(landmarks, self.mp_pose.PoseLandmark.RIGHT_KNEE),
            'left_ankle': self.get_landmark_coordinates(landmarks, self.mp_pose.PoseLandmark.LEFT_ANKLE),
            'right_ankle': self.get_landmark_coordinates(landmarks, self.mp_pose.PoseLandmark.RIGHT_ANKLE)
        }
        
        # Calculate angles if landmarks are available
        if all([landmarks_dict['left_shoulder'], landmarks_dict['left_hip'], landmarks_dict['left_knee']]):
            angles['left_knee_angle'] = self.calculate_angle(
                landmarks_dict['left_hip'], landmarks_dict['left_knee'], landmarks_dict['left_ankle']
            )
            angles['left_hip_angle'] = self.calculate_angle(
                landmarks_dict['left_shoulder'], landmarks_dict['left_hip'], landmarks_dict['left_knee']
            )
            angles['left_back_angle'] = self.calculate_angle(
                landmarks_dict['left_shoulder'], landmarks_dict['left_hip'], landmarks_dict['left_ankle']
            )
        
        if all([landmarks_dict['right_shoulder'], landmarks_dict['right_hip'], landmarks_dict['right_knee']]):
            angles['right_knee_angle'] = self.calculate_angle(
                landmarks_dict['right_hip'], landmarks_dict['right_knee'], landmarks_dict['right_ankle']
            )
            angles['right_hip_angle'] = self.calculate_angle(
                landmarks_dict['right_shoulder'], landmarks_dict['right_hip'], landmarks_dict['right_knee']
            )
            angles['right_back_angle'] = self.calculate_angle(
                landmarks_dict['right_shoulder'], landmarks_dict['right_hip'], landmarks_dict['right_ankle']
            )
        
        if all([landmarks_dict['left_shoulder'], landmarks_dict['left_elbow'], landmarks_dict['left_wrist']]):
            angles['left_elbow_angle'] = self.calculate_angle(
                landmarks_dict['left_shoulder'], landmarks_dict['left_elbow'], landmarks_dict['left_wrist']
            )
            angles['left_shoulder_angle'] = self.calculate_angle(
                landmarks_dict['left_elbow'], landmarks_dict['left_shoulder'], landmarks_dict['left_hip']
            )
        
        if all([landmarks_dict['right_shoulder'], landmarks_dict['right_elbow'], landmarks_dict['right_wrist']]):
            angles['right_elbow_angle'] = self.calculate_angle(
                landmarks_dict['right_shoulder'], landmarks_dict['right_elbow'], landmarks_dict['right_wrist']
            )
            angles['right_shoulder_angle'] = self.calculate_angle(
                landmarks_dict['right_elbow'], landmarks_dict['right_shoulder'], landmarks_dict['right_hip']
            )
        
        # Average angles for bilateral exercises
        if 'left_knee_angle' in angles and 'right_knee_angle' in angles:
            angles['knee_angle'] = (angles['left_knee_angle'] + angles['right_knee_angle']) / 2
        if 'left_hip_angle' in angles and 'right_hip_angle' in angles:
            angles['hip_angle'] = (angles['left_hip_angle'] + angles['right_hip_angle']) / 2
        if 'left_back_angle' in angles and 'right_back_angle' in angles:
            angles['back_angle'] = (angles['left_back_angle'] + angles['right_back_angle']) / 2
        if 'left_elbow_angle' in angles and 'right_elbow_angle' in angles:
            angles['elbow_angle'] = (angles['left_elbow_angle'] + angles['right_elbow_angle']) / 2
        if 'left_shoulder_angle' in angles and 'right_shoulder_angle' in angles:
            angles['shoulder_angle'] = (angles['left_shoulder_angle'] + angles['right_shoulder_angle']) / 2
        
        return angles
    
    def detect_exercise_advanced(self, landmarks) -> Dict[str, float]:
        """Advanced exercise detection using multiple indicators"""
        if not landmarks:
            return {"exercise": "unknown", "confidence": 0.0}
        
        angles = self.calculate_all_angles(landmarks)
        exercise_scores = {}
        
        # Score each exercise based on angle patterns
        for exercise, pattern in self.exercise_patterns.items():
            score = 0.0
            total_checks = 0
            
            # Check primary indicators
            if 'knee_bend' in pattern['primary_indicators']:
                if 'knee_angle' in angles and angles['knee_angle'] < 120:
                    score += 1.0
                total_checks += 1
            
            if 'hip_drop' in pattern['primary_indicators']:
                if 'hip_angle' in angles and angles['hip_angle'] < 90:
                    score += 1.0
                total_checks += 1
            
            if 'horizontal_position' in pattern['primary_indicators']:
                if 'shoulder_angle' in angles and angles['shoulder_angle'] > 160:
                    score += 1.0
                total_checks += 1
            
            if 'arm_bend' in pattern['primary_indicators']:
                if 'elbow_angle' in angles and angles['elbow_angle'] < 120:
                    score += 1.0
                total_checks += 1
            
            if 'static_position' in pattern['primary_indicators']:
                # Check if body is relatively straight and stable
                if 'back_angle' in angles and angles['back_angle'] > 160:
                    score += 1.0
                total_checks += 1
            
            # Calculate confidence score
            if total_checks > 0:
                exercise_scores[exercise] = score / total_checks
        
        # Find the exercise with highest confidence
        if exercise_scores:
            best_exercise = max(exercise_scores, key=exercise_scores.get)
            confidence = exercise_scores[best_exercise]
            
            # Only return if confidence is above threshold
            if confidence > 0.6:
                return {"exercise": best_exercise, "confidence": confidence}
        
        return {"exercise": "unknown", "confidence": 0.0}
    
    def check_form_generic(self, exercise: str, angles: Dict[str, float]) -> List[str]:
        """Generic form checking for any exercise"""
        feedback = []
        
        if exercise not in self.exercise_database:
            return ["Exercise not in database"]
        
        exercise_config = self.exercise_database[exercise]
        
        # Check each key angle
        for angle_name in exercise_config['key_angles']:
            if angle_name in angles:
                angle_value = angles[angle_name]
                thresholds = exercise_config['thresholds'][angle_name]
                
                if angle_value < thresholds['min']:
                    feedback.append(f"{angle_name.replace('_', ' ').title()} too small - increase range")
                elif angle_value > thresholds['max']:
                    feedback.append(f"{angle_name.replace('_', ' ').title()} too large - decrease range")
                else:
                    # Check if optimal
                    optimal_diff = abs(angle_value - thresholds['optimal'])
                    if optimal_diff > 10:
                        feedback.append(f"Adjust {angle_name.replace('_', ' ').title()} for optimal form")
        
        # Check alignment
        for alignment_check in exercise_config['alignment_checks']:
            if alignment_check == 'back_straight' and 'back_angle' in angles:
                if angles['back_angle'] < 160:
                    feedback.append("Keep your back straight")
            
            elif alignment_check == 'body_straight':
                if 'shoulder_angle' in angles and angles['shoulder_angle'] < 160:
                    feedback.append("Keep your body in a straight line")
            
            elif alignment_check == 'knee_alignment':
                # Check if knees are aligned with feet
                feedback.append("Ensure knees are aligned with your feet")
            
            elif alignment_check == 'elbow_fixed':
                feedback.append("Keep your elbows in a fixed position")
        
        return feedback
    
    def analyze_pose_enhanced(self, frame) -> Dict:
        """Enhanced pose analysis for any exercise"""
        start_time = time.time()
        
        # Convert BGR to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Process the frame
        results = self.pose.process(rgb_frame)
        
        if not results.pose_landmarks:
            return {
                "exercise": "unknown",
                "status": "no_pose_detected",
                "feedback": ["No pose detected - please ensure you are visible in the camera"],
                "processing_time": time.time() - start_time,
                "confidence": 0.0,
                "angles": {},
                "supported_exercises": list(self.exercise_database.keys())
            }
        
        # Advanced exercise detection
        detection_result = self.detect_exercise_advanced(results.pose_landmarks)
        exercise = detection_result["exercise"]
        confidence = detection_result["confidence"]
        
        # Calculate all angles
        angles = self.calculate_all_angles(results.pose_landmarks)
        
        # Check form
        if exercise != "unknown":
            feedback = self.check_form_generic(exercise, angles)
        else:
            feedback = ["Exercise not recognized. Try a different position or exercise."]
        
        # Determine status
        status = "correct" if len(feedback) == 0 else "incorrect"
        
        return {
            "exercise": exercise,
            "status": status,
            "feedback": feedback,
            "processing_time": time.time() - start_time,
            "confidence": confidence,
            "angles": angles,
            "supported_exercises": list(self.exercise_database.keys())
        }
    
    def get_exercise_instructions(self, exercise: str) -> Dict:
        """Get instructions for a specific exercise"""
        if exercise in self.exercise_database:
            config = self.exercise_database[exercise]
            return {
                "exercise": exercise,
                "key_angles": config['key_angles'],
                "thresholds": config['thresholds'],
                "alignment_checks": config['alignment_checks'],
                "movement_pattern": config['movement_pattern'],
                "primary_muscles": config['primary_muscles']
            }
        return {"error": "Exercise not found"}
    
    def get_all_exercises(self) -> List[str]:
        """Get list of all supported exercises"""
        return list(self.exercise_database.keys())
    
    def analyze_pose(self, frame) -> Dict:
        """Main pose analysis method (backward compatibility)"""
        return self.analyze_pose_enhanced(frame)
    
    def process_video_stream(self, video_source=0):
        """Process video stream for real-time pose analysis"""
        cap = cv2.VideoCapture(video_source)
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            
            # Analyze pose
            result = self.analyze_pose_enhanced(frame)
            
            # Draw pose landmarks
            if result["status"] != "no_pose_detected":
                self.mp_drawing.draw_landmarks(
                    frame, 
                    results.pose_landmarks, 
                    self.mp_pose.POSE_CONNECTIONS
                )
            
            # Display result on frame
            cv2.putText(frame, f"Exercise: {result['exercise']}", (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(frame, f"Confidence: {result['confidence']:.2f}", (10, 60), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(frame, f"Status: {result['status']}", (10, 90), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0) if result['status'] == 'correct' else (0, 0, 255), 2)
            
            # Display feedback
            for i, feedback in enumerate(result['feedback'][:3]):  # Show first 3 feedback items
                cv2.putText(frame, feedback, (10, 130 + i * 25), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
            
            cv2.imshow('Enhanced Pose Analysis', frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    # Test the enhanced pose estimation model
    model = PoseEstimationModel()
    print("Enhanced Pose Estimation Model initialized successfully!")
    print(f"Supported exercises: {model.get_all_exercises()}")
    print("Starting video stream... Press 'q' to quit.")
    model.process_video_stream()
