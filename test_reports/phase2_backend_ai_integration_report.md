# Phase 2: Backend AI Integration Test Report

**Test Date:** 2025-09-12T18:41:45.154829

## Summary
- **Total Tests:** 17
- **Passed:** 0
- **Failed:** 17
- **Pass Rate:** 0.00%
- **Average Latency:** 23.77ms

## Endpoint Test Results

### Chatbot
- Tests: 2
- Passed: 0
- Failed: 2
- Average Latency: 26.33ms

| Test ID | Input | Expected | Actual | Pass/Fail | Latency |
|---------|-------|----------|--------|-----------|---------|
| CB-API-001 | {'message': "What's the best e... | {'status': 200, 'has_response'... | {'status': 401, 'body': '{"pat... | FAIL | 37ms |
| CB-API-002 | {'message': 'I have severe che... | {'status': 200, 'safe_response... | {'status': 401, 'body': '{"pat... | FAIL | 16ms |

### Nutrition Plan
- Tests: 2
- Passed: 0
- Failed: 2
- Average Latency: 19.86ms

| Test ID | Input | Expected | Actual | Pass/Fail | Latency |
|---------|-------|----------|--------|-----------|---------|
| NP-API-001 | {'dietary_preferences': {'diet... | {'status': 200, 'respects_pref... | {'status': 401, 'body': '{"pat... | FAIL | 33ms |
| NP-API-002 | {'dietary_preferences': {'diet... | {'status': 200, 'follows_macro... | {'status': 401, 'body': '{"pat... | FAIL | 6ms |

### Pose Check
- Tests: 3
- Passed: 0
- Failed: 3
- Average Latency: 29.38ms

| Test ID | Input | Expected | Actual | Pass/Fail | Latency |
|---------|-------|----------|--------|-----------|---------|
| PC-API-001 | {'image_data': 'base64_encoded... | {'status': 200, 'has_feedback'... | {'status': 401, 'body': '{"pat... | FAIL | 12ms |
| PC-API-002 | {'invalid_field': 'test'}... | {'status': 400, 'has_error_mes... | {'status': 401, 'body': {'path... | FAIL | 38ms |
| PC-API-003 | {'image_data': 'xxxxxxxxxxxxxx... | {'status_ok': True, 'timeout_h... | {'status': 401, 'handled': Tru... | FAIL | 38ms |

### Workout Recommendation
- Tests: 2
- Passed: 0
- Failed: 2
- Average Latency: 19.50ms

| Test ID | Input | Expected | Actual | Pass/Fail | Latency |
|---------|-------|----------|--------|-----------|---------|
| WR-API-001 | {'user_profile': {'age': 25, '... | {'status': 200, 'has_workout_p... | {'status': 401, 'body': '{"pat... | FAIL | 30ms |
| WR-API-002 | {'user_profile': {'age': 35, '... | {'status': 200, 'considers_inj... | {'status': 401, 'body': '{"pat... | FAIL | 9ms |

## Error Handling Tests

- Total Tests: 8
- Passed: 0
- Failed: 8

## Performance Metrics

- **Concurrent Requests:** 10
- **Successful:** 0
- **Failed:** 10
- **Error Rate:** 100.00%
- **Avg Response Time:** 33.47ms
- **Max Response Time:** 57.75ms
- **Min Response Time:** 17.68ms
