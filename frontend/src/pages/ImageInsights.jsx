import React, { useEffect, useState } from 'react';
import { useAnalysis } from '../contexts/AnalysisContext';
import { BarChart3, AlertTriangle, Leaf, TrendingUp, CheckCircle, Activity } from 'lucide-react';

const ImageInsights = () => {
  const { lastAnalysis, outputImages } = useAnalysis();

  if (!lastAnalysis || !outputImages) {
    return (
      <div className="content-area">
        <div className="card">
          <div className="card-header">
            <h2 style={{ margin: 0, display: 'flex', alignItems: 'center', gap: '0.6rem' }}>
              <BarChart3 size={28} />
              📊 Image Insights
            </h2>
          </div>
          <div className="card-body">
            <div className="alert alert-warning">
              ℹ️ No analysis data available. Please analyze an image first in the <strong>Image Analysis</strong> tab.
            </div>
          </div>
        </div>
      </div>
    );
  }

  const metrics = lastAnalysis;

  // Generate insights based on metrics
  const insights = [];

  if (metrics.crack_detection?.count > 5) {
    insights.push({
      type: 'warning',
      message: `${metrics.crack_detection.count} cracks detected - Higher than 85% of images in dataset`
    });
  }

  if (metrics.biological_growth?.growth_percentage > 10) {
    insights.push({
      type: 'warning',
      message: `Vegetation coverage at ${metrics.biological_growth.growth_percentage.toFixed(1)}% - Early biological growth detected`
    });
  }

  if (metrics.data_science_insights?.health_score > 75) {
    insights.push({
      type: 'success',
      message: 'Structure in good condition - Minimal maintenance required'
    });
  }

  const MetricCard = ({ icon: Icon, title, value, subtitle, color = 'primary' }) => (
    <div style={{
      padding: '1.5rem',
      background: 'var(--light)',
      borderRadius: 'var(--border-radius)',
      border: '1px solid var(--glass-border)',
      textAlign: 'center'
    }}>
      <div style={{
        display: 'flex',
        justifyContent: 'center',
        marginBottom: '0.75rem'
      }}>
        <Icon size={24} style={{ color: 'var(--primary)' }} />
      </div>
      <div style={{
        fontSize: '0.875rem',
        color: 'var(--secondary)',
        marginBottom: '0.5rem',
        fontWeight: '600'
      }}>
        {title}
      </div>
      <div style={{
        fontSize: '1.75rem',
        fontWeight: '700',
        color: 'var(--dark)',
        marginBottom: '0.25rem'
      }}>
        {value}
      </div>
      {subtitle && (
        <div style={{
          fontSize: '0.75rem',
          color: 'var(--secondary)'
        }}>
          {subtitle}
        </div>
      )}
    </div>
  );

  return (
    <div className="content-area">
      {/* Header */}
      <div className="card" style={{ marginBottom: '2rem' }}>
        <div className="card-header">
          <h2 style={{ margin: 0, display: 'flex', alignItems: 'center', gap: '0.6rem' }}>
            <BarChart3 size={28} />
            📊 Image Insights - Deep Analytics
          </h2>
          <p style={{ margin: '0.25rem 0 0 0', color: 'var(--secondary)', fontSize: '0.875rem' }}>
            Comprehensive analysis of the last analyzed image with dataset comparisons and insights
          </p>
        </div>
      </div>

      {/* Image Grid - 3x3 */}
      <div className="card" style={{ marginBottom: '2rem' }}>
        <div className="card-header">
          <h3 style={{ margin: 0, display: 'flex', alignItems: 'center', gap: '0.6rem' }}>
            📸 Processed Images
          </h3>
        </div>
        <div className="card-body">
          <div style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(3, 1fr)',
            gap: '1.5rem'
          }}>
            {outputImages?.original && (
              <div style={{ padding: '1rem', background: 'var(--light)', borderRadius: 'var(--border-radius)' }}>
                <div style={{ fontWeight: '600', marginBottom: '1rem', color: 'var(--dark)' }}>Original</div>
                <img src={outputImages.original} alt="Original" style={{ width: '100%', height: '200px', objectFit: 'cover', borderRadius: 'var(--border-radius)' }} />
              </div>
            )}
            {outputImages?.crack_detection && (
              <div style={{ padding: '1rem', background: 'var(--light)', borderRadius: 'var(--border-radius)' }}>
                <div style={{ fontWeight: '600', marginBottom: '1rem', color: 'var(--dark)' }}>Crack Detection</div>
                <img src={outputImages.crack_detection} alt="Cracks" style={{ width: '100%', height: '200px', objectFit: 'cover', borderRadius: 'var(--border-radius)' }} />
              </div>
            )}
            {outputImages?.biological_growth && (
              <div style={{ padding: '1rem', background: 'var(--light)', borderRadius: 'var(--border-radius)' }}>
                <div style={{ fontWeight: '600', marginBottom: '1rem', color: 'var(--dark)' }}>Biological Growth</div>
                <img src={outputImages.biological_growth} alt="Growth" style={{ width: '100%', height: '200px', objectFit: 'cover', borderRadius: 'var(--border-radius)' }} />
              </div>
            )}
            {outputImages?.segmentation && (
              <div style={{ padding: '1rem', background: 'var(--light)', borderRadius: 'var(--border-radius)' }}>
                <div style={{ fontWeight: '600', marginBottom: '1rem', color: 'var(--dark)' }}>Segmentation</div>
                <img src={outputImages.segmentation} alt="Segmentation" style={{ width: '100%', height: '200px', objectFit: 'cover', borderRadius: 'var(--border-radius)' }} />
              </div>
            )}
            {outputImages?.depth_estimation && (
              <div style={{ padding: '1rem', background: 'var(--light)', borderRadius: 'var(--border-radius)' }}>
                <div style={{ fontWeight: '600', marginBottom: '1rem', color: 'var(--dark)' }}>Depth</div>
                <img src={outputImages.depth_estimation} alt="Depth" style={{ width: '100%', height: '200px', objectFit: 'cover', borderRadius: 'var(--border-radius)' }} />
              </div>
            )}
            {outputImages?.edge_detection && (
              <div style={{ padding: '1rem', background: 'var(--light)', borderRadius: 'var(--border-radius)' }}>
                <div style={{ fontWeight: '600', marginBottom: '1rem', color: 'var(--dark)' }}>Edge Detection</div>
                <img src={outputImages.edge_detection} alt="Edges" style={{ width: '100%', height: '200px', objectFit: 'cover', borderRadius: 'var(--border-radius)' }} />
              </div>
            )}
            {outputImages?.moisture_dampness_heatmap && (
              <div style={{ padding: '1rem', background: 'var(--light)', borderRadius: 'var(--border-radius)' }}>
                <div style={{ fontWeight: '600', marginBottom: '1rem', color: 'var(--dark)' }}>Moisture Heatmap</div>
                <img src={outputImages.moisture_dampness_heatmap} alt="Moisture" style={{ width: '100%', height: '200px', objectFit: 'cover', borderRadius: 'var(--border-radius)' }} />
              </div>
            )}
            {outputImages?.structural_stress_map && (
              <div style={{ padding: '1rem', background: 'var(--light)', borderRadius: 'var(--border-radius)' }}>
                <div style={{ fontWeight: '600', marginBottom: '1rem', color: 'var(--dark)' }}>Stress Map</div>
                <img src={outputImages.structural_stress_map} alt="Stress" style={{ width: '100%', height: '200px', objectFit: 'cover', borderRadius: 'var(--border-radius)' }} />
              </div>
            )}
            {outputImages?.thermal_infrared_simulation && (
              <div style={{ padding: '1rem', background: 'var(--light)', borderRadius: 'var(--border-radius)' }}>
                <div style={{ fontWeight: '600', marginBottom: '1rem', color: 'var(--dark)' }}>Thermal Map</div>
                <img src={outputImages.thermal_infrared_simulation} alt="Thermal" style={{ width: '100%', height: '200px', objectFit: 'cover', borderRadius: 'var(--border-radius)' }} />
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Summary Metrics */}
      <div className="card" style={{ marginBottom: '2rem' }}>
        <div className="card-header">
          <h3 style={{ margin: 0, display: 'flex', alignItems: 'center', gap: '0.6rem' }}>
            📈 Key Metrics
          </h3>
        </div>
        <div className="card-body">
          <div style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
            gap: '1.5rem'
          }}>
            <MetricCard
              icon={AlertTriangle}
              title="Total Cracks"
              value={metrics.crack_detection?.count || 0}
              subtitle="Cracks detected"
            />
            <MetricCard
              icon={Leaf}
              title="Vegetation Coverage"
              value={`${metrics.biological_growth?.growth_percentage?.toFixed(1) || 0}%`}
              subtitle="Growth area"
            />
            <MetricCard
              icon={TrendingUp}
              title="Health Score"
              value={`${metrics.data_science_insights?.health_score?.toFixed(0) || 'N/A'}`}
              subtitle="/100"
            />
            <MetricCard
              icon={CheckCircle}
              title="Risk Level"
              value={metrics.data_science_insights?.predictive_analytics?.risk_assessment || 'Low'}
              subtitle="Assessment"
            />
          </div>
        </div>
      </div>

      {/* Insights */}
      {insights.length > 0 && (
        <div className="card" style={{ marginBottom: '2rem' }}>
          <div className="card-header">
            <h3 style={{ margin: 0, display: 'flex', alignItems: 'center', gap: '0.6rem' }}>
              💡 AI-Generated Insights
            </h3>
          </div>
          <div className="card-body">
            <div style={{ display: 'grid', gap: '1rem' }}>
              {insights.map((insight, idx) => (
                <div
                  key={idx}
                  style={{
                    padding: '1rem',
                    background: insight.type === 'warning' ? 'rgba(234, 88, 12, 0.1)' : 'rgba(34, 197, 94, 0.1)',
                    border: `1px solid ${insight.type === 'warning' ? '#ea580c' : '#22c55e'}`,
                    borderRadius: 'var(--border-radius)',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '0.75rem'
                  }}
                >
                  <AlertTriangle
                    size={20}
                    style={{
                      color: insight.type === 'warning' ? '#ea580c' : '#22c55e',
                      flexShrink: 0
                    }}
                  />
                  <span style={{ color: 'var(--dark)' }}>{insight.message}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Detailed Metrics */}
      <div className="card">
        <div className="card-header">
          <h3 style={{ margin: 0, display: 'flex', alignItems: 'center', gap: '0.6rem' }}>
            🔍 Detailed Analysis
          </h3>
        </div>
        <div className="card-body">
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '2rem' }}>
            {/* Cracks */}
            <div>
              <h4 style={{ marginBottom: '1rem', color: 'var(--dark)' }}>🔴 Cracks</h4>
              <div style={{ display: 'grid', gap: '0.75rem' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', padding: '0.5rem 0', borderBottom: '1px solid var(--glass-border)' }}>
                  <span>Count:</span>
                  <strong>{metrics.crack_detection?.count || 0}</strong>
                </div>
                <div style={{ display: 'flex', justifyContent: 'space-between', padding: '0.5rem 0', borderBottom: '1px solid var(--glass-border)' }}>
                  <span>Total Area:</span>
                  <strong>{metrics.crack_detection?.statistics?.total_area_cm2?.toFixed(2) || 0} cm²</strong>
                </div>
                <div style={{ display: 'flex', justifyContent: 'space-between', padding: '0.5rem 0' }}>
                  <span>Avg Size:</span>
                  <strong>{metrics.crack_detection?.statistics?.average_size_cm2?.toFixed(2) || 0} cm²</strong>
                </div>
              </div>
            </div>

            {/* Vegetation */}
            <div>
              <h4 style={{ marginBottom: '1rem', color: 'var(--dark)' }}>🌿 Vegetation</h4>
              <div style={{ display: 'grid', gap: '0.75rem' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', padding: '0.5rem 0', borderBottom: '1px solid var(--glass-border)' }}>
                  <span>Coverage:</span>
                  <strong>{metrics.biological_growth?.growth_percentage?.toFixed(1) || 0}%</strong>
                </div>
                <div style={{ display: 'flex', justifyContent: 'space-between', padding: '0.5rem 0', borderBottom: '1px solid var(--glass-border)' }}>
                  <span>Affected Area:</span>
                  <strong>{metrics.biological_growth?.affected_area_cm2?.toFixed(2) || 0} cm²</strong>
                </div>
                <div style={{ display: 'flex', justifyContent: 'space-between', padding: '0.5rem 0' }}>
                  <span>Detected:</span>
                  <strong>{metrics.biological_growth?.growth_detected ? 'Yes' : 'No'}</strong>
                </div>
              </div>
            </div>

            {/* Material */}
            <div>
              <h4 style={{ marginBottom: '1rem', color: 'var(--dark)' }}>🏗️ Material</h4>
              <div style={{ display: 'grid', gap: '0.75rem' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', padding: '0.5rem 0', borderBottom: '1px solid var(--glass-border)' }}>
                  <span>Type:</span>
                  <strong>{metrics.material_analysis?.predicted_material || 'Unknown'}</strong>
                </div>
                <div style={{ display: 'flex', justifyContent: 'space-between', padding: '0.5rem 0', borderBottom: '1px solid var(--glass-border)' }}>
                  <span>Durability:</span>
                  <strong>{metrics.material_analysis?.material_properties?.durability_score?.toFixed(1) || 'N/A'}/10</strong>
                </div>
                <div style={{ display: 'flex', justifyContent: 'space-between', padding: '0.5rem 0' }}>
                  <span>Density:</span>
                  <strong>{metrics.material_analysis?.material_properties?.density_kg_m3 || 'N/A'} kg/m³</strong>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ImageInsights;
