# Analytics Backend API Specification

This document specifies the backend API endpoints required for the comprehensive Analytics dashboard.

## Required Endpoints

### 1. `/api/analytics/dataset` (GET or POST)

**Purpose:** Returns dataset-level statistics from the crack_preprocess and vegetation_preprocess folders.

**Dataset Path:** `D:/Projects/AI-Powered_-Civil_Infrastructure/Dataset/`
- `crack_preprocess/` (train, test, valid subfolders)
- `vegetation_preprocess/` (train, test, valid subfolders)

**Sample Response:**
```json
{
  "total_images": 2458,
  "crack_count": 1247,
  "vegetation_count": 1211,
  "avg_severity": 6.2,
  "class_balance": {
    "crack_percentage": 50.8,
    "vegetation_percentage": 49.2
  },
  "split_info": {
    "train": 1850,
    "test": 410,
    "valid": 198
  }
}
```

---

### 2. `/api/analytics/hidden_damage` (GET or POST)

**Purpose:** Returns analytics for hidden damage indicators (moisture, stress, thermal).

**Sample Response:**
```json
{
  "avg_moisture_intensity": 42.3,
  "avg_stress_index": 58.7,
  "thermal_hotspot_count": 87,
  "stress_categories": {
    "Low": 120,
    "Medium": 65,
    "High": 28
  },
  "moisture_zones": {
    "Dry": 95,
    "Moderate": 78,
    "Wet": 40
  }
}
```

---

### 3. `/api/analytics/last_image` (GET)

**Purpose:** Returns comparison data for the last analyzed image vs dataset averages.

**Sample Response:**
```json
{
  "filename": "bridge_section_7.jpg",
  "upload_time": "2024-01-15T14:32:18Z",
  "comparison_radar": [
    {
      "metric": "Crack Density",
      "current": 65,
      "dataset_avg": 45,
      "fullMark": 100
    },
    {
      "metric": "Severity Score",
      "current": 72,
      "dataset_avg": 58,
      "fullMark": 100
    },
    {
      "metric": "Material Damage",
      "current": 48,
      "dataset_avg": 42,
      "fullMark": 100
    },
    {
      "metric": "Vegetation Cover",
      "current": 35,
      "dataset_avg": 28,
      "fullMark": 100
    },
    {
      "metric": "Moisture Level",
      "current": 58,
      "dataset_avg": 40,
      "fullMark": 100
    },
    {
      "metric": "Stress Index",
      "current": 70,
      "dataset_avg": 52,
      "fullMark": 100
    }
  ],
  "structural_health_score": 35,
  "risk_level": "High"
}
```

---

### 4. `/api/analytics/crack` (GET or POST) [Optional Enhancement]

**Purpose:** Detailed crack analytics across the dataset.

**Sample Response:**
```json
{
  "severity_distribution": {
    "Critical": 45,
    "Severe": 78,
    "Moderate": 132,
    "Minor": 210
  },
  "length_histogram": [
    { "range": "0-5mm", "count": 180 },
    { "range": "5-10mm", "count": 140 },
    { "range": "10-20mm", "count": 85 },
    { "range": "20-50mm", "count": 45 },
    { "range": ">50mm", "count": 15 }
  ],
  "depth_vs_length": [
    { "length": 2.3, "depth": 0.8, "severity": "Minor" },
    { "length": 5.7, "depth": 1.5, "severity": "Moderate" },
    { "length": 12.4, "depth": 3.2, "severity": "Severe" },
    { "length": 28.5, "depth": 7.8, "severity": "Critical" }
  ],
  "avg_crack_length": 8.4,
  "avg_crack_depth": 2.3
}
```

---

### 5. `/api/analytics/vegetation` (GET or POST) [Optional Enhancement]

**Purpose:** Detailed vegetation/biological growth analytics.

**Sample Response:**
```json
{
  "coverage_distribution": {
    "Low": 120,
    "Medium": 85,
    "High": 48
  },
  "type_distribution": {
    "Moss": 95,
    "Algae": 78,
    "Vines": 45,
    "Roots": 35
  },
  "severity_vs_health": [
    { "severity": 1, "health": 95 },
    { "severity": 3, "health": 78 },
    { "severity": 5, "health": 62 },
    { "severity": 7, "health": 45 },
    { "severity": 9, "health": 28 }
  ],
  "avg_coverage_percentage": 18.7
}
```

---

### 6. `/api/analytics/statistical_tests` (POST) [Optional Enhancement]

**Purpose:** Performs statistical hypothesis tests on current image vs dataset.

**Request Body:**
```json
{
  "current_image_id": "bridge_section_7.jpg",
  "test_types": ["t_test", "chi_square", "anova", "regression"]
}
```

**Sample Response:**
```json
{
  "t_test": {
    "test": "T-Test (Current vs Dataset)",
    "p_value": 0.0342,
    "significant": true,
    "interpretation": "Current image's damage metrics differ significantly from dataset mean (p < 0.05)"
  },
  "chi_square": {
    "test": "Chi-Square (Damage Categories)",
    "p_value": 0.0089,
    "significant": true,
    "interpretation": "Damage category distribution is non-uniform (p < 0.01)"
  },
  "anova": {
    "test": "ANOVA (Severity Groups)",
    "p_value": 0.0012,
    "significant": true,
    "interpretation": "Significant variance exists between severity groups (p < 0.01)"
  },
  "regression": {
    "test": "Linear Regression (Crack Length vs Depth)",
    "r_squared": 0.87,
    "p_value": 0.0001,
    "equation": "Depth = 0.28 * Length + 0.34",
    "interpretation": "Strong linear relationship with 87% variance explained"
  }
}
```

---

## Implementation Notes

### Backend Implementation (finalwebapp_api.py)

Add these routes to your Flask backend:

```python
from flask import Flask, jsonify, request
import os
import json
from pathlib import Path
import numpy as np
from scipy import stats

@app.route('/api/analytics/dataset', methods=['GET', 'POST'])
def get_dataset_stats():
    """Calculate dataset-level statistics"""
    dataset_path = Path("D:/Projects/AI-Powered_-Civil_Infrastructure/Dataset/")
    
    crack_path = dataset_path / "crack_preprocess"
    veg_path = dataset_path / "vegetation_preprocess"
    
    # Count images
    crack_count = sum(1 for f in crack_path.rglob('*.jpg'))
    veg_count = sum(1 for f in veg_path.rglob('*.jpg'))
    total = crack_count + veg_count
    
    return jsonify({
        "total_images": total,
        "crack_count": crack_count,
        "vegetation_count": veg_count,
        "avg_severity": 6.2,  # Calculate from metadata if available
        "class_balance": {
            "crack_percentage": round((crack_count / total) * 100, 1),
            "vegetation_percentage": round((veg_count / total) * 100, 1)
        }
    })

@app.route('/api/analytics/hidden_damage', methods=['GET', 'POST'])
def get_hidden_damage_analytics():
    """Returns moisture, stress, thermal analytics"""
    # Calculate from analysis history or database
    return jsonify({
        "avg_moisture_intensity": 42.3,
        "avg_stress_index": 58.7,
        "thermal_hotspot_count": 87,
        "stress_categories": {
            "Low": 120,
            "Medium": 65,
            "High": 28
        }
    })

@app.route('/api/analytics/last_image', methods=['GET'])
def get_last_image_comparison():
    """Get comparison of last analyzed image vs dataset averages"""
    # Retrieve from session or database
    last_analysis = session.get('last_analysis', {})
    
    return jsonify({
        "comparison_radar": [
            {"metric": "Crack Density", "current": 65, "dataset_avg": 45, "fullMark": 100},
            {"metric": "Severity Score", "current": 72, "dataset_avg": 58, "fullMark": 100},
            # ... more metrics
        ]
    })
```

---

## Current Status

✅ **Frontend:** Complete Analytics.jsx with all 8 sections and recharts visualizations
✅ **Mock Data:** Frontend uses mock data for development/testing
⏳ **Backend:** Endpoints need implementation in `finalwebapp_api.py`

---

## Testing

1. Start backend: `python finalwebapp_api.py`
2. Start frontend: `cd frontend && npm start`
3. Navigate to Analytics tab
4. Verify all 8 sections render correctly with mock data
5. Implement backend endpoints one-by-one and replace mock data with real API calls

---

## Frontend Integration

The Analytics.jsx component fetches data in `useEffect`:

```javascript
// Dataset Overview
const datasetRes = await fetch('http://localhost:5002/api/analytics/dataset');
const datasetJson = await datasetRes.json();
setDatasetStats(datasetJson);

// Hidden Damage
const hiddenDamageRes = await fetch('http://localhost:5002/api/analytics/hidden_damage');
const hiddenDamageJson = await hiddenDamageRes.json();
setHiddenDamageData(hiddenDamageJson);

// Current Image Comparison
const currentImageRes = await fetch('http://localhost:5002/api/analytics/last_image');
const currentImageJson = await currentImageRes.json();
setCurrentImageData(currentImageJson);
```

Replace mock data in Analytics.jsx once backend endpoints are live.
