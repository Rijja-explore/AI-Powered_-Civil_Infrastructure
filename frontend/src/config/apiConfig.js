// API Configuration
// Use environment variable if available, otherwise default based on environment
const getApiUrl = () => {
  // Check for REACT_APP_API_URL environment variable
  if (process.env.REACT_APP_API_URL) {
    return process.env.REACT_APP_API_URL;
  }
  
  // For production builds (deployed on Vercel), use the backend URL from environment
  if (process.env.NODE_ENV === 'production') {
    // This should be set in Vercel environment variables
    return process.env.REACT_APP_API_URL || 'https://your-backend-url.com';
  }
  
  // Default for local development
  return 'http://localhost:7860';
};

export const API_URL = getApiUrl();

export default API_URL;
