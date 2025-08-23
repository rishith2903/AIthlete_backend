package com.fitness.aifitness.entity;

import jakarta.persistence.*;
import java.time.LocalDateTime;

@Entity
@Table(name = "nutrition_plans")
public class NutritionPlan {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @ManyToOne
    @JoinColumn(name = "user_id", nullable = false)
    private User user;
    
    private Integer targetCalories;
    
    private Integer targetProtein; // in grams
    
    private Integer targetCarbs; // in grams
    
    private Integer targetFat; // in grams
    
    private String mealPlan; // JSON string of weekly meal plan
    
    private String dietaryRestrictions; // JSON string of restrictions
    
    private String goal; // weight_loss, muscle_gain, maintenance
    
    @Column(name = "start_date")
    private LocalDateTime startDate;
    
    @Column(name = "end_date")
    private LocalDateTime endDate;
    
    private String status; // active, completed, paused
    
    private String notes;
    
    @Column(name = "created_at")
    private LocalDateTime createdAt;
    
    @Column(name = "updated_at")
    private LocalDateTime updatedAt;
    
    @PrePersist
    protected void onCreate() {
        createdAt = LocalDateTime.now();
        updatedAt = LocalDateTime.now();
    }
    
    @PreUpdate
    protected void onUpdate() {
        updatedAt = LocalDateTime.now();
    }
    
    // Constructors
    public NutritionPlan() {}
    
    public NutritionPlan(User user, Integer targetCalories, String goal) {
        this.user = user;
        this.targetCalories = targetCalories;
        this.goal = goal;
    }
    
    // Getters and Setters
    public Long getId() {
        return id;
    }
    
    public void setId(Long id) {
        this.id = id;
    }
    
    public User getUser() {
        return user;
    }
    
    public void setUser(User user) {
        this.user = user;
    }
    
    public Integer getTargetCalories() {
        return targetCalories;
    }
    
    public void setTargetCalories(Integer targetCalories) {
        this.targetCalories = targetCalories;
    }
    
    public Integer getTargetProtein() {
        return targetProtein;
    }
    
    public void setTargetProtein(Integer targetProtein) {
        this.targetProtein = targetProtein;
    }
    
    public Integer getTargetCarbs() {
        return targetCarbs;
    }
    
    public void setTargetCarbs(Integer targetCarbs) {
        this.targetCarbs = targetCarbs;
    }
    
    public Integer getTargetFat() {
        return targetFat;
    }
    
    public void setTargetFat(Integer targetFat) {
        this.targetFat = targetFat;
    }
    
    public String getMealPlan() {
        return mealPlan;
    }
    
    public void setMealPlan(String mealPlan) {
        this.mealPlan = mealPlan;
    }
    
    public String getDietaryRestrictions() {
        return dietaryRestrictions;
    }
    
    public void setDietaryRestrictions(String dietaryRestrictions) {
        this.dietaryRestrictions = dietaryRestrictions;
    }
    
    public String getGoal() {
        return goal;
    }
    
    public void setGoal(String goal) {
        this.goal = goal;
    }
    
    public LocalDateTime getStartDate() {
        return startDate;
    }
    
    public void setStartDate(LocalDateTime startDate) {
        this.startDate = startDate;
    }
    
    public LocalDateTime getEndDate() {
        return endDate;
    }
    
    public void setEndDate(LocalDateTime endDate) {
        this.endDate = endDate;
    }
    
    public String getStatus() {
        return status;
    }
    
    public void setStatus(String status) {
        this.status = status;
    }
    
    public String getNotes() {
        return notes;
    }
    
    public void setNotes(String notes) {
        this.notes = notes;
    }
    
    public LocalDateTime getCreatedAt() {
        return createdAt;
    }
    
    public void setCreatedAt(LocalDateTime createdAt) {
        this.createdAt = createdAt;
    }
    
    public LocalDateTime getUpdatedAt() {
        return updatedAt;
    }
    
    public void setUpdatedAt(LocalDateTime updatedAt) {
        this.updatedAt = updatedAt;
    }
}




