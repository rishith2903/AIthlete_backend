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
@RequestMapping("/nutrition")
@Tag(name = "Nutrition", description = "Nutrition management endpoints")
public class NutritionController {

    @Autowired
    private MlServiceIntegration mlServiceIntegration;

    @PostMapping("/generate-meal-plan")
    @Operation(summary = "Generate personalized meal plan")
    public ResponseEntity<?> generateMealPlan(@RequestBody Map<String, Object> userProfile) {
        try {
            Map<String, Object> mealPlan = mlServiceIntegration.getNutritionPlan(userProfile);
            return ResponseEntity.ok(mealPlan);
        } catch (Exception e) {
            Map<String, String> error = new HashMap<>();
            error.put("error", "Failed to generate meal plan: " + e.getMessage());
            return ResponseEntity.badRequest().body(error);
        }
    }

    @PostMapping("/calculate-bmr")
    @Operation(summary = "Calculate Basal Metabolic Rate")
    public ResponseEntity<?> calculateBMR(@RequestBody Map<String, Object> userData) {
        try {
            // This would use the ML service to calculate BMR
            Map<String, Object> bmrData = Map.of(
                "bmr", 1800,
                "tdee", 2200,
                "recommendations", Map.of(
                    "weight_loss", 1700,
                    "maintenance", 2200,
                    "muscle_gain", 2500
                )
            );
            return ResponseEntity.ok(bmrData);
        } catch (Exception e) {
            Map<String, String> error = new HashMap<>();
            error.put("error", "Failed to calculate BMR: " + e.getMessage());
            return ResponseEntity.badRequest().body(error);
        }
    }

    @PostMapping("/calculate-macros")
    @Operation(summary = "Calculate macronutrient distribution")
    public ResponseEntity<?> calculateMacros(@RequestBody Map<String, Object> request) {
        try {
            // This would use the ML service to calculate macros
            Map<String, Object> macros = Map.of(
                "protein", 150,
                "carbs", 200,
                "fat", 67,
                "calories", 2000,
                "goal", request.get("goal")
            );
            return ResponseEntity.ok(macros);
        } catch (Exception e) {
            Map<String, String> error = new HashMap<>();
            error.put("error", "Failed to calculate macros: " + e.getMessage());
            return ResponseEntity.badRequest().body(error);
        }
    }
}




