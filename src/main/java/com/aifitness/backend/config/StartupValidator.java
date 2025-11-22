package com.aifitness.backend.config;

import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.CommandLineRunner;
import org.springframework.core.env.Environment;
import org.springframework.stereotype.Component;

import java.util.Arrays;

@Component
@Slf4j
public class StartupValidator implements CommandLineRunner {

    private final Environment environment;

    @Value("${spring.data.mongodb.uri:}")
    private String mongoUri;

    public StartupValidator(Environment environment) {
        this.environment = environment;
    }

    @Override
    public void run(String... args) throws Exception {
        String[] activeProfiles = environment.getActiveProfiles();
        boolean isProduction = Arrays.asList(activeProfiles).contains("production");

        if (isProduction) {
            log.info("Running in PRODUCTION mode. Validating configuration...");

            if (mongoUri == null || mongoUri.isEmpty() || mongoUri.contains("localhost") || mongoUri.contains("127.0.0.1")) {
                log.error("CRITICAL CONFIGURATION ERROR: Invalid MongoDB URI for production!");
                log.error("Current URI: " + (mongoUri == null || mongoUri.isEmpty() ? "[EMPTY]" : mongoUri));
                log.error("In production, you must provide a valid MongoDB connection string via the MONGODB_URI environment variable.");
                log.error("If you are deploying on Render, ensure you are using a Blueprint (render.yaml) OR have manually added MONGODB_URI to the Environment Variables.");
                
                // We want to fail fast, but Spring might have already failed to connect. 
                // This log ensures the user sees WHY it failed if the connection timeout hasn't happened yet.
                // Throwing an exception here ensures we stop if by some miracle we connected to a local mongo (unlikely in cloud).
                throw new RuntimeException("Production deployment failed: Missing or invalid MONGODB_URI environment variable.");
            }
            
            log.info("Configuration validation passed.");
        } else {
            log.info("Running in DEV/TEST mode. Skipping production validation.");
        }
    }
}
