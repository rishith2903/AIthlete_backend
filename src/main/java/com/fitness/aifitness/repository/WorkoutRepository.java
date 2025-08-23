package com.fitness.aifitness.repository;

import com.fitness.aifitness.entity.Workout;
import com.fitness.aifitness.entity.User;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.time.LocalDateTime;
import java.util.List;

@Repository
public interface WorkoutRepository extends JpaRepository<Workout, Long> {
    
    List<Workout> findByUserOrderByScheduledDateDesc(User user);
    
    List<Workout> findByUserAndStatus(User user, String status);
    
    List<Workout> findByUserAndScheduledDateBetween(User user, LocalDateTime startDate, LocalDateTime endDate);
    
    List<Workout> findByUserAndWorkoutType(User user, String workoutType);
}




