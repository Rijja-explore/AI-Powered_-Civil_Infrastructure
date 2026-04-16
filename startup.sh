#!/bin/bash
# Startup script for InfraVision AI on Hugging Face Spaces

echo "🚀 Starting InfraVision AI API Server..."
echo "📍 Loading models and initializing system..."

# Run the Flask app on port 7860 (Hugging Face Spaces default)
python3 finalwebapp_api.py
