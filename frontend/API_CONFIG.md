# API Configuration Guide

## Local Development

The frontend is configured to connect to the backend API on port 7860:
- `REACT_APP_API_URL=http://localhost:7860`

Make sure your Flask backend is running on this port:
```bash
python -m flask run --host=0.0.0.0 --port=7860
```

## Production Deployment (Vercel)

For the deployed frontend on Vercel (https://infravision-kohl.vercel.app/), you need to set the backend API URL:

### Steps:
1. Go to your Vercel project settings
2. Navigate to **Environment Variables**
3. Add a new environment variable:
   - **Name:** `REACT_APP_API_URL`
   - **Value:** Your deployed backend URL (e.g., `https://your-backend-domain.huggingface.co`)
   - **Environments:** Select "Production"
4. Redeploy your application

## Available Configuration Files

- `.env` - Local development settings
- `.env.production` - Production template (update with your actual backend URL in Vercel UI)

## Supported Environment Variables

- `REACT_APP_API_URL` - The backend API base URL (defaults to http://localhost:7860 in development)
