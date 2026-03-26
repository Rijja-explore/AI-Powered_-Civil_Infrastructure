# InfraVision AI - Intelligent Infrastructure Monitoring System

An advanced AI-powered platform for real-time structural health monitoring and infrastructure assessment using computer vision and machine learning.

---

## 📋 Table of Contents
- [Quick Start](#quick-start)
- [Features](#features)
- [Installation](#installation)
- [Project Structure](#project-structure)
- [API Endpoints](#api-endpoints)
- [Usage Guide](#usage-guide)

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 14+
- pip & npm
- Camera (optional, for real-time monitoring)

### Installation

**Step 1: Clone & Setup Backend**
```bash
cd d:\AI-Powered_Civil_Infrastructure
python -m venv venv
venv\Scripts\activate  # Windows
# For Linux/Mac: source venv/bin/activate
pip install -r requirements.txt
```

**Step 2: Setup Frontend**
```bash
cd frontend
npm install
cd ..
```

**Step 3: Start Backend API**
```bash
python finalwebapp_api.py
# Server runs on http://localhost:5002
```

**Step 4: Start Frontend (in another terminal)**
```bash
cd frontend
npm start
# App opens at http://localhost:3000
```

---

## ✨ Features

### 1. **Image Analysis**
- Upload infrastructure photographs (JPG, PNG)
- AI-powered crack detection with severity assessment
- Biological growth detection
- Environmental impact analysis
- Real-time severity scoring
- Visual output with damage annotations

### 2. **Video Analysis**
- Real-time & file-based video processing
- Frame-by-frame damage detection
- Temporal trend analysis
- Critical frame identification
- Comprehensive analysis reports
- JSON export capability

### 3. **Real-Time Monitoring**
- Live camera feed processing
- Continuous infrastructure assessment
- Performance metrics (FPS, latency)
- System health dashboard

### 4. **3D Visualization**
- Convert 2D crack patterns to 3D heightmaps
- GLB/STL model generation
- Interactive 3D viewer
- Export for AR/VR applications

---

## 📦 Installation Details

### Python Environment (Windows)
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Python Environment (Linux/Mac)
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Frontend Setup
```bash
cd frontend
npm install
npm start  # Development server on localhost:3000
```

---

## 📂 Project Structure

```
InfraVision AI/
│
├── frontend/                     # React UI Application
│   ├── public/                   # Static assets
│   ├── src/
│   │   ├── pages/                # Application pages
│   │   │   ├── ImageAnalysis.jsx      # Image upload & analysis
│   │   │   ├── Heightmap3D.jsx        # 3D visualization
│   │   │   ├── RealTimeMonitoring.jsx # Live monitoring
│   │   │   └── Environmental.jsx      # Environmental metrics
│   │   ├── components/           # React components
│   │   ├── contexts/             # React contexts
│   │   └── styles/               # CSS styling
│   └── package.json
│
├── Backend (Root Level)
│   ├── finalwebapp_api.py        # Main Flask API server
│   ├── finalwebapp.py            # Core analysis engine
│   ├── image_3d_heightmap.py     # 3D model generation
│   ├── segmentation_with_localisation.py  # Segmentation analysis
│   ├── requirements.txt          # Python dependencies
│   ├── Procfile                  # Deployment configuration
│   └── render.yaml               # Render.com deployment spec
│
├── analytics_pipeline/
│   ├── data_loading.py
│   ├── feature_extraction.py
│   ├── statistics.py
│   └── export_json.py
│
├── Dataset/
│   ├── crack_preprocess/         # Crack detection training data
│   │   ├── train/
│   │   ├── valid/
│   │   └── test/
│   └── vegetation_preprocess/    # Vegetation detection training data
│       ├── train/
│       ├── valid/
│       └── test/
│
├── segmentation_model/
│   ├── weights/
│   │   ├── best.pt               # Best trained model
│   │   └── last.pt               # Last checkpoint
│   ├── args.yaml
│   └── results.csv
│
├── runs/
│   └── detect/
│       └── train/
│           ├── weights/          # Training weights
│           └── results.csv
│
├── .env.example                  # Environment variables template
├── .gitignore                    # Git ignore rules
├── .github/                      # GitHub workflows
├── README.md                     # This file
└── PROJECT_REPORT.md             # Comprehensive project documentation
```

---

## 🔌 API Endpoints

### Analysis Endpoints
- **POST** `/api/analyze-image` - Analyze single image
- **POST** `/api/analyze-video` - Analyze video file
- **POST** `/api/analyze-stream` - Real-time camera stream analysis
- **POST** `/api/analyze-frame` - Analyze single frame

### 3D Model Generation
- **POST** `/api/generate-heightmap` - Generate 3D heightmap from crack detection
- **GET** `/api/models/<model_id>` - Retrieve generated 3D model

### Analytics & Data
- **GET** `/api/analytics` - Get aggregated analytics data
- **POST** `/api/export-report` - Export analysis as report

### Health Check
- **GET** `/health` - API health status

---

## 📖 Usage Guide

### Analyzing Images

1. Go to **Image Analysis** page
2. Upload or capture infrastructure photo
3. System analyzes for:
   - Crack patterns & severity
   - Material type & condition
   - Biological growth
   - Environmental factors
4. View detailed annotation report
5. Download results as JSON

### Video Analysis

1. Go to **Video Analysis** page
2. Upload video or stream from camera
3. System processes frame-by-frame
4. Generates:
   - Frame-wise damage detection
   - Temporal trend analysis
   - Critical frame identification
5. Export comprehensive report

### Real-Time Monitoring

1. Go to **Real-Time Monitoring**
2. Connect camera feed
3. Monitor continuous assessment
4. View live metrics and alerts
5. Track performance statistics

### 3D Visualization

1. Go to **3D Visualization (Heightmap)**
2. Upload crack detection results
3. Generate 3D heightmap model
4. Interactive viewer for exploration
5. Export as GLB/STL for AR/VR

---

## 🛠️ Configuration

### Environment Variables
Create `.env` file (copy from `.env.example`):

```
# Flask Configuration
FLASK_ENV=production
FLASK_DEBUG=False

# CORS Settings
CORS_ORIGINS=http://localhost:3000

# Model Paths
CRACK_MODEL_PATH=segmentation_model/weights/best.pt

# Optional: Database
DATABASE_URL=postgresql://user:password@localhost/db
```

---

## 📋 Requirements

**Python Dependencies:** See [requirements.txt](requirements.txt) for complete list

**Key Libraries:**
- Flask - Web framework
- YOLOv8 - Object detection
- TensorFlow - Deep learning
- OpenCV - Computer vision
- PyTorch - ML framework
- Scikit-learn - ML utilities
- Trimesh - 3D model generation

**Frontend:**
- React 18+
- Plotly - Data visualization
- Three.js - 3D visualization

---

## 🚀 Deployment

### Render.com Deployment
```bash
# Ensure render.yaml is configured
# Push to GitHub
git push origin main

# Render will auto-deploy from GitHub
```

See `Procfile` and `render.yaml` for deployment configuration.

---

## 📊 Performance Metrics

- Image analysis: ~2-5 seconds
- Video frame processing: ~0.3-0.5 seconds per frame
- 3D model generation: ~1-3 seconds
- Real-time streaming: 30+ FPS on modern hardware

---

## ⚠️ Important Notes

1. **Model Files**: Trained weights stored in `segmentation_model/weights/`. Ensure these are not deleted.
2. **Dataset**: Training datasets in `Dataset/` folder required for model retraining.
3. **GPU Support**: For faster processing, ensure NVIDIA GPU drivers and CUDA are installed.
4. **Memory**: Minimum 4GB RAM recommended, 8GB+ for optimal performance.

---

## 🤝 Contributing

To improve or extend this project:

1. Create feature branch: `git checkout -b feature/your-feature`
2. Make changes
3. Test thoroughly
4. Commit: `git commit -m "Add your feature"`
5. Push: `git push origin feature/your-feature`
6. Create Pull Request

---

## 📝 License

This project is licensed under the MIT License - see LICENSE file for details.

---

## 📧 Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Contact project maintainers

---

**Last Updated**: March 26, 2026
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
