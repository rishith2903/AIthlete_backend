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
@RequestMapping("/pose")
@Tag(name = "Pose Analysis", description = "Pose estimation and form checking endpoints")
public class PoseController {

    @Autowired
    private MlServiceIntegration mlServiceIntegration;

    @PostMapping("/analyze")
    @Operation(summary = "Analyze exercise form from image/video")
    public ResponseEntity<?> analyzePose(@RequestBody Map<String, String> request) {
        try {
            String imageData = request.get("image_data");
            String exerciseType = request.get("exercise_type");

            Map<String, Object> analysis = mlServiceIntegration.analyzePose(imageData, exerciseType);
            return ResponseEntity.ok(analysis);
        } catch (Exception e) {
            Map<String, String> error = new HashMap<>();
            error.put("error", "Failed to analyze pose: " + e.getMessage());
            return ResponseEntity.badRequest().body(error);
        }
    }

    @PostMapping("/detect-exercise")
    @Operation(summary = "Detect exercise type from pose")
    public ResponseEntity<?> detectExercise(@RequestBody Map<String, String> request) {
        try {
            String imageData = request.get("image_data");
            
            // This would use the ML service to detect exercise type
            Map<String, Object> detection = Map.of(
                "exercise_type", "squat",
                "confidence", 0.92,
                "alternative_exercises", java.util.Arrays.asList("lunge", "deadlift")
            );
            return ResponseEntity.ok(detection);
        } catch (Exception e) {
            Map<String, String> error = new HashMap<>();
            error.put("error", "Failed to detect exercise: " + e.getMessage());
            return ResponseEntity.badRequest().body(error);
        }
    }

    @PostMapping("/check-form")
    @Operation(summary = "Check exercise form quality")
    public ResponseEntity<?> checkForm(@RequestBody Map<String, Object> request) {
        try {
            String exerciseType = (String) request.get("exercise_type");
            Map<String, Object> angles = (Map<String, Object>) request.get("angles");
            
            // This would use the ML service to check form
            Map<String, Object> formCheck = Map.of(
                "form_quality", "good",
                "score", 85,
                "feedback", java.util.Arrays.asList(
                    "Keep your back straight",
                    "Knees should not go past toes"
                ),
                "angles", angles
            );
            return ResponseEntity.ok(formCheck);
        } catch (Exception e) {
            Map<String, String> error = new HashMap<>();
            error.put("error", "Failed to check form: " + e.getMessage());
            return ResponseEntity.badRequest().body(error);
        }
    }

    @GetMapping("/exercises")
    @Operation(summary = "Get supported exercises for pose analysis")
    public ResponseEntity<?> getSupportedExercises() {
        try {
            Map<String, Object> exercises = Map.of(
                "exercises", java.util.Arrays.asList(
                    "squat", "push-up", "deadlift", "lunge", "plank",
                    "pull-up", "burpee", "mountain_climber", "jumping_jack"
                )
            );
            return ResponseEntity.ok(exercises);
        } catch (Exception e) {
            Map<String, String> error = new HashMap<>();
            error.put("error", "Failed to fetch exercises: " + e.getMessage());
            return ResponseEntity.badRequest().body(error);
        }
    }
}




