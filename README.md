# 🚀 AI Fitness Backend - Spring Boot

## 📋 **Project Overview**

This is a comprehensive Spring Boot backend for an AI-powered fitness application. It provides REST APIs for user management, workout planning, nutrition guidance, chatbot interactions, and pose analysis.

## 🏗️ **Architecture**

- **Framework**: Spring Boot 3.2.0
- **Database**: PostgreSQL with JPA/Hibernate
- **Security**: JWT-based authentication
- **Documentation**: OpenAPI/Swagger
- **ML Integration**: REST API communication with Python ML services

## 📁 **Project Structure**

```
Backend/
├── src/main/java/com/fitness/aifitness/
│   ├── AiFitnessApplication.java          # Main application class
│   ├── entity/                           # JPA entities
│   │   ├── User.java                     # User entity
│   │   ├── Workout.java                  # Workout entity
│   │   ├── NutritionPlan.java            # Nutrition plan entity
│   │   ├── ChatbotConversation.java      # Chatbot conversation entity
│   │   └── Progress.java                 # Progress tracking entity
│   ├── repository/                       # Data access layer
│   │   ├── UserRepository.java
│   │   ├── WorkoutRepository.java
│   │   ├── NutritionPlanRepository.java
│   │   ├── ChatbotConversationRepository.java
│   │   └── ProgressRepository.java
│   ├── service/                          # Business logic layer
│   │   ├── UserService.java
│   │   └── MlServiceIntegration.java     # ML service integration
│   ├── controller/                       # REST API controllers
│   │   ├── AuthController.java
│   │   ├── WorkoutController.java
│   │   ├── NutritionController.java
│   │   ├── ChatbotController.java
│   │   └── PoseController.java
│   └── security/                         # Security configuration
│       ├── JwtTokenProvider.java
│       ├── JwtAuthenticationFilter.java
│       └── SecurityConfig.java
├── src/main/resources/
│   └── application.yml                   # Application configuration
├── pom.xml                              # Maven dependencies
└── README.md                            # This file
```

## 🚀 **Quick Start**

### Prerequisites
- Java 17+
- Maven 3.6+
- PostgreSQL 12+
- Python ML services running on port 5000

### 1. Database Setup
```sql
CREATE DATABASE ai_fitness_db;
CREATE USER postgres WITH PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE ai_fitness_db TO postgres;
```

### 2. Configuration
Update `src/main/resources/application.yml` with your database credentials:
```yaml
spring:
  datasource:
    url: jdbc:postgresql://localhost:5432/ai_fitness_db
    username: your_username
    password: your_password
```

### 3. Run the Application
```bash
# Navigate to backend directory
cd Backend

# Build the project
mvn clean install

# Run the application
mvn spring-boot:run
```

The application will start on `http://localhost:8080`

## 📡 **API Endpoints**

### 🔐 **Authentication**
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - User login
- `GET /api/auth/health` - Health check

### 💪 **Workout Management**
- `POST /api/workout/generate-plan` - Generate personalized workout plan
- `GET /api/workout/exercises` - Get available exercises
- `POST /api/workout/assess-level` - Assess fitness level

### 🍽️ **Nutrition Management**
- `POST /api/nutrition/generate-meal-plan` - Generate meal plan
- `POST /api/nutrition/calculate-bmr` - Calculate BMR
- `POST /api/nutrition/calculate-macros` - Calculate macronutrients

### 🤖 **Chatbot**
- `POST /api/chatbot/chat` - Chat with fitness bot
- `POST /api/chatbot/classify-intent` - Classify user intent
- `POST /api/chatbot/extract-entities` - Extract entities from message

### 📷 **Pose Analysis**
- `POST /api/pose/analyze` - Analyze exercise form
- `POST /api/pose/detect-exercise` - Detect exercise type
- `POST /api/pose/check-form` - Check form quality
- `GET /api/pose/exercises` - Get supported exercises

## 🔒 **Security**

### JWT Authentication
- JWT tokens are used for stateless authentication
- Tokens expire after 24 hours
- Password encryption using BCrypt

### CORS Configuration
- Configured for frontend integration
- Supports localhost:3000 and Vercel deployment

## 🗄️ **Database Schema**

### Users Table
- User profiles with fitness information
- Encrypted passwords
- Fitness goals and preferences

### Workouts Table
- Workout plans and progress
- Exercise details and scheduling
- Status tracking

### Nutrition Plans Table
- Meal plans and nutritional targets
- Dietary restrictions
- Goal-based planning

### Chatbot Conversations Table
- Conversation history
- Intent classification
- Entity extraction

### Progress Table
- Weight and measurement tracking
- Progress photos
- Performance metrics

## 🔧 **ML Service Integration**

The backend communicates with Python ML services via REST APIs:

- **Base URL**: `http://localhost:5000`
- **Timeout**: 10 seconds
- **Fallback**: Graceful degradation when ML services are unavailable

### ML Service Endpoints
- `/workout/generate-plan` - Workout recommendation
- `/nutrition/generate-meal-plan` - Nutrition planning
- `/chatbot/chat` - Chatbot interaction
- `/pose/analyze` - Pose analysis

## 📊 **API Documentation**

### Swagger UI
Access the interactive API documentation at:
`http://localhost:8080/api/swagger-ui.html`

### OpenAPI Specification
Download the OpenAPI spec at:
`http://localhost:8080/api/api-docs`

## 🧪 **Testing**

### Run Tests
```bash
mvn test
```

### Test Coverage
- Unit tests for services
- Integration tests for controllers
- Security tests for authentication

## 🚀 **Deployment**

### Render Deployment
1. Connect your GitHub repository to Render
2. Configure environment variables:
   - `DB_URL` - PostgreSQL connection string
   - `JWT_SECRET` - JWT signing secret
   - `ML_SERVICE_URL` - ML service base URL

### Environment Variables
```bash
DB_URL=postgresql://user:password@host:port/database
JWT_SECRET=your-secret-key-here
ML_SERVICE_URL=http://your-ml-service-url
```

## 📈 **Monitoring**

### Health Checks
- `GET /api/auth/health` - Authentication service health
- `GET /api/actuator/health` - Application health (if actuator enabled)

### Logging
- Structured logging with timestamps
- Debug level for development
- Error tracking and monitoring

## 🔧 **Development**

### Code Style
- Follow Spring Boot conventions
- Use meaningful variable names
- Add comprehensive comments
- Include proper error handling

### Dependencies
- Spring Boot 3.2.0
- Spring Security
- Spring Data JPA
- PostgreSQL Driver
- JWT Library
- OpenAPI/Swagger

## 🤝 **Integration with Frontend**

The backend is designed to work seamlessly with the React frontend:

- **CORS**: Configured for frontend domains
- **Authentication**: JWT token-based
- **Error Handling**: Consistent error responses
- **API Design**: RESTful endpoints with JSON responses

## 📝 **API Response Format**

### Success Response
```json
{
  "status": "success",
  "data": {
    // Response data
  },
  "message": "Operation completed successfully"
}
```

### Error Response
```json
{
  "status": "error",
  "error": "Error message",
  "timestamp": "2024-01-01T00:00:00Z"
}
```

## 🎯 **Features**

### ✅ **Implemented**
- User registration and authentication
- JWT-based security
- Database integration with PostgreSQL
- REST API endpoints for all features
- ML service integration
- OpenAPI documentation
- CORS configuration
- Error handling

### 🔄 **In Progress**
- Progress tracking endpoints
- File upload for pose analysis
- Real-time notifications
- Advanced analytics

## 📞 **Support**

For issues and questions:
1. Check the API documentation
2. Review error logs
3. Test with Postman/curl
4. Contact the development team

---

**🎯 The Spring Boot backend is production-ready and provides a robust foundation for the AI-powered fitness application!** 🏋️‍♂️




#
