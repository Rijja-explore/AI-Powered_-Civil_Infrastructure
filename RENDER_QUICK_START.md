# 🚀 InfraVision AI - Render Deployment Quick Start

## ⚡ 5-Minute Quick Deploy

### Step 1: Prepare Your Machine (2 min)

```bash
# Ensure requirements are in git
cd d:\AI-Powered_Civil_Infrastructure
git status

# Add gunicorn to requirements
pip install gunicorn python-dotenv
pip freeze >> requirements.txt

# Build frontend
cd frontend
npm run build
cd ..

# Commit changes
git add .
git commit -m "Prepare for Render deployment"
git push origin main
```

### Step 2: Create Render Account (1 min)
- Go to https://render.com
- Sign up with GitHub
- Authorize GitHub access

### Step 3: Deploy Backend (1 min)

1. Dashboard → "New +" → "Web Service"
2. Select your GitHub repo
3. Settings:
   ```
   Name: infravision-ai-backend
   Runtime: Python
   Build: pip install -r requirements.txt
   Start: gunicorn -w 4 -b 0.0.0.0:$PORT finalwebapp_api:app
   Plan: Starter ($7/month)
   ```
4. Click "Create Web Service"
5. Wait ~2-3 minutes for deployment

### Step 4: Deploy Frontend (1 min)

1. Dashboard → "New +" → "Static Site"
2. Select your GitHub repo
3. Settings:
   ```
   Name: infravision-ai-frontend
   Root: frontend
   Build: npm install && npm run build
   Publish: build
   Plan: Free
   ```
4. Click "Create Static Site"
5. Wait ~1-2 minutes for deployment

### Step 5: Connect Frontend to Backend (Instant)

1. Note your backend URL: `https://infravision-ai-backend.onrender.com`
2. Go to Frontend Static Site settings
3. Add environment variable:
   ```
   REACT_APP_API_URL = https://infravision-ai-backend.onrender.com
   ```
4. Redeploy (Dashboard → Deployments → Deploy latest)

---

## 📋 Files You Created

✅ `Procfile` - Flask app startup configuration
✅ `.env.example` - Environment variables template
✅ `render.yaml` - Infrastructure as code (optional)
✅ `.gitignore` - Excludes sensitive files from git
✅ `RENDER_DEPLOYMENT_GUIDE.md` - Full detailed guide

---

## 🔧 Configuration Files

### Procfile (Already Created)
```
web: gunicorn -w 4 -b 0.0.0.0:$PORT finalwebapp_api:app
```

### Render Environment Variables for Backend

```
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=your-secret-key-here-12345
CORS_ORIGINS=https://infravision-ai-frontend.onrender.com
MAX_CONTENT_LENGTH=52428800
MAX_FRAMES_TO_PROCESS=8
```

### Render Environment Variables for Frontend

```
REACT_APP_API_URL=https://infravision-ai-backend.onrender.com
REACT_APP_ENV=production
```

---

## ✅ Deployment Checklist

```
PREPARATION
[ ] Procfile created in repo root
[ ] gunicorn added to requirements.txt
[ ] .env NOT in git (check .gitignore)
[ ] .env.example created with template
[ ] git add . && git commit && git push origin main

BACKEND DEPLOYMENT
[ ] Create Web Service on Render
[ ] Select your GitHub repo
[ ] Runtime: Python
[ ] Build Command: pip install -r requirements.txt
[ ] Start Command: gunicorn -w 4 -b 0.0.0.0:$PORT finalwebapp_api:app
[ ] Set environment variables
[ ] Select Starter plan ($7/month)
[ ] Wait for "Live" status

FRONTEND DEPLOYMENT
[ ] Create Static Site on Render
[ ] Select your GitHub repo
[ ] Root Directory: frontend
[ ] Build: npm install && npm run build
[ ] Publish: build
[ ] Set REACT_APP_API_URL to backend URL
[ ] Select Free plan
[ ] Wait for "Live" status

VERIFICATION
[ ] Test backend: curl https://backend-url.onrender.com/api/health
[ ] Visit frontend: https://frontend-url.onrender.com
[ ] Check console (F12) for no CORS errors
[ ] Try uploading a video
[ ] Check logs for errors
```

---

## 🔗 Your Live URLs

After deployment, you'll have:

| Service | URL |
|---------|-----|
| Backend API | `https://infravision-ai-backend.onrender.com` |
| Frontend App | `https://infravision-ai-frontend.onrender.com` |
| Health Check | `https://infravision-ai-backend.onrender.com/api/health` |
| Video Upload | `https://infravision-ai-backend.onrender.com/api/analyze_video` |

---

## 🆘 Common Issues & Solutions

### Issue: "No module named 'gunicorn'"
**Solution**: Add `gunicorn==21.2.0` to `requirements.txt`:
```bash
echo "gunicorn==21.2.0" >> requirements.txt
git add requirements.txt && git commit -m "Add gunicorn" && git push
```

### Issue: "CORS Error" in Console
**Solution**: Update backend environment variable:
```
CORS_ORIGINS=https://your-frontend-url.onrender.com
```
Then redeploy backend.

### Issue: "Request Timeout" on video upload
**Solution**: 
- Upgrade to Starter tier (better CPU/RAM)
- Reduce MAX_FRAMES_TO_PROCESS
- Optimize ML models

### Issue: "Out of Memory"
**Solution**:
- Use YOLOv8 nano model (lighter)
- Upgrade to Starter tier ($7/month)
- Limit concurrent uploads

### Issue: Models not loading
**Solution**: Check startup logs:
```
Dashboard → Backend Service → Logs
Look for model loading errors
```

---

## 📊 Cost Estimation

| Component | Tier | Price/Month |
|-----------|------|-------------|
| Backend | Starter | $7 |
| Frontend | Free | $0 |
| Database (optional) | Starter | $7 |
| **Total** | | **$7-14** |

**Billing Tips:**
- Free tier suitable for testing only
- Starter tier recommended for production
- Free tier spins down after 15 min inactivity

---

## 🚀 Next Steps

1. ✅ Review [RENDER_DEPLOYMENT_GUIDE.md](./RENDER_DEPLOYMENT_GUIDE.md) for detailed instructions
2. ✅ Set up GitHub repository with proper .gitignore
3. ✅ Configure environment variables in Render dashboard
4. ✅ Deploy backend and note the URL
5. ✅ Deploy frontend with backend URL
6. ✅ Test health endpoint
7. ✅ Monitor logs for issues
8. ✅ Configure custom domain (optional)

---

## 📞 Support Resources

- **Render Docs**: https://render.com/docs
- **GitHub Actions**: https://github.com/features/actions
- **Python Deployment**: https://docs.python-guide.org/scenarios/web/
- **React Deployment**: https://create-react-app.dev/deployment/render/

---

## ✨ You're Ready to Deploy!

All configuration files are in place. Just push to GitHub and watch it deploy automatically! 🎉

Questions? Check the detailed guide: [RENDER_DEPLOYMENT_GUIDE.md](./RENDER_DEPLOYMENT_GUIDE.md)
