# InfraVision AI - Intelligent Infrastructure Monitoring System

An advanced AI-powered platform for real-time structural health monitoring and infrastructure assessment using computer vision and machine learning.

---

## 📋 Table of Contents
- [Quick Start](#quick-start)
- [Key Features](#key-features)  
- [Installation](#installation)
- [Project Structure](#project-structure)
- [Usage Guide](#usage-guide)
- [API Documentation](#api-documentation)
- [System Architecture](#system-architecture)

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 14+
- Camera (optional, for real-time monitoring)

### Installation

1. **Clone & Setup**
```bash
cd d:\AI-Powered_Civil_Infrastructure
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

2. **Install Frontend Dependencies**
```bash
cd frontend
npm install
cd ..
```

3. **Start Backend API**
```bash
python finalwebapp_api.py
```

4. **Start Frontend (in another terminal)**
```bash
cd frontend
npm start
```

5. **Access Application**
```
http://localhost:3000
```

---

## ✨ Key Features

### 1. **Image Analysis**
- Upload infrastructure photographs (JPG, PNG)
- AI-powered crack detection and classification
- Biological growth detection
- Material type classification
- Environmental impact assessment
- Real-time severity scoring
- Visual output with damage annotations

### 2. **Video Analysis** 
- Real-time video stream processing
- Frame-by-frame damage detection
- Temporal trend analysis
- Critical frame identification
- Comprehensive summary reports
- Export analysis results as JSON

### 3. **Real-Time Monitoring**
- Live camera feed streaming
- Continuous infrastructure assessment
- Instant alert generation
- System health metrics
- Performance monitoring (FPS, latency)

### 4. **3D Visualization**
- Convert 2D crack patterns to 3D heightmaps
- GLB model generation
- Interactive 3D viewer
- Export 3D models for AR/VR applications

### 5. **Data Analytics**
- Material analysis with confidence scores
- Biological growth metrics
- Environmental impact calculations
- Structural health scoring
- Risk assessment and recommendations

---

## 📦 Installation

### Option A: Development Environment

```bash
# Clone repository
git clone <repository-url>
cd d:\AI-Powered_Civil_Infrastructure

# Create Python environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup frontend
cd frontend
npm install
cd ..
```

### Option B: Using Docker (Optional)

```bash
# Build Docker image
docker build -t infravision-ai .

# Run container
docker run -p 5002:5002 -p 3000:3000 infravision-ai
```

---

## 📂 Project Structure

```
InfraVision AI/
├── frontend/                          # React UI
│   ├── public/
│   ├── src/
│   │   ├── pages/
│   │   │   ├── ImageAnalysis.jsx      # Upload & analyze images
│   │   │   ├── VideoAnalysis.jsx      # Real-time & file video analysis
│   │   │   ├── RealTimeMonitoring.jsx # Live stream dashboard
│   │   │   └── Heightmap3D.jsx        # 3D visualization
│   │   ├── components/
│   │   ├── contexts/
│   │   └── styles/
│   └── package.json
│
├── backend API/
│   ├── finalwebapp_api.py             # Flask REST API (main)
│   ├── finalwebapp.py                 # Core ML functions
│   ├── segmentation_with_localisation.py
│   └── image_3d_heightmap.py
│
├── models/
│   ├── segmentation_model/
│   │   └── weights/best.pt            # YOLOv8 segmentation model
│   └── runs/detect/train3/weights/   # YOLO crack detection model
│
├── data/
│   ├── Dataset/                       # Training datasets
│   │   ├── crack_preprocess/
│   │   └── vegetation_preprocess/
│   ├── uploads/                       # User uploads
│   ├── segmentation_outputs/         # Analysis outputs
│   └── dataset_analytics.json         # Analytics data
│
├── requirements.txt                   # Python dependencies
├── package.json                       # Node dependencies
├── README.md                          # This file
└── .gitignore
```

---

## 🎯 Usage Guide

### Image Analysis Workflow

1. **Open Application** → Navigate to "Image Analysis" tab
2. **Upload Image** → Select JPG/PNG file (infrastructure photo)
3. **Wait for Processing** → AI analyzes image (5-10 seconds)
4. **View Results**:
   - Crack detection heatmap
   - Biological growth overlay
   - Material classification
   - Health score and recommendations
5. **Download Report** → Save JSON or screenshot

### Video Analysis Workflow

1. **Navigate** → "Video Analysis" tab
2. **Choose Mode**:
   - **Upload Video File**: Select MP4/AVI/MOV
   - **Real-Time Stream**: Click "Connect Camera" → "Start Real-Time Analysis"
3. **Processing**: Frames analyzed automatically
4. **Results**: Frame-by-frame analysis with timeline
5. **Export**: Download comprehensive JSON report

### Real-Time Monitoring

1. **Open** → "Real-Time Monitoring" tab
2. **Connect Camera** → System initializes webcam
3. **Start Streaming** → Live feed with real-time analysis
4. **View Metrics**:
   - Live crack count
   - Health score trends
   - Alert notifications
   - Performance stats (FPS, latency)

### 3D Heightmap Generation

1. **Navigate** → "3D Heightmap" tab
2. **Upload Image** → Select infrastructure photo
3. **Generate 3D Model** → System processes image
4. **View & Interact** → Rotate, zoom, inspect 3D model
5. **Export** → Save as GLB for AR/VR use

---

## 🔌 API Documentation

**Base URL**: `http://localhost:5002`

### Core Endpoints

#### Image Analysis
```
POST /api/analyze
Content-Type: application/json

Request:
{
  "image": "base64_encoded_image",
  "px_to_cm_ratio": 0.1,
  "confidence_threshold": 0.3
}

Response:
{
  "results": {
    "crack_detection": { "count": 10, "severity": "Moderate" },
    "biological_growth": { "percentage": 5.2 },
    "material_analysis": { "type": "Brick", "confidence": 0.92 },
    "health_score": 6.8
  },
  "output_images": { "original": "data:image/png;base64,..." }
}
```

#### Video Analysis
```
POST /api/analyze_video
Content-Type: multipart/form-data

Request:
- video: <file>
- analysis_type: "comprehensive"
- px_to_cm_ratio: 0.1
- confidence_threshold: 0.3

Response:
{
  "total_frames": 150,
  "frames_processed": 50,
  "analysis_duration": 45.2,
  "frame_results": { ... },
  "comprehensive_summary": { ... }
}
```

#### Camera Connection
```
POST /api/connect_camera
Response: { "success": true, "message": "Camera connected" }

POST /api/disconnect_camera
Response: { "success": true, "message": "Camera disconnected" }
```

#### Real-Time Capture
```
POST /api/capture_and_analyze
Response:
{
  "success": true,
  "frame": "data:image/jpeg;base64,...",
  "analysis": { "crack_count": 3, "health_score": 7.2 }
}
```

#### Health Check
```
GET /api/health
Response: { "status": "healthy", "timestamp": "2024-03-25T10:30:00Z" }
```

---

## 🏗️ System Architecture

### Frontend (React)
- **Pages**: 4 main analysis views (Image, Video, Real-Time, 3D)
- **Context API**: Shared state management
- **HTTP Client**: Fetch API for backend communication
- **UI Components**: Lucide icons, custom CSS
- **Real-Time Updates**: WebSocket-ready architecture

### Backend (Flask)
- **REST API**: 15+ endpoints for analysis
- **CORS**: Enabled for frontend communication
- **Image Processing**: OpenCV, NumPy, Pillow
- **AI Models**:
  - YOLOv8: Crack and damage detection
  - YOLO Segmentation: Instance segmentation
  - MobileNetV2: Material classification
- **Data Pipeline**: Preprocessing → Detection → Classification → Analytics

### ML Models
- **Crack Detection**: `runs/detect/train3/weights/best.pt` (YOLOv8)
- **Segmentation**: `segmentation_model/weights/best.pt` (YOLOv8)
- **Material Classification**: MobileNetV2 (ImageNet pretrained)
- **3D Generation**: Image-to-heightmap conversion algorithm

### Data Flow
```
User Input (Image/Video) 
    ↓
API Endpoint
    ↓
Image Preprocessing
    ↓
AI Model Inference (YOLO)
    ↓
Post-Processing & Analysis
    ↓
Results Aggregation
    ↓
JSON Response + Output Images
    ↓
Frontend Rendering
```

---

## 🛠️ Configuration

### Environment Variables
Create `.env` file (optional):
```
FLASK_ENV=production
FLASK_PORT=5002
REACT_APP_API_URL=http://localhost:5002
YOLO_CONFIDENCE=0.3
MAX_IMAGE_SIZE=50MB
```

### Model Configuration
- Modify `confidence_threshold` in API requests (default: 0.3)
- Adjust `px_to_cm_ratio` for accurate measurements (default: 0.1)
- YOLO model paths configurable in `finalwebapp_api.py`

---

## 📊 Output Examples

### Image Analysis Output
```json
{
  "crack_detection": {
    "count": 10,
    "severity": "Moderate",
    "details": [
      {"width_cm": 2.5, "length_cm": 15.0, "severity": "High"},
      {"width_cm": 1.2, "length_cm": 8.5, "severity": "Low"}
    ]
  },
  "biological_growth": {
    "affected_area_cm2": 125.5,
    "growth_percentage": 8.3,
    "growth_detected": true
  },
  "material_analysis": {
    "predicted_material": "Brick",
    "confidence": 0.92
  },
  "health_score": 6.8,
  "maintenance_urgency": "Medium"
}
```

---

## 🔍 Troubleshooting

### Backend API Won't Start
- Ensure Python 3.8+ is installed
- Run `pip install -r requirements.txt`
- Check port 5002 isn't in use: `netstat -an | findstr 5002`

### Camera Not Detected
- Check camera permissions in Windows
- Try `cv2.VideoCapture(0)` in Python console
- Restart application if camera disconnected

### Frontend Won't Connect to API
- Verify backend is running on port 5002
- Check CORS is enabled (should be in Flask app)
- Clear browser cache and reload

### YOLO Model Errors
- Download model: `yolo detect predict model=yolov8n.pt`
- Check `runs/detect/train3/weights/best.pt` exists
- Verify PyTorch installation: `python -c "import torch; print(torch.cuda.is_available())"`

---

## 📝 License & Credits

**InfraVision AI** - Advanced Infrastructure Monitoring Platform

- **ML Models**: YOLOv8 (Ultralytics)
- **Framework**: Flask, React, PyTorch
- **Data**: Civil infrastructure photo dataset

---

## 📞 Support & Contributions

For issues, feature requests, or contributions:
1. Check existing documentation
2. Review API setup guide: [API_SETUP_GUIDE.md](API_SETUP_GUIDE.md)
3. Open an issue with detailed steps to reproduce

---

**Last Updated**: March 25, 2026  
**Version**: 2.0 (Clean Architecture)
