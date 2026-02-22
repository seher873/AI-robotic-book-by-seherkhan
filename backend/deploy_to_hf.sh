#!/bin/bash
# Deploy Backend to Hugging Face Spaces
# This script helps you deploy your FastAPI backend to Hugging Face Spaces

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}==================================${NC}"
echo -e "${GREEN}Hugging Face Spaces Deployment${NC}"
echo -e "${GREEN}==================================${NC}"
echo ""

# Check if huggingface-cli is installed
if ! command -v huggingface-cli &> /dev/null; then
    echo -e "${YELLOW}Installing huggingface_hub...${NC}"
    pip install huggingface_hub
fi

# Login to Hugging Face
echo -e "${YELLOW}Logging in to Hugging Face...${NC}"
huggingface-cli login

# Get user's Hugging Face username
echo -e "${YELLOW}Enter your Hugging Face username:${NC}"
read -r HF_USERNAME

# Get space name
echo -e "${YELLOW}Enter your Space name (e.g., physical-ai-backend):${NC}"
read -r SPACE_NAME

# Create full repo name
REPO_NAME="${HF_USERNAME}/${SPACE_NAME}"

echo -e "${GREEN}Deploying to: ${REPO_NAME}${NC}"
echo ""

# Create space if it doesn't exist
echo -e "${YELLOW}Creating/verifying Space...${NC}"
huggingface-cli repo create "${SPACE_NAME}" --type space --space_sdk docker

# Clone the space repository
TEMP_DIR=$(mktemp -d)
echo -e "${YELLOW}Cloning space repository to ${TEMP_DIR}...${NC}"
git clone "https://huggingface.co/spaces/${REPO_NAME}" "${TEMP_DIR}"

# Copy necessary files
echo -e "${YELLOW}Copying deployment files...${NC}"
cp Dockerfile "${TEMP_DIR}/"
cp main.py "${TEMP_DIR}/"
cp requirements.txt "${TEMP_DIR}/"
cp .dockerignore "${TEMP_DIR}/"

# Copy service directories
cp -r auth "${TEMP_DIR}/"
cp -r routes "${TEMP_DIR}/"
cp -r services "${TEMP_DIR}/"
cp -r utils "${TEMP_DIR}/"

# Create .gitignore for the space
cat > "${TEMP_DIR}/.gitignore" << EOF
# Python cache
__pycache__/
*.py[cod]
*$py.class
*.so
.Python

# Virtual environments
venv/
env/
ENV/
.venv/

# Environment variables
.env
.env.*

# IDEs
.vscode/
.idea/
*.swp
*.swo
*~
.DS_Store

# Logs
*.log
logs/

# Test files
test_*.py
*_test.py

# Build artifacts
build/
dist/
*.egg-info/
EOF

# Create README for the space
cat > "${TEMP_DIR}/README.md" << EOF
---
title: Physical AI RAG Chatbot Backend
emoji: 🤖
colorFrom: blue
colorTo: purple
sdk: docker
pinned: false
license: mit
---

# Physical AI Textbook RAG Chatbot Backend

This is a FastAPI backend for a RAG (Retrieval-Augmented Generation) chatbot specialized in Physical AI & Humanoid Robotics.

## Features

- 📚 RAG-based question answering
- 🔐 JWT Authentication
- 📊 Vector search with Qdrant
- 🚀 FastAPI with rate limiting
- 🌐 CORS enabled

## API Endpoints

- \`GET /\` - Root endpoint
- \`GET /health\` - Health check
- \`POST /chat\` - Chat with the RAG system
- \`POST /ingest\` - Ingest documents

## Environment Variables (Secrets)

Make sure to set these in your Space Settings → Variables and secrets:

- \`COHERE_API_KEY\` - Your Cohere API key
- \`OPENROUTER_API_KEY\` - Your OpenRouter API key
- \`QDRANT_URL\` - Your Qdrant Cloud URL
- \`QDRANT_API_KEY\` - Your Qdrant API key
- \`OPENROUTER_MODEL\` - Model to use (e.g., google/gemini-flash-1.5)

## Testing

Once deployed, test the health endpoint:
\`\`\`bash
curl https://${HF_USERNAME}-${SPACE_NAME}.hf.space/health
\`\`\`
EOF

# Commit and push
cd "${TEMP_DIR}"
git config user.email "deploy@huggingface.co"
git config user.name "Hugging Face Deploy"
git add .
git commit -m "Deploy FastAPI RAG backend"
git push

echo ""
echo -e "${GREEN}==================================${NC}"
echo -e "${GREEN}Deployment Complete!${NC}"
echo -e "${GREEN}==================================${NC}"
echo ""
echo -e "Your backend is deploying at:"
echo -e "${YELLOW}https://huggingface.co/spaces/${REPO_NAME}${NC}"
echo ""
echo -e "Health check URL:"
echo -e "${YELLOW}https://${HF_USERNAME}-${SPACE_NAME}.hf.space/health${NC}"
echo ""
echo -e "${YELLOW}Note: Don't forget to add your API keys in Space Settings → Variables and secrets${NC}"

# Cleanup
cd - > /dev/null
rm -rf "${TEMP_DIR}"

echo -e "${GREEN}Done!${NC}"
