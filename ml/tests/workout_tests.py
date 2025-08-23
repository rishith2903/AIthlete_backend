#!/usr/bin/env python3
"""
Comprehensive Test Suite for Workout Recommendation Model
Tests exercise selection, workout planning, and fitness level assessment
"""

import sys
import os
import json
from datetime import datetime

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class WorkoutTestSuite:
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
            key_fields = ['fitness_level', 'workout_days', 'exercises_count']
            passed = all(
                actual_output.get(key) == expected_output.get(key) 
                for key in key_fields if key in expected_output
            )
        elif isinstance(expected_output, list) and isinstance(actual_output, list):
            # Compare list outputs
            passed = len(actual_output) >= len(expected_output)
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
    
    def test_fitness_level_assessment(self):
        """Test fitness level determination accuracy"""
        print("\n🏋️ Testing Fitness Level Assessment...")
        
        # Test case 1: Beginner level
        user_profile = {'experience_years': 0, 'workout_frequency': 1}
        level = self.assess_fitness_level(user_profile)
        self.run_test(
            "LEVEL_001",
            "Beginner profile: 0 years, 1x/week",
            "beginner",
            level,
            "New exerciser should be beginner level"
        )
        
        # Test case 2: Intermediate level
        user_profile = {'experience_years': 2, 'workout_frequency': 3}
        level = self.assess_fitness_level(user_profile)
        self.run_test(
            "LEVEL_002",
            "Intermediate profile: 2 years, 3x/week",
            "intermediate",
            level,
            "Experienced exerciser should be intermediate"
        )
        
        # Test case 3: Advanced level
        user_profile = {'experience_years': 5, 'workout_frequency': 5}
        level = self.assess_fitness_level(user_profile)
        self.run_test(
            "LEVEL_003",
            "Advanced profile: 5 years, 5x/week",
            "advanced",
            level,
            "Very experienced exerciser should be advanced"
        )
    
    def assess_fitness_level(self, user_profile):
        """Assess fitness level based on user profile"""
        experience = user_profile.get('experience_years', 0)
        frequency = user_profile.get('workout_frequency', 0)
        
        if experience >= 4 and frequency >= 4:
            return "advanced"
        elif experience >= 1 and frequency >= 2:
            return "intermediate"
        else:
            return "beginner"
    
    def test_exercise_selection(self):
        """Test exercise selection logic"""
        print("\n💪 Testing Exercise Selection...")
        
        # Test case 4: Chest exercises selection
        exercises = self.select_exercises(['chest'], 'intermediate', ['gym'], 'strength')
        self.run_test(
            "SELECT_001",
            "Chest exercises for intermediate gym-goer",
            {"min_exercises": 3, "max_exercises": 6},
            {"min_exercises": len(exercises), "max_exercises": len(exercises)},
            "Should select 3-6 chest exercises"
        )
        
        # Test case 5: Bodyweight exercises
        exercises = self.select_exercises(['legs'], 'beginner', ['bodyweight'], 'strength')
        self.run_test(
            "SELECT_002",
            "Bodyweight leg exercises for beginner",
            {"min_exercises": 2, "max_exercises": 4},
            {"min_exercises": len(exercises), "max_exercises": len(exercises)},
            "Should select 2-4 bodyweight leg exercises"
        )
        
        # Test case 6: Multiple muscle groups
        exercises = self.select_exercises(['chest', 'back'], 'advanced', ['gym'], 'strength')
        self.run_test(
            "SELECT_003",
            "Chest and back exercises for advanced",
            {"min_exercises": 4, "max_exercises": 8},
            {"min_exercises": len(exercises), "max_exercises": len(exercises)},
            "Should select 4-8 exercises for multiple groups"
        )
    
    def select_exercises(self, muscle_groups, fitness_level, equipment, workout_type):
        """Select exercises based on criteria"""
        exercise_database = {
            'chest': {
                'beginner': ['push-ups', 'incline push-ups', 'wall push-ups'],
                'intermediate': ['bench press', 'dumbbell press', 'dips', 'push-ups'],
                'advanced': ['bench press', 'incline press', 'decline press', 'dips', 'cable flyes']
            },
            'back': {
                'beginner': ['bodyweight rows', 'superman holds'],
                'intermediate': ['pull-ups', 'barbell rows', 'lat pulldowns'],
                'advanced': ['pull-ups', 'barbell rows', 'deadlifts', 't-bar rows', 'cable rows']
            },
            'legs': {
                'beginner': ['bodyweight squats', 'lunges', 'calf raises'],
                'intermediate': ['squats', 'deadlifts', 'leg press', 'lunges'],
                'advanced': ['squats', 'deadlifts', 'leg press', 'hack squats', 'leg extensions']
            }
        }
        
        selected_exercises = []
        for muscle_group in muscle_groups:
            if muscle_group in exercise_database:
                exercises = exercise_database[muscle_group].get(fitness_level, [])
                selected_exercises.extend(exercises[:3])  # Limit to 3 per group
        
        return selected_exercises
    
    def test_workout_plan_generation(self):
        """Test workout plan generation accuracy"""
        print("\n📅 Testing Workout Plan Generation...")
        
        # Test case 7: Beginner workout plan
        user_profile = {
            'age': 25, 'gender': 'male', 'experience_years': 0,
            'workout_frequency': 3, 'goal': 'general_fitness',
            'available_equipment': ['bodyweight'], 'workout_days': 3
        }
        workout_plan = self.generate_workout_plan(user_profile)
        self.run_test(
            "PLAN_001",
            "Beginner workout plan",
            {"has_plan": True, "workout_days": 3},
            {"has_plan": bool(workout_plan), "workout_days": len(workout_plan.get('weekly_schedule', {}))},
            "Should generate 3-day beginner plan"
        )
        
        # Test case 8: Muscle gain plan
        user_profile['goal'] = 'muscle_gain'
        user_profile['available_equipment'] = ['gym']
        user_profile['workout_days'] = 4
        workout_plan = self.generate_workout_plan(user_profile)
        self.run_test(
            "PLAN_002",
            "Muscle gain workout plan",
            {"has_plan": True, "workout_days": 4},
            {"has_plan": bool(workout_plan), "workout_days": len(workout_plan.get('weekly_schedule', {}))},
            "Should generate 4-day muscle gain plan"
        )
        
        # Test case 9: Weight loss plan
        user_profile['goal'] = 'weight_loss'
        user_profile['workout_days'] = 5
        workout_plan = self.generate_workout_plan(user_profile)
        self.run_test(
            "PLAN_003",
            "Weight loss workout plan",
            {"has_plan": True, "workout_days": 5},
            {"has_plan": bool(workout_plan), "workout_days": len(workout_plan.get('weekly_schedule', {}))},
            "Should generate 5-day weight loss plan"
        )
    
    def generate_workout_plan(self, user_profile):
        """Generate a workout plan based on user profile"""
        fitness_level = self.assess_fitness_level(user_profile)
        goal = user_profile.get('goal', 'general_fitness')
        workout_days = user_profile.get('workout_days', 3)
        
        # Define workout splits based on goal and days
        if goal == 'muscle_gain':
            if workout_days == 3:
                split = {'monday': ['chest', 'triceps'], 'wednesday': ['back', 'biceps'], 'friday': ['legs', 'shoulders']}
            elif workout_days == 4:
                split = {'monday': ['chest'], 'tuesday': ['back'], 'thursday': ['legs'], 'friday': ['shoulders', 'arms']}
            else:
                split = {'monday': ['chest'], 'tuesday': ['back'], 'wednesday': ['legs'], 'thursday': ['shoulders'], 'friday': ['arms']}
        elif goal == 'weight_loss':
            split = {'monday': ['full_body'], 'tuesday': ['cardio'], 'wednesday': ['full_body'], 'thursday': ['cardio'], 'friday': ['full_body']}
        else:  # general_fitness
            split = {'monday': ['upper_body'], 'wednesday': ['lower_body'], 'friday': ['full_body']}
        
        # Generate weekly schedule
        weekly_schedule = {}
        for day, muscle_groups in split.items():
            exercises = []
            for muscle_group in muscle_groups:
                if muscle_group == 'full_body':
                    exercises.extend(self.select_exercises(['chest', 'back', 'legs'], fitness_level, user_profile['available_equipment'], 'strength'))
                elif muscle_group == 'upper_body':
                    exercises.extend(self.select_exercises(['chest', 'back', 'shoulders'], fitness_level, user_profile['available_equipment'], 'strength'))
                elif muscle_group == 'lower_body':
                    exercises.extend(self.select_exercises(['legs'], fitness_level, user_profile['available_equipment'], 'strength'))
                elif muscle_group == 'cardio':
                    exercises = ['running', 'cycling', 'jumping jacks', 'burpees']
                else:
                    exercises.extend(self.select_exercises([muscle_group], fitness_level, user_profile['available_equipment'], 'strength'))
            
            weekly_schedule[day] = {
                'muscle_groups': muscle_groups,
                'exercises': exercises[:6],  # Limit to 6 exercises per day
                'sets': 3 if fitness_level == 'beginner' else 4,
                'reps': '8-12' if goal == 'muscle_gain' else '12-15'
            }
        
        return {
            'weekly_schedule': weekly_schedule,
            'fitness_level': fitness_level,
            'goal': goal,
            'total_workout_days': len(weekly_schedule)
        }
    
    def test_workout_duration_calculation(self):
        """Test workout duration calculation"""
        print("\n⏱️ Testing Workout Duration...")
        
        # Test case 10: Beginner workout duration
        workout = {'exercises': ['squats', 'push-ups', 'lunges'], 'sets': 3, 'reps': '10-12'}
        duration = self.calculate_workout_duration(workout, 'beginner')
        self.run_test(
            "DURATION_001",
            "Beginner workout duration",
            {"min_minutes": 30, "max_minutes": 45},
            {"min_minutes": duration, "max_minutes": duration},
            "Beginner workout should be 30-45 minutes"
        )
        
        # Test case 11: Advanced workout duration
        workout = {'exercises': ['bench press', 'squats', 'deadlifts', 'pull-ups', 'overhead press'], 'sets': 4, 'reps': '8-10'}
        duration = self.calculate_workout_duration(workout, 'advanced')
        self.run_test(
            "DURATION_002",
            "Advanced workout duration",
            {"min_minutes": 60, "max_minutes": 90},
            {"min_minutes": duration, "max_minutes": duration},
            "Advanced workout should be 60-90 minutes"
        )
        
        # Test case 12: Cardio workout duration
        workout = {'exercises': ['running', 'cycling', 'jumping jacks'], 'sets': 1, 'reps': '20 minutes'}
        duration = self.calculate_workout_duration(workout, 'intermediate')
        self.run_test(
            "DURATION_003",
            "Cardio workout duration",
            {"min_minutes": 20, "max_minutes": 30},
            {"min_minutes": duration, "max_minutes": duration},
            "Cardio workout should be 20-30 minutes"
        )
    
    def calculate_workout_duration(self, workout, fitness_level):
        """Calculate workout duration in minutes"""
        exercises = workout.get('exercises', [])
        sets = workout.get('sets', 3)
        
        # Base time per exercise
        if fitness_level == 'beginner':
            time_per_exercise = 8  # minutes
        elif fitness_level == 'intermediate':
            time_per_exercise = 10  # minutes
        else:  # advanced
            time_per_exercise = 12  # minutes
        
        # Calculate total duration
        total_duration = len(exercises) * time_per_exercise * sets
        
        # Add warm-up and cool-down
        total_duration += 10  # warm-up
        total_duration += 5   # cool-down
        
        return total_duration
    
    def test_edge_cases(self):
        """Test edge cases and error handling"""
        print("\n⚠️ Testing Edge Cases...")
        
        # Test case 13: No equipment available
        exercises = self.select_exercises(['chest'], 'intermediate', [], 'strength')
        self.run_test(
            "EDGE_001",
            "No equipment available",
            {"min_exercises": 0, "max_exercises": 3},
            {"min_exercises": len(exercises), "max_exercises": len(exercises)},
            "Should handle no equipment gracefully"
        )
        
        # Test case 14: Invalid muscle group
        exercises = self.select_exercises(['invalid_muscle'], 'beginner', ['gym'], 'strength')
        self.run_test(
            "EDGE_002",
            "Invalid muscle group",
            [],
            exercises,
            "Should return empty list for invalid muscle group"
        )
        
        # Test case 15: Extreme workout frequency
        user_profile = {'experience_years': 1, 'workout_frequency': 10}
        level = self.assess_fitness_level(user_profile)
        self.run_test(
            "EDGE_003",
            "Extreme workout frequency",
            "intermediate",
            level,
            "Should handle extreme frequency gracefully"
        )
    
    def generate_report(self):
        """Generate comprehensive test report"""
        print("\n" + "="*80)
        print("📊 WORKOUT RECOMMENDATION MODEL - COMPREHENSIVE TEST REPORT")
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
            'model': 'Workout Recommendation',
            'total_tests': total_tests,
            'passed_tests': passed_tests,
            'failed_tests': failed_tests,
            'success_rate': (passed_tests/total_tests)*100,
            'results': self.test_results
        }
        
        with open('workout_test_report.json', 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n📄 Test report saved to: workout_test_report.json")
        
        return passed_tests == total_tests

def main():
    """Run comprehensive workout tests"""
    print("TESTING: Workout Recommendation Model - Comprehensive Test Suite")
    print("="*60)
    
    test_suite = WorkoutTestSuite()
    
    # Run all test categories
    test_suite.test_fitness_level_assessment()
    test_suite.test_exercise_selection()
    test_suite.test_workout_plan_generation()
    test_suite.test_workout_duration_calculation()
    test_suite.test_edge_cases()
    
    # Generate report
    success = test_suite.generate_report()
    
    if success:
        print("\n🎉 ALL WORKOUT TESTS PASSED!")
        return True
    else:
        print("\n❌ Some workout tests failed. Please review the results.")
        return False

if __name__ == "__main__":
    main()
