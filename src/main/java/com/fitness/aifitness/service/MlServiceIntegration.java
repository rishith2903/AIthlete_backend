package com.fitness.aifitness.service;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import java.util.Map;

@Service
public class MlServiceIntegration {

    @Autowired
    private RestTemplate restTemplate;

    @Value("${ml.service.base-url}")
    private String mlServiceBaseUrl;

    @Value("${ml.service.timeout}")
    private int timeout;

    public Map<String, Object> getWorkoutPlan(Map<String, Object> userProfile) {
        String url = mlServiceBaseUrl + "/workout/generate-plan";
        return makeRequest(url, userProfile);
    }

    public Map<String, Object> getNutritionPlan(Map<String, Object> userProfile) {
        String url = mlServiceBaseUrl + "/nutrition/generate-meal-plan";
        return makeRequest(url, userProfile);
    }

    public Map<String, Object> chatWithBot(String message, String sessionId) {
        String url = mlServiceBaseUrl + "/chatbot/chat";
        Map<String, Object> request = Map.of(
            "message", message,
            "session_id", sessionId
        );
        return makeRequest(url, request);
    }

    public Map<String, Object> analyzePose(String imageData, String exerciseType) {
        String url = mlServiceBaseUrl + "/pose/analyze";
        Map<String, Object> request = Map.of(
            "image_data", imageData,
            "exercise_type", exerciseType
        );
        return makeRequest(url, request);
    }

    private Map<String, Object> makeRequest(String url, Object requestBody) {
        try {
            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_JSON);

            HttpEntity<Object> entity = new HttpEntity<>(requestBody, headers);
            ResponseEntity<Map> response = restTemplate.postForEntity(url, entity, Map.class);

            return response.getBody();
        } catch (Exception e) {
            // Return fallback response if ML service is unavailable
            return Map.of(
                "error", "ML service temporarily unavailable",
                "fallback", true
            );
        }
    }
}




