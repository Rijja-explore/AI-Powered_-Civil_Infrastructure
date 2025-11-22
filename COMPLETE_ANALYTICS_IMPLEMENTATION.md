# 🚀 Complete Analytics Pipeline - Implementation Guide

## 📋 Overview

This package includes **3 complete solutions** for your AI-powered structural health monitoring system:

### ✅ PROMPT 1: Dataset-Level Analytics (Quick Analytics Tab)
- **Jupyter Notebook:** `Dataset_Analytics_Pipeline.ipynb`
- **Purpose:** Load all images, extract features, run statistical tests
- **Output:** `dataset_analytics.json` → React Quick Analytics tab
- **Features:**
  - 12-panel visualization dashboard
  - 6 statistical hypothesis tests
  - Top-risk image rankings
  - Feature correlation analysis

### ✅ PROMPT 2: Image-Level Analytics (Image Insights Tab)
- **Class:** `ImageInsightsAnalyzer` in notebook
- **Purpose:** Analyze individual image results vs dataset statistics
- **Output:** Per-image JSON with radar chart data, overlap analysis, insights
- **Features:**
  - Radar chart comparison vs dataset mean
  - Hidden damage overlap analysis
  - Risk contribution breakdown
  - Percentile rankings & z-scores
  - 5+ actionable insights per image

### ✅ PROMPT 3: Architecture Fix (Prevent Data Loss)
- **Guide:** `ARCHITECTURE_FIX_GUIDE.md` in notebook outputs
- **Problem:** Data disappears when switching tabs
- **Solution:** Shared state pattern (lift state up)
- **Implementation:** React parent component with useState + props

---

## 📁 Files Created by Notebook

When you run the notebook, it creates:

### 1. **dataset_analytics.json** (Primary for Quick Analytics)
```
Location: D:/Projects/AI-Powered_-Civil_Infrastructure/dataset_analytics.json
Size: ~200-500 KB
Purpose: Feed to /api/analytics/dataset endpoint
Contains:
  - crack_analysis: severity distribution, metrics, histograms
  - vegetation_analysis: type distribution, metrics, histograms
  - statistical_tests: 6 tests with p-values & interpretations
  - top_risk_images: Top 10 high-risk images
```

### 2. **dataset_stats_comprehensive.json**
```
Location: D:/Projects/AI-Powered_-Civil_Infrastructure/dataset_stats_comprehensive.json
Contains: Feature-level statistics (mean/median/std/min/max)
Use for: Reference & threshold setting
```

### 3. **example_image_insights.json**
```
Location: D:/Projects/AI-Powered_-Civil_Infrastructure/example_image_insights.json
Purpose: Template for /api/image_insights endpoint response
Structure: Radar data, overlap analysis, contribution breakdown, insights array
```

### 4. **DATASET_ANALYTICS_SUMMARY.md**
```
Location: D:/Projects/AI-Powered_-Civil_Infrastructure/DATASET_ANALYTICS_SUMMARY.md
Purpose: Human-readable summary of findings
Contains: Crack patterns, vegetation patterns, degradation risk analysis
```

### 5. **ARCHITECTURE_FIX_GUIDE.md**
```
Location: D:/Projects/AI-Powered_-Civil_Infrastructure/ARCHITECTURE_FIX_GUIDE.md
Purpose: Step-by-step React implementation
Contains: Code examples, flow diagrams, file-by-file changes
```

### 6. **analytics_dashboard.png**
```
Location: D:/Projects/AI-Powered_-Civil_Infrastructure/analytics_dashboard.png
Purpose: Visual reference of all analytics
Contains: 12-panel dashboard with distributions & correlations
```

---

## 🎯 Implementation Roadmap

### Phase 1: Backend Setup (1 hour)

**Step 1.1: Load Analytics JSON into API**
```python
# In finalwebapp_api.py

import json

# Load dataset analytics
with open('dataset_analytics.json', 'r') as f:
    DATASET_ANALYTICS = json.load(f)

@app.route('/api/analytics/dataset', methods=['GET'])
def get_dataset_analytics():
    """Return dataset-level analytics for Quick Analytics tab"""
    return jsonify({
        'crack_analysis': DATASET_ANALYTICS['crack_analysis'],
        'vegetation_analysis': DATASET_ANALYTICS['vegetation_analysis'],
        'statistical_tests': DATASET_ANALYTICS['statistical_tests'],
        'top_risk_images': DATASET_ANALYTICS['top_risk_images']
    })
```

**Step 1.2: Implement Image Insights Endpoint**
```python
# In finalwebapp_api.py

from analytics_aggregator import ImageInsightsAnalyzer

# Initialize analyzer with dataset statistics
analyzer = ImageInsightsAnalyzer(df_crack, df_vegetation)

@app.route('/api/image_insights', methods=['POST'])
def compute_image_insights():
    """Analyze a single image result against dataset"""
    image_metrics = request.json
    insights = analyzer.analyze_image(image_metrics)
    return jsonify(insights)
```

### Phase 2: Frontend Setup (2-3 hours)

**Step 2.1: Create QuickAnalytics.jsx Tab**

```jsx
// frontend/src/pages/QuickAnalytics.jsx
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { BarChart, PieChart, LineChart, RadarChart } from 'recharts';

export default function QuickAnalytics() {
  const [analytics, setAnalytics] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    axios.get('http://localhost:5002/api/analytics/dataset')
      .then(res => {
        setAnalytics(res.data);
        setLoading(false);
      })
      .catch(err => {
        console.error('Error loading analytics:', err);
        setLoading(false);
      });
  }, []);

  if (loading) return <div>Loading analytics...</div>;
  if (!analytics) return <div>Error loading analytics</div>;

  return (
    <div className="quick-analytics">
      <h1>Dataset Analytics Dashboard</h1>

      {/* Section 1: Crack Analysis */}
      <section className="section-crack-analysis">
        <h2>🔴 Crack Analysis</h2>
        <div className="grid-2">
          <div className="card">
            <h3>Severity Distribution</h3>
            <PieChart data={analytics.crack_analysis.severity_distribution}>
              {/* Chart implementation */}
            </PieChart>
          </div>
          <div className="card">
            <h3>Feature Metrics</h3>
            <p>Mean Density: {analytics.crack_analysis.metrics.mean_crack_density.toFixed(3)}</p>
            <p>Std Dev: {analytics.crack_analysis.metrics.std_crack_density.toFixed(3)}</p>
          </div>
        </div>
      </section>

      {/* Section 2: Vegetation Analysis */}
      <section className="section-vegetation">
        <h2>🟢 Vegetation Analysis</h2>
        <div className="grid-2">
          <div className="card">
            <h3>Type Distribution</h3>
            <BarChart data={analytics.vegetation_analysis.type_distribution}>
              {/* Chart implementation */}
            </BarChart>
          </div>
        </div>
      </section>

      {/* Section 3: Statistical Tests */}
      <section className="section-tests">
        <h2>📊 Statistical Hypothesis Tests</h2>
        {analytics.statistical_tests.map((test, i) => (
          <div key={i} className="test-card">
            <h4>{test.test_name}</h4>
            <p>p-value: {test.p_value.toFixed(4)}</p>
            <p className={test.significant ? 'significant' : 'not-significant'}>
              {test.interpretation}
            </p>
          </div>
        ))}
      </section>

      {/* Section 4: Top Risk Images */}
      <section className="section-risk">
        <h2>⚠️ Top Risk Images</h2>
        <div className="risk-table">
          <h3>High-Risk Cracks</h3>
          <table>
            <thead>
              <tr>
                <th>Filename</th>
                <th>Risk Score</th>
                <th>Severity</th>
              </tr>
            </thead>
            <tbody>
              {analytics.top_risk_images.crack.map((img, i) => (
                <tr key={i}>
                  <td>{img.filename}</td>
                  <td>{(img.risk_score * 100).toFixed(1)}%</td>
                  <td>{img.severity}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>
    </div>
  );
}
```

**Step 2.2: Create ImageInsights.jsx Tab**

```jsx
// frontend/src/pages/ImageInsights.jsx
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { RadarChart, BarChart, LineChart, Radar, Bar, Line } from 'recharts';

export default function ImageInsights({ lastAnalysis }) {
  const [insights, setInsights] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!lastAnalysis?.metrics) return;

    setLoading(true);
    axios.post('http://localhost:5002/api/image_insights', lastAnalysis.metrics)
      .then(res => {
        setInsights(res.data);
        setLoading(false);
      })
      .catch(err => {
        console.error('Error computing insights:', err);
        setLoading(false);
      });
  }, [lastAnalysis]);

  if (!lastAnalysis) {
    return <div className="no-data">Upload an image to see insights</div>;
  }

  if (loading) return <div>Computing insights...</div>;
  if (!insights) return <div>Error computing insights</div>;

  return (
    <div className="image-insights">
      <h1>Image Insights - {insights.risk_level}</h1>

      {/* Section 1: Image Grid + Summary */}
      <section className="section-1">
        <div className="grid-container">
          <div className="images-grid-3x3">
            {lastAnalysis.images.map((img, i) => (
              <div key={i} className="image-cell">
                <img src={img} alt={`Analysis ${i}`} />
                <label>{getLabel(i)}</label>
              </div>
            ))}
          </div>
          <div className="summary-card">
            <h2>Summary</h2>
            <p>{insights.summary}</p>
            <div className="health-score">
              <span className="label">Health Score:</span>
              <span className="value">{insights.health_score}/100</span>
            </div>
          </div>
        </div>
      </section>

      {/* Section 2: Radar Chart */}
      <section className="section-2">
        <h2>Comparison vs Dataset</h2>
        <RadarChart data={insights.radar_chart_data.metrics}>
          <Radar dataKey="current" name="This Image" stroke="#FF6B6B" />
          <Radar dataKey="dataset_mean" name="Dataset Mean" stroke="#4ECDC4" />
        </RadarChart>
      </section>

      {/* Section 3: Overlap Analysis */}
      <section className="section-3">
        <h2>Hidden Damage Analysis</h2>
        <BarChart data={formatOverlapData(insights.overlap_analysis)}>
          <Bar dataKey="value" fill="#FFD93D" />
        </BarChart>
      </section>

      {/* Section 4: Contribution Breakdown */}
      <section className="section-4">
        <h2>Risk Contribution Breakdown</h2>
        <BarChart data={insights.contribution_breakdown}>
          <Bar dataKey="contribution_to_risk" fill="#6BCB77" />
        </BarChart>
      </section>

      {/* Section 5: Insights */}
      <section className="section-5">
        <h2>Insights & Alerts</h2>
        <div className="insights-list">
          {insights.insights.map((insight, i) => (
            <div key={i} className={`insight-card insight-${insight.type}`}>
              <p>{insight.message}</p>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}

function getLabel(i) {
  const labels = ['Original', 'Crack', 'Vegetation', 'Segmentation', 'Depth', 
                  'Edges', 'Moisture', 'Stress', 'Thermal'];
  return labels[i];
}

function formatOverlapData(overlap) {
  return Object.entries(overlap).map(([key, value]) => ({
    name: key.replace(/_/g, ' '),
    value: value
  }));
}
```

**Step 2.3: Update MainDashboard.jsx (Fix Data Loss)**

```jsx
// frontend/src/components/MainDashboard.jsx
import React, { useState } from 'react';
import HomePage from '../pages/HomePage';
import ImageAnalysis from '../pages/ImageAnalysis';
import ImageInsights from '../pages/ImageInsights';
import VideoAnalysis from '../pages/VideoAnalysis';
import RealTimeMonitoring from '../pages/RealTimeMonitoring';
import Analytics from '../pages/Analytics';
import QuickAnalytics from '../pages/QuickAnalytics';

export default function MainDashboard() {
  const [activeTab, setActiveTab] = useState('home');
  const [lastAnalysis, setLastAnalysis] = useState(null);  // ✨ Shared state

  return (
    <div className="dashboard">
      <nav className="tabs-nav">
        <button onClick={() => setActiveTab('home')}>Home</button>
        <button onClick={() => setActiveTab('analysis')}>Image Analysis</button>
        <button onClick={() => setActiveTab('insights')}>Image Insights</button>
        <button onClick={() => setActiveTab('quick-analytics')}>Quick Analytics</button>
        <button onClick={() => setActiveTab('video')}>Video Analysis</button>
        <button onClick={() => setActiveTab('rtm')}>Real-Time</button>
        <button onClick={() => setActiveTab('analytics')}>Analytics</button>
      </nav>

      <div className="tab-content">
        {activeTab === 'home' && <HomePage />}
        
        {activeTab === 'analysis' && (
          <ImageAnalysis 
            lastAnalysis={lastAnalysis}
            onAnalysisComplete={setLastAnalysis}
          />
        )}
        
        {activeTab === 'insights' && (
          <ImageInsights lastAnalysis={lastAnalysis} />
        )}
        
        {activeTab === 'quick-analytics' && <QuickAnalytics />}
        {activeTab === 'video' && <VideoAnalysis />}
        {activeTab === 'rtm' && <RealTimeMonitoring />}
        {activeTab === 'analytics' && <Analytics />}
      </div>
    </div>
  );
}
```

**Step 2.4: Update ImageAnalysis.jsx**

```jsx
// In ImageAnalysis.jsx, update handleImageUpload:

const handleImageUpload = async (e) => {
  const file = e.target.files[0];
  if (!file) return;

  setLoading(true);
  try {
    const formData = new FormData();
    formData.append('file', file);

    const response = await axios.post('http://localhost:5002/api/analyze', formData);

    const analysisResult = {
      images: response.data.analysis_images,
      metrics: response.data.metrics
    };

    setOutputImages(analysisResult.images);
    setOutputMetrics(analysisResult.metrics);
    
    // ✨ IMPORTANT: Notify parent
    onAnalysisComplete(analysisResult);

  } catch (error) {
    console.error('Analysis failed:', error);
  } finally {
    setLoading(false);
  }
};
```

### Phase 3: Testing & Validation (1 hour)

**Test Checklist:**
- [ ] Start backend: `python finalwebapp_api.py`
- [ ] Start frontend: `cd frontend && npm start`
- [ ] Test /api/analytics/dataset endpoint (should return JSON)
- [ ] Upload test image → ImageAnalysis tab
- [ ] Verify 9 analysis images appear
- [ ] Switch to ImageInsights tab → data should persist
- [ ] Verify radar chart renders correctly
- [ ] Switch to QuickAnalytics tab → loads dataset stats
- [ ] Check all tabs in sequence → no data loss
- [ ] Verify insights cards display alerts

---

## 📊 JSON Structure Reference

### dataset_analytics.json
```json
{
  "metadata": { ... },
  "crack_analysis": {
    "severity_distribution": { "Critical": 5, "Severe": 12, ... },
    "metrics": { "mean_crack_density": 0.12, "std_crack_density": 0.04 },
    "histograms": { "crack_density": { "bins": 20, "data": [...] } }
  },
  "vegetation_analysis": { ... },
  "statistical_tests": [
    {
      "test_name": "Mann-Whitney U Test: Severe vs Mild Cracks",
      "p_value": 0.0342,
      "significant": true,
      "interpretation": "..."
    }
  ],
  "top_risk_images": {
    "crack": [{ "filename": "...", "risk_score": 0.82, "severity": "Critical" }]
  }
}
```

### example_image_insights.json
```json
{
  "summary": "...",
  "health_score": 38,
  "risk_level": "High",
  "radar_chart_data": { "metrics": [...] },
  "overlap_analysis": { "cracks_in_damp_areas": 65, ... },
  "contribution_breakdown": [
    { "feature": "cracks", "contribution_to_risk": 35.2, "weight": 0.35 }
  ],
  "insights": [
    { "type": "warning", "message": "..." }
  ]
}
```

---

## 🚀 Quick Start Commands

```bash
# 1. Run Jupyter Notebook to generate JSON files
jupyter notebook Dataset_Analytics_Pipeline.ipynb

# 2. Copy JSON files to backend
cp dataset_analytics.json ./

# 3. Update backend with new endpoint
# Edit finalwebapp_api.py (see Phase 1 above)

# 4. Start backend
python finalwebapp_api.py

# 5. In another terminal, start frontend
cd frontend
npm start

# 6. Open browser and test
# http://localhost:3000/quick-analytics
# http://localhost:3000/image-insights
```

---

## 🎓 Key Concepts

### 1. Feature Extraction
- **Crack features:** crack_pixel_ratio, edge_density, skeleton_length_proxy, glcm_entropy
- **Vegetation features:** vegetation_coverage, green_index_mean, glcm_entropy, saturation_mean
- **Risk score:** Weighted combination of features (0-1 scale)

### 2. Statistical Tests
- **Mann-Whitney U:** Compare crack density between severity levels
- **ANOVA:** Test differences across multiple categories
- **Linear Regression:** Predict risk score from features
- **Chi-Square:** Test independence of categorical variables

### 3. Image Insights Logic
- **Z-scores:** Standardized deviation from dataset mean
- **Percentiles:** Rank within dataset distribution
- **Overlap analysis:** Percentage of cracks/vegetation in damp/stressed areas
- **Contribution breakdown:** Feature weights in health score calculation

### 4. Shared State Pattern
- Lift state up to parent component (MainDashboard)
- Pass as props to child components (ImageAnalysis, ImageInsights)
- Callback function (onAnalysisComplete) updates parent state
- Prevents data loss on tab switches

---

## 📞 Troubleshooting

**Issue:** dataset_analytics.json not generated
- **Solution:** Ensure dataset paths exist: `D:/Projects/.../Dataset/crack_preprocess/` and `vegetation_preprocess/`

**Issue:** Image Insights tab shows "Upload an image" even after uploading
- **Solution:** Check that ImageAnalysis calls `onAnalysisComplete()`
- Verify lastAnalysis is passed correctly in props

**Issue:** Statistical tests show "test not performed"
- **Solution:** Ensure dataset has images in multiple severity/type categories
- Check that df_crack/df_vegetation have enough rows

**Issue:** Radar chart renders blank
- **Solution:** Verify all metrics are numeric values (0-1 range)
- Check that chart data format matches Recharts requirements

---

## 📚 References

- Jupyter Notebook: `Dataset_Analytics_Pipeline.ipynb` (complete source code)
- Architecture Guide: `ARCHITECTURE_FIX_GUIDE.md` (React state patterns)
- Summary Report: `DATASET_ANALYTICS_SUMMARY.md` (findings & insights)
- Example Output: `example_image_insights.json` (JSON schema reference)

---

**Status:** ✅ Ready for implementation  
**Last Updated:** November 22, 2025  
**Version:** 1.0
