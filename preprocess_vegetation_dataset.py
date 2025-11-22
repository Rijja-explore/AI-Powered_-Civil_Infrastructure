#!/usr/bin/env python3
"""
Preprocessing Pipeline for Vegetation Detection Dataset
Handles: image loading, resizing, normalization, augmentation, and dataset statistics
"""

import os
import cv2
import numpy as np
from pathlib import Path
import json
from collections import defaultdict
import albumentations as A

# Configuration
DATASET_PATH = Path("D:/Projects/AI-Powered_-Civil_Infrastructure/Dataset/vegetation_preprocess")
OUTPUT_STATS_PATH = Path("dataset_stats_vegetation.json")
TARGET_SIZE = (640, 640)

def get_vegetation_type_from_filename(filename):
    """Extract vegetation type from filename if available"""
    filename_lower = filename.lower()
    types = []
    
    if 'moss' in filename_lower:
        types.append('Moss')
    if 'algae' in filename_lower:
        types.append('Algae')
    if 'lichen' in filename_lower:
        types.append('Lichen')
    if 'vine' in filename_lower or 'root' in filename_lower:
        types.append('Vines/Roots')
    if 'plant' in filename_lower or 'growth' in filename_lower:
        types.append('Plants')
    
    return types if types else ['Unknown']

def get_severity_from_filename(filename):
    """Extract coverage severity from filename"""
    filename_lower = filename.lower()
    if 'high' in filename_lower or 'dense' in filename_lower:
        return 'High'
    elif 'medium' in filename_lower or 'moderate' in filename_lower:
        return 'Medium'
    elif 'low' in filename_lower or 'sparse' in filename_lower:
        return 'Low'
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
    Preprocess a single image for vegetation detection
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
        
        # Compute greenness metric (indicator of vegetation)
        img_hsv = cv2.cvtColor(img_resized, cv2.COLOR_RGB2HSV)
        green_mask = cv2.inRange(img_hsv, np.array([35, 40, 40]), np.array([90, 255, 255]))
        greenness_score = np.sum(green_mask > 0) / green_mask.size * 100
        
        return {
            'image': img_normalized,
            'original_shape': img_bgr.shape,
            'resized_shape': img_resized.shape,
            'pixel_mean': np.mean(img_normalized),
            'pixel_std': np.std(img_normalized),
            'greenness_score': greenness_score
        }
    except Exception as e:
        print(f"❌ Error processing {image_path}: {e}")
        return None

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
            'vegetation_types': defaultdict(int),
            'coverage_distribution': defaultdict(int)
        },
        'image_statistics': {
            'size_distribution': [],
            'pixel_mean': [],
            'pixel_std': [],
            'greenness_scores': []
        },
        'preprocessing_config': {
            'target_size': TARGET_SIZE,
            'normalization': 'MinMax [0,1]',
            'augmentation': 'Yes (flip, rotate, brightness, contrast, blur)'
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
            
            # Get vegetation info
            veg_types = get_vegetation_type_from_filename(img_path.name)
            for vtype in veg_types:
                stats['dataset_info']['vegetation_types'][vtype] += 1
            
            coverage = get_severity_from_filename(img_path.name)
            stats['dataset_info']['coverage_distribution'][coverage] += 1
            
            # Preprocess
            result = preprocess_image(img_path)
            if result:
                stats['image_statistics']['size_distribution'].append(result['original_shape'])
                stats['image_statistics']['pixel_mean'].append(float(result['pixel_mean']))
                stats['image_statistics']['pixel_std'].append(float(result['pixel_std']))
                stats['image_statistics']['greenness_scores'].append(float(result['greenness_score']))
    
    # Convert to serializable format
    stats['dataset_info']['vegetation_types'] = dict(stats['dataset_info']['vegetation_types'])
    stats['dataset_info']['coverage_distribution'] = dict(stats['dataset_info']['coverage_distribution'])
    
    # Compute aggregate statistics
    if stats['image_statistics']['pixel_mean']:
        stats['image_statistics']['aggregate'] = {
            'mean_pixel_mean': float(np.mean(stats['image_statistics']['pixel_mean'])),
            'mean_pixel_std': float(np.mean(stats['image_statistics']['pixel_std'])),
            'std_pixel_mean': float(np.std(stats['image_statistics']['pixel_mean'])),
            'std_pixel_std': float(np.std(stats['image_statistics']['pixel_std'])),
            'avg_greenness_score': float(np.mean(stats['image_statistics']['greenness_scores'])),
            'max_greenness_score': float(np.max(stats['image_statistics']['greenness_scores'])),
            'min_greenness_score': float(np.min(stats['image_statistics']['greenness_scores']))
        }
    
    return stats

def main():
    """Main preprocessing pipeline"""
    print("🚀 Starting Vegetation Dataset Preprocessing...")
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
    print(f"   Vegetation types: {stats['dataset_info']['vegetation_types']}")
    print(f"   Coverage distribution: {stats['dataset_info']['coverage_distribution']}")
    print(f"   Statistics saved to: {OUTPUT_STATS_PATH}")

if __name__ == '__main__':
    main()
