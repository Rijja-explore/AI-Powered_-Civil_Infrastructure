# 🚀 QUICK START GUIDE - 3D GLB HEIGHTMAP

## ⚡ 5-MINUTE SETUP

### Step 1: Access the Application
```
Open Browser: http://localhost:3001
```

### Step 2: Navigate to 3D Heightmap
Click the **"3D Heightmap"** tab in the navigation

### Step 3: Upload an Image
- **Drag & Drop**: Drop image onto the upload area
- **Click Browse**: Select file manually
- Supported: JPG, PNG, GIF, BMP

### Step 4: Configure (Optional)
Click **"Advanced"** to customize:
- 🔧 Resolution: 100-500 pixels (default: 300)
- 📏 Height Scale: 2-30 units (default: 12)
- 🌊 Smoothing: 0-5 sigma (default: 1.2)

### Step 5: View & Download
- Rotate: **Left mouse drag**
- Zoom: **Scroll wheel**
- Pan: **Middle mouse drag**
- Download: Click **"Download GLB"** or **"Download STL"**

---

## 📊 FORMAT COMPARISON

| | GLB | STL |
|---|---|---|
| Colors | 🎨 Yes | ❌ No |
| File Size | 📦 Small | 📦 Large |
| Web | ⚡ Fast | 🐢 Slow |
| Print | ✅ OK | ✅ Better |
| Recommended | ⭐ YES | 👍 Legacy |

---

## 🔧 API REFERENCE

### Endpoint
```
POST /api/generate-3d-glb
```

### cURL Example
```bash
curl -X POST http://localhost:5002/api/generate-3d-glb \
  -F "image=@photo.jpg" \
  > model.glb
```

### With Parameters
```bash
curl -X POST "http://localhost:5002/api/generate-3d-glb?resize_to=400&height_scale=15" \
  -F "image=@photo.jpg" \
  > model.glb
```

### Response
- **Success**: Binary GLB file (MIME: `model/gltf-binary`)
- **Error**: JSON error message

---

## 📁 FILES CREATED/MODIFIED

```
✅ image_3d_heightmap.py        (NEW) Backend GLB generator
✅ Heightmap3D.jsx               (UPDATED) Enhanced React component
✅ finalwebapp_api.py            (UPDATED) Added /api/generate-3d-glb
✅ This guide                     (NEW) Documentation
```

---

## ✅ WHAT'S WORKING

- ✅ Backend: Running on http://localhost:5002
- ✅ Frontend: Running on http://localhost:3001
- ✅ GLB Generation: Full textured 3D model creation
- ✅ STL Support: Legacy format still works
- ✅ Interactive Viewer: Full 3D controls
- ✅ File Download: GLB and STL export
- ✅ Advanced Settings: Parameter customization
- ✅ Drag-and-Drop: Easy file upload
- ✅ Error Handling: Graceful error messages
- ✅ Styling: Professional glass-morphism UI

---

## 🎯 EXAMPLE WORKFLOWS

### Workflow 1: Generate & View
```
1. Upload image → 2. View 3D → 3. Download
```

### Workflow 2: Optimize Quality
```
1. Upload → 2. Adjust resolution → 3. Increase height scale → 4. Download
```

### Workflow 3: Batch Processing (API)
```python
import requests

for image_file in image_list:
    with open(image_file, 'rb') as f:
        r = requests.post(
            'http://localhost:5002/api/generate-3d-glb',
            files={'image': f}
        )
        with open(f'{image_file}.glb', 'wb') as out:
            out.write(r.content)
```

---

## 📈 PARAMETER GUIDE

### Resolution (resize_to)
- **100**: Quick preview, low detail
- **300**: Balanced (default)
- **500**: High detail, large file

### Height Scale (height_scale)
- **2**: Flat surface
- **12**: Normal (default)
- **30**: Very pronounced

### Smoothing (smooth_sigma)
- **0**: No smoothing, sharp
- **1.2**: Natural (default)
- **5**: Very smooth

---

## 🐛 TROUBLESHOOTING

| Problem | Solution |
|---------|----------|
| "Module not found" | `pip install trimesh` |
| "Port already in use" | Kill process: `fuser -k 5002/tcp` |
| "Blank 3D viewer" | Check browser console, try different image |
| "Download doesn't work" | Check browser settings, allow pop-ups |
| "Slow performance" | Reduce resolution or smoothing |

---

## 💡 PRO TIPS

1. **Best Results**: Use high-contrast images with clear edges
2. **3D Printing**: Use STL format, adjust height scale for desired thickness
3. **Web Display**: Use GLB format, download for web distribution
4. **Performance**: Start with resolution=300, increase if needed
5. **Batch Processing**: Use API directly with Python scripts

---

## 📞 NEED HELP?

Check: `3D_GLB_INTEGRATION_COMPLETE.md` for detailed documentation

---

**Status**: ✅ READY TO USE  
**Version**: 2.0  
**Last Updated**: Nov 20, 2025
