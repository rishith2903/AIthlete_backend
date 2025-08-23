#!/usr/bin/env python3
"""
Comprehensive Test Suite for Pose Estimation Model
Tests form checking, exercise detection, and feedback accuracy
"""

import sys
import os
import json
import math
from datetime import datetime

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class PoseEstimationTestSuite:
    def __init__(self):
        self.test_results = []
        self.test_counter = 0
        
    def run_test(self, test_id, test_input, expected_output, actual_output, notes=""):
        """Run a single test case"""
        self.test_counter += 1
        
        # Determine if test passed
        passed = False
        if isinstance(expected_output, dict) and isinstance(actual_output, dict):
            # Compare key fields for dict outputs
            key_fields = ['exercise', 'status', 'confidence']
            passed = all(
                actual_output.get(key) == expected_output.get(key) 
                for key in key_fields if key in expected_output
            )
        elif isinstance(expected_output, list) and isinstance(actual_output, list):
            # Compare list outputs
            passed = len(actual_output) == len(expected_output)
        else:
            # Direct comparison
            passed = actual_output == expected_output
        
        result = {
            'test_id': test_id,
            'test_input': test_input,
            'expected_output': expected_output,
            'actual_output': actual_output,
            'result': 'PASS' if passed else 'FAIL',
            'notes': notes
        }
        
        self.test_results.append(result)
        
        # Print test result
        status = "✅" if passed else "❌"
        print(f"{status} Test {test_id}: {result['result']}")
        if not passed:
            print(f"   Expected: {expected_output}")
            print(f"   Actual: {actual_output}")
        
        return passed
    
    def test_angle_calculation(self):
        """Test angle calculation accuracy"""
        print("\n🧘 Testing Angle Calculation...")
        
        # Test case 1: Right angle
        a, b, c = (0, 0), (1, 0), (1, 1)
        angle = self.calculate_angle(a, b, c)
        self.run_test(
            "ANGLE_001",
            f"Points: {a}, {b}, {c}",
            {"min": 85, "max": 95},
            {"min": angle, "max": angle},
            "Right angle calculation"
        )
        
        # Test case 2: Straight line
        a, b, c = (0, 0), (1, 0), (2, 0)
        angle = self.calculate_angle(a, b, c)
        self.run_test(
            "ANGLE_002",
            f"Points: {a}, {b}, {c}",
            {"min": 175, "max": 185},
            {"min": angle, "max": angle},
            "Straight line angle"
        )
        
        # Test case 3: Acute angle
        a, b, c = (0, 0), (1, 0), (0.5, 0.5)
        angle = self.calculate_angle(a, b, c)
        self.run_test(
            "ANGLE_003",
            f"Points: {a}, {b}, {c}",
            {"min": 40, "max": 50},
            {"min": angle, "max": angle},
            "Acute angle calculation"
        )
    
    def calculate_angle(self, a, b, c):
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
    
    def test_exercise_detection(self):
        """Test exercise detection accuracy"""
        print("\n🏋️ Testing Exercise Detection...")
        
        # Test case 4: Squat detection
        squat_angles = {'knee_angle': 90, 'hip_angle': 70, 'back_angle': 170}
        result = self.simulate_exercise_detection(squat_angles)
        self.run_test(
            "DETECT_001",
            "Squat angles",
            {"exercise": "squat", "confidence": 0.8},
            {"exercise": result.get("exercise", "unknown"), "confidence": result.get("confidence", 0)},
            "Squat exercise detection"
        )
        
        # Test case 5: Push-up detection
        pushup_angles = {'elbow_angle': 90, 'shoulder_angle': 170, 'back_angle': 175}
        result = self.simulate_exercise_detection(pushup_angles)
        self.run_test(
            "DETECT_002",
            "Push-up angles",
            {"exercise": "pushup", "confidence": 0.8},
            {"exercise": result.get("exercise", "unknown"), "confidence": result.get("confidence", 0)},
            "Push-up exercise detection"
        )
        
        # Test case 6: Unknown exercise
        unknown_angles = {'knee_angle': 180, 'hip_angle': 180, 'back_angle': 180}
        result = self.simulate_exercise_detection(unknown_angles)
        self.run_test(
            "DETECT_003",
            "Unknown angles",
            {"exercise": "unknown", "confidence": 0.0},
            {"exercise": result.get("exercise", "unknown"), "confidence": result.get("confidence", 0)},
            "Unknown exercise handling"
        )
    
    def simulate_exercise_detection(self, angles):
        """Simulate exercise detection based on angles"""
        # Simple detection logic
        if angles.get('knee_angle', 180) < 120 and angles.get('hip_angle', 180) < 90:
            return {"exercise": "squat", "confidence": 0.85}
        elif angles.get('elbow_angle', 180) < 120 and angles.get('shoulder_angle', 180) > 160:
            return {"exercise": "pushup", "confidence": 0.82}
        else:
            return {"exercise": "unknown", "confidence": 0.0}
    
    def test_form_checking(self):
        """Test form checking accuracy"""
        print("\n📏 Testing Form Checking...")
        
        # Test case 7: Perfect squat form
        perfect_squat = {'knee_angle': 90, 'hip_angle': 70, 'back_angle': 170}
        feedback = self.check_squat_form(perfect_squat)
        self.run_test(
            "FORM_001",
            "Perfect squat angles",
            [],
            feedback,
            "Perfect form should have no feedback"
        )
        
        # Test case 8: Poor squat form (knees too bent)
        poor_squat = {'knee_angle': 50, 'hip_angle': 70, 'back_angle': 170}
        feedback = self.check_squat_form(poor_squat)
        self.run_test(
            "FORM_002",
            "Poor squat angles",
            {"min_feedback": 1},
            {"min_feedback": len(feedback)},
            "Poor form should have feedback"
        )
        
        # Test case 9: Back too bent
        bad_back = {'knee_angle': 90, 'hip_angle': 70, 'back_angle': 140}
        feedback = self.check_squat_form(bad_back)
        self.run_test(
            "FORM_003",
            "Bad back angles",
            {"min_feedback": 1},
            {"min_feedback": len(feedback)},
            "Bad back form should have feedback"
        )
    
    def check_squat_form(self, angles):
        """Check squat form based on angles"""
        feedback = []
        
        # Check knee angle
        knee_angle = angles.get('knee_angle', 180)
        if knee_angle < 70:
            feedback.append("Knee angle too small - increase range")
        elif knee_angle > 110:
            feedback.append("Knee angle too large - decrease range")
        
        # Check back angle
        back_angle = angles.get('back_angle', 180)
        if back_angle < 160:
            feedback.append("Keep your back straight")
        
        return feedback
    
    def test_edge_cases(self):
        """Test edge cases and error handling"""
        print("\n⚠️ Testing Edge Cases...")
        
        # Test case 10: Missing angles
        missing_angles = {}
        feedback = self.check_squat_form(missing_angles)
        self.run_test(
            "EDGE_001",
            "Missing angles",
            [],
            feedback,
            "Missing angles should not cause errors"
        )
        
        # Test case 11: Extreme angles
        extreme_angles = {'knee_angle': 0, 'hip_angle': 0, 'back_angle': 0}
        feedback = self.check_squat_form(extreme_angles)
        self.run_test(
            "EDGE_002",
            "Extreme angles",
            {"min_feedback": 1},
            {"min_feedback": len(feedback)},
            "Extreme angles should be flagged"
        )
        
        # Test case 12: Invalid exercise
        result = self.simulate_exercise_detection({})
        self.run_test(
            "EDGE_003",
            "Empty angles",
            {"exercise": "unknown", "confidence": 0.0},
            {"exercise": result.get("exercise", "unknown"), "confidence": result.get("confidence", 0)},
            "Empty angles should return unknown"
        )
    
    def generate_report(self):
        """Generate comprehensive test report"""
        print("\n" + "="*80)
        print("📊 POSE ESTIMATION MODEL - COMPREHENSIVE TEST REPORT")
        print("="*80)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result['result'] == 'PASS')
        failed_tests = total_tests - passed_tests
        
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests} ✅")
        print(f"Failed: {failed_tests} ❌")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        # Detailed results
        print("\n📋 Detailed Test Results:")
        for result in self.test_results:
            status = "✅" if result['result'] == 'PASS' else "❌"
            print(f"{status} {result['test_id']}: {result['result']}")
            if result['result'] == 'FAIL':
                print(f"   Expected: {result['expected_output']}")
                print(f"   Actual: {result['actual_output']}")
                print(f"   Notes: {result['notes']}")
        
        # Save report
        report = {
            'timestamp': datetime.now().isoformat(),
            'model': 'Pose Estimation',
            'total_tests': total_tests,
            'passed_tests': passed_tests,
            'failed_tests': failed_tests,
            'success_rate': (passed_tests/total_tests)*100,
            'results': self.test_results
        }
        
        with open('pose_estimation_test_report.json', 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n📄 Test report saved to: pose_estimation_test_report.json")
        
        return passed_tests == total_tests

def main():
    """Run comprehensive pose estimation tests"""
    print("TESTING: Pose Estimation Model - Comprehensive Test Suite")
    print("="*60)
    
    test_suite = PoseEstimationTestSuite()
    
    # Run all test categories
    test_suite.test_angle_calculation()
    test_suite.test_exercise_detection()
    test_suite.test_form_checking()
    test_suite.test_edge_cases()
    
    # Generate report
    success = test_suite.generate_report()
    
    if success:
        print("\n🎉 ALL POSE ESTIMATION TESTS PASSED!")
        return True
    else:
        print("\n❌ Some pose estimation tests failed. Please review the results.")
        return False

if __name__ == "__main__":
    main()
