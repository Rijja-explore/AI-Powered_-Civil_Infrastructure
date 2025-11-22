#!/usr/bin/env python3
"""
Preprocessing Pipeline for Crack Detection Dataset
Handles: image loading, resizing, normalization, augmentation, and dataset statistics
"""

import os
import cv2
import numpy as np
from pathlib import Path
import json
from collections import defaultdict
import albumentations as A
from albumentations.pytorch import ToTensorV2

# Configuration
DATASET_PATH = Path("D:/Projects/AI-Powered_-Civil_Infrastructure/Dataset/crack_preprocess")
OUTPUT_STATS_PATH = Path("dataset_stats_crack.json")
TARGET_SIZE = (640, 640)

def get_severity_from_filename(filename):
    """Extract severity from filename if available"""
    filename_lower = filename.lower()
    if 'critical' in filename_lower:
        return 'Critical'
    elif 'severe' in filename_lower:
        return 'Severe'
    elif 'moderate' in filename_lower:
        return 'Moderate'
    elif 'minor' in filename_lower or 'small' in filename_lower:
        return 'Minor'
    else:
        return 'Unknown'

def load_images_from_split(split_path):
    """Load all images from a train/test/valid split"""
    images = []
    valid_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff'}
    
    if not split_path.exists():
        print(f"⚠️ Split path does not exist: {split_path}")
        return images
    
    for file_path in split_path.rglob('*'):
        if file_path.suffix.lower() in valid_extensions:
            images.append(file_path)
    
    return images

def preprocess_image(image_path, target_size=TARGET_SIZE):
    """
    Preprocess a single image:
    1. Load image
    2. Convert BGR to RGB
    3. Resize to target size
    4. Normalize pixel values
    """
    try:
        # Load image
        img_bgr = cv2.imread(str(image_path))
        if img_bgr is None:
            return None
        
        # Convert BGR to RGB
        img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
        
        # Resize
        img_resized = cv2.resize(img_rgb, target_size, interpolation=cv2.INTER_LANCZOS4)
        
        # Normalize to [0, 1]
        img_normalized = img_resized.astype(np.float32) / 255.0
        
        return {
            'image': img_normalized,
            'original_shape': img_bgr.shape,
            'resized_shape': img_resized.shape,
            'pixel_mean': np.mean(img_normalized),
            'pixel_std': np.std(img_normalized)
        }
    except Exception as e:
        print(f"❌ Error processing {image_path}: {e}")
        return None

def create_augmentation_pipeline():
    """Create augmentation transformations for robustness"""
    return A.Compose([
        A.HorizontalFlip(p=0.5),
        A.VerticalFlip(p=0.3),
        A.Rotate(limit=15, p=0.5),
        A.RandomBrightnessContrast(brightness_limit=0.2, contrast_limit=0.2, p=0.5),
        A.GaussNoise(p=0.2),
        A.GaussianBlur(blur_limit=3, p=0.2),
        A.Affine(scale=(0.8, 1.2), p=0.3),
        A.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ], bbox_params=A.BboxParams(format='pascal_voc', min_visibility=0.3))

def compute_dataset_statistics():
    """Compute comprehensive dataset statistics"""
    stats = {
        'dataset_info': {
            'total_images': 0,
            'image_splits': {
                'train': 0,
                'test': 0,
                'valid': 0
            },
            'severity_distribution': defaultdict(int),
            'total_splits': {}
        },
        'image_statistics': {
            'size_distribution': [],
            'pixel_mean': [],
            'pixel_std': []
        },
        'preprocessing_config': {
            'target_size': TARGET_SIZE,
            'normalization': 'MinMax [0,1]',
            'augmentation': 'Yes (flip, rotate, brightness, noise, blur, affine)'
        }
    }
    
    for split in ['train', 'test', 'valid']:
        split_path = DATASET_PATH / split
        images = load_images_from_split(split_path)
        stats['dataset_info']['image_splits'][split] = len(images)
        stats['dataset_info']['total_images'] += len(images)
        
        print(f"📊 Processing {split} split ({len(images)} images)...")
        
        for i, img_path in enumerate(images):
            if i % max(1, len(images) // 10) == 0:
                print(f"  Progress: {i}/{len(images)}")
            
            # Get severity
            severity = get_severity_from_filename(img_path.name)
            stats['dataset_info']['severity_distribution'][severity] += 1
            
            # Preprocess
            result = preprocess_image(img_path)
            if result:
                stats['image_statistics']['size_distribution'].append(result['original_shape'])
                stats['image_statistics']['pixel_mean'].append(float(result['pixel_mean']))
                stats['image_statistics']['pixel_std'].append(float(result['pixel_std']))
    
    # Convert to serializable format
    stats['dataset_info']['severity_distribution'] = dict(stats['dataset_info']['severity_distribution'])
    
    # Compute aggregate statistics
    if stats['image_statistics']['pixel_mean']:
        stats['image_statistics']['aggregate'] = {
            'mean_pixel_mean': float(np.mean(stats['image_statistics']['pixel_mean'])),
            'mean_pixel_std': float(np.mean(stats['image_statistics']['pixel_std'])),
            'std_pixel_mean': float(np.std(stats['image_statistics']['pixel_mean'])),
            'std_pixel_std': float(np.std(stats['image_statistics']['pixel_std']))
        }
    
    return stats

def main():
    """Main preprocessing pipeline"""
    print("🚀 Starting Crack Dataset Preprocessing...")
    print(f"📂 Dataset path: {DATASET_PATH}")
    
    if not DATASET_PATH.exists():
        print(f"❌ Dataset path does not exist: {DATASET_PATH}")
        return
    
    # Compute statistics
    print("\n📊 Computing dataset statistics...")
    stats = compute_dataset_statistics()
    
    # Save statistics
    with open(OUTPUT_STATS_PATH, 'w') as f:
        json.dump(stats, f, indent=2)
    
    print(f"\n✅ Preprocessing complete!")
    print(f"   Total images: {stats['dataset_info']['total_images']}")
    print(f"   Train: {stats['dataset_info']['image_splits']['train']}")
    print(f"   Test: {stats['dataset_info']['image_splits']['test']}")
    print(f"   Valid: {stats['dataset_info']['image_splits']['valid']}")
    print(f"   Severity distribution: {stats['dataset_info']['severity_distribution']}")
    print(f"   Statistics saved to: {OUTPUT_STATS_PATH}")

if __name__ == '__main__':
    main()
