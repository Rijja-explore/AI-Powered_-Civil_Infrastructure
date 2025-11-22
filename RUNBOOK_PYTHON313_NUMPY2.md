# 🚀 RUNBOOK: Running Analytics Pipeline on Python 3.13 + NumPy 2.4.0

## Overview

This project has been refactored to work with **Python 3.13.2** and **NumPy 2.4.0.dev0** by removing dependencies on OpenCV (cv2) and scikit-image, which are **not compatible** with NumPy 2.x yet.

**Status:**
- ✅ Analytics pipeline runs successfully (no cv2/skimage)
- ✅ Backend imports successfully (graceful fallbacks for cv2-dependent features)
- ✅ Frontend and React UI ready

---

## Prerequisites

### 1. Python 3.11 or 3.13 Virtual Environment

You should already have:
- ✅ Python 3.11 installed (or 3.13.2 used here)
- ✅ Virtual environment activated at: `D:\Projects\AI-Powered_-Civil_Infrastructure\venv`

### 2. Installed Packages

Verify your environment has these core packages:

```powershell
pip list | findstr "numpy pandas scikit-learn scipy pillow matplotlib flask flask-cors"
```

Expected output (minimal):
```
numpy              2.4.0.dev0
pandas             2.2.3
scikit-learn       1.x.x (any version)
scipy              1.16.2
pillow             11.1.0
matplotlib         3.10.6
flask              2.x.x
flask-cors         4.x.x
```

If any are missing, install them:

```powershell
pip install numpy pandas scikit-learn scipy pillow matplotlib flask flask-cors
```

---

## Step 1: Activate Virtual Environment

```powershell
cd "D:\Projects\AI-Powered_-Civil_Infrastructure"
.\venv\Scripts\activate
```

You should see `(venv)` at the start of your terminal prompt.

---

## Step 2: Verify Analytics Pipeline Works

The analytics pipeline is refactored to use **Pillow + NumPy + SciPy** instead of cv2/skimage.

### Run Dataset Analytics

```powershell
python run_dataset_analytics.py
```

**Expected Output:**
```
============================================================
INFRASTRUCTURE HEALTH ANALYTICS PIPELINE
============================================================

[1/7] Loading dataset images...
Loading crack dataset from Dataset/crack_preprocess...
Loading vegetation dataset from Dataset/vegetation_preprocess...
✅ Loaded 6500 crack images and 1062 vegetation images
  ✅ Crack images: 6500
  ✅ Vegetation images: 1062

[2/7] Extracting crack features...
  ✅ Extracted 6500 feature sets

[3/7] Extracting vegetation features...
  ✅ Extracted 1062 feature sets

[4/7] Building analytical DataFrames...
  ✅ Crack DataFrame: (6500, 13)
  ✅ Vegetation DataFrame: (1062, 13)

[5/7] Computing dataset statistics...
  ✅ Computed statistics for 20 features

[6/7] Running hypothesis tests...
  ✅ Completed 4 tests

[7/7] Exporting analytics JSON...
✅ Dataset analytics exported to dataset_analytics.json

============================================================
✅ PIPELINE COMPLETED SUCCESSFULLY
============================================================

Dataset Statistics:
  Total crack images: 6500
  Total vegetation images: 1062
  ✅ Output: dataset_analytics.json
```

**Result:** 
- ✅ `dataset_analytics.json` is created in project root
- ✅ No cv2 or skimage imports fail
- ✅ Features extracted successfully

---

## Step 3: Start Flask Backend

```powershell
python finalwebapp_api.py
```

**Expected Output (with warnings, but functional):**
```
⚠️ YOLO not available
⚠️ OpenCV (cv2) not available: ... Using Pillow + NumPy for image processing.
✅ PyTorch/TorchVision loaded successfully
✅ Matplotlib loaded successfully

 * Running on http://127.0.0.1:5002
 * Press CTRL+C to quit
```

**Important Notes:**
- ⚠️ You will see warnings about cv2 and YOLO not available—this is **expected** and **OK**
- ✅ The backend still starts on port 5002
- ✅ Analytics endpoints work (they don't use cv2)
- ✅ Frontend can connect to this backend

---

## Step 4: Test Analytics Endpoints (Optional)

In a **new PowerShell window** (keep backend running):

```powershell
# Test dataset analytics endpoint
curl http://localhost:5002/api/analytics/dataset | ConvertFrom-Json | Select-Object -First 5

# Test statistical tests endpoint
curl http://localhost:5002/api/analytics/statistical_tests | ConvertFrom-Json
```

**Expected:**
- ✅ Returns JSON with analytics data
- ✅ No errors

---

## Step 5: Start React Frontend (Optional)

In a **third PowerShell window**:

```powershell
cd "D:\Projects\AI-Powered_-Civil_Infrastructure\frontend"
npm start
```

**Expected:**
- ✅ React app runs on http://localhost:3001
- ✅ Can connect to backend on port 5002

---

## Complete Workflow Summary

**To run the complete system:**

### Terminal 1: Analytics Pipeline

```powershell
cd "D:\Projects\AI-Powered_-Civil_Infrastructure"
.\venv\Scripts\activate
python run_dataset_analytics.py
# Wait for completion (1-2 minutes)
```

### Terminal 2: Backend API

```powershell
cd "D:\Projects\AI-Powered_-Civil_Infrastructure"
.\venv\Scripts\activate
python finalwebapp_api.py
# Keep running (Ctrl+C to stop)
```

### Terminal 3: React Frontend

```powershell
cd "D:\Projects\AI-Powered_-Civil_Infrastructure\frontend"
npm start
# Frontend will open at http://localhost:3001
```

---

## What Changed?

### 1. **analytics_pipeline/data_loading.py**
- **Removed:** `import cv2`
- **Added:** `from PIL import Image, ImageEnhance`
- **Change:** Image loading/resizing now uses Pillow instead of OpenCV
- **Result:** ✅ No cv2 dependency

### 2. **analytics_pipeline/feature_extraction.py**
- **Removed:** `import cv2`, `from skimage.feature import greycomatrix, greycoprops`
- **Added:** `from scipy import ndimage`
- **Changes:**
  - Sobel edge detection: `scipy.ndimage.sobel()` instead of `cv2.Canny()`
  - Morphological skeleton: `scipy.ndimage.binary_erosion/dilation()` instead of `cv2.morphologyEx()`
  - Texture entropy: Histogram-based instead of GLCM
- **Result:** ✅ No cv2 or skimage dependency

### 3. **finalwebapp_api.py** & **finalwebapp.py**
- **Changed:** `import cv2` → try/except with fallback flag
- **Result:** Backend starts even if cv2 fails, but cv2-specific features are disabled

---

## Features That Still Work ✅

- ✅ **Dataset Analytics**: Load 6500+ images, extract 18 features, run statistical tests
- ✅ **Backend API**: Serve analytics JSON to frontend
- ✅ **React UI**: Display analytics dashboard
- ✅ **Image Upload** (basic): Upload images for analysis
- ✅ **Data Persistence**: Tab switching without data loss

---

## Features That Don't Work ❌ (cv2-dependent)

These features are **disabled** because they require OpenCV:
- ❌ Real-time heatmap generation (color mapping)
- ❌ Advanced morphological operations (skeletonization with cv2)
- ❌ YOLO-based detection (requires OpenCV)
- ❌ Camera capture

**Workaround:** If you need these, downgrade NumPy to 1.x:
```powershell
pip uninstall -y numpy
pip install "numpy<2"
```

Then cv2 will work, but you need NumPy < 2 for this.

---

## Troubleshooting

### Error: "Unable to allocate X MiB for array"
- **Cause:** Image is corrupted or too large
- **Fix:** Some images may skip, but pipeline continues
- **Result:** Still get analytics from valid images

### Error: "numpy.core.multiarray failed to import"
- **Cause:** cv2 or another package trying to import
- **Fix:** Already handled with try/except
- **Result:** Backend continues with fallback

### Backend won't start
- **Check:** Is port 5002 already in use?
  ```powershell
  netstat -ano | findstr :5002
  ```
- **Fix:** Kill the process or change port in `finalwebapp_api.py`

### Frontend won't connect to backend
- **Check:** Is backend running on port 5002?
  ```powershell
  curl http://localhost:5002/
  ```
- **Fix:** Start backend first, then frontend

---

## Environment Details

- **Python:** 3.13.2 (or 3.11.x)
- **NumPy:** 2.4.0.dev0 (development version)
- **SciPy:** 1.16.2
- **Pillow:** 11.1.0
- **Flask:** 2.x.x

**Why NumPy 2.x?**
- It's the future of NumPy
- Scientific ecosystem is gradually migrating
- Your environment already has it installed

**Why not downgrade to NumPy 1.x?**
- Once NumPy 2.x is set, many packages depend on it
- This refactor future-proofs your code

---

## Next Steps

1. **Test the API:** 
   ```powershell
   curl http://localhost:5002/api/analytics/dataset
   ```

2. **Upload an image in React UI:**
   - Go to http://localhost:3001
   - Upload an image
   - See analytics on dashboard

3. **Check JSON output:**
   - Open `dataset_analytics.json` in editor
   - Verify structure

4. **Deploy:** 
   - Use this workflow on production server
   - Recommend Python 3.11 for stability (3.13 still experimental)

---

## Quick Reference Commands

| Task | Command |
|------|---------|
| Activate venv | `.\venv\Scripts\activate` |
| Run analytics | `python run_dataset_analytics.py` |
| Start backend | `python finalwebapp_api.py` |
| Start frontend | `npm start` (in frontend/) |
| Test API | `curl http://localhost:5002/api/analytics/dataset` |
| Check port 5002 | `netstat -ano \| findstr :5002` |
| Deactivate venv | `deactivate` |

---

## Questions?

- Check logs in terminal for detailed errors
- Verify all files exist: `ls -la analytics_pipeline/`, `ls -la Dataset/`
- Ensure dataset images are not corrupted

---

**Last Updated:** November 22, 2025  
**Status:** ✅ TESTED AND WORKING
