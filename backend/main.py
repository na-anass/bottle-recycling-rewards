from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import shutil
import os
import uuid
from typing import Optional

# Import our modules
from models import DetectionResult, UserPoints
from detection import process_image, process_video
from database import get_user_points, update_user_points

# Create FastAPI app
app = FastAPI(
    title="Plastic Bottle Recycling Reward API",
    description="API for detecting plastic bottles in trash bins and rewarding users",
    version="1.0.0"
)

# Configure CORS to allow requests from the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080", "http://127.0.0.1:8080"],  # Specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure upload directory exists
os.makedirs("uploads", exist_ok=True)

@app.post("/api/upload", response_model=DetectionResult)
async def upload_media(
    file: UploadFile = File(...),
    user_id: str = Form(...)
):
    """
    Upload an image or video for plastic bottle detection.
    
    Parameters:
    - file: Image or video file
    - user_id: Unique identifier for the user
    
    Returns:
    - Detection results and points earned
    """
    # Validate file type
    if not (file.content_type.startswith('image/') or file.content_type.startswith('video/')):
        raise HTTPException(status_code=400, detail="File must be an image or video")
    
    # Create a unique filename
    file_extension = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = os.path.join("uploads", unique_filename)
    
    # Save the uploaded file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    try:
        # Process the file based on type
        if file.content_type.startswith('image/'):
            result = process_image(file_path, user_id)
        else:
            result = process_video(file_path, user_id)
        
        # Update user points
        current_points = get_user_points(user_id)
        new_points = current_points + result.points_earned
        update_user_points(user_id, new_points)
        
        # Update the result with total points
        result.total_points = new_points
        
        return result
    except Exception as e:
        # Clean up if an error occurs
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # Optionally remove the file after processing
        # Uncomment if you don't need to keep uploads
        # if os.path.exists(file_path):
        #     os.remove(file_path)
        pass

@app.get("/api/user/points/{user_id}", response_model=UserPoints)
async def get_points(user_id: str):
    """
    Get the total points for a user.
    
    Parameters:
    - user_id: Unique identifier for the user
    
    Returns:
    - User ID and total points
    """
    points = get_user_points(user_id)
    return UserPoints(user_id=user_id, points=points)

@app.get("/")
async def root():
    """API root endpoint."""
    return {"message": "Welcome to the Plastic Bottle Recycling Reward API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)