import React, { createContext, useContext, useState } from 'react';

const AnalysisContext = createContext();

export const useAnalysis = () => {
  const context = useContext(AnalysisContext);
  if (!context) {
    throw new Error('useAnalysis must be used within an AnalysisProvider');
  }
  return context;
};

export const AnalysisProvider = ({ children }) => {
  const [lastAnalysis, setLastAnalysis] = useState(null);
  const [outputImages, setOutputImages] = useState(null);

  const updateAnalysis = (analysisData, images) => {
    setLastAnalysis(analysisData);
    setOutputImages(images);
  };

  const clearAnalysis = () => {
    setLastAnalysis(null);
    setOutputImages(null);
  };

  return (
    <AnalysisContext.Provider value={{
      lastAnalysis,
      outputImages,
      updateAnalysis,
      clearAnalysis
    }}>
      {children}
    </AnalysisContext.Provider>
  );
};