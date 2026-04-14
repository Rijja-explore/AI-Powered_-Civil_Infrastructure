import React, { useState, useEffect } from 'react';
import { Camera, Video, Activity, BarChart3, Leaf, Shield, Zap, Eye, Wifi, WifiOff, Clock, AlertTriangle, Box } from 'lucide-react';
import './styles/main.css';
import './styles/mobile-responsive.css';

// Import pages
import ImageAnalysis from './pages/ImageAnalysis';
import RealTimeMonitoring from './pages/RealTimeMonitoring';
import Heightmap3D from './pages/Heightmap3D';
import { AnalysisProvider } from './contexts/AnalysisContext';
  

function App() {
  const [activeTab, setActiveTab] = useState('image-analysis');
  const [systemStatus, setSystemStatus] = useState({
    backendConnected: false,
    lastAnalysis: null,
    activeStreams: 0,
    alertsCount: 0
  });

  // Status updates removed - footer only shows copyright

  const routes = [
    { id: 'image-analysis', label: 'Image Analysis', Icon: Camera, Component: ImageAnalysis, description: 'AI-powered crack detection & material analysis' },
    { id: '3d-heightmap', label: '3D Heightmap', Icon: Box, Component: Heightmap3D, description: 'Convert 2D images to 3D heightmaps' }
  ];

  const features = [
    { icon: Shield, title: 'AI-Powered Analysis', desc: 'Advanced ML models for infrastructure assessment' },
    { icon: Eye, title: 'Real-time Monitoring', desc: 'Continuous surveillance & instant alerts' },
    { icon: Zap, title: 'Instant Insights', desc: 'Rapid assessment & actionable reports' }
  ];

  return (
    <AnalysisProvider>
      <div className="app-container">
      {/* Hero Section */}
      <section className="hero-section">
        <div className="hero-overlay"></div>
        
        {/* Uploaded Logos - Corner Layout */}
        <div style={{ position: 'absolute', top: '20px', right: '20px', display: 'flex', gap: '1rem', zIndex: '20' }}>
          <div style={{ width: '80px', height: '80px', background: 'rgba(255,255,255,0.1)', borderRadius: '12px', border: '2px solid rgba(255,255,255,0.3)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
            <img src="./sdg9.png" alt="SDG 9" style={{ width: '70px', height: '70px', borderRadius: '8px', objectFit: 'contain' }} />
          </div>
          <div style={{ width: '80px', height: '80px', background: 'rgba(255,255,255,0.1)', borderRadius: '12px', border: '2px solid rgba(255,255,255,0.3)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
            <img src="./sdg.png" alt="SDG" style={{ width: '70px', height: '70px', borderRadius: '8px', objectFit: 'contain' }} />
          </div>
          <div style={{ width: '80px', height: '80px', background: 'rgba(255,255,255,0.1)', borderRadius: '12px', border: '2px solid rgba(255,255,255,0.3)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
            <img src="./sdg11.png" alt="SDG 11" style={{ width: '70px', height: '70px', borderRadius: '8px', objectFit: 'contain' }} />
          </div>
        </div>

        <div className="hero-content">
          <div className="hero-text">
            <h1 className="hero-title">
              InfraVision AI
            </h1>
            <p className="hero-subtitle">
              Intelligent Structural Health Monitoring & Advanced Infrastructure Analysis
            </p>
            <div className="hero-features">
              {features.map((feature, index) => (
                <div key={index} className="hero-feature">
                  <feature.icon className="feature-icon" size={24} />
                  <div>
                    <h3>{feature.title}</h3>
                    <p>{feature.desc}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
          <div className="hero-visual">
            <div className="floating-elements">
              <div className="floating-card card-1">
                <Camera size={40} />
                <span>Analysis</span>
              </div>
              <div className="floating-card card-2">
                <Activity size={40} />
                <span>Monitoring</span>
              </div>
              <div className="floating-card card-3">
                <BarChart3 size={40} />
                <span>Insights</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Main Dashboard */}
      <div className="dashboard-container">
        {/* Navigation */}
        <nav className="nav-tabs-container">
          <div className="nav-tabs">
            {routes.map(({ id, label, Icon, description }) => (
              <button
                key={id}
                className={`nav-tab ${activeTab === id ? 'active' : ''}`}
                onClick={() => setActiveTab(id)}
                title={description}
              >
                <Icon size={20} />
                <span className="nav-label">{label}</span>
                <span className="nav-desc">{description}</span>
              </button>
            ))}
          </div>
        </nav>

        {/* Main Content */}
        <main className="main-content-frame">
          <div className="content-frame">
            {routes.map(({ id, Component }) =>
              activeTab === id && <Component key={id} />
            )}
          </div>
        </main>
      </div>

      {/* Footer */}
      <footer className="app-footer">
        <div className="footer-bottom">
          <div className="sdg-badges">
            <div className="sdg-badge" title="SDG 9: Industry, Innovation & Infrastructure">
              <svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
                <rect width="100" height="100" fill="#DD1C3D"/>
                <text x="50" y="50" textAnchor="middle" dy=".3em" fontSize="24" fontWeight="bold" fill="white">9</text>
              </svg>
              <span>SDG 9</span>
            </div>
            <div className="sdg-badge" title="SDG 11: Sustainable Cities & Communities">
              <svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
                <rect width="100" height="100" fill="#FCC30B"/>
                <text x="50" y="50" textAnchor="middle" dy=".3em" fontSize="24" fontWeight="bold" fill="#333">11</text>
              </svg>
              <span>SDG 11</span>
            </div>
            <div className="sdg-badge" title="SDG 13: Climate Action">
              <svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
                <rect width="100" height="100" fill="#407D52"/>
                <text x="50" y="50" textAnchor="middle" dy=".3em" fontSize="24" fontWeight="bold" fill="white">13</text>
              </svg>
              <span>SDG 13</span>
            </div>
          </div>
          <p>&copy; 2026 Rijja H and Rohith Varshighan S</p>
        </div>
      </footer>
    </div>
    </AnalysisProvider>
  );
}

export default App;
