import cv2
import numpy as np
from ultralytics import YOLO
from models import DetectionResult, BoundingBox, FrameDetection
from typing import List, Dict, Any, Optional

# Load pre-trained YOLO model
# You can replace this with a custom-trained model path if available
model = YOLO('yolov8x.pt')  # Using the "nano" model for speed

# Constants
CONFIDENCE_THRESHOLD = 0.2
BOTTLE_CLASS_ID = 39  # Class 39 in COCO dataset is 'bottle'
POINTS_PER_BOTTLE_IMAGE = 10
POINTS_PER_BOTTLE_VIDEO = 5

def process_image(image_path: str, user_id: str) -> DetectionResult:
    """
    Process an image to detect plastic bottles.
    
    Args:
        image_path: Path to the uploaded image
        user_id: User identifier
        
    Returns:
        DetectionResult object with detection information
    """
    # Load the image
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"Could not read image at {image_path}")
    
    # Run YOLO detection
    results = model(img)
    
    # Parse results
    bottles_detected = 0
    bottle_locations: List[BoundingBox] = []
    
    # Process detection results for the first (and only) image
    result = results[0]
    for box in result.boxes:
        cls = int(box.cls[0])
        conf = float(box.conf[0])
        
        # Check if it's a bottle with sufficient confidence
        if cls == BOTTLE_CLASS_ID and conf > CONFIDENCE_THRESHOLD:
            bottles_detected += 1
            
            # Get coordinates (convert to int for JSON serialization)
            x1, y1, x2, y2 = box.xyxy[0].tolist()
            bottle_locations.append(BoundingBox(
                x1=int(x1),
                y1=int(y1),
                x2=int(x2),
                y2=int(y2),
                confidence=conf
            ))
    
    # Calculate points earned (simple model: 10 points per bottle)
    points_earned = bottles_detected * POINTS_PER_BOTTLE_IMAGE
    
    return DetectionResult(
        success=True,
        bottles_detected=bottles_detected,
        bottle_locations=bottle_locations,
        points_earned=points_earned,
        total_points=0  # Will be updated in main.py
    )

def process_video(video_path: str, user_id: str) -> DetectionResult:
    """
    Process a video to detect plastic bottles.
    
    Args:
        video_path: Path to the uploaded video
        user_id: User identifier
        
    Returns:
        DetectionResult object with detection information
    """
    # Open the video
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError(f"Could not open video at {video_path}")
    
    frame_count = 0
    bottles_detected_total = 0
    bottle_frames: List[FrameDetection] = []
    
    # Process every 10th frame to save computation
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        frame_count += 1
        if frame_count % 10 != 0:
            continue
        
        # Run YOLO detection on the frame
        results = model(frame)
        
        # Process results
        bottles_in_frame = 0
        bottle_locations: List[BoundingBox] = []
        
        for result in results:
            for box in result.boxes:
                cls = int(box.cls[0])
                conf = float(box.conf[0])
                
                # Check if it's a bottle with sufficient confidence
                if cls == BOTTLE_CLASS_ID and conf > CONFIDENCE_THRESHOLD:
                    bottles_in_frame += 1
                    
                    # Get coordinates
                    x1, y1, x2, y2 = box.xyxy[0].tolist()
                    bottle_locations.append(BoundingBox(
                        x1=int(x1),
                        y1=int(y1),
                        x2=int(x2),
                        y2=int(y2),
                        confidence=conf
                    ))
        
        if bottles_in_frame > 0:
            bottle_frames.append(FrameDetection(
                frame=frame_count,
                bottles=bottles_in_frame,
                locations=bottle_locations
            ))
            bottles_detected_total += bottles_in_frame
    
    cap.release()
    
    # Calculate rewards - for videos, we count unique frames with bottles
    # This helps avoid counting the same bottle multiple times
    unique_frames_with_bottles = len(bottle_frames)
    points_earned = unique_frames_with_bottles * POINTS_PER_BOTTLE_VIDEO
    
    return DetectionResult(
        success=True,
        bottles_detected=bottles_detected_total,
        bottle_frames=bottle_frames,
        points_earned=points_earned,
        total_points=0  # Will be updated in main.py
    )