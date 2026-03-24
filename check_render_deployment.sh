#!/bin/bash
# InfraVision AI - Render Deployment Preparation Script
# Run this before pushing to Render

echo "🚀 InfraVision AI - Render Deployment Checker"
echo "=============================================="
echo ""

# Check 1: Procfile exists
if [ -f "Procfile" ]; then
    echo "✅ Procfile exists"
else
    echo "❌ Procfile missing"
    exit 1
fi

# Check 2: requirements.txt exists
if [ -f "requirements.txt" ]; then
    echo "✅ requirements.txt exists"
    # Check for gunicorn
    if grep -q "gunicorn" requirements.txt; then
        echo "  ✅ gunicorn included"
    else
        echo "  ⚠️  gunicorn missing - add: echo 'gunicorn==21.2.0' >> requirements.txt"
    fi
else
    echo "❌ requirements.txt missing"
    exit 1
fi

# Check 3: .env file not in git
if [ -f ".env" ]; then
    if grep -q ".env" .gitignore 2>/dev/null; then
        echo "✅ .env in .gitignore"
    else
        echo "❌ .env exists and might be committed"
    fi
else
    echo "✅ No .env file (good - use .env.example)"
fi

# Check 4: .env.example exists
if [ -f ".env.example" ]; then
    echo "✅ .env.example exists"
else
    echo "⚠️  .env.example missing - helpful for Render"
fi

# Check 5: Git repository
if [ -d ".git" ]; then
    echo "✅ Git repository initialized"
    # Check if remote is set
    if git remote | grep -q origin; then
        echo "  ✅ GitHub remote configured"
    else
        echo "  ❌ GitHub remote not configured"
    fi
else
    echo "❌ Git repository not initialized"
    echo "  Run: git init"
    exit 1
fi

# Check 6: Frontend build
if [ -d "frontend/build" ]; then
    echo "✅ Frontend build exists"
else
    echo "⚠️  Frontend build missing"
    echo "  Run: cd frontend && npm run build"
fi

# Check 7: Python dependencies check
echo ""
echo "📦 Checking Python dependencies..."

# Check for critical packages
for package in Flask Flask-CORS opencv-python ultralytics numpy pandas; do
    if grep -q "$package" requirements.txt; then
        echo "  ✅ $package"
    else
        echo "  ⚠️  $package might be missing"
    fi
done

echo ""
echo "=============================================="
echo "🎯 Deployment Checklist"
echo "=============================================="
echo ""
echo "Before pushing to GitHub:"
echo "  [ ] Run: pip install gunicorn python-dotenv"
echo "  [ ] Add to requirements.txt if needed"
echo "  [ ] Create Procfile with gunicorn command"
echo "  [ ] Update .gitignore to exclude .env"
echo "  [ ] Test locally: gunicorn -w 4 finalwebapp_api:app"
echo ""
echo "Before creating Render service:"
echo "  [ ] Push code to GitHub main branch"
echo "  [ ] Create Procfile in repo root"
echo "  [ ] Copy environment variables to Render dashboard"
echo "  [ ] Set REACT_APP_API_URL in frontend env vars"
echo ""
echo "After deployment:"
echo "  [ ] Test health endpoint: GET /api/health"
echo "  [ ] Check frontend loads without errors"
echo "  [ ] Verify API calls from frontend work"
echo "  [ ] Monitor logs for errors"
echo ""
echo "✨ Ready for Render deployment!"
