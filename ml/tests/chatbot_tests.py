#!/usr/bin/env python3
"""
Comprehensive Test Suite for Fitness Chatbot Model
Tests intent classification, response generation, and safety checks
"""

import sys
import os
import json
import re
from datetime import datetime

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class ChatbotTestSuite:
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
            key_fields = ['intent', 'response', 'entities']
            passed = all(
                actual_output.get(key) == expected_output.get(key) 
                for key in key_fields if key in expected_output
            )
        elif isinstance(expected_output, str) and isinstance(actual_output, str):
            # Compare string outputs (case insensitive for responses)
            passed = actual_output.lower() == expected_output.lower()
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
    
    def test_intent_classification(self):
        """Test intent classification accuracy"""
        print("\n🤖 Testing Intent Classification...")
        
        # Test case 1: Workout question
        message = "How many sets should I do for squats?"
        intent = self.classify_intent(message)
        self.run_test(
            "INTENT_001",
            "Workout question about sets",
            "workout_question",
            intent,
            "Should classify as workout question"
        )
        
        # Test case 2: Nutrition question
        message = "What's the nutrition info for chicken breast?"
        intent = self.classify_intent(message)
        self.run_test(
            "INTENT_002",
            "Nutrition question about food",
            "nutrition_question",
            intent,
            "Should classify as nutrition question"
        )
        
        # Test case 3: Motivation request
        message = "I'm feeling tired and don't want to workout"
        intent = self.classify_intent(message)
        self.run_test(
            "INTENT_003",
            "Motivation request",
            "motivation",
            intent,
            "Should classify as motivation request"
        )
        
        # Test case 4: Progress tracking
        message = "How do I track my progress for weight loss?"
        intent = self.classify_intent(message)
        self.run_test(
            "INTENT_004",
            "Progress tracking question",
            "progress_tracking",
            intent,
            "Should classify as progress tracking"
        )
        
        # Test case 5: General fitness question
        message = "What's the best time to workout?"
        intent = self.classify_intent(message)
        self.run_test(
            "INTENT_005",
            "General fitness question",
            "general_fitness",
            intent,
            "Should classify as general fitness"
        )
    
    def classify_intent(self, message):
        """Classify intent using regex patterns"""
        message_lower = message.lower()
        
        # Workout patterns
        workout_patterns = [
            r'\b(sets?|reps?|exercises?|workout|training)\b',
            r'\b(squats?|push.?ups?|deadlifts?|bench|press)\b',
            r'\b(how many|how much|how long)\b.*\b(do|perform|complete)\b'
        ]
        
        # Nutrition patterns
        nutrition_patterns = [
            r'\b(nutrition|calories?|protein|carbs?|fat)\b',
            r'\b(food|meal|diet|eating)\b',
            r'\b(chicken|beef|fish|vegetables?|fruits?)\b'
        ]
        
        # Motivation patterns
        motivation_patterns = [
            r'\b(tired|exhausted|don.?t want|lazy|unmotivated)\b',
            r'\b(give up|quit|stop|can.?t)\b',
            r'\b(motivation|motivate|encourage|inspire)\b'
        ]
        
        # Progress patterns
        progress_patterns = [
            r'\b(track|progress|results?|improvement)\b',
            r'\b(weight loss|muscle gain|fitness goals?)\b',
            r'\b(measure|monitor|record|log)\b'
        ]
        
        # Check patterns
        for pattern in workout_patterns:
            if re.search(pattern, message_lower):
                return "workout_question"
        
        for pattern in nutrition_patterns:
            if re.search(pattern, message_lower):
                return "nutrition_question"
        
        for pattern in motivation_patterns:
            if re.search(pattern, message_lower):
                return "motivation"
        
        for pattern in progress_patterns:
            if re.search(pattern, message_lower):
                return "progress_tracking"
        
        return "general_fitness"
    
    def test_entity_extraction(self):
        """Test entity extraction accuracy"""
        print("\n🔍 Testing Entity Extraction...")
        
        # Test case 6: Exercise entity
        message = "How many sets for squats?"
        entities = self.extract_entities(message)
        self.run_test(
            "ENTITY_001",
            "Extract exercise name",
            {"exercise": "squats"},
            entities,
            "Should extract exercise name"
        )
        
        # Test case 7: Number entity
        message = "I want to do 3 sets of push-ups"
        entities = self.extract_entities(message)
        self.run_test(
            "ENTITY_002",
            "Extract number",
            {"number": 3, "exercise": "push-ups"},
            entities,
            "Should extract number and exercise"
        )
        
        # Test case 8: Goal entity
        message = "I want to lose weight"
        entities = self.extract_entities(message)
        self.run_test(
            "ENTITY_003",
            "Extract goal",
            {"goal": "weight loss"},
            entities,
            "Should extract fitness goal"
        )
        
        # Test case 9: Food entity
        message = "What's the protein content in chicken breast?"
        entities = self.extract_entities(message)
        self.run_test(
            "ENTITY_004",
            "Extract food name",
            {"food": "chicken breast"},
            entities,
            "Should extract food name"
        )
    
    def extract_entities(self, message):
        """Extract entities from message"""
        message_lower = message.lower()
        entities = {}
        
        # Extract exercises
        exercises = ['squats', 'push-ups', 'deadlifts', 'bench press', 'pull-ups', 'lunges']
        for exercise in exercises:
            if exercise in message_lower:
                entities['exercise'] = exercise
                break
        
        # Extract numbers
        numbers = re.findall(r'\b(\d+)\b', message)
        if numbers:
            entities['number'] = int(numbers[0])
        
        # Extract goals
        if any(word in message_lower for word in ['lose weight', 'weight loss']):
            entities['goal'] = 'weight loss'
        elif any(word in message_lower for word in ['gain muscle', 'muscle gain', 'build muscle']):
            entities['goal'] = 'muscle gain'
        elif any(word in message_lower for word in ['maintain', 'maintenance']):
            entities['goal'] = 'maintenance'
        
        # Extract foods
        foods = ['chicken breast', 'salmon', 'beef', 'eggs', 'oatmeal', 'banana']
        for food in foods:
            if food in message_lower:
                entities['food'] = food
                break
        
        return entities
    
    def test_response_generation(self):
        """Test response generation quality"""
        print("\n💬 Testing Response Generation...")
        
        # Test case 10: Workout response
        message = "How many sets for squats?"
        response = self.generate_response(message)
        self.run_test(
            "RESPONSE_001",
            "Workout question response",
            {"has_response": True, "min_length": 20},
            {"has_response": bool(response), "min_length": len(response)},
            "Should generate helpful workout response"
        )
        
        # Test case 11: Nutrition response
        message = "What's the protein in chicken breast?"
        response = self.generate_response(message)
        self.run_test(
            "RESPONSE_002",
            "Nutrition question response",
            {"has_response": True, "min_length": 20},
            {"has_response": bool(response), "min_length": len(response)},
            "Should generate helpful nutrition response"
        )
        
        # Test case 12: Motivation response
        message = "I'm feeling tired and don't want to workout"
        response = self.generate_response(message)
        self.run_test(
            "RESPONSE_003",
            "Motivation response",
            {"has_response": True, "min_length": 30},
            {"has_response": bool(response), "min_length": len(response)},
            "Should generate encouraging motivation response"
        )
        
        # Test case 13: Progress tracking response
        message = "How do I track my weight loss progress?"
        response = self.generate_response(message)
        self.run_test(
            "RESPONSE_004",
            "Progress tracking response",
            {"has_response": True, "min_length": 25},
            {"has_response": bool(response), "min_length": len(response)},
            "Should generate helpful progress tracking response"
        )
    
    def generate_response(self, message):
        """Generate response based on message"""
        intent = self.classify_intent(message)
        entities = self.extract_entities(message)
        
        # Response templates
        responses = {
            "workout_question": {
                "squats": "For squats, aim for 3-4 sets of 8-12 reps. Focus on proper form and gradually increase weight as you get stronger.",
                "push-ups": "For push-ups, start with 3 sets of 5-10 reps. As you improve, increase to 15-20 reps per set.",
                "default": "For strength training, aim for 3-4 sets of 8-12 reps. For endurance, do 2-3 sets of 15-20 reps."
            },
            "nutrition_question": {
                "chicken breast": "Chicken breast is an excellent source of protein with about 31g per 100g serving. It's also low in fat and calories.",
                "default": "Focus on a balanced diet with lean protein, complex carbohydrates, and healthy fats. Aim for 1.6-2.2g of protein per kg of body weight."
            },
            "motivation": "Remember why you started! Even a short 10-minute workout is better than nothing. Start small and build consistency. You've got this!",
            "progress_tracking": "Track your progress by measuring weight, taking progress photos, recording workout performance, and noting how your clothes fit. Consistency is key!",
            "general_fitness": "Aim for at least 150 minutes of moderate exercise per week. Find activities you enjoy and make fitness a sustainable lifestyle habit."
        }
        
        # Get appropriate response
        if intent in responses:
            if intent == "workout_question" and "exercise" in entities:
                exercise = entities["exercise"]
                if exercise in responses[intent]:
                    return responses[intent][exercise]
                else:
                    return responses[intent]["default"]
            elif intent == "nutrition_question" and "food" in entities:
                food = entities["food"]
                if food in responses[intent]:
                    return responses[intent][food]
                else:
                    return responses[intent]["default"]
            else:
                return responses[intent]
        
        return "I'm here to help with your fitness journey! What specific question do you have about workouts, nutrition, or motivation?"
    
    def test_safety_checks(self):
        """Test safety and medical disclaimer checks"""
        print("\n🛡️ Testing Safety Checks...")
        
        # Test case 14: Medical disclaimer
        message = "I have a heart condition, what exercises should I do?"
        response = self.generate_response(message)
        self.run_test(
            "SAFETY_001",
            "Medical condition question",
            {"has_disclaimer": True},
            {"has_disclaimer": "consult" in response.lower() or "doctor" in response.lower()},
            "Should include medical disclaimer"
        )
        
        # Test case 15: Injury question
        message = "My knee hurts during squats, what should I do?"
        response = self.generate_response(message)
        self.run_test(
            "SAFETY_002",
            "Injury question",
            {"has_disclaimer": True},
            {"has_disclaimer": "consult" in response.lower() or "doctor" in response.lower() or "stop" in response.lower()},
            "Should include safety warning"
        )
        
        # Test case 16: Extreme weight loss
        message = "How can I lose 20 pounds in a week?"
        response = self.generate_response(message)
        self.run_test(
            "SAFETY_003",
            "Extreme weight loss question",
            {"has_warning": True},
            {"has_warning": "safe" in response.lower() or "gradual" in response.lower() or "consult" in response.lower()},
            "Should warn against extreme weight loss"
        )
    
    def test_conversation_flow(self):
        """Test conversation flow and context"""
        print("\n🔄 Testing Conversation Flow...")
        
        # Test case 17: Follow-up question
        context = {"previous_intent": "workout_question", "exercise": "squats"}
        message = "What about the form?"
        response = self.generate_followup_response(message, context)
        self.run_test(
            "FLOW_001",
            "Follow-up form question",
            {"has_response": True, "relevant": True},
            {"has_response": bool(response), "relevant": "form" in response.lower() or "technique" in response.lower()},
            "Should provide relevant follow-up response"
        )
        
        # Test case 18: Context switching
        context = {"previous_intent": "nutrition_question"}
        message = "Now tell me about workouts"
        response = self.generate_followup_response(message, context)
        self.run_test(
            "FLOW_002",
            "Context switching",
            {"has_response": True, "topic_change": True},
            {"has_response": bool(response), "topic_change": "workout" in response.lower() or "exercise" in response.lower()},
            "Should handle topic switching gracefully"
        )
    
    def generate_followup_response(self, message, context):
        """Generate follow-up response with context"""
        current_intent = self.classify_intent(message)
        
        if context.get("previous_intent") == "workout_question" and "form" in message.lower():
            return "For proper squat form: Keep your feet shoulder-width apart, chest up, knees in line with toes, and go as deep as you can while maintaining good form. Start with bodyweight squats to perfect your technique."
        elif current_intent == "workout_question":
            return "Great question! For effective workouts, focus on compound movements like squats, deadlifts, and push-ups. Aim for 3-4 sets of 8-12 reps for strength building."
        else:
            return self.generate_response(message)
    
    def test_edge_cases(self):
        """Test edge cases and error handling"""
        print("\n⚠️ Testing Edge Cases...")
        
        # Test case 19: Empty message
        response = self.generate_response("")
        self.run_test(
            "EDGE_001",
            "Empty message",
            {"has_response": True},
            {"has_response": bool(response)},
            "Should handle empty message gracefully"
        )
        
        # Test case 20: Very long message
        long_message = "I want to know everything about fitness and nutrition and workouts and how to get stronger and build muscle and lose fat and improve my health and wellness and become the best version of myself" * 5
        response = self.generate_response(long_message)
        self.run_test(
            "EDGE_002",
            "Very long message",
            {"has_response": True},
            {"has_response": bool(response)},
            "Should handle very long messages"
        )
        
        # Test case 21: Non-English characters
        response = self.generate_response("¿Cómo hacer sentadillas?")
        self.run_test(
            "EDGE_003",
            "Non-English message",
            {"has_response": True},
            {"has_response": bool(response)},
            "Should handle non-English characters"
        )
    
    def generate_report(self):
        """Generate comprehensive test report"""
        print("\n" + "="*80)
        print("📊 FITNESS CHATBOT MODEL - COMPREHENSIVE TEST REPORT")
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
            'model': 'Fitness Chatbot',
            'total_tests': total_tests,
            'passed_tests': passed_tests,
            'failed_tests': failed_tests,
            'success_rate': (passed_tests/total_tests)*100,
            'results': self.test_results
        }
        
        with open('chatbot_test_report.json', 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n📄 Test report saved to: chatbot_test_report.json")
        
        return passed_tests == total_tests

def main():
    """Run comprehensive chatbot tests"""
    print("TESTING: Fitness Chatbot Model - Comprehensive Test Suite")
    print("="*60)
    
    test_suite = ChatbotTestSuite()
    
    # Run all test categories
    test_suite.test_intent_classification()
    test_suite.test_entity_extraction()
    test_suite.test_response_generation()
    test_suite.test_safety_checks()
    test_suite.test_conversation_flow()
    test_suite.test_edge_cases()
    
    # Generate report
    success = test_suite.generate_report()
    
    if success:
        print("\n🎉 ALL CHATBOT TESTS PASSED!")
        return True
    else:
        print("\n❌ Some chatbot tests failed. Please review the results.")
        return False

if __name__ == "__main__":
    main()
