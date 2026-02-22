"""
RAG Service - Handles embedding generation, vector search, and response generation
"""
import os
import cohere
import qdrant_client
import openai
from dotenv import load_dotenv
from utils.logger import setup_logger

# Load environment variables
load_dotenv()

logger = setup_logger("rag_service")

# Global clients
_cohere_client = None
_qdrant_client = None
_openai_client = None

# Constants
COLLECTION_NAME = os.getenv("QDRANT_COLLECTION_NAME", "seher_robotic_book_netlify_app")
EMBEDDING_MODEL = "embed-english-v3.0"
GENERATION_MODEL = os.getenv("OPENROUTER_MODEL", "google/gemini-flash-1.5")


def initialize_rag_services():
    """Initialize all RAG-related services"""
    global _cohere_client, _qdrant_client, _openai_client

    cohere_key = os.getenv("COHERE_API_KEY")
    openrouter_key = os.getenv("OPENROUTER_API_KEY")
    qdrant_url = os.getenv("QDRANT_URL")
    qdrant_api_key = os.getenv("QDRANT_API_KEY")

    # Initialize Cohere
    if not cohere_key:
        logger.error("COHERE_API_KEY missing")
    else:
        _cohere_client = cohere.Client(cohere_key)
        logger.info("✓ Cohere initialized")

    # Initialize OpenRouter
    if not openrouter_key:
        logger.error("OPENROUTER_API_KEY missing")
    else:
        _openai_client = openai.OpenAI(
            api_key=openrouter_key,
            base_url="https://openrouter.ai/api/v1",
        )
        logger.info("✓ OpenRouter initialized")

    # Initialize Qdrant
    if not qdrant_url:
        logger.error("QDRANT_URL missing")
    elif not qdrant_api_key:
        logger.warning("QDRANT_API_KEY not set")
        _qdrant_client = qdrant_client.QdrantClient(url=qdrant_url)
        logger.info("✓ Qdrant initialized (no API key)")
    else:
        _qdrant_client = qdrant_client.QdrantClient(
            url=qdrant_url,
            api_key=qdrant_api_key
        )
        logger.info("✓ Qdrant initialized")


def get_cohere_client():
    """Get Cohere client instance"""
    return _cohere_client


def get_qdrant_client():
    """Get Qdrant client instance"""
    return _qdrant_client


def get_openai_client():
    """Get OpenAI/OpenRouter client instance"""
    return _openai_client


def get_collection_name():
    """Get Qdrant collection name"""
    return COLLECTION_NAME


def get_embedding_model():
    """Get Cohere embedding model name"""
    return EMBEDDING_MODEL


def get_generation_model():
    """Get LLM generation model name"""
    return GENERATION_MODEL
