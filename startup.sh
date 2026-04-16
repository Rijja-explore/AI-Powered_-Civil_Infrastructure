#!/bin/bash
# Startup script for InfraVision AI on Hugging Face Spaces

set -e  # Exit on error

echo "🚀 Starting InfraVision AI API Server..."
echo "📍 Loading models and initializing system..."

# Set working directory
cd /app

# Download models from Hugging Face Hub before starting Flask
echo ""
echo "📥 Downloading trained models from Hugging Face..."
python3 -c "
from hf_model_loader import download_models_from_hf
try:
    download_models_from_hf()
except Exception as e:
    print(f'⚠️ Warning: Model download had issues: {e}')
    print('   Will continue with available models or fallbacks')
"

# Run the Flask app on port 7860 (Hugging Face Spaces default)
echo ""
echo "🔧 Starting Flask API server..."
python3 finalwebapp_api.py
