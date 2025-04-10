from ultralytics import YOLO
import yaml
import os
import shutil
from pathlib import Path

"""
This script helps you train a custom YOLO model specifically for plastic bottles in trash bins.

For best results:
1. Collect diverse images of trash bins with plastic bottles
2. Label the plastic bottles in the images
3. Split them into training and validation sets
4. Run this script to train a custom model
"""

# Configuration
CONFIG = {
    'model_type': 'yolov8s.pt',  # Base model to fine-tune (s = small)
    'epochs': 100,               # Number of training epochs
    'img_size': 640,             # Input image size
    'batch_size': 16,            # Batch size
    'patience': 20,              # Early stopping patience
    'project_name': 'plastic_bottle_detector',  # Project name
    'classes': {                 # Class mapping
        0: 'plastic_bottle',
    }
}

def setup_directories():
    """Create the necessary directory structure."""
    dirs = [
        'dataset/images/train',
        'dataset/images/val',
        'dataset/labels/train',
        'dataset/labels/val'
    ]
    
    for d in dirs:
        os.makedirs(d, exist_ok=True)
    
    return Path('dataset')

def create_dataset_config(dataset_path):
    """Create the dataset configuration file (dataset.yaml)."""
    config_path = dataset_path.parent / 'dataset.yaml'
    
    dataset_config = {
        'path': str(dataset_path),  # Dataset root dir
        'train': 'images/train',    # Train images (relative to 'path')
        'val': 'images/val',        # Val images (relative to 'path')
        'names': CONFIG['classes']  # Class names
    }
    
    # Save the dataset configuration
    with open(config_path, 'w') as f:
        yaml.dump(dataset_config, f, default_flow_style=False)
    
    return config_path

def check_dataset(dataset_path):
    """Check if the dataset is properly set up."""
    train_images = list(Path(dataset_path / 'images/train').glob('*'))
    val_images = list(Path(dataset_path / 'images/val').glob('*'))
    train_labels = list(Path(dataset_path / 'labels/train').glob('*'))
    val_labels = list(Path(dataset_path / 'labels/val').glob('*'))
    
    print(f"Found {len(train_images)} training images and {len(train_labels)} training labels")
    print(f"Found {len(val_images)} validation images and {len(val_labels)} validation labels")
    
    if len(train_images) == 0 or len(val_images) == 0:
        print("ERROR: No images found in dataset directory!")
        return False
    
    if len(train_labels) == 0 or len(val_labels) == 0:
        print("ERROR: No labels found in dataset directory!")
        return False
    
    if len(train_images) != len(train_labels) or len(val_images) != len(val_labels):
        print("WARNING: Number of images and labels don't match!")
    
    return True

def train_model(config_path):
    """Train the YOLO model on the dataset."""
    # Load a pre-trained model
    model = YOLO(CONFIG['model_type'])
    
    # Train the model
    results = model.train(
        data=str(config_path),
        epochs=CONFIG['epochs'],
        imgsz=CONFIG['img_size'],
        batch=CONFIG['batch_size'],
        patience=CONFIG['patience'],
        name=CONFIG['project_name']
    )
    
    return results

def validate_model(config_path):
    """Validate the trained model on the validation set."""
    # Load the best model
    model_path = f"runs/detect/{CONFIG['project_name']}/weights/best.pt"
    if not os.path.exists(model_path):
        print(f"ERROR: Model not found at {model_path}")
        return None
    
    model = YOLO(model_path)
    
    # Run validation
    results = model.val(data=str(config_path))
    
    return results

def export_model():
    """Export the model to different formats."""
    # Load the best model
    model_path = f"runs/detect/{CONFIG['project_name']}/weights/best.pt"
    if not os.path.exists(model_path):
        print(f"ERROR: Model not found at {model_path}")
        return
    
    model = YOLO(model_path)
    
    # Export to different formats
    model.export(format='onnx')   # ONNX format
    model.export(format='torchscript')  # TorchScript format
    
    print(f"Model exported to runs/detect/{CONFIG['project_name']}/weights/")

def main():
    print("=" * 50)
    print("Plastic Bottle Detector - Training Script")
    print("=" * 50)
    
    # Setup
    print("\n[1] Setting up directories...")
    dataset_path = setup_directories()
    
    # Check for dataset
    print("\n[2] Checking dataset...")
    if not check_dataset(dataset_path):
        print("\nDataset preparation guide:")
        print("1. Place your training images in 'dataset/images/train/'")
        print("2. Place your validation images in 'dataset/images/val/'")
        print("3. Place your training labels in 'dataset/labels/train/'")
        print("4. Place your validation labels in 'dataset/labels/val/'")
        print("\nLabel format should be YOLO format: class_id x_center y_center width height")
        print("Run this script again after preparing your dataset.")
        return
    
    # Create config
    print("\n[3] Creating dataset config...")
    config_path = create_dataset_config(dataset_path)
    
    # Train model
    print("\n[4] Training model...")
    print(f"Using base model: {CONFIG['model_type']}")
    print(f"Training for {CONFIG['epochs']} epochs with batch size {CONFIG['batch_size']}")
    input("Press Enter to start training (Ctrl+C to cancel)...")
    
    train_results = train_model(config_path)
    
    # Validate model
    print("\n[5] Validating model...")
    val_results = validate_model(config_path)
    
    # Export model
    print("\n[6] Exporting model...")
    export_model()
    
    print("\n" + "=" * 50)
    print("Training complete!")
    print(f"Model saved to: runs/detect/{CONFIG['project_name']}/weights/")
    print("=" * 50)

if __name__ == "__main__":
    main()