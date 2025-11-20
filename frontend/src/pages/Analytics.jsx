import React, { useState, useEffect } from 'react';
import { TrendingUp, AlertTriangle, BarChart3, Target, Wind, Droplet, Zap, Leaf, Shield, Activity, CheckCircle } from 'lucide-react';
import { Pie, Bar, Line, Column, Radar, Area } from '@ant-design/plots';
import { useAnalysis } from '../contexts/AnalysisContext';

const Analytics = () => {
  const [loading, setLoading] = useState(true);
  const { lastAnalysis } = useAnalysis();

  useEffect(() => {
    setTimeout(() => setLoading(false), 500);
  }, []);

  if (loading || !lastAnalysis) {
    return (
      <div className="content-area">
        <div className="card" style={{ textAlign: 'center', padding: '3rem' }}>
          <div style={{ fontSize: '1.25rem', color: 'var(--secondary)' }}>
            📊 Upload an image first to view analytics
          </div>
        </div>
      </div>
    );
  }

  const data = lastAnalysis;
  const crackData = data.crack_detection || {};
  const materialData = data.material_analysis || {};
  const envData = data.environmental_impact_assessment || {};
  const bioData = data.biological_growth || {};
  const insights = data.data_science_insights || {};

  // KPI Metrics
  const kpiMetrics = [
    {
      label: 'Structural Health',
      value: `${insights.statistical_summary?.structural_health_score?.toFixed(1) || 0}/100`,
      icon: Shield,
      color: '#3b82f6',
      gradient: 'rgba(59, 130, 246, 0.1)'
    },
    {
      label: 'Total Damage Count',
      value: crackData.count || 0,
      icon: AlertTriangle,
      color: '#dc2626',
      gradient: 'rgba(220, 38, 38, 0.1)'
    },
    {
      label: 'Material Durability',
      value: `${materialData.durability_score?.toFixed(1) || 0}/10`,
      icon: Target,
      color: '#16a34a',
      gradient: 'rgba(34, 197, 94, 0.1)'
    },
    {
      label: 'Environmental Score',
      value: `${envData.sustainability_score?.toFixed(1) || 0}/10`,
      icon: Leaf,
      color: '#8b5cf6',
      gradient: 'rgba(139, 92, 246, 0.1)'
    }
  ];

  // Severity Distribution
  const severityData = crackData.statistics?.severity_distribution
    ? Object.entries(crackData.statistics.severity_distribution).map(([key, value]) => ({
        type: key,
        value: value,
        color: {
          'Critical': '#dc2626',
          'Severe': '#ea580c',
          'Moderate': '#ca8a04',
          'Minor': '#16a34a'
        }[key]
      }))
    : [];

  const severityConfig = severityData.length > 0 ? {
    data: severityData,
    angleField: 'value',
    colorField: 'type',
    radius: 0.8,
    innerRadius: 0.6,
    label: { content: '{percentage}' },
    color: ({ type }) => {
      const colors = {
        'Critical': '#dc2626',
        'Severe': '#ea580c',
        'Moderate': '#ca8a04',
        'Minor': '#16a34a'
      };
      return colors[type] || '#6b7280';
    }
  } : null;

  // Material Composition
  const materialChartData = materialData.probabilities
    ? Object.entries(materialData.probabilities).map(([material, prob]) => ({
        material,
        confidence: parseFloat((prob * 100).toFixed(1))
      }))
    : [];

  const materialConfig = materialChartData.length > 0 ? {
    data: materialChartData,
    xField: 'material',
    yField: 'confidence',
    seriesField: 'material',
    color: '#3b82f6',
    columnStyle: { radius: [8, 8, 0, 0] }
  } : null;

  // Health Trend
  const healthTrendData = [
    {
      date: 'Current',
      'Health Score': insights.statistical_summary?.structural_health_score || 0,
      'Risk Level': 100 - (insights.statistical_summary?.structural_health_score || 0)
    }
  ];

  const healthTrendConfig = {
    data: healthTrendData,
    xField: 'date',
    yField: ['Health Score', 'Risk Level'],
    seriesField: 'y',
    smooth: true
  };

  // Environmental Impact
  const envRadarData = [
    {
      metric: 'Carbon Impact',
      value: Math.min((envData.carbon_footprint_kg / 1000) * 100, 100) || 0
    },
    {
      metric: 'Water Usage',
      value: Math.min((envData.water_footprint_liters / 5000) * 100, 100) || 0
    },
    {
      metric: 'Energy',
      value: Math.min((envData.energy_consumption_kwh / 500) * 100, 100) || 0
    },
    {
      metric: 'Bio-Growth',
      value: bioData.growth_percentage || 0
    },
    {
      metric: 'Eco-Efficiency',
      value: (envData.eco_efficiency_rating / 10) * 100 || 0
    }
  ];

  const radarConfig = {
    data: envRadarData,
    xField: 'metric',
    yField: 'value',
    appendPadding: [15, 15, 15, 15],
    color: '#3b82f6',
    point: { size: 3, shape: 'circle' },
    smooth: true
  };

  // Crack Details Table
  const damageMetrics = [
    {
      label: 'Critical Issues',
      value: crackData.statistics?.severity_distribution?.Critical || 0,
      color: '#dc2626'
    },
    {
      label: 'Severe Issues',
      value: crackData.statistics?.severity_distribution?.Severe || 0,
      color: '#ea580c'
    },
    {
      label: 'Moderate Issues',
      value: crackData.statistics?.severity_distribution?.Moderate || 0,
      color: '#ca8a04'
    },
    {
      label: 'Minor Issues',
      value: crackData.statistics?.severity_distribution?.Minor || 0,
      color: '#16a34a'
    }
  ];

  return (
    <div className="content-area">
      {/* Header */}
      <div className="card" style={{ marginBottom: '2rem' }}>
        <div className="card-header">
          <h2 style={{ margin: 0, display: 'flex', alignItems: 'center', gap: '0.6rem' }}>
            <BarChart3 size={28} />
            📊 Comprehensive Analytics Dashboard
          </h2>
          <p style={{ margin: '0.25rem 0 0 0', color: 'var(--secondary)', fontSize: '0.875rem' }}>
            Project-specific metrics: structural damage, material analysis, environmental impact & deterioration forecasting
          </p>
        </div>
      </div>

      {/* KPI Cards */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1.5rem', marginBottom: '2rem' }}>
        {kpiMetrics.map((metric, idx) => (
          <div key={idx} style={{ background: metric.gradient, padding: '1.5rem', borderRadius: 'var(--border-radius)', border: `1px solid ${metric.color}20` }}>
            <div style={{ fontSize: '0.75rem', color: 'var(--secondary)', fontWeight: '600', marginBottom: '0.5rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <metric.icon size={16} /> {metric.label}
            </div>
            <div style={{ fontSize: '2rem', fontWeight: '700', color: metric.color }}>
              {metric.value}
            </div>
          </div>
        ))}
      </div>

      {/* Charts Grid */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(500px, 1fr))', gap: '2rem', marginBottom: '2rem' }}>
        {/* Severity Distribution */}
        <div className="card">
          <div className="card-header">
            <h3 style={{ margin: 0, display: 'flex', alignItems: 'center', gap: '0.6rem' }}>
              <AlertTriangle size={20} />
              Damage Severity Distribution
            </h3>
          </div>
          <div className="card-body" style={{ height: '300px' }}>
            {severityConfig ? (
              <Pie {...severityConfig} />
            ) : (
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: '100%', color: 'var(--secondary)' }}>
                No damage severity data
              </div>
            )}
          </div>
        </div>

        {/* Environmental Impact */}
        <div className="card">
          <div className="card-header">
            <h3 style={{ margin: 0, display: 'flex', alignItems: 'center', gap: '0.6rem' }}>
              <Wind size={20} />
              Environmental Impact Profile
            </h3>
          </div>
          <div className="card-body" style={{ height: '300px' }}>
            <Radar {...radarConfig} />
          </div>
        </div>
      </div>

      {/* Second Row Charts */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(500px, 1fr))', gap: '2rem', marginBottom: '2rem' }}>
        {/* Material Composition */}
        <div className="card">
          <div className="card-header">
            <h3 style={{ margin: 0, display: 'flex', alignItems: 'center', gap: '0.6rem' }}>
              <Target size={20} />
              Material Composition Analysis
            </h3>
          </div>
          <div className="card-body" style={{ height: '300px' }}>
            {materialConfig ? (
              <Column {...materialConfig} />
            ) : (
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: '100%', color: 'var(--secondary)' }}>
                No material data
              </div>
            )}
          </div>
        </div>

        {/* Damage Breakdown */}
        <div className="card">
          <div className="card-header">
            <h3 style={{ margin: 0, display: 'flex', alignItems: 'center', gap: '0.6rem' }}>
              <BarChart3 size={20} />
              Damage Category Breakdown
            </h3>
          </div>
          <div className="card-body">
            <div style={{ display: 'grid', gap: '1rem' }}>
              {damageMetrics.map((metric, idx) => (
                <div key={idx} style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '1rem', background: 'var(--light)', borderRadius: 'var(--border-radius)', border: '1px solid var(--glass-border)' }}>
                  <div style={{ fontSize: '0.875rem', fontWeight: '500', color: 'var(--dark)' }}>
                    {metric.label}
                  </div>
                  <div style={{ fontSize: '1.5rem', fontWeight: '700', color: metric.color }}>
                    {metric.value}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Environmental Summary */}
      <div className="card" style={{ marginBottom: '2rem' }}>
        <div className="card-header">
          <h3 style={{ margin: 0, display: 'flex', alignItems: 'center', gap: '0.6rem' }}>
            <Zap size={20} />
            Environmental Impact Summary
          </h3>
        </div>
        <div className="card-body">
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1.5rem' }}>
            <div style={{ padding: '1.5rem', background: 'linear-gradient(135deg, rgba(220, 38, 38, 0.1), rgba(239, 68, 68, 0.1))', borderRadius: 'var(--border-radius)', border: '1px solid rgba(220, 38, 38, 0.2)' }}>
              <div style={{ fontSize: '0.75rem', color: 'var(--secondary)', fontWeight: '600', marginBottom: '0.5rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                <Wind size={16} /> Carbon Footprint
              </div>
              <div style={{ fontSize: '1.75rem', fontWeight: '700', color: '#dc2626' }}>
                {envData.carbon_footprint_kg?.toFixed(2) || 0} kg CO₂
              </div>
            </div>

            <div style={{ padding: '1.5rem', background: 'linear-gradient(135deg, rgba(59, 130, 246, 0.1), rgba(139, 92, 246, 0.1))', borderRadius: 'var(--border-radius)', border: '1px solid rgba(59, 130, 246, 0.2)' }}>
              <div style={{ fontSize: '0.75rem', color: 'var(--secondary)', fontWeight: '600', marginBottom: '0.5rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                <Droplet size={16} /> Water Footprint
              </div>
              <div style={{ fontSize: '1.75rem', fontWeight: '700', color: '#3b82f6' }}>
                {envData.water_footprint_liters?.toFixed(2) || 0} L
              </div>
            </div>

            <div style={{ padding: '1.5rem', background: 'linear-gradient(135deg, rgba(245, 158, 11, 0.1), rgba(249, 180, 0, 0.1))', borderRadius: 'var(--border-radius)', border: '1px solid rgba(245, 158, 11, 0.2)' }}>
              <div style={{ fontSize: '0.75rem', color: 'var(--secondary)', fontWeight: '600', marginBottom: '0.5rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                <Zap size={16} /> Energy Consumption
              </div>
              <div style={{ fontSize: '1.75rem', fontWeight: '700', color: '#f59e0b' }}>
                {envData.energy_consumption_kwh?.toFixed(2) || 0} kWh
              </div>
            </div>

            <div style={{ padding: '1.5rem', background: 'linear-gradient(135deg, rgba(34, 197, 94, 0.1), rgba(22, 163, 74, 0.1))', borderRadius: 'var(--border-radius)', border: '1px solid rgba(34, 197, 94, 0.2)' }}>
              <div style={{ fontSize: '0.75rem', color: 'var(--secondary)', fontWeight: '600', marginBottom: '0.5rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                <Leaf size={16} /> Eco-Efficiency
              </div>
              <div style={{ fontSize: '1.75rem', fontWeight: '700', color: '#16a34a' }}>
                {(envData.eco_efficiency_rating / 10 * 100)?.toFixed(0) || 0}%
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Key Insights */}
      <div className="card">
        <div className="card-header">
          <h3 style={{ margin: 0, display: 'flex', alignItems: 'center', gap: '0.6rem' }}>
            <CheckCircle size={20} />
            💡 Key Insights & Recommendations
          </h3>
        </div>
        <div className="card-body">
          <div style={{ display: 'grid', gap: '1rem' }}>
            <div style={{ padding: '1rem', background: 'var(--light)', borderRadius: 'var(--border-radius)', border: '1px solid var(--glass-border)', display: 'flex', alignItems: 'flex-start', gap: '1rem' }}>
              <AlertTriangle size={20} style={{ color: '#3b82f6', flexShrink: 0, marginTop: '0.25rem' }} />
              <div>
                <div style={{ fontWeight: '600', color: 'var(--dark)', marginBottom: '0.25rem' }}>Structural Assessment</div>
                <div style={{ fontSize: '0.875rem', color: 'var(--secondary)' }}>
                  {insights.statistical_summary?.structural_health_score > 75 ? '✓ Structure is in excellent condition. Continue regular monitoring.' : 
                   insights.statistical_summary?.structural_health_score > 50 ? '⚠ Structure requires scheduled maintenance within 6-12 months.' : 
                   '✗ Structure requires immediate inspection and repairs.'}
                </div>
              </div>
            </div>

            <div style={{ padding: '1rem', background: 'var(--light)', borderRadius: 'var(--border-radius)', border: '1px solid var(--glass-border)', display: 'flex', alignItems: 'flex-start', gap: '1rem' }}>
              <Leaf size={20} style={{ color: '#10b981', flexShrink: 0, marginTop: '0.25rem' }} />
              <div>
                <div style={{ fontWeight: '600', color: 'var(--dark)', marginBottom: '0.25rem' }}>Biological Contamination</div>
                <div style={{ fontSize: '0.875rem', color: 'var(--secondary)' }}>
                  {bioData.growth_percentage > 20 ? '⚠️ High biological contamination detected. Recommend cleaning and treatment.' :
                   bioData.growth_percentage > 10 ? '⚡ Moderate contamination. Monitor and clean if necessary.' :
                   '✓ Minimal biological growth. Maintain current maintenance schedule.'}
                </div>
              </div>
            </div>

            <div style={{ padding: '1rem', background: 'var(--light)', borderRadius: 'var(--border-radius)', border: '1px solid var(--glass-border)', display: 'flex', alignItems: 'flex-start', gap: '1rem' }}>
              <Shield size={20} style={{ color: '#f59e0b', flexShrink: 0, marginTop: '0.25rem' }} />
              <div>
                <div style={{ fontWeight: '600', color: 'var(--dark)', marginBottom: '0.25rem' }}>Environmental Sustainability</div>
                <div style={{ fontSize: '0.875rem', color: 'var(--secondary)' }}>
                  Carbon footprint: {envData.carbon_footprint_kg?.toFixed(2) || 0} kg CO₂. Eco-efficiency rating: {envData.eco_efficiency_rating?.toFixed(1) || 0}/10.
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Analytics;
