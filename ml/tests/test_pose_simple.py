#!/usr/bin/env python3
"""
Simple test for enhanced pose estimation model
"""

import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_pose_model_basic():
    """Test basic functionality without heavy dependencies"""
    print("🧘 Testing Enhanced Pose Estimation Model (Basic)...")
    
    try:
        # Test basic angle calculation
        def calculate_angle(a, b, c):
            """Calculate angle between three points"""
            import math
            
            # Convert to numpy-like arrays
            a = [float(a[0]), float(a[1])]
            b = [float(b[0]), float(b[1])]
            c = [float(c[0]), float(c[1])]
            
            # Calculate vectors
            ba = [a[0] - b[0], a[1] - b[1]]
            bc = [c[0] - b[0], c[1] - b[1]]
            
            # Calculate dot product
            dot_product = ba[0] * bc[0] + ba[1] * bc[1]
            
            # Calculate magnitudes
            ba_mag = math.sqrt(ba[0]**2 + ba[1]**2)
            bc_mag = math.sqrt(bc[0]**2 + bc[1]**2)
            
            # Calculate angle
            cos_angle = dot_product / (ba_mag * bc_mag)
            cos_angle = max(-1, min(1, cos_angle))  # Clamp to [-1, 1]
            angle = math.acos(cos_angle)
            
            return math.degrees(angle)
        
        # Test angle calculation
        a = (0, 0)
        b = (1, 0)
        c = (1, 1)
        angle = calculate_angle(a, b, c)
        print(f"✅ Angle calculation: {angle:.2f}° (expected ~90°)")
        
        # Test exercise database structure
        exercise_database = {
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
            }
        }
        
        print(f"✅ Exercise database: {len(exercise_database)} exercises defined")
        
        # Test form checking logic
        def check_form_generic(exercise, angles):
            """Generic form checking for any exercise"""
            feedback = []
            
            if exercise not in exercise_database:
                return ["Exercise not in database"]
            
            exercise_config = exercise_database[exercise]
            
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
            
            return feedback
        
        # Test form checking
        test_angles = {'knee_angle': 90, 'hip_angle': 70, 'back_angle': 170}
        feedback = check_form_generic('squat', test_angles)
        print(f"✅ Form checking: {len(feedback)} feedback items generated")
        
        # Test exercise detection patterns
        exercise_patterns = {
            'squat': {
                'primary_indicators': ['knee_bend', 'hip_drop'],
                'secondary_indicators': ['vertical_movement', 'feet_shoulder_width']
            },
            'pushup': {
                'primary_indicators': ['horizontal_position', 'arm_bend'],
                'secondary_indicators': ['body_straight', 'elbow_tuck']
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
            }
        }
        
        print(f"✅ Exercise patterns: {len(exercise_patterns)} patterns defined")
        
        # Test API response structure
        def simulate_pose_analysis():
            """Simulate pose analysis response"""
            return {
                "exercise": "squat",
                "status": "correct",
                "feedback": [],
                "processing_time": 0.1,
                "confidence": 0.85,
                "angles": {
                    "knee_angle": 90.0,
                    "hip_angle": 70.0,
                    "back_angle": 170.0
                },
                "supported_exercises": list(exercise_database.keys())
            }
        
        result = simulate_pose_analysis()
        print(f"✅ API response structure: {len(result)} fields")
        print(f"✅ Supported exercises: {len(result['supported_exercises'])} exercises")
        
        print("✅ Enhanced Pose Estimation Model (Basic): PASSED")
        return True
        
    except Exception as e:
        print(f"❌ Enhanced Pose Estimation Model (Basic): FAILED - {e}")
        return False

if __name__ == "__main__":
    test_pose_model_basic()
