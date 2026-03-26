FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY finalwebapp_api.py .
COPY finalwebapp.py .
COPY segmentation_with_localisation.py .
COPY image_3d_heightmap.py .
COPY . .

# Expose port
EXPOSE 7860

# Run the app
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0", "--port=7860"]
