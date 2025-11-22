#!/usr/bin/env python3
"""
Headless Analytics Pipeline Runner
Runs dataset analytics without Jupyter UI.
Can be triggered on backend startup or via endpoint.
Regenerates dataset_analytics.json automatically.
"""

import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from analytics_pipeline import (
    load_images_from_dataset,
    extract_crack_features,
    extract_vegetation_features,
    compute_risk_score,
    build_dataframes,
    run_statistical_tests,
    export_dataset_analytics
)
from analytics_pipeline.statistics import compute_dataset_statistics


def run_analytics_pipeline(
    crack_dir: str = "Dataset/crack_preprocess",
    vegetation_dir: str = "Dataset/vegetation_preprocess",
    output_file: str = "dataset_analytics.json"
) -> str:
    """
    Run complete analytics pipeline headless.
    
    Args:
        crack_dir: Path to crack dataset
        vegetation_dir: Path to vegetation dataset
        output_file: Output JSON file path
    
    Returns:
        Path to generated JSON file
    """
    print("=" * 60)
    print("INFRASTRUCTURE HEALTH ANALYTICS PIPELINE")
    print("=" * 60)
    
    # Step 1: Load images
    print("\n[1/7] Loading dataset images...")
    try:
        crack_data, vegetation_data = load_images_from_dataset(
            crack_dir=crack_dir,
            vegetation_dir=vegetation_dir,
            target_size=(640, 640)
        )
        print(f"  ✅ Crack images: {len(crack_data['images'])}")
        print(f"  ✅ Vegetation images: {len(vegetation_data['images'])}")
    except Exception as e:
        print(f"  ❌ Error loading images: {e}")
        return None
    
    # Step 2: Extract crack features
    print("\n[2/7] Extracting crack features...")
    try:
        crack_features_list = []
        crack_risk_scores = []
        
        for i, img in enumerate(crack_data['images']):
            try:
                features = extract_crack_features(img)
                risk_score = compute_risk_score(features, feature_type='crack')
                crack_features_list.append(features)
                crack_risk_scores.append(risk_score)
            except Exception as e:
                print(f"  ⚠️  Error processing crack image {i}: {e}")
                # Add default features
                crack_features_list.append({
                    'crack_pixel_ratio': 0.0,
                    'edge_density': 0.0,
                    'skeleton_length_proxy': 0.0,
                    'glcm_entropy': 0.0,
                    'brightness': 0.0,
                    'color_mean_r': 0.0,
                    'color_mean_g': 0.0,
                    'color_mean_b': 0.0,
                    'roughness': 0.0
                })
                crack_risk_scores.append(0.0)
        
        print(f"  ✅ Extracted {len(crack_features_list)} feature sets")
    except Exception as e:
        print(f"  ❌ Error extracting crack features: {e}")
        return None
    
    # Step 3: Extract vegetation features
    print("\n[3/7] Extracting vegetation features...")
    try:
        vegetation_features_list = []
        vegetation_risk_scores = []
        
        for i, img in enumerate(vegetation_data['images']):
            try:
                features = extract_vegetation_features(img)
                risk_score = compute_risk_score(features, feature_type='vegetation')
                vegetation_features_list.append(features)
                vegetation_risk_scores.append(risk_score)
            except Exception as e:
                print(f"  ⚠️  Error processing vegetation image {i}: {e}")
                vegetation_features_list.append({
                    'vegetation_coverage': 0.0,
                    'green_index_mean': 0.0,
                    'glcm_entropy': 0.0,
                    'brightness': 0.0,
                    'color_mean_r': 0.0,
                    'color_mean_g': 0.0,
                    'color_mean_b': 0.0,
                    'roughness': 0.0,
                    'saturation_mean': 0.0
                })
                vegetation_risk_scores.append(0.0)
        
        print(f"  ✅ Extracted {len(vegetation_features_list)} feature sets")
    except Exception as e:
        print(f"  ❌ Error extracting vegetation features: {e}")
        return None
    
    # Step 4: Build DataFrames
    print("\n[4/7] Building analytical DataFrames...")
    try:
        df_crack, df_vegetation = build_dataframes(
            crack_data=crack_data,
            vegetation_data=vegetation_data,
            crack_features_list=crack_features_list,
            vegetation_features_list=vegetation_features_list,
            crack_risk_scores=crack_risk_scores,
            vegetation_risk_scores=vegetation_risk_scores
        )
        print(f"  ✅ Crack DataFrame: {df_crack.shape}")
        print(f"  ✅ Vegetation DataFrame: {df_vegetation.shape}")
    except Exception as e:
        print(f"  ❌ Error building DataFrames: {e}")
        return None
    
    # Step 5: Compute statistics
    print("\n[5/7] Computing dataset statistics...")
    try:
        crack_stats = compute_dataset_statistics(df_crack, prefix='crack_')
        vegetation_stats = compute_dataset_statistics(df_vegetation, prefix='vegetation_')
        print(f"  ✅ Computed statistics for {len(crack_stats) + len(vegetation_stats)} features")
    except Exception as e:
        print(f"  ❌ Error computing statistics: {e}")
        return None
    
    # Step 6: Run statistical tests
    print("\n[6/7] Running hypothesis tests...")
    try:
        statistical_tests = run_statistical_tests(df_crack, df_vegetation)
        print(f"  ✅ Completed {len(statistical_tests)} tests")
        for i, test in enumerate(statistical_tests, 1):
            sig = "✓" if test['significant'] else "✗"
            print(f"    {sig} {test['test_name']}: p={test['p_value']:.6f}")
    except Exception as e:
        print(f"  ❌ Error running tests: {e}")
        return None
    
    # Step 7: Export JSON
    print("\n[7/7] Exporting analytics JSON...")
    try:
        json_path = export_dataset_analytics(
            df_crack=df_crack,
            df_vegetation=df_vegetation,
            statistical_tests=statistical_tests,
            crack_stats=crack_stats,
            vegetation_stats=vegetation_stats,
            output_path=output_file
        )
        print(f"  ✅ Exported to {output_file}")
    except Exception as e:
        print(f"  ❌ Error exporting JSON: {e}")
        return None
    
    print("\n" + "=" * 60)
    print("✅ PIPELINE COMPLETED SUCCESSFULLY")
    print("=" * 60)
    print(f"\nDataset Statistics:")
    print(f"  Total crack images: {len(df_crack)}")
    print(f"  Total vegetation images: {len(df_vegetation)}")
    print(f"  Crack features: {len(crack_stats)}")
    print(f"  Vegetation features: {len(vegetation_stats)}")
    print(f"  Statistical tests: {len(statistical_tests)}")
    print(f"\n✅ Output: {output_file}")
    
    return json_path


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Run analytics pipeline headless")
    parser.add_argument("--crack-dir", default="Dataset/crack_preprocess", help="Crack dataset path")
    parser.add_argument("--vegetation-dir", default="Dataset/vegetation_preprocess", help="Vegetation dataset path")
    parser.add_argument("--output", default="dataset_analytics.json", help="Output JSON file")
    
    args = parser.parse_args()
    
    result = run_analytics_pipeline(
        crack_dir=args.crack_dir,
        vegetation_dir=args.vegetation_dir,
        output_file=args.output
    )
    
    sys.exit(0 if result else 1)
