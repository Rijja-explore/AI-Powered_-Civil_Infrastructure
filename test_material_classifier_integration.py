#!/usr/bin/env python3
"""
Test material classifier integration
Verifies that trained models load correctly in finalwebapp.py and finalwebapp_api.py
"""

import os
import sys
import numpy as np
from PIL import Image

print("=" * 70)
print("Material Classifier Integration Test")
print("=" * 70)

# Test 1: Check if trained models exist
print("\n[1/5] Checking trained models...")
models_dir = os.path.join(os.path.dirname(__file__), "materialclassification_model")
h5_path = os.path.join(models_dir, "material_classifier.h5")
tflite_path = os.path.join(models_dir, "material_classifier.tflite")

if os.path.exists(h5_path):
    size_mb = os.path.getsize(h5_path) / 1e6
    print(f"   ✅ .h5 model found ({size_mb:.1f}MB)")
else:
    print(f"   ❌ .h5 model NOT found at {h5_path}")

if os.path.exists(tflite_path):
    size_mb = os.path.getsize(tflite_path) / 1e6
    print(f"   ✅ .tflite model found ({size_mb:.1f}MB)")
else:
    print(f"   ❌ .tflite model NOT found at {tflite_path}")

# Test 2: Try to import dependencies
print("\n[2/5] Checking dependencies...")
try:
    import cv2
    print("   ✅ OpenCV (cv2) available")
except ImportError as e:
    print(f"   ❌ OpenCV not available: {e}")

try:
    import torch
    print(f"   ✅ PyTorch available (version {torch.__version__})")
except ImportError as e:
    print(f"   ⚠️  PyTorch not available: {e}")

try:
    import tensorflow as tf
    print(f"   ✅ TensorFlow available (version {tf.__version__})")
    tf_available = True
except ImportError as e:
    print(f"   ⚠️  TensorFlow not available: {e}")
    tf_available = False

# Test 3: Load finalwebapp module
print("\n[3/5] Loading finalwebapp module...")
sys.path.insert(0, os.path.dirname(__file__))
try:
    from finalwebapp import material_model, classify_material, material_classes, MODELS_INIT_STATUS
    print("   ✅ finalwebapp imported successfully")
    print(f"   Material classes: {material_classes}")
    print(f"   Material model type: {type(material_model)}")
    if material_model:
        print(f"   ✅ Material model loaded: {MODELS_INIT_STATUS.get('material', 'Unknown status')}")
    else:
        print(f"   ⚠️  Material model is None")
except Exception as e:
    print(f"   ❌ Failed to import finalwebapp: {e}")
    import traceback
    traceback.print_exc()

# Test 4: Try classification on a test image
print("\n[4/5] Testing material classification...")
try:
    # Create a test image (simple gray image)
    test_image = np.ones((224, 224, 3), dtype=np.uint8) * 128
    material, probs = classify_material(test_image)
    print(f"   ✅ Classification successful")
    print(f"   Predicted material: {material}")
    print(f"   Confidence: {probs[list(probs.keys()).index(material)]:.2%}")
except Exception as e:
    print(f"   ❌ Classification failed: {e}")
    import traceback
    traceback.print_exc()

# Test 5: Load and test API module
print("\n[5/5] Loading finalwebapp_api module...")
try:
    from finalwebapp_api import MATERIAL_MODEL, MODELS_STATUS
    print("   ✅ finalwebapp_api imported successfully")
    print(f"   API Material model type: {type(MATERIAL_MODEL)}")
    if MATERIAL_MODEL:
        print(f"   ✅ API Material model loaded: {MODELS_STATUS.get('material', 'Unknown status')}")
    else:
        print(f"   ⚠️  API Material model is None")
except Exception as e:
    print(f"   ❌ Failed to import finalwebapp_api: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 70)
print("Test completed!")
print("=" * 70)
