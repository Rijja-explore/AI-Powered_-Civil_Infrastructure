#!/usr/bin/env python3
"""Test if models are loaded and working correctly"""

from finalwebapp_api import detect_with_yolo, YOLO_MODEL
import numpy as np

print("="*50)
print("Testing Model Loading and Detection")
print("="*50)

# Check if model is loaded
print(f"\n1. YOLO_MODEL loaded: {YOLO_MODEL is not None}")
if YOLO_MODEL:
    print(f"   Model type: {type(YOLO_MODEL)}")
    print(f"   Model class names: {list(YOLO_MODEL.names.values())}")
    
    # Create a test image
    print("\n2. Creating test image...")
    test_image = np.ones((640, 480, 3), dtype=np.uint8) * 128
    print(f"   Test image shape: {test_image.shape}")
    
    # Test detection
    print("\n3. Running detection...")
    try:
        annotated, cracks = detect_with_yolo(test_image, px_to_cm_ratio=0.1, model=YOLO_MODEL)
        print(f"   ✓ Detection completed!")
        print(f"   Number of detections: {len(cracks)}")
        if cracks and len(cracks) > 0:
            for i, crack in enumerate(cracks):
                print(f"\n   Detection {i+1}:")
                print(f"     Label: {crack.get('label', 'unknown')}")
                print(f"     Confidence: {crack.get('confidence', 'N/A')}")
                print(f"     Width: {crack.get('width_cm', 'N/A')}cm")
                print(f"     Length: {crack.get('length_cm', 'N/A')}cm")
    except Exception as e:
        print(f"   ✗ Detection failed: {e}")
        import traceback
        traceback.print_exc()
else:
    print("   ✗ YOLO_MODEL is None!")

print("\n" + "="*50)
