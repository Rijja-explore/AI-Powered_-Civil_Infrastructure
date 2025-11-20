import React, { useState, useEffect } from 'react';
import { TrendingUp, AlertTriangle, BarChart3, Target, Wind, Droplet, Zap, Leaf, Shield, Activity, CheckCircle, AlertCircle } from 'lucide-react';
import { Pie, Bar, Line, Column, Radar } from '@ant-design/plots';
import toast from 'react-hot-toast';
import { useAnalysis } from '../contexts/AnalysisContext';

const Analytics = () => {
  const [loading, setLoading] = useState(true);
  const { lastAnalysis } = useAnalysis();

  useEffect(() => {
    // Simulate loading delay for UX
    setTimeout(() => setLoading(false), 500);
  }, []);

  if (loading || !lastAnalysis) {
    return (
      <div className="content-area">
        <div className="card" style={{ textAlign: 'center', padding: '3rem' }}>
          <div style={{ fontSize: '1.25rem', color: 'var(--secondary)' }}>
            📊 Upload an image first to view detailed analytics
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

  // Data for Severity Distribution Pie Chart
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

  // Data for Material Composition Bar Chart
  const materialChartData = materialData.probabilities
    ? Object.entries(materialData.probabilities).map(([material, prob]) => ({
        material,
        confidence: (prob * 100).toFixed(1)
      }))
    : [];

  // Health Score Trend (simulated from current data)
  const healthTrendData = [
    {
      date: 'Current Analysis',
      'Health Score': insights.health_score || 0,
      'Deterioration Index': 100 - (insights.health_score || 0)
    }
  ];

  // Damage Assessment Metrics
  const damageMetrics = [
    {
      label: '🔴 Critical Issues',
      value: crackData.statistics?.severity_distribution?.Critical || 0,
      color: '#dc2626'
    },
    {
      label: '🟠 Severe Issues',
      value: crackData.statistics?.severity_distribution?.Severe || 0,
      color: '#ea580c'
    },
    {
      label: '🟡 Moderate Issues',
      value: crackData.statistics?.severity_distribution?.Moderate || 0,
      color: '#ca8a04'
    },
    {
      label: '🟢 Minor Issues',
      value: crackData.statistics?.severity_distribution?.Minor || 0,
      color: '#16a34a'
    }
  ];

  // Environmental Impact Radar Data
  const environmentalRadarData = [
    {
      metric: 'Carbon Impact',
      value: Math.min((envData.carbon_footprint_kg / 1000) * 100, 100) || 0
    },
    {
      metric: 'Water Usage',
      value: Math.min((envData.water_footprint_liters / 5000) * 100, 100) || 0
    },
    {
      metric: 'Energy Consumption',
      value: Math.min((envData.energy_consumption_kwh / 500) * 100, 100) || 0
    },
    {
      metric: 'Bio-contamination',
      value: bioData.growth_percentage || 0
    },
    {
      metric: 'Eco-Efficiency',
      value: (envData.eco_efficiency_rating / 10) * 100 || 0
    }
  ];

  const severityConfig = severityData.length > 0 ? {
    data: severityData,
    angleField: 'value',
    colorField: 'type',
    radius: 0.8,
    innerRadius: 0.6,
    label: {
      content: '{percentage}'
    },
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

  const materialConfig = materialChartData.length > 0 ? {
    data: materialChartData,
    xField: 'material',
    yField: 'confidence',
    seriesField: 'material',
    color: '#3b82f6',
    columnStyle: {
      radius: [8, 8, 0, 0]
    }
  } : null;

  const healthTrendConfig = {
    data: healthTrendData,
    xField: 'date',
    yField: ['Health Score', 'Deterioration Index'],
    seriesField: 'y',
    geometryOptions: [
      {
        geometry: 'line',
        color: ['#3b82f6', '#ef4444']
      }
    ]
  };

  const radarConfig = {
    data: environmentalRadarData,
    xField: 'metric',
    yField: 'value',
    seriesField: 'category',
    appendPadding: [15, 15, 15, 15],
    color: ['#3b82f6'],
    point: {
      size: 3,
      shape: 'circle'
    },
    smooth: true
  };

  return (
    <div className="content-area">
      {/* Header */}
      <div className="card" style={{ marginBottom: '2rem' }}>
        <div className="card-header">
          <h2 style={{ margin: 0, display: 'flex', alignItems: 'center', gap: '0.6rem' }}>
            <BarChart3 size={28} />
            📊 Infrastructure Health Analytics
          </h2>
          <p style={{ margin: '0.25rem 0 0 0', color: 'var(--secondary)', fontSize: '0.875rem' }}>
            Project-specific metrics: structural damage, material analysis, environmental impact & deterioration forecasting
          </p>
        </div>
      </div>

      {/* Executive Summary Cards */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1.5rem', marginBottom: '2rem' }}>
        <div style={{ background: 'linear-gradient(135deg, rgba(59, 130, 246, 0.1), rgba(99, 102, 241, 0.1))', padding: '1.5rem', borderRadius: 'var(--border-radius)', border: '1px solid rgba(59, 130, 246, 0.2)' }}>
          <div style={{ fontSize: '0.75rem', color: 'var(--secondary)', fontWeight: '600', marginBottom: '0.5rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <Activity size={16} /> Overall Health Score
          </div>
          <div style={{ fontSize: '2.5rem', fontWeight: '700', color: '#3b82f6' }}>
            {insights.health_score?.toFixed(1) || 'N/A'}/100
          </div>
          <div style={{ fontSize: '0.7rem', color: 'var(--secondary)', marginTop: '0.5rem' }}>
            {insights.health_score > 75 ? '✓ Excellent' : insights.health_score > 50 ? '⚠ Fair' : '✗ Poor'}
          </div>
        </div>

        <div style={{ background: 'linear-gradient(135deg, rgba(239, 68, 68, 0.1), rgba(245, 158, 11, 0.1))', padding: '1.5rem', borderRadius: 'var(--border-radius)', border: '1px solid rgba(239, 68, 68, 0.2)' }}>
          <div style={{ fontSize: '0.75rem', color: 'var(--secondary)', fontWeight: '600', marginBottom: '0.5rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <AlertTriangle size={16} /> Total Damage Count
          </div>
          <div style={{ fontSize: '2.5rem', fontWeight: '700', color: '#dc2626' }}>
            {crackData.count || 0}
          </div>
          <div style={{ fontSize: '0.7rem', color: 'var(--secondary)', marginTop: '0.5rem' }}>
            Affected area: {crackData.statistics?.total_area_cm2?.toFixed(2) || 0} cm²
          </div>
        </div>

        <div style={{ background: 'linear-gradient(135deg, rgba(34, 197, 94, 0.1), rgba(22, 163, 74, 0.1))', padding: '1.5rem', borderRadius: 'var(--border-radius)', border: '1px solid rgba(34, 197, 94, 0.2)' }}>
          <div style={{ fontSize: '0.75rem', color: 'var(--secondary)', fontWeight: '600', marginBottom: '0.5rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <Shield size={16} /> Primary Material
          </div>
          <div style={{ fontSize: '1.5rem', fontWeight: '700', color: '#16a34a', marginTop: '0.5rem' }}>
            {materialData.predicted_material || 'Unknown'}
          </div>
          <div style={{ fontSize: '0.7rem', color: 'var(--secondary)', marginTop: '0.5rem' }}>
            Durability: {materialData.durability_score?.toFixed(1) || 'N/A'}/10
          </div>
        </div>

        <div style={{ background: 'linear-gradient(135deg, rgba(59, 130, 246, 0.1), rgba(139, 92, 246, 0.1))', padding: '1.5rem', borderRadius: 'var(--border-radius)', border: '1px solid rgba(59, 130, 246, 0.2)' }}>
          <div style={{ fontSize: '0.75rem', color: 'var(--secondary)', fontWeight: '600', marginBottom: '0.5rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <Leaf size={16} /> Biological Growth
          </div>
          <div style={{ fontSize: '2.5rem', fontWeight: '700', color: '#8b5cf6' }}>
            {bioData.growth_percentage?.toFixed(1) || 0}%
          </div>
          <div style={{ fontSize: '0.7rem', color: 'var(--secondary)', marginTop: '0.5rem' }}>
            Coverage intensity level
          </div>
        </div>
      </div>

      {/* Main Analytics Grid */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(500px, 1fr))', gap: '2rem', marginBottom: '2rem' }}>
        {/* Severity Distribution */}
        <div className="card">
          <div className="card-header">
            <h3 style={{ margin: 0, display: 'flex', alignItems: 'center', gap: '0.6rem' }}>
              <AlertTriangle size={20} />
              ⚠️ Damage Severity Distribution
            </h3>
          </div>
          <div className="card-body" style={{ height: '300px' }}>
            {severityConfig ? (
              <Pie {...severityConfig} />
            ) : (
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: '100%', color: 'var(--secondary)' }}>
                No damage severity data available
              </div>
            )}
          </div>
        </div>

        {/* Environmental Impact Radar */}
        <div className="card">
          <div className="card-header">
            <h3 style={{ margin: 0, display: 'flex', alignItems: 'center', gap: '0.6rem' }}>
              <Wind size={20} />
              🌍 Environmental Impact Profile
            </h3>
          </div>
          <div className="card-body" style={{ height: '300px' }}>
            <Radar {...radarConfig} />
          </div>
        </div>
      </div>

      {/* Material & Damage Metrics */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(500px, 1fr))', gap: '2rem', marginBottom: '2rem' }}>
        {/* Material Composition */}
        <div className="card">
          <div className="card-header">
            <h3 style={{ margin: 0, display: 'flex', alignItems: 'center', gap: '0.6rem' }}>
              <Target size={20} />
              🏗️ Material Composition Analysis
            </h3>
          </div>
          <div className="card-body" style={{ height: '300px' }}>
            {materialConfig ? (
              <Column {...materialConfig} />
            ) : (
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: '100%', color: 'var(--secondary)' }}>
                No material data available
              </div>
            )}
          </div>
        </div>

        {/* Damage Category Breakdown */}
        <div className="card">
          <div className="card-header">
            <h3 style={{ margin: 0, display: 'flex', alignItems: 'center', gap: '0.6rem' }}>
              <BarChart3 size={20} />
              📋 Damage Category Breakdown
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

      {/* Environmental Metrics Summary */}
      <div className="card">
        <div className="card-header">
          <h3 style={{ margin: 0, display: 'flex', alignItems: 'center', gap: '0.6rem' }}>
            <Zap size={20} />
            ⚡ Environmental Impact Summary
          </h3>
        </div>
        <div className="card-body">
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '1.5rem' }}>
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

      {/* Key Insights Card */}
      <div className="card" style={{ marginTop: '2rem' }}>
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
                  {insights.health_score > 75 ? '✓ Structure is in excellent condition. Continue regular monitoring.' : 
                   insights.health_score > 50 ? '⚠ Structure requires scheduled maintenance within 6-12 months.' : 
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
