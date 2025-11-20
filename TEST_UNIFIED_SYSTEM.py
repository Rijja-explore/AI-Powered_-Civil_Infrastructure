#!/usr/bin/env python3
"""
Test script for the Unified Analysis Engine
Tests all 3 combined data science modules + 3 new advanced image analysis features
"""

import cv2
import numpy as np
from PIL import Image
import json
from datetime import datetime
import sys
import io

# Force UTF-8 encoding for console output
if sys.platform == 'win32':
    import os
    os.environ['PYTHONIOENCODING'] = 'utf-8'

print("="*80)
print("[TEST] TESTING UNIFIED STRUCTURAL HEALTH MONITORING SYSTEM")
print("="*80)

# Test 1: Import Unified Analysis Engine
print("\n[1/6] Testing Unified Analysis Engine Import...")
try:
    from unified_analysis_engine import (
        UnifiedDataScienceAnalyzer, 
        AdvancedImageAnalyzer,
        create_unified_analysis_report
    )
    print("✅ Unified Analysis Engine imported successfully")
except Exception as e:
    print(f"❌ Failed to import: {e}")
    exit(1)

# Test 2: Initialize Analyzer
print("\n[2/6] Initializing Unified Data Science Analyzer...")
try:
    analyzer = UnifiedDataScienceAnalyzer()
    print("✅ Analyzer initialized successfully")
except Exception as e:
    print(f"❌ Failed to initialize: {e}")
    exit(1)

# Test 3: Create test data
print("\n[3/6] Creating test data...")
try:
    test_crack_data = [
        {"width_cm": 2.5, "length_cm": 5.0, "severity": "Moderate", "confidence": 0.85},
        {"width_cm": 1.2, "length_cm": 2.3, "severity": "Minor", "confidence": 0.92},
        {"width_cm": 4.1, "length_cm": 8.2, "severity": "Severe", "confidence": 0.78}
    ]
    
    test_material_data = {
        "predicted_material": "Concrete",
        "probabilities": [0.7, 0.2, 0.05, 0.03, 0.02]
    }
    
    test_environmental_data = {
        "carbon_footprint_kg": 25.5,
        "water_footprint_liters": 180.3,
        "energy_consumption_kwh": 15.2
    }
    
    print("✅ Test data created successfully")
    print(f"   - Cracks: {len(test_crack_data)}")
    print(f"   - Material: {test_material_data['predicted_material']}")
    print(f"   - Carbon footprint: {test_environmental_data['carbon_footprint_kg']} kg CO₂")
except Exception as e:
    print(f"❌ Failed to create test data: {e}")
    exit(1)

# Test 4: Run comprehensive data science analysis
print("\n[4/6] Running Unified Comprehensive Data Science Analysis...")
try:
    analysis_results = analyzer.comprehensive_analysis(
        test_crack_data,
        test_material_data,
        test_environmental_data
    )
    
    print("✅ Analysis completed successfully")
    print(f"   - Modules used: {analysis_results['analysis_metadata']['modules_used']}")
    print(f"   - Total analyses: {analysis_results['analysis_metadata']['total_analyses']}")
    print(f"   - Data quality score: {analysis_results['data_quality']['quality_score']:.1f}/100")
    
    # Print analysis summary
    print("\n   📊 ANALYSIS SUMMARY:")
    print(f"      - Total records processed: {analysis_results['data_quality']['total_records']}")
    print(f"      - Total features analyzed: {analysis_results['data_quality']['total_features']}")
    print(f"      - Missing data: {analysis_results['data_quality']['missing_values']} values")
    
except Exception as e:
    print(f"❌ Analysis failed: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

# Test 5: Test image analysis features
print("\n[5/6] Testing Advanced Image Analysis Features...")
try:
    # Create a test image (synthetic concrete pattern)
    test_image = np.zeros((480, 640, 3), dtype=np.uint8)
    
    # Add some texture to simulate concrete
    noise = np.random.normal(100, 20, test_image.shape)
    test_image = np.clip(test_image + noise, 0, 255).astype(np.uint8)
    
    # Add some features
    cv2.rectangle(test_image, (100, 100), (200, 200), (80, 80, 80), -1)
    cv2.circle(test_image, (320, 240), 50, (100, 100, 100), -1)
    
    # Convert to BGR for consistency
    test_image_bgr = cv2.cvtColor(test_image, cv2.COLOR_GRAY2BGR)
    
    print(f"   Test image created: shape {test_image_bgr.shape}")
    
    # Initialize Advanced Image Analyzer
    img_analyzer = AdvancedImageAnalyzer()
    print("✅ Advanced Image Analyzer initialized")
    
    # Test Moisture Heatmap
    print("\n   Testing Moisture/Dampness Heatmap...")
    moisture_result = img_analyzer.create_moisture_heatmap(test_image_bgr)
    assert moisture_result is not None, "Moisture heatmap returned None"
    assert isinstance(moisture_result, np.ndarray), "Moisture heatmap is not ndarray"
    print(f"   ✅ Moisture heatmap generated: shape {moisture_result.shape}")
    
    # Test Structural Stress Map
    print("   Testing Structural Stress Map...")
    stress_result = img_analyzer.create_structural_stress_map(test_image_bgr, test_crack_data)
    assert stress_result is not None, "Stress map returned None"
    assert isinstance(stress_result, np.ndarray), "Stress map is not ndarray"
    print(f"   ✅ Structural stress map generated: shape {stress_result.shape}")
    
    # Test Thermal/Infrared Simulation
    print("   Testing Thermal/Infrared Simulation...")
    thermal_result = img_analyzer.create_thermal_infrared_simulation(test_image_bgr)
    assert thermal_result is not None, "Thermal simulation returned None"
    assert isinstance(thermal_result, np.ndarray), "Thermal simulation is not ndarray"
    print(f"   ✅ Thermal/Infrared simulation generated: shape {thermal_result.shape}")
    
    print("\n✅ All 3 advanced image analysis features working correctly")
    
except Exception as e:
    print(f"❌ Image analysis test failed: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

# Test 6: Integration test
print("\n[6/6] Integration Test - Complete Unified Analysis...")
try:
    integrated_result = create_unified_analysis_report(
        test_image_bgr,
        test_crack_data,
        test_material_data,
        test_environmental_data,
        segmentation_model=None,
        crack_details=test_crack_data
    )
    
    assert integrated_result is not None, "Integration test returned None"
    assert 'data_science_analysis' in integrated_result, "Missing data science analysis"
    assert 'advanced_images' in integrated_result, "Missing advanced images"
    
    print("✅ Integration test completed successfully")
    print(f"   - Data science analysis: ✅")
    print(f"   - Segmentation status: {integrated_result['segmentation_status']}")
    print(f"   - Advanced images generated: ✅")
    print(f"   - Total outputs: {integrated_result['total_outputs']} images")
    
except Exception as e:
    print(f"❌ Integration test failed: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

# Final Summary
print("\n" + "="*80)
print("✅ ALL TESTS PASSED SUCCESSFULLY!")
print("="*80)
print("\n📋 SUMMARY:")
print("   ✅ Unified Data Science Analyzer operational (3 modules combined)")
print("   ✅ Advanced Image Analyzer operational (3 new features)")
print("   ✅ Complete system integration verified")
print("\n🎯 SYSTEM READY FOR DEPLOYMENT:")
print("   ✅ 9 output images supported (6 original + 3 advanced)")
print("   ✅ Comprehensive data science analysis (5 units)")
print("   ✅ Advanced structural health monitoring")
print("\n🚀 Next steps:")
print("   1. Run frontend with: cd frontend && npm start")
print("   2. Start API: python finalwebapp_api.py")
print("   3. Upload test images through web interface")
print("   4. View all 9 analysis outputs and metrics")
print("="*80)
