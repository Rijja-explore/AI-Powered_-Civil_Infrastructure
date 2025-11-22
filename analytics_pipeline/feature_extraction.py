"""
Feature Extraction Module (Pure NumPy implementation)
Extracts numerical features from images without cv2 or skimage.
"""

import numpy as np
from typing import Dict
from scipy import ndimage




def _simple_edge_detection(gray: np.ndarray) -> np.ndarray:
    """Simple Sobel edge detection using scipy.ndimage."""
    try:
        sx = ndimage.sobel(gray, axis=0)
        sy = ndimage.sobel(gray, axis=1)
        edges = np.hypot(sx, sy)
        edges = (edges / edges.max() * 255).astype(np.uint8) if edges.max() > 0 else edges
        return edges
    except Exception:
        return np.zeros_like(gray)


def _simple_morphological_skeleton(binary: np.ndarray) -> np.ndarray:
    """Simple binary thinning approximation using scipy.ndimage."""
    try:
        from scipy.ndimage import binary_erosion, binary_dilation
        skeleton = binary.copy().astype(bool)
        for _ in range(5):
            eroded = binary_erosion(skeleton)
            dilated = binary_dilation(eroded)
            skeleton = skeleton & ~dilated
        return skeleton.astype(np.uint8) * 255
    except Exception:
        return binary


def _glcm_entropy_simple(gray: np.ndarray) -> float:
    """Simple entropy computation as proxy for GLCM entropy."""
    try:
        hist, _ = np.histogram(gray, bins=256, range=(0, 256))
        hist = hist / hist.sum()
        entropy = -np.sum(hist * np.log(hist + 1e-10))
        return float(entropy)
    except Exception:
        return 0.0


def extract_crack_features(image: np.ndarray) -> Dict[str, float]:
    """
    Extract features from crack images using pure NumPy + SciPy.
    No cv2 or skimage dependency.
    
    Features:
    - crack_pixel_ratio: Ratio of dark pixels (cracks)
    - edge_density: Density of edges (Sobel)
    - skeleton_length_proxy: Proxy for total crack length
    - glcm_entropy: Texture entropy (histogram-based)
    - brightness: Mean pixel intensity
    - color_mean_r/g/b: Per-channel means
    - roughness: Pixel intensity standard deviation
    
    Args:
        image: Preprocessed image (H, W, 3) in range [0, 1]
    
    Returns:
        Dictionary of feature names to values
    """
    features = {}
    
    try:
        # Ensure image is in correct format
        if image.dtype != np.float32:
            image = image.astype(np.float32)
        
        # Convert to grayscale using luminance formula
        if len(image.shape) == 3 and image.shape[2] == 3:
            gray = 0.299 * image[:, :, 0] + 0.587 * image[:, :, 1] + 0.114 * image[:, :, 2]
        else:
            gray = image if len(image.shape) == 2 else image[:, :, 0]
        
        # Convert to uint8 for thresholding
        gray_uint8 = (gray * 255).astype(np.uint8)
        
        # 1. Crack pixel ratio (threshold-based)
        threshold = 127
        binary = (gray_uint8 < threshold).astype(np.uint8) * 255
        crack_pixels = np.sum(binary > 0)
        total_pixels = binary.size
        features['crack_pixel_ratio'] = float(crack_pixels / total_pixels)
        
        # 2. Edge density (Sobel edges)
        edges = _simple_edge_detection(gray_uint8)
        edge_pixels = np.sum(edges > 50)
        features['edge_density'] = float(edge_pixels / total_pixels)
        
        # 3. Skeleton length proxy
        skeleton = _simple_morphological_skeleton(binary)
        skeleton_pixels = np.sum(skeleton > 0)
        features['skeleton_length_proxy'] = float(skeleton_pixels / total_pixels)
        
        # 4. GLCM entropy (simplified)
        features['glcm_entropy'] = _glcm_entropy_simple(gray_uint8)
        
        # 5. Brightness
        features['brightness'] = float(np.mean(gray))
        
        # 6. Color means
        if len(image.shape) == 3 and image.shape[2] == 3:
            features['color_mean_r'] = float(np.mean(image[:, :, 0]))
            features['color_mean_g'] = float(np.mean(image[:, :, 1]))
            features['color_mean_b'] = float(np.mean(image[:, :, 2]))
        else:
            features['color_mean_r'] = float(np.mean(gray))
            features['color_mean_g'] = float(np.mean(gray))
            features['color_mean_b'] = float(np.mean(gray))
        
        # 7. Roughness
        features['roughness'] = float(np.std(gray_uint8) / 255.0)
        
        return features
    
    except Exception as e:
        print(f"Warning: Error extracting crack features: {e}")
        return {
            'crack_pixel_ratio': 0.0,
            'edge_density': 0.0,
            'skeleton_length_proxy': 0.0,
            'glcm_entropy': 0.0,
            'brightness': 0.0,
            'color_mean_r': 0.0,
            'color_mean_g': 0.0,
            'color_mean_b': 0.0,
            'roughness': 0.0
        }



def extract_vegetation_features(image: np.ndarray) -> Dict[str, float]:
    """
    Extract features from vegetation images using pure NumPy + SciPy.
    No cv2 or skimage dependency.
    
    Features:
    - vegetation_coverage: Percentage of green pixels
    - green_index_mean: Mean Excess Green (ExG) index
    - glcm_entropy: Texture entropy (histogram-based)
    - brightness: Mean pixel intensity
    - color_mean_r/g/b: Per-channel means
    - roughness: Pixel intensity standard deviation
    - saturation_mean: Mean color saturation (computed from RGB)
    
    Args:
        image: Preprocessed image (H, W, 3) in range [0, 1]
    
    Returns:
        Dictionary of feature names to values
    """
    features = {}
    
    try:
        # Ensure image is in correct format
        if image.dtype != np.float32:
            image = image.astype(np.float32)
        
        # Convert to grayscale
        if len(image.shape) == 3 and image.shape[2] == 3:
            gray = 0.299 * image[:, :, 0] + 0.587 * image[:, :, 1] + 0.114 * image[:, :, 2]
        else:
            gray = image if len(image.shape) == 2 else image[:, :, 0]
        
        gray_uint8 = (gray * 255).astype(np.uint8)
        
        # Extract RGB channels
        if len(image.shape) == 3 and image.shape[2] == 3:
            r = image[:, :, 0]
            g = image[:, :, 1]
            b = image[:, :, 2]
        else:
            r = g = b = gray
        
        # 1. Vegetation coverage using Excess Green index
        exg = 2 * g - r - b
        green_mask = exg > 0.1
        features['vegetation_coverage'] = float(np.sum(green_mask) / green_mask.size)
        
        # 2. Green index mean
        if np.sum(green_mask) > 0:
            features['green_index_mean'] = float(np.mean(exg[green_mask]))
        else:
            features['green_index_mean'] = 0.0
        
        # 3. GLCM entropy (simplified)
        features['glcm_entropy'] = _glcm_entropy_simple(gray_uint8)
        
        # 4. Brightness
        features['brightness'] = float(np.mean(gray))
        
        # 5. Color means
        features['color_mean_r'] = float(np.mean(r))
        features['color_mean_g'] = float(np.mean(g))
        features['color_mean_b'] = float(np.mean(b))
        
        # 6. Roughness
        features['roughness'] = float(np.std(gray_uint8) / 255.0)
        
        # 7. Saturation mean (computed from RGB)
        max_rgb = np.maximum(np.maximum(r, g), b)
        min_rgb = np.minimum(np.minimum(r, g), b)
        saturation = np.zeros_like(max_rgb)
        mask = max_rgb > 0
        saturation[mask] = (max_rgb[mask] - min_rgb[mask]) / max_rgb[mask]
        features['saturation_mean'] = float(np.mean(saturation))
        
        return features
    
    except Exception as e:
        print(f"Warning: Error extracting vegetation features: {e}")
        return {
            'vegetation_coverage': 0.0,
            'green_index_mean': 0.0,
            'glcm_entropy': 0.0,
            'brightness': 0.0,
            'color_mean_r': 0.0,
            'color_mean_g': 0.0,
            'color_mean_b': 0.0,
            'roughness': 0.0,
            'saturation_mean': 0.0
        }


def compute_risk_score(features: Dict[str, float], feature_type: str = 'crack') -> float:
    """
    Compute a composite risk score based on features.
    
    Args:
        features: Dictionary of features
        feature_type: 'crack' or 'vegetation'
    
    Returns:
        Risk score in range [0, 1]
    """
    risk_score = 0.0
    
    if feature_type == 'crack':
        # Weights for crack features
        risk_score += features.get('crack_pixel_ratio', 0) * 0.35
        risk_score += features.get('edge_density', 0) * 0.25
        risk_score += features.get('skeleton_length_proxy', 0) * 0.20
        risk_score += (1 - features.get('brightness', 1)) * 0.10  # Darker = riskier
        risk_score += features.get('roughness', 0) * 0.10
        
    elif feature_type == 'vegetation':
        # Weights for vegetation features
        risk_score += features.get('vegetation_coverage', 0) * 0.30
        risk_score += features.get('green_index_mean', 0) * 0.20
        risk_score += features.get('saturation_mean', 0) * 0.15
        risk_score += (1 - features.get('brightness', 1)) * 0.15  # Darker vegetation = risk
        risk_score += features.get('glcm_entropy', 0) * 0.20
    
    # Clip to [0, 1]
    return float(np.clip(risk_score, 0, 1))


def classify_feature_value(value: float, feature_name: str, dataset_mean: float, dataset_std: float) -> str:
    """
    Classify a feature value as Low/Medium/High based on z-score.
    
    Args:
        value: Feature value
        feature_name: Name of feature
        dataset_mean: Mean of feature in dataset
        dataset_std: Standard deviation in dataset
    
    Returns:
        Classification string
    """
    try:
        if dataset_std == 0 or np.isnan(dataset_std):
            return "Normal"
        
        z_score = (value - dataset_mean) / dataset_std
        
        if z_score < -0.5:
            return "Low"
        elif z_score > 0.5:
            return "High"
        else:
            return "Medium"
    except Exception:
        return "Normal"
