# Plastic Bottle Recycling Reward API Documentation

## Base URL
`<BASE_URL>`

## Authentication
This demo implementation uses a simple user ID parameter. In a production environment, you would implement proper authentication (OAuth, JWT, etc.).

## Endpoints

### Upload Media for Detection
Uploads an image or video file for plastic bottle detection and rewards calculation.

**URL**: `/api/upload`  
**Method**: `POST`  
**Content-Type**: `multipart/form-data`

**Parameters**:
- `file` (required): The image or video file to process
- `user_id` (required): Unique identifier for the user

**Response**:
```json
{
  "success": true,
  "bottles_detected": 2,
  "bottle_locations": [
    {
      "x1": 120,
      "y1": 240,
      "x2": 180,
      "y2": 350,
      "confidence": 0.92
    },
    {
      "x1": 300,
      "y1": 220,
      "x2": 360,
      "y2": 340,
      "confidence": 0.85
    }
  ],
  "points_earned": 20,
  "total_points": 120
}
```

For video files, the response includes `bottle_frames` instead of `bottle_locations`:
```json
{
  "success": true,
  "bottles_detected": 5,
  "bottle_frames": [
    {
      "frame": 10,
      "bottles": 2,
      "locations": [
        {
          "x1": 120,
          "y1": 240,
          "x2": 180,
          "y2": 350,
          "confidence": 0.89
        },
        {
          "x1": 300,
          "y1": 220,
          "x2": 360,
          "y2": 340,
          "confidence": 0.76
        }
      ]
    },
    {
      "frame": 20,
      "bottles": 3,
      "locations": [
        /* ... */
      ]
    }
  ],
  "points_earned": 10,
  "total_points": 130
}
```

**Error Response**:
```json
{
  "detail": "Error message"
}
```

### Get User Points
Retrieves the total points for a user.

**URL**: `/api/user/points/{user_id}`  
**Method**: `GET`  

**URL Parameters**:
- `user_id` (required): Unique identifier for the user

**Response**:
```json
{
  "user_id": "user_1234",
  "points": 120
}
```

**Error Response**:
```json
{
  "detail": "Error message"
}
```

## Data Models

### BoundingBox
```json
{
  "x1": 120,       // Left coordinate
  "y1": 240,       // Top coordinate
  "x2": 180,       // Right coordinate
  "y2": 350,       // Bottom coordinate
  "confidence": 0.92  // Detection confidence score (0-1)
}
```

### FrameDetection
```json
{
  "frame": 10,     // Frame number in the video
  "bottles": 2,    // Number of bottles detected in this frame
  "locations": []  // Array of BoundingBox objects
}
```

### DetectionResult
```json
{
  "success": true,           // Whether processing succeeded
  "bottles_detected": 2,     // Total number of bottles detected
  "bottle_locations": [],    // Array of BoundingBox objects (for images)
  "bottle_frames": [],       // Array of FrameDetection objects (for videos)
  "points_earned": 20,       // Points earned from this detection
  "total_points": 120        // Total points for the user
}
```

### UserPoints
```json
{
  "user_id": "user_1234",  // User identifier
  "points": 120            // Total points
}
```

## Notes

1. Image processing awards 10 points per detected bottle
2. Video processing awards 5 points per unique frame containing bottles
