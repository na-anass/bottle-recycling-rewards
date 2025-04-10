from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any

class BoundingBox(BaseModel):
    """Bounding box coordinates for a detected object."""
    x1: int
    y1: int 
    x2: int
    y2: int
    confidence: float = Field(..., description="Detection confidence score")

class FrameDetection(BaseModel):
    """Detections for a single frame in a video."""
    frame: int
    bottles: int
    locations: List[BoundingBox]

class DetectionResult(BaseModel):
    """Result of image or video detection processing."""
    success: bool = True
    bottles_detected: int = Field(..., description="Total number of bottles detected")
    bottle_locations: Optional[List[BoundingBox]] = Field(None, description="Bounding boxes for image detections")
    bottle_frames: Optional[List[FrameDetection]] = Field(None, description="Frame-by-frame detections for video")
    points_earned: int = Field(..., description="Points earned from this upload")
    total_points: int = Field(..., description="Total accumulated points for the user")

class UserPoints(BaseModel):
    """User points model."""
    user_id: str
    points: int