
const imageInput = document.getElementById("waste-image");
const preview = document.getElementById("image-preview");
const identifyBtn = document.getElementById("identify-btn");
const cameraBtn = document.getElementById("camera-btn");
const statusMessage = document.getElementById("status-message");

let selectedImage = null;

// Display the selected image
imageInput.addEventListener("change", function () {
    const file = imageInput.files[0];

    if (!file) return;

    if (!file.type.startsWith("image/")) {
        statusMessage.textContent = "Please select a valid image.";
        return;
    }

    selectedImage = file;

    const imageURL = URL.createObjectURL(file);

    preview.replaceChildren();

    const image = document.createElement("img");
    image.src = imageURL;
    image.alt = "Selected waste image";

    preview.appendChild(image);

    identifyBtn.disabled = false;
    statusMessage.textContent =
        "Image selected successfully! Ready for identification.";
});



// Placeholder until the AI backend is connected
identifyBtn.addEventListener("click", function () {
    if (!selectedImage) return;

    statusMessage.textContent =
        "Image ready! AI classification will be connected in the next step.";
});

const cameraContainer = document.getElementById("camera-container");
const cameraVideo = document.getElementById("camera-video");
const captureBtn = document.getElementById("capture-btn");
const closeCameraBtn = document.getElementById("close-camera-btn");
const cameraCanvas = document.getElementById("camera-canvas");

let cameraStream = null;

cameraBtn.addEventListener("click", async function () {
    try {
        if (!navigator.mediaDevices?.getUserMedia) {
            statusMessage.textContent =
                "Camera unavailable. Please use Live Server or HTTPS.";
            return;
        }

        cameraStream = await navigator.mediaDevices.getUserMedia({
            video: { facingMode: "environment" },
            audio: false
        });

        cameraVideo.srcObject = cameraStream;
        cameraContainer.hidden = false;
        statusMessage.textContent = "Camera opened successfully!";
    } catch (error) {
        statusMessage.textContent =
            "Camera access failed. Allow permission or use Choose Image.";
    }
});

captureBtn.addEventListener("click", function () {
    if (!cameraStream || !cameraVideo.videoWidth) {
        statusMessage.textContent = "Please wait for the camera to start.";
        return;
    }

    cameraCanvas.width = cameraVideo.videoWidth;
    cameraCanvas.height = cameraVideo.videoHeight;

    const context = cameraCanvas.getContext("2d");
    context.drawImage(
        cameraVideo,
        0,
        0,
        cameraCanvas.width,
        cameraCanvas.height
    );

    cameraCanvas.toBlob(function (blob) {
        if (!blob) {
            statusMessage.textContent = "Photo capture failed.";
            return;
        }

        selectedImage = new File(
            [blob],
            "waste-photo.jpg",
            { type: "image/jpeg" }
        );

        imageInput.value = "";

        preview.replaceChildren();

        const image = document.createElement("img");
        image.src = URL.createObjectURL(blob);
        image.alt = "Captured waste photo";
        preview.appendChild(image);

        identifyBtn.disabled = false;
        statusMessage.textContent =
            "Photo captured! Ready for identification.";

        stopCamera();
    }, "image/jpeg", 0.9);
});

function stopCamera() {
    if (cameraStream) {
        cameraStream.getTracks().forEach(track => track.stop());
        cameraStream = null;
    }

    cameraVideo.srcObject = null;
    cameraContainer.hidden = true;
}

closeCameraBtn.addEventListener("click", function () {
    stopCamera();
    statusMessage.textContent = "Camera closed.";
});

window.addEventListener("pagehide", stopCamera);