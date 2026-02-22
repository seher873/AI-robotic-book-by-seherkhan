"""
FastAPI Backend for Physical AI & Humanoid Robotics Textbook
Provides RAG chatbot and authentication APIs
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os
import sys
import logging

# Add backend directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# Import rate limiter
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

# Import services
from services.rag_service import initialize_rag_services, get_cohere_client, get_qdrant_client, get_openai_client
from utils.logger import setup_logger

# Import routes
from routes.chat import router as chat_router
from routes.ingest import router as ingest_router
from auth.main import init_auth_routes

# Setup logging
logger = setup_logger()

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize services on startup"""
    try:
        initialize_rag_services()
        logger.info("✓ All services initialized successfully")
    except Exception as e:
        logger.error(f"✗ Failed to initialize services: {e}")
        raise
    yield
    # Cleanup can be added here if needed

# Initialize FastAPI app
app = FastAPI(
    title="Physical AI Textbook Backend",
    description="RAG chatbot and authentication API for Physical AI & Humanoid Robotics textbook",
    version="1.0.0",
    lifespan=lifespan
)

# Add rate limiter to app state
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(chat_router, prefix="/api", tags=["Chatbot"])
app.include_router(ingest_router, prefix="/api", tags=["Ingestion"])
init_auth_routes(app)


@app.get("/")
async def read_root():
    """Root endpoint with API information"""
    return {
        "message": "Physical AI Textbook Backend API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "chat": "/api/chat",
            "ingest": "/api/ingest",
            "auth": "/api/auth"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint with service dependency status"""
    cohere_client = get_cohere_client()
    qdrant_client = get_qdrant_client()
    openai_client = get_openai_client()
    
    services_status = {
        "cohere": "up" if cohere_client is not None else "down",
        "qdrant": "up" if qdrant_client is not None else "down",
        "openrouter": "up" if openai_client is not None else "down"
    }

    all_up = all(status == "up" for status in services_status.values())

    return {
        "status": "healthy" if all_up else "unhealthy",
        "service": "Physical AI Textbook Backend",
        "version": "1.0.0",
        "services": services_status
    }


@app.get("/users/{user_id}/tasks")
async def get_user_tasks(user_id: str, limit: int = 100, offset: int = 0):
    """Get tasks for a specific user"""
    return {
        "tasks": [],
        "total": 0,
        "limit": limit,
        "offset": offset
    }


@app.get("/users/{user_id}/tasks/{task_id}")
async def get_user_task(user_id: str, task_id: str):
    """Get a specific task for a user"""
    return {"detail": "Task not found"}


@app.post("/users/{user_id}/tasks")
async def create_user_task(user_id: str, request: Request):
    """Create a task for a user"""
    return {"detail": "Task created successfully"}


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 7860))
    uvicorn.run(app, host="0.0.0.0", port=port)
