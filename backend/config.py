import os

class Config:
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173").split(",")
    MODEL_ID = os.getenv("MODEL_ID", "watersplash/waste-classification")
    MODEL_ENABLED = os.getenv("MODEL_ENABLED", "true").lower() == "true"
    MODEL_CACHE = os.getenv("HF_HOME", os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "models", "cache")))
    OVERPASS_URL = os.getenv("OVERPASS_URL", "https://overpass-api.de/api/interpreter")
