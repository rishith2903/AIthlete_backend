"""Training stub for Workout Recommendation Model
This file contains training orchestration and saving logic for the workout recommender.
In real use: replace sample data loading with dataset pipelines and training code.
"""
import json
from pathlib import Path
import os
import sys

# ensure package path
sys.path.append(os.path.dirname(__file__))
from workout_recommendation.recommendation_model import HybridWorkoutRecommender, users, workouts, ratings

MODELS_DIR = Path(__file__).parent / "models"
MODELS_DIR.mkdir(parents=True, exist_ok=True)

def train_and_save():
    # Instantiate and train the recommender
    recommender = HybridWorkoutRecommender(users, workouts, ratings)
    recommender.prepare()
    artifacts = recommender.save_artifacts(prefix='workout_recommender_v0.1.0_')

    # Save a simple manifest as well
    manifest = {
        "name": "workout_recommender",
        "version": "0.1.0",
        "artifacts": artifacts
    }
    out = MODELS_DIR / "workout_recommender_v0.1.0.json"
    with open(out, "w") as f:
        json.dump(manifest, f, indent=2)
    print(f"Saved manifest to {out}")

if __name__ == '__main__':
    train_and_save()
