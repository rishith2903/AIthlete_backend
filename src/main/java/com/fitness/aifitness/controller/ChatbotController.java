package com.fitness.aifitness.controller;

import com.fitness.aifitness.service.MlServiceIntegration;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.Map;
import java.util.HashMap;
import java.util.UUID;

@RestController
@RequestMapping("/chatbot")
@Tag(name = "Chatbot", description = "Fitness chatbot endpoints")
public class ChatbotController {

    @Autowired
    private MlServiceIntegration mlServiceIntegration;

    @PostMapping("/chat")
    @Operation(summary = "Chat with fitness bot")
    public ResponseEntity<?> chat(@RequestBody Map<String, String> chatRequest) {
        try {
            String message = chatRequest.get("message");
            String sessionId = chatRequest.getOrDefault("session_id", UUID.randomUUID().toString());

            Map<String, Object> response = mlServiceIntegration.chatWithBot(message, sessionId);
            
            // Add session ID to response
            response.put("session_id", sessionId);
            
            return ResponseEntity.ok(response);
        } catch (Exception e) {
            Map<String, String> error = new HashMap<>();
            error.put("error", "Failed to process chat message: " + e.getMessage());
            return ResponseEntity.badRequest().body(error);
        }
    }

    @PostMapping("/classify-intent")
    @Operation(summary = "Classify user intent")
    public ResponseEntity<?> classifyIntent(@RequestBody Map<String, String> request) {
        try {
            String message = request.get("message");
            
            // This would use the ML service to classify intent
            Map<String, Object> intent = Map.of(
                "intent", "workout_question",
                "confidence", 0.85,
                "entities", Map.of(
                    "exercise", "squats",
                    "sets", 3
                )
            );
            return ResponseEntity.ok(intent);
        } catch (Exception e) {
            Map<String, String> error = new HashMap<>();
            error.put("error", "Failed to classify intent: " + e.getMessage());
            return ResponseEntity.badRequest().body(error);
        }
    }

    @PostMapping("/extract-entities")
    @Operation(summary = "Extract entities from message")
    public ResponseEntity<?> extractEntities(@RequestBody Map<String, String> request) {
        try {
            String message = request.get("message");
            
            // This would use the ML service to extract entities
            Map<String, Object> entities = Map.of(
                "exercise", "push-ups",
                "sets", 3,
                "reps", 10,
                "goal", "strength"
            );
            return ResponseEntity.ok(entities);
        } catch (Exception e) {
            Map<String, String> error = new HashMap<>();
            error.put("error", "Failed to extract entities: " + e.getMessage());
            return ResponseEntity.badRequest().body(error);
        }
    }
}




