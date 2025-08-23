import pandas as pd
import numpy as np
import json
import random
from typing import Dict, List, Tuple, Optional
import math
from datetime import datetime, timedelta

class NutritionModel:
    def __init__(self):
        """Initialize the nutrition model with food database"""
        self.food_data = None
        self.nutrient_data = None
        self.load_food_database()
        
        # Activity level multipliers for TDEE calculation
        self.activity_multipliers = {
            'sedentary': 1.2,      # Little or no exercise
            'light': 1.375,        # Light exercise 1-3 days/week
            'moderate': 1.55,      # Moderate exercise 3-5 days/week
            'active': 1.725,       # Hard exercise 6-7 days/week
            'very_active': 1.9     # Very hard exercise, physical job
        }
        
        # Macro ratios for different goals
        self.macro_ratios = {
            'weight_loss': {'protein': 0.3, 'carbs': 0.4, 'fat': 0.3},
            'muscle_gain': {'protein': 0.35, 'carbs': 0.45, 'fat': 0.2},
            'maintenance': {'protein': 0.25, 'carbs': 0.5, 'fat': 0.25},
            'endurance': {'protein': 0.2, 'carbs': 0.6, 'fat': 0.2}
        }
        
        # Meal timing distribution
        self.meal_distribution = {
            'breakfast': 0.25,
            'lunch': 0.35,
            'dinner': 0.35,
            'snack': 0.05
        }
        
        # Dietary restriction filters
        self.dietary_filters = {
            'vegan': ['animal_products', 'dairy', 'eggs'],
            'vegetarian': ['meat', 'fish'],
            'keto': ['high_carb'],
            'gluten_free': ['gluten'],
            'dairy_free': ['dairy']
        }
    
    def load_food_database(self):
        """Load food database from CSV files"""
        try:
            # Load main food data
            self.food_data = pd.read_csv('../Dataset/FoodData_Central_csv_2025-04-24/food.csv')
            
            # Load nutrient data
            self.nutrient_data = pd.read_csv('../Dataset/FoodData_Central_csv_2025-04-24/food_nutrient.csv')
            
            # Load nutrient definitions
            nutrient_defs = pd.read_csv('../Dataset/FoodData_Central_csv_2025-04-24/nutrient.csv')
            
            # Create nutrient mapping
            self.nutrient_mapping = dict(zip(nutrient_defs['id'], nutrient_defs['name']))
            
            # Filter and clean data
            self.clean_food_data()
            
            print(f"Loaded {len(self.food_data)} foods and {len(self.nutrient_data)} nutrient records")
            
        except Exception as e:
            print(f"Error loading food database: {e}")
            # Create sample data for testing
            self.create_sample_data()
    
    def clean_food_data(self):
        """Clean and prepare food data for analysis"""
        # Merge food and nutrient data
        self.food_nutrients = pd.merge(
            self.food_data, 
            self.nutrient_data, 
            on='fdc_id', 
            how='left'
        )
        
        # Pivot to get nutrients as columns
        self.food_nutrients_pivot = self.food_nutrients.pivot_table(
            index='fdc_id',
            columns='nutrient_id',
            values='amount',
            aggfunc='mean'
        ).reset_index()
        
        # Add food names back
        self.food_nutrients_pivot = pd.merge(
            self.food_nutrients_pivot,
            self.food_data[['fdc_id', 'description']],
            on='fdc_id',
            how='left'
        )
        
        # Fill NaN values with 0
        self.food_nutrients_pivot = self.food_nutrients_pivot.fillna(0)
    
    def create_sample_data(self):
        """Create sample food data for testing"""
        sample_foods = [
            {'fdc_id': 1, 'description': 'Chicken Breast', 'protein': 31, 'carbs': 0, 'fat': 3.6, 'calories': 165},
            {'fdc_id': 2, 'description': 'Brown Rice', 'protein': 2.6, 'carbs': 23, 'fat': 0.9, 'calories': 111},
            {'fdc_id': 3, 'description': 'Broccoli', 'protein': 2.8, 'carbs': 6.6, 'fat': 0.4, 'calories': 34},
            {'fdc_id': 4, 'description': 'Salmon', 'protein': 20, 'carbs': 0, 'fat': 13, 'calories': 208},
            {'fdc_id': 5, 'description': 'Sweet Potato', 'protein': 2, 'carbs': 20, 'fat': 0.2, 'calories': 86},
            {'fdc_id': 6, 'description': 'Greek Yogurt', 'protein': 10, 'carbs': 3.6, 'fat': 0.4, 'calories': 59},
            {'fdc_id': 7, 'description': 'Oatmeal', 'protein': 2.4, 'carbs': 12, 'fat': 1.4, 'calories': 68},
            {'fdc_id': 8, 'description': 'Banana', 'protein': 1.1, 'carbs': 23, 'fat': 0.3, 'calories': 89},
            {'fdc_id': 9, 'description': 'Eggs', 'protein': 13, 'carbs': 1.1, 'fat': 11, 'calories': 155},
            {'fdc_id': 10, 'description': 'Spinach', 'protein': 2.9, 'carbs': 3.6, 'fat': 0.4, 'calories': 23}
        ]
        
        self.food_data = pd.DataFrame(sample_foods)
        print("Created sample food data for testing")
    
    def calculate_bmr(self, age: int, gender: str, weight: float, height: float) -> float:
        """Calculate Basal Metabolic Rate using Mifflin-St Jeor Equation"""
        if gender.lower() == 'male':
            bmr = 10 * weight + 6.25 * height - 5 * age + 5
        else:
            bmr = 10 * weight + 6.25 * height - 5 * age - 161
        
        return bmr
    
    def calculate_tdee(self, bmr: float, activity_level: str) -> float:
        """Calculate Total Daily Energy Expenditure"""
        if activity_level not in self.activity_multipliers:
            activity_level = 'moderate'  # Default to moderate
        
        tdee = bmr * self.activity_multipliers[activity_level]
        return tdee
    
    def adjust_calories_for_goal(self, tdee: float, goal: str) -> float:
        """Adjust calories based on fitness goal"""
        if goal == 'weight_loss':
            return tdee - 500  # 500 calorie deficit
        elif goal == 'muscle_gain':
            return tdee + 300  # 300 calorie surplus
        else:
            return tdee  # Maintenance
    
    def calculate_macros(self, calories: float, goal: str) -> Dict[str, float]:
        """Calculate macronutrient targets"""
        if goal not in self.macro_ratios:
            goal = 'maintenance'
        
        ratios = self.macro_ratios[goal]
        
        # Calculate grams (protein and carbs = 4 cal/g, fat = 9 cal/g)
        protein_g = (calories * ratios['protein']) / 4
        carbs_g = (calories * ratios['carbs']) / 4
        fat_g = (calories * ratios['fat']) / 9
        
        return {
            'calories': calories,
            'protein': round(protein_g, 1),
            'carbs': round(carbs_g, 1),
            'fat': round(fat_g, 1)
        }
    
    def find_foods_by_macros(self, target_protein: float, target_carbs: float, 
                           target_fat: float, meal_type: str, 
                           dietary_restrictions: List[str] = None) -> List[Dict]:
        """Find foods that match target macros for a meal"""
        if self.food_data is None:
            return self.get_sample_foods_for_meal(meal_type)
        
        # Filter foods based on dietary restrictions
        available_foods = self.food_data.copy()
        
        if dietary_restrictions:
            for restriction in dietary_restrictions:
                if restriction in self.dietary_filters:
                    # Simple filtering - in real implementation, you'd have more detailed food attributes
                    pass
        
        # Calculate macro scores for each food
        foods_with_scores = []
        
        for _, food in available_foods.iterrows():
            # Calculate how well this food fits the target macros
            protein_score = 1 - abs(food.get('protein', 0) - target_protein * 0.3) / (target_protein * 0.3 + 1)
            carbs_score = 1 - abs(food.get('carbs', 0) - target_carbs * 0.3) / (target_carbs * 0.3 + 1)
            fat_score = 1 - abs(food.get('fat', 0) - target_fat * 0.3) / (target_fat * 0.3 + 1)
            
            total_score = (protein_score + carbs_score + fat_score) / 3
            
            foods_with_scores.append({
                'food': food,
                'score': total_score
            })
        
        # Sort by score and return top matches
        foods_with_scores.sort(key=lambda x: x['score'], reverse=True)
        
        return [item['food'] for item in foods_with_scores[:5]]
    
    def get_sample_foods_for_meal(self, meal_type: str) -> List[Dict]:
        """Get sample foods for different meal types"""
        meal_foods = {
            'breakfast': [
                {'description': 'Oatmeal with banana', 'protein': 8, 'carbs': 45, 'fat': 3, 'calories': 240},
                {'description': 'Greek yogurt with berries', 'protein': 15, 'carbs': 12, 'fat': 2, 'calories': 130},
                {'description': 'Whole grain toast with eggs', 'protein': 12, 'carbs': 25, 'fat': 8, 'calories': 220}
            ],
            'lunch': [
                {'description': 'Grilled chicken with rice', 'protein': 35, 'carbs': 45, 'fat': 8, 'calories': 380},
                {'description': 'Salmon with quinoa', 'protein': 28, 'carbs': 35, 'fat': 15, 'calories': 380},
                {'description': 'Turkey sandwich with vegetables', 'protein': 25, 'carbs': 40, 'fat': 6, 'calories': 310}
            ],
            'dinner': [
                {'description': 'Lean beef with sweet potato', 'protein': 30, 'carbs': 35, 'fat': 12, 'calories': 380},
                {'description': 'Tofu stir-fry with brown rice', 'protein': 18, 'carbs': 45, 'fat': 8, 'calories': 320},
                {'description': 'Fish with vegetables', 'protein': 25, 'carbs': 15, 'fat': 10, 'calories': 250}
            ],
            'snack': [
                {'description': 'Apple with almonds', 'protein': 4, 'carbs': 15, 'fat': 8, 'calories': 140},
                {'description': 'Protein shake', 'protein': 20, 'carbs': 5, 'fat': 2, 'calories': 120},
                {'description': 'Carrot sticks with hummus', 'protein': 3, 'carbs': 12, 'fat': 4, 'calories': 90}
            ]
        }
        
        return meal_foods.get(meal_type, meal_foods['lunch'])
    
    def generate_meal_plan(self, user_profile: Dict) -> Dict:
        """Generate a personalized 7-day meal plan"""
        # Extract user information
        age = user_profile.get('age', 30)
        gender = user_profile.get('gender', 'male')
        weight = user_profile.get('weight', 70)  # kg
        height = user_profile.get('height', 170)  # cm
        activity_level = user_profile.get('activity_level', 'moderate')
        goal = user_profile.get('goal', 'maintenance')
        dietary_restrictions = user_profile.get('dietary_restrictions', [])
        
        # Calculate nutritional needs
        bmr = self.calculate_bmr(age, gender, weight, height)
        tdee = self.calculate_tdee(bmr, activity_level)
        target_calories = self.adjust_calories_for_goal(tdee, goal)
        target_macros = self.calculate_macros(target_calories, goal)
        
        # Generate 7-day meal plan
        meal_plan = {
            'user_profile': user_profile,
            'nutritional_targets': target_macros,
            'weekly_plan': {}
        }
        
        for day in range(1, 8):
            day_name = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'][day - 1]
            
            day_plan = {
                'meals': {},
                'total_calories': 0,
                'total_protein': 0,
                'total_carbs': 0,
                'total_fat': 0
            }
            
            # Generate meals for the day
            for meal_type, calorie_ratio in self.meal_distribution.items():
                meal_calories = target_calories * calorie_ratio
                meal_protein = target_macros['protein'] * calorie_ratio
                meal_carbs = target_macros['carbs'] * calorie_ratio
                meal_fat = target_macros['fat'] * calorie_ratio
                
                # Find suitable foods for this meal
                foods = self.find_foods_by_macros(meal_protein, meal_carbs, meal_fat, meal_type, dietary_restrictions)
                
                # Select a food (in real implementation, you'd create combinations)
                selected_food = random.choice(foods) if foods else {
                    'description': f'Sample {meal_type} meal',
                    'protein': meal_protein,
                    'carbs': meal_carbs,
                    'fat': meal_fat,
                    'calories': float(meal_calories)
                }
                
                # Safely read numeric nutrition values (some food entries may be pandas Series)
                def _num(val, default=0.0):
                    try:
                        return float(val)
                    except Exception:
                        return default

                item_cal = _num(selected_food.get('calories', selected_food.get('energy', meal_calories)))
                item_pro = _num(selected_food.get('protein', 0.0))
                item_carbs = _num(selected_food.get('carbs', 0.0))
                item_fat = _num(selected_food.get('fat', 0.0))

                day_plan['meals'][meal_type] = {
                    'item': str(selected_food.get('description', selected_food.get('description', f'Sample {meal_type}'))),
                    'calories': round(item_cal, 0),
                    'protein': round(item_pro, 1),
                    'carbs': round(item_carbs, 1),
                    'fat': round(item_fat, 1)
                }

                # Update totals
                day_plan['total_calories'] += item_cal
                day_plan['total_protein'] += item_pro
                day_plan['total_carbs'] += item_carbs
                day_plan['total_fat'] += item_fat
            
            meal_plan['weekly_plan'][day_name] = day_plan
        
        return meal_plan
    
    def get_nutrition_info(self, food_name: str) -> Dict:
        """Get nutrition information for a specific food"""
        if self.food_data is None:
            return {'error': 'Food database not loaded'}
        
        # Search for food by name
        matching_foods = self.food_data[
            self.food_data['description'].str.contains(food_name, case=False, na=False)
        ]
        
        if len(matching_foods) == 0:
            return {'error': f'Food "{food_name}" not found'}
        
        # Return nutrition info for the first match
        food = matching_foods.iloc[0]
        
        return {
            'name': food['description'],
            'protein': food.get('protein', 0),
            'carbs': food.get('carbs', 0),
            'fat': food.get('fat', 0),
            'calories': food.get('calories', 0)
        }

if __name__ == "__main__":
    # Test the nutrition model
    model = NutritionModel()
    
    # Test user profile
    user_profile = {
        'age': 25,
        'gender': 'male',
        'weight': 75,  # kg
        'height': 180,  # cm
        'activity_level': 'moderate',
        'goal': 'weight_loss',
        'dietary_restrictions': []
    }
    
    # Generate meal plan
    meal_plan = model.generate_meal_plan(user_profile)
    
    print("Nutrition Model Test Results:")
    print(f"Target Calories: {meal_plan['nutritional_targets']['calories']}")
    print(f"Target Protein: {meal_plan['nutritional_targets']['protein']}g")
    print(f"Target Carbs: {meal_plan['nutritional_targets']['carbs']}g")
    print(f"Target Fat: {meal_plan['nutritional_targets']['fat']}g")
    
    # Show sample day
    sample_day = list(meal_plan['weekly_plan'].keys())[0]
    print(f"\nSample Day ({sample_day}):")
    for meal, info in meal_plan['weekly_plan'][sample_day]['meals'].items():
        print(f"{meal.capitalize()}: {info['item']} ({info['calories']} cal)")




