package com.fitness.aifitness.repository;

import com.fitness.aifitness.entity.ChatbotConversation;
import com.fitness.aifitness.entity.User;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface ChatbotConversationRepository extends JpaRepository<ChatbotConversation, Long> {
    
    List<ChatbotConversation> findByUserOrderByCreatedAtDesc(User user);
    
    List<ChatbotConversation> findByUserAndSessionIdOrderByCreatedAtAsc(User user, String sessionId);
    
    List<ChatbotConversation> findByUserAndIntent(User user, String intent);
}




