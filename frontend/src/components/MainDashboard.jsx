import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Camera, Upload, Activity, BarChart3, Leaf, AlertTriangle, Download, Settings, Play, Video, Wifi, TrendingUp, Droplet, Wind, Zap, CheckCircle, XCircle, Loader } from 'lucide-react';
import ImageAnalysis from '../pages/ImageAnalysis';
import ImageInsights from '../pages/ImageInsights';

const MainDashboard = () => {
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState('image-analysis');
  const [lastAnalysis, setLastAnalysis] = useState(null);
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [loading, setLoading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);
  const [outputImages, setOutputImages] = useState(null);
  const fileInputRef = useRef(null);
  
  const [settings, setSettings] = useState({
    confidenceThreshold: 0.3,
    pixelToCmRatio: 0.1
  });

  const API_URL = 'http://localhost:5002';

  const handleTabChange = (tab) => {
    setActiveTab(tab);
    navigate(`/${tab}`);
  };

  return (
    <div className="dashboard-container">
      <div className="tab-navigation">
        <button onClick={() => handleTabChange('image-analysis')}>Image Analysis</button>
        <button onClick={() => handleTabChange('image-insights')}>Image Insights</button>
      </div>

      <div className="tab-content">
        {activeTab === 'image-analysis' && (
          <ImageAnalysis
            lastAnalysis={lastAnalysis}
            onAnalysisComplete={setLastAnalysis}
          />
        )}
        {activeTab === 'image-insights' && <ImageInsights lastAnalysis={lastAnalysis} />}
      </div>
    </div>
  );
};

export default MainDashboard;