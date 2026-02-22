# FastAPI Backend Deployment Guide

## Overview

This guide will help you deploy the FastAPI backend to your new HuggingFace Space: `https://huggingface.co/spaces/sehrkhan873/robotic_text_book`

**Note**: Your old Gradio chatbot at `https://sehrkhan873-text-book.hf.space` will remain running unchanged.

---

## Quick Start

### 1. Configure HuggingFace Space Secrets

Go to your Space settings and add these secrets:

```
COHERE_API_KEY=your_cohere_key_here
OPENROUTER_API_KEY=your_openrouter_key_here
OPENROUTER_MODEL=google/gemini-flash-1.5
QDRANT_URL=https://your-qdrant-cluster.qdrant.io
QDRANT_API_KEY=your_qdrant_api_key_here
JWT_SECRET=your_jwt_secret_min_32_characters_random
BETTER_AUTH_SECRET=your_better_auth_secret_min_32_chars_random
```

### 2. Deploy via Git

```bash
cd /mnt/c/Users/user/Desktop/robotic_book/seher_ai_book/backend
git init
git remote add hf https://huggingface.co/spaces/sehrkhan873/robotic_text_book
git add .
git commit -m "Deploy FastAPI backend"
git push hf main
```

### 3. Test Deployment

```bash
# Test health endpoint
curl https://sehrkhan873-robotic_text_book.hf.space/health

# Test chat endpoint
curl -X POST https://sehrkhan873-robotic_text_book.hf.space/api/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "What is Physical AI?", "max_results": 3}'
```

---

## File Structure

```
backend/
├── main.py                    # FastAPI application entry point
├── Dockerfile                 # Docker configuration for HF Spaces
├── requirements.txt           # Python dependencies
├── .dockerignore             # Docker ignore rules
├── .env.example              # Example environment variables
├── README.md                 # Space README (displayed on HF)
│
├── auth/                     # Authentication module
│   ├── __init__.py
│   ├── main.py               # Auth routes (/auth/signup, /signin, /me)
│   ├── models.py             # SQLAlchemy models
│   ├── schemas.py            # Pydantic schemas
│   ├── services.py           # Auth business logic
│   ├── utils.py              # JWT & password utilities
│   ├── config.py             # Configuration
│   ├── database.py           # Database connection
│   └── dependencies.py       # FastAPI dependencies
│
├── routes/                   # API routes
│   ├── __init__.py
│   ├── chat.py               # RAG chatbot (/api/chat)
│   └── ingest.py             # Document ingestion (/api/ingest)
│
├── services/                 # Business logic
│   ├── __init__.py
│   └── rag_service.py        # RAG pipeline services
│
├── utils/                    # Utilities
│   ├── __init__.py
│   └── logger.py             # Logging configuration
│
└── scripts/                  # Helper scripts
    ├── init_db.py            # Initialize database
    ├── ingest_all_content.py # Ingest docs to Qdrant
    ├── check_qdrant_data.py  # Check Qdrant data
    └── test_backend.py       # Test backend API
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
| `POST` | `/api/chat` | Query the textbook chatbot |
| `POST` | `/api/ingest` | Ingest documents into vector database |

---

## Update Frontend Proxy

After deployment, update `frontend/netlify.toml`:

```toml
[[redirects]]
  from = "/api/*"
  to = "https://sehrkhan873-robotic_text_book.hf.space/:splat"
  status = 200
  force = true
```

Then push to GitHub:

```bash
git add frontend/netlify.toml
git commit -m "Update backend URL to new HF Space"
git push origin main
```

---

## Local Testing

### Run Locally

```bash
cd backend
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your API keys
uvicorn main:app --reload --port 7860
```

### Test with Script

```bash
cd backend/scripts
python test_backend.py
```

---

## Troubleshooting

### Backend not starting
- Check Space logs in HuggingFace dashboard
- Verify all secrets are set correctly
- Ensure Dockerfile is in root of backend folder

### API calls failing
- Test backend directly first: `https://sehrkhan873-robotic_text_book.hf.space/health`
- Check CORS settings in `main.py`
- Verify netlify.toml proxy configuration

### Services not initialized
- Check logs for missing API keys
- Verify Qdrant URL and API key
- Ensure COHERE_API_KEY and OPENROUTER_API_KEY are set

### Database issues
- Run `python scripts/init_db.py` to initialize tables
- Note: SQLite resets on redeploy (HF Spaces limitation)

---

## Next Steps

1. ✅ Deploy backend to HF Spaces
2. ✅ Test all endpoints
3. ✅ Update frontend proxy URL
4. ✅ Test frontend → backend integration
5. ✅ Ingest textbook content using `scripts/ingest_all_content.py`

---

## Security Notes

⚠️ **IMPORTANT**:
- Never commit `.env` file to git
- Rotate all API keys if they were previously exposed
- Use HuggingFace Spaces secrets for sensitive data
- In production, use external database (not SQLite)
