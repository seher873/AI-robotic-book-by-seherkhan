"""
Test script for FastAPI Backend
Tests health, chat, and auth endpoints
"""
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

# Backend URL (change based on deployment)
BASE_URL = os.getenv("BACKEND_URL", "http://localhost:7860")

print(f"Testing backend at: {BASE_URL}\n")

# Test 1: Health Check
print("=" * 50)
print("TEST 1: Health Check")
print("=" * 50)
try:
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
except Exception as e:
    print(f"Error: {e}")

# Test 2: Root Endpoint
print("\n" + "=" * 50)
print("TEST 2: Root Endpoint")
print("=" * 50)
try:
    response = requests.get(f"{BASE_URL}/")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
except Exception as e:
    print(f"Error: {e}")

# Test 3: Chat Endpoint
print("\n" + "=" * 50)
print("TEST 3: Chat Endpoint")
print("=" * 50)
try:
    chat_data = {
        "query": "What is Physical AI?",
        "max_results": 3
    }
    response = requests.post(
        f"{BASE_URL}/api/chat",
        json=chat_data,
        headers={"Content-Type": "application/json"}
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"Query: {result.get('query')}")
        print(f"Response: {result.get('response')[:200]}...")
        print(f"Sources: {len(result.get('sources', []))} found")
    else:
        print(f"Error: {response.text}")
except Exception as e:
    print(f"Error: {e}")

# Test 4: Auth Signup
print("\n" + "=" * 50)
print("TEST 4: Auth Signup")
print("=" * 50)
try:
    signup_data = {
        "email": "test@example.com",
        "password": "test123",
        "name": "Test User"
    }
    response = requests.post(
        f"{BASE_URL}/auth/signup",
        json=signup_data,
        headers={"Content-Type": "application/json"}
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"User created: {result.get('user', {}).get('email')}")
        print(f"Token: {result.get('access_token')[:50]}...")
    else:
        print(f"Error: {response.text}")
except Exception as e:
    print(f"Error: {e}")

# Test 5: Auth Signin
print("\n" + "=" * 50)
print("TEST 5: Auth Signin")
print("=" * 50)
try:
    signin_data = {
        "email": "test@example.com",
        "password": "test123"
    }
    response = requests.post(
        f"{BASE_URL}/auth/signin",
        json=signin_data,
        headers={"Content-Type": "application/json"}
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"Signed in: {result.get('user', {}).get('email')}")
        print(f"Token: {result.get('access_token')[:50]}...")
    else:
        print(f"Error: {response.text}")
except Exception as e:
    print(f"Error: {e}")

print("\n" + "=" * 50)
print("All tests completed!")
print("=" * 50)
