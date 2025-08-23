#!/usr/bin/env python3
"""
Comprehensive test script for all 4 AI Fitness Models
"""

import sys
import os
import json
import time
import numpy as np
from datetime import datetime

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import models
try:
    from pose_estimation.pose_model import PoseEstimationModel
    from nutrition.nutrition_model import NutritionModel
    from workout.workout_model import WorkoutModel
    from chatbot.chatbot_model import FitnessChatbot
    print("✅ All models imported successfully")
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)

def test_pose_estimation():
    """Test enhanced pose estimation model"""
    print("\n🧘 Testing Enhanced Pose Estimation Model...")
    
    try:
        # Initialize model
        pose_model = PoseEstimationModel()
        print("✅ Enhanced pose model initialized")
        
        # Test angle calculation
        a = (0, 0)
        b = (1, 0)
        c = (1, 1)
        angle = pose_model.calculate_angle(a, b, c)
        assert 80 < angle < 100, f"Angle calculation error: {angle}"
        print("✅ Angle calculation working")
        
        # Test exercise database
        exercises = pose_model.get_all_exercises()
        assert len(exercises) >= 10, f"Expected 10+ exercises, got {len(exercises)}"
        print(f"✅ Exercise database: {len(exercises)} exercises supported")
        
        # Test exercise instructions
        squat_instructions = pose_model.get_exercise_instructions('squat')
        assert 'key_angles' in squat_instructions, "Exercise instructions error"
        print("✅ Exercise instructions working")
        
        # Test advanced exercise detection
        detection_result = pose_model.detect_exercise_advanced(None)
        assert isinstance(detection_result, dict), "Exercise detection should return dict"
        print("✅ Advanced exercise detection working")
        
        # Test generic form checking
        angles = {'knee_angle': 90, 'hip_angle': 70, 'back_angle': 170}
        feedback = pose_model.check_form_generic('squat', angles)
        assert isinstance(feedback, list), "Generic form checking should return list"
        print("✅ Generic form checking working")
        
        print("✅ Enhanced Pose Estimation Model: PASSED")
        return True
        
    except Exception as e:
        print(f"❌ Enhanced Pose Estimation Model: FAILED - {e}")
        return False

def test_nutrition_model():
    """Test nutrition model"""
    print("\n🍽️ Testing Nutrition Model...")
    
    try:
        # Initialize model
        nutrition_model = NutritionModel()
        print("✅ Nutrition model initialized")
        
        # Test BMR calculation
        bmr = nutrition_model.calculate_bmr(25, 'male', 75, 180)
        assert 1500 < bmr < 2000, f"BMR calculation error: {bmr}"
        print("✅ BMR calculation working")
        
        # Test TDEE calculation
        tdee = nutrition_model.calculate_tdee(bmr, 'moderate')
        assert bmr < tdee < bmr * 2, f"TDEE calculation error: {tdee}"
        print("✅ TDEE calculation working")
        
        # Test macro calculation
        macros = nutrition_model.calculate_macros(2000, 'maintenance')
        assert 'calories' in macros and 'protein' in macros, "Macro calculation error"
        print("✅ Macro calculation working")
        
        # Test meal plan generation
        user_profile = {
            'age': 25,
            'gender': 'male',
            'weight': 75,
            'height': 180,
            'activity_level': 'moderate',
            'goal': 'weight_loss',
            'dietary_restrictions': []
        }
        
        meal_plan = nutrition_model.generate_meal_plan(user_profile)
        assert 'weekly_plan' in meal_plan, "Meal plan generation error"
        print("✅ Meal plan generation working")
        
        print("✅ Nutrition Model: PASSED")
        return True
        
    except Exception as e:
        print(f"❌ Nutrition Model: FAILED - {e}")
        return False

def test_workout_model():
    """Test workout model"""
    print("\n🏋️ Testing Workout Model...")
    
    try:
        # Initialize model
        workout_model = WorkoutModel()
        print("✅ Workout model initialized")
        
        # Test exercise database
        exercises = list(workout_model.exercises_database.keys())
        assert len(exercises) >= 10, f"Expected 10+ exercises, got {len(exercises)}"
        print(f"✅ Exercise database: {len(exercises)} exercises loaded")
        
        # Test fitness level determination
        user_profile = {
            'experience_years': 2,
            'workout_frequency': 3
        }
        level = workout_model.get_user_fitness_level(user_profile)
        assert level in ['beginner', 'intermediate', 'advanced'], f"Invalid fitness level: {level}"
        print("✅ Fitness level determination working")
        
        # Test workout plan generation
        user_profile = {
            'age': 25,
            'gender': 'male',
            'experience_years': 2,
            'workout_frequency': 4,
            'goal': 'muscle_gain',
            'available_equipment': ['minimal'],
            'workout_days': 4
        }
        
        workout_plan = workout_model.generate_weekly_workout_plan(user_profile)
        assert 'weekly_schedule' in workout_plan, "Workout plan generation error"
        print("✅ Workout plan generation working")
        
        # Test exercise selection
        exercises = workout_model.select_exercises_for_workout(
            ['chest', 'back'], 'intermediate', ['minimal'], 'strength'
        )
        assert len(exercises) > 0, "Exercise selection error"
        print("✅ Exercise selection working")
        
        print("✅ Workout Model: PASSED")
        return True
        
    except Exception as e:
        print(f"❌ Workout Model: FAILED - {e}")
        return False

def test_chatbot_model():
    """Test chatbot model"""
    print("\n🤖 Testing Fitness Chatbot...")
    
    try:
        # Initialize model
        chatbot = FitnessChatbot()
        print("✅ Chatbot initialized")
        
        # Test intent classification
        test_messages = [
            "How many sets should I do for squats?",
            "What's the nutrition info for chicken breast?",
            "I'm feeling tired and don't want to workout",
            "How do I track my progress for weight loss?"
        ]
        
        for message in test_messages:
            response = chatbot.process_message(message)
            assert 'response' in response, "Message processing error"
            assert 'intent' in response, "Intent classification error"
            print(f"✅ Intent classification: '{message[:30]}...' -> {response['intent']}")
        
        # Test entity extraction
        response = chatbot.process_message("How many sets for squats?")
        assert 'entities' in response, "Entity extraction error"
        print("✅ Entity extraction working")
        
        # Test response generation
        response = chatbot.process_message("I need motivation")
        assert len(response['response']) > 10, "Response generation error"
        print("✅ Response generation working")
        
        # Test conversation history
        summary = chatbot.get_conversation_summary()
        assert 'total_messages' in summary, "Conversation summary error"
        print("✅ Conversation history working")
        
        print("✅ Fitness Chatbot: PASSED")
        return True
        
    except Exception as e:
        print(f"❌ Fitness Chatbot: FAILED - {e}")
        return False

def test_api_integration():
    """Test API server integration"""
    print("\n🌐 Testing API Integration...")
    
    try:
        # Import API server components
        from api_server import app
        
        # Test health endpoint
        with app.test_client() as client:
            response = client.get('/health')
            assert response.status_code == 200, "Health endpoint error"
            data = json.loads(response.data)
            assert data['status'] == 'healthy', "Health status error"
            print("✅ Health endpoint working")
        
        print("✅ API Integration: PASSED")
        return True
        
    except Exception as e:
        print(f"❌ API Integration: FAILED - {e}")
        return False

def test_performance():
    """Test model performance"""
    print("\n⚡ Testing Performance...")
    
    try:
        # Test pose estimation speed
        pose_model = PoseEstimationModel()
        start_time = time.time()
        
        # Create dummy image data
        dummy_image = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
        result = pose_model.analyze_pose(dummy_image)
        
        processing_time = time.time() - start_time
        assert processing_time < 1.0, f"Pose processing too slow: {processing_time:.3f}s"
        print(f"✅ Pose processing time: {processing_time:.3f}s")
        
        # Test nutrition calculation speed
        nutrition_model = NutritionModel()
        start_time = time.time()
        
        user_profile = {
            'age': 25, 'gender': 'male', 'weight': 75, 'height': 180,
            'activity_level': 'moderate', 'goal': 'weight_loss'
        }
        meal_plan = nutrition_model.generate_meal_plan(user_profile)
        
        processing_time = time.time() - start_time
        assert processing_time < 5.0, f"Nutrition processing too slow: {processing_time:.3f}s"
        print(f"✅ Nutrition processing time: {processing_time:.3f}s")
        
        # Test workout generation speed
        workout_model = WorkoutModel()
        start_time = time.time()
        
        workout_plan = workout_model.generate_weekly_workout_plan(user_profile)
        
        processing_time = time.time() - start_time
        assert processing_time < 2.0, f"Workout processing too slow: {processing_time:.3f}s"
        print(f"✅ Workout processing time: {processing_time:.3f}s")
        
        # Test chatbot response speed
        chatbot = FitnessChatbot()
        start_time = time.time()
        
        response = chatbot.process_message("How many sets for squats?")
        
        processing_time = time.time() - start_time
        assert processing_time < 2.0, f"Chatbot processing too slow: {processing_time:.3f}s"
        print(f"✅ Chatbot processing time: {processing_time:.3f}s")
        
        print("✅ Performance Tests: PASSED")
        return True
        
    except Exception as e:
        print(f"❌ Performance Tests: FAILED - {e}")
        return False

def generate_test_report(results):
    """Generate test report"""
    print("\n" + "="*60)
    print("📊 TEST REPORT")
    print("="*60)
    
    total_tests = len(results)
    passed_tests = sum(results.values())
    failed_tests = total_tests - passed_tests
    
    print(f"Total Tests: {total_tests}")
    print(f"Passed: {passed_tests} ✅")
    print(f"Failed: {failed_tests} ❌")
    print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
    
    if failed_tests == 0:
        print("\n🎉 ALL TESTS PASSED! Models are ready for production.")
    else:
        print(f"\n⚠️ {failed_tests} test(s) failed. Please check the errors above.")
    
    # Save report
    report = {
        'timestamp': datetime.now().isoformat(),
        'total_tests': total_tests,
        'passed_tests': passed_tests,
        'failed_tests': failed_tests,
        'success_rate': (passed_tests/total_tests)*100,
        'results': results
    }
    
    with open('test_report.json', 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\n📄 Test report saved to: test_report.json")

def main():
    """Main test function"""
    print("🧪 AI Fitness Models - Comprehensive Test Suite")
    print("="*60)
    
    # Run all tests
    test_results = {
        'Pose Estimation': test_pose_estimation(),
        'Nutrition Model': test_nutrition_model(),
        'Workout Model': test_workout_model(),
        'Fitness Chatbot': test_chatbot_model(),
        'API Integration': test_api_integration(),
        'Performance': test_performance()
    }
    
    # Generate report
    generate_test_report(test_results)
    
    # Exit with appropriate code
    if all(test_results.values()):
        print("\n🚀 All models are working correctly!")
        sys.exit(0)
    else:
        print("\n❌ Some tests failed. Please fix the issues before deployment.")
        sys.exit(1)

if __name__ == "__main__":
    main()
