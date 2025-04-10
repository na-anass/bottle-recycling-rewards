// Configuration
const API_URL = "http://localhost:8000/api"; // FastAPI backend URL

// Generate a random user ID for this demo (in a real app, use authentication)
const userId = "user_" + Math.floor(Math.random() * 10000).toString();
console.log(`Using demo user ID: ${userId}`);

// DOM elements
let uploadContainer,
  fileInput,
  preview,
  videoPreview,
  previewContainer,
  processing,
  results,
  bottlesDetected,
  pointsEarned,
  totalPoints,
  progressBar;

// Initialize the app
document.addEventListener("DOMContentLoaded", function () {
  // Get all DOM elements
  uploadContainer = document.getElementById("upload-container");
  fileInput = document.getElementById("file-input");
  preview = document.getElementById("preview");
  videoPreview = document.getElementById("video-preview");
  previewContainer = document.getElementById("preview-container");
  processing = document.getElementById("processing");
  results = document.getElementById("results");
  bottlesDetected = document.getElementById("bottles-detected");
  pointsEarned = document.getElementById("points-earned");
  totalPoints = document.getElementById("total-points");
  progressBar = document.getElementById("progress-bar");

  // Hide elements initially
  preview.style.display = "none";
  videoPreview.style.display = "none";
  processing.style.display = "none";
  results.style.display = "none";

  // Set up event listeners
  setupDragAndDrop();
  setupFileInput();

  // Load initial user points
  fetchUserPoints();
});

// Set up drag and drop functionality
function setupDragAndDrop() {
  uploadContainer.addEventListener("dragover", (e) => {
    e.preventDefault();
    uploadContainer.classList.add("drag-active");
  });

  uploadContainer.addEventListener("dragleave", () => {
    uploadContainer.classList.remove("drag-active");
  });

  uploadContainer.addEventListener("drop", (e) => {
    e.preventDefault();
    uploadContainer.classList.remove("drag-active");

    if (e.dataTransfer.files.length) {
      handleFile(e.dataTransfer.files[0]);
    }
  });

  // Click to upload
  uploadContainer.addEventListener("click", () => {
    fileInput.click();
  });
}

// Set up file input
function setupFileInput() {
  fileInput.addEventListener("change", (e) => {
    if (e.target.files.length) {
      handleFile(e.target.files[0]);
    }
  });
}

// Handle the selected file
function handleFile(file) {
  // Clear previous detection boxes
  clearDetectionBoxes();

  // Check if it's an image or video
  if (file.type.startsWith("image/")) {
    preview.style.display = "block";
    videoPreview.style.display = "none";

    const reader = new FileReader();
    reader.onload = (e) => {
      preview.src = e.target.result;
    };
    reader.readAsDataURL(file);
  } else if (file.type.startsWith("video/")) {
    preview.style.display = "none";
    videoPreview.style.display = "block";

    const url = URL.createObjectURL(file);
    videoPreview.src = url;
  } else {
    showError("Please upload an image or video file.");
    return;
  }

  // Show processing indicator
  processing.style.display = "block";
  results.style.display = "none";

  // Prepare form data
  const formData = new FormData();
  formData.append("file", file);
  formData.append("user_id", userId);

  // Send to API
  fetch(`${API_URL}/upload`, {
    method: "POST",
    body: formData,
  })
    .then((response) => {
      if (!response.ok) {
        return response.json().then((err) => {
          throw new Error(err.detail || "Error uploading file");
        });
      }
      return response.json();
    })
    .then((data) => {
      // Hide processing indicator
      processing.style.display = "none";

      if (data.success) {
        // Show results
        results.style.display = "block";
        bottlesDetected.textContent = `${data.bottles_detected} plastic bottle${
          data.bottles_detected !== 1 ? "s" : ""
        } detected`;
        pointsEarned.textContent = data.points_earned;
        totalPoints.textContent = data.total_points;

        // Update progress bar
        const progress = (data.total_points % 500) / 5;
        progressBar.style.width = `${progress}%`;

        // If it's an image, show detection boxes
        if (file.type.startsWith("image/") && data.bottle_locations) {
          drawDetectionBoxes(data.bottle_locations);
        }

        // Apply animation to points
        pointsEarned.classList.remove("points-animation");
        void pointsEarned.offsetWidth; // Trigger reflow
        pointsEarned.classList.add("points-animation");
      } else {
        showError("Error processing your file. Please try again.");
      }
    })
    .catch((error) => {
      console.error("Error:", error);
      processing.style.display = "none";
      showError("Error uploading file. Please try again.");
    });
}

// Fetch user points from the API
function fetchUserPoints() {
  fetch(`${API_URL}/user/points/${userId}`)
    .then((response) => {
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      return response.json();
    })
    .then((data) => {
      totalPoints.textContent = data.points;

      // Update progress bar
      const progress = (data.points % 500) / 5;
      progressBar.style.width = `${progress}%`;

      // Calculate progress toward next reward
      const pointsToNextReward = 500 - (data.points % 500);
      if (pointsToNextReward < 500) {
        const progressElement = document.querySelector(".progress + p");
        if (progressElement) {
          progressElement.textContent = `${pointsToNextReward} more points until your next reward!`;
        }
      }
    })
    .catch((error) => {
      console.error("Error fetching user points:", error);
    });
}

// Draw detection boxes on the image
function drawDetectionBoxes(locations) {
  if (!locations || locations.length === 0) return;

  const previewImg = document.getElementById("preview");

  // Make sure the image is loaded before getting dimensions
  if (!previewImg.complete) {
    previewImg.onload = () =>
      drawDetectionBoxesWithDimensions(locations, previewImg);
    return;
  }

  drawDetectionBoxesWithDimensions(locations, previewImg);
}

function drawDetectionBoxesWithDimensions(locations, previewImg) {
  // Get the actual displayed dimensions of the image
  const displayedWidth = previewImg.clientWidth;
  const displayedHeight = previewImg.clientHeight;

  // Get the natural dimensions of the image
  const naturalWidth = previewImg.naturalWidth;
  const naturalHeight = previewImg.naturalHeight;

  // Calculate scale factors
  const scaleX = displayedWidth / naturalWidth;
  const scaleY = displayedHeight / naturalHeight;

  locations.forEach((loc) => {
    const box = document.createElement("div");
    box.className = "detection-box";

    // Scale the coordinates to match the displayed image size
    const x1 = loc.x1 * scaleX;
    const y1 = loc.y1 * scaleY;
    const x2 = loc.x2 * scaleX;
    const y2 = loc.y2 * scaleY;

    box.style.left = `${x1}px`;
    box.style.top = `${y1}px`;
    box.style.width = `${x2 - x1}px`;
    box.style.height = `${y2 - y1}px`;

    // Add confidence label
    const label = document.createElement("span");
    label.textContent = `${Math.round(loc.confidence * 100)}%`;
    label.className = "confidence-label";

    box.appendChild(label);
    previewContainer.appendChild(box);
  });
}

// Clear detection boxes
function clearDetectionBoxes() {
  const boxes = document.querySelectorAll(".detection-box");
  boxes.forEach((box) => box.remove());
}

// Show error message
function showError(message) {
  alert(message);
}

// Reset the UI to allow new uploads
function resetUI() {
  // Clear detection boxes
  clearDetectionBoxes();

  // Hide results and preview
  results.style.display = "none";
  preview.style.display = "none";
  videoPreview.style.display = "none";

  // Show upload container
  uploadContainer.style.display = "block";

  // Clear file input
  fileInput.value = "";
}

// Add a reset button event listener
document.addEventListener("DOMContentLoaded", function () {
  // Add reset button if it exists
  const resetBtn = document.getElementById("reset-btn");
  if (resetBtn) {
    resetBtn.addEventListener("click", resetUI);
  }
});
