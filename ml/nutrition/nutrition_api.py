from flask import Flask, request, jsonify
from nutrition_model import NutritionModel

app = Flask(__name__)

# Initialize the nutrition model
try:
    nutrition_model = NutritionModel()
except Exception as e:
    # If the model fails to load, we'll handle it gracefully
    nutrition_model = None
    print(f"Failed to initialize NutritionModel: {e}")

@app.route('/api/nutrition', methods=['POST'])
def get_diet_plan():
    if not nutrition_model:
        return jsonify({'error': 'Nutrition model is not available'}), 503

    data = request.get_json()
    
    # Basic validation
    required_fields = ['age', 'weight', 'height', 'gender', 'activity_level', 'goal']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        # Assuming the model has a method to generate a full diet plan
        # This is a placeholder for the actual method call
        plan = nutrition_model.generate_diet_plan(
            age=data['age'],
            weight=data['weight'],
            height=data['height'],
            gender=data['gender'],
            activity_level=data['activity_level'],
            goal=data['goal'],
            dietary_restrictions=data.get('dietary_restrictions', [])
        )
        return jsonify(plan)
    except Exception as e:
        return jsonify({'error': f'Failed to generate diet plan: {e}'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5002)
