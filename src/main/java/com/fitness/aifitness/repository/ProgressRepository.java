package com.fitness.aifitness.repository;

import com.fitness.aifitness.entity.Progress;
import com.fitness.aifitness.entity.User;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.time.LocalDateTime;
import java.util.List;

@Repository
public interface ProgressRepository extends JpaRepository<Progress, Long> {
    
    List<Progress> findByUserOrderByRecordedDateDesc(User user);
    
    List<Progress> findByUserAndRecordedDateBetween(User user, LocalDateTime startDate, LocalDateTime endDate);
    
    Progress findTopByUserOrderByRecordedDateDesc(User user);
}




