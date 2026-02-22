# Backend Deployment Instructions

## Deployment Status

✅ **All backend files are ready** in `/mnt/c/Users/user/Desktop/robotic_book/seher_ai_book/backend/`

Git repository initialized and committed. Ready to push to HuggingFace Spaces.

---

## How to Deploy

### Option 1: Using Deploy Script (Recommended)

```bash
cd backend

# Set your HuggingFace token
export HF_TOKEN=your_huggingface_token_here

# Run deploy script
bash deploy.sh
```

### Option 2: Manual Git Push

```bash
cd backend

# Push using your HF token
git remote add hf https://YOUR_HF_TOKEN@huggingface.co/spaces/sehrkhan873/robotic_text_book
git push hf main
```

### Option 3: Upload via HuggingFace Web Interface

1. Go to https://huggingface.co/spaces/sehrkhan873/robotic_text_book
2. Click "Files" → "Add file" → "Upload files"
3. Upload all backend files
4. Commit changes

---

## Before Deploying: Configure Space Secrets

Go to your Space settings and add these secrets:

**URL**: https://huggingface.co/spaces/sehrkhan873/robotic_text_book → Settings → Repository secrets

```bash
COHERE_API_KEY=your_cohere_key_here
OPENROUTER_API_KEY=your_openrouter_key_here
OPENROUTER_MODEL=google/gemini-flash-1.5
QDRANT_URL=https://your-qdrant-cluster.qdrant.io
QDRANT_API_KEY=your_qdrant_api_key_here
JWT_SECRET=your_jwt_secret_min_32_characters_random
BETTER_AUTH_SECRET=your_better_auth_secret_min_32_chars_random
```

---

## After Deployment: Test Endpoints

```bash
# Health check
curl https://sehrkhan873-robotic_text_book.hf.space/health

# Root endpoint
curl https://sehrkhan873-robotic_text_book.hf.space/

# Chat endpoint
curl -X POST https://sehrkhan873-robotic_text_book.hf.space/api/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "What is Physical AI?", "max_results": 3}'
```

---

## Update Frontend Proxy

After backend is live, update `frontend/netlify.toml`:

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

## Get HuggingFace Token

1. Go to https://huggingface.co/settings/tokens
2. Click "New token"
3. Give it a name (e.g., "robotic-textbook-deploy")
4. Select "Write" permission
5. Copy the token and use it in deployment

---

## Troubleshooting

### Build Fails
- Check Space logs: https://huggingface.co/spaces/sehrkhan873/robotic_text_book → Logs
- Verify all secrets are set correctly
- Check Dockerfile is in backend root

### Services Not Initialized
- Verify API keys in Space secrets
- Check Qdrant URL and API key
- Look for error messages in logs

### 404 Errors
- Wait 2-3 minutes for build to complete
- Check Space is running (not paused)
- Verify endpoint paths include `/api/` prefix

---

## Current Status

- ✅ Backend code complete
- ✅ Dockerfile configured
- ✅ Requirements.txt updated
- ✅ Git initialized and committed
- ⏳ Waiting for: HF token for push
- ⏳ Waiting for: Space secrets configuration
