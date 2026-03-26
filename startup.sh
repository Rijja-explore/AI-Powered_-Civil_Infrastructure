#!/bin/bash
# Startup script for InfraVision API
# Attempts to ensure trained models are available before starting the Flask app

echo "🚀 InfraVision API Startup"
echo "========================="

# Function to check and attempt to download missing models
check_models() {
    local model_path="$1"
    local model_name="$2"
    
    if [ -f "$model_path" ]; then
        size=$(du -h "$model_path" | cut -f1)
        echo "✅ Found $model_name: $size"
        return 0
    else
        echo "⚠️ Missing $model_name at $model_path"
        return 1
    fi
}

# Check for trained models
echo ""
echo "Checking for trained models..."
echo "Looking for crack detection model..."
check_models "runs/detect/train3/weights/best.pt" "Crack Detection Model" || {
    echo "  - Provided models not available"
    echo "  - App will use YOLOv8n default model at startup"
}

echo ""
echo "Looking for segmentation model..."
check_models "segmentation_model/weights/best.pt" "Segmentation Model" || {
    echo "  - Provided models not available"
    echo "  - App will use YOLOv8n-seg default model at startup"
}

echo ""
echo "Starting Flask application on port 7860..."
echo ""

# Start Flask app
python -m flask run --host=0.0.0.0 --port=7860
