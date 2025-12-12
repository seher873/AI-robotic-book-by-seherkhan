#!/bin/bash

# Script to start Docusaurus server with proper error handling
# This script addresses network connectivity issues by ensuring proper server configuration

echo "Starting Docusaurus server with fixes..."

# Kill any existing docusaurus processes
echo "Stopping any existing Docusaurus processes..."
pkill -f "docusaurus" 2>/dev/null || true

# Wait for processes to fully terminate
sleep 3

# Build the site to ensure it's up to date
echo "Building the site..."
npx docusaurus build

if [ $? -ne 0 ]; then
    echo "Build failed. Please check the configuration."
    exit 1
fi

echo "Build completed successfully."

# Start the server with specific host and port settings
echo "Starting server on 0.0.0.0:3000..."
npx docusaurus serve --host 0.0.0.0 --port 3000 --no-open > /tmp/docusaurus_server.log 2>&1 &

# Wait a moment for the server to start
sleep 5

# Check if the server is running
if pgrep -f "docusaurus serve" > /dev/null; then
    echo "Docusaurus server is running successfully!"
    echo "Access your dashboard at: http://localhost:3000/dashboard"
    echo "Access the main site at: http://localhost:3000"
    echo "Server logs are available at: /tmp/docusaurus_server.log"
    
    # Test if the server is responding
    if curl -s --connect-timeout 10 http://localhost:3000/ | grep -i "physical ai" > /dev/null; then
        echo "✓ Server is responding to requests"
        echo "✓ Dashboard is accessible at: http://localhost:3000/dashboard"
    else
        echo "⚠ Server process is running but not responding to requests"
        echo "Check the logs at /tmp/docusaurus_server.log for details"
    fi
else
    echo "Failed to start Docusaurus server"
    echo "Check logs with: cat /tmp/docusaurus_server.log"
    exit 1
fi