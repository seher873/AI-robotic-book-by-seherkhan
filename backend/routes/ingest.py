"""
Document ingestion routes for RAG system
"""
from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel
from typing import Optional, List

from qdrant_client.http import models

from services.rag_service import (
    get_cohere_client,
    get_qdrant_client,
    get_collection_name,
    get_embedding_model
)
from utils.logger import setup_logger

logger = setup_logger("ingest_routes")

router = APIRouter()


class Document(BaseModel):
    id: str
    content: str
    title: Optional[str] = None
    path: Optional[str] = None


@router.post("/ingest")
async def ingest_documents(request: Request, documents: List[Document]):
    """
    Ingest documents into the vector database
    
    Args:
        request: FastAPI request object (for rate limiting)
        documents: List of documents to ingest
        
    Returns:
        Success message with count of ingested documents
    """
    cohere_client = get_cohere_client()
    qdrant = get_qdrant_client()
    
    if cohere_client is None or qdrant is None:
        raise HTTPException(status_code=500, detail="Services not initialized")

    try:
        # Prepare documents for embedding
        texts_to_embed = [doc.content for doc in documents]

        # Generate embeddings using Cohere
        embeddings_response = cohere_client.embed(
            texts=texts_to_embed,
            model=get_embedding_model(),
            input_type="search_document"
        )

        embeddings = embeddings_response.embeddings

        # Prepare points for Qdrant
        points = []
        for i, doc in enumerate(documents):
            points.append(models.PointStruct(
                id=doc.id,
                vector=embeddings[i],
                payload={
                    "content": doc.content,
                    "title": doc.title or "",
                    "path": doc.path or ""
                }
            ))

        # Upsert points to Qdrant
        qdrant.upsert(
            collection_name=get_collection_name(),
            points=points
        )

        logger.info(f"Successfully ingested {len(documents)} documents")
        return {"message": f"Successfully ingested {len(documents)} documents"}

    except Exception as e:
        logger.error(f"Error ingesting documents: {e}")
        raise HTTPException(status_code=500, detail=str(e))
