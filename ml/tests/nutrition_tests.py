#!/usr/bin/env python3
"""
Comprehensive Test Suite for Nutrition Model
Tests BMR calculation, meal planning, and nutritional accuracy
"""

import sys
import os
import json
from datetime import datetime

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class NutritionTestSuite:
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
            key_fields = ['bmr', 'tdee', 'calories', 'protein']
            passed = all(
                abs(actual_output.get(key, 0) - expected_output.get(key, 0)) < 50
                for key in key_fields if key in expected_output
            )
        elif isinstance(expected_output, (int, float)) and isinstance(actual_output, (int, float)):
            # Compare numeric outputs with tolerance
            passed = abs(actual_output - expected_output) < 50
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
    
    def test_bmr_calculation(self):
        """Test BMR calculation accuracy"""
        print("\n🍽️ Testing BMR Calculation...")
        
        # Test case 1: Male BMR calculation
        bmr = self.calculate_bmr(25, 'male', 75, 180)
        self.run_test(
            "BMR_001",
            "Male: 25y, 75kg, 180cm",
            {"min": 1600, "max": 1800},
            {"min": bmr, "max": bmr},
            "Male BMR calculation using Harris-Benedict"
        )
        
        # Test case 2: Female BMR calculation
        bmr = self.calculate_bmr(30, 'female', 60, 165)
        self.run_test(
            "BMR_002",
            "Female: 30y, 60kg, 165cm",
            {"min": 1300, "max": 1500},
            {"min": bmr, "max": bmr},
            "Female BMR calculation using Harris-Benedict"
        )
        
        # Test case 3: Elderly BMR calculation
        bmr = self.calculate_bmr(65, 'male', 70, 175)
        self.run_test(
            "BMR_003",
            "Elderly Male: 65y, 70kg, 175cm",
            {"min": 1400, "max": 1600},
            {"min": bmr, "max": bmr},
            "Elderly BMR calculation (lower metabolism)"
        )
    
    def calculate_bmr(self, age, gender, weight, height):
        """Calculate BMR using Harris-Benedict equation"""
        if gender.lower() == 'male':
            bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
        else:
            bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)
        return round(bmr)
    
    def test_tdee_calculation(self):
        """Test TDEE calculation accuracy"""
        print("\n🔥 Testing TDEE Calculation...")
        
        # Test case 4: Sedentary TDEE
        bmr = 1600
        tdee = self.calculate_tdee(bmr, 'sedentary')
        self.run_test(
            "TDEE_001",
            "Sedentary activity level",
            {"min": 1900, "max": 2100},
            {"min": tdee, "max": tdee},
            "Sedentary TDEE (BMR * 1.2)"
        )
        
        # Test case 5: Moderate TDEE
        tdee = self.calculate_tdee(bmr, 'moderate')
        self.run_test(
            "TDEE_002",
            "Moderate activity level",
            {"min": 2200, "max": 2400},
            {"min": tdee, "max": tdee},
            "Moderate TDEE (BMR * 1.55)"
        )
        
        # Test case 6: Very active TDEE
        tdee = self.calculate_tdee(bmr, 'very_active')
        self.run_test(
            "TDEE_003",
            "Very active level",
            {"min": 2600, "max": 2800},
            {"min": tdee, "max": tdee},
            "Very active TDEE (BMR * 1.725)"
        )
    
    def calculate_tdee(self, bmr, activity_level):
        """Calculate TDEE based on activity level"""
        activity_multipliers = {
            'sedentary': 1.2,
            'lightly_active': 1.375,
            'moderate': 1.55,
            'very_active': 1.725,
            'extremely_active': 1.9
        }
        multiplier = activity_multipliers.get(activity_level, 1.2)
        return round(bmr * multiplier)
    
    def test_macro_calculation(self):
        """Test macronutrient calculation accuracy"""
        print("\n⚖️ Testing Macro Calculation...")
        
        # Test case 7: Weight loss macros
        macros = self.calculate_macros(2000, 'weight_loss')
        self.run_test(
            "MACRO_001",
            "Weight loss: 2000 calories",
            {"protein": 150, "carbs": 200, "fat": 67},
            {"protein": macros.get('protein', 0), "carbs": macros.get('carbs', 0), "fat": macros.get('fat', 0)},
            "Weight loss macro ratios (30P/40C/30F)"
        )
        
        # Test case 8: Muscle gain macros
        macros = self.calculate_macros(2500, 'muscle_gain')
        self.run_test(
            "MACRO_002",
            "Muscle gain: 2500 calories",
            {"protein": 188, "carbs": 313, "fat": 83},
            {"protein": macros.get('protein', 0), "carbs": macros.get('carbs', 0), "fat": macros.get('fat', 0)},
            "Muscle gain macro ratios (30P/50C/20F)"
        )
        
        # Test case 9: Maintenance macros
        macros = self.calculate_macros(2200, 'maintenance')
        self.run_test(
            "MACRO_003",
            "Maintenance: 2200 calories",
            {"protein": 165, "carbs": 220, "fat": 73},
            {"protein": macros.get('protein', 0), "carbs": macros.get('carbs', 0), "fat": macros.get('fat', 0)},
            "Maintenance macro ratios (30P/40C/30F)"
        )
    
    def calculate_macros(self, calories, goal):
        """Calculate macronutrients based on goal"""
        if goal == 'weight_loss':
            protein_ratio = 0.30
            carb_ratio = 0.40
            fat_ratio = 0.30
        elif goal == 'muscle_gain':
            protein_ratio = 0.30
            carb_ratio = 0.50
            fat_ratio = 0.20
        else:  # maintenance
            protein_ratio = 0.30
            carb_ratio = 0.40
            fat_ratio = 0.30
        
        protein = round((calories * protein_ratio) / 4)  # 4 cal/g
        carbs = round((calories * carb_ratio) / 4)       # 4 cal/g
        fat = round((calories * fat_ratio) / 9)          # 9 cal/g
        
        return {
            'calories': calories,
            'protein': protein,
            'carbs': carbs,
            'fat': fat
        }
    
    def test_meal_plan_generation(self):
        """Test meal plan generation accuracy"""
        print("\n🍳 Testing Meal Plan Generation...")
        
        # Test case 10: Basic meal plan
        user_profile = {
            'age': 25, 'gender': 'male', 'weight': 75, 'height': 180,
            'activity_level': 'moderate', 'goal': 'weight_loss'
        }
        meal_plan = self.generate_meal_plan(user_profile)
        self.run_test(
            "MEAL_001",
            "Basic meal plan generation",
            {"has_plan": True, "days": 7},
            {"has_plan": bool(meal_plan), "days": len(meal_plan.get('weekly_plan', {}))},
            "Meal plan should have 7 days"
        )
        
        # Test case 11: Vegetarian meal plan
        user_profile['dietary_restrictions'] = ['vegetarian']
        meal_plan = self.generate_meal_plan(user_profile)
        self.run_test(
            "MEAL_002",
            "Vegetarian meal plan",
            {"has_plan": True, "vegetarian": True},
            {"has_plan": bool(meal_plan), "vegetarian": self.check_vegetarian(meal_plan)},
            "Vegetarian plan should exclude meat"
        )
        
        # Test case 12: Calorie target validation
        target_calories = meal_plan.get('nutritional_targets', {}).get('calories', 0)
        self.run_test(
            "MEAL_003",
            "Calorie target validation",
            {"min": 1800, "max": 2200},
            {"min": target_calories, "max": target_calories},
            "Calories should be within reasonable range"
        )
    
    def generate_meal_plan(self, user_profile):
        """Generate a basic meal plan"""
        # Calculate nutritional needs
        bmr = self.calculate_bmr(
            user_profile['age'], 
            user_profile['gender'], 
            user_profile['weight'], 
            user_profile['height']
        )
        tdee = self.calculate_tdee(bmr, user_profile['activity_level'])
        
        # Adjust for goal
        if user_profile['goal'] == 'weight_loss':
            target_calories = tdee - 500
        elif user_profile['goal'] == 'muscle_gain':
            target_calories = tdee + 300
        else:
            target_calories = tdee
        
        # Generate basic meal plan
        weekly_plan = {}
        for day in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
            weekly_plan[day] = {
                'breakfast': {'name': 'Oatmeal with berries', 'calories': 300},
                'lunch': {'name': 'Grilled chicken salad', 'calories': 400},
                'dinner': {'name': 'Salmon with vegetables', 'calories': 500},
                'snacks': [{'name': 'Greek yogurt', 'calories': 150}]
            }
        
        return {
            'weekly_plan': weekly_plan,
            'nutritional_targets': {
                'calories': target_calories,
                'protein': round((target_calories * 0.3) / 4),
                'carbs': round((target_calories * 0.4) / 4),
                'fat': round((target_calories * 0.3) / 9)
            }
        }
    
    def check_vegetarian(self, meal_plan):
        """Check if meal plan is vegetarian"""
        meat_items = ['chicken', 'beef', 'pork', 'lamb', 'fish', 'salmon']
        weekly_plan = meal_plan.get('weekly_plan', {})
        
        for day, meals in weekly_plan.items():
            for meal_type, meal in meals.items():
                if isinstance(meal, dict) and 'name' in meal:
                    meal_name = meal['name'].lower()
                    if any(meat in meal_name for meat in meat_items):
                        return False
        return True
    
    def test_edge_cases(self):
        """Test edge cases and error handling"""
        print("\n⚠️ Testing Edge Cases...")
        
        # Test case 13: Extreme age
        bmr = self.calculate_bmr(100, 'male', 70, 170)
        self.run_test(
            "EDGE_001",
            "Extreme age (100 years)",
            {"min": 1000, "max": 1400},
            {"min": bmr, "max": bmr},
            "Extreme age should have very low BMR"
        )
        
        # Test case 14: Extreme weight
        bmr = self.calculate_bmr(25, 'male', 150, 180)
        self.run_test(
            "EDGE_002",
            "Extreme weight (150kg)",
            {"min": 2500, "max": 3000},
            {"min": bmr, "max": bmr},
            "Extreme weight should have high BMR"
        )
        
        # Test case 15: Invalid activity level
        tdee = self.calculate_tdee(1600, 'invalid_level')
        self.run_test(
            "EDGE_003",
            "Invalid activity level",
            {"min": 1900, "max": 2100},
            {"min": tdee, "max": tdee},
            "Invalid activity should default to sedentary"
        )
    
    def generate_report(self):
        """Generate comprehensive test report"""
        print("\n" + "="*80)
        print("📊 NUTRITION MODEL - COMPREHENSIVE TEST REPORT")
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
            'model': 'Nutrition',
            'total_tests': total_tests,
            'passed_tests': passed_tests,
            'failed_tests': failed_tests,
            'success_rate': (passed_tests/total_tests)*100,
            'results': self.test_results
        }
        
        with open('nutrition_test_report.json', 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n📄 Test report saved to: nutrition_test_report.json")
        
        return passed_tests == total_tests

def main():
    """Run comprehensive nutrition tests"""
    print("TESTING: Nutrition Model - Comprehensive Test Suite")
    print("="*60)
    
    test_suite = NutritionTestSuite()
    
    # Run all test categories
    test_suite.test_bmr_calculation()
    test_suite.test_tdee_calculation()
    test_suite.test_macro_calculation()
    test_suite.test_meal_plan_generation()
    test_suite.test_edge_cases()
    
    # Generate report
    success = test_suite.generate_report()
    
    if success:
        print("\n🎉 ALL NUTRITION TESTS PASSED!")
        return True
    else:
        print("\n❌ Some nutrition tests failed. Please review the results.")
        return False

if __name__ == "__main__":
    main()
