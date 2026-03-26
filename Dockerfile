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

# Copy trained models - CRITICAL for crack detection and segmentation
# These directories must exist (may contain .gitkeep placeholder if empty in CI/CD)
COPY runs/ ./runs/
COPY segmentation_model/ ./segmentation_model/

# Copy any other Python files and static assets
COPY *.py ./
COPY frontend/ ./frontend/

# Expose port
EXPOSE 7860

# Set Flask app environment variable
ENV FLASK_APP=finalwebapp_api.py

# Run the app
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0", "--port=7860"]
