
import os
import numpy as np
from PIL import Image
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.mobilenet_v2 import (
    preprocess_input
)

# Location of your trained waste classification model
MODEL_PATH = os.path.join(
    os.path.dirname(__file__),
    "waste_model.keras"
)

# These labels MUST match the class order used during training.
# Update them to match your actual dataset.
CLASS_NAMES = [
    "cardboard",
    "glass",
    "metal",
    "paper",
    "plastic",
    "trash"
]

_model = None


def load_waste_model():
    """Load the trained model only when first needed."""
    global _model

    if _model is None:
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(
                f"Trained model not found: {MODEL_PATH}. "
                "Train the waste classifier and save it as "
                "'waste_model.keras'."
            )

        _model = load_model(MODEL_PATH)

    return _model


def predict_waste(image_file):
    """
    Predict the waste category from an image file.

    Args:
        image_file: Path or file-like object containing an image.

    Returns:
        Dictionary with predicted category and confidence.
    """
    model = load_waste_model()

    # MobileNetV2 commonly uses 224 x 224 RGB images
    image = Image.open(image_file).convert("RGB")
    image = image.resize((224, 224))

    image_array = np.asarray(image, dtype=np.float32)
    image_array = np.expand_dims(image_array, axis=0)

    # Use the same preprocessing used during model training
    image_array = preprocess_input(image_array)

    predictions = model.predict(image_array, verbose=0)[0]

    if len(predictions) != len(CLASS_NAMES):
        raise ValueError(
            "Model output count does not match CLASS_NAMES. "
            "Check the model's training class order."
        )

    predicted_index = int(np.argmax(predictions))
    category = CLASS_NAMES[predicted_index]
    confidence = float(predictions[predicted_index])

    return {
        "category": category,
        "confidence": round(confidence, 4)
    }
