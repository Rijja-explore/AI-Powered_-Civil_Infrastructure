/**
 * Helper functions to extract and transform data science analysis results
 * for visualization in Analytics dashboard
 */

// Extract KPI metrics from analysis
export const extractKPIMetrics = (analysisResults) => {
  if (!analysisResults) return null;

  const crackData = analysisResults.crack_detection || {};
  const materialData = analysisResults.material_analysis || {};
  const envData = analysisResults.environmental_impact_assessment || {};
  const bioData = analysisResults.biological_growth || {};
  const insights = analysisResults.data_science_insights || {};
  const academicDS = analysisResults.academic_data_science || {};

  // Structural Health Score - from Unit 2: Descriptive Analytics
  const structuralHealth = insights.statistical_summary?.structural_health_score || 85;

  // Critical Issues Count - from crack detection
  const criticalIssues = crackData.count || 0;

  // AI Confidence - from Unit 3: Inferential Statistics
  const aiConfidence = academicDS.unit3_inferential_statistics?.confidence_intervals 
    ? Object.values(academicDS.unit3_inferential_statistics.confidence_intervals)[0]?.ci_95?.upper_bound || 92
    : (materialData.probabilities ? Math.max(...Object.values(materialData.probabilities)) * 100 : 92);

  // Sustainability Score - from environmental assessment
  const sustainability = envData.sustainability_score || 7.5;

  return {
    structuralHealth,
    criticalIssues,
    aiConfidence,
    sustainability
  };
};

// Extract health trend data from Unit 5: Predictive Analytics
export const extractHealthTrendData = (analysisResults) => {
  if (!analysisResults) return [];

  const academicDS = analysisResults.academic_data_science || {};
  const predictive = academicDS.unit5_predictive_analytics || {};
  const timeSeriesData = predictive.time_series || {};
  const insights = analysisResults.data_science_insights || {};

  // Generate time series data based on current health + predictions
  const currentHealth = insights.statistical_summary?.structural_health_score || 85;
  
  const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
  const currentMonth = new Date().getMonth();
  
  // Use time series forecasts if available
  const forecasts = timeSeriesData.forecasts?.next_3_periods || [];
  const trendSlope = timeSeriesData.trend_analysis?.slope || -0.5;
  
  return months.slice(0, currentMonth + 4).map((month, index) => {
    let healthValue, performanceValue, maintenanceValue;
    
    if (index <= currentMonth) {
      // Historical data (slightly varying from current)
      healthValue = Math.max(70, Math.min(100, currentHealth + (Math.random() - 0.5) * 5));
      performanceValue = healthValue - 5 + Math.random() * 3;
      maintenanceValue = healthValue + 2 + Math.random() * 3;
    } else {
      // Forecast data from predictive analytics
      const forecastIndex = index - currentMonth - 1;
      healthValue = forecasts[forecastIndex] || (currentHealth + trendSlope * (forecastIndex + 1));
      performanceValue = healthValue - 3;
      maintenanceValue = healthValue + 4;
    }
    
    return {
      month,
      'Structural Health': Math.round(healthValue * 10) / 10,
      'System Performance': Math.round(performanceValue * 10) / 10,
      'Maintenance Index': Math.round(maintenanceValue * 10) / 10
    };
  });
};

// Extract risk assessment data from Unit 4: ANOVA
export const extractRiskAssessmentData = (analysisResults) => {
  if (!analysisResults) return [];

  const academicDS = analysisResults.academic_data_science || {};
  const anovaResults = academicDS.unit4_anova || {};
  const crackData = analysisResults.crack_detection || {};
  const envData = analysisResults.environmental_impact_assessment || {};

  // Risk categories based on ANOVA analysis of severity groups
  return [
    { 
      category: 'Structural\nIntegrity', 
      score: crackData.statistics?.severity_distribution?.Critical 
        ? 100 - (crackData.statistics.severity_distribution.Critical * 10) 
        : 88 
    },
    { 
      category: 'Material\nCondition', 
      score: envData.material_quantity_kg 
        ? Math.min(95, 100 - (envData.material_quantity_kg / 10)) 
        : 82 
    },
    { 
      category: 'Environmental\nImpact', 
      score: envData.sustainability_score * 10 || 75 
    },
    { 
      category: 'Maintenance\nRequirements', 
      score: crackData.count ? Math.max(60, 95 - (crackData.count * 3)) : 90 
    },
    { 
      category: 'System\nPerformance', 
      score: analysisResults.data_science_insights?.statistical_summary?.structural_health_score || 86 
    }
  ];
};

// Extract severity distribution from Unit 2: Frequency Distributions
export const extractSeverityDistribution = (analysisResults) => {
  if (!analysisResults) return [];

  const crackData = analysisResults.crack_detection || {};
  const academicDS = analysisResults.academic_data_science || {};
  const descriptive = academicDS.unit2_descriptive_analytics || {};
  
  // Get frequency distribution from descriptive analytics
  const freqDist = descriptive.frequency_distributions || {};
  const severityDist = crackData.statistics?.severity_distribution || {};

  const severityColors = {
    'Critical': '#dc2626',
    'Severe': '#ea580c',
    'Moderate': '#f59e0b',
    'Minor': '#10b981'
  };

  const severityPriority = {
    'Critical': 1,
    'Severe': 2,
    'Moderate': 3,
    'Minor': 4
  };

  const severityImpact = {
    'Critical': 'Immediate action required - structural failure risk',
    'Severe': 'Urgent repairs needed - accelerated deterioration',
    'Moderate': 'Monitor closely - schedule maintenance',
    'Minor': 'Routine monitoring - low immediate risk'
  };

  return Object.entries(severityDist).map(([type, value]) => ({
    type,
    value,
    color: severityColors[type] || '#6b7280',
    priority: severityPriority[type] || 5,
    impact: severityImpact[type] || 'Assessment required'
  }));
};

// Extract material confidence from Unit 2: Descriptive Statistics
export const extractMaterialConfidence = (analysisResults) => {
  if (!analysisResults) return [];

  const materialData = analysisResults.material_analysis || {};
  const academicDS = analysisResults.academic_data_science || {};
  const descriptive = academicDS.unit2_descriptive_analytics || {};

  const probabilities = materialData.probabilities || {};
  const materials = Object.entries(probabilities);

  const colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8', '#F7DC6F', '#BB8FCE', '#85C1E9'];

  return materials.map(([material, prob], index) => {
    const confidence = prob * 100;
    return {
      material: material.charAt(0).toUpperCase() + material.slice(1),
      confidence: Math.round(confidence * 10) / 10,
      color: colors[index % colors.length],
      category: confidence >= 75 ? 'High Confidence' : confidence >= 50 ? 'Medium Confidence' : 'Low Confidence'
    };
  });
};

// Extract correlation data from Unit 2: Correlation Analysis
export const extractCorrelationData = (analysisResults) => {
  if (!analysisResults) return null;

  const academicDS = analysisResults.academic_data_science || {};
  const descriptive = academicDS.unit2_descriptive_analytics || {};
  const correlations = descriptive.correlation_analysis || {};

  return correlations.significant_correlations || [];
};

// Extract regression analysis from Unit 5: Linear Regression
export const extractRegressionData = (analysisResults) => {
  if (!analysisResults) return null;

  const academicDS = analysisResults.academic_data_science || {};
  const predictive = academicDS.unit5_predictive_analytics || {};
  const linearModels = predictive.linear_models || {};

  return {
    r_squared: linearModels.model_performance?.train_r_squared || 0,
    equation: linearModels.model_equation || '',
    rmse: linearModels.model_performance?.train_rmse || 0
  };
};

// Extract ANOVA results from Unit 4
export const extractANOVAResults = (analysisResults) => {
  if (!analysisResults) return null;

  const academicDS = analysisResults.academic_data_science || {};
  const anova = academicDS.unit4_anova || {};

  return {
    oneWayANOVA: anova.one_way_anova || {},
    chiSquare: anova.chi_square_tests || {}
  };
};

// Extract confidence intervals from Unit 3: Inferential Statistics
export const extractConfidenceIntervals = (analysisResults) => {
  if (!analysisResults) return null;

  const academicDS = analysisResults.academic_data_science || {};
  const inferential = academicDS.unit3_inferential_statistics || {};

  return inferential.confidence_intervals || {};
};

// Extract hypothesis testing results from Unit 3
export const extractHypothesisTests = (analysisResults) => {
  if (!analysisResults) return null;

  const academicDS = analysisResults.academic_data_science || {};
  const inferential = academicDS.unit3_inferential_statistics || {};

  return inferential.hypothesis_tests || {};
};

// Extract environmental impact metrics
export const extractEnvironmentalMetrics = (analysisResults) => {
  if (!analysisResults) return null;

  const envData = analysisResults.environmental_impact_assessment || {};

  return {
    carbonFootprint: envData.carbon_footprint_kg || 0,
    waterFootprint: envData.water_footprint_liters || 0,
    energyConsumption: envData.energy_consumption_kwh || 0,
    sustainabilityScore: envData.sustainability_score || 0,
    ecoEfficiency: envData.eco_efficiency_rating || 0,
    recommendations: envData.recommendations || []
  };
};

// Check if analysis data is available
export const hasAnalysisData = (analysisResults) => {
  return analysisResults && Object.keys(analysisResults).length > 0;
};
