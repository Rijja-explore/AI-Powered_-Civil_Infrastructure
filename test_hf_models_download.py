#!/usr/bin/env python3
"""
Test Hugging Face Model Download
Verifies that models can be downloaded from HF Hub models repository
"""

import os
from pathlib import Path
from huggingface_hub import hf_hub_download, list_repo_files
import sys

# Configuration
HF_REPO_ID = "RijjaExplore/InfraVision-Models"

print("=" * 70)
print("Hugging Face Model Download Test")
print("=" * 70)

# Step 1: List available files in HF repo
print(f"\n[1/3] Checking models in HF repository: {HF_REPO_ID}")
print("-" * 70)

try:
    files = list_repo_files(repo_id=HF_REPO_ID)
    model_files = [f for f in files if f.endswith(('.pt', '.h5', '.tflite'))]
    
    if not model_files:
        print("⚠️ No model files found in repository!")
        print(f"Available files: {files[:10]}")
        sys.exit(1)
    
    print(f"✅ Found {len(model_files)} model files:")
    for f in model_files:
        print(f"   • {f}")
        
except Exception as e:
    print(f"❌ Error listing files: {e}")
    print("   Make sure your HF token is configured: huggingface-cli login")
    sys.exit(1)

# Step 2: Test downloading each model
print(f"\n[2/3] Testing model downloads")
print("-" * 70)

models_to_test = [
    'material_classifier.h5',
    'material_classifier.tflite',
    'train3_best.pt',
    'segmentation_best.pt'
]

downloaded_count = 0
for model_filename in models_to_test:
    if model_filename not in model_files:
        print(f"⚠️ {model_filename} - NOT found in HF repo")
        continue
    
    try:
        print(f"📥 Downloading {model_filename}...")
        path = hf_hub_download(
            repo_id=HF_REPO_ID,
            filename=model_filename,
            cache_dir=None,
            force_download=False
        )
        size_mb = os.path.getsize(path) / (1024 * 1024)
        print(f"   ✅ Downloaded ({size_mb:.1f}MB) → {path}")
        downloaded_count += 1
    except Exception as e:
        print(f"   ❌ Failed: {e}")

# Step 3: Check hf_model_loader.py configuration
print(f"\n[3/3] Configuration check")
print("-" * 70)

with open('hf_model_loader.py', 'r') as f:
    content = f.read()
    if HF_REPO_ID in content:
        print(f"✅ hf_model_loader.py configured with: {HF_REPO_ID}")
    else:
        print(f"⚠️ hf_model_loader.py not configured with {HF_REPO_ID}")

print("\n" + "=" * 70)
print(f"Summary: {downloaded_count}/{len(models_to_test)} models downloaded successfully")
print("=" * 70)

if downloaded_count == len(models_to_test):
    print("✅ All models accessible from HF Hub - deployment ready!")
    sys.exit(0)
else:
    print("⚠️ Some models missing - upload to HF Hub first")
    sys.exit(1)
