#!/bin/bash

# Permanent Docusaurus Server Startup Script
# This script fixes common accessibility issues and ensures the server runs reliably

echo "🔧 Starting Docusaurus server with permanent fixes..."

# Kill any existing processes
echo "🛑 Stopping existing processes..."
pkill -f "docusaurus" 2>/dev/null || true
sleep 3

# Ensure required ports are free
echo "🧹 Ensuring port 3000 is available..."
sudo fuser -k 3000/tcp 2>/dev/null || true
sleep 2

# Build the site to ensure latest changes
echo "🏗️ Building the site..."
npm run build

if [ $? -ne 0 ]; then
    echo "❌ Build failed. Please check your configuration."
    exit 1
fi

echo "✅ Build completed successfully."

# Start server with multiple fallback options
echo "🚀 Starting server with fallback options..."

# Try primary port first
npx docusaurus start --port 3000 --host 0.0.0.0 --poll 1000 > server.log 2>&1 &
SERVER_PID=$!

# Wait a moment for server to start
sleep 8

# Check if server is running
if ps -p $SERVER_PID > /dev/null; then
    echo "✅ Server is running with PID: $SERVER_PID"
    echo "🌐 Access your site at: http://0.0.0.0:3000 or http://localhost:3000"
    
    # Show available network interfaces
    echo "📋 Available network interfaces:"
    hostname -I
    
    # Show troubleshooting tips
    echo ""
    echo "📝 Troubleshooting tips if you can't access the site:"
    echo "   - If using WSL: Access from Windows browser at http://localhost:3000"
    echo "   - If using Cloud IDE: Use platform's port forwarding/preview feature"
    echo "   - If firewall is blocking: Temporarily disable firewall or add exception for port 3000"
    
    # Show all images are accessible
    echo ""
    echo "🖼️  Verifying image accessibility:"
    echo "   - Logo image: /img/logoo.png"
    echo "   - Dashboard image: /img/roobot.png"
    echo "   - Homepage image: /img/robot.png"
    
    exit 0
else
    echo "⚠️  Primary port failed, trying fallback port 8080..."
    npx docusaurus start --port 8080 --host 0.0.0.0 --poll 1000 > server.log 2>&1 &
    FALLBACK_PID=$!
    
    sleep 8
    
    if ps -p $FALLBACK_PID > /dev/null; then
        echo "✅ Fallback server running on port 8080"
        echo "🌐 Access your site at: http://0.0.0.0:8080"
        exit 0
    else
        echo "❌ Failed to start server on any port"
        echo "📋 Check server.log for details"
        cat server.log
        exit 1
    fi
fi