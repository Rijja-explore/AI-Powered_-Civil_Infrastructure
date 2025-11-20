# 🏗️ AI-Powered Structural Health Monitoring for Civil Infrastructure

**A complete AI-driven platform for intelligent infrastructure analysis and monitoring.**

**InfraVision AI** combines state-of-the-art computer vision, machine learning, and statistical analysis to provide comprehensive structural health monitoring. This production-ready system enables predictive maintenance, automated damage detection, and data-driven infrastructure management decisions.

---

## 📋 Table of Contents

- [Project Overview](#project-overview)
- [Key Features](#key-features)
- [System Architecture](#system-architecture)
- [Quick Start Guide](#quick-start-guide)
- [Installation & Setup](#installation--setup)
- [How-To Guides](#how-to-guides)
- [API Documentation](#api-documentation)
- [Technology Stack](#technology-stack)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)
- [Development Workflow](#development-workflow)

---

## 🎯 Project Overview

**InfraVision AI** is a comprehensive solution for monitoring and analyzing the structural health of civil infrastructure. It combines:

- **🎥 Computer Vision**: YOLOv8-based detection and segmentation models
- **🧠 Machine Learning**: MobileNetV2 for material classification, scikit-learn for severity prediction
- **📊 Statistical Analysis**: Hypothesis testing, ANOVA, predictive modeling, confidence intervals
- **📈 Environmental Assessment**: Carbon footprint, water usage, sustainability metrics
- **🌍 Real-Time Monitoring**: Live camera feeds with instant analysis and alerting
- **📱 Modern UI**: React.js with Glass-Morphism design for professional interaction

### 💡 Innovation Points

✅ **Complete Image Analysis**: 6 simultaneous image outputs (Original, Cracks, Biological Growth, Segmentation, Depth Estimation, Edge Detection)  
✅ **Advanced Material Intelligence**: Classify 8 material types with density, durability, and quality metrics  
✅ **Biological Growth Tracking**: Detect and classify moss, algae, lichen, vegetation with intensity scoring  
✅ **Severity Classification**: Automatic categorization into Critical/Severe/Moderate/Minor with distribution analysis  
✅ **Statistical Rigor**: Comprehensive hypothesis testing with p-values, confidence intervals, effect sizes  
✅ **Environmental Integration**: Carbon and water impact calculations for sustainable infrastructure management  

---

## ✨ Key Features

### 📸 **Image Analysis**
- Automated crack detection with severity classification
- Building material identification (Stone, Brick, Concrete, Marble, Plaster, Wood, Metal, Sandstone)
- Biological growth detection (Moss, Algae, Lichen, Vegetation)
- Edge detection using Canny algorithm
- Depth estimation via shadow analysis
- Segmentation with YOLOv8
- PDF report generation with detailed findings

### 🎥 **Video Analysis**
- Frame-by-frame structural analysis
- Temporal trend detection across video sequences
- Aggregated statistics from all frames
- Frame navigation and detailed breakdown
- Executive summary with key findings
- Critical issue identification across time

### 📡 **Real-Time Monitoring**
- Live camera feed integration (USB/IP cameras)
- Instant damage detection and alerting
- Dashboard metrics for continuous visualization
- Historical trend tracking
- Performance indicators and KPIs
- Connection management and configuration

### 📊 **Analytics Dashboard**
- Infrastructure health scoring (0-100)
- Severity distribution visualization
- Material composition analysis
- Risk assessment matrices
- Predictive deterioration trends
- Environmental impact charts
- Maintenance recommendation engine

### 🌿 **Environmental Assessment**
- Carbon footprint calculations (kg CO₂ equivalent)
- Water usage impact metrics
- Energy consumption analysis
- Sustainability scoring
- Environmental recommendations
- Green infrastructure insights

### 🧮 **Statistical Analysis**
- **Descriptive Statistics**: Mean, median, mode, standard deviation, quartiles
- **Hypothesis Testing**: t-tests, chi-square, Mann-Whitney U tests
- **Inferential Statistics**: Confidence intervals, effect sizes, p-values
- **ANOVA**: One-way and two-way analysis of variance with post-hoc tests
- **Predictive Modeling**: Linear regression, classification models, time series forecasting
- **Distribution Analysis**: Normality testing, outlier detection, frequency distributions

---

## 🏛️ System Architecture

```
┌────────────────────────────────────────────────────────────────────┐
│           AI-POWERED STRUCTURAL HEALTH MONITORING PLATFORM         │
└────────────────────────────────────────────────────────────────────┘
                             │
          ┌──────────────────┼──────────────────┐
          │                  │                  │
    ⚛️  FRONTEND         🐍  BACKEND       📊  ANALYTICS
    React 18.x      Streamlit + Flask    ML + Statistics
   http://3000      Ports: 8501, 5002    YOLOv8, MobileNetV2
          │                  │                  │
          └──────────────────┼──────────────────┘
                             │
          ┌──────────────────┼──────────────────┐
          │                  │                  │
    🎥 VISION          🔍 DETECTION        📈 PREDICTIONS
   YOLOv8 v8         Cracks, Materials     Deterioration
   Segmentation      Biological Growth     Maintenance
   Edge Detection    Severity Levels       Forecasting
```

### 🖥️ Frontend Architecture (React)

**Location**: `./frontend/`  
**Port**: `http://localhost:3000`  
**Framework**: React 18 with Hooks and Context API

#### Component Structure
```
frontend/src/
├── components/
│   ├── MainDashboard.jsx    # Dashboard layout
│   └── Navbar.jsx            # Navigation bar
├── pages/
│   ├── HomePage.jsx          # Landing page
│   ├── ImageAnalysis.jsx     # Image upload & analysis (⭐ Enhanced)
│   ├── VideoAnalysis.jsx     # Video processing
│   ├── RealTimeMonitoring.jsx # Live monitoring
│   ├── Analytics.jsx         # Statistical dashboard
│   ├── Environmental.jsx     # Environmental metrics
│   └── About.jsx             # Project information
├── contexts/
│   └── AnalysisContext.js    # Global state management
├── utils/
│   └── dataScienceHelpers.js # API communication
└── styles/
    ├── main.css              # Primary styles
    └── new-professional.css  # Glass-UI theme
```

#### Recent Enhancements (ImageAnalysis.jsx)
✅ 3-column image grid displaying all 6 outputs  
✅ Severity classification cards with color-coded badges  
✅ Material properties with density and durability metrics  
✅ Biological growth assessment with type classification  

### 🐍 Backend Architecture (Python)

| Service | Type | Port | Purpose |
|---------|------|------|---------|
| **Main Backend** | Streamlit | 8501 | Primary server, API handling, file processing |
| **Flask API** | REST | 5002 | Secondary endpoints, CORS-enabled for React |
| **Analytics** | Module | - | Statistical analysis, ML predictions |
| **Models** | YOLOv8 | - | Detection and segmentation (runs/detect/train3/weights/best.pt) |

#### Backend File Structure
```
├── finalwebapp.py                    # Main Streamlit server (~1000 lines)
├── finalwebapp_api.py                # Flask REST API (~900 lines)
├── advanced_data_analytics.py        # Statistics & ML processing
├── camera_capture.py                 # Camera integration
├── pdf_report.py                     # PDF generation
├── segmentation_with_localisation.py # CV processing utilities
├── requirements.txt                  # Python dependencies
└── runs/
    ├── detect/train3/weights/       # YOLO detection model (best.pt, last.pt)
    └── segmentation_model/weights/  # Segmentation model
```

#### Key Backend Functions

**Image Analysis Pipeline** (`finalwebapp.py`)
```python
detect_with_yolo()                    # Crack detection → severity, confidence, bbox
detect_biological_growth_advanced()   # Moss/algae detection → coverage %, type
classify_material()                   # Material classification → 8 types with density
apply_canny_edge_detection()          # Edge detection → edge image
segment_image()                       # Image segmentation → segmented regions
create_depth_estimation_heatmap()     # Depth analysis → heatmap visualization
calculate_carbon_footprint()          # Environmental → kg CO₂
calculate_water_footprint()           # Environmental → water usage metrics
analyze_image_comprehensive()         # Full pipeline → all 6 outputs + statistics
```

**REST API Endpoints** (`finalwebapp_api.py`)
```
POST   /api/analyze                   # Main image analysis endpoint
GET    /api/health                    # Service health check
GET    /api/analytics                 # Retrieve cached results
POST   /api/connect_camera            # Camera connection
POST   /api/disconnect_camera         # Camera disconnection
POST   /api/start_stream              # Start real-time stream
POST   /api/stop_stream               # Stop streaming
GET    /api/stream_metrics            # Live metrics
POST   /api/camera_capture            # Single frame capture
```

---

## 🚀 Quick Start Guide

### Option 1: Automated Startup (Recommended)
```bash
# Install all dependencies
pip install -r requirements.txt
cd frontend && npm install && cd ..

# Start the platform
python start_enhanced_app.py
```

### Option 2: Manual Multi-Terminal Startup
```bash
# Terminal 1: Frontend
cd frontend
npm install
npm start

# Terminal 2: Python Backend
python finalwebapp.py

# Terminal 3: Flask API (optional)
python finalwebapp_api.py
```

### 🌐 Access Application

| Service | URL | Status |
|---------|-----|--------|
| **React App** | http://localhost:3000 | Main Interface ✨ |
| **Streamlit** | http://localhost:8501 | Backend Server |
| **Flask API** | http://localhost:5002 | REST Endpoints |
| **Health Check** | http://localhost:5002/api/health | Diagnostics |

---

## 📦 Installation & Setup

### 📋 Prerequisites

#### 🖥️ System Requirements
- **OS**: Windows 10+, macOS 10.14+, or Linux (Ubuntu 20.04+)
- **Storage**: 2GB free space (for models and processing)
- **RAM**: 4GB minimum, 8GB recommended
- **Network**: Active internet connection (for model downloads)

#### Node.js (for React Frontend)
- **Version**: 16.x LTS or higher
- **npm**: 8.x or higher
- **Installation**: Download from [nodejs.org](https://nodejs.org/)

```bash
# Verify installation
node --version
npm --version
```

#### Python (for Backend)
- **Version**: 3.8 or higher (3.10+ recommended)
- **pip**: Latest version
- **venv**: Python virtual environment module

```bash
# Verify installation
python --version
pip --version

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate    # Linux/Mac
# or
venv\Scripts\activate        # Windows
```

### 🔧 Step 1: Clone Repository & Prepare Environment

```bash
# Clone the project
git clone <repository-url>
cd AI-Powered_-Civil_Infrastructure

# Create Python virtual environment (recommended)
python -m venv venv
source venv/bin/activate    # Linux/Mac
# or
venv\Scripts\activate        # Windows
```

### 📥 Step 2: Install Python Dependencies

```bash
# Install from requirements.txt
pip install -r requirements.txt

# Individual key packages:
pip install flask streamlit
pip install opencv-python pillow
pip install ultralytics torch torchvision
pip install numpy pandas scipy scikit-learn
pip install matplotlib seaborn plotly
pip install reportlab requests
```

### ⚛️ Step 3: Install React Frontend

```bash
cd frontend

# Install Node dependencies
npm install

# Or with specific package manager
npm install --legacy-peer-deps  # if dependency conflicts occur

cd ..
```

### ✅ Step 4: Verify Installation

```bash
# Check Python packages
python -c "import flask, streamlit, cv2, ultralytics, numpy, pandas, scipy, sklearn; print('✓ All Python packages installed')"

# Check Node packages
cd frontend && npm list react react-dom axios && cd ..
```

### 🚀 Step 5: Launch Application

```bash
# Option A: Automated startup
python start_enhanced_app.py

# Option B: Manual startup in 3 terminals
# Terminal 1:
cd frontend && npm start

# Terminal 2:
python finalwebapp.py

# Terminal 3:
python finalwebapp_api.py
```

### ✨ Access the Application

Open browser and navigate to:
- **Main App**: http://localhost:3000
- **Streamlit**: http://localhost:8501
- **Flask API**: http://localhost:5002

🎉 **You're ready to start analyzing infrastructure!**

---

## 📚 How-To Guides

### 🖼️ **Guide 1: Analyzing an Image**

#### Step-by-Step Instructions

1. **Open the Application**
   - Navigate to http://localhost:3000
   - Click "Image Analysis" in the navigation menu

2. **Upload an Image**
   - Click the "Upload Image" button or drag-drop an image
   - Supported formats: JPG, PNG, BMP
   - Maximum size: 50MB

3. **Wait for Analysis**
   - Analysis typically takes 5-15 seconds
   - Progress indicator shows processing status
   - Do not close or reload the page

4. **Review Results**
   
   **Section 1: Image Grid (6 Outputs)**
   - **Original**: Your uploaded image
   - **Crack Detection**: Red boxes showing detected cracks
   - **Biological Growth**: Blue/green areas showing moss/algae
   - **Segmentation**: Colored regions of different materials
   - **Depth Estimation**: Heatmap showing depth (red=closer, blue=farther)
   - **Edge Detection**: White lines showing structural edges

   **Section 2: Analysis Summary**
   - **Health Score**: 0-100 rating of structural condition
   - **Crack Count**: Total number of detected cracks
   - **AI Confidence**: How certain the AI is in detections

   **Section 3: Material Analysis**
   - **Primary Material**: Detected building material (Stone, Brick, etc.)
   - **Material Density**: kg/m³ of the material
   - **Durability Score**: 1-10 rating
   - **Material Quality**: Excellent/Very Good/Good/Fair/Poor

   **Section 4: Severity Classification**
   - **Critical**: Red badge with count (immediate repair needed)
   - **Severe**: Orange badge with count (urgent repair)
   - **Moderate**: Yellow badge with count (planned repair)
   - **Minor**: Green badge with count (monitor condition)

   **Section 5: Biological Growth Assessment**
   - **Moss/Lichen Growth**: Percentage and intensity
   - **Algae Growth**: Percentage and intensity
   - **Vegetation**: Percentage and intensity
   - **Growth Coverage**: 0-100% intensity bar

   **Section 6: Environmental Impact**
   - **Carbon Footprint**: kg CO₂ equivalent
   - **Water Footprint**: Water usage metrics
   - **Energy Consumption**: Estimated energy impact
   - **Eco-Efficiency**: Environmental rating

5. **Download PDF Report**
   - Click "Generate PDF Report"
   - Report includes all images and analysis
   - Save to your local computer

#### 💡 Tips & Best Practices

✅ Use high-resolution images (1920x1080 or higher) for better accuracy  
✅ Ensure good lighting conditions when photographing  
✅ Capture perpendicular angles for accurate measurements  
✅ Clean camera lens before capturing  
✅ Avoid shadows and reflections in images  

---

### 🎥 **Guide 2: Processing Video Files**

1. **Navigate to Video Analysis**
   - Open http://localhost:3000
   - Click "Video Analysis" in navigation menu

2. **Upload Video**
   - Click "Upload Video" button
   - Supported formats: MP4, AVI, MOV, MKV
   - Maximum size: 500MB

3. **Wait for Processing**
   - System extracts frames at 1fps
   - Each frame analyzed independently
   - Processing time: ~1-2 minutes per 60-second video

4. **Review Frame-by-Frame Results**
   - Navigate between frames using Previous/Next buttons
   - View detailed analysis for each frame
   - Review executive summary across all frames

#### Video Recording Tips
✅ Use steady camera (tripod recommended)  
✅ Record entire structure systematically  
✅ Maintain consistent distance from structure  
✅ Capture different angles  

---

### 📡 **Guide 3: Real-Time Monitoring with Camera**

1. **Connect Camera**
   - Plug USB camera into computer
   - Navigate to "Real-Time Monitoring" page
   - Click "Connect Camera" button

2. **Start Monitoring**
   - Click "Start Live Stream"
   - Live feed appears in video player
   - Analysis updates every 2-5 seconds

3. **Monitor Alerts**
   - 🔴 RED: Critical issue (immediate action)
   - 🟠 ORANGE: Severe issue (urgent action)
   - 🟡 YELLOW: Moderate issue (schedule repair)
   - 🟢 GREEN: Normal condition

#### Camera Requirements
✅ USB camera or IP camera on same network  
✅ Minimum resolution: 1280x720  
✅ Grant OS permissions to access camera  

---

### 📊 **Guide 4: Understanding the Analytics Dashboard**

The Analytics dashboard displays:
- **Structural Health Index**: 0-100 overall rating
- **Severity Distribution**: Breakdown of Critical/Severe/Moderate/Minor
- **Risk Assessment**: 5-dimensional risk radar chart
- **Material Composition**: Bar chart of detected materials
- **Temporal Trends**: Line chart showing health changes over time
- **Predictive Forecast**: Future condition predictions

#### Health Score Interpretation
- 90-100: Excellent - No maintenance needed
- 75-89: Good - Routine maintenance recommended
- 60-74: Fair - Repair planning needed
- 45-59: Poor - Urgent repairs required
- <45: Critical - Immediate intervention needed

---

## 🔌 API Documentation

### REST API Base URL
```
http://localhost:5002
```

### Core Endpoints

#### **POST /api/analyze**
Analyze a single image for structural defects.

**Request**
```bash
curl -X POST http://localhost:5002/api/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "image_data": "<base64_encoded_image>",
    "file_name": "structure.jpg"
  }'
```

**Response** (200 OK)
```json
{
  "status": "success",
  "results": {
    "crack_detection": {
      "detected_cracks": 5,
      "severity": "Severe",
      "statistics": {
        "severity_distribution": {
          "Critical": 1,
          "Severe": 2,
          "Moderate": 1,
          "Minor": 1
        }
      }
    },
    "material_analysis": {
      "primary_material": "Concrete",
      "density_kg_m3": 2400,
      "durability_score": 7.5,
      "material_quality": "Very Good"
    },
    "biological_growth": {
      "coverage_percentage": 15.5,
      "growth_types": ["Moss", "Algae"],
      "growth_intensity": 65
    },
    "environmental_impact_assessment": {
      "carbon_footprint": 1250,
      "water_footprint": 3500
    },
    "data_science_insights": {
      "health_score": 62,
      "ai_confidence": 0.92
    }
  },
  "output_images": {
    "original": "data:image/png;base64,...",
    "crack_detection": "data:image/png;base64,...",
    "biological_growth": "data:image/png;base64,...",
    "segmentation": "data:image/png;base64,...",
    "depth_estimation": "data:image/png;base64,...",
    "edge_detection": "data:image/png;base64,..."
  }
}
```

#### **GET /api/health**
Check if API is running.

**Request**
```bash
curl http://localhost:5002/api/health
```

**Response** (200 OK)
```json
{
  "status": "operational",
  "service": "InfraVision API",
  "version": "1.0.0"
}
```

---

## 💾 Technology Stack

### ⚛️ Frontend
- **React**: 18.2.0+ - UI framework
- **React Router**: Navigation
- **Axios**: HTTP client
- **Lucide React**: Icons (250+)
- **CSS3**: Glass-Morphism design

### 🐍 Backend
- **Streamlit**: 1.28.0+ - Web framework
- **Flask**: 2.3.0+ - REST API
- **Python**: 3.8+

### 🧠 Machine Learning
- **YOLOv8**: 8.0.0+ - Object detection
- **PyTorch**: 2.0.0+ - Neural networks
- **OpenCV**: 4.8.0+ - Image processing (Canny edges)
- **Pillow**: 9.0.0+ - Image manipulation

### 📊 Data Science
- **NumPy**: 1.21.0+ - Numerical computing
- **Pandas**: 1.5.0+ - Data manipulation
- **SciPy**: 1.9.0+ - Scientific computing
- **Scikit-learn**: 1.1.0+ - ML algorithms
- **Statsmodels**: 0.13.0+ - Statistical modeling
- **Matplotlib/Seaborn**: Visualization
- **Plotly**: 5.0.0+ - Interactive charts

### 🛠️ Utilities
- **ReportLab**: PDF generation
- **Requests**: HTTP library
- **Python-dotenv**: Environment variables

---

## ⚙️ Configuration

### 🐍 Environment Variables (`.env`)
```bash
# Server Configuration
FLASK_PORT=5002
STREAMLIT_PORT=8501
REACT_PORT=3000

# Model Configuration
MODEL_CONFIDENCE_THRESHOLD=0.3
YOLO_MODEL_PATH=runs/detect/train3/weights/best.pt
SEG_MODEL_PATH=segmentation_model/weights/best.pt

# Processing Configuration
PX_TO_CM_RATIO=0.1
MAX_UPLOAD_SIZE=52428800  # 50MB

# Camera Configuration
CAMERA_RESOLUTION=1920,1080
CAMERA_FPS=30
```

### ⚛️ React Configuration (Frontend `.env`)
```
REACT_APP_API_URL=http://localhost:5002
REACT_APP_STREAMLIT_URL=http://localhost:8501
REACT_APP_MAX_UPLOAD_SIZE=52428800
```

---

## 🆘 Troubleshooting

### ❌ **Port Already in Use**

```bash
# Windows: Kill process on port
netstat -ano | findstr :3000
taskkill /PID <PID> /F

# Mac/Linux: Kill process on port
lsof -i :3000
kill -9 <PID>
```

### ❌ **Python Dependencies Installation Fails**

```bash
# Clear cache and reinstall
pip cache purge
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

### ❌ **YOLO Model Download Issues**

```bash
# Manually download YOLOv8
python -c "from ultralytics import YOLO; YOLO('yolov8n.pt')"

# Check model cache
python -c "from ultralytics import YOLO; print(YOLO.cache_dir)"
```

### ❌ **API Connection Failed**

1. **Check backend is running**:
   ```bash
   curl http://localhost:5002/api/health
   ```

2. **Check CORS configuration** - Verify Flask API allows localhost:3000

3. **Check firewall** - Add Python/Node to firewall exceptions

### ❌ **Camera Connection Failed**

**Windows/Mac/Linux**: Grant camera permissions in OS settings  

```python
# Verify camera availability
import cv2
cap = cv2.VideoCapture(0)
if cap.isOpened():
    print("Camera found")
else:
    print("Camera not found")
cap.release()
```

### ❌ **Out of Memory During Analysis**

```python
# Use CPU instead of GPU
# Edit finalwebapp_api.py:
yolo_model = YOLO('best.pt', device='cpu')
```

---

## 🔄 Development Workflow

### 📁 Project Structure
```
AI-Powered_-Civil_Infrastructure/
├── frontend/                # React Application
│   ├── src/pages/          # Page components (6 pages)
│   ├── src/components/     # Reusable components
│   ├── src/contexts/       # State management
│   ├── src/styles/         # CSS files
│   └── package.json        # Dependencies
├── finalwebapp.py          # Main Streamlit server
├── finalwebapp_api.py      # Flask REST API
├── requirements.txt        # Python dependencies
├── runs/detect/train3/     # YOLO models
└── segmentation_model/     # Segmentation models
```

### 🖥️ Frontend Development

```bash
# Start development server
cd frontend
npm install
npm start

# Build for production
npm run build

# Run tests
npm test

# Lint code
npm run lint
```

### 🐍 Backend Development

```bash
# Start Streamlit backend
python finalwebapp.py

# Start Flask API
python finalwebapp_api.py

# Run tests
pytest tests/

# Run with debug logging
python -m flask run --reload
```

---

## 📝 License

This project is licensed under the MIT License - see LICENSE file for details.

---

## 🙏 Acknowledgments

- **YOLOv8** - Ultralytics for state-of-the-art object detection
- **PyTorch** - Deep learning framework
- **React** - UI framework
- **Streamlit** - Rapid backend development
- **Open Source Community** - All amazing contributors

---

## 🎯 Project Status

**Version**: 1.0.0  
**Status**: ✅ Production Ready  
**Last Updated**: January 2024

✨ **If you found this helpful, please star this repository!** ⭐

---

## 🚀 Next Steps

1. **Set up your environment** following the Installation & Setup section
2. **Upload a test image** to verify the system is working
3. **Explore the Analytics dashboard** to understand available metrics
4. **Check the How-To Guides** for detailed feature walkthroughs
5. **Review API Documentation** for integration possibilities

🌟 **Happy Infrastructure Monitoring!**
