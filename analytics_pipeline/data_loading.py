"""
Data Loading Module
Loads and preprocesses images from dataset directories.
"""

import os
import numpy as np
from pathlib import Path
from typing import Tuple, List, Dict
from PIL import Image, ImageEnhance
import warnings
warnings.filterwarnings('ignore')


def load_images_from_dataset(
    crack_dir: str = "Dataset/crack_preprocess",
    vegetation_dir: str = "Dataset/vegetation_preprocess",
    target_size: Tuple[int, int] = (640, 640),
    splits: List[str] = ["train", "test", "valid"]
) -> Tuple[Dict, Dict]:
    """
    Load all images from crack and vegetation datasets.
    
    Args:
        crack_dir: Path to crack dataset directory
        vegetation_dir: Path to vegetation dataset directory
        target_size: Target image size (width, height)
        splits: Dataset splits to load (train, test, valid)
    
    Returns:
        Tuple of (crack_data_dict, vegetation_data_dict)
        Each dict contains: {
            'images': list of preprocessed images,
            'filenames': list of filenames,
            'split': list of split labels (train/test/valid),
            'severity': list of severity labels (if available)
        }
    """
    crack_data = {
        'images': [],
        'filenames': [],
        'split': [],
        'severity': []
    }
    
    vegetation_data = {
        'images': [],
        'filenames': [],
        'split': [],
        'type': [],
        'coverage': []
    }
    
    # Load crack dataset
    print(f"Loading crack dataset from {crack_dir}...")
    for split in splits:
        split_path = os.path.join(crack_dir, split)
        if os.path.exists(split_path):
            # Iterate through severity folders if they exist
            severity_folders = [d for d in os.listdir(split_path) 
                              if os.path.isdir(os.path.join(split_path, d))]
            
            if severity_folders:
                for severity in severity_folders:
                    severity_path = os.path.join(split_path, severity)
                    image_files = [f for f in os.listdir(severity_path) 
                                  if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
                    
                    for filename in image_files:
                        img_path = os.path.join(severity_path, filename)
                        try:
                            img = preprocess_image(img_path, target_size)
                            crack_data['images'].append(img)
                            crack_data['filenames'].append(filename)
                            crack_data['split'].append(split)
                            crack_data['severity'].append(severity)
                        except Exception as e:
                            print(f"Error loading {img_path}: {e}")
            else:
                # No severity folders, load directly
                image_files = [f for f in os.listdir(split_path) 
                              if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
                
                for filename in image_files:
                    img_path = os.path.join(split_path, filename)
                    try:
                        img = preprocess_image(img_path, target_size)
                        crack_data['images'].append(img)
                        crack_data['filenames'].append(filename)
                        crack_data['split'].append(split)
                        # Try to extract severity from filename
                        severity = extract_severity_from_filename(filename)
                        crack_data['severity'].append(severity)
                    except Exception as e:
                        print(f"Error loading {img_path}: {e}")
    
    # Load vegetation dataset
    print(f"Loading vegetation dataset from {vegetation_dir}...")
    for split in splits:
        split_path = os.path.join(vegetation_dir, split)
        if os.path.exists(split_path):
            # Iterate through vegetation type folders if they exist
            type_folders = [d for d in os.listdir(split_path) 
                           if os.path.isdir(os.path.join(split_path, d))]
            
            if type_folders:
                for veg_type in type_folders:
                    type_path = os.path.join(split_path, veg_type)
                    image_files = [f for f in os.listdir(type_path) 
                                  if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
                    
                    for filename in image_files:
                        img_path = os.path.join(type_path, filename)
                        try:
                            img = preprocess_image(img_path, target_size)
                            vegetation_data['images'].append(img)
                            vegetation_data['filenames'].append(filename)
                            vegetation_data['split'].append(split)
                            vegetation_data['type'].append(veg_type)
                            vegetation_data['coverage'].append(0.0)  # Will be computed later
                        except Exception as e:
                            print(f"Error loading {img_path}: {e}")
            else:
                # No type folders, load directly
                image_files = [f for f in os.listdir(split_path) 
                              if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
                
                for filename in image_files:
                    img_path = os.path.join(split_path, filename)
                    try:
                        img = preprocess_image(img_path, target_size)
                        vegetation_data['images'].append(img)
                        vegetation_data['filenames'].append(filename)
                        vegetation_data['split'].append(split)
                        veg_type = extract_vegetation_type_from_filename(filename)
                        vegetation_data['type'].append(veg_type)
                        vegetation_data['coverage'].append(0.0)
                    except Exception as e:
                        print(f"Error loading {img_path}: {e}")
    
    print(f"✅ Loaded {len(crack_data['images'])} crack images and {len(vegetation_data['images'])} vegetation images")
    return crack_data, vegetation_data


def preprocess_image(
    image_path: str,
    target_size: Tuple[int, int] = (640, 640),
    apply_clahe: bool = True,
    normalize: bool = True
) -> np.ndarray:
    """
    Load and preprocess a single image using Pillow (PIL).
    
    Args:
        image_path: Path to image file
        target_size: Target size (width, height)
        apply_clahe: Apply basic contrast enhancement (Pillow-based)
        normalize: Normalize to [0, 1]
    
    Returns:
        Preprocessed image as numpy array (H, W, 3) in RGB format
    """
    try:
        # Load image with Pillow (automatically handles RGB)
        img = Image.open(image_path)
        
        # Convert RGBA or grayscale to RGB
        if img.mode != 'RGB':
            if img.mode == 'RGBA':
                # Convert RGBA to RGB (remove alpha)
                background = Image.new('RGB', img.size, (255, 255, 255))
                background.paste(img, mask=img.split()[3] if len(img.split()) == 4 else None)
                img = background
            elif img.mode == 'L':
                # Grayscale to RGB
                img = img.convert('RGB')
            else:
                img = img.convert('RGB')
        
        # Resize
        img = img.resize(target_size, Image.Resampling.LANCZOS)
        
        # Convert to numpy array
        img_array = np.array(img, dtype=np.uint8)
        
        # Apply basic contrast enhancement
        if apply_clahe:
            # Simple contrast enhancement using Pillow
            img_pil = Image.fromarray(img_array)
            enhancer = ImageEnhance.Contrast(img_pil)
            img_pil = enhancer.enhance(1.5)
            img_array = np.array(img_pil, dtype=np.uint8)
        
        # Normalize to [0, 1]
        if normalize:
            img_array = img_array.astype(np.float32) / 255.0
        else:
            img_array = img_array.astype(np.float32)
        
        return img_array
    
    except Exception as e:
        raise ValueError(f"Failed to load/preprocess image: {image_path}. Error: {e}")


def extract_severity_from_filename(filename: str) -> str:
    """
    Extract crack severity from filename.
    Looks for keywords like 'mild', 'moderate', 'severe'.
    """
    filename_lower = filename.lower()
    if 'severe' in filename_lower:
        return 'Severe'
    elif 'moderate' in filename_lower or 'medium' in filename_lower:
        return 'Moderate'
    elif 'mild' in filename_lower or 'light' in filename_lower:
        return 'Mild'
    elif 'no' in filename_lower or 'none' in filename_lower or 'clean' in filename_lower:
        return 'None'
    else:
        return 'Unknown'


def extract_vegetation_type_from_filename(filename: str) -> str:
    """
    Extract vegetation type from filename.
    Looks for keywords like 'moss', 'algae', 'lichen', etc.
    """
    filename_lower = filename.lower()
    if 'moss' in filename_lower:
        return 'Moss'
    elif 'algae' in filename_lower:
        return 'Algae'
    elif 'lichen' in filename_lower:
        return 'Lichen'
    elif 'ivy' in filename_lower or 'vine' in filename_lower:
        return 'Ivy/Vine'
    elif 'none' in filename_lower or 'clean' in filename_lower:
        return 'None'
    else:
        return 'Other'
