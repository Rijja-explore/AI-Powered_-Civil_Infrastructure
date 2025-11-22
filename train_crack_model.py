#!/usr/bin/env python3
"""
Model Training for Crack Detection using YOLOv8
Trains on crack_preprocess dataset and saves metrics
"""

from ultralytics import YOLO
from pathlib import Path
import json
import yaml

# Configuration
DATASET_PATH = Path("D:/Projects/AI-Powered_-Civil_Infrastructure/Dataset/crack_preprocess")
MODEL_NAME = "yolov8m.pt"  # medium model
RUNS_DIR = Path("runs/detect/crack")
METRICS_OUTPUT = Path("metrics_crack.json")

def create_dataset_yaml():
    """Create dataset.yaml for YOLO training"""
    dataset_config = {
        'path': str(DATASET_PATH.parent),
        'train': str(DATASET_PATH / 'train'),
        'val': str(DATASET_PATH / 'valid'),
        'test': str(DATASET_PATH / 'test'),
        'nc': 1,  # number of classes
        'names': ['crack']  # class names
    }
    
    yaml_path = DATASET_PATH.parent / 'crack_dataset.yaml'
    with open(yaml_path, 'w') as f:
        yaml.dump(dataset_config, f)
    
    return yaml_path

def train_crack_model():
    """Train YOLOv8 model for crack detection"""
    print("🚀 Starting Crack Detection Model Training...")
    
    # Create dataset.yaml
    dataset_yaml = create_dataset_yaml()
    print(f"📝 Dataset config: {dataset_yaml}")
    
    # Load model
    print(f"📥 Loading base model: {MODEL_NAME}")
    model = YOLO(MODEL_NAME)
    
    # Train
    print("🔨 Training model...")
    results = model.train(
        data=str(dataset_yaml),
        epochs=100,
        imgsz=640,
        batch=16,
        device=0,  # GPU device
        patience=20,  # early stopping
        save=True,
        augment=True,
        flipud=0.5,
        fliplr=0.5,
        mosaic=1.0,
        project='runs/detect',
        name='crack',
        seed=42,
        verbose=True
    )
    
    print("✅ Training complete!")
    
    # Evaluate on test set
    print("📊 Evaluating on test set...")
    metrics = model.val()
    
    # Extract key metrics
    metrics_dict = {
        'training_config': {
            'model': MODEL_NAME,
            'epochs': 100,
            'batch_size': 16,
            'image_size': 640,
            'augmentation': True
        },
        'performance_metrics': {
            'precision': float(metrics.box.mp) if hasattr(metrics, 'box') else 0.0,
            'recall': float(metrics.box.mr) if hasattr(metrics, 'box') else 0.0,
            'mAP50': float(metrics.box.map50) if hasattr(metrics, 'box') else 0.0,
            'mAP50_95': float(metrics.box.map) if hasattr(metrics, 'box') else 0.0,
            'fitness': float(metrics.box.fitness) if hasattr(metrics, 'box') else 0.0,
        },
        'dataset_info': {
            'train_images': len(list((DATASET_PATH / 'train').rglob('*.jpg'))) + len(list((DATASET_PATH / 'train').rglob('*.png'))),
            'val_images': len(list((DATASET_PATH / 'valid').rglob('*.jpg'))) + len(list((DATASET_PATH / 'valid').rglob('*.png'))),
            'test_images': len(list((DATASET_PATH / 'test').rglob('*.jpg'))) + len(list((DATASET_PATH / 'test').rglob('*.png')))
        },
        'model_path': str(RUNS_DIR / 'weights' / 'best.pt'),
        'status': 'completed'
    }
    
    # Save metrics
    with open(METRICS_OUTPUT, 'w') as f:
        json.dump(metrics_dict, f, indent=2)
    
    print(f"📊 Metrics saved to: {METRICS_OUTPUT}")
    print(f"🎯 Performance: mAP50={metrics_dict['performance_metrics']['mAP50']:.3f}, mAP50-95={metrics_dict['performance_metrics']['mAP50_95']:.3f}")
    
    return metrics_dict

def main():
    """Main training pipeline"""
    if not DATASET_PATH.exists():
        print(f"❌ Dataset path does not exist: {DATASET_PATH}")
        return
    
    train_crack_model()
    print("✨ Crack detection model training complete!")

if __name__ == '__main__':
    main()
