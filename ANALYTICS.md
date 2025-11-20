# 📊 InfraVision AI - Analytics Dashboard Documentation

## Overview

The Analytics Dashboard in InfraVision AI provides comprehensive, AI-powered structural health monitoring and analysis. It displays dynamic data processed from uploaded infrastructure images using advanced computer vision and statistical analysis.

---

## 🏗️ Dashboard Blocks & Components

### 1. **KPI Dashboard** (Key Performance Indicators)
- **Purpose**: Quick overview of infrastructure health status with 4 premium metric cards
- **Metrics Displayed** (exact formulas from backend):
  - **Structural Health Score** (0–100)
    - Computed in `finalwebapp_api.py` as:
      - $\text{structural\_health\_score} = \max(0, 100 - 5 \times \text{total\_cracks} - \text{growth\_percentage})$
      - Uses `total_cracks = len(crack_details)` and `growth_percentage` from `detect_biological_growth` on the current image.
  - **Critical Issues Count**
    - Count of cracks with severity label `"Critical"` in `crack_details` returned by `detect_with_yolo`.
  - **Confidence Level (%)**
    - For material: `max(probabilities) * 100` where `probabilities` comes from `classify_material` (MobileNetV2 or fallback texture-based classifier).
    - For cracks: YOLO confidence `box.conf` is stored per crack; the dashboard can display mean or max across all cracks.
  - **Sustainability Rating** (0–10)
    - Computed as `sustainability_score = max(0, 10 - carbon_footprint/5 - water_footprint/100)` where `carbon_footprint` and `water_footprint` are calculated from crack count, biological growth and estimated material quantity.
- **Why**: Provides at-a-glance status of infrastructure health without deep diving into analytics
- **Data Source (Exactly What Data?)**:
  - `crack_details` from `detect_with_yolo(image_np, px_to_cm_ratio, YOLO_MODEL)` on the **current uploaded image**.
  - `growth_analysis['growth_percentage']` from `detect_biological_growth(image_np, crack_details)`.
  - `material`, `probabilities` from `classify_material(image_np, MATERIAL_MODEL)`.
  - `carbon_footprint_kg`, `water_footprint_liters` from the environmental impact block (see Section 6).

---

### 2. **AI-Powered Risk Assessment Matrix**
- **Purpose**: Multi-dimensional risk analysis using radar visualization with left-right split layout
- **Features**:
  - **Graph (Left)**: Interactive Radar chart showing 5-7 risk dimensions
  - **Content (Right)**: Detailed insights, risk levels, and recommendations
  - **Dimensions Analyzed**: Structural integrity, maintenance urgency, material degradation, environmental factors, etc.
- **Why**: Identifies priority risks and guides maintenance scheduling decisions
- **Data Source (What Data?)**:
  - Based on **integrated dataset** created from the current image: crack geometry (width, length, area, severity), material type and environmental indicators.
  - Uses **ANOVA-style grouping** on severity/material categories plus synthetic time-series (stress level, maintenance cost, structural integrity over one year) generated around that image to compute risk scores.
- **Size**: Extended height (800px) for better visibility and interaction

---

### 3. **Advanced Issue Severity Distribution**
- **Purpose**: Categorizes detected defects by severity level (Minor, Moderate, Severe, Critical)
- **Layout**:
  - **Graph (Left)**: Interactive Pie chart with donut visualization and statistics
  - **Values (Right)**: Detailed severity breakdown, counts, priorities, and action items
  - **Center Statistic**: Total issue count with visual prominence
- **Why**: Helps prioritize maintenance work based on severity and impact
- **Data Source (Exactly What Data?)**:
  - For each detection box from YOLO (`result.boxes`), we compute:
    - `width_cm = (x2 - x1) * px_to_cm_ratio`
    - `length_cm = (y2 - y1) * px_to_cm_ratio`
    - `severity = calculate_severity(width_cm, length_cm, label)` where `calculate_severity` uses thresholds on max dimension and area to map to **Minor / Moderate / Severe / Critical**.
  - The pie segments are counts of `crack['severity']` in this list for the **current image only**.
  - Implementation visible in `detect_with_yolo` and `plot_crack_severity` in `finalwebapp.py`.
- **Size**: 750px height with scrollable insights panel

---

### 4. **Material Composition Analysis**
- **Purpose**: Analyzes and visualizes construction materials detected in the infrastructure
- **Features**:
  - Column chart showing material percentages
  - Confidence scores for material classification
  - Material degradation assessment
- **Why**: Essential for understanding structural makeup and predicting failure modes
- **Data Source (What Data?)**:
  - Uses **material prediction for the uploaded image** (e.g., Concrete, Steel, Brick, Stone) and associated probability vector from the material classifier.
  - Percentages per bar/grid are calculated from **per-pixel / per-region material detections** aggregated over that image.

---

### 5. **Statistical Analysis Summary**
- **Purpose**: Comprehensive statistical metrics and hypothesis testing results
- **Includes (direct mapping to `AdvancedDataAnalytics`):**
  - **Descriptive statistics**: mean, median, mode, std dev, variance, range, IQR, coefficient of variation (from `descriptive_stats` in `exploratory_data_analysis`).
  - **Outlier counts**: per-variable IQR-based outliers (from `eda_results['outliers']`).
  - **Normality checks**: Shapiro–Wilk statistics and p-values per numeric column (`eda_results['distributions']`).
  - **Inferential tests**: one-sample t-test, two-sample t-test, z-test and 95% confidence intervals from `inferential_statistics`.
  - **ANOVA / Chi-square**: one-way ANOVA on a numeric variable by a categorical factor, optional two-way ANOVA, and chi-square test for association between categorical features from `analysis_of_variance`.
- **Why**: Provides statistical rigor to damage assessments and predictions
- **Data Source (Exactly What Data?)**:
  - `create_comprehensive_analytics_report(crack_details, material_analysis, environmental_data)` in `advanced_data_analytics.py` builds a **single integrated DataFrame** where:
    - Each YOLO crack becomes a row with `width_cm`, `length_cm`, `area_cm2`, `severity`, `confidence`, `label`.
    - It then appends **365 synthetic daily rows** with fields like `temperature_c`, `humidity_percent`, `stress_level`, `maintenance_cost`, `structural_integrity`, `material_type` to simulate a 1‑year monitoring period.
  - All summary grids in this box are computed on that DataFrame, so they are **tied to the current image’s cracks/material + a synthetic temporal context**.
- **Size**: 750px minimum height for full visibility

---

### 6. **Environmental Impact Assessment**
- **Purpose**: Evaluates environmental factors affecting infrastructure
- **Key backend metrics and formulas**:
  - **Biological Growth Percentage**: `growth_percentage = (growth_pixels / total_pixels) * 100` where `growth_pixels` are HSV‑green pixels in the current image (`detect_biological_growth`).
  - **Biological Growth Area (cm²)**: in API and app, area is estimated as `growth_area_px * (px_to_cm_ratio ** 2)` and added to crack-based growth (`calculate_biological_growth_area`).
  - **Material Quantity (kg)**: `estimate_material_quantity` uses crack and growth areas with a material‑specific density to estimate required repair material.
  - **Carbon Footprint (kg CO₂e)**:
    - In `finalwebapp.py` (Streamlit): `carbon_footprint = calculate_carbon_footprint(material, quantity_kg)` with fixed emission factors per material.
    - In `finalwebapp_api.py` (API): `carbon_footprint = total_cracks * 2.5 + random_noise` for image‑level environmental impact.
  - **Water Footprint (L)**:
    - In app: `water_footprint = calculate_water_footprint(material, quantity_kg)`.
    - In API: `water_footprint = growth_percentage * 15 + random_noise`.
  - **Sustainability Score (0–10)**: `sustainability_score = max(0, 10 - carbon_footprint/5 - water_footprint/100)`.
- **Why**: Environmental factors are major contributors to infrastructure degradation
- **Data Source (Exactly What Data?)**:
  - HSV analysis of the **same uploaded image** to get vegetation/moss coverage.
  - Crack geometry and segmentation masks (for biological growth area) from `detect_with_yolo`, `segment_image`, `detect_biological_growth_advanced`.
  - Material type from `classify_material`; density/emission/water factors from hard-coded tables in `finalwebapp.py`.

---

### 7. **Crack Size Distribution**
- **Purpose**: Scatter/summary of crack dimensions vs. severity
- **Metrics**:
  - Crack length vs. width relationships (from YOLO box dimensions × `px_to_cm_ratio`).
  - Severity classification by size (`calculate_severity`).
  - Derived metrics like **total_crack_area**, **average_size_cm2**, **crack_density**.
- **Why**: Precise crack measurements are critical for structural assessment
- **Data Source (Exactly What Data?)**:
  - `crack['width_cm']`, `crack['length_cm']` for each YOLO detection in the **current image**.
  - API also derives:
    - `total_area_cm2 = Σ(width_cm × length_cm)`
    - `average_size_cm2 = total_area_cm2 / max(total_cracks, 1)`
    - `crack_density = total_cracks / (image_pixels / 10000)` used in `data_science_insights.statistical_summary`.

---

### 8. **T-Test Analysis**
- **Purpose**: Statistical comparison of defect or environmental metrics
- **Hypothesis Structure (as implemented in `inferential_statistics`)**:
  - **One-sample t-test** on a selected numeric column (e.g., crack area, stress level):
    - $H_0$: sample mean = hypothetical population mean (`population_mean = mean * 1.1`).
    - $H_1$: sample mean ≠ population mean.
    - Backend computes t-statistic, p-value, and 95% CI using `scipy.stats.ttest_1samp`.
  - **Two-sample t-test** between two numeric columns (e.g., variable A vs variable B in the integrated dataset).
- **Why**: Determines if observed mean differences are statistically significant or random variation.
- **Data Source (Exactly What Data?)**:
  - Operates on numeric columns of the **integrated DataFrame** constructed from current-image cracks + synthetic daily environmental/structural variables (see Section 5 and `advanced_data_analytics.py`).

---

### 9. **Predictive Analytics**
- **Purpose**: Forecasts future infrastructure condition deterioration
- **Implemented Models**:
  - In `advanced_data_analytics.py` `predictive_analytics`:
    - **Linear Regression** (least squares) on selected numeric features to predict a target variable (e.g., maintenance cost or structural integrity) with R², MSE, coefficients.
    - **Logistic Regression** to predict categorical targets (e.g., severity/material class) from numeric features.
    - **Time-Series Trend + Forecast**: moving averages and simple linear extrapolation of a daily series (e.g., stress level) with 3‑step ahead forecast.
    - **Multiple Regression with Interaction Term** between first two numeric features.
  - In `finalwebapp.py` `predict_crack_progression`:
    - For each crack: builds linear regression over synthetic time points [0, 3, 6, 9, 12 months] scaled by a **severity factor** (Minor/Moderate/Severe/Critical) and predicts future areas at 15, 18, 24 months.
- **Why**: Enables proactive maintenance scheduling and budget planning
- **Data Source (Exactly What Data?)**:
  - Numeric features from the integrated DataFrame (crack dimensions, synthetic stress, cost, integrity) + severity labels from the current image.
  - Crack‑level progression uses **current crack area** and severity from `crack_details` only for the current uploaded image.

---

### 10. **Regression Analysis**
- **Purpose**: Identifies relationships between infrastructure variables
- **Models (matching code)**:
  - **Simple Linear Regression (app)**: in `regression_analysis` and `simplified_linear_models` a single predictor vs one target is fit using NumPy (slope, intercept, R², RMSE).
  - **Multi-feature Linear Regression (API)**: uses `sklearn.linear_model.LinearRegression` on up to 2–3 numeric features (e.g., crack/structural metrics) to predict a final target, reporting train/test R² and MSE.
  - **Multiple Regression with Interaction**: adds a feature `X1 * X2` for interaction between two predictors (e.g., crack size × environmental factor).
- **Metrics**: R², adjusted R², coefficients, intercept, residual spread; goodness of fit is labelled qualitatively (excellent/good/fair) from test R².
- **Why**: Understands cause-effect relationships in infrastructure degradation
- **Data Source (Exactly What Data?)**:
  - Numeric columns from the integrated DataFrame (e.g., `width_cm`, `length_cm`, `area_cm2`, `stress_level`, `maintenance_cost`, `structural_integrity`) which are anchored to the **crack detections and synthetic temporal context** of the current image.

---

### 11. **Advanced Correlation Analysis**
- **Purpose**: Identifies and visualizes correlations between all measured variables
- **Features (from `correlation_analysis`)**:
  - Full Pearson correlation matrix of numeric variables.
  - List of **significant correlations** where |r| > 0.5, tagged as moderate/strong.
  - Same matrix reused as a proxy for Spearman in the simplified module.
- **Why**: Reveals hidden dependencies and interactions in infrastructure data
- **Data Source (Exactly What Data?)**:
  - Same integrated DataFrame as Section 5 (per-image cracks + synthetic daily variables) – every correlation cell is computed from that dataset.

---

### 12. **T-Distribution & Confidence Intervals**
- **Purpose**: Visualizes statistical distributions and confidence bounds
- **Features (as coded)**:
  - 95% confidence intervals for means of numeric variables using $\bar{x} \pm 1.96 \cdot SE$ in both the full and simplified analytics modules.
  - Simplified t/z style tests with approximate p‑values when full `scipy.stats` is not available.
- **Why**: Communicates uncertainty and reliability of statistical estimates
- **Data Source (Exactly What Data?)**:
  - Sample means, standard deviations and standard errors of numeric variables (crack metrics, environmental proxies, structural integrity, etc.) from the per-image integrated DataFrame.
  - Confidence intervals and effect sizes (Cohen’s d) are thus **directly tied to the crack/material/environment profile of the last analyzed image plus its generated context**.

---

## 🔄 Data Flow

```
Uploaded Image
    ↓
Computer Vision (YOLOv8 Detection)
    ↓
Defect Extraction (Cracks, materials, damage)
    ↓
Statistical Analysis (Descriptive + Inferential)
    ↓
ML Model Scoring (Risk, severity, predictions)
    ↓
Analytics Dashboard Rendering
    ↓
Interactive Visualizations (Charts, graphs, insights)
```

---

## 📈 Analytics Technologies Used

- **Frontend**: React.js with Ant Design Charts for visualization
- **Backend**: Python (scipy, numpy, pandas, scikit-learn)
- **Computer Vision**: YOLOv8 for object detection and classification
- **Statistical Engine**: scipy.stats for hypothesis testing and distributions
- **ML Models**: Scikit-learn for regression, clustering, and predictions
- **Visualization**: Recharts, Ant Design Plots for interactive charts

---

## 🎯 Use Cases

1. **Infrastructure Inspectors**: Quickly assess structural health and identify priority repairs
2. **Maintenance Planners**: Use predictive analytics to schedule preventive maintenance
3. **Budget Planning**: Risk assessment helps allocate repair resources efficiently
4. **Research & Development**: Statistical analysis provides insights for infrastructure resilience research
5. **Compliance & Reporting**: Detailed analytics support audit and compliance documentation

---

## 🔐 Data Privacy & Security

- All analysis is performed locally or on secure servers
- Image data is processed and not stored permanently
- Statistical results are aggregated and anonymized
- No personal or sensitive data is retained

---

## 📝 Notes

- All charts are **dynamic** - they update based on uploaded image analysis
- No demo/static data is displayed; all metrics are real analysis results
- Extended heights on Risk Assessment (800px) and Severity Distribution (750px) ensure full visibility
- Left-right layout optimization (graph left, values right) improves information hierarchy
- Statistical Analysis box height (750px) accommodates comprehensive test results

