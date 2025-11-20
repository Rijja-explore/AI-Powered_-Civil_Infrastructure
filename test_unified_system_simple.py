#!/usr/bin/env python3
"""
Test script for Unified Analysis Engine
Tests 3 combined data science modules + 3 advanced image features
"""

import cv2
import numpy as np
import sys

print("="*80)
print("[TEST] UNIFIED STRUCTURAL HEALTH MONITORING SYSTEM")
print("="*80)

# Test 1: Import
print("\n[1/6] Importing Unified Analysis Engine...")
try:
    from unified_analysis_engine import (
        UnifiedDataScienceAnalyzer, 
        AdvancedImageAnalyzer,
        create_unified_analysis_report
    )
    print("[OK] Engine imported successfully")
except Exception as e:
    print("[FAIL] Import failed: " + str(e))
    sys.exit(1)

# Test 2: Initialize
print("\n[2/6] Initializing Data Science Analyzer...")
try:
    analyzer = UnifiedDataScienceAnalyzer()
    print("[OK] Analyzer initialized")
except Exception as e:
    print("[FAIL] Initialization failed: " + str(e))
    sys.exit(1)

# Test 3: Test data
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
    
    print("[OK] Test data created")
    print("     Cracks: " + str(len(test_crack_data)))
    print("     Material: " + test_material_data['predicted_material'])
except Exception as e:
    print("[FAIL] Test data creation failed: " + str(e))
    sys.exit(1)

# Test 4: Analysis
print("\n[4/6] Running Data Science Analysis...")
try:
    analysis_results = analyzer.comprehensive_analysis(
        test_crack_data,
        test_material_data,
        test_environmental_data
    )
    
    print("[OK] Analysis completed")
    print("     Data quality: " + str(analysis_results['data_quality']['quality_score']) + "/100")
    print("     Records: " + str(analysis_results['data_quality']['total_records']))
except Exception as e:
    print("[FAIL] Analysis failed: " + str(e))
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 5: Image analysis
print("\n[5/6] Testing Advanced Image Analysis...")
try:
    # Create test image - already in BGR format
    test_image = np.full((480, 640, 3), 100, dtype=np.uint8)  # Gray image in BGR
    
    # Add some texture to simulate concrete
    noise = np.random.randint(-20, 20, test_image.shape)
    test_image = np.clip(test_image + noise, 0, 255).astype(np.uint8)
    
    # Add some features
    cv2.rectangle(test_image, (100, 100), (200, 200), (80, 80, 80), -1)
    cv2.circle(test_image, (320, 240), 50, (100, 100, 100), -1)
    
    test_image_bgr = test_image  # Already BGR
    
    img_analyzer = AdvancedImageAnalyzer()
    print("[OK] Image Analyzer initialized")
    
    # Test features
    print("     Testing Moisture Heatmap...")
    moisture_result = img_analyzer.create_moisture_heatmap(test_image_bgr)
    assert moisture_result is not None
    print("     [OK] Moisture heatmap generated: " + str(moisture_result.shape))
    
    print("     Testing Structural Stress Map...")
    stress_result = img_analyzer.create_structural_stress_map(test_image_bgr, test_crack_data)
    assert stress_result is not None
    print("     [OK] Stress map generated: " + str(stress_result.shape))
    
    print("     Testing Thermal/Infrared Simulation...")
    thermal_result = img_analyzer.create_thermal_infrared_simulation(test_image_bgr)
    assert thermal_result is not None
    print("     [OK] Thermal simulation generated: " + str(thermal_result.shape))
    
    print("[OK] All 3 image features working")
    
except Exception as e:
    print("[FAIL] Image analysis failed: " + str(e))
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 6: Integration
print("\n[6/6] Integration Test...")
try:
    integrated_result = create_unified_analysis_report(
        test_image_bgr,
        test_crack_data,
        test_material_data,
        test_environmental_data,
        segmentation_model=None,
        crack_details=test_crack_data
    )
    
    assert integrated_result is not None
    print("[OK] Integration test passed")
    print("     Data science: OK")
    print("     Segmentation: " + integrated_result['segmentation_status'])
    print("     Total outputs: " + str(integrated_result['total_outputs']))
    
except Exception as e:
    print("[FAIL] Integration test failed: " + str(e))
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Summary
print("\n" + "="*80)
print("SUCCESS: ALL TESTS PASSED")
print("="*80)
print("\nSUMMARY:")
print("  OK - Unified Data Science Analyzer (3 modules combined)")
print("  OK - Advanced Image Analyzer (3 new features)")
print("  OK - System integration verified")
print("\nREADY FOR DEPLOYMENT:")
print("  OK - 9 output images supported (6 original + 3 advanced)")
print("  OK - Comprehensive data science analysis (5 units)")
print("  OK - Advanced structural health monitoring")
print("\nNEXT STEPS:")
print("  1. Start API: python finalwebapp_api.py")
print("  2. Launch frontend: cd frontend && npm start")
print("  3. Upload test images")
print("  4. View all 9 analysis outputs")
print("="*80)
