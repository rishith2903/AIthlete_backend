package com.fitness.aifitness.controller;

import com.fitness.aifitness.service.MlServiceIntegration;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.Map;
import java.util.HashMap;

@RestController
@RequestMapping("/workout")
@Tag(name = "Workout", description = "Workout management endpoints")
public class WorkoutController {

    @Autowired
    private MlServiceIntegration mlServiceIntegration;

    @PostMapping("/generate-plan")
    @Operation(summary = "Generate personalized workout plan")
    public ResponseEntity<?> generateWorkoutPlan(@RequestBody Map<String, Object> userProfile) {
        try {
            Map<String, Object> workoutPlan = mlServiceIntegration.getWorkoutPlan(userProfile);
            return ResponseEntity.ok(workoutPlan);
        } catch (Exception e) {
            Map<String, String> error = new HashMap<>();
            error.put("error", "Failed to generate workout plan: " + e.getMessage());
            return ResponseEntity.badRequest().body(error);
        }
    }

    @GetMapping("/exercises")
    @Operation(summary = "Get available exercises")
    public ResponseEntity<?> getAvailableExercises() {
        try {
            // This would typically fetch from a database or ML service
            Map<String, Object> exercises = Map.of(
                "exercises", java.util.Arrays.asList(
                    "Squats", "Push-ups", "Pull-ups", "Deadlifts", "Bench Press",
                    "Lunges", "Planks", "Burpees", "Mountain Climbers", "Jumping Jacks"
                )
            );
            return ResponseEntity.ok(exercises);
        } catch (Exception e) {
            Map<String, String> error = new HashMap<>();
            error.put("error", "Failed to fetch exercises: " + e.getMessage());
            return ResponseEntity.badRequest().body(error);
        }
    }

    @PostMapping("/assess-level")
    @Operation(summary = "Assess user fitness level")
    public ResponseEntity<?> assessFitnessLevel(@RequestBody Map<String, Object> userProfile) {
        try {
            // This would use the ML service to assess fitness level
            Map<String, Object> assessment = Map.of(
                "fitness_level", "intermediate",
                "confidence", 0.85,
                "recommendations", java.util.Arrays.asList(
                    "Focus on progressive overload",
                    "Include both strength and cardio",
                    "Rest 48-72 hours between muscle groups"
                )
            );
            return ResponseEntity.ok(assessment);
        } catch (Exception e) {
            Map<String, String> error = new HashMap<>();
            error.put("error", "Failed to assess fitness level: " + e.getMessage());
            return ResponseEntity.badRequest().body(error);
        }
    }
}




