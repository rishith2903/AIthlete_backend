FROM eclipse-temurin:17-jdk-jammy
WORKDIR /app
COPY pom.xml ./
COPY mvnw ./
COPY .mvn .mvn
COPY src ./src

# Ensure mvnw is executable
RUN chmod +x ./mvnw || true

# Build the application
RUN ./mvnw -q -DskipTests package

# Run stage
FROM eclipse-temurin:17-jre-jammy
WORKDIR /app
COPY --from=0 /app/target/ai-fitness-backend-1.0.0.jar app.jar
ENV SPRING_PROFILES_ACTIVE=docker
EXPOSE 8080
ENTRYPOINT ["java","-jar","/app/app.jar"]
