"""
Model downloader for distributed deployment
Downloads trained models from GitHub releases at runtime
"""
import os
import urllib.request
import shutil
from pathlib import Path

# GitHub raw content URLs for model files
MODEL_URLS = {
    'crack_detection': {
        'best': 'https://github.com/Rijja-explore/AI-Powered_Civil_Infrastructure/releases/download/models/train3_best.pt',
        'last': 'https://github.com/Rijja-explore/AI-Powered_Civil_Infrastructure/releases/download/models/train3_last.pt',
        'dest_dir': 'runs/detect/train3/weights'
    },
    'segmentation': {
        'best': 'https://github.com/Rijja-explore/AI-Powered_Civil_Infrastructure/releases/download/models/segmentation_best.pt',
        'last': 'https://github.com/Rijja-explore/AI-Powered_Civil_Infrastructure/releases/download/models/segmentation_last.pt',
        'dest_dir': 'segmentation_model/weights'
    }
}

def download_model(url, dest_path):
    """Download a model file with progress indicator"""
    try:
        print(f"📥 Downloading {os.path.basename(dest_path)}...")
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
        urllib.request.urlretrieve(url, dest_path)
        size_mb = os.path.getsize(dest_path) / (1024 * 1024)
        print(f"✅ Downloaded {os.path.basename(dest_path)} ({size_mb:.1f}MB)")
        return True
    except Exception as e:
        print(f"⚠️ Failed to download {url}: {e}")
        return False

def ensure_models_exist():
    """Ensure trained models are available, download if missing"""
    print("\n🔍 Checking for trained models...")
    
    models_found = 0
    total_models = 0
    
    for model_type, files in MODEL_URLS.items():
        dest_dir = files['dest_dir']
        
        for file_key in ['best', 'last']:
            total_models += 1
            dest_path = os.path.join(dest_dir, f"{file_key}.pt")
            
            if os.path.exists(dest_path):
                size_mb = os.path.getsize(dest_path) / (1024 * 1024)
                print(f"✅ Found {model_type} {file_key} model ({size_mb:.1f}MB)")
                models_found += 1
            else:
                url = files[file_key]
                if download_model(url, dest_path):
                    models_found += 1
    
    print(f"\n📊 Models ready: {models_found}/{total_models}")
    return models_found > 0

if __name__ == '__main__':
    ensure_models_exist()
