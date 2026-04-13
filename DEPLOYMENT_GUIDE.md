# InfraVision Deployment Guide - Material Classifier Integration

## Overview

InfraVision is deployed across two platforms:
- **Frontend**: Vercel (React application)
- **Backend**: Hugging Face (Flask API with Docker)

The material classifier integration includes:
- **Trained TensorFlow Keras model** (`material_classifier.h5` - 21.7MB)
- **TensorFlow Lite model** (`material_classifier.tflite` - 8.9MB)
- **PyTorch fallback** (MobileNetV2 for environments without TensorFlow)

---

## 🔧 Deployment Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Vercel (Frontend)                        │
│  React App → Environment Variable: REACT_APP_API_URL        │
└──────────────────────────┬──────────────────────────────────┘
                           │ API Calls
                           ↓
┌─────────────────────────────────────────────────────────────┐
│              Hugging Face Spaces (Backend)                  │
│  Flask API (Port 7860)                                      │
│  ├── 🎯 Crack Detection (YOLOv8)                            │
│  ├── 🎯 Segmentation (YOLOv8-Seg)                           │
│  └── 🎯 Material Classification (Keras/TFLite/PyTorch)     │
└─────────────────────────────────────────────────────────────┘
```

---

## 📤 Deploying Backend to Hugging Face

### 1. Prepare Models in Hugging Face Hub

First, upload all trained models to your HF Hub repository:

```bash
# Install huggingface_hub CLI
pip install huggingface-hub

# Login to Hugging Face
huggingface-cli login

# Create a repo (if not already created)
huggingface-cli repo create InfraVision-Models --type model

# Upload models to your HF Hub repo
huggingface-cli upload RijjaExplore/InfraVision-Models runs/detect/train3/weights/best.pt train3_best.pt
huggingface-cli upload RijjaExplore/InfraVision-Models segmentation_model/weights/best.pt segmentation_best.pt
huggingface-cli upload RijjaExplore/InfraVision-Models materialclassification_model/material_classifier.h5 material_classifier.h5
huggingface-cli upload RijjaExplore/InfraVision-Models materialclassification_model/material_classifier.tflite material_classifier.tflite
```

### 2. Create Hugging Face Space

1. Go to [huggingface.co/spaces](https://huggingface.co/spaces)
2. Click **"Create new Space"**
3. Name: `InfraVision-API`
4. SDK: **Docker**
5. Visibility: **Public** (or Private if needed)
6. Click **"Create Space"**

### 3. Setup Git for HF Space

```bash
cd d:\AI-Powered_Civil_Infrastructure

# Add HF Space as remote
git remote add hf https://huggingface.co/spaces/<your-username>/InfraVision-API

# Push code to HF
git push hf main
```

### 4. Automatic Model Downloads

The `hf_model_loader.py` automatically downloads models during startup:

```python
# Models will be downloaded from HF Hub in this order:
1. Crack detection: train3_best.pt
2. Segmentation: segmentation_best.pt
3. Material classifier: material_classifier.h5
4. Material classifier: material_classifier.tflite
```

The `startup.sh` orchestrates this:

```bash
#!/bin/bash
# Step 1: Download models from HF Hub
python hf_model_loader.py

# Step 2: Start Flask app
python -m flask run --host=0.0.0.0 --port=7860
```

---

## 🎨 Deploying Frontend to Vercel

### 1. Connect GitHub Repository

1. Go to [vercel.com/dashboard](https://vercel.com/dashboard)
2. Click **"Add New Project"**
3. Import your GitHub repository
4. Select the repository root (not `/frontend`)
5. Configure: **Root Directory** → `./frontend`

### 2. Set Environment Variables

**Project Settings → Environment Variables**

Add:
```
Name:  REACT_APP_API_URL
Value: https://<your-username>-infravision-api.hf.space
Environments: Production, Preview, Development
```

For local development, create `.env.local`:
```
REACT_APP_API_URL=http://localhost:7860
```

### 3. Build Settings

- **Framework Preset**: Next.js (or React if not using Next.js)
- **Build Command**: `npm run build`
- **Output Directory**: `build` (or `.next` for Next.js)
- **Install Command**: `npm install`

### 4. Deploy

```bash
# Vercel will auto-deploy on every push to main
# Or manually deploy:
npm install -g vercel
vercel --prod
```

---

## 🚀 Model Loading Hierarchy

The backend uses intelligent fallback logic:

```
┌─────────────────────────────────────────────────────────────┐
│ Material Classification Model Loading Priority              │
├─────────────────────────────────────────────────────────────┤
│ 1. TensorFlow Available? → Load material_classifier.h5      │
│    └─ Highest performance, full training utilized           │
│                                                              │
│ 2. TensorFlow Lite Available? → Load material_classifier.   │
│    └─ Lightweight, optimized for inference                  │
│                                                              │
│ 3. PyTorch Available? → Load MobileNetV2 + ImageNet weights │
│    └─ Fallback, generic model includes HSV color fallback   │
│                                                              │
│ 4. No Models? → HSV-based texture classification only       │
│    └─ Last resort, heuristic-based classification          │
└─────────────────────────────────────────────────────────────┘
```

---

## 📊 Deployment Checklist

### Before Deployment

- [ ] Update `HF_REPO_ID` in `hf_model_loader.py`
- [ ] Upload all models to Hugging Face Hub
- [ ] Test locally with `python test_material_classifier_integration.py`
- [ ] Verify `Dockerfile` includes material classifier directories
- [ ] Check `requirements.txt` includes TensorFlow (optional but recommended)

### Vercel Frontend

- [ ] Create `.env.local` for local development
- [ ] Add `REACT_APP_API_URL` environment variable in Vercel
- [ ] Test API connection in network tab
- [ ] Verify images can be uploaded and analyzed

### Hugging Face Backend

- [ ] Push code to HF Space
- [ ] Monitor space logs for model download issues
- [ ] Test API endpoints directly (curl/Postman)
- [ ] Verify material classification returns proper predictions

---

## 🧪 Testing

### Test Material Classification

```bash
# Local test
python test_material_classifier_integration.py

# API endpoint test
curl -X POST http://localhost:7860/api/analyze-image \
  -F "image=@test_image.jpg"
```

### Monitor HF Space Logs

1. Go to your HF Space: `https://huggingface.co/spaces/<you>/InfraVision-API`
2. Click **"View Logs"** in the top menu
3. Check for model download status and API startup messages

---

## 🔄 Updating Models

To update trained models:

```bash
# 1. Update models locally
# (train new YOLOv8 or material classifier)

# 2. Upload to HF Hub
huggingface-cli upload RijjaExplore/InfraVision-Models material_classifier.h5 material_classifier.h5

# 3. Restart HF Space
# - Go to Space settings → "Restart Space"
# - Or push code update to trigger rebuild
```

---

## 📝 API Endpoints

### Material Classification
```
POST /api/analyze-image

Request Body:
- image: Multi-part form file

Response:
{
  "material": "Concrete",
  "material_probabilities": {
    "Brick": 0.05,
    "Concrete": 0.85,
    "Stone": 0.05,
    "Sandstone": 0.02,
    "Marble": 0.01,
    "Plaster": 0.01,
    "Wood": 0.01,
    "Metal": 0.00
  },
  "confidence_score": 0.85
}
```

---

## ⚠️ Troubleshooting

### Models Not Loading on HF
- Check `hf_model_loader.py` logs in Space
- Verify models exist in HF Hub: `https://huggingface.co/RijjaExplore/InfraVision-Models`
- Check HF token: `huggingface-cli login`

### Frontend Can't Reach Backend
- Verify `REACT_APP_API_URL` matches actual HF Space URL
- Check CORS settings in `finalwebapp_api.py` (should have `CORS(app)`)
- Test API directly: `curl https://<hf-space-url>/api/status`

### TensorFlow Not Loading
- Check `requirements.txt` includes TensorFlow
- Rebuild HF Space if `requirements.txt` was updated
- Backend will automatically use PyTorch fallback if TensorFlow unavailable

### Low Material Classification Accuracy
- Ensure trained model (not generic MobileNetV2) is loaded
- Check logs: material model should show trained `.h5` or `.tflite`, not "ImageNet" weights
- Consider retraining classifier on your specific material dataset

---

## 📚 Project Structure

```
d:\AI-Powered_Civil_Infrastructure/
├── finalwebapp_api.py          # Flask API (Backend)
├── finalwebapp.py              # Analysis functions
├── hf_model_loader.py          # Model downloader for HF
├── startup.sh                  # Docker startup script
├── Dockerfile                  # HF Space deployment config
├── requirements.txt            # Python dependencies
├── materialclassification_model/
│   ├── material_classifier.h5          # Trained model (21.7MB)
│   └── material_classifier.tflite      # Lite model (8.9MB)
├── frontend/
│   ├── src/config/apiConfig.js # API URL config
│   ├── src/pages/ImageAnalysis.jsx
│   └── package.json
└── README.md                   # This file
```

---

## 🎯 Next Steps

1. **Push trained models to HF Hub** (if not already done)
2. **Deploy backend to HF Spaces**
3. **Configure frontend on Vercel**
4. **Monitor logs and test endpoints**
5. **Iterate on model performance**

For detailed API documentation, see `frontend/API_CONFIG.md`
