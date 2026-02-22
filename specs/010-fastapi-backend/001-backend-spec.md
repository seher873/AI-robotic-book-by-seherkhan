# FastAPI Backend for Physical AI Textbook

## Overview
Deploy a FastAPI backend to HuggingFace Spaces (`sehrkhan873/robotic_text_book`) that provides RAG chatbot and authentication APIs matching the frontend's `/api/*` proxy configuration.

**Important**: The existing Gradio chatbot at `https://sehrkhan873-text-book.hf.space` will remain running unchanged. This new backend will be deployed to a **different space** (`https://sehrkhan873/robotic_text_book`).

---

## Architecture

```
┌─────────────────┐     ┌──────────────────────┐     ┌─────────────────────────┐
│   Frontend      │     │   New HF Space       │     │   External Services     │
│   (Docusaurus)  │────▶│   (FastAPI Backend)  │────▶│   - Cohere (Embedding)  │
│   netlify.app   │     │   robotic_text_book  │     │   - OpenRouter (Gemini) │
│                 │     │                      │     │   - Qdrant (Vector DB)  │
└─────────────────┘     └──────────────────────┘     └─────────────────────────┘
       │                        │
       │ /api/* proxy           │ Port 7860 (HF Spaces)
       ▼                        ▼
```

---

## Backend Structure

```
backend/
├── main.py                 # FastAPI application (root routes + health)
├── Dockerfile              # Docker config for HF Spaces
├── requirements.txt        # Python dependencies
├── .dockerignore          # Docker ignore rules
├── .env.example           # Example environment variables
│
├── auth/                  # Authentication module
│   ├── __init__.py
│   ├── main.py            # Auth routes (/auth/signup, /auth/signin, /auth/me)
│   ├── models.py          # SQLAlchemy database models
│   ├── schemas.py         # Pydantic schemas
│   ├── services.py        # Business logic
│   ├── utils.py           # JWT & password utilities
│   ├── config.py          # Auth configuration
│   ├── database.py        # Database connection (SQLite for HF Spaces)
│   └── dependencies.py    # FastAPI dependencies
│
├── routes/                # API routes
│   ├── __init__.py
│   ├── chat.py            # RAG chatbot endpoints (/chat)
│   └── ingest.py          # Document ingestion endpoints (/ingest)
│
├── services/              # Business logic
│   ├── __init__.py
│   ├── rag_service.py     # RAG pipeline (embed → search → generate)
│   └── qdrant_service.py  # Vector database operations
│
├── utils/                 # Utilities
│   ├── __init__.py
│   └── logger.py          # Logging configuration
│
└── scripts/
    ├── init_db.py         # Initialize database
    ├── ingest_all_content.py  # Ingest textbook docs to Qdrant
    └── check_qdrant_data.py   # Check Qdrant data
```

---

## API Endpoints

### Health & Info
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Root endpoint with API info |
| `GET` | `/health` | Health check with service status |

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/auth/signup` | User registration |
| `POST` | `/auth/signin` | User login |
| `GET` | `/auth/me` | Get current user (requires JWT) |

### RAG Chatbot
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/chat` | Query the textbook chatbot |
| `POST` | `/ingest` | Ingest documents into vector database |

---

## Request/Response Examples

### POST /chat

**Request:**
```json
{
  "query": "What is Physical AI?",
  "max_results": 5
}
```

**Response:**
```json
{
  "query": "What is Physical AI?",
  "response": "Physical AI is the integration of artificial intelligence with physical systems...",
  "sources": [
    {
      "id": "doc_001",
      "title": "Module 1: Introduction to Physical AI",
      "path": "/docs/module1/intro.md",
      "score": 0.89
    }
  ]
}
```

### POST /auth/signup

**Request:**
```json
{
  "email": "user@example.com",
  "password": "securepassword123",
  "name": "John Doe"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": "usr_123",
    "email": "user@example.com",
    "name": "John Doe"
  }
}
```

---

## Environment Variables (HF Space Secrets)

These must be configured in HuggingFace Space Settings → Repository secrets:

```bash
# Cohere (Embedding)
COHERE_API_KEY=your_cohere_key_here

# OpenRouter (LLM - Gemini Flash 1.5)
OPENROUTER_API_KEY=your_openrouter_key_here
OPENROUTER_MODEL=google/gemini-flash-1.5

# Qdrant (Vector Database)
QDRANT_URL=https://your-qdrant-cluster.qdrant.io
QDRANT_API_KEY=your_qdrant_api_key_here

# Authentication
JWT_SECRET=your_jwt_secret_min_32_characters_random
BETTER_AUTH_SECRET=your_better_auth_secret_min_32_chars_random

# Optional: Rate limiting
RATE_LIMIT_ENABLED=true
RATE_LIMIT_REQUESTS_PER_MINUTE=10
```

---

## Dockerfile (for HF Spaces)

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port (HF Spaces uses 7860)
EXPOSE 7860

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]
```

---

## Requirements.txt

```
fastapi==0.109.0
uvicorn[standard]==0.27.0
pydantic==2.5.3
python-dotenv==1.0.0
cohere==4.48
qdrant-client==1.7.0
openai==1.10.0
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6
slowapi==0.1.9
sqlalchemy==2.0.25
```

---

## Deployment Steps

### 1. Create New HuggingFace Space

1. Go to https://huggingface.co/spaces/sehrkhan873/robotic_text_book
2. Ensure Space SDK is set to **Docker**
3. Set visibility to **Public**

### 2. Configure Space Secrets

In Space Settings → Repository secrets, add all environment variables listed above.

### 3. Deploy Backend

```bash
cd backend
git init
git remote add hf https://huggingface.co/spaces/sehrkhan873/robotic_text_book
git add .
git commit -m "Deploy FastAPI backend"
git push hf main
```

### 4. Update Frontend Proxy

Update `frontend/netlify.toml`:

```toml
[[redirects]]
  from = "/api/*"
  to = "https://sehrkhan873-robotic_text_book.hf.space/:splat"
  status = 200
  force = true
```

---

## Testing

### Test Health Endpoint
```bash
curl https://sehrkhan873-robotic_text_book.hf.space/health
```

### Test Chat Endpoint
```bash
curl -X POST https://sehrkhan873-robotic_text_book.hf.space/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "What is Physical AI?", "max_results": 5}'
```

### Test Auth Endpoint
```bash
curl -X POST https://sehrkhan873-robotic_text_book.hf.space/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "test123", "name": "Test User"}'
```

---

## Success Criteria

- ✅ Backend deploys successfully to `sehrkhan873/robotic_text_book` HF Space
- ✅ Health endpoint returns `status: "healthy"`
- ✅ Chat endpoint returns RAG responses with sources
- ✅ Auth endpoints (signup/signin) work correctly
- ✅ Frontend can call `/api/*` endpoints via Netlify proxy
- ✅ Old Gradio chatbot at `sehrkhan873-text-book.hf.space` remains running

---

## Notes

- **Old Gradio space remains untouched** - This spec creates a new backend in a different space
- **SQLite for auth** - HF Spaces doesn't support persistent databases, so auth data will reset on redeploy. For production, consider external DB.
- **Qdrant is external** - Vector database is hosted separately (Qdrant Cloud)
- **Rate limiting enabled** - Prevents abuse (10 requests/minute for chat)
