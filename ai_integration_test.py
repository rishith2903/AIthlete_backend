#!/usr/bin/env python3
"""
AI Model Integration Test Suite for Spring Boot Backend
Tests all AI endpoints and their integration with ML services
"""

import requests
import json
import time
import base64
from typing import Dict, Any, List
import concurrent.futures
import statistics

class AIIntegrationTester:
    def __init__(self, base_url: str = "http://localhost:8080/api"):
        self.base_url = base_url
        self.results = []
        self.session = requests.Session()
        
    def log_test(self, endpoint: str, test_input: Dict, expected_response: Dict, 
                 actual_response: Dict, status: str, latency_ms: float):
        """Log test results"""
        # Convert type objects to strings for JSON serialization
        serializable_expected = {}
        for key, value in expected_response.items():
            if isinstance(value, type):
                serializable_expected[key] = value.__name__
            else:
                serializable_expected[key] = value
                
        result = {
            "endpoint": endpoint,
            "test_input": test_input,
            "expected_response": serializable_expected,
            "actual_response": actual_response,
            "status": status,
            "latency_ms": latency_ms
        }
        self.results.append(result)
        print(f"✅ {endpoint}: {status} ({latency_ms:.2f}ms)")
        
    def test_pose_analysis(self) -> List[Dict]:
        """Test pose analysis endpoints"""
        print("\n🔍 Testing Pose Analysis Endpoints...")
        
        # Test 1: Analyze pose with valid data
        test_input = {
            "image_data": base64.b64encode(b"fake_image_data").decode(),
            "exercise_type": "squat"
        }
        expected_response = {
            "form_quality": str,
            "score": int,
            "feedback": list
        }
        
        start_time = time.time()
        try:
            response = self.session.post(
                f"{self.base_url}/pose/analyze",
                json=test_input,
                timeout=10
            )
            latency = (time.time() - start_time) * 1000
            
            if response.status_code == 200:
                actual_response = response.json()
                self.log_test("/pose/analyze", test_input, expected_response, actual_response, "PASS", latency)
            else:
                self.log_test("/pose/analyze", test_input, expected_response, {"error": response.text}, "FAIL", latency)
        except Exception as e:
            latency = (time.time() - start_time) * 1000
            self.log_test("/pose/analyze", test_input, expected_response, {"error": str(e)}, "FAIL", latency)
        
        # Test 2: Get supported exercises
        test_input = {}
        expected_response = {"exercises": list}
        
        start_time = time.time()
        try:
            response = self.session.get(f"{self.base_url}/pose/exercises", timeout=10)
            latency = (time.time() - start_time) * 1000
            
            if response.status_code == 200:
                actual_response = response.json()
                self.log_test("/pose/exercises", test_input, expected_response, actual_response, "PASS", latency)
            else:
                self.log_test("/pose/exercises", test_input, expected_response, {"error": response.text}, "FAIL", latency)
        except Exception as e:
            latency = (time.time() - start_time) * 1000
            self.log_test("/pose/exercises", test_input, expected_response, {"error": str(e)}, "FAIL", latency)
        
        # Test 3: Invalid pose data
        test_input = {
            "image_data": "invalid_data",
            "exercise_type": "invalid_exercise"
        }
        expected_response = {"error": str}
        
        start_time = time.time()
        try:
            response = self.session.post(
                f"{self.base_url}/pose/analyze",
                json=test_input,
                timeout=10
            )
            latency = (time.time() - start_time) * 1000
            
            if response.status_code == 400:
                actual_response = response.json()
                self.log_test("/pose/analyze (invalid)", test_input, expected_response, actual_response, "PASS", latency)
            else:
                self.log_test("/pose/analyze (invalid)", test_input, expected_response, {"error": "Expected 400"}, "FAIL", latency)
        except Exception as e:
            latency = (time.time() - start_time) * 1000
            self.log_test("/pose/analyze (invalid)", test_input, expected_response, {"error": str(e)}, "FAIL", latency)
    
    def test_workout_recommendation(self) -> List[Dict]:
        """Test workout recommendation endpoints"""
        print("\n💪 Testing Workout Recommendation Endpoints...")
        
        # Test 1: Generate workout plan
        test_input = {
            "age": 25,
            "gender": "male",
            "weight": 70,
            "height": 175,
            "fitness_level": "intermediate",
            "goal": "strength",
            "equipment": "gym"
        }
        expected_response = {
            "workouts": list,
            "duration": int,
            "frequency": int
        }
        
        start_time = time.time()
        try:
            response = self.session.post(
                f"{self.base_url}/workout/generate-plan",
                json=test_input,
                timeout=10
            )
            latency = (time.time() - start_time) * 1000
            
            if response.status_code == 200:
                actual_response = response.json()
                self.log_test("/workout/generate-plan", test_input, expected_response, actual_response, "PASS", latency)
            else:
                self.log_test("/workout/generate-plan", test_input, expected_response, {"error": response.text}, "FAIL", latency)
        except Exception as e:
            latency = (time.time() - start_time) * 1000
            self.log_test("/workout/generate-plan", test_input, expected_response, {"error": str(e)}, "FAIL", latency)
        
        # Test 2: Get available exercises
        test_input = {}
        expected_response = {"exercises": list}
        
        start_time = time.time()
        try:
            response = self.session.get(f"{self.base_url}/workout/exercises", timeout=10)
            latency = (time.time() - start_time) * 1000
            
            if response.status_code == 200:
                actual_response = response.json()
                self.log_test("/workout/exercises", test_input, expected_response, actual_response, "PASS", latency)
            else:
                self.log_test("/workout/exercises", test_input, expected_response, {"error": response.text}, "FAIL", latency)
        except Exception as e:
            latency = (time.time() - start_time) * 1000
            self.log_test("/workout/exercises", test_input, expected_response, {"error": str(e)}, "FAIL", latency)
    
    def test_nutrition_planning(self) -> List[Dict]:
        """Test nutrition planning endpoints"""
        print("\n🍎 Testing Nutrition Planning Endpoints...")
        
        # Test 1: Generate meal plan
        test_input = {
            "age": 25,
            "gender": "female",
            "weight": 60,
            "height": 165,
            "activity_level": "moderate",
            "goal": "weight_loss",
            "dietary_restrictions": ["vegetarian"]
        }
        expected_response = {
            "daily_calories": int,
            "macros": dict,
            "meals": list
        }
        
        start_time = time.time()
        try:
            response = self.session.post(
                f"{self.base_url}/nutrition/generate-meal-plan",
                json=test_input,
                timeout=10
            )
            latency = (time.time() - start_time) * 1000
            
            if response.status_code == 200:
                actual_response = response.json()
                self.log_test("/nutrition/generate-meal-plan", test_input, expected_response, actual_response, "PASS", latency)
            else:
                self.log_test("/nutrition/generate-meal-plan", test_input, expected_response, {"error": response.text}, "FAIL", latency)
        except Exception as e:
            latency = (time.time() - start_time) * 1000
            self.log_test("/nutrition/generate-meal-plan", test_input, expected_response, {"error": str(e)}, "FAIL", latency)
        
        # Test 2: Calculate BMR
        test_input = {
            "age": 30,
            "gender": "male",
            "weight": 80,
            "height": 180
        }
        expected_response = {
            "bmr": int,
            "tdee": int,
            "recommendations": dict
        }
        
        start_time = time.time()
        try:
            response = self.session.post(
                f"{self.base_url}/nutrition/calculate-bmr",
                json=test_input,
                timeout=10
            )
            latency = (time.time() - start_time) * 1000
            
            if response.status_code == 200:
                actual_response = response.json()
                self.log_test("/nutrition/calculate-bmr", test_input, expected_response, actual_response, "PASS", latency)
            else:
                self.log_test("/nutrition/calculate-bmr", test_input, expected_response, {"error": response.text}, "FAIL", latency)
        except Exception as e:
            latency = (time.time() - start_time) * 1000
            self.log_test("/nutrition/calculate-bmr", test_input, expected_response, {"error": str(e)}, "FAIL", latency)
    
    def test_chatbot(self) -> List[Dict]:
        """Test chatbot endpoints"""
        print("\n🤖 Testing Chatbot Endpoints...")
        
        # Test 1: Chat with bot
        test_input = {
            "message": "How many calories should I eat to lose weight?",
            "session_id": "test_session_123"
        }
        expected_response = {
            "response": str,
            "session_id": str
        }
        
        start_time = time.time()
        try:
            response = self.session.post(
                f"{self.base_url}/chatbot/chat",
                json=test_input,
                timeout=10
            )
            latency = (time.time() - start_time) * 1000
            
            if response.status_code == 200:
                actual_response = response.json()
                self.log_test("/chatbot/chat", test_input, expected_response, actual_response, "PASS", latency)
            else:
                self.log_test("/chatbot/chat", test_input, expected_response, {"error": response.text}, "FAIL", latency)
        except Exception as e:
            latency = (time.time() - start_time) * 1000
            self.log_test("/chatbot/chat", test_input, expected_response, {"error": str(e)}, "FAIL", latency)
        
        # Test 2: Classify intent
        test_input = {
            "message": "I want to do 3 sets of squats"
        }
        expected_response = {
            "intent": str,
            "confidence": float,
            "entities": dict
        }
        
        start_time = time.time()
        try:
            response = self.session.post(
                f"{self.base_url}/chatbot/classify-intent",
                json=test_input,
                timeout=10
            )
            latency = (time.time() - start_time) * 1000
            
            if response.status_code == 200:
                actual_response = response.json()
                self.log_test("/chatbot/classify-intent", test_input, expected_response, actual_response, "PASS", latency)
            else:
                self.log_test("/chatbot/classify-intent", test_input, expected_response, {"error": response.text}, "FAIL", latency)
        except Exception as e:
            latency = (time.time() - start_time) * 1000
            self.log_test("/chatbot/classify-intent", test_input, expected_response, {"error": str(e)}, "FAIL", latency)
    
    def test_error_handling(self) -> List[Dict]:
        """Test error handling scenarios"""
        print("\n⚠️ Testing Error Handling...")
        
        # Test 1: Invalid JSON
        test_input = "invalid json"
        expected_response = {"error": str}
        
        start_time = time.time()
        try:
            response = self.session.post(
                f"{self.base_url}/workout/generate-plan",
                data=test_input,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            latency = (time.time() - start_time) * 1000
            
            if response.status_code == 400:
                actual_response = response.json()
                self.log_test("/workout/generate-plan (invalid JSON)", test_input, expected_response, actual_response, "PASS", latency)
            else:
                self.log_test("/workout/generate-plan (invalid JSON)", test_input, expected_response, {"error": "Expected 400"}, "FAIL", latency)
        except Exception as e:
            latency = (time.time() - start_time) * 1000
            self.log_test("/workout/generate-plan (invalid JSON)", test_input, expected_response, {"error": str(e)}, "FAIL", latency)
        
        # Test 2: Missing required fields
        test_input = {"age": 25}  # Missing other required fields
        expected_response = {"error": str}
        
        start_time = time.time()
        try:
            response = self.session.post(
                f"{self.base_url}/nutrition/generate-meal-plan",
                json=test_input,
                timeout=10
            )
            latency = (time.time() - start_time) * 1000
            
            if response.status_code == 400:
                actual_response = response.json()
                self.log_test("/nutrition/generate-meal-plan (missing fields)", test_input, expected_response, actual_response, "PASS", latency)
            else:
                self.log_test("/nutrition/generate-meal-plan (missing fields)", test_input, expected_response, {"error": "Expected 400"}, "FAIL", latency)
        except Exception as e:
            latency = (time.time() - start_time) * 1000
            self.log_test("/nutrition/generate-meal-plan (missing fields)", test_input, expected_response, {"error": str(e)}, "FAIL", latency)
    
    def test_performance(self) -> List[Dict]:
        """Test performance with concurrent requests"""
        print("\n⚡ Testing Performance...")
        
        def make_request(endpoint: str, data: Dict) -> Dict:
            start_time = time.time()
            try:
                response = self.session.post(f"{self.base_url}{endpoint}", json=data, timeout=10)
                latency = (time.time() - start_time) * 1000
                return {
                    "endpoint": endpoint,
                    "status_code": response.status_code,
                    "latency_ms": latency,
                    "success": response.status_code == 200
                }
            except Exception as e:
                latency = (time.time() - start_time) * 1000
                return {
                    "endpoint": endpoint,
                    "error": str(e),
                    "latency_ms": latency,
                    "success": False
                }
        
        # Concurrent requests test
        test_data = [
            ("/workout/generate-plan", {"age": 25, "gender": "male", "weight": 70, "height": 175, "fitness_level": "beginner", "goal": "strength"}),
            ("/nutrition/generate-meal-plan", {"age": 25, "gender": "female", "weight": 60, "height": 165, "activity_level": "moderate", "goal": "weight_loss"}),
            ("/chatbot/chat", {"message": "Hello", "session_id": "perf_test"}),
        ]
        
        print("Running concurrent performance test...")
        start_time = time.time()
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(make_request, endpoint, data) for endpoint, data in test_data * 3]  # 9 total requests
            results = [future.result() for future in concurrent.futures.as_completed(futures)]
        
        total_time = (time.time() - start_time) * 1000
        successful_requests = sum(1 for r in results if r["success"])
        latencies = [r["latency_ms"] for r in results]
        
        performance_summary = {
            "total_requests": len(results),
            "successful_requests": successful_requests,
            "success_rate": (successful_requests / len(results)) * 100,
            "total_time_ms": total_time,
            "avg_latency_ms": statistics.mean(latencies) if latencies else 0,
            "min_latency_ms": min(latencies) if latencies else 0,
            "max_latency_ms": max(latencies) if latencies else 0,
            "requests_per_second": len(results) / (total_time / 1000)
        }
        
        print(f"Performance Summary:")
        print(f"  Total Requests: {performance_summary['total_requests']}")
        print(f"  Success Rate: {performance_summary['success_rate']:.1f}%")
        print(f"  Average Latency: {performance_summary['avg_latency_ms']:.2f}ms")
        print(f"  Requests/Second: {performance_summary['requests_per_second']:.2f}")
        
        return performance_summary
    
    def run_all_tests(self) -> Dict[str, Any]:
        """Run all integration tests"""
        print("🚀 Starting AI Integration Tests...")
        print(f"Testing backend at: {self.base_url}")
        
        # Run all test suites
        self.test_pose_analysis()
        self.test_workout_recommendation()
        self.test_nutrition_planning()
        self.test_chatbot()
        self.test_error_handling()
        performance_results = self.test_performance()
        
        # Calculate overall statistics
        total_tests = len(self.results)
        passed_tests = sum(1 for r in self.results if r["status"] == "PASS")
        failed_tests = total_tests - passed_tests
        success_rate = (passed_tests / total_tests) * 100 if total_tests > 0 else 0
        
        latencies = [r["latency_ms"] for r in self.results if r["status"] == "PASS"]
        avg_latency = statistics.mean(latencies) if latencies else 0
        
        # Generate summary
        summary = {
            "total_tests": total_tests,
            "passed_tests": passed_tests,
            "failed_tests": failed_tests,
            "success_rate": success_rate,
            "average_latency_ms": avg_latency,
            "performance_results": performance_results,
            "test_results": self.results
        }
        
        print(f"\n📊 Test Summary:")
        print(f"  Total Tests: {total_tests}")
        print(f"  Passed: {passed_tests}")
        print(f"  Failed: {failed_tests}")
        print(f"  Success Rate: {success_rate:.1f}%")
        print(f"  Average Latency: {avg_latency:.2f}ms")
        
        if success_rate >= 95:
            print("✅ AI Integration Test PASSED (≥95% success rate)")
        else:
            print("❌ AI Integration Test FAILED (<95% success rate)")
        
        return summary
    
    def save_results(self, filename: str = "ai_integration_test_results.json"):
        """Save test results to file"""
        with open(filename, 'w') as f:
            json.dump(self.results, f, indent=2)
        print(f"📄 Test results saved to {filename}")

def main():
    """Main test execution"""
    import sys
    
    # Parse command line arguments
    base_url = "http://localhost:8080/api"
    if len(sys.argv) > 1:
        base_url = sys.argv[1]
    
    # Create tester and run tests
    tester = AIIntegrationTester(base_url)
    summary = tester.run_all_tests()
    
    # Save results
    tester.save_results()
    
    # Exit with appropriate code
    if summary["success_rate"] >= 95:
        sys.exit(0)  # Success
    else:
        sys.exit(1)  # Failure

if __name__ == "__main__":
    main()
