# API Configuration Guide

## Local Development

The frontend is configured to connect to the backend API on port 7860:
- `REACT_APP_API_URL=http://localhost:7860`

Make sure your Flask backend is running on this port:
```bash
python -m flask run --host=0.0.0.0 --port=7860
```

## Production Deployment (Vercel)

For the deployed frontend on Vercel (https://infravision-kohl.vercel.app/), configure the backend API URL:

### Steps:
1. Go to your Vercel project settings
2. Navigate to **Environment Variables**
3. Add a new environment variable:
   - **Name:** `REACT_APP_API_URL`
   - **Value:** Your deployed backend URL (e.g., `https://<username>-infravision-api.hf.space`)
   - **Environments:** Select "Production"
4. Redeploy your application

## Available Configuration Files

- `.env` - Local development settings
- `.env.production` - Production template (update with your actual backend URL in Vercel UI)

## Supported Environment Variables

- `REACT_APP_API_URL` - The backend API base URL (defaults to http://localhost:7860 in development)

---

## Material Classification API

### Endpoint
```
POST /api/analyze-image
```

### Request
```javascript
const formData = new FormData();
formData.append('image', imageFile);

const response = await fetch(`${API_URL}/api/analyze-image`, {
  method: 'POST',
  body: formData
});

const result = await response.json();
```

### Response
```json
{
  "success": true,
  "image_size": "1920x1080",
  "crack_analysis": {
    "crack_count": 3,
    "total_pixels": 45230,
    "total_area_cm2": 12.5,
    "average_width_cm": 2.3
  },
  "material_classification": {
    "material": "Concrete",
    "probabilities": {
      "Brick": 0.05,
      "Concrete": 0.85,
      "Stone": 0.05,
      "Sandstone": 0.02,
      "Marble": 0.01,
      "Plaster": 0.01,
      "Wood": 0.005,
      "Metal": 0.005
    }
  },
  "segmentation": {
    "class_counts": {"crack": 45, "discolouration": 12}
  },
  "processed_image": "data:image/jpeg;base64,..."
}
```

### Material Classes
1. **Brick** - Common in masonry structures
2. **Concrete** - Prevalent in modern infrastructure
3. **Stone** - Natural stone surfaces
4. **Sandstone** - Sedimentary stone
5. **Marble** - Premium stone finishes
6. **Plaster** - Finished surfaces
7. **Wood** - Timber structures
8. **Metal** - Steel/iron elements

---

## Backend Deployment (Hugging Face)
