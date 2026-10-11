from io import BytesIO
from PIL import Image
import pytest
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "backend"))
from app import create_app
import services.waste_classifier as waste_classifier

@pytest.fixture
def client():
    return create_app({"TESTING": True}).test_client()

def image_bytes():
    image = Image.new("RGB", (16, 16), "green")
    stream = BytesIO()
    image.save(stream, format="PNG")
    return stream.getvalue()

def test_health_reports_model_status(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json["status"] == "ok"
    assert "ready" in response.json["model"]

def test_missing_image(client):
    response = client.post("/api/detect")
    assert response.status_code == 400
    assert "image" in response.json["error"].lower()

def test_invalid_image_content(client):
    response = client.post("/api/detect", data={"image": (BytesIO(b"not an image"), "photo.png")}, content_type="multipart/form-data")
    assert response.status_code == 400
    assert "valid image" in response.json["error"].lower()

def test_valid_image_is_preprocessed_and_mock_inference(client, monkeypatch):
    def prediction(_image):
        return {"category": "plastic", "confidence": 0.82, "model": "test-model", "inference": "image-classification"}
    monkeypatch.setattr(waste_classifier.classifier, "predict", prediction)
    response = client.post("/api/detect", data={"image": (BytesIO(image_bytes()), "photo.png")}, content_type="multipart/form-data")
    assert response.status_code == 200
    assert response.json["category"] == "plastic"
    assert response.json["confidence"] == 0.82
    assert response.json["guidance"]["title"] == "Plastic"

def test_model_unavailable_returns_503(client, monkeypatch):
    def unavailable(_image): raise RuntimeError("Model unavailable")
    monkeypatch.setattr(waste_classifier.classifier, "predict", unavailable)
    response = client.post("/api/detect", data={"image": (BytesIO(image_bytes()), "photo.png")}, content_type="multipart/form-data")
    assert response.status_code == 503

def test_oversized_upload_rejected(client):
    response = client.post("/api/detect", data={"image": (BytesIO(b"x" * (10 * 1024 * 1024 + 1)), "big.png")}, content_type="multipart/form-data")
    assert response.status_code == 413
