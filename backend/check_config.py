#!/usr/bin/env python3
"""
Configuration verification script for the Physical AI Textbook RAG Chatbot Backend
"""

import os
import sys
from dotenv import load_dotenv
import requests
import qdrant_client
from openai import OpenAI
import cohere

def check_env_vars():
    """Check if all required environment variables are set"""
    print("🔍 Checking Environment Variables...")

    required_vars = [
        'COHERE_API_KEY',
        'OPENROUTER_API_KEY',
        'QDRANT_URL',
        'JWT_SECRET',
        'DATABASE_URL'
    ]

    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)

    # QDRANT_API_KEY is optional for local development
    if not os.getenv('QDRANT_API_KEY') and 'localhost' not in os.getenv('QDRANT_URL', ''):
        print("⚠️  QDRANT_API_KEY is empty - this is OK for local Qdrant but required for Qdrant Cloud")

    if missing_vars:
        print(f"❌ Missing environment variables: {missing_vars}")
        return False
    else:
        print("✅ All required environment variables are set")
        return True

def check_cohere_connection():
    """Test Cohere API connection"""
    print("\n🔍 Testing Cohere Connection...")

    try:
        cohere_api_key = os.getenv('COHERE_API_KEY')
        cohere_client = cohere.Client(cohere_api_key)

        # Test embedding generation with proper input_type
        response = cohere_client.embed(
            texts=["test"],
            model="embed-english-v3.0",
            input_type="search_document"
        )

        if response and response.embeddings:
            print("✅ Cohere connection successful")
            return True
        else:
            print("❌ Cohere connection failed - no embeddings returned")
            return False

    except Exception as e:
        print(f"❌ Cohere connection failed: {str(e)}")
        return False

def check_openrouter_connection():
    """Test OpenRouter API connection"""
    print("\n🔍 Testing OpenRouter Connection...")

    try:
        openrouter_api_key = os.getenv('OPENROUTER_API_KEY')
        openrouter_model = os.getenv('OPENROUTER_MODEL', 'google/gemini-flash-1.5')

        client = OpenAI(
            api_key=openrouter_api_key,
            base_url="https://openrouter.ai/api/v1",
        )

        # Test chat completion
        response = client.chat.completions.create(
            model=openrouter_model,
            messages=[{"role": "user", "content": "Hello"}],
            max_tokens=10
        )

        if response and response.choices:
            print("✅ OpenRouter connection successful")
            return True
        else:
            print("❌ OpenRouter connection failed - no response returned")
            return False

    except Exception as e:
        print(f"❌ OpenRouter connection failed: {str(e)}")
        return False

def check_qdrant_connection():
    """Test Qdrant connection"""
    print("\n🔍 Testing Qdrant Connection...")

    try:
        qdrant_url = os.getenv('QDRANT_URL')
        qdrant_api_key = os.getenv('QDRANT_API_KEY')

        # Only use API key if it's set and not connecting to localhost
        if qdrant_api_key and qdrant_api_key.strip() and 'localhost' not in qdrant_url:
            client = qdrant_client.QdrantClient(
                url=qdrant_url,
                api_key=qdrant_api_key,
                timeout=10
            )
        else:
            client = qdrant_client.QdrantClient(
                url=qdrant_url,
                timeout=10
            )

        # Test getting collections
        collections = client.get_collections()
        print(f"✅ Qdrant connection successful")
        print(f"   Available collections: {[col.name for col in collections.collections]}")
        return True

    except Exception as e:
        print(f"❌ Qdrant connection failed: {str(e)}")
        print("💡 Hint: Make sure your QDRANT_URL is correct and Qdrant service is running")
        print("💡 For local development: Start Qdrant with 'docker run -p 6333:6333 qdrant/qdrant'")
        return False

def main():
    """Main configuration check function"""
    print("="*60)
    print("Physical AI Textbook Backend - Configuration Verifier")
    print("="*60)

    # Load environment variables
    load_dotenv()

    print("Starting configuration verification...\n")

    # Run all checks
    env_ok = check_env_vars()
    cohere_ok = check_cohere_connection() if env_ok else False
    openrouter_ok = check_openrouter_connection() if env_ok else False
    qdrant_ok = check_qdrant_connection() if env_ok else False

    print("\n" + "="*60)
    print("CONFIGURATION SUMMARY")
    print("="*60)

    print(f"Environment Variables: {'✅ PASS' if env_ok else '❌ FAIL'}")
    print(f"Cohere API: {'✅ PASS' if cohere_ok else '❌ FAIL'}")
    print(f"OpenRouter API: {'✅ PASS' if openrouter_ok else '❌ FAIL'}")
    print(f"Qdrant Connection: {'✅ PASS' if qdrant_ok else '❌ FAIL'}")

    all_good = env_ok and cohere_ok and openrouter_ok and qdrant_ok

    print("\n" + "="*60)
    if all_good:
        print("🎉 All configurations are working properly!")
        print("You can now run the backend server with: python main.py")
    else:
        print("⚠️  Some configurations need attention before running the server.")
        print("Please fix the failed checks above before starting the backend.")
    print("="*60)

    return all_good

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)