"""
Analytics Pipeline Package
Complete end-to-end pipeline for infrastructure health monitoring analytics.

Modules:
- data_loading: Load and preprocess images from datasets
- feature_extraction: Extract features (cracks, vegetation, etc.)
- statistics: Run hypothesis tests and generate insights
- export_json: Export analytics to JSON for React consumption
"""

__version__ = "1.0.0"
__author__ = "AI Pipeline"

from .data_loading import load_images_from_dataset, preprocess_image
from .feature_extraction import extract_crack_features, extract_vegetation_features, compute_risk_score
from .statistics import run_statistical_tests, build_dataframes
from .export_json import export_dataset_analytics, export_image_insights

__all__ = [
    "load_images_from_dataset",
    "preprocess_image",
    "extract_crack_features",
    "extract_vegetation_features",
    "compute_risk_score",
    "run_statistical_tests",
    "build_dataframes",
    "export_dataset_analytics",
    "export_image_insights",
]
