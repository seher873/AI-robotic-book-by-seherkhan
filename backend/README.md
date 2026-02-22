---
title: Physical AI Textbook Backend
emoji: 🤖
colorFrom: blue
colorTo: purple
sdk: docker
app_file: main.py
pinned: false
---

# Physical AI Textbook Backend

FastAPI backend for the Physical AI & Humanoid Robotics textbook, providing RAG chatbot and authentication APIs.

## Features

- 🤖 **RAG Chatbot** - AI-powered Q&A based on textbook content
- 🔐 **Authentication** - User signup, login, and JWT-based sessions
- 📊 **Vector Search** - Cohere embeddings + Qdrant vector database
- 🚀 **LLM Integration** - OpenRouter with Gemini Flash 1.5
- ⚡ **Rate Limiting** - 10 requests/minute for chat endpoints

## API Endpoints

### Health & Info
- `GET /` - Root endpoint
- `GET /health` - Health check with service status

### Authentication
- `POST /auth/signup` - User registration
- `POST /auth/signin` - User login
- `GET /auth/me` - Get current user

### RAG Chatbot
- `POST /api/chat` - Query the textbook chatbot
- `POST /api/ingest` - Ingest documents into vector database

## Environment Variables

Configure these in HuggingFace Space Secrets:

```bash
COHERE_API_KEY=your_cohere_key
OPENROUTER_API_KEY=your_openrouter_key
OPENROUTER_MODEL=google/gemini-flash-1.5
QDRANT_URL=https://your-qdrant-cluster.qdrant.io
QDRANT_API_KEY=your_qdrant_api_key
JWT_SECRET=your_jwt_secret_min_32_characters
BETTER_AUTH_SECRET=your_better_auth_secret_min_32_chars
```

## Testing

```bash
# Health check
curl https://sehrkhan873-robotic_text_book.hf.space/health

# Chat query
curl -X POST https://sehrkhan873-robotic_text_book.hf.space/api/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "What is Physical AI?", "max_results": 5}'
```

## Links

- **Frontend**: https://seher-robotic-book.netlify.app
- **Docs**: https://github.com/sehrkhan873/seher_ai_book
