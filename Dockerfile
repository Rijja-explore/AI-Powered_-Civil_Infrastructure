FROM python:3.11-slim

WORKDIR /app

# Force rebuild - ensure runs/, segmentation_model/, frontend/ directories are properly included
# BuildKit cache bust: 2026-03-26T23:47:00
ARG BUILD_DATE=2026-03-26T23:47:00
LABEL builder.date="${BUILD_DATE}"

# Install system dependencies for image processing and OpenGL support
RUN apt-get update && apt-get install -y \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY finalwebapp_api.py .
COPY finalwebapp.py .
COPY pdf_report.py .
COPY segmentation_with_localisation.py .
COPY image_3d_heightmap.py .

# Install git-lfs to ensure LFS files are properly downloaded
RUN apt-get update && apt-get install -y git-lfs curl && rm -rf /var/lib/apt/lists/*

# Copy all other Python files
COPY *.py ./

# Create necessary directory structure for models and frontend
RUN mkdir -p /app/runs/detect/train/weights /app/runs/detect/train3/weights && \
    mkdir -p /app/segmentation_model/weights && \
    mkdir -p /app/frontend/src /app/frontend/public && \
    mkdir -p /app/frontend/node_modules /app/__pycache__

# Copy trained model weights (tracked via Git LFS)
COPY runs/detect/train/weights/best.pt /app/runs/detect/train/weights/ 2>/dev/null || true
COPY runs/detect/train/weights/last.pt /app/runs/detect/train/weights/ 2>/dev/null || true
COPY runs/detect/train3/weights/best.pt /app/runs/detect/train3/weights/ 2>/dev/null || true
COPY runs/detect/train3/weights/last.pt /app/runs/detect/train3/weights/ 2>/dev/null || true
COPY segmentation_model/weights/best.pt /app/segmentation_model/weights/ 2>/dev/null || true
COPY segmentation_model/weights/last.pt /app/segmentation_model/weights/ 2>/dev/null || true

# Expose port
EXPOSE 7860

# Set Flask app environment variable
ENV FLASK_APP=finalwebapp_api.py

# Run the app (models will load if available in containers, or app will use defaults)
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0", "--port=7860"]
