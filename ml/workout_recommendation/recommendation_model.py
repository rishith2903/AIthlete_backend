import os
import pickle
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import TruncatedSVD
import joblib

# Sample Data
users = pd.DataFrame({
    'user_id': [1, 2, 3, 4, 5],
    'age': [25, 30, 22, 35, 28],
    'fitness_goal': ['build muscle', 'lose weight', 'build muscle', 'improve endurance', 'lose weight']
})

workouts = pd.DataFrame({
    'workout_id': [101, 102, 103, 104, 105],
    'title': ['Push-up Challenge', 'HIIT Cardio', 'Full Body Strength', 'Long Distance Run', 'Yoga Flow'],
    'description': ['A 30-day push-up challenge to build upper body strength.',
                    'High-Intensity Interval Training for maximum calorie burn.',
                    'A comprehensive workout targeting all major muscle groups.',
                    'A 5km run to improve cardiovascular endurance.',
                    'A relaxing yoga sequence to improve flexibility and balance.'],
    'tags': ['bodyweight, upper body', 'cardio, weight loss', 'strength, full body', 'cardio, endurance', 'flexibility, balance']
})

ratings = pd.DataFrame({
    'user_id': [1, 1, 2, 3, 4, 5, 5],
    'workout_id': [101, 103, 102, 103, 104, 102, 105],
    'rating': [5, 4, 5, 3, 4, 4, 5]
})

class HybridWorkoutRecommender:
    def __init__(self, users, workouts, ratings):
        self.users = users
        self.workouts = workouts
        self.ratings = ratings
        self.tfidf_matrix = None
        self.tfidf_vectorizer = None
        self.svd = None
        # artifact directory inside Backend/ml/models
        self.artifact_dir = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', 'models'))
        os.makedirs(self.artifact_dir, exist_ok=True)
        # attempt to load pre-saved artifacts (if available)
        try:
            self.load_artifacts(prefix='workout_recommender_v0.1.0_')
        except Exception:
            # no artifacts yet, will prepare when needed
            pass

    def _prepare_models(self):
        # Content-Based Model
        self.workouts['combined_features'] = self.workouts['title'] + ' ' + self.workouts['description'] + ' ' + self.workouts['tags']
        tfidf = TfidfVectorizer(stop_words='english')
        self.tfidf_matrix = tfidf.fit_transform(self.workouts['combined_features'])
        self.tfidf_vectorizer = tfidf

        # Collaborative Filtering Model (matrix factorization via TruncatedSVD)
        pivot = self.ratings.pivot_table(index='user_id', columns='workout_id', values='rating')
        pivot = pivot.reindex(index=self.users['user_id'], columns=self.workouts['workout_id'])
        pivot_filled = pivot.fillna(0)
        matrix = pivot_filled.values
        if matrix.shape[1] > 1:
            n_comp = min(10, matrix.shape[1] - 1)
            self.svd = TruncatedSVD(n_components=n_comp)
            user_factors = self.svd.fit_transform(matrix)
            item_factors = self.svd.components_.T
            # store factors
            self.user_factors = user_factors
            self.item_factors = item_factors
        else:
            self.user_factors = None
            self.item_factors = None

    # Backwards-compatible prepare wrapper
    def prepare(self):
        if self.tfidf_vectorizer is None or self.tfidf_matrix is None or self.svd is None:
            self._prepare_models()

    def save_artifacts(self, prefix='workout_recommender_v'):
        # save TF-IDF vectorizer and SVD model
        tfidf_path = os.path.join(self.artifact_dir, prefix + 'tfidf.pkl')
        svd_path = os.path.join(self.artifact_dir, prefix + 'svd.pkl')
        joblib.dump(self.tfidf_vectorizer, tfidf_path)
        # save sklearn SVD and factors
        joblib.dump({'svd': self.svd, 'user_factors': getattr(self, 'user_factors', None), 'item_factors': getattr(self, 'item_factors', None)}, svd_path)
        return {'tfidf': tfidf_path, 'svd': svd_path}

    def load_artifacts(self, prefix='workout_recommender_v'):
        tfidf_path = os.path.join(self.artifact_dir, prefix + 'tfidf.pkl')
        svd_path = os.path.join(self.artifact_dir, prefix + 'svd.pkl')
        if os.path.exists(tfidf_path):
            self.tfidf_vectorizer = joblib.load(tfidf_path)
            # rebuild matrix
            self.tfidf_matrix = self.tfidf_vectorizer.transform(self.workouts['title'] + ' ' + self.workouts['description'] + ' ' + self.workouts['tags'])
        if os.path.exists(svd_path):
            obj = joblib.load(svd_path)
            self.svd = obj.get('svd')
            self.user_factors = obj.get('user_factors')
            self.item_factors = obj.get('item_factors')
        return {'tfidf': os.path.exists(tfidf_path), 'svd': os.path.exists(svd_path)}

    

    def get_content_based_recommendations(self, user_id, n=5):
        # ensure models prepared
        if self.tfidf_matrix is None:
            if self.tfidf_vectorizer is None:
                self.prepare()
            else:
                # rebuild matrix from vectorizer
                self.tfidf_matrix = self.tfidf_vectorizer.transform(self.workouts['combined_features'])
        user_profile = self.users.loc[self.users['user_id'] == user_id]
        if user_profile.empty:
            return pd.DataFrame()

        user_workouts = self.ratings[self.ratings['user_id'] == user_id]
        if not user_workouts.empty:
            last_workout_id = user_workouts.iloc[-1]['workout_id']
            workout_idx = self.workouts.index[self.workouts['workout_id'] == last_workout_id].tolist()[0]
            sim_scores = list(enumerate(cosine_similarity(self.tfidf_matrix[workout_idx], self.tfidf_matrix)[0]))
        else:
            # If user has no history, recommend based on fitness goal
            goal = user_profile['fitness_goal'].iloc[0]
            goal_workouts = self.workouts[self.workouts['tags'].str.contains(goal.split(' ')[-1], case=False)]
            if goal_workouts.empty:
                return self.workouts.head(n) # Fallback
            
            workout_idx = goal_workouts.index[0]
            sim_scores = list(enumerate(cosine_similarity(self.tfidf_matrix[workout_idx], self.tfidf_matrix)[0]))

        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:n+1]
        workout_indices = [i[0] for i in sim_scores]
        return self.workouts.iloc[workout_indices]

    def get_collaborative_filtering_recommendations(self, user_id, n=5):
        # ensure SVD trained
        try:
            _ = self.svd.predict(user_id, self.workouts['workout_id'].iloc[0])
        except Exception:
            self.prepare()

        workout_ids = list(self.workouts['workout_id'].unique())
        rated_workout_ids = self.ratings[self.ratings['user_id'] == user_id]['workout_id']
        unrated_workout_ids = [workout_id for workout_id in workout_ids if workout_id not in rated_workout_ids.values]

        # If we have factorization available, compute estimated scores via dot product
        preds = []
        if getattr(self, 'user_factors', None) is not None and getattr(self, 'item_factors', None) is not None:
            # map user_id to index in users DataFrame
            try:
                user_index = int(self.users.index[self.users['user_id'] == user_id].tolist()[0])
            except Exception:
                user_index = None

            for wid in unrated_workout_ids:
                try:
                    item_index = list(self.workouts['workout_id']).index(wid)
                except ValueError:
                    continue
                if user_index is not None:
                    user_vec = self.user_factors[user_index]
                    item_vec = self.item_factors[item_index]
                    score = float(np.dot(user_vec, item_vec))
                else:
                    score = 0.0
                preds.append((wid, score))
        else:
            # fallback: random score
            for wid in unrated_workout_ids:
                preds.append((wid, 0.0))

        preds.sort(key=lambda x: x[1], reverse=True)
        top_workout_ids = [p[0] for p in preds[:n]]
        return self.workouts[self.workouts['workout_id'].isin(top_workout_ids)]

    def get_hybrid_recommendations(self, user_id, n=5):
        content_recs = self.get_content_based_recommendations(user_id, n)
        collab_recs = self.get_collaborative_filtering_recommendations(user_id, n)

        hybrid_recs = pd.concat([content_recs, collab_recs]).drop_duplicates().head(n)
        return hybrid_recs

# Example Usage
recommender = HybridWorkoutRecommender(users, workouts, ratings)
user_id_to_recommend = 1
recommendations = recommender.get_hybrid_recommendations(user_id_to_recommend)
print(f"Recommendations for User {user_id_to_recommend}:")
print(recommendations)
