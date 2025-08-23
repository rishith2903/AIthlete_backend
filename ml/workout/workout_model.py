import pandas as pd
import numpy as np
import json
import random
from typing import Dict, List, Tuple, Optional
from datetime import datetime, timedelta
import math

class WorkoutModel:
    def __init__(self):
        """Initialize the workout recommendation model"""
        self.exercises_database = self.load_exercises_database()
        
        # Exercise categories and muscle groups
        self.muscle_groups = {
            'chest': ['bench_press', 'push_ups', 'dumbbell_flyes', 'incline_press'],
            'back': ['pull_ups', 'rows', 'deadlifts', 'lat_pulldowns'],
            'legs': ['squats', 'lunges', 'deadlifts', 'leg_press', 'calf_raises'],
            'shoulders': ['overhead_press', 'lateral_raises', 'front_raises', 'rear_delt_flyes'],
            'arms': ['bicep_curls', 'tricep_dips', 'hammer_curls', 'skull_crushers'],
            'core': ['planks', 'crunches', 'russian_twists', 'leg_raises'],
            'cardio': ['running', 'cycling', 'jumping_jacks', 'burpees']
        }
        
        # Exercise difficulty levels
        self.difficulty_levels = {
            'beginner': 1,
            'intermediate': 2,
            'advanced': 3
        }
        
        # Equipment availability
        self.equipment_types = {
            'none': ['push_ups', 'squats', 'lunges', 'planks', 'burpees', 'jumping_jacks'],
            'minimal': ['dumbbells', 'resistance_bands', 'pull_up_bar'],
            'gym': ['barbells', 'machines', 'cable_equipment', 'treadmill', 'elliptical']
        }
        
        # Workout frequency recommendations
        self.frequency_recommendations = {
            'beginner': {'strength': 2, 'cardio': 2, 'rest': 3},
            'intermediate': {'strength': 3, 'cardio': 3, 'rest': 1},
            'advanced': {'strength': 4, 'cardio': 4, 'rest': 0}
        }
        
        # Rest periods (in seconds)
        self.rest_periods = {
            'strength': {'beginner': 90, 'intermediate': 60, 'advanced': 45},
            'cardio': {'beginner': 30, 'intermediate': 20, 'advanced': 10},
            'hiit': {'beginner': 60, 'intermediate': 45, 'advanced': 30}
        }
    
    def load_exercises_database(self) -> Dict:
        """Load or create exercises database"""
        exercises = {
            'bench_press': {
                'name': 'Bench Press',
                'muscle_group': 'chest',
                'difficulty': 'intermediate',
                'equipment': 'gym',
                'instructions': 'Lie on bench, lower bar to chest, press up',
                'sets_range': (3, 5),
                'reps_range': (8, 12),
                'rest_time': 90
            },
            'squats': {
                'name': 'Squats',
                'muscle_group': 'legs',
                'difficulty': 'beginner',
                'equipment': 'none',
                'instructions': 'Stand with feet shoulder-width, lower hips back and down',
                'sets_range': (3, 4),
                'reps_range': (10, 15),
                'rest_time': 60
            },
            'push_ups': {
                'name': 'Push-ups',
                'muscle_group': 'chest',
                'difficulty': 'beginner',
                'equipment': 'none',
                'instructions': 'Plank position, lower body to ground, push up',
                'sets_range': (2, 4),
                'reps_range': (8, 20),
                'rest_time': 60
            },
            'pull_ups': {
                'name': 'Pull-ups',
                'muscle_group': 'back',
                'difficulty': 'intermediate',
                'equipment': 'minimal',
                'instructions': 'Hang from bar, pull body up until chin over bar',
                'sets_range': (2, 4),
                'reps_range': (5, 12),
                'rest_time': 90
            },
            'deadlifts': {
                'name': 'Deadlifts',
                'muscle_group': 'back',
                'difficulty': 'advanced',
                'equipment': 'gym',
                'instructions': 'Stand with feet hip-width, bend at hips and knees, lift bar',
                'sets_range': (3, 5),
                'reps_range': (5, 10),
                'rest_time': 120
            },
            'lunges': {
                'name': 'Lunges',
                'muscle_group': 'legs',
                'difficulty': 'beginner',
                'equipment': 'none',
                'instructions': 'Step forward, lower back knee toward ground',
                'sets_range': (2, 3),
                'reps_range': (10, 15),
                'rest_time': 45
            },
            'planks': {
                'name': 'Planks',
                'muscle_group': 'core',
                'difficulty': 'beginner',
                'equipment': 'none',
                'instructions': 'Hold body in straight line from head to heels',
                'sets_range': (2, 3),
                'reps_range': (1, 1),  # Duration-based
                'duration': 30,  # seconds
                'rest_time': 30
            },
            'bicep_curls': {
                'name': 'Bicep Curls',
                'muscle_group': 'arms',
                'difficulty': 'beginner',
                'equipment': 'minimal',
                'instructions': 'Hold dumbbells, curl up toward shoulders',
                'sets_range': (2, 3),
                'reps_range': (10, 15),
                'rest_time': 60
            },
            'overhead_press': {
                'name': 'Overhead Press',
                'muscle_group': 'shoulders',
                'difficulty': 'intermediate',
                'equipment': 'minimal',
                'instructions': 'Press weight overhead while keeping core tight',
                'sets_range': (3, 4),
                'reps_range': (8, 12),
                'rest_time': 75
            },
            'running': {
                'name': 'Running',
                'muscle_group': 'cardio',
                'difficulty': 'beginner',
                'equipment': 'none',
                'instructions': 'Jog at moderate pace',
                'sets_range': (1, 1),
                'reps_range': (1, 1),  # Duration-based
                'duration': 1800,  # 30 minutes
                'rest_time': 0
            },
            'burpees': {
                'name': 'Burpees',
                'muscle_group': 'cardio',
                'difficulty': 'intermediate',
                'equipment': 'none',
                'instructions': 'Squat, jump back to plank, jump forward, jump up',
                'sets_range': (2, 4),
                'reps_range': (8, 15),
                'rest_time': 45
            }
        }
        
        return exercises
    
    def get_user_fitness_level(self, user_profile: Dict) -> str:
        """Determine user's fitness level based on profile"""
        experience_years = user_profile.get('experience_years', 0)
        # prefer explicit workout_frequency but fall back to workout_days (test uses workout_days)
        current_frequency = user_profile.get('workout_frequency', user_profile.get('workout_days', 0))

        if experience_years < 1 or current_frequency < 2:
            return 'beginner'
        elif experience_years < 3 or current_frequency < 4:
            return 'intermediate'
        else:
            return 'advanced'
    
    def filter_exercises_by_equipment(self, exercises: List[str], available_equipment: List[str]) -> List[str]:
        """Filter exercises based on available equipment"""
        available_exercises = []
        
        for exercise in exercises:
            exercise_info = self.exercises_database.get(exercise)
            if exercise_info:
                equipment_needed = exercise_info['equipment']
                if equipment_needed == 'none' or equipment_needed in available_equipment:
                    available_exercises.append(exercise)
        
        return available_exercises
    
    def select_exercises_for_workout(self, muscle_groups: List[str], difficulty: str, 
                                   available_equipment: List[str], workout_type: str) -> List[Dict]:
        """Select exercises for a specific workout"""
        selected_exercises = []
        
        # Get all exercises for the target muscle groups
        all_exercises = []
        for muscle_group in muscle_groups:
            if muscle_group in self.muscle_groups:
                all_exercises.extend(self.muscle_groups[muscle_group])
        
        # Filter by available equipment
        available_exercises = self.filter_exercises_by_equipment(all_exercises, available_equipment)
        
        # Filter by difficulty
        difficulty_level = self.difficulty_levels.get(difficulty, 1)
        filtered_exercises = []
        
        for exercise in available_exercises:
            exercise_info = self.exercises_database.get(exercise)
            if exercise_info:
                exercise_difficulty = self.difficulty_levels.get(exercise_info['difficulty'], 1)
                if exercise_difficulty <= difficulty_level:
                    filtered_exercises.append(exercise)
        
        # Select exercises based on workout type
        if workout_type == 'strength':
            # Select 4-6 exercises for strength training
            num_exercises = min(6, len(filtered_exercises))
            selected_exercise_names = random.sample(filtered_exercises, num_exercises)
        elif workout_type == 'cardio':
            # Select 2-3 cardio exercises
            cardio_exercises = [ex for ex in filtered_exercises if self.exercises_database[ex]['muscle_group'] == 'cardio']
            num_exercises = min(3, len(cardio_exercises))
            selected_exercise_names = random.sample(cardio_exercises, num_exercises)
        else:  # HIIT or mixed
            # Select 3-4 exercises for HIIT
            num_exercises = min(4, len(filtered_exercises))
            selected_exercise_names = random.sample(filtered_exercises, num_exercises)
        
        # Create exercise details
        for exercise_name in selected_exercise_names:
            exercise_info = self.exercises_database[exercise_name].copy()
            
            # Determine sets and reps based on workout type and difficulty
            if workout_type == 'strength':
                sets = random.randint(*exercise_info['sets_range'])
                reps = random.randint(*exercise_info['reps_range'])
                rest_time = exercise_info['rest_time']
            elif workout_type == 'cardio':
                sets = 1
                reps = 1
                duration = exercise_info.get('duration', 1800)  # Default 30 minutes
                rest_time = 0
            else:  # HIIT
                sets = random.randint(3, 5)
                reps = random.randint(10, 20)
                rest_time = self.rest_periods['hiit'][difficulty]
            
            selected_exercises.append({
                'exercise': exercise_info['name'],
                'muscle_group': exercise_info['muscle_group'],
                'instructions': exercise_info['instructions'],
                'sets': sets,
                'reps': reps,
                'rest_time': rest_time,
                'duration': exercise_info.get('duration', None)
            })
        
        return selected_exercises
    
    def generate_weekly_workout_plan(self, user_profile: Dict) -> Dict:
        """Generate a personalized weekly workout plan"""
        # Extract user information
        fitness_level = self.get_user_fitness_level(user_profile)
        goal = user_profile.get('goal', 'general_fitness')
        available_equipment = user_profile.get('available_equipment', ['none'])
        workout_days = user_profile.get('workout_days', 3)
        
        # Determine workout split based on goal and level
        if goal == 'muscle_gain' and fitness_level in ['intermediate', 'advanced']:
            workout_split = self.generate_muscle_gain_split(fitness_level)
        elif goal == 'weight_loss':
            workout_split = self.generate_weight_loss_split(fitness_level)
        else:
            workout_split = self.generate_general_fitness_split(fitness_level)
        
        # Generate weekly plan
        weekly_plan = {
            'user_profile': user_profile,
            'fitness_level': fitness_level,
            'goal': goal,
            'weekly_schedule': {}
        }
        
        days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

        for i, day in enumerate(days_of_week):
            if i < workout_days:
                workout_type = workout_split[i % len(workout_split)]
                muscle_groups = self.get_muscle_groups_for_workout(workout_type, goal)

                exercises = self.select_exercises_for_workout(
                    muscle_groups, fitness_level, available_equipment, workout_type
                )

                weekly_plan['weekly_schedule'][day] = {
                    'workout_type': workout_type,
                    'muscle_groups': muscle_groups,
                    'exercises': exercises,
                    'estimated_duration': self.calculate_workout_duration(exercises, fitness_level)
                }
            else:
                weekly_plan['weekly_schedule'][day] = {
                    'workout_type': 'rest',
                    'muscle_groups': [],
                    'exercises': [],
                    'estimated_duration': 0
                }

        # Backwards-compatible fields: some older tests expect top-level keys
        # 'workouts' (weekly schedule), 'duration' (total weekly minutes) and 'frequency' (workout_days)
        total_weekly_duration = sum(day.get('estimated_duration', 0) for day in weekly_plan['weekly_schedule'].values())
        weekly_plan['workouts'] = weekly_plan['weekly_schedule']
        weekly_plan['duration'] = total_weekly_duration
        weekly_plan['frequency'] = workout_days

        return weekly_plan
    
    def generate_muscle_gain_split(self, fitness_level: str) -> List[str]:
        """Generate workout split for muscle gain"""
        if fitness_level == 'beginner':
            return ['strength', 'strength', 'strength']  # Full body 3x/week
        elif fitness_level == 'intermediate':
            return ['strength', 'strength', 'strength', 'strength']  # Upper/Lower split
        else:  # advanced
            return ['strength', 'strength', 'strength', 'strength', 'strength']  # Push/Pull/Legs
    
    def generate_weight_loss_split(self, fitness_level: str) -> List[str]:
        """Generate workout split for weight loss"""
        if fitness_level == 'beginner':
            return ['strength', 'cardio', 'strength']
        elif fitness_level == 'intermediate':
            return ['strength', 'cardio', 'strength', 'cardio']
        else:  # advanced
            return ['strength', 'cardio', 'strength', 'cardio', 'hiit']
    
    def generate_general_fitness_split(self, fitness_level: str) -> List[str]:
        """Generate workout split for general fitness"""
        if fitness_level == 'beginner':
            return ['strength', 'cardio', 'strength']
        elif fitness_level == 'intermediate':
            return ['strength', 'cardio', 'strength', 'cardio']
        else:  # advanced
            return ['strength', 'cardio', 'strength', 'cardio', 'strength']
    
    def get_muscle_groups_for_workout(self, workout_type: str, goal: str) -> List[str]:
        """Get target muscle groups for a specific workout"""
        if workout_type == 'strength':
            if goal == 'muscle_gain':
                # Focus on specific muscle groups per workout
                return random.choice([
                    ['chest', 'shoulders', 'triceps'],
                    ['back', 'biceps'],
                    ['legs', 'core']
                ])
            else:
                # Full body or compound movements
                return ['chest', 'back', 'legs', 'shoulders', 'arms', 'core']
        elif workout_type == 'cardio':
            return ['cardio']
        else:  # HIIT
            return ['cardio', 'core']
    
    def calculate_workout_duration(self, exercises: List[Dict], fitness_level: str) -> int:
        """Calculate estimated workout duration in minutes"""
        total_time = 0
        
        for exercise in exercises:
            # Exercise time (assuming 30 seconds per set)
            exercise_time = exercise['sets'] * 30
            
            # Rest time between sets
            rest_time = exercise['rest_time'] * (exercise['sets'] - 1)
            
            # Duration-based exercises (like cardio)
            if exercise.get('duration'):
                exercise_time = exercise['duration']
                rest_time = 0
            
            total_time += exercise_time + rest_time
        
        # Add warm-up and cool-down time
        total_time += 300  # 5 minutes warm-up + cool-down
        
        return round(total_time / 60)  # Convert to minutes
    
    def get_exercise_details(self, exercise_name: str) -> Dict:
        """Get detailed information about a specific exercise"""
        for exercise_key, exercise_info in self.exercises_database.items():
            if exercise_info['name'].lower() == exercise_name.lower():
                return exercise_info
        
        return {'error': f'Exercise "{exercise_name}" not found'}

if __name__ == "__main__":
    # Test the workout model
    model = WorkoutModel()
    
    # Test user profile
    user_profile = {
        'age': 25,
        'gender': 'male',
        'experience_years': 2,
        'workout_frequency': 3,
        'goal': 'muscle_gain',
        'available_equipment': ['minimal'],
        'workout_days': 4
    }
    
    # Generate workout plan
    workout_plan = model.generate_weekly_workout_plan(user_profile)
    
    print("Workout Model Test Results:")
    print(f"Fitness Level: {workout_plan['fitness_level']}")
    print(f"Goal: {workout_plan['goal']}")
    
    # Show sample workout day
    for day, workout in workout_plan['weekly_schedule'].items():
        if workout['workout_type'] != 'rest':
            print(f"\n{day} - {workout['workout_type'].capitalize()} Workout:")
            print(f"Muscle Groups: {', '.join(workout['muscle_groups'])}")
            print(f"Duration: {workout['estimated_duration']} minutes")
            print("Exercises:")
            for exercise in workout['exercises']:
                if exercise.get('duration'):
                    print(f"  - {exercise['exercise']}: {exercise['sets']} set(s) for {exercise['duration']} seconds")
                else:
                    print(f"  - {exercise['exercise']}: {exercise['sets']} sets x {exercise['reps']} reps")
            break




