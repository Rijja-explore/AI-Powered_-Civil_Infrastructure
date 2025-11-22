"""
Statistics Module
Runs hypothesis tests and builds analytical dataframes
"""

import numpy as np
import pandas as pd
from scipy import stats
from typing import Dict, List, Tuple, Any


def build_dataframes(
    crack_data: Dict,
    vegetation_data: Dict,
    crack_features_list: List[Dict],
    vegetation_features_list: List[Dict],
    crack_risk_scores: List[float],
    vegetation_risk_scores: List[float]
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Build pandas DataFrames from extracted features.
    
    Args:
        crack_data: Dictionary with crack image metadata
        vegetation_data: Dictionary with vegetation image metadata
        crack_features_list: List of crack feature dictionaries
        vegetation_features_list: List of vegetation feature dictionaries
        crack_risk_scores: List of crack risk scores
        vegetation_risk_scores: List of vegetation risk scores
    
    Returns:
        Tuple of (df_crack, df_vegetation)
    """
    # Build crack DataFrame
    crack_rows = []
    for i, features in enumerate(crack_features_list):
        row = {
            'filename': crack_data['filenames'][i],
            'split': crack_data['split'][i],
            'severity': crack_data['severity'][i],
            'risk_score': crack_risk_scores[i]
        }
        row.update(features)
        crack_rows.append(row)
    
    df_crack = pd.DataFrame(crack_rows)
    
    # Build vegetation DataFrame
    vegetation_rows = []
    for i, features in enumerate(vegetation_features_list):
        row = {
            'filename': vegetation_data['filenames'][i],
            'split': vegetation_data['split'][i],
            'type': vegetation_data['type'][i],
            'risk_score': vegetation_risk_scores[i]
        }
        row.update(features)
        vegetation_rows.append(row)
    
    df_vegetation = pd.DataFrame(vegetation_rows)
    
    return df_crack, df_vegetation


def run_statistical_tests(
    df_crack: pd.DataFrame,
    df_vegetation: pd.DataFrame
) -> List[Dict[str, Any]]:
    """
    Run 6 statistical hypothesis tests on the datasets.
    
    Returns:
        List of test result dictionaries with p-values and interpretations
    """
    tests = []
    
    # Test 1: Mann-Whitney U Test (Cracks by severity)
    if 'severity' in df_crack.columns and len(df_crack['severity'].unique()) > 1:
        try:
            severity_groups = df_crack['severity'].unique()
            if len(severity_groups) >= 2:
                group1 = df_crack[df_crack['severity'] == severity_groups[0]]['crack_pixel_ratio'].values
                group2 = df_crack[df_crack['severity'] == severity_groups[1]]['crack_pixel_ratio'].values
                
                stat, p_value = stats.mannwhitneyu(group1, group2)
                tests.append({
                    'test_name': 'Mann-Whitney U Test',
                    'description': 'Comparing crack density between severity groups',
                    'p_value': float(p_value),
                    'significant': p_value < 0.05,
                    'statistic': float(stat),
                    'interpretation': 'Crack density significantly differs between groups' if p_value < 0.05 else 'No significant difference in crack density'
                })
        except Exception as e:
            print(f"Error in Mann-Whitney U test: {e}")
    
    # Test 2: One-way ANOVA (Cracks across splits)
    if 'split' in df_crack.columns:
        try:
            split_groups = []
            for split in df_crack['split'].unique():
                split_groups.append(df_crack[df_crack['split'] == split]['crack_pixel_ratio'].values)
            
            f_stat, p_value = stats.f_oneway(*split_groups)
            tests.append({
                'test_name': 'One-way ANOVA',
                'description': 'Comparing crack pixel ratio across train/test/valid splits',
                'p_value': float(p_value),
                'significant': p_value < 0.05,
                'statistic': float(f_stat),
                'interpretation': 'Significant difference in cracks across splits' if p_value < 0.05 else 'No significant difference across splits'
            })
        except Exception as e:
            print(f"Error in one-way ANOVA: {e}")
    
    # Test 3: Linear Regression (Crack features → risk score)
    if len(df_crack) > 10:
        try:
            from sklearn.linear_model import LinearRegression
            from sklearn.metrics import r2_score
            
            feature_cols = [col for col in df_crack.columns if col not in ['filename', 'split', 'severity', 'risk_score']]
            X = df_crack[feature_cols].values
            y = df_crack['risk_score'].values
            
            model = LinearRegression()
            model.fit(X, y)
            y_pred = model.predict(X)
            r2 = r2_score(y, y_pred)
            
            # Compute p-value for model significance
            n = len(X)
            k = X.shape[1]
            f_stat = (r2 / k) / ((1 - r2) / (n - k - 1))
            p_value = 1 - stats.f.cdf(f_stat, k, n - k - 1)
            
            tests.append({
                'test_name': 'Linear Regression (Crack Features)',
                'description': 'Predicting crack risk score from image features',
                'p_value': float(p_value),
                'significant': p_value < 0.05,
                'r_squared': float(r2),
                'interpretation': f'Features explain {r2*100:.1f}% of crack risk variance'
            })
        except Exception as e:
            print(f"Error in linear regression: {e}")
    
    # Test 4: ANOVA (Vegetation by type)
    if 'type' in df_vegetation.columns and len(df_vegetation['type'].unique()) > 1:
        try:
            type_groups = []
            for veg_type in df_vegetation['type'].unique():
                type_groups.append(df_vegetation[df_vegetation['type'] == veg_type]['vegetation_coverage'].values)
            
            f_stat, p_value = stats.f_oneway(*type_groups)
            tests.append({
                'test_name': 'ANOVA (Vegetation Types)',
                'description': 'Comparing vegetation coverage across different types',
                'p_value': float(p_value),
                'significant': p_value < 0.05,
                'statistic': float(f_stat),
                'interpretation': 'Vegetation types differ in coverage' if p_value < 0.05 else 'No significant difference in coverage across types'
            })
        except Exception as e:
            print(f"Error in vegetation ANOVA: {e}")
    
    # Test 5: Linear Regression (Vegetation features → risk score)
    if len(df_vegetation) > 10:
        try:
            from sklearn.linear_model import LinearRegression
            from sklearn.metrics import r2_score
            
            feature_cols = [col for col in df_vegetation.columns if col not in ['filename', 'split', 'type', 'risk_score', 'coverage']]
            X = df_vegetation[feature_cols].values
            y = df_vegetation['risk_score'].values
            
            model = LinearRegression()
            model.fit(X, y)
            y_pred = model.predict(X)
            r2 = r2_score(y, y_pred)
            
            # Compute p-value
            n = len(X)
            k = X.shape[1]
            f_stat = (r2 / k) / ((1 - r2) / (n - k - 1))
            p_value = 1 - stats.f.cdf(f_stat, k, n - k - 1)
            
            tests.append({
                'test_name': 'Linear Regression (Vegetation Features)',
                'description': 'Predicting vegetation risk score from image features',
                'p_value': float(p_value),
                'significant': p_value < 0.05,
                'r_squared': float(r2),
                'interpretation': f'Features explain {r2*100:.1f}% of vegetation risk variance'
            })
        except Exception as e:
            print(f"Error in vegetation regression: {e}")
    
    # Test 6: Chi-Square (Crack severity vs Risk level)
    if 'severity' in df_crack.columns:
        try:
            df_crack['risk_level'] = pd.cut(df_crack['risk_score'], bins=[0, 0.33, 0.66, 1.0], labels=['Low', 'Medium', 'High'])
            contingency_table = pd.crosstab(df_crack['severity'], df_crack['risk_level'])
            chi2, p_value, dof, expected = stats.chi2_contingency(contingency_table)
            
            tests.append({
                'test_name': 'Chi-Square Test',
                'description': 'Association between crack severity and risk level',
                'p_value': float(p_value),
                'significant': p_value < 0.05,
                'statistic': float(chi2),
                'interpretation': 'Severity and risk level are associated' if p_value < 0.05 else 'No association between severity and risk'
            })
        except Exception as e:
            print(f"Error in chi-square test: {e}")
    
    return tests


def compute_dataset_statistics(df: pd.DataFrame, prefix: str = '') -> Dict[str, Dict[str, float]]:
    """
    Compute basic statistics for numerical columns.
    
    Args:
        df: DataFrame
        prefix: Prefix for statistic names (e.g., 'crack_')
    
    Returns:
        Dictionary of statistics
    """
    stats_dict = {}
    
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        stats_dict[f'{prefix}{col}'] = {
            'mean': float(df[col].mean()),
            'median': float(df[col].median()),
            'std': float(df[col].std()),
            'min': float(df[col].min()),
            'max': float(df[col].max()),
            'q25': float(df[col].quantile(0.25)),
            'q75': float(df[col].quantile(0.75))
        }
    
    return stats_dict


def get_top_risk_images(
    df: pd.DataFrame,
    n: int = 10
) -> List[Dict[str, Any]]:
    """
    Get top N highest risk images.
    
    Args:
        df: DataFrame with risk_score column
        n: Number of top images to return
    
    Returns:
        List of dictionaries with image info
    """
    top_images = df.nlargest(n, 'risk_score')[['filename', 'risk_score']].to_dict('records')
    return top_images


def get_distribution_histogram(
    series: pd.Series,
    bins: int = 20
) -> Dict[str, Any]:
    """
    Create histogram data for a series.
    
    Args:
        series: Pandas series
        bins: Number of bins
    
    Returns:
        Dictionary with bin edges and values
    """
    counts, edges = np.histogram(series.values, bins=bins)
    return {
        'bins': bins,
        'counts': counts.tolist(),
        'edges': edges.tolist()
    }
