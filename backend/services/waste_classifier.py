import os
import threading
from config import Config

class WasteClassifier:
    """Loads a genuine Hugging Face image classifier once; no fallback guesses."""
    def __init__(self):
        self.model = None
        self.processor = None
        self.error = None
        self.lock = threading.Lock()
        self.model_id = Config.MODEL_ID
        if Config.MODEL_ENABLED:
            self._load()
        else:
            self.error = "Model loading is disabled by MODEL_ENABLED."

    def _load(self):
        try:
            os.environ.setdefault("HF_HOME", Config.MODEL_CACHE)
            os.environ.setdefault("HF_HUB_DISABLE_XET", "1")
            os.environ.setdefault("HF_HUB_DOWNLOAD_TIMEOUT", "30")
            os.environ.setdefault("HF_HUB_ETAG_TIMEOUT", "10")
            from transformers import AutoImageProcessor, AutoModelForImageClassification
            self.processor = AutoImageProcessor.from_pretrained(self.model_id)
            self.model = AutoModelForImageClassification.from_pretrained(self.model_id)
            self.model.eval()
            self.error = None
        except Exception as exc:
            self.model = self.processor = None
            self.error = f"Could not load model {self.model_id}: {type(exc).__name__}. Check dependencies and network/model cache."

    def status(self):
        return {"ready": self.model is not None, "id": self.model_id, "error": self.error}

    def predict(self, image):
        if self.model is None:
            raise RuntimeError("The AI model is not ready. Install backend dependencies and allow the model weights to download, then restart the backend.")
        import torch
        try:
            with self.lock, torch.no_grad():
                inputs = self.processor(images=image, return_tensors="pt")
                logits = self.model(**inputs).logits
                probabilities = torch.softmax(logits, dim=-1)[0]
                index = int(probabilities.argmax().item())
                label = self.model.config.id2label.get(index, self.model.config.id2label.get(str(index)))
                if not label:
                    raise RuntimeError("Model has no label for its predicted class.")
                confidence = float(probabilities[index].item())
        except Exception as exc:
            raise RuntimeError("Image analysis failed. Try a clearer, well-lit photo of one item.") from exc
        return {"category": label, "confidence": confidence, "model": self.model_id, "inference": "image-classification"}

classifier = WasteClassifier()
