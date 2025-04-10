# Plastic Bottle Recycling Reward System

A machine learning-based application that detects plastic bottles in trash bins and rewards users for recycling.

## Overview

This project builds a complete system for detecting when users recycle plastic bottles and rewards them with points. It consists of:

1. A Python backend using FastAPI and YOLO object detection
2. A web-based frontend for uploading images/videos
3. A reward points tracking system

## Project Structure

```
bottle-recycling-rewards/
├── backend/
│   ├── main.py                # Main FastAPI application
│   ├── models.py              # Pydantic data models
│   ├── detection.py           # YOLO detection logic
│   ├── database.py            # Database operations (in-memory for this demo)
│   ├── requirements.txt       # Python dependencies
│   └── uploads/               # Directory for uploaded files (auto-created)
├── frontend/
│   ├── index.html             # Web interface
│   ├── app.js                 # Frontend logic
│   └── styles.css             # Optional additional styles
├── model/
│   ├── train.py               # Custom model training script
│   ├── dataset.yaml           # Dataset configuration
│   └── dataset/               # Training data (when using custom model)
│       ├── images/
│       │   ├── train/         # Training images
│       │   └── val/           # Validation images
│       └── labels/
│           ├── train/         # Training labels
│           └── val/           # Validation labels
├── .gitignore                 # Git ignore file
└── README.md                  # This documentation
```

## Getting Started

### Prerequisites

- Python 3.8+
- Node.js (optional, for development server)
- Web browser

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/bottle-recycling-rewards.git
   cd bottle-recycling-rewards
   ```

2. Set up the backend:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. Start the backend server:
   ```bash
   uvicorn main:app --reload
   ```

4. Serve the frontend:
   - Using Python's built-in server:
     ```bash
     cd ../frontend
     python -m http.server 8000
     ```
   - Or using a Node.js development server:
     ```bash
     cd ../frontend
     npx http-server
     ```

5. Open your browser and navigate to:
   - Frontend: http://localhost:8000
   - API Documentation: http://localhost:8000/docs (FastAPI automatic swagger docs)

## How It Works

### Backend

The FastAPI backend:
- Provides endpoints for image/video upload and processing
- Uses YOLO to detect plastic bottles in images and videos
- Tracks user points in a database (in-memory for this demo)
- Returns detection results and reward points to the client

### Frontend

The web frontend:
- Allows users to upload images/videos via drag-and-drop or file picker
- Displays detection results with bounding boxes around detected bottles
- Shows points earned and progress toward rewards
- Provides a visual progress bar for user engagement

### YOLO Detection

By default, the system uses a pre-trained YOLOv8 model that can detect bottles (class 39 in COCO dataset). For better accuracy, you can train a custom model using the provided training script.

## API Endpoints

- `POST /api/upload`: Upload and process images/videos
  - Request: `multipart/form-data` with `file` and `user_id` fields
  - Response: Detection results and points earned

- `GET /api/user/points/{user_id}`: Get user's total points
  - Response: User ID and total points

## Custom Training (Optional)

If you want to improve detection accuracy for your specific use case:

1. Collect images of trash bins with plastic bottles
2. Label them using tools like CVAT, LabelImg, or Roboflow
3. Organize the dataset according to the structure in `model/dataset/`
4. Run the training script:
   ```bash
   cd model
   python train.py
   ```
5. Update the model path in `backend/detection.py`

## Configuration

- Default detection threshold: 0.5 (adjust in `backend/detection.py`)
- Default reward: 10 points per bottle (adjust in `backend/main.py`)
- Model path: Can be changed to use a custom-trained model

## Technologies Used

- **Backend**:
  - FastAPI: Modern, high-performance web framework for Python
  - Ultralytics YOLOv8: State-of-the-art object detection
  - OpenCV: Image and video processing
  - Pydantic: Data validation and settings management

## License

This project is licensed under the MIT License - see the LICENSE file for details.