# 🚀 InfraVision AI - Render Deployment Guide

## Overview
This guide covers deploying your InfraVision AI project on Render:
- **Backend**: Flask API on Render Web Service
- **Frontend**: React on Render Static Site
- **Database**: PostgreSQL on Render (optional)

---

## 📋 Prerequisites

Before starting, you need:
1. **Render Account** - Sign up at https://render.com
2. **GitHub Account** - Push code to GitHub (Render integrates via GitHub)
3. **Credit Card** - For paid tier (free tier has limitations)

---

## 🔧 Step 1: Prepare Your Project for Deployment

### 1.1 Create Production Build (Frontend)

```bash
cd frontend
npm run build
```

This creates an optimized `build/` folder.

### 1.2 Create `.env.production` (Frontend)

In `frontend/` folder, create `.env.production`:

```env
REACT_APP_API_URL=https://your-backend-service.onrender.com
```

Replace `your-backend-service` with your actual Render backend service name.

### 1.3 Create `Procfile` (Backend)

In root folder, create `Procfile`:

```
web: gunicorn -w 4 -b 0.0.0.0:$PORT finalwebapp_api:app
```

This tells Render how to start your Flask app.

### 1.4 Update `requirements.txt` (Backend)

Add these production dependencies:

```
gunicorn==21.2.0
python-dotenv==1.0.0
```

Your requirements.txt already has most dependencies, but ensure it includes:
```
Flask==3.0.0
Flask-CORS==4.0.0
opencv-python==4.9.0
```

### 1.5 Create `.env` Template (Backend)

In root folder, create `render.env` (don't commit, use for reference):

```env
# Flask Configuration
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=your-secret-key-here
PORT=10000

# CORS Configuration
CORS_ORIGINS=https://your-frontend-domain.onrender.com

# Database (if using)
DATABASE_URL=postgresql://user:password@host:5432/dbname

# API Configuration
API_PORT=5002
MAX_CONTENT_LENGTH=52428800
MAX_VIDEO_SIZE=1000
```

---

## 🌐 Step 2: Push Code to GitHub

### 2.1 Create GitHub Repository

```bash
git init
git add .
git commit -m "Initial commit for Render deployment"
git branch -M main
git remote add origin https://github.com/yourusername/infravision-ai.git
git push -u origin main
```

### 2.2 `.gitignore` Update

Ensure `.gitignore` includes:

```
venv/
.env
.env.local
node_modules/
build/
*.pyc
__pycache__/
.DS_Store
uploads/
runs/
segmentation_outputs/
.cache/
```

---

## 🎯 Step 3: Deploy Backend on Render

### 3.1 Create New Web Service

1. Go to https://dashboard.render.com
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Fill in:
   - **Name**: `infravision-ai-backend`
   - **Repository**: Select your repo
   - **Branch**: `main`
   - **Runtime**: `Python 3`
   - **Root Directory**: `.` (leave empty)
   - **Build Command**: 
     ```
     pip install -r requirements.txt
     ```
   - **Start Command**: 
     ```
     gunicorn -w 4 -b 0.0.0.0:$PORT finalwebapp_api:app
     ```

### 3.2 Environment Variables

In the Web Service settings, add Environment Variables:

```
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=your-super-secret-key-12345
CORS_ORIGINS=https://your-frontend-domain.onrender.com
MAX_CONTENT_LENGTH=52428800
```

### 3.3 Plan & Deploy

1. Select plan:
   - **Free**: Starts at $0/month but spins down after 15 min inactivity
   - **Starter**: $7/month (recommended)
   - **Standard**: $25+/month (production)

2. Click **"Create Web Service"**

3. Render will automatically:
   - Install dependencies
   - Build your app
   - Deploy to `https://infravision-ai-backend.onrender.com`

Monitor the deployment in **Logs** tab.

---

## 🎨 Step 4: Deploy Frontend on Render

### 4.1 Create Static Site

1. Go to https://dashboard.render.com
2. Click **"New +"** → **"Static Site"**
3. Fill in:
   - **Name**: `infravision-ai-frontend`
   - **Repository**: Select same repo
   - **Branch**: `main`
   - **Root Directory**: `frontend`
   - **Build Command**: 
     ```
     npm install && npm run build
     ```
   - **Publish Directory**: 
     ```
     build
     ```

### 4.2 Environment Variables

Add in the Static Site settings:

```
REACT_APP_API_URL=https://infravision-ai-backend.onrender.com
```

### 4.3 Deploy

1. Click **"Create Static Site"**
2. Render builds and deploys to `https://infravision-ai-frontend.onrender.com`

---

## 🔗 Step 5: Update API CORS

Since frontend URL changes, update backend `finalwebapp_api.py`:

Find the CORS configuration (around line 100-150):

```python
from flask_cors import CORS

# Development CORS settings
if os.getenv('FLASK_ENV') == 'production':
    cors_origins = os.getenv('CORS_ORIGINS', 'https://infravision-ai-frontend.onrender.com').split(',')
else:
    cors_origins = ['http://localhost:3000', 'http://localhost:5002']

CORS(app, origins=cors_origins, supports_credentials=True)
```

Or simply allow all origins (less secure):

```python
CORS(app, resources={r"/api/*": {"origins": "*"}})
```

---

## ⚙️ Step 6: Critical Configuration for Render

### 6.1 Memory & Compute Limits

Render has memory limitations for free/starter tiers:

Edit `finalwebapp_api.py` to handle limits:

```python
# Reduce model loading overhead
import warnings
warnings.filterwarnings('ignore')

# Lazy load heavy models
def load_models_on_demand():
    global YOLO_MODEL
    if YOLO_MODEL is None:
        from ultralytics import YOLO
        YOLO_MODEL = YOLO("yolov8n.pt")  # Use nano model for memory
    return YOLO_MODEL
```

### 6.2 Startup Timeout

Render has a 15-minute startup window. If models take time to load:

```python
# Preload models at startup (in main app initialization)
if __name__ == '__main__':
    try:
        load_models_on_demand()
        app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)))
    except Exception as e:
        print(f"Startup error: {e}")
```

### 6.3 Request Timeout

Add to `finalwebapp_api.py`:

```python
from werkzeug.exceptions import RequestTimeout

@app.errorhandler(RequestTimeout)
def handle_timeout(e):
    return jsonify({"error": "Request timeout"}), 408
```

### 6.4 Static File Serving

For React build files, ensure Flask serves them:

```python
from flask import send_from_directory

@app.route('/')
def index():
    return send_from_directory('build', 'index.html')

@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(f'build/{path}'):
        return send_from_directory('build', path)
    return send_from_directory('build', 'index.html')
```

---

## 🗄️ Step 7: Database Setup (Optional)

### 7.1 Create PostgreSQL on Render

1. Dashboard → **"New +"** → **"PostgreSQL"**
2. Configuration:
   - **Name**: `infravision-db`
   - **Region**: Same as backend
   - **PostgreSQL Version**: 15

3. Copy connection string from Info tab

4. Add to backend environment variables:
   ```
   DATABASE_URL=postgresql://yourusername:yourpassword@dpg-xxxxx.onrender.com:5432/infravision_db
   ```

### 7.2 Update Backend Connection

```python
import os
from sqlalchemy import create_engine

DATABASE_URL = os.getenv('DATABASE_URL')

if DATABASE_URL:
    engine = create_engine(DATABASE_URL, pool_pre_ping=True)
else:
    # Use SQLite locally
    engine = create_engine('sqlite:///app.db')
```

---

## 📊 Step 8: Monitoring & Logs

### View Logs
1. Dashboard → Select service
2. Click **"Logs"** tab
3. Monitor real-time output

### Common Issues

**Issue**: "ModuleNotFoundError: No module named 'cv2'"
```
Solution: cv2 needs system libraries. Add to build command:
pip install opencv-python-headless (instead of opencv-python)
```

**Issue**: "Out of memory"
```
Solution: 
- Upgrade to Starter tier ($7/month)
- Or optimize model (use YOLOv8n instead of YOLOv8s)
```

**Issue**: "CORS Error"
```
Solution: Update CORS_ORIGINS environment variable with frontend URL
```

---

## 🚀 Step 9: Custom Domain (Optional)

### 9.1 Point Domain to Render

1. Dashboard → Service → **"Settings"** → **"Custom Domain"**
2. Add your domain: `api.yourdomain.com`
3. Follow DNS instructions in your domain provider
4. Render provides free SSL certificate

---

## ✅ Step 10: Verify Deployment

### Backend Health Check

```bash
curl https://infravision-ai-backend.onrender.com/api/health
```

Expected response:
```json
{
  "status": "ok",
  "api_version": "2.0",
  "timestamp": "2026-03-25T12:00:00Z"
}
```

### Frontend Access

Visit: `https://infravision-ai-frontend.onrender.com`

Expected:
- ✅ Page loads without errors
- ✅ Console has no CORS errors
- ✅ API calls to backend succeed
- ✅ Real-time features show live data

---

## 📝 Deployment Checklist

Before going live:

- [ ] GitHub repository public and synced
- [ ] `.env` variables NOT in repo (use .gitignore)
- [ ] `Procfile` committed to repo root
- [ ] `requirements.txt` updated with gunicorn
- [ ] Backend env variables set on Render
- [ ] Frontend API URL points to backend
- [ ] CORS configured for frontend domain
- [ ] Models can load within memory limits
- [ ] Database configured (if needed)
- [ ] Health check endpoint working
- [ ] Logs accessible and monitored
- [ ] Domain configured (custom or Render subdomain)

---

## 🎯 Quick Reference: URLs After Deployment

| Component | URL |
|-----------|-----|
| Backend API | https://infravision-ai-backend.onrender.com |
| Frontend | https://infravision-ai-frontend.onrender.com |
| Database | postgresql://host:5432/db |
| API Health | https://infravision-ai-backend.onrender.com/api/health |
| Video Upload | https://infravision-ai-backend.onrender.com/api/analyze_video |

---

## 💡 Cost Breakdown

| Tier | Backend | Frontend | Database | Total/Month |
|------|---------|----------|----------|-------------|
| Free | $0 (limited) | $0 (limited) | N/A | $0 |
| Starter | $7 | $0 (included) | $7 | $14 |
| Standard | $25+ | Included | $15+ | $40+ |

- Free tier: Suitable for testing, spins down after 15 min
- Starter: Recommended for small deployments
- Standard: Recommended for production

---

## 🆘 Getting Help

### Render Support
- **Docs**: https://render.com/docs
- **Status Page**: https://status.render.com
- **Community**: https://community.render.com

### Debugging Tips

1. Check logs in real-time:
   ```
   Dashboard → Service → Logs (tail last 1000 lines)
   ```

2. Rebuild deployment:
   ```
   Dashboard → Service → Manual Deploy → Deploy latest commit
   ```

3. Restart service:
   ```
   Dashboard → Service → Settings → Restart Instance
   ```

4. Check environment variables:
   ```
   Dashboard → Service → Environment
   ```

---

## 📌 Final Notes

- **Auto-deploy**: Render auto-deploys on git push to main
- **Cold starts**: Free tier may have 30-60 sec cold starts
- **Scaling**: Upgrade tier for better performance/uptime
- **SSL**: Free HTTPS certificate provided
- **Backups**: Database backups available (paid feature)

**Your deployed app will be live at:**
- 🌐 Frontend: https://infravision-ai-frontend.onrender.com
- 🔌 Backend: https://infravision-ai-backend.onrender.com
