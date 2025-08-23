package com.fitness.aifitness.entity;

import jakarta.persistence.*;
import java.time.LocalDateTime;

@Entity
@Table(name = "progress")
public class Progress {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @ManyToOne
    @JoinColumn(name = "user_id", nullable = false)
    private User user;
    
    private Double weight; // current weight in kg
    
    private Double bodyFatPercentage;
    
    private Double muscleMass; // in kg
    
    private String measurements; // JSON string of body measurements
    
    private String progressPhotos; // URLs to progress photos
    
    private String notes;
    
    @Column(name = "recorded_date")
    private LocalDateTime recordedDate;
    
    @Column(name = "created_at")
    private LocalDateTime createdAt;
    
    @PrePersist
    protected void onCreate() {
        createdAt = LocalDateTime.now();
        if (recordedDate == null) {
            recordedDate = LocalDateTime.now();
        }
    }
    
    // Constructors
    public Progress() {}
    
    public Progress(User user, Double weight) {
        this.user = user;
        this.weight = weight;
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
    
    public Double getWeight() {
        return weight;
    }
    
    public void setWeight(Double weight) {
        this.weight = weight;
    }
    
    public Double getBodyFatPercentage() {
        return bodyFatPercentage;
    }
    
    public void setBodyFatPercentage(Double bodyFatPercentage) {
        this.bodyFatPercentage = bodyFatPercentage;
    }
    
    public Double getMuscleMass() {
        return muscleMass;
    }
    
    public void setMuscleMass(Double muscleMass) {
        this.muscleMass = muscleMass;
    }
    
    public String getMeasurements() {
        return measurements;
    }
    
    public void setMeasurements(String measurements) {
        this.measurements = measurements;
    }
    
    public String getProgressPhotos() {
        return progressPhotos;
    }
    
    public void setProgressPhotos(String progressPhotos) {
        this.progressPhotos = progressPhotos;
    }
    
    public String getNotes() {
        return notes;
    }
    
    public void setNotes(String notes) {
        this.notes = notes;
    }
    
    public LocalDateTime getRecordedDate() {
        return recordedDate;
    }
    
    public void setRecordedDate(LocalDateTime recordedDate) {
        this.recordedDate = recordedDate;
    }
    
    public LocalDateTime getCreatedAt() {
        return createdAt;
    }
    
    public void setCreatedAt(LocalDateTime createdAt) {
        this.createdAt = createdAt;
    }
}




