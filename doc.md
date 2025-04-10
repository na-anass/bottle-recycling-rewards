# Complete Tutorial: Plastic Bottle Recycling Reward System with FastAPI and YOLO

I've created a comprehensive solution for your plastic bottle recycling reward system. This system uses YOLOv8 for detection and FastAPI for the backend. Here's how to get started:

## Project Overview

This system detects plastic bottles in trash bins from images or videos uploaded by users, then rewards them with points. Key features:

- **Object detection**: Uses pre-trained YOLOv8 (can be customized)
- **FastAPI backend**: High-performance REST API
- **Interactive frontend**: User-friendly interface with visual feedback
- **Points system**: Rewards users for recycling

## Project Structure

```
bottle-recycling-rewards/
├── backend/               # FastAPI server
│   ├── main.py            # API endpoints
│   ├── models.py          # Data models (Pydantic)
│   ├── detection.py       # YOLO detection logic
│   ├── database.py        # Simple DB implementation
│   └── requirements.txt   # Dependencies
├── frontend/              # Web client
│   ├── index.html         # User interface
│   ├── app.js             # Frontend logic
│   └── styles.css         # CSS styling
├── model/                 # Custom model training (optional)
│   ├── train.py           # Training script
│   └── dataset.yaml       # Dataset configuration
└── .gitignore             # Git ignore file
```

## Setup Instructions

### 1. Backend Setup

First, set up the Python environment and install the required dependencies:

```bash
# Create and navigate to project directory
mkdir bottle-recycling-rewards
cd bottle-recycling-rewards

# Create backend directory
mkdir -p backend
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

The backend uses these key components:
- FastAPI for the API server
- YOLOv8 (via ultralytics) for object detection
- Pydantic for data validation

### 2. Run the Backend

```bash
# From the backend directory
uvicorn main:app --reload
```

This starts the FastAPI server at http://localhost:8000. The automatic documentation is available at http://localhost:8000/docs.

### 3. Setup the Frontend

```bash
# Create frontend directory
mkdir -p frontend
cd frontend

# Serve the frontend (simple method)
python -m http.server 8000
```

Navigate to http://localhost:8000 in your browser to use the application.

## How the System Works

### Detection Process

1. **Upload**: User uploads an image/video through the web interface
2. **Processing**: Backend processes the media using YOLO to detect bottles
3. **Analysis**: System identifies bottles with confidence scores above 0.5
4. **Reward**: Points are awarded based on detections (10 points per bottle in images, 5 points per unique frame with bottles in videos)

### Pre-trained vs. Custom Model

The system uses a pre-trained YOLOv8 model that can already detect bottles (class 39 in COCO dataset). This works well for general bottle detection, but for better accuracy with plastic bottles specifically in trash bins, you can train a custom model:

```bash
# Navigate to the model directory
cd model

# Prepare your dataset:
# - Place training images in dataset/images/train/
# - Place validation images in dataset/images/val/
# - Place training labels in dataset/labels/train/
# - Place validation labels in dataset/labels/val/

# Run the training script
python train.py
```

After training, update the model path in `backend/detection.py`:

```python
# Change this line
model = YOLO('yolov8n.pt')  

# To use your custom model
model = YOLO('../model/runs/detect/plastic_bottle_detector/weights/best.pt')
```

## Customization Options

- **Point values**: Adjust reward points in `backend/detection.py`
- **Detection threshold**: Modify the confidence threshold (currently 0.5)
- **UI theme**: Customize the frontend styles in `frontend/styles.css`
- **Database**: Replace the in-memory DB with a real database (SQLite, PostgreSQL, etc.)

## Key Files

1. **backend/main.py**: FastAPI application with API endpoints
2. **backend/detection.py**: YOLO detection implementation
3. **frontend/app.js**: Client-side logic for the web interface
4. **model/train.py**: Custom model training script

This implementation provides a solid foundation that you can expand with additional features like user authentication, more sophisticated reward systems, or database persistence.