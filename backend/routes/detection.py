from flask import Blueprint, jsonify, request, current_app
from services.waste_classifier import classifier
from services.recycling_assistant import get_guidance
from utils.image_processing import read_valid_image, InvalidImage

detection_bp = Blueprint("detection", __name__)

@detection_bp.post("/detect")
def detect():
    upload = request.files.get("image")
    if upload is None:
        return jsonify({"error": "Choose an image to analyse."}), 400
    try:
        image = read_valid_image(upload, current_app.config["MAX_CONTENT_LENGTH"])
    except InvalidImage as exc:
        return jsonify({"error": str(exc)}), 400
    try:
        prediction = classifier.predict(image)
    except RuntimeError as exc:
        return jsonify({"error": str(exc)}), 503
    prediction["guidance"] = get_guidance(prediction["category"])
    return jsonify(prediction)
