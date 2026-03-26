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

# Copy all other Python files
COPY *.py ./

# Create necessary directory structure for models and frontend
# Docker build context may not include these directories (they may need to be loaded separately)
# The application will check these directories at runtime and load models if available
RUN mkdir -p /app/runs/detect/train/weights /app/runs/detect/train3/weights && \
    mkdir -p /app/segmentation_model/weights && \
    mkdir -p /app/frontend/src /app/frontend/public && \
    mkdir -p /app/frontend/node_modules /app/__pycache__

# Expose port
EXPOSE 7860

# Set Flask app environment variable
ENV FLASK_APP=finalwebapp_api.py

# Run the app
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0", "--port=7860"]
