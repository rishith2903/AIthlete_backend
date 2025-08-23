import json
import re
import random
from typing import Dict, List, Tuple, Optional
from datetime import datetime, timedelta
import numpy as np

class FitnessChatbot:
    def __init__(self):
        """Initialize the fitness chatbot"""
        self.load_knowledge_base()
        self.conversation_history = []
        self.user_context = {}
        
        # Intent patterns for classification
        self.intent_patterns = {
            'workout_question': [
                r'\b(workout|exercise|training|fitness)\b',
                r'\b(how|what|when|where)\b.*\b(exercise|workout|train)\b',
                r'\b(sets|reps|weight|routine)\b'
            ],
            'nutrition_question': [
                r'\b(nutrition|diet|food|meal|calorie|protein|carbs|fat)\b',
                r'\b(how|what|when)\b.*\b(eat|food|meal)\b',
                r'\b(calories|macros|supplements)\b'
            ],
            'motivation': [
                r'\b(motivate|motivation|encourage|inspire)\b',
                r'\b(tired|lazy|don\'t want|can\'t)\b',
                r'\b(quitting|giving up|stopping)\b'
            ],
            'progress_tracking': [
                r'\b(progress|results|improvement|track)\b',
                r'\b(weight|strength|endurance|muscle)\b.*\b(gain|lose|build)\b',
                r'\b(measure|track|monitor)\b'
            ],
            'injury_concern': [
                r'\b(pain|hurt|injury|sore|ache)\b',
                r'\b(should|can)\b.*\b(exercise|workout)\b.*\b(pain|hurt)\b',
                r'\b(rest|recovery|heal)\b'
            ],
            'general_health': [
                r'\b(health|healthy|wellness|lifestyle)\b',
                r'\b(sleep|stress|energy|mood)\b',
                r'\b(water|hydration|vitamins)\b'
            ]
        }
        
        # Response templates
        self.response_templates = {
            'workout_question': [
                "For {exercise}, I recommend {sets} sets of {reps} reps. Make sure to maintain proper form!",
                "When doing {exercise}, focus on {focus_point}. Start with {sets} sets and adjust based on your fitness level.",
                "For {exercise}, proper form is key. Try {sets} sets of {reps} reps with {rest_time} seconds rest between sets."
            ],
            'nutrition_question': [
                "For {goal}, aim for {calories} calories daily with {protein}g protein, {carbs}g carbs, and {fat}g fat.",
                "When it comes to {food}, it contains {calories} calories per serving. Great for {benefit}!",
                "For {meal_type}, try {suggestion}. It's {benefit} and fits well in a {diet_type} diet."
            ],
            'motivation': [
                "Remember why you started! Every workout brings you closer to your goals. You've got this! 💪",
                "Progress isn't always linear, but consistency is key. Keep pushing forward!",
                "Think about how good you'll feel after this workout. Your future self will thank you!"
            ],
            'progress_tracking': [
                "Great question! Track your {metric} weekly to see your progress. Consistency is key!",
                "For {goal}, measure {metrics} regularly. Progress takes time, but you're on the right track!",
                "Keep a workout log to track your {metric}. You'll be amazed at your progress over time!"
            ],
            'injury_concern': [
                "If you're experiencing {symptom}, it's best to rest and consult a healthcare professional.",
                "Listen to your body! If {symptom} persists, take a break and consider seeing a doctor.",
                "For {symptom}, try {remedy}. If it doesn't improve, please consult a medical professional."
            ],
            'general_health': [
                "For overall health, focus on {aspects}. Small changes add up to big results!",
                "Remember to {health_tip}. It's just as important as your workouts!",
                "A healthy lifestyle includes {components}. Keep up the great work!"
            ]
        }
        
        # Exercise database for specific questions
        self.exercise_db = {
            'squats': {
                'sets': '3-4',
                'reps': '10-15',
                'focus_point': 'keeping your back straight and knees aligned with toes',
                'rest_time': '60-90'
            },
            'push-ups': {
                'sets': '2-4',
                'reps': '8-20',
                'focus_point': 'maintaining a straight line from head to heels',
                'rest_time': '60'
            },
            'deadlifts': {
                'sets': '3-5',
                'reps': '5-10',
                'focus_point': 'keeping the bar close to your body and engaging your core',
                'rest_time': '120'
            },
            'bench_press': {
                'sets': '3-5',
                'reps': '8-12',
                'focus_point': 'keeping your feet flat and maintaining shoulder blade retraction',
                'rest_time': '90'
            }
        }
        
        # Nutrition database
        self.nutrition_db = {
            'chicken_breast': {
                'calories': 165,
                'protein': 31,
                'carbs': 0,
                'fat': 3.6,
                'benefit': 'excellent source of lean protein'
            },
            'rice': {
                'calories': 111,
                'protein': 2.6,
                'carbs': 23,
                'fat': 0.9,
                'benefit': 'good source of complex carbohydrates'
            },
            'banana': {
                'calories': 89,
                'protein': 1.1,
                'carbs': 23,
                'fat': 0.3,
                'benefit': 'great pre-workout fuel'
            }
        }
    
    def load_knowledge_base(self):
        """Load fitness knowledge base"""
        self.knowledge_base = {
            'workout_tips': [
                "Always warm up before exercising to prevent injury",
                "Focus on proper form over heavy weights",
                "Progressive overload is key to building strength",
                "Rest days are just as important as workout days",
                "Compound exercises work multiple muscle groups efficiently"
            ],
            'nutrition_tips': [
                "Protein helps with muscle recovery and growth",
                "Complex carbs provide sustained energy for workouts",
                "Healthy fats are essential for hormone production",
                "Stay hydrated throughout the day",
                "Eat a balanced meal 2-3 hours before working out"
            ],
            'motivation_quotes': [
                "The only bad workout is the one that didn't happen",
                "Strength doesn't come from what you can do, it comes from overcoming the things you thought you couldn't",
                "Your body can stand almost anything, it's your mind you have to convince",
                "The difference between try and triumph is just a little umph!",
                "Don't wish for it, work for it"
            ]
        }
    
    def classify_intent(self, message: str) -> str:
        """Classify user intent from message"""
        message_lower = message.lower()
        
        # Check each intent pattern
        for intent, patterns in self.intent_patterns.items():
            for pattern in patterns:
                if re.search(pattern, message_lower):
                    return intent
        
        return 'general_question'
    
    def extract_entities(self, message: str) -> Dict:
        """Extract relevant entities from user message"""
        entities = {}
        message_lower = message.lower()
        
        # Extract exercise names
        for exercise in self.exercise_db.keys():
            if exercise in message_lower:
                entities['exercise'] = exercise
        
        # Extract food names
        for food in self.nutrition_db.keys():
            if food.replace('_', ' ') in message_lower:
                entities['food'] = food
        
        # Extract numbers (sets, reps, weight, etc.)
        numbers = re.findall(r'\d+', message)
        if numbers:
            entities['numbers'] = [int(n) for n in numbers]
        
        # Extract goals
        goals = ['weight loss', 'muscle gain', 'strength', 'endurance', 'flexibility']
        for goal in goals:
            if goal in message_lower:
                entities['goal'] = goal
        
        return entities
    
    def generate_response(self, intent: str, entities: Dict, user_context: Dict = None) -> str:
        """Generate appropriate response based on intent and entities"""
        
        if intent == 'workout_question':
            if 'exercise' in entities:
                exercise = entities['exercise']
                exercise_info = self.exercise_db.get(exercise, {})
                return random.choice(self.response_templates['workout_question']).format(
                    exercise=exercise.replace('_', ' ').title(),
                    sets=exercise_info.get('sets', '3-4'),
                    reps=exercise_info.get('reps', '10-15'),
                    focus_point=exercise_info.get('focus_point', 'proper form'),
                    rest_time=exercise_info.get('rest_time', '60-90')
                )
            else:
                return "I'd be happy to help with workout questions! What specific exercise are you asking about?"
        
        elif intent == 'nutrition_question':
            if 'food' in entities:
                food = entities['food']
                food_info = self.nutrition_db.get(food, {})
                return random.choice(self.response_templates['nutrition_question']).format(
                    food=food.replace('_', ' ').title(),
                    calories=food_info.get('calories', 'varies'),
                    protein=food_info.get('protein', 'varies'),
                    carbs=food_info.get('carbs', 'varies'),
                    fat=food_info.get('fat', 'varies'),
                    benefit=food_info.get('benefit', 'nutritious'),
                    meal_type='meal',
                    suggestion='a balanced plate',
                    diet_type='healthy'
                )
            else:
                return "I can help with nutrition questions! What specific food or nutrition topic are you interested in?"
        
        elif intent == 'motivation':
            return random.choice(self.response_templates['motivation'])
        
        elif intent == 'progress_tracking':
            goal = entities.get('goal', 'fitness')
            metrics = {
                'weight loss': 'weight and body measurements',
                'muscle gain': 'strength and body measurements',
                'strength': 'lifting weights and reps',
                'endurance': 'cardio duration and intensity',
                'flexibility': 'range of motion and stretch depth'
            }
            return random.choice(self.response_templates['progress_tracking']).format(
                metric=metrics.get(goal, 'progress'),
                goal=goal,
                metrics=metrics.get(goal, 'key metrics')
            )
        
        elif intent == 'injury_concern':
            return random.choice(self.response_templates['injury_concern']).format(
                symptom='pain or discomfort',
                remedy='rest and ice'
            )
        
        elif intent == 'general_health':
            return random.choice(self.response_templates['general_health']).format(
                aspects='balanced nutrition, regular exercise, and adequate sleep',
                health_tip='stay hydrated and get enough sleep',
                components='exercise, nutrition, sleep, and stress management'
            )
        
        else:
            return self.get_general_response()
    
    def get_general_response(self) -> str:
        """Generate general fitness response"""
        general_responses = [
            "I'm here to help with your fitness journey! Ask me about workouts, nutrition, or motivation.",
            "Great question! I can help with exercise form, nutrition advice, or workout planning.",
            "I'd love to help! What aspect of fitness would you like to know more about?",
            "That's an interesting question! I can provide guidance on workouts, nutrition, or general fitness tips."
        ]
        return random.choice(general_responses)
    
    def get_workout_suggestion(self, user_level: str = 'beginner', goal: str = 'general') -> str:
        """Get workout suggestion based on user level and goal"""
        suggestions = {
            'beginner': {
                'general': "Start with bodyweight exercises like squats, push-ups, and planks. 3 sets of 10-15 reps each.",
                'strength': "Focus on compound movements: squats, deadlifts, and push-ups. Start with 3 sets of 8-12 reps.",
                'cardio': "Begin with walking or light jogging for 20-30 minutes, 3-4 times per week."
            },
            'intermediate': {
                'general': "Mix strength training with cardio. Try 4-5 exercises per workout, 3-4 sets each.",
                'strength': "Incorporate progressive overload. Focus on major lifts with 3-5 sets of 6-10 reps.",
                'cardio': "Add interval training: 30 seconds high intensity, 90 seconds rest, repeat for 20 minutes."
            },
            'advanced': {
                'general': "Implement periodization. Vary intensity and volume weekly for optimal results.",
                'strength': "Use advanced techniques like supersets and drop sets. 4-6 sets of 4-8 reps for strength.",
                'cardio': "High-intensity interval training: 20 seconds max effort, 10 seconds rest, 8 rounds."
            }
        }
        
        return suggestions.get(user_level, {}).get(goal, "Focus on consistency and progressive overload!")
    
    def get_nutrition_tip(self, goal: str = 'general') -> str:
        """Get nutrition tip based on goal"""
        tips = {
            'weight_loss': "Create a calorie deficit of 500 calories per day for sustainable weight loss. Focus on protein and vegetables.",
            'muscle_gain': "Eat in a slight calorie surplus with 1.6-2.2g protein per kg body weight. Include complex carbs for energy.",
            'strength': "Prioritize protein (1.6-2.2g/kg) and time your meals around workouts. Include creatine if desired.",
            'endurance': "Focus on carbohydrates for fuel (6-10g/kg) and adequate protein for recovery (1.2-1.6g/kg).",
            'general': "Eat a balanced diet with lean protein, complex carbohydrates, healthy fats, and plenty of vegetables."
        }
        
        return tips.get(goal, tips['general'])
    
    def process_message(self, message: str, user_context: Dict = None) -> Dict:
        """Process user message and generate response"""
        # Classify intent
        intent = self.classify_intent(message)
        
        # Extract entities
        entities = self.extract_entities(message)
        
        # Generate response
        response = self.generate_response(intent, entities, user_context)
        
        # Update conversation history
        self.conversation_history.append({
            'timestamp': datetime.now().isoformat(),
            'user_message': message,
            'intent': intent,
            'entities': entities,
            'bot_response': response
        })
        
        # Keep only last 10 messages
        if len(self.conversation_history) > 10:
            self.conversation_history = self.conversation_history[-10:]
        
        return {
            'response': response,
            'intent': intent,
            'entities': entities,
            'confidence': 0.85,  # Placeholder confidence score
            'suggestions': self.get_follow_up_suggestions(intent, entities)
        }
    
    def get_follow_up_suggestions(self, intent: str, entities: Dict) -> List[str]:
        """Get follow-up question suggestions"""
        suggestions = {
            'workout_question': [
                "How many sets should I do?",
                "What's the proper form?",
                "How much weight should I use?"
            ],
            'nutrition_question': [
                "How many calories should I eat?",
                "What's a good meal plan?",
                "Should I take supplements?"
            ],
            'motivation': [
                "I'm feeling tired today",
                "How do I stay consistent?",
                "What if I miss a workout?"
            ],
            'progress_tracking': [
                "How often should I measure?",
                "What metrics should I track?",
                "How long until I see results?"
            ]
        }
        
        return suggestions.get(intent, [
            "Tell me about workouts",
            "Help with nutrition",
            "I need motivation"
        ])
    
    def get_conversation_summary(self) -> Dict:
        """Get summary of conversation history"""
        if not self.conversation_history:
            return {'message': 'No conversation history available'}
        
        intents = [msg['intent'] for msg in self.conversation_history]
        intent_counts = {}
        for intent in intents:
            intent_counts[intent] = intent_counts.get(intent, 0) + 1
        
        return {
            'total_messages': len(self.conversation_history),
            'intent_distribution': intent_counts,
            'last_message_time': self.conversation_history[-1]['timestamp'],
            'common_topics': list(intent_counts.keys())
        }

if __name__ == "__main__":
    # Test the chatbot
    chatbot = FitnessChatbot()
    
    # Test messages
    test_messages = [
        "How many sets should I do for squats?",
        "What's the nutrition info for chicken breast?",
        "I'm feeling tired and don't want to workout",
        "How do I track my progress for weight loss?",
        "My knee hurts when I exercise",
        "What's a good workout for beginners?"
    ]
    
    print("Fitness Chatbot Test Results:")
    print("=" * 50)
    
    for message in test_messages:
        print(f"\nUser: {message}")
        response = chatbot.process_message(message)
        print(f"Bot: {response['response']}")
        print(f"Intent: {response['intent']}")
        print(f"Entities: {response['entities']}")
    
    # Show conversation summary
    print("\n" + "=" * 50)
    print("Conversation Summary:")
    summary = chatbot.get_conversation_summary()
    print(json.dumps(summary, indent=2))




