package com.fitness.aifitness.controller;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.core.ParameterizedTypeReference;
import org.springframework.http.HttpMethod;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.client.RestTemplate;

import java.util.Map;

@RestController
@RequestMapping("/api/integration")
public class MlProxyController {

    private final RestTemplate restTemplate;

    @Value("${ml.api.base:http://host.docker.internal:5000}")
    private String mlApiBase;

    public MlProxyController(RestTemplate restTemplate) {
        this.restTemplate = restTemplate;
    }

    @GetMapping("/ml-health")
    public ResponseEntity<Map<String, Object>> mlHealth() {
        String url = mlApiBase + "/health";
        ResponseEntity<Map<String, Object>> resp = restTemplate.exchange(
                url,
                HttpMethod.GET,
                null,
                new ParameterizedTypeReference<Map<String, Object>>() {}
        );
        return ResponseEntity.status(resp.getStatusCode()).body(resp.getBody());
    }
}
