const choiceContainer = document.getElementById("choice-container");
const fileUploadContainer = document.getElementById("file-upload-container");
const cameraContainer = document.getElementById("camera-container");
const chooseFileUploadBtn = document.getElementById("choose-file-upload");
const chooseCameraBtn = document.getElementById("choose-camera");

const dropZone = document.getElementById("drop-zone");
const fileInput = document.getElementById("file-input");
const dropText = document.getElementById("drop-text");
const clearBtn = document.getElementById("clear-btn");
const loadingOverlay = document.getElementById("loading-overlay");
const submitButton = document.querySelector(
  "#upload-form button[type='submit']"
);
const cancelFileUploadBtn = document.getElementById("cancel-file-upload");

const cameraFeed = document.getElementById("camera-feed");
const captureBtn = document.getElementById("capture-btn");
const closeCameraBtn = document.getElementById("close-camera-btn");

// Ensure the clear button is hidden and submit button is disabled on page load
clearBtn.hidden = true;
submitButton.disabled = true;

// Handle choice between File Upload and Camera
chooseFileUploadBtn.addEventListener("click", () => {
  choiceContainer.hidden = true;
  fileUploadContainer.hidden = false;
  cameraContainer.hidden = true;
});

chooseCameraBtn.addEventListener("click", () => {
  choiceContainer.hidden = true; // Hide the choice screen
  cameraContainer.hidden = false; // Show the camera interface
  fileUploadContainer.hidden = true; // Ensure the file upload interface is hidden
  startCamera(); // Start the camera
});

// File Upload Functionality
dropZone.addEventListener("click", () => fileInput.click());

fileInput.addEventListener("change", () => {
  if (fileInput.files.length > 0) {
    dropText.textContent = fileInput.files[0].name;
    clearBtn.hidden = false;
    submitButton.disabled = false;
  } else {
    dropText.innerHTML =
      'Drag & Drop your file here, or <span class="browse">browse</span>';
    clearBtn.hidden = true;
    submitButton.disabled = true;
  }
});

dropZone.addEventListener("dragover", (e) => {
  e.preventDefault();
  dropZone.classList.add("dragging");
});

dropZone.addEventListener("dragleave", () => {
  dropZone.classList.remove("dragging");
});

dropZone.addEventListener("drop", (e) => {
  e.preventDefault();
  dropZone.classList.remove("dragging");
  fileInput.files = e.dataTransfer.files;
  if (fileInput.files.length > 0) {
    dropText.textContent = fileInput.files[0].name;
    clearBtn.hidden = false;
    submitButton.disabled = false;
  } else {
    dropText.innerHTML =
      'Drag & Drop your file here, or <span class="browse">browse</span>';
    clearBtn.hidden = true;
    submitButton.disabled = true;
  }
});

clearBtn.addEventListener("click", (e) => {
  e.stopPropagation();
  fileInput.value = "";
  dropText.innerHTML =
    'Drag & Drop your file here, or <span class="browse">browse</span>';
  clearBtn.hidden = true;
  submitButton.disabled = true;
});

cancelFileUploadBtn.addEventListener("click", () => {
  // Reset the file input and drop zone
  fileInput.value = "";
  dropText.innerHTML =
    'Drag & Drop your file here, or <span class="browse">browse</span>';
  clearBtn.hidden = true;
  submitButton.disabled = true;

  // Hide the file upload interface and show the choice screen
  fileUploadContainer.hidden = true;
  choiceContainer.hidden = false;
});

// Camera Functionality
function startCamera() {
  if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
    console.error("getUserMedia is not supported in this browser.");
    return;
  }

  navigator.mediaDevices
    .getUserMedia({
      video: { facingMode: { ideal: "environment" } },
    })
    .then((stream) => {
      cameraFeed.srcObject = stream;
    })
    .catch((err) => {
      console.error("Error accessing the camera: ", err);
    });
}

captureBtn.addEventListener("click", () => {
  // Show the loading overlay immediately
  loadingOverlay.hidden = false;

  const canvas = document.createElement("canvas");
  canvas.width = cameraFeed.videoWidth;
  canvas.height = cameraFeed.videoHeight;
  const context = canvas.getContext("2d");
  context.drawImage(cameraFeed, 0, 0, canvas.width, canvas.height);

  // Convert the canvas image to a Blob
  canvas.toBlob((blob) => {
    const file = new File([blob], "captured-image.png", { type: "image/png" });

    // Create a FormData object and append the file
    const formData = new FormData();
    formData.append("file", file);

    fetch("/classify", {
      method: "POST",
      body: formData,
    })
      .then((response) => response.text())
      .then((html) => {
        document.body.innerHTML = html;
        if (cameraFeed.srcObject) {
          cameraFeed.srcObject.getTracks().forEach((track) => track.stop());
        }
        cameraContainer.hidden = true;
        choiceContainer.hidden = false;
      })
      .catch((error) => {
        console.error("Error:", error);
        loadingOverlay.hidden = true;
      });
  }, "image/png");
});

closeCameraBtn.addEventListener("click", () => {
  cameraFeed.srcObject.getTracks().forEach((track) => track.stop());
  cameraContainer.hidden = true;
  choiceContainer.hidden = false;
});

document.getElementById("upload-form").addEventListener("submit", (e) => {
  loadingOverlay.hidden = false;
});
