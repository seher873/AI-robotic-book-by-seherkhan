# Backend Integration Guide

## Current Status

✅ **Frontend**: Deployed successfully on Netlify
- URL: https://seher-robotic-book.netlify.app
- Configuration: `frontend/netlify.toml`
- API Proxy: `/api/*` → `https://sehrkhan873-text-book.hf.space`

⚠️ **Backend**: Needs deployment to HuggingFace Spaces
- Current HF Space: https://sehrkhan873-text-book.hf.space (running Gradio app)
- Target: Deploy FastAPI backend from `backend/` folder

## Backend Files Ready for Deployment

All backend code is in `backend/` folder:

```
backend/
├── main.py                 # FastAPI application
├── Dockerfile              # Docker config for HF Spaces
├── requirements.txt        # Python dependencies
├── .dockerignore          # Docker ignore rules
├── auth/                  # Authentication module
│   ├── main.py           # Auth routes
│   ├── models.py         # Database models
│   ├── schemas.py        # Pydantic schemas
│   ├── services.py       # Business logic
│   ├── utils.py          # JWT & password utilities
│   ├── config.py         # Auth configuration
│   ├── database.py       # Database connection
│   └── dependencies.py   # FastAPI dependencies
├── scripts/
│   ├── init_db.py        # Initialize database
│   ├── ingest_all_content.py  # Ingest docs to Qdrant
│   └── check_qdrant_data.py   # Check Qdrant data
└── [guides and tests]
```

## Deployment Steps

### 1. Create New HuggingFace Space

1. Go to https://huggingface.co/spaces
2. Click "Create new Space"
3. Settings:
   - **Space name**: `robotic-textbook-backend` (or similar)
   - **License**: MIT
   - **Space SDK**: Docker
   - **Visibility**: Public

### 2. Configure Space Secrets

In your new Space, go to Settings → Repository secrets → Add secret:

```
COHERE_API_KEY=your_cohere_key_here
OPENROUTER_API_KEY=your_openrouter_key_here
QDRANT_URL=https://your-qdrant-cluster.qdrant.io
QDRANT_API_KEY=your_qdrant_api_key_here
JWT_SECRET=your_jwt_secret_min_32_characters
BETTER_AUTH_SECRET=your_better_auth_secret_min_32_chars
OPENROUTER_MODEL=google/gemini-flash-1.5
```

### 3. Deploy Backend

**Option A: Push via Git**

```bash
cd backend
git init
git remote add hf https://huggingface.co/spaces/sehrkhan873/robotic-textbook-backend
git add .
git commit -m "Deploy FastAPI backend"
git push hf main
```

**Option B: Upload Files**

1. Clone your new Space:
   ```bash
   git clone https://huggingface.co/spaces/sehrkhan873/robotic-textbook-backend
   ```
2. Copy all backend files into the cloned folder
3. Push:
   ```bash
   git add .
   git commit -m "Deploy FastAPI backend"
   git push
   ```

### 4. Update Frontend Configuration

After backend is deployed, update `frontend/netlify.toml`:

```toml
[[redirects]]
  from = "/api/*"
  to = "https://sehrkhan873-robotic-textbook-backend.hf.space/:splat"
  status = 200
  force = true
```

Then push to GitHub to trigger Netlify deploy:

```bash
git add frontend/netlify.toml
git commit -m "Update backend URL to new HF Space"
git push origin main
```

## API Endpoints

Once deployed, these endpoints will be available:

### Health & Info
- `GET /` - Root endpoint
- `GET /health` - Health check

### Authentication
- `POST /auth/signup` - User registration
- `POST /auth/signin` - User login
- `GET /auth/me` - Get current user

### RAG Chatbot
- `POST /chat` - Query the textbook chatbot
- `POST /ingest` - Ingest documents into vector database

## Testing

After deployment, test the backend:

```bash
# Test health endpoint
curl https://sehrkhan873-robotic-textbook-backend.hf.space/health

# Test chat endpoint
curl -X POST https://sehrkhan873-robotic-textbook-backend.hf.space/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "What is Physical AI?", "max_results": 5}'
```

## Troubleshooting

### Backend not starting
- Check Space logs in HuggingFace dashboard
- Verify all secrets are set correctly
- Check Dockerfile is in root of backend folder

### API calls failing from frontend
- Verify CORS settings in `main.py`
- Check netlify.toml proxy configuration
- Test backend directly first

### Database issues
- Run `python scripts/init_db.py` to initialize
- Check Qdrant connection in Space logs

## Security Notes

⚠️ **IMPORTANT**: API keys were previously exposed in git history. Make sure to:
1. Rotate all API keys (Cohere, OpenRouter, Qdrant)
2. Never commit `.env` file
3. Use HuggingFace Spaces secrets for sensitive data

## File Safety

✅ **Frontend files are safe** - Only backend files will be modified
✅ **Netlify deployment unchanged** - Only backend URL in netlify.toml needs update
✅ **Git history cleaned** - Sensitive files removed from history
