# 🎥 Frame-Wise Video Analysis Output Format

**Version**: 2.0  
**Updated**: March 25, 2026

---

## Real-Time Frame Output (Compact & Clean)

### Endpoint: `POST /api/capture_and_analyze`

**Purpose**: Capture single frame from camera and return quick analysis (every 2 seconds)

**Response Format** (Compact - Frame-Wise):
```json
{
  "success": true,
  "frame": "data:image/jpeg;base64,/9j/4AAQSkZJRg...",
  "analysis": {
    "cracks": 3,
    "severity": "Low",
    "material": "Brick",
    "confidence": 0.92,
    "growth_detected": false,
    "health_score": 85.5
  },
  "message": "Detected 3 cracks | Health: 85.5%"
}
```

### Frame Analysis Fields Explained

| Field | Type | Meaning | Range |
|-------|------|---------|-------|
| `cracks` | int | Number of cracks detected | 0+ |
| `severity` | string | Overall severity level | "Low", "Medium", "High" |
| `material` | string | Predicted material type | "Brick", "Concrete", "Stone", etc. |
| `confidence` | float | Material classification confidence | 0.0 - 1.0 |
| `growth_detected` | bool | Biological growth present | true/false |
| `health_score` | float | Structural health score | 0 - 100 |

---

## Usage Examples

### 1. Real-Time Camera Capture (Every 2 Seconds)
```javascript
// Frontend: VideoAnalysis.jsx
setInterval(async () => {
  const response = await fetch('http://localhost:5002/api/capture_and_analyze', {
    method: 'POST'
  });
  
  const data = await response.json();
  
  if (data.success) {
    // Display frame
    displayFrame(data.frame);
    
    // Show quick stats
    console.log(`Frame Analysis:`);
    console.log(`  Cracks: ${data.analysis.cracks}`);
    console.log(`  Health: ${data.analysis.health_score}%`);
    console.log(`  Material: ${data.analysis.material}`);
  }
}, 2000); // Every 2 seconds
```

### 2. Frame-Wise Video File Processing
```javascript
// Upload video and process frames
POST /api/analyze_video
Input: { video: File }

Response:
{
  "frame_results": {
    "0": {           // Frame 0
      "timestamp": 0.0,
      "crack_detection": { "count": 2 },
      "data_science_insights": { "structural_health_score": 88 }
    },
    "10": {          // Frame 10
      "timestamp": 0.333,
      "crack_detection": { "count": 3 },
      "data_science_insights": { "structural_health_score": 85 }
    }
    // ... more frames
  }
}
```

### 3. Frontend Display
```jsx
// Show frame-by-frame results
{frameResults[currentFrame] && (
  <div className="frame-results">
    <h3>Frame {currentFrame}</h3>
    
    <div className="metrics">
      <div className="metric">
        <span>Cracks</span>
        <strong>{frameResults[currentFrame].crack_detection.count}</strong>
      </div>
      
      <div className="metric">
        <span>Health Score</span>
        <strong>{frameResults[currentFrame].data_science_insights.structural_health_score}%</strong>
      </div>
      
      <div className="metric">
        <span>Severity</span>
        <strong>{getSeverity(frameResults[currentFrame].crack_detection.count)}</strong>
      </div>
    </div>
  </div>
)}
```

---

## API Error Codes (Frame Analysis)

| Code | Message | Solution |
|------|---------|----------|
| 200 | Success | Frame analyzed successfully |
| 400 | "Camera not connected" | Call /api/connect_camera first |
| 500 | "Failed to capture frame" | Check camera hardware/permissions |
| 500 | Analysis error | Backend issue, check logs |

---

## Frame Processing Workflow

```
User clicks "Start Real-Time"
         ↓
Connect Camera (/api/connect_camera)
         ↓
Start Interval (every 2 seconds)
         ↓
Capture Frame (/api/capture_and_analyze)
         ↓
Get Frame-Wise Results:
├─ Current frame as image
├─ Crack count
├─ Health score (0-100%)
├─ Material type
└─ Quick message
         ↓
Display in UI
         ↓
Repeat every 2 seconds
```

---

## Performance Metrics

| Metric | Value | Notes |
|--------|-------|-------|
| Frame Capture | <500ms | Quick capture from camera |
| AI Analysis | 1-2s | Per frame inference time |
| Total per Frame | 1.5-2.5s | Include encode + upload |
| Update Rate | Every 2s | Responsive but not overwhelming |
| Memory per Frame | ~2MB | One JPEG at a time |

---

## Frame Storage (Optional)

If you want to keep historical frame data:
```python
frame_history = {
  "timestamp_1": frame_data_1,
  "timestamp_2": frame_data_2,
  # ... keeps growing
}
```

**Warning**: Frame data grows quickly! 
- 30 frames × 2MB = 60MB per minute
- Consider clearing old frames or using database

---

## Troubleshooting Frame Analysis

### Q: Frame analysis returns "Camera not connected"
**A**: You must call `POST /api/connect_camera` first
```javascript
await fetch('http://localhost:5002/api/connect_camera', { method: 'POST' });
```

### Q: Frame analysis is slow (>3 seconds)
**A**: 
- AI models take 1-2s per frame (normal)
- Check CPU/GPU usage
- Reduce image resolution if custom camera

### Q: Frames are black/empty
**A**:
- Check camera initialization
- Verify camera permissions in Windows
- Try: `python -c "import cv2; print(cv2.VideoCapture(0).isOpened())"`

### Q: Crack count keeps at 0
**A**:
- Model confidence threshold too high
- Try adjusting py_to_cm_ratio parameter
- Check image quality/brightness

---

## Advanced: Custom Frame Analysis

### Capture and Save Frames
```python
# In backend, add to capture_and_analyze():
frame_timestamp = datetime.now().isoformat()
cv2.imwrite(f'frames/{frame_timestamp}.jpg', frame)
```

### Batch Process Frames
```javascript
// Process multiple frames at once
for (let i = 0; i < 10; i++) {
  const result = await captureFrame();
  results.push(result);
  await sleep(2000); // 2-second interval
}
```

### Export Frame Data
```javascript
// Download frame analysis as CSV
const csv = frameResults.map(f => 
  `${f.timestamp},${f.cracks},${f.health_score}`
).join('\n');

downloadCSV(csv, 'frame-analysis.csv');
```

---

## Status: ✅ Ready for Use

- ✅ Compact frame-wise output
- ✅ Real-time capture (every 2s)
- ✅ Clean API response
- ✅ Error handling
- ✅ Performance optimized

**Next Step**: Restart frontend and backend, then test video analysis
```bash
# Backend
python finalwebapp_api.py

# Frontend (new terminal)
cd frontend
npm start
```

---

**Documentation**: Frame-wise video analysis format  
**Last Updated**: March 25, 2026
