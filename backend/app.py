from flask import Flask, jsonify
from flask_cors import CORS
from config import Config
from routes.detection import detection_bp
from routes.recycling import recycling_bp
from services.waste_classifier import classifier

def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_object(Config)
    if test_config:
        app.config.update(test_config)
    CORS(app, resources={r"/api/*": {"origins": app.config["CORS_ORIGINS"]}})
    app.register_blueprint(detection_bp, url_prefix="/api")
    app.register_blueprint(recycling_bp, url_prefix="/api")

    @app.get("/api/health")
    def health():
        return jsonify({"status": "ok", "model": classifier.status(), "nearby_search": "OpenStreetMap Overpass"})

    @app.errorhandler(413)
    def too_large(_error):
        return jsonify({"error": "Image is too large. Choose an image under 10 MB."}), 413
    return app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
