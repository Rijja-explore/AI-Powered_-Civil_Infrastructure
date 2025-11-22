"""
Export Module
Exports analytics results to JSON for React consumption
"""

import json
import numpy as np
import pandas as pd
from datetime import datetime
from typing import Dict, List, Any


class NumpyEncoder(json.JSONEncoder):
    """JSON encoder that handles NumPy types"""
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, (np.integer, np.floating)):
            return float(obj)
        elif isinstance(obj, np.bool_):
            return bool(obj)
        return super().default(obj)


def export_dataset_analytics(
    df_crack: pd.DataFrame,
    df_vegetation: pd.DataFrame,
    statistical_tests: List[Dict[str, Any]],
    crack_stats: Dict[str, Dict[str, float]],
    vegetation_stats: Dict[str, Dict[str, float]],
    output_path: str = 'dataset_analytics.json'
) -> str:
    """
    Export complete dataset analytics to JSON.
    
    Args:
        df_crack: Crack features DataFrame
        df_vegetation: Vegetation features DataFrame
        statistical_tests: List of test results
        crack_stats: Crack feature statistics
        vegetation_stats: Vegetation feature statistics
        output_path: Output JSON file path
    
    Returns:
        Path to created JSON file
    """
    from .statistics import get_top_risk_images, get_distribution_histogram
    
    analytics = {
        'metadata': {
            'generated_at': datetime.now().isoformat(),
            'total_crack_images': len(df_crack),
            'total_vegetation_images': len(df_vegetation),
            'total_images': len(df_crack) + len(df_vegetation)
        },
        'crack_analysis': {
            'image_count': len(df_crack),
            'split_distribution': df_crack['split'].value_counts().to_dict() if 'split' in df_crack.columns else {},
            'severity_distribution': df_crack['severity'].value_counts().to_dict() if 'severity' in df_crack.columns else {},
            'metrics': crack_stats,
            'histograms': {},
            'top_risk_images': get_top_risk_images(df_crack, n=10)
        },
        'vegetation_analysis': {
            'image_count': len(df_vegetation),
            'split_distribution': df_vegetation['split'].value_counts().to_dict() if 'split' in df_vegetation.columns else {},
            'type_distribution': df_vegetation['type'].value_counts().to_dict() if 'type' in df_vegetation.columns else {},
            'metrics': vegetation_stats,
            'histograms': {},
            'top_risk_images': get_top_risk_images(df_vegetation, n=10)
        },
        'statistical_tests': statistical_tests,
        'correlation_matrices': {}
    }
    
    # Add histograms for key features
    if 'crack_pixel_ratio' in df_crack.columns:
        analytics['crack_analysis']['histograms']['crack_pixel_ratio'] = get_distribution_histogram(
            df_crack['crack_pixel_ratio'], bins=20
        )
    
    if 'risk_score' in df_crack.columns:
        analytics['crack_analysis']['histograms']['risk_score'] = get_distribution_histogram(
            df_crack['risk_score'], bins=20
        )
    
    if 'vegetation_coverage' in df_vegetation.columns:
        analytics['vegetation_analysis']['histograms']['vegetation_coverage'] = get_distribution_histogram(
            df_vegetation['vegetation_coverage'], bins=20
        )
    
    if 'risk_score' in df_vegetation.columns:
        analytics['vegetation_analysis']['histograms']['risk_score'] = get_distribution_histogram(
            df_vegetation['risk_score'], bins=20
        )
    
    # Correlation matrices
    numeric_crack_cols = df_crack.select_dtypes(include=[np.number]).columns
    if len(numeric_crack_cols) > 1:
        corr_matrix = df_crack[numeric_crack_cols].corr()
        analytics['correlation_matrices']['crack'] = corr_matrix.values.tolist()
    
    numeric_veg_cols = df_vegetation.select_dtypes(include=[np.number]).columns
    if len(numeric_veg_cols) > 1:
        corr_matrix = df_vegetation[numeric_veg_cols].corr()
        analytics['correlation_matrices']['vegetation'] = corr_matrix.values.tolist()
    
    # Write to JSON
    with open(output_path, 'w') as f:
        json.dump(analytics, f, cls=NumpyEncoder, indent=2)
    
    print(f"✅ Dataset analytics exported to {output_path}")
    return output_path


def export_image_insights(
    image_metrics: Dict[str, Any],
    dataset_stats: Dict[str, Dict[str, float]],
    dataset_analytics: Dict[str, Any],
    output_path: str = 'image_insights.json'
) -> str:
    """
    Export per-image insights to JSON.
    
    Args:
        image_metrics: Metrics for current image
        dataset_stats: Dataset statistics
        dataset_analytics: Complete dataset analytics
        output_path: Output JSON file path
    
    Returns:
        Path to created JSON file
    """
    # Compute z-scores and percentiles
    statistical_comparison = {}
    for metric_name, metric_value in image_metrics.items():
        if metric_name in dataset_stats:
            dataset_info = dataset_stats[metric_name]
            mean = dataset_info.get('mean', 0)
            std = dataset_info.get('std', 1)
            
            z_score = (metric_value - mean) / std if std > 0 else 0
            percentile = 50  # Placeholder
            
            if std > 0:
                from scipy.stats import norm
                percentile = norm.cdf(z_score) * 100
            
            # Classify
            if z_score < -0.5:
                classification = 'Low'
            elif z_score > 0.5:
                classification = 'High'
            else:
                classification = 'Medium'
            
            statistical_comparison[metric_name] = {
                'value': float(metric_value),
                'mean': float(mean),
                'std': float(std),
                'z_score': float(z_score),
                'percentile': float(percentile),
                'classification': classification
            }
    
    # Compute health score (weighted combination)
    health_score = compute_health_score(image_metrics)
    risk_level = get_risk_level(health_score)
    
    # Generate insights
    insights = generate_insights(image_metrics, statistical_comparison, dataset_analytics)
    
    # Overlap analysis
    overlap_analysis = compute_overlap_analysis(image_metrics)
    
    # Contribution breakdown
    contribution = compute_contribution_breakdown(image_metrics)
    
    # Radar chart data
    radar_data = generate_radar_chart_data(image_metrics, dataset_stats)
    
    result = {
        'summary': generate_summary(health_score, risk_level, image_metrics),
        'health_score': int(health_score),
        'risk_level': risk_level,
        'radar_chart_data': radar_data,
        'overlap_analysis': overlap_analysis,
        'contribution_breakdown': contribution,
        'insights': insights,
        'statistical_comparison': statistical_comparison
    }
    
    with open(output_path, 'w') as f:
        json.dump(result, f, cls=NumpyEncoder, indent=2)
    
    print(f"✅ Image insights exported to {output_path}")
    return output_path


def compute_health_score(metrics: Dict[str, Any]) -> float:
    """
    Compute overall health score (0-100, higher is better).
    
    Args:
        metrics: Image metrics dictionary
    
    Returns:
        Health score 0-100
    """
    # Start at 100 and subtract risk factors
    health = 100.0
    
    # Penalize for cracks
    if 'crack_risk_score' in metrics:
        health -= metrics['crack_risk_score'] * 40
    
    # Penalize for vegetation
    if 'vegetation_risk_score' in metrics:
        health -= metrics['vegetation_risk_score'] * 30
    
    # Penalize for moisture
    if 'moisture_intensity' in metrics:
        health -= metrics['moisture_intensity'] * 20
    
    # Penalize for stress
    if 'stress_index' in metrics:
        health -= metrics['stress_index'] * 10
    
    return float(np.clip(health, 0, 100))


def get_risk_level(health_score: float) -> str:
    """Get risk level from health score."""
    if health_score >= 70:
        return 'Low'
    elif health_score >= 40:
        return 'Medium'
    else:
        return 'High'


def generate_insights(
    metrics: Dict[str, Any],
    statistical_comparison: Dict[str, Dict],
    dataset_analytics: Dict[str, Any]
) -> List[Dict[str, str]]:
    """
    Generate textual insights based on metrics.
    
    Args:
        metrics: Image metrics
        statistical_comparison: Z-scores and percentiles
        dataset_analytics: Dataset-level analytics
    
    Returns:
        List of insight dictionaries
    """
    insights = []
    
    # Crack insights
    if 'crack_risk_score' in metrics and metrics['crack_risk_score'] > 0.5:
        insights.append({
            'type': 'warning',
            'message': 'High crack density detected. Surface integrity at risk.'
        })
    
    # Vegetation insights
    if 'vegetation_risk_score' in metrics and metrics['vegetation_risk_score'] > 0.5:
        insights.append({
            'type': 'warning',
            'message': 'Significant biological growth. May trap moisture and accelerate degradation.'
        })
    
    # Moisture insights
    if 'moisture_intensity' in metrics and metrics['moisture_intensity'] > 0.6:
        insights.append({
            'type': 'warning',
            'message': 'High moisture detected. Increases risk of corrosion and material expansion.'
        })
    
    # Stress insights
    if 'stress_index' in metrics and metrics['stress_index'] > 0.5:
        insights.append({
            'type': 'warning',
            'message': 'High structural stress areas detected. Monitor for crack propagation.'
        })
    
    # Combined insights
    if 'crack_risk_score' in metrics and 'vegetation_risk_score' in metrics:
        if metrics['crack_risk_score'] > 0.4 and metrics['vegetation_risk_score'] > 0.4:
            insights.append({
                'type': 'warning',
                'message': 'Combined crack + vegetation issue. Prioritize for maintenance.'
            })
    
    # Positive insights
    if len(insights) == 0:
        insights.append({
            'type': 'ok',
            'message': 'Surface condition appears stable. Continue routine monitoring.'
        })
    
    # Percentile insights
    for metric_name, comp in statistical_comparison.items():
        if comp['percentile'] > 95:
            insights.append({
                'type': 'warning',
                'message': f'{metric_name} is in the top 5% of dataset. Higher than expected.'
            })
        elif comp['percentile'] < 5:
            insights.append({
                'type': 'info',
                'message': f'{metric_name} is exceptionally low. Better than 95% of dataset.'
            })
    
    return insights[:5]  # Limit to top 5 insights


def compute_overlap_analysis(metrics: Dict[str, Any]) -> Dict[str, float]:
    """
    Compute overlap between damage types.
    """
    overlap = {
        'cracks_in_damp_areas': 0.0,
        'cracks_in_stress_zones': 0.0,
        'vegetation_in_damp_areas': 0.0,
        'vegetation_in_stress_zones': 0.0
    }
    
    # Simulate overlap percentages
    if 'crack_risk_score' in metrics and 'moisture_intensity' in metrics:
        overlap['cracks_in_damp_areas'] = metrics['crack_risk_score'] * metrics['moisture_intensity'] * 100
    
    if 'crack_risk_score' in metrics and 'stress_index' in metrics:
        overlap['cracks_in_stress_zones'] = metrics['crack_risk_score'] * metrics['stress_index'] * 100
    
    if 'vegetation_risk_score' in metrics and 'moisture_intensity' in metrics:
        overlap['vegetation_in_damp_areas'] = metrics['vegetation_risk_score'] * metrics['moisture_intensity'] * 100
    
    if 'vegetation_risk_score' in metrics and 'stress_index' in metrics:
        overlap['vegetation_in_stress_zones'] = metrics['vegetation_risk_score'] * metrics['stress_index'] * 100
    
    return overlap


def compute_contribution_breakdown(metrics: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Compute contribution of each factor to health score.
    """
    total = 40 + 30 + 20 + 10  # Total weights
    
    breakdown = []
    
    if 'crack_risk_score' in metrics:
        breakdown.append({
            'feature': 'Cracks',
            'contribution_to_risk': float(metrics['crack_risk_score'] * 40),
            'weight': 40 / total
        })
    
    if 'vegetation_risk_score' in metrics:
        breakdown.append({
            'feature': 'Vegetation',
            'contribution_to_risk': float(metrics['vegetation_risk_score'] * 30),
            'weight': 30 / total
        })
    
    if 'moisture_intensity' in metrics:
        breakdown.append({
            'feature': 'Moisture',
            'contribution_to_risk': float(metrics['moisture_intensity'] * 20),
            'weight': 20 / total
        })
    
    if 'stress_index' in metrics:
        breakdown.append({
            'feature': 'Stress',
            'contribution_to_risk': float(metrics['stress_index'] * 10),
            'weight': 10 / total
        })
    
    return breakdown


def generate_radar_chart_data(
    image_metrics: Dict[str, Any],
    dataset_stats: Dict[str, Dict[str, float]]
) -> Dict[str, List[Dict]]:
    """
    Generate data for radar chart (image vs dataset).
    """
    metrics = []
    
    key_metrics = ['crack_risk_score', 'vegetation_risk_score', 'moisture_intensity', 'stress_index']
    
    for metric_name in key_metrics:
        if metric_name in image_metrics and metric_name in dataset_stats:
            current = image_metrics[metric_name]
            dataset_mean = dataset_stats[metric_name].get('mean', 0)
            dataset_std = dataset_stats[metric_name].get('std', 1)
            
            metrics.append({
                'metric': metric_name.replace('_', ' ').title(),
                'current': float(current),
                'dataset_mean': float(dataset_mean),
                'dataset_std': float(dataset_std)
            })
    
    return {'metrics': metrics}


def generate_summary(health_score: float, risk_level: str, metrics: Dict[str, Any]) -> str:
    """Generate a text summary."""
    summary = f"Health Score: {int(health_score)}/100 ({risk_level} Risk). "
    
    if health_score >= 70:
        summary += "Surface is in good condition. Continue routine monitoring."
    elif health_score >= 40:
        summary += "Surface shows moderate damage. Plan maintenance within 3-6 months."
    else:
        summary += "Surface requires urgent attention. Recommend immediate inspection and repair."
    
    return summary
