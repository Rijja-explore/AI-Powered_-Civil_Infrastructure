# InfraVision AI - Complete Render Deployment Guide

Deploy your full-stack AI infrastructure monitoring system on Render.com as a single integrated project.

---

## 📋 Prerequisites

Before starting, ensure you have:

1. ✅ **GitHub Account** - Repository pushed with all code
2. ✅ **Render Account** - Free tier available at [render.com](https://render.com)
3. ✅ **Git configured** - For deployment webhooks
4. ✅ **Project up-to-date** - All changes pushed to `main` branch

---

## 🚀 Step-by-Step Deployment

### **Step 1: Prepare Your GitHub Repository**

Ensure your latest code is pushed:

```bash
cd d:\AI-Powered_Civil_Infrastructure
git status
git add .
git commit -m "Ready for Render deployment"
git push origin main
```

**Verify on GitHub:**
- Go to https://github.com/Rijja-explore/AI-Powered_Civil_Infrastructure
- Confirm `render.yaml`, `Procfile`, `requirements.txt`, and `frontend/` are visible

---

### **Step 2: Create Render Account & Connect GitHub**

1. **Sign up at** [render.com](https://render.com)
2. **Go to Dashboard** → Click **"New +"** button
3. **Select "Web Service"**
4. **Connect GitHub Repository:**
   - Click "Connect GitHub Account"
   - Authorize Render to access your repositories
   - Select `AI-Powered_Civil_Infrastructure` repository

---

### **Step 3: Deploy with render.yaml**

The `render.yaml` file contains the full configuration for both backend and frontend.

**Option A: Deploy from Dashboard (Recommended)**

1. **Create New Environment**
   - Click **"New +"** → **"Blueprint"**
   - Name: `InfraVision AI Full Stack`
   - Connect your GitHub repository
   - Branch: `main`

2. **Render will automatically read** `render.yaml` and create:
   - ✅ Backend API service (Python/Flask)
   - ✅ Frontend static site (React)
   - ✅ Automatic deployments on push

3. **Click "Deploy"** and wait for completion

---

### **Step 4: Manual Backend Service Setup (Alternative)**

If you prefer to configure manually:

1. **Create Backend Service:**
   - New Web Service
   - **Name:** `infravision-ai-backend`
   - **Environment:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn -w 4 -b 0.0.0.0:$PORT finalwebapp_api:app`
   - **Plan:** Starter ($7/month) or Standard
   - **Region:** US East (or nearest to you)
   - **Auto Deploy:** Enable

2. **Set Environment Variables:**
   - `FLASK_ENV` = `production`
   - `FLASK_DEBUG` = `False`
   - `CORS_ORIGINS` = `https://infravision-ai-frontend.onrender.com`
   - `MAX_CONTENT_LENGTH` = `52428800` (50MB for video uploads)
   - `MAX_FRAMES_TO_PROCESS` = `8` (limit concurrent frame processing)
   - `USE_GPU` = `False` (CPU inference for cost efficiency)

3. **Health Check:**
   - Add health check path: `/api/health`
   - Interval: 10 seconds
   - Timeout: 3 seconds

---

### **Step 5: Manual Frontend Service Setup (Alternative)**

1. **Create Static Site Service:**
   - New Static Site
   - **Name:** `infravision-ai-frontend`
   - **Build Command:** 
     ```bash
     cd frontend
     npm install
     npm run build
     ```
   - **Publish Directory:** `frontend/build`
   - **Plan:** Free
   - **Region:** US East
   - **Auto Deploy:** Enable

2. **Set Environment Variables:**
   - `REACT_APP_API_URL` = `https://infravision-ai-backend.onrender.com`
   - `REACT_APP_ENV` = `production`

3. **Add Redirect Rule (important!):**
   - Configure fallback to `index.html` for SPA routing:
     - In "Rewrites and Redirects"
     - Rewrite all to `/index.html` (for React Router)

---

## ✅ Verification & Testing

### **Step 1: Verify Backend is Running**

```bash
# Check health endpoint
curl https://infravision-ai-backend.onrender.com/api/health

# Expected response:
{
  "status": "success",
  "message": "API is running",
  "timestamp": "2026-03-26T..."
}
```

### **Step 2: Verify Frontend is Running**

1. Open https://infravision-ai-frontend.onrender.com
2. Should see homepage with navigation menu
3. Check browser console for no CORS errors

### **Step 3: Test Image Analysis**

1. Go to **Image Analysis** page
2. Upload a test image (JPG/PNG)
3. Click **Analyze**
4. Should process and show results in ~5-15 seconds

### **Step 4: Test API Connectivity**

In browser console:
```javascript
fetch('https://infravision-ai-backend.onrender.com/api/health')
  .then(r => r.json())
  .then(d => console.log(d))
```

---

## 🔧 Configuration & Optimization

### **Backend Performance Tuning**

**For CPU-bound ML inference:**

```yaml
# In render.yaml for backend service
envVars:
  - key: GUNICORN_WORKERS
    value: "4"  # Match CPU cores (Starter has 1 vCPU, use 2-4)
  - key: GUNICORN_THREADS
    value: "2"  # Enable threading for I/O
  - key: MAX_FRAMES_TO_PROCESS
    value: "8"  # Limit concurrent frame processing
```

### **Frontend Build Optimization**

```json
// frontend/package.json - Production build
{
  "scripts": {
    "build": "GENERATE_SOURCEMAP=false react-scripts build",
    "build:analyze": "source-map-explorer 'build/static/js/*.js'"
  }
}
```

### **Cost Optimization**

| Component | Render Plan | Monthly Cost |
|-----------|------------|--------------|
| Backend (Starter) | 1 vCPU, 0.5GB RAM | $7 |
| Frontend (Free) | Included | Free |
| Database (Optional) | Starter PostgreSQL | $7 |
| **Total** | - | **$7-14/month** |

**Cost-Saving Tips:**
- ✅ Use free frontend tier
- ✅ Starter plan for backend (sufficient for <100 users/day)
- ✅ CPU-based inference (no GPU)
- ✅ Enable native runtimes (faster cold starts)

---

## 📊 Monitoring & Debugging

### **View Logs**

1. **Backend Logs:**
   - Go to service dashboard
   - Click "Logs" tab
   - See Flask startup messages and API requests

2. **Frontend Logs:**
   - Open browser Developer Tools
   - Check "Console" for client errors
   - Check "Network" for API calls

### **Common Issues & Solutions**

#### **Issue: 502 Bad Gateway**

**Cause:** Backend service not responding
**Solution:**
```bash
# Check service is running
curl https://infravision-ai-backend.onrender.com/api/health

# If fails, check logs for:
- Import errors (missing packages)
- Port binding issues
- Memory/CPU exhaustion
```

#### **Issue: CORS Errors**

**Cause:** Frontend can't reach backend
**Solution:**
```bash
# Verify CORS_ORIGINS environment variable
CORS_ORIGINS=https://infravision-ai-frontend.onrender.com

# Test from browser console:
fetch('https://infravision-ai-backend.onrender.com/api/health', {
  headers: { 'Accept': 'application/json' }
})
```

#### **Issue: Slow Image Processing**

**Cause:** Starter plan CPU limitations
**Solution:**
- Upgrade to Standard plan ($12/month)
- Optimize model inference (quantization)
- Implement request queuing
- Use caching for repeated images

#### **Issue: Frontend Not Loading**

**Cause:** Build failed or incorrect publish path
**Solution:**
1. Check build logs for errors
2. Verify `frontend/build` exists locally
3. Ensure `npm run build` succeeds
4. Check publish directory = `frontend/build`

---

## 🔄 Continuous Deployment

### **Auto-Deploy on Git Push**

The system is configured to auto-deploy on changes:

```bash
# Any push to main branch triggers:
git push origin main

# Render automatically:
1. Detects changes via GitHub webhook
2. Pulls latest code
3. Runs build commands
4. Restarts services
5. Updates DNS (no downtime)
```

### **Manual Redeploy**

If needed, redeploy without code changes:

1. **Backend:** 
   - Dashboard → Service → Top-right menu → "Redeploy"

2. **Frontend:**
   - Dashboard → Static Site → Top-right menu → "Clear Cache and Redeploy"

---

## 📈 Performance Metrics

**Expected Performance on Starter Plan:**

| Metric | Value |
|--------|-------|
| **Cold Start** | 30-45 seconds (first request) |
| **Warm Response** | 2-5 seconds |
| **Image Analysis** | 5-15 seconds (YOLOv8 inference) |
| **Concurrent Users** | ~50-100 light users |
| **Max Upload Size** | 50MB (configured) |
| **API Response Time** | <2s for small operations |

**Scaling to Standard Plan:**

- More vCPU (faster inference)
- More RAM (handle larger models)
- Better concurrency
- ~$12/month per service

---

## 🔐 Security & Best Practices

### **Environment Variables**

Never commit credentials! Use Render's secret management:

1. Dashboard → Service → "Environment"
2. Click "Add Secret File" for sensitive data:
   ```
   # render.secret
   SECRET_KEY=your-secret-key-here
   DATABASE_URL=postgresql://...
   API_KEY=...
   ```

3. Reference in render.yaml:
   ```yaml
   - key: SECRET_KEY
     fromFile: render.secret
   ```

### **HTTPS & SSL**

✅ **Automatic** - Render provides free SSL certificates
- All traffic encrypted
- Automatic HTTP → HTTPS redirect

### **CORS Configuration**

Change CORS origins before production:

```yaml
# In render.yaml
CORS_ORIGINS: "https://your-frontend.onrender.com"
```

---

## 🎯 Post-Deployment Checklist

- [ ] Backend service running (health check passing)
- [ ] Frontend service deployed (static site loading)
- [ ] Both services visible in Render dashboard
- [ ] Image upload works (test with sample image)
- [ ] Analysis endpoint working (5-15 second processing)
- [ ] 3D visualization loads (Heightmap3D page)
- [ ] Real-time monitoring works (if camera available)
- [ ] Environment variables correctly set
- [ ] CORS errors resolved
- [ ] Database optional (currently not used)

---

## 🚀 Next Steps

1. **Monitor Performance:**
   - Watch logs for errors
   - Track response times
   - Monitor CPU/memory usage

2. **Optimize:**
   - Cache frequently analyzed images
   - Implement request queuing for videos
   - Use CDN for static assets (optional)

3. **Scale:**
   - Upgrade to Standard plan if needed
   - Add database for data persistence
   - Implement user authentication

4. **Enhance:**
   - Add API documentation (Swagger/OpenAPI)
   - Implement rate limiting
   - Add email notifications for alerts

---

## 📞 Support & Resources

- **Render Docs:** https://render.com/docs
- **Flask Deployment:** https://flask.palletsprojects.com/deployment/
- **React Deployment:** https://create-react-app.dev/deployment/render/
- **YOLOv8 Inference:** https://docs.ultralytics.com/

---

## 📝 Deployment History

| Date | Action | Status |
|------|--------|--------|
| 2026-03-26 | Initial guide created | ✅ Active |
| - | Backend deployed | Ready |
| - | Frontend deployed | Ready |

---

**Last Updated:** March 26, 2026

**Status:** 🟢 Ready for Production Deployment
