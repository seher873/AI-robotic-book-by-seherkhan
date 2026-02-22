"""
Chat routes for RAG chatbot
"""
from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any
import os

from services.rag_service import (
    get_cohere_client,
    get_qdrant_client,
    get_openai_client,
    get_collection_name,
    get_embedding_model
)
from utils.logger import setup_logger

logger = setup_logger("chat_routes")

router = APIRouter()


class ChatRequest(BaseModel):
    query: str
    max_results: Optional[int] = 5


class ChatResponse(BaseModel):
    query: str
    response: str
    sources: list[Dict[str, Any]]


@router.post("/chat", response_model=ChatResponse)
async def chat(request: Request, chat_request: ChatRequest):
    """
    Chat with the RAG-powered textbook assistant
    
    Args:
        request: FastAPI request object (for rate limiting)
        chat_request: Chat request with query and max_results
        
    Returns:
        ChatResponse with answer and sources
    """
    cohere_client = get_cohere_client()
    qdrant = get_qdrant_client()
    openai_client = get_openai_client()
    
    if cohere_client is None or qdrant is None or openai_client is None:
        raise HTTPException(status_code=500, detail="Services not initialized")

    try:
        # Generate embedding for the query
        query_response = cohere_client.embed(
            texts=[chat_request.query],
            model=get_embedding_model(),
            input_type="search_query"
        )
        query_embedding = query_response.embeddings[0]

        # Search for relevant documents in Qdrant
        try:
            # Try the newer search_points method first
            search_results = qdrant.search_points(
                collection_name=get_collection_name(),
                vector=query_embedding,
                limit=chat_request.max_results,
                with_payload=True
            )
        except AttributeError:
            # Fall back to the traditional search method
            search_results = qdrant.search(
                collection_name=get_collection_name(),
                query_vector=query_embedding,
                limit=chat_request.max_results,
                with_payload=True
            )

        # Extract content from search results
        relevant_contents = []
        sources = []

        for result in search_results:
            if hasattr(result, 'payload'):
                # Newer Qdrant client format (ScoredPoint)
                content = result.payload.get("content", "")
                sources.append({
                    "id": result.id,
                    "title": result.payload.get("title", "Unknown"),
                    "path": result.payload.get("path", "Unknown"),
                    "score": result.score
                })
            else:
                # Older format or dict format
                content = result.get('payload', {}).get("content", "")
                sources.append({
                    "id": result.get('id', ''),
                    "title": result.get('payload', {}).get("title", "Unknown"),
                    "path": result.get('payload', {}).get("path", "Unknown"),
                    "score": result.get('score', 0.0)
                })
            relevant_contents.append(content)

        # If no relevant content found, return appropriate response
        if not relevant_contents:
            return ChatResponse(
                query=chat_request.query,
                response="I'm sorry, I couldn't find relevant information in the textbook to answer your question.",
                sources=[]
            )

        # Combine context for generation
        context = "\n\n".join(relevant_contents)

        # Create prompt for response generation
        prompt = f"""
You are an expert AI professor specialized in the "Physical AI & Humanoid Robotics" textbook.
Use the following retrieved context to answer the student's question accurately.

Context:
{context}

Question: {chat_request.query}

Guidelines:
- Answer directly based on the context provided.
- If the exact answer isn't in the context but relates to Physical AI topics, provide a helpful general answer.
- Only say "I couldn't find this in the textbook" if the question is completely unrelated to Robotics or Physical AI.

Answer:
"""

        # Generate response using OpenRouter
        response = openai_client.chat.completions.create(
            model=get_generation_model(),
            messages=[
                {"role": "system", "content": "You are an AI assistant for the Physical AI & Humanoid Robotics textbook. Answer questions based on the provided context."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )

        # Extract the response text
        response_text = response.choices[0].message.content

        # Check if response indicates information is not in the book
        if "Not found in the book" in response_text or response_text.strip() == "":
            return ChatResponse(
                query=chat_request.query,
                response="I'm sorry, I couldn't find this information in the textbook.",
                sources=[]
            )

        return ChatResponse(
            query=chat_request.query,
            response=response_text,
            sources=sources
        )

    except Exception as e:
        logger.error(f"Error processing chat request: {e}")
        raise HTTPException(status_code=500, detail=str(e))
