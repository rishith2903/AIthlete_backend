from flask import Flask, request, jsonify
from recommendation_model import HybridWorkoutRecommender, users, workouts, ratings
import os

app = Flask(__name__)

# Initialize the recommender
recommender = HybridWorkoutRecommender(users, workouts, ratings)
# Try loading pre-saved artifacts if available
recommender.load_artifacts(prefix='workout_recommender_v0.1.0_')

@app.route('/api/workout', methods=['POST'])
def get_recommendations():
    data = request.get_json()
    user_id = data.get('user_id')

    if not user_id:
        return jsonify({'error': 'User ID is required'}), 400

    try:
        user_id = int(user_id)
        if user_id not in recommender.users['user_id'].values:
            return jsonify({'error': 'User not found'}), 404
    # Ensure models are prepared (build vectorizer/matrix or train SVD if missing)
    recommender.prepare()

    recommendations = recommender.get_hybrid_recommendations(user_id)
    return jsonify(recommendations.to_dict(orient='records'))
    except ValueError:
        return jsonify({'error': 'Invalid User ID format'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)
