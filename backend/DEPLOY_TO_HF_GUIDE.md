# 🚀 Deploy Backend to Hugging Face Spaces - Complete Guide

This guide will help you deploy your FastAPI RAG backend to Hugging Face Spaces without errors.

## 📋 Prerequisites

1. **Hugging Face Account**: Create one at [huggingface.co](https://huggingface.co/join)
2. **API Keys**: Have these ready:
   - Cohere API Key
   - OpenRouter API Key
   - Qdrant URL and API Key

## 🎯 Method 1: Automated Deployment (Recommended)

### Step 1: Install Hugging Face CLI

```bash
pip install huggingface_hub
```

### Step 2: Run the Deployment Script

```bash
cd backend
chmod +x deploy_to_hf.sh
./deploy_to_hf.sh
```

### Step 3: Follow the Prompts

The script will:
1. Log you in to Hugging Face
2. Ask for your username
3. Ask for a space name
4. Create the space and upload files
5. Push to Hugging Face

### Step 4: Add Secrets (IMPORTANT!)

After deployment:

1. Go to your Space page on Hugging Face
2. Click **Settings** tab
3. Scroll to **Variables and secrets**
4. Click **New secret** and add:

| Name | Value |
|------|-------|
| `COHERE_API_KEY` | Your Cohere key |
| `OPENROUTER_API_KEY` | Your OpenRouter key |
| `QDRANT_URL` | Your Qdrant Cloud URL |
| `QDRANT_API_KEY` | Your Qdrant API key |
| `OPENROUTER_MODEL` | `google/gemini-flash-1.5` |

⚠️ **Important**: Add these as **Secrets**, NOT Variables!

### Step 5: Restart the Space

After adding secrets:
1. Go to **Settings** tab
2. Click **Factory reboot** or **Restart Space**

## 🎯 Method 2: Manual Deployment (Web Interface)

### Step 1: Create a New Space

1. Go to [huggingface.co/new-space](https://huggingface.co/new-space)
2. Fill in:
   - **Space name**: `physical-ai-backend` (or your choice)
   - **License**: MIT
   - **SDK**: **Docker**
   - **Hardware**: CPU Basic (free tier is fine)
3. Click **Create Space**

### Step 2: Upload Files

Upload these files from your `backend` folder:

**Required files:**
- `Dockerfile`
- `main.py`
- `requirements.txt`
- `.dockerignore`

**Required folders:**
- `auth/`
- `routes/`
- `services/`
- `utils/`

You can upload via:
- **Web interface**: Drag and drop files
- **Git clone**:
  ```bash
  git clone https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE_NAME
  # Copy files to the cloned directory
  cd YOUR_SPACE_NAME
  git add .
  git commit -m "Initial deployment"
  git push
  ```

### Step 3: Configure Port

Your `Dockerfile` already uses port `7860`, which Hugging Face expects. No changes needed!

### Step 4: Add Secrets

Same as Method 1, Step 4 above.

### Step 5: Wait for Build

The Space will:
1. Build the Docker image (~2-5 minutes)
2. Start the container
3. Show "Running" status

## ✅ Verify Deployment

### Test Health Endpoint

```bash
curl https://YOUR_USERNAME-YOUR_SPACE_NAME.hf.space/health
```

Expected response:
```json
{
  "status": "healthy",
  "service": "RAG Chatbot Backend",
  "version": "1.0.0",
  "services": {
    "database": "up",
    "qdrant": "up",
    "openrouter": "up"
  }
}
```

### Test Root Endpoint

```bash
curl https://YOUR_USERNAME-YOUR_SPACE_NAME.hf.space/
```

Expected response:
```json
{
  "message": "Physical AI Textbook RAG Chatbot Backend"
}
```

### Test Chat Endpoint

```bash
curl -X POST https://YOUR_USERNAME-YOUR_SPACE_NAME.hf.space/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "What is physical AI?", "max_results": 3}'
```

## 🔧 Troubleshooting

### ❌ "Services not initialized" Error

**Cause**: Missing or incorrect API keys

**Fix**:
1. Go to Space Settings → Variables and secrets
2. Verify all secrets are set correctly
3. Restart the Space

### ❌ Docker Build Fails

**Cause**: Missing required files

**Fix**: Ensure these files are uploaded:
- `Dockerfile`
- `main.py`
- `requirements.txt`
- All service folders (`auth/`, `routes/`, `services/`, `utils/`)

### ❌ 500 Error on Chat

**Cause**: Qdrant or API connection issue

**Fix**:
1. Check your Qdrant URL is correct
2. Verify API keys are valid
3. Check Space logs in the **Logs** tab

### ❌ CORS Errors

**Fix**: The backend already has CORS enabled for all origins. If you need to restrict:
1. Edit `main.py`
2. Change `allow_origins=["*"]` to your specific frontend URL
3. Redeploy

## 📊 Monitoring

View your Space:
- **Logs**: Click the "Logs" tab to see real-time logs
- **Files**: Click "Files" to see deployed files
- **Settings**: Manage secrets and hardware

## 🔐 Security Best Practices

✅ **DO**:
- Use Secrets (not Variables) for API keys
- Keep `.env` files out of the repository
- Use the provided `.dockerignore`

❌ **DON'T**:
- Commit `.env` files with real keys
- Hardcode API keys in code
- Share your API keys publicly

## 📞 Support

If you encounter issues:
1. Check the Space logs
2. Verify all secrets are set
3. Test the health endpoint
4. Review this guide's troubleshooting section

---

**Your backend URL will be**: `https://YOUR_USERNAME-YOUR_SPACE_NAME.hf.space`

**Health check**: `https://YOUR_USERNAME-YOUR_SPACE_NAME.hf.space/health`
