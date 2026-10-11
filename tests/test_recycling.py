import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "backend"))
from app import create_app
from routes import recycling as recycling_routes

def test_supported_recycling_categories():
    client = create_app({"TESTING": True}).test_client()
    for category in ("paper", "plastic", "battery", "biological"):
        response = client.get(f"/api/recycling/{category}")
        assert response.status_code == 200
        assert response.json["title"]
        assert response.json["steps"]

def test_invalid_recycling_category():
    response = create_app({"TESTING": True}).test_client().get("/api/recycling/unobtainium")
    assert response.status_code == 404

def test_nearby_requires_coordinates():
    response = create_app({"TESTING": True}).test_client().get("/api/recycling/nearby")
    assert response.status_code == 400

def test_nearby_rejects_invalid_coordinates():
    response = create_app({"TESTING": True}).test_client().get("/api/recycling/nearby?lat=95&lon=0")
    assert response.status_code == 400

def test_nearby_returns_points_sorted_by_distance(monkeypatch):
    class Response:
        def raise_for_status(self): pass
        def json(self):
            return {"elements": [
                {"type": "node", "lat": 12.01, "lon": 77.0, "tags": {"name": "Far point", "amenity": "recycling"}},
                {"type": "node", "lat": 12.001, "lon": 77.0, "tags": {"name": "Near point", "amenity": "recycling"}},
            ]}
    monkeypatch.setattr(recycling_routes.requests, "post", lambda *args, **kwargs: Response())
    response = create_app({"TESTING": True}).test_client().get("/api/recycling/nearby?lat=12&lon=77")
    assert response.status_code == 200
    assert response.json["centers"][0]["name"] == "Near point"
    assert response.json["centers"][0]["distance_m"] < response.json["centers"][1]["distance_m"]
