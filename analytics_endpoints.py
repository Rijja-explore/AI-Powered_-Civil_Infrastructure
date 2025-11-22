"""
Backend Analytics Endpoints
Flask/FastAPI endpoints for analytics pipeline integration.
Add these to your finalwebapp_api.py or create a separate blueprint.
"""

import os
import json
import logging
from pathlib import Path
from datetime import datetime
from flask import Blueprint, jsonify, request, send_file
import numpy as np

# Import analytics pipeline
from analytics_pipeline.export_json import ImageInsightsAnalyzer

# Create blueprint
analytics_bp = Blueprint('analytics', __name__, url_prefix='/api/analytics')

# Configure logging
logger = logging.getLogger(__name__)

# Paths
DATASET_ANALYTICS_PATH = 'dataset_analytics.json'
LAST_ANALYSIS_PATH = 'last_analysis.json'


# ============================================================================
# ENDPOINT 1: GET /api/analytics/dataset
# Returns complete dataset-level analytics
# ============================================================================

@analytics_bp.route('/dataset', methods=['GET'])
def get_dataset_analytics():
    """
    Get complete dataset analytics.
    Used by Quick Analytics tab.
    
    Returns:
        {
            'metadata': {...},
            'crack_analysis': {...},
            'vegetation_analysis': {...},
            'statistical_tests': [...],
            'correlation_matrices': {...}
        }
    """
    try:
        if not os.path.exists(DATASET_ANALYTICS_PATH):
            return jsonify({
                'error': 'Dataset analytics not found',
                'message': 'Run run_dataset_analytics.py first'
            }), 404
        
        with open(DATASET_ANALYTICS_PATH, 'r') as f:
            data = json.load(f)
        
        logger.info('✅ Dataset analytics retrieved')
        return jsonify(data), 200
    
    except Exception as e:
        logger.error(f'❌ Error retrieving dataset analytics: {e}')
        return jsonify({'error': str(e)}), 500


# ============================================================================
# ENDPOINT 2: GET /api/analytics/last_image
# Returns insights for the last analyzed image
# ============================================================================

@analytics_bp.route('/last_image', methods=['GET'])
def get_last_image_insights():
    """
    Get insights for the last analyzed image.
    Used by Image Insights tab.
    
    Assumes last_analysis.json exists with image metrics.
    Uses ImageInsightsAnalyzer to compute detailed insights.
    
    Returns:
        {
            'summary': str,
            'health_score': int (0-100),
            'risk_level': str (Low/Medium/High),
            'radar_chart_data': {...},
            'overlap_analysis': {...},
            'contribution_breakdown': [...],
            'insights': [...]
        }
    """
    try:
        # Check if last analysis exists
        if not os.path.exists(LAST_ANALYSIS_PATH):
            return jsonify({
                'error': 'No image analyzed yet',
                'message': 'Analyze an image first'
            }), 404
        
        # Check if dataset analytics exists
        if not os.path.exists(DATASET_ANALYTICS_PATH):
            return jsonify({
                'error': 'Dataset analytics not found',
                'message': 'Run run_dataset_analytics.py first'
            }), 404
        
        # Load last analysis metrics
        with open(LAST_ANALYSIS_PATH, 'r') as f:
            last_analysis = json.load(f)
        
        # Create analyzer and analyze image
        analyzer = ImageInsightsAnalyzer(DATASET_ANALYTICS_PATH)
        insights = analyzer.analyze_image(last_analysis.get('metrics', {}))
        
        logger.info('✅ Image insights computed')
        return jsonify(insights), 200
    
    except Exception as e:
        logger.error(f'❌ Error computing image insights: {e}')
        return jsonify({'error': str(e)}), 500


# ============================================================================
# ENDPOINT 3: GET /api/analytics/statistical_tests
# Returns only the statistical test results
# ============================================================================

@analytics_bp.route('/statistical_tests', methods=['GET'])
def get_statistical_tests():
    """
    Get statistical test results.
    
    Returns:
        [
            {
                'test_name': str,
                'p_value': float,
                'significant': bool,
                'interpretation': str,
                ...
            }
        ]
    """
    try:
        if not os.path.exists(DATASET_ANALYTICS_PATH):
            return jsonify({'error': 'Dataset analytics not found'}), 404
        
        with open(DATASET_ANALYTICS_PATH, 'r') as f:
            data = json.load(f)
        
        tests = data.get('statistical_tests', [])
        logger.info(f'✅ Retrieved {len(tests)} statistical tests')
        return jsonify({'tests': tests}), 200
    
    except Exception as e:
        logger.error(f'❌ Error retrieving tests: {e}')
        return jsonify({'error': str(e)}), 500


# ============================================================================
# ENDPOINT 4: POST /api/analytics/rebuild
# Trigger analytics pipeline rebuild
# ============================================================================

@analytics_bp.route('/rebuild', methods=['POST'])
def rebuild_analytics():
    """
    Trigger analytics pipeline rebuild.
    Regenerates dataset_analytics.json from scratch.
    
    Optional POST data:
        {
            'crack_dir': 'Dataset/crack_preprocess',
            'vegetation_dir': 'Dataset/vegetation_preprocess'
        }
    
    Returns:
        {
            'status': 'success' | 'error',
            'message': str,
            'timestamp': datetime
        }
    """
    try:
        # Get paths from request or use defaults
        data = request.get_json() or {}
        crack_dir = data.get('crack_dir', 'Dataset/crack_preprocess')
        vegetation_dir = data.get('vegetation_dir', 'Dataset/vegetation_preprocess')
        
        logger.info(f'🔄 Starting analytics rebuild...')
        
        # Import and run pipeline
        from run_dataset_analytics import run_analytics_pipeline
        
        result_path = run_analytics_pipeline(
            crack_dir=crack_dir,
            vegetation_dir=vegetation_dir,
            output_file=DATASET_ANALYTICS_PATH
        )
        
        if result_path:
            logger.info('✅ Analytics rebuild completed')
            return jsonify({
                'status': 'success',
                'message': 'Analytics rebuilt successfully',
                'output_file': result_path,
                'timestamp': datetime.now().isoformat()
            }), 200
        else:
            return jsonify({
                'status': 'error',
                'message': 'Pipeline failed',
                'timestamp': datetime.now().isoformat()
            }), 500
    
    except Exception as e:
        logger.error(f'❌ Error rebuilding analytics: {e}')
        return jsonify({
            'status': 'error',
            'message': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500


# ============================================================================
# ENDPOINT 5: Modified /api/analyze
# Save metrics to last_analysis.json and return full structure
# ============================================================================

def save_image_analysis(metrics):
    """
    Helper function to save image analysis to disk.
    Call this in your /api/analyze endpoint after processing.
    
    Args:
        metrics: Dict with keys like:
            - crack_risk_score
            - vegetation_risk_score
            - moisture_intensity
            - stress_index
            - thermal_hotspot_score
            - material_durability
            - etc.
    """
    try:
        analysis_data = {
            'timestamp': datetime.now().isoformat(),
            'metrics': metrics
        }
        
        with open(LAST_ANALYSIS_PATH, 'w') as f:
            json.dump(analysis_data, f, indent=2)
        
        logger.info('✅ Image analysis saved to last_analysis.json')
        return True
    except Exception as e:
        logger.error(f'❌ Error saving image analysis: {e}')
        return False


# ============================================================================
# CODE TO ADD TO YOUR /api/analyze ENDPOINT
# ============================================================================

"""
# Add this to your existing /api/analyze endpoint in finalwebapp_api.py:

from analytics_endpoints import save_image_analysis

@app.route('/api/analyze', methods=['POST'])
def analyze_image():
    # ... your existing code to process the image ...
    
    # After computing all the outputs and metrics:
    image_metrics = {
        'crack_risk_score': float(crack_risk_score),
        'vegetation_risk_score': float(vegetation_risk_score),
        'moisture_intensity': float(moisture_intensity),
        'stress_index': float(stress_index),
        'thermal_hotspot_score': float(thermal_score),
        'material_durability': float(material_score),
        # Add other metrics as needed
    }
    
    # Save for /api/analytics/last_image endpoint
    save_image_analysis(image_metrics)
    
    # Return results
    return jsonify({
        'images': [
            'url_to_original',
            'url_to_cracks',
            'url_to_vegetation',
            'url_to_segmentation',
            'url_to_depth_map',
            'url_to_edges',
            'url_to_moisture',
            'url_to_stress',
            'url_to_thermal'
        ],
        'metrics': image_metrics
    })
"""


# ============================================================================
# REGISTRATION CODE FOR MAIN APP
# ============================================================================

"""
# Add this to your Flask app initialization in finalwebapp_api.py:

from analytics_endpoints import analytics_bp

app.register_blueprint(analytics_bp)
"""


# ============================================================================
# QUICK REFERENCE: JSON SCHEMAS
# ============================================================================

DATASET_ANALYTICS_SCHEMA = {
    'metadata': {
        'generated_at': 'ISO datetime string',
        'total_crack_images': 'int',
        'total_vegetation_images': 'int',
        'total_images': 'int'
    },
    'crack_analysis': {
        'image_count': 'int',
        'split_distribution': {'train': int, 'test': int, 'valid': int},
        'severity_distribution': {'None': int, 'Mild': int, 'Moderate': int, 'Severe': int},
        'metrics': {
            'crack_crack_pixel_ratio': {'mean': float, 'std': float, 'min': float, 'max': float},
            # ... other features
        },
        'histograms': {
            'crack_pixel_ratio': {'bins': 20, 'counts': list, 'edges': list},
            'risk_score': {'bins': 20, 'counts': list, 'edges': list}
        },
        'top_risk_images': [
            {'filename': str, 'risk_score': float}
        ]
    },
    'vegetation_analysis': {
        # ... similar structure
    },
    'statistical_tests': [
        {
            'test_name': 'Mann-Whitney U Test',
            'p_value': float,
            'significant': bool,
            'interpretation': str
        }
    ],
    'correlation_matrices': {
        'crack': [[float]],  # 2D array
        'vegetation': [[float]]
    }
}

IMAGE_INSIGHTS_SCHEMA = {
    'summary': 'str',
    'health_score': 'int (0-100)',
    'risk_level': 'str (Low/Medium/High)',
    'radar_chart_data': {
        'metrics': [
            {
                'metric': 'str',
                'current': 'float',
                'dataset_mean': 'float',
                'dataset_std': 'float'
            }
        ]
    },
    'overlap_analysis': {
        'cracks_in_damp_areas': 'float',
        'cracks_in_stress_zones': 'float',
        'vegetation_in_damp_areas': 'float',
        'vegetation_in_stress_zones': 'float'
    },
    'contribution_breakdown': [
        {
            'feature': 'str',
            'contribution_to_risk': 'float',
            'weight': 'float'
        }
    ],
    'insights': [
        {
            'type': 'warning|info|ok',
            'message': 'str'
        }
    ]
}
