# 🚀 3D Heightmap Generator - Quick Start Guide

## Installation & Setup

### Step 1: Install Backend Dependencies
```bash
cd d:\Projects\AI-Powered_-Civil_Infrastructure

# Install Python packages
pip install -r requirements.txt

# Verify trimesh is installed
pip list | findstr trimesh
```

**Expected Output:**
```
trimesh                      3.21.0
```

---

### Step 2: Update Frontend Dependencies
```bash
cd frontend

# Update package.json with new 3D libraries
# (Already done - package.json was updated)

# Install npm packages
npm install --legacy-peer-deps
```

**Wait for completion** - This installs:
- `@react-three/fiber@^8.17.6`
- `@react-three/drei@^9.100.0`
- `three@^r128`

---

## Running the Application

### Terminal 1: Start Flask Backend
```bash
cd d:\Projects\AI-Powered_-Civil_Infrastructure
python finalwebapp_api.py
```

**Expected Output:**
```
🚀 Starting InfraVision AI API Server...
📍 Server will be available at: http://localhost:5002
✅ 3D heightmap module loaded successfully
✅ All models loaded successfully
```

### Terminal 2: Start React Frontend
```bash
cd d:\Projects\AI-Powered_-Civil_Infrastructure\frontend
npm start
```

**Expected Output:**
```
Compiled successfully!

You can now view infravision-ai-frontend in the browser.

  Local:            http://localhost:3000
  On Your Network:  http://192.168.x.x:3000
```

---

## Using 3D Heightmap Generator

### Step 1: Navigate to the Feature
1. Open http://localhost:3000 in your browser
2. Look for the **"3D Heightmap"** tab in the navigation (with Cube 🔷 icon)
3. Click on it to open the 3D Heightmap Generator

### Step 2: Upload an Image
Choose one of these methods:

**Method A: Click to Browse**
- Click the "Choose File" button
- Select a JPG, PNG, or other image format
- Image will auto-process

**Method B: Drag & Drop**
- Drag an image file directly onto the drop zone
- It will automatically start processing

**Supported Formats:**
- JPG / JPEG ✅
- PNG ✅
- GIF ✅
- BMP ✅
- WebP ✅

### Step 3: View the 3D Model
Once uploaded, you'll see:
- 3D interactive heightmap rendering
- Model information panel
- Control instructions

### Step 4: Interact with the 3D Model
**Mouse Controls:**
- **Left Click + Drag** → Rotate the model
- **Scroll Wheel** → Zoom in/out
- **Middle Click + Drag** → Pan the view
- **Right Click + Drag** → Alternative rotation

### Step 5: Download STL File
- Click **"📥 Download STL File"** button
- File `heightmap.stl` will be saved to Downloads folder
- Can be opened in CAD software or used for 3D printing

---

## What Each Button Does

| Button | Function |
|--------|----------|
| **Choose File** | Browse computer for image file |
| **📥 Download STL File** | Download the generated 3D model as STL format |
| **🔄 Generate New** | Clear current model and upload a new image |

---

## Understanding the Output

### Model Information Panel
Shows technical details about your 3D model:
- **Resolution:** 200 × 200 pixels (mesh size)
- **Height Scale:** 10.0 units (vertical exaggeration)
- **Smoothing:** Gaussian (σ=1.0) for noise reduction
- **Format:** STL (ASCII compatible with all CAD software)

### 3D Model Visualization
- **Color:** Blue with metallic sheen (Phong material)
- **Lighting:** 3-point lighting for optimal depth perception
- **Background:** Subtle gradient for visual appeal

---

## Features Showcase

The page includes a **Features** section explaining:

1. **🎨 Automatic Conversion** - 2D brightness → 3D height mapping
2. **🔍 Interactive Viewer** - Full 360° rotation and zoom controls
3. **💾 STL Export** - Compatible with 3D printers and CAD software
4. **⚙️ Advanced Processing** - Gaussian smoothing and optimization
5. **🏗️ Infrastructure Ready** - Perfect for structural health monitoring
6. **🚀 Real-time Processing** - Instant conversion and preview

---

## Advanced: STL File Usage

### For 3D Printing
1. Download the STL file
2. Open in 3D slicer software (Cura, PrusaSlicer, etc.)
3. Position and scale for your printer
4. Generate G-code and print

### For CAD Analysis
1. Download the STL file
2. Import into CAD software:
   - **Autodesk Fusion 360** - File → Open → Select STL
   - **FreeCAD** - File → Open → Select STL
   - **Blender** - File → Import → STL
3. Perform structural analysis or modification

### For Further Processing
```bash
# Convert STL to OBJ (using trimesh via Python)
python -c "
import trimesh
mesh = trimesh.load('heightmap.stl')
mesh.export('heightmap.obj')
"

# Convert to other formats: GLTF, PLY, OFF, etc.
```

---

## Troubleshooting

### Issue: "Cannot find module 'three'" or similar npm error
**Solution:**
```bash
cd frontend
npm install --legacy-peer-deps
npm start
```

### Issue: "No image file provided" error
**Solution:**
- Make sure you selected a valid image file
- Try a different image format (JPG instead of PNG, etc.)
- Ensure file size is reasonable (< 10 MB)

### Issue: 3D model appears blank or doesn't load
**Solution:**
1. Check browser console (F12 → Console tab)
2. Verify backend is running: Open http://localhost:5002/api/health
3. Check network tab for failed requests
4. Try uploading a simpler image

### Issue: "Failed to generate 3D model" error
**Solution:**
- Backend may be offline
- Try restarting Flask API: `python finalwebapp_api.py`
- Check that trimesh is properly installed: `pip install trimesh`

### Issue: Downloaded STL file is too large
**Solution:**
- STL files are typically larger than expected (especially ASCII format)
- This is normal; file size depends on image resolution
- For smaller files, use binary STL (future enhancement)

---

## Performance Tips

### Optimization
- Use 200×200 resolution (default) for balance of quality and performance
- Larger resolutions (512×512) will generate slower but with more detail
- Gaussian smoothing (σ=1.0) reduces noise without over-smoothing

### Browser Tips
- Use Chrome, Firefox, or Edge for best 3D rendering performance
- Close other heavy applications to improve responsiveness
- If model is laggy, try lowering screen resolution temporarily

---

## Integration with Other Features

The 3D Heightmap Generator **complements** existing features:

| Feature | Purpose | Workflow |
|---------|---------|----------|
| **Image Analysis** | Crack detection, growth analysis | Upload image → Get 2D analysis |
| **3D Heightmap** | 3D visualization, structural modeling | Upload same image → Get 3D model |
| **Video Analysis** | Real-time monitoring | Stream video → Extract frames → Use in heightmap |

### Combined Workflow Example
1. Use **Image Analysis** to detect cracks and growth
2. Use **3D Heightmap** on the same image to visualize surface topology
3. Download STL and compare 3D structure with 2D analysis results
4. Export both reports for comprehensive documentation

---

## API Endpoint Reference

### Backend Endpoint

**POST** `/api/generate-3d-heightmap`

**Request:**
```
Content-Type: multipart/form-data
Field Name: "image"
Field Value: [binary image file]
```

**Success Response (200):**
```
Content-Type: model/stl
Content-Disposition: attachment; filename=heightmap.stl
Body: Binary STL mesh data
```

**Error Response (400/500):**
```json
{
  "error": "Descriptive error message"
}
```

**Example using cURL:**
```bash
curl -X POST http://localhost:5002/api/generate-3d-heightmap \
  -F "image=@path/to/image.jpg" \
  -o heightmap.stl
```

---

## Support & Resources

### Documentation Files
- `3D_HEIGHTMAP_INTEGRATION.md` - Full technical documentation
- `image_to_heightmap.py` - Source code with detailed comments
- `frontend/src/pages/Heightmap3D.jsx` - React component source

### External Resources
- **Three.js Documentation:** https://threejs.org/docs/
- **React Three Fiber:** https://docs.pmnd.rs/react-three-fiber/
- **trimesh Documentation:** https://trimsh.org/
- **STL Format:** https://en.wikipedia.org/wiki/STL_(file_format)

---

## Quick Reference

| Command | Purpose |
|---------|---------|
| `python finalwebapp_api.py` | Start Flask backend |
| `npm start` | Start React frontend |
| `pip install trimesh` | Install 3D mesh library |
| `npm install --legacy-peer-deps` | Install frontend dependencies |
| `http://localhost:3000` | Access web application |
| `http://localhost:5002` | Access backend API |

---

## Success Checklist

- ✅ Backend running at http://localhost:5002
- ✅ Frontend running at http://localhost:3000
- ✅ **"3D Heightmap"** tab visible in navigation
- ✅ Can upload image files
- ✅ 3D model renders in browser
- ✅ Can rotate/zoom the model
- ✅ Can download STL file
- ✅ STL file opens in CAD software or 3D viewer

---

## Next Steps

1. **Test with sample images:** Try different structural photos
2. **Experiment with parameters:** Modify smoothing or height scale in code
3. **Integrate with workflows:** Use alongside Image Analysis and Video Analysis
4. **Export for analysis:** Download STL and use in CAD/3D printing software
5. **Share results:** Export both 2D analysis and 3D models for reports

---

**Ready to go! 🚀 Enjoy exploring 3D infrastructure visualization!**
