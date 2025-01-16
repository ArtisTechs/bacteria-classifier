const dropZone = document.getElementById("drop-zone");
const fileInput = document.getElementById("file-input");
const dropText = document.getElementById("drop-text");
const clearBtn = document.getElementById("clear-btn");
const loadingOverlay = document.getElementById("loading-overlay");
const submitButton = document.querySelector("button[type='submit']"); // Get the Classify button

// Ensure the clear button is hidden and submit button is disabled on page load
clearBtn.hidden = true;
submitButton.disabled = true; // Disable the submit button initially

// Handle click to open file dialog
dropZone.addEventListener("click", () => fileInput.click());

// Update drop zone text and toggle button state on file selection
fileInput.addEventListener("change", () => {
  if (fileInput.files.length > 0) {
    dropText.textContent = fileInput.files[0].name;
    clearBtn.hidden = false; // Show the clear button
    submitButton.disabled = false; // Enable the submit button
  } else {
    dropText.innerHTML =
      'Drag & Drop your file here, or <span class="browse">browse</span>';
    clearBtn.hidden = true; // Hide the clear button
    submitButton.disabled = true; // Disable the submit button
  }
});

// Drag and drop functionality
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
    clearBtn.hidden = false; // Show the clear button
    submitButton.disabled = false; // Enable the submit button
  } else {
    dropText.innerHTML =
      'Drag & Drop your file here, or <span class="browse">browse</span>';
    clearBtn.hidden = true; // Hide the clear button
    submitButton.disabled = true; // Disable the submit button
  }
});

// Clear the file input and reset the drop zone
clearBtn.addEventListener("click", (e) => {
  e.stopPropagation();
  fileInput.value = ""; // Clear the file input
  dropText.innerHTML =
    'Drag & Drop your file here, or <span class="browse">browse</span>';
  clearBtn.hidden = true;
  submitButton.disabled = true;
});

document.getElementById("upload-form").addEventListener("submit", (e) => {
  loadingOverlay.style.display = "flex";
  setTimeout(() => {
    loadingOverlay.style.display = "none";
  }, 3000);
});
