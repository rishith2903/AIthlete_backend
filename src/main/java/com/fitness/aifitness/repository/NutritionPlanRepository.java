package com.fitness.aifitness.repository;

import com.fitness.aifitness.entity.NutritionPlan;
import com.fitness.aifitness.entity.User;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
public interface NutritionPlanRepository extends JpaRepository<NutritionPlan, Long> {
    
    List<NutritionPlan> findByUserOrderByCreatedAtDesc(User user);
    
    Optional<NutritionPlan> findByUserAndStatus(User user, String status);
    
    List<NutritionPlan> findByUserAndGoal(User user, String goal);
}




