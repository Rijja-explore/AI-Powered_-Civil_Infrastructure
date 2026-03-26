#!/bin/bash
# Startup script for InfraVision API
# Automatically downloads trained models from Hugging Face Hub before starting the Flask app

echo "🚀 InfraVision API Startup"
echo "========================="
echo ""

# Try to download models from Hugging Face Hub
echo "Step 1: Attempting to load trained models from Hugging Face Hub..."
python hf_model_loader.py

echo ""
echo "Step 2: Starting Flask application on port 7860..."
echo ""

# Start Flask app
python -m flask run --host=0.0.0.0 --port=7860
