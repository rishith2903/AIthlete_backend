#!/usr/bin/env python3
"""
Simple test to check if Spring Boot backend is running
"""

import requests
import time
import sys

def test_backend():
    base_url = "http://localhost:8080/api"
    
    print("Testing Spring Boot Backend...")
    print(f"Base URL: {base_url}")
    
    # Test endpoints
    endpoints = [
        "/pose/exercises",
        "/workout/exercises", 
        "/auth/health"
    ]
    
    for endpoint in endpoints:
        url = base_url + endpoint
        print(f"\nTesting: {url}")
        
        try:
            response = requests.get(url, timeout=5)
            print(f"Status: {response.status_code}")
            print(f"Response: {response.text[:200]}...")
        except requests.exceptions.ConnectionError:
            print("❌ Connection Error - Server not running")
            return False
        except requests.exceptions.Timeout:
            print("❌ Timeout - Server not responding")
            return False
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
    
    print("\n✅ Backend is running and accessible!")
    return True

if __name__ == "__main__":
    # Wait for server to start
    print("Waiting for server to start...")
    time.sleep(5)
    
    if test_backend():
        sys.exit(0)
    else:
        sys.exit(1)


