import React, { useEffect, useState } from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell, LineChart, Line, CartesianGrid, ScatterChart, Scatter, ZAxis } from 'recharts';
import './quickAnalytics.css';

/**
 * QuickAnalytics Component
 * Displays dataset-level analytics:
 * - Image distribution by split and category
 * - Statistical test results
 * - Risk score distributions
 * - Correlation matrices as heatmaps
 */

const QuickAnalytics = () => {
  const [analyticsData, setAnalyticsData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchAnalytics();
  }, []);

  const fetchAnalytics = async () => {
    try {
      setLoading(true);
      const response = await fetch('/api/analytics/dataset');
      if (!response.ok) throw new Error('Failed to load analytics');
      const data = await response.json();
      setAnalyticsData(data);
    } catch (err) {
      setError(err.message);
      console.error('Error fetching analytics:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="quick-analytics-container">
        <div className="loading">Loading dataset analytics...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="quick-analytics-container">
        <div className="error">
          <h3>⚠️ Error</h3>
          <p>{error}</p>
          <button onClick={fetchAnalytics} className="retry-btn">Retry</button>
        </div>
      </div>
    );
  }

  if (!analyticsData) {
    return (
      <div className="quick-analytics-container">
        <div className="empty-state">No analytics data available. Run dataset analysis first.</div>
      </div>
    );
  }

  // Prepare data for visualizations
  const crackAnalysis = analyticsData.crack_analysis || {};
  const vegetationAnalysis = analyticsData.vegetation_analysis || {};
  const tests = analyticsData.statistical_tests || [];
  const metadata = analyticsData.metadata || {};

  // Convert distribution dicts to arrays for charts
  const splitDistribution = Object.entries(crackAnalysis.split_distribution || {}).map(([name, count]) => ({
    name: name.charAt(0).toUpperCase() + name.slice(1),
    value: count
  }));

  const crackSeverity = Object.entries(crackAnalysis.severity_distribution || {}).map(([name, count]) => ({
    name,
    value: count
  }));

  const vegetationType = Object.entries(vegetationAnalysis.type_distribution || {}).map(([name, count]) => ({
    name,
    value: count
  }));

  const colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8'];

  return (
    <div className="quick-analytics-container">
      {/* Header */}
      <div className="analytics-header">
        <h1>📊 Quick Analytics Dashboard</h1>
        <p className="metadata">
          Generated: {new Date(metadata.generated_at).toLocaleDateString()} |
          Total Images: {metadata.total_images} |
          Cracks: {metadata.total_crack_images} |
          Vegetation: {metadata.total_vegetation_images}
        </p>
      </div>

      {/* Summary Cards */}
      <div className="summary-cards">
        <div className="card">
          <h3>🖼️ Total Images</h3>
          <p className="big-number">{metadata.total_images}</p>
        </div>
        <div className="card">
          <h3>🔴 Crack Images</h3>
          <p className="big-number">{metadata.total_crack_images}</p>
        </div>
        <div className="card">
          <h3>🌿 Vegetation Images</h3>
          <p className="big-number">{metadata.total_vegetation_images}</p>
        </div>
        <div className="card">
          <h3>📈 Tests Run</h3>
          <p className="big-number">{tests.length}</p>
        </div>
      </div>

      {/* Charts Grid */}
      <div className="charts-grid">
        {/* Chart 1: Split Distribution */}
        {splitDistribution.length > 0 && (
          <div className="chart-card">
            <h3>Dataset Split Distribution</h3>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={splitDistribution}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ name, value }) => `${name}: ${value}`}
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {splitDistribution.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={colors[index % colors.length]} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </div>
        )}

        {/* Chart 2: Crack Severity */}
        {crackSeverity.length > 0 && (
          <div className="chart-card">
            <h3>Crack Severity Distribution</h3>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={crackSeverity}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="value" fill="#FF6B6B" name="Count" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        )}

        {/* Chart 3: Vegetation Type */}
        {vegetationType.length > 0 && (
          <div className="chart-card">
            <h3>Vegetation Type Distribution</h3>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={vegetationType}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="value" fill="#4ECDC4" name="Count" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        )}

        {/* Chart 4: Risk Score Histograms */}
        {crackAnalysis.histograms?.risk_score && (
          <div className="chart-card">
            <h3>Crack Risk Score Distribution</h3>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={formatHistogramData(crackAnalysis.histograms.risk_score)}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="range" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="count" fill="#FFA07A" name="Frequency" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        )}
      </div>

      {/* Statistical Tests */}
      <div className="tests-section">
        <h2>📋 Statistical Hypothesis Tests</h2>
        <div className="tests-grid">
          {tests.map((test, index) => (
            <div key={index} className={`test-card ${test.significant ? 'significant' : ''}`}>
              <h4>{test.test_name}</h4>
              <p className="description">{test.description}</p>
              <div className="test-results">
                <div className="result-row">
                  <span>P-Value:</span>
                  <strong>{test.p_value.toFixed(6)}</strong>
                </div>
                <div className="result-row">
                  <span>Significant (α=0.05):</span>
                  <strong className={test.significant ? 'significant' : 'not-significant'}>
                    {test.significant ? '✓ Yes' : '✗ No'}
                  </strong>
                </div>
                {test.r_squared !== undefined && (
                  <div className="result-row">
                    <span>R²:</span>
                    <strong>{test.r_squared.toFixed(4)}</strong>
                  </div>
                )}
                <div className="interpretation">{test.interpretation}</div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Top Risk Images */}
      {(crackAnalysis.top_risk_images || vegetationAnalysis.top_risk_images) && (
        <div className="risk-images-section">
          <h2>⚠️ Top Risk Images</h2>
          <div className="risk-images-grid">
            {crackAnalysis.top_risk_images && crackAnalysis.top_risk_images.length > 0 && (
              <div className="risk-category">
                <h3>High-Risk Cracks</h3>
                <table>
                  <thead>
                    <tr>
                      <th>Filename</th>
                      <th>Risk Score</th>
                    </tr>
                  </thead>
                  <tbody>
                    {crackAnalysis.top_risk_images.slice(0, 5).map((img, idx) => (
                      <tr key={idx}>
                        <td>{img.filename}</td>
                        <td>
                          <span className="risk-badge" style={{ width: `${img.risk_score * 100}%` }}>
                            {(img.risk_score * 100).toFixed(1)}%
                          </span>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}

            {vegetationAnalysis.top_risk_images && vegetationAnalysis.top_risk_images.length > 0 && (
              <div className="risk-category">
                <h3>High-Risk Vegetation</h3>
                <table>
                  <thead>
                    <tr>
                      <th>Filename</th>
                      <th>Risk Score</th>
                    </tr>
                  </thead>
                  <tbody>
                    {vegetationAnalysis.top_risk_images.slice(0, 5).map((img, idx) => (
                      <tr key={idx}>
                        <td>{img.filename}</td>
                        <td>
                          <span className="risk-badge" style={{ width: `${img.risk_score * 100}%` }}>
                            {(img.risk_score * 100).toFixed(1)}%
                          </span>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Refresh Button */}
      <div className="actions">
        <button onClick={fetchAnalytics} className="refresh-btn">
          🔄 Refresh Analytics
        </button>
      </div>
    </div>
  );
};

/**
 * Helper function to convert histogram data to chart format
 */
function formatHistogramData(histogram) {
  const { counts, edges } = histogram;
  return counts.map((count, i) => ({
    range: `${(edges[i] * 100).toFixed(0)}-${(edges[i + 1] * 100).toFixed(0)}%`,
    count
  }));
}

export default QuickAnalytics;
