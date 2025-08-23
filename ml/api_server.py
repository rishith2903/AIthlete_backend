from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import base64
import cv2
import numpy as np
from datetime import datetime
import traceback

# Import our models
from pose_estimation.pose_model import PoseEstimationModel
from nutrition.nutrition_model import NutritionModel
from workout.workout_model import WorkoutModel
from chatbot.chatbot_model import FitnessChatbot

app = Flask(__name__)
CORS(app)

# Initialize models
pose_model = PoseEstimationModel()
nutrition_model = NutritionModel()
workout_model = WorkoutModel()
chatbot_model = FitnessChatbot()

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'models_loaded': {
            'pose_estimation': True,
            'nutrition': True,
            'workout': True,
            'chatbot': True
        }
    })

# Pose Estimation Endpoints
@app.route('/api/pose/analyze', methods=['POST'])
def analyze_pose():
    """Analyze pose from image or video frame"""
    try:
        data = request.get_json()
        
        if not data or 'image' not in data:
            return jsonify({'error': 'No image data provided'}), 400
        
        # Decode base64 image
        image_data = base64.b64decode(data['image'].split(',')[1])
        nparr = np.frombuffer(image_data, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if frame is None:
            return jsonify({'error': 'Invalid image data'}), 400
        
        # Analyze pose
        result = pose_model.analyze_pose(frame)
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({
            'error': 'Pose analysis failed',
            'details': str(e),
            'traceback': traceback.format_exc()
        }), 500

@app.route('/api/pose/exercises', methods=['GET'])
def get_supported_exercises():
    """Get list of supported exercises"""
    exercises = pose_model.get_all_exercises()
    return jsonify({
        'supported_exercises': exercises,
        'total_exercises': len(exercises)
    })

@app.route('/api/pose/exercise/<exercise_name>', methods=['GET'])
def get_exercise_instructions(exercise_name):
    """Get detailed instructions for a specific exercise"""
    try:
        instructions = pose_model.get_exercise_instructions(exercise_name)
        return jsonify(instructions)
    except Exception as e:
        return jsonify({
            'error': 'Failed to get exercise instructions',
            'details': str(e)
        }), 500

@app.route('/api/pose/analyze-enhanced', methods=['POST'])
def analyze_pose_enhanced():
    """Enhanced pose analysis with detailed feedback"""
    try:
        data = request.get_json()
        
        if not data or 'image' not in data:
            return jsonify({'error': 'No image data provided'}), 400
        
        # Decode base64 image
        image_data = base64.b64decode(data['image'].split(',')[1])
        nparr = np.frombuffer(image_data, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if frame is None:
            return jsonify({'error': 'Invalid image data'}), 400
        
        # Analyze pose with enhanced method
        result = pose_model.analyze_pose_enhanced(frame)
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({
            'error': 'Enhanced pose analysis failed',
            'details': str(e),
            'traceback': traceback.format_exc()
        }), 500

# Nutrition Endpoints
@app.route('/api/nutrition/meal-plan', methods=['POST'])
def generate_meal_plan():
    """Generate personalized meal plan"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No user profile provided'}), 400
        
        # Generate meal plan
        meal_plan = nutrition_model.generate_meal_plan(data)
        
        return jsonify(meal_plan)
    
    except Exception as e:
        return jsonify({
            'error': 'Meal plan generation failed',
            'details': str(e),
            'traceback': traceback.format_exc()
        }), 500

@app.route('/api/nutrition/food-info', methods=['GET'])
def get_food_info():
    """Get nutrition information for a specific food"""
    try:
        food_name = request.args.get('food')
        
        if not food_name:
            return jsonify({'error': 'Food name not provided'}), 400
        
        food_info = nutrition_model.get_nutrition_info(food_name)
        
        return jsonify(food_info)
    
    except Exception as e:
        return jsonify({
            'error': 'Food info retrieval failed',
            'details': str(e)
        }), 500

@app.route('/api/nutrition/calculate-needs', methods=['POST'])
def calculate_nutritional_needs():
    """Calculate nutritional needs based on user profile"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No user profile provided'}), 400
        
        # Extract user information
        age = data.get('age', 30)
        gender = data.get('gender', 'male')
        weight = data.get('weight', 70)
        height = data.get('height', 170)
        activity_level = data.get('activity_level', 'moderate')
        goal = data.get('goal', 'maintenance')
        
        # Calculate needs
        bmr = nutrition_model.calculate_bmr(age, gender, weight, height)
        tdee = nutrition_model.calculate_tdee(bmr, activity_level)
        target_calories = nutrition_model.adjust_calories_for_goal(tdee, goal)
        target_macros = nutrition_model.calculate_macros(target_calories, goal)
        
        return jsonify({
            'user_profile': data,
            'bmr': round(bmr, 0),
            'tdee': round(tdee, 0),
            'target_calories': round(target_calories, 0),
            'target_macros': target_macros
        })
    
    except Exception as e:
        return jsonify({
            'error': 'Nutrition calculation failed',
            'details': str(e)
        }), 500

# Workout Endpoints
@app.route('/api/workout/plan', methods=['POST'])
def generate_workout_plan():
    """Generate personalized workout plan"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No user profile provided'}), 400
        
        # Generate workout plan
        workout_plan = workout_model.generate_weekly_workout_plan(data)
        
        return jsonify(workout_plan)
    
    except Exception as e:
        return jsonify({
            'error': 'Workout plan generation failed',
            'details': str(e),
            'traceback': traceback.format_exc()
        }), 500

@app.route('/api/workout/exercises', methods=['GET'])
def get_exercises():
    """Get list of available exercises"""
    exercises = list(workout_model.exercises_database.keys())
    exercise_details = {}
    
    for exercise in exercises:
        exercise_details[exercise] = {
            'name': workout_model.exercises_database[exercise]['name'],
            'muscle_group': workout_model.exercises_database[exercise]['muscle_group'],
            'difficulty': workout_model.exercises_database[exercise]['difficulty'],
            'equipment': workout_model.exercises_database[exercise]['equipment']
        }
    
    return jsonify({
        'exercises': exercise_details,
        'total_exercises': len(exercises)
    })

@app.route('/api/workout/exercise/<exercise_name>', methods=['GET'])
def get_exercise_details(exercise_name):
    """Get detailed information about a specific exercise"""
    try:
        exercise_info = workout_model.get_exercise_details(exercise_name)
        
        if 'error' in exercise_info:
            return jsonify(exercise_info), 404
        
        return jsonify(exercise_info)
    
    except Exception as e:
        return jsonify({
            'error': 'Exercise details retrieval failed',
            'details': str(e)
        }), 500

# Chatbot Endpoints
@app.route('/api/chatbot/message', methods=['POST'])
def process_chat_message():
    """Process chatbot message and return response"""
    try:
        data = request.get_json()
        
        if not data or 'message' not in data:
            return jsonify({'error': 'No message provided'}), 400
        
        message = data['message']
        user_context = data.get('context', {})
        
        # Process message
        response = chatbot_model.process_message(message, user_context)
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({
            'error': 'Message processing failed',
            'details': str(e),
            'traceback': traceback.format_exc()
        }), 500

@app.route('/api/chatbot/suggestions', methods=['GET'])
def get_chat_suggestions():
    """Get conversation suggestions"""
    try:
        intent = request.args.get('intent', 'general')
        entities = request.args.get('entities', '{}')
        
        if entities:
            entities = json.loads(entities)
        
        suggestions = chatbot_model.get_follow_up_suggestions(intent, entities)
        
        return jsonify({
            'suggestions': suggestions,
            'intent': intent
        })
    
    except Exception as e:
        return jsonify({
            'error': 'Suggestions retrieval failed',
            'details': str(e)
        }), 500

@app.route('/api/chatbot/conversation-summary', methods=['GET'])
def get_conversation_summary():
    """Get conversation history summary"""
    try:
        summary = chatbot_model.get_conversation_summary()
        return jsonify(summary)
    
    except Exception as e:
        return jsonify({
            'error': 'Conversation summary retrieval failed',
            'details': str(e)
        }), 500

# Combined Endpoints
@app.route('/api/fitness/complete-plan', methods=['POST'])
def generate_complete_fitness_plan():
    """Generate complete fitness plan (workout + nutrition)"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No user profile provided'}), 400
        
        # Generate workout plan
        workout_plan = workout_model.generate_weekly_workout_plan(data)
        
        # Generate meal plan
        meal_plan = nutrition_model.generate_meal_plan(data)
        
        # Combine plans
        complete_plan = {
            'user_profile': data,
            'workout_plan': workout_plan,
            'nutrition_plan': meal_plan,
            'generated_at': datetime.now().isoformat(),
            'recommendations': {
                'workout_frequency': workout_plan.get('weekly_schedule', {}),
                'nutrition_targets': meal_plan.get('nutritional_targets', {}),
                'tips': [
                    "Start with lighter weights and focus on form",
                    "Stay hydrated throughout your workouts",
                    "Get adequate sleep for recovery",
                    "Track your progress consistently"
                ]
            }
        }
        
        return jsonify(complete_plan)
    
    except Exception as e:
        return jsonify({
            'error': 'Complete plan generation failed',
            'details': str(e),
            'traceback': traceback.format_exc()
        }), 500

@app.route('/api/fitness/quick-advice', methods=['POST'])
def get_quick_advice():
    """Get quick fitness advice based on user query"""
    try:
        data = request.get_json()
        
        if not data or 'query' not in data:
            return jsonify({'error': 'No query provided'}), 400
        
        query = data['query']
        
        # Process with chatbot
        response = chatbot_model.process_message(query)
        
        # Add additional context based on query type
        advice = {
            'query': query,
            'response': response['response'],
            'intent': response['intent'],
            'additional_tips': []
        }
        
        # Add relevant tips based on intent
        if response['intent'] == 'workout_question':
            advice['additional_tips'] = [
                "Always warm up before exercising",
                "Focus on proper form over heavy weights",
                "Progressive overload is key to building strength"
            ]
        elif response['intent'] == 'nutrition_question':
            advice['additional_tips'] = [
                "Eat a balanced diet with lean protein",
                "Stay hydrated throughout the day",
                "Time your meals around workouts"
            ]
        elif response['intent'] == 'motivation':
            advice['additional_tips'] = [
                "Set specific, achievable goals",
                "Track your progress regularly",
                "Find a workout buddy for accountability"
            ]
        
        return jsonify(advice)
    
    except Exception as e:
        return jsonify({
            'error': 'Quick advice generation failed',
            'details': str(e)
        }), 500

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    print("Starting AI Fitness API Server...")
    print("Available endpoints:")
    print("  - GET  /health")
    print("  - POST /api/pose/analyze")
    print("  - GET  /api/pose/exercises")
    print("  - POST /api/nutrition/meal-plan")
    print("  - GET  /api/nutrition/food-info")
    print("  - POST /api/nutrition/calculate-needs")
    print("  - POST /api/workout/plan")
    print("  - GET  /api/workout/exercises")
    print("  - GET  /api/workout/exercise/<name>")
    print("  - POST /api/chatbot/message")
    print("  - GET  /api/chatbot/suggestions")
    print("  - GET  /api/chatbot/conversation-summary")
    print("  - POST /api/fitness/complete-plan")
    print("  - POST /api/fitness/quick-advice")
    
    app.run(host='0.0.0.0', port=5000, debug=True)
