# EcoVision AI

An image-based waste sorting assistant for a student hackathon demo. Upload a clear photo of one waste item to receive a category suggestion, practical sorting guidance, and an optional search for mapped recycling points near your location.

## Problem and objectives

People are often unsure which bin or collection point is right for everyday items. EcoVision AI aims to make that first decision easier by combining image classification with concise, cautious disposal guidance and nearby recycling point lookup.

## Features

- Responsive React homepage with upload, drag and drop, device camera preview, and in-browser photo capture.
- JPEG, PNG, and WebP validation in the browser and backend, 10 MB request limit, image decoding checks, and pixel-count limit.
- Real single-image classification using a Hugging Face Transformers image-classification model when weights and dependencies are available.
- Category-specific recycling, preparation, reuse, and safety advice with reminders to check local rules.
- Optional browser geolocation and nearby recycling point search through OpenStreetMap Overpass, with a random sample-city search for demos.
- Backend health endpoint reports whether the model loaded; unavailable inference returns an error instead of a guessed result.
- Pytest coverage for API validation, model error behavior, and recycling guidance.

The classifier identifies an image category, not the material composition of an object. Confidence is the model's softmax score, not a calibrated probability of correctness. Recommendations are general guidance, not a guarantee that a local facility accepts an item.

## Technologies

React 18, Vite, JavaScript, CSS, Python, Flask, Flask-CORS, Pillow, Requests, PyTorch, Transformers, pytest, Hugging Face Hub, and OpenStreetMap Overpass.

## Architecture

```text
Browser (React/Vite :5173)
  ├─ POST /api/detect ──> Flask :5000 ──> Pillow validation ──> Transformers model
  ├─ GET /api/health ───> model readiness status
  └─ GET /api/recycling/nearby ──> OpenStreetMap Overpass
       category guidance is served locally by Flask
```

## Project structure

```text
EcoVision-AI/
├── backend/
│   ├── app.py, config.py, requirements.txt
│   ├── routes/ (detection.py, recycling.py)
│   ├── services/ (waste_classifier.py, recycling_assistant.py)
│   ├── utils/image_processing.py
│   └── uploads/.gitkeep
├── frontend/
│   ├── index.html, package.json, vite.config.js
│   └── src/ (App.jsx, index.css, components/, services/)
├── models/README.md
├── tests/ (test_detection.py, test_recycling.py)
├── docs/demo-guide.md
├── .env.example
├── .gitignore
├── README.md
└── start.bat
```

## Prerequisites (Windows)

- Python 3.10 or newer; Python 3.11 is a good default.
- Node.js 18 or newer and npm.
- Internet access for the first model download and optional Overpass nearby search.
- Several GB of free disk space may be needed for PyTorch and model cache. CPU inference works but may take time. Install a hardware-specific PyTorch build only if you have a compatible GPU and know its CUDA requirements.

## Install

Open PowerShell in the project root.

```powershell
py -3 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r backend\requirements.txt
cd frontend
npm install
Copy-Item ..\.env.example .env
cd ..
```

If PowerShell blocks activation, either use `Set-ExecutionPolicy -Scope Process Bypass` for that terminal, or run `.venv\Scripts\python.exe` directly without activating.

## Model and configuration

Default model: [`watersplash/waste-classification`](https://huggingface.co/watersplash/waste-classification). Its Hugging Face model card describes a ViT image classifier, links to the author's GitHub repository, lists 12 target labels, and says its training data is the Kaggle Garbage Classification dataset. The card reports 98% accuracy; this project has not independently verified that figure, the evaluation setup, or the model's redistribution license. Review the upstream model card, source repository, and dataset terms before redistribution or public deployment. Model files download into the ignored `models/cache/` folder on first startup by default; override this with `HF_HOME` if desired.

To configure, copy `backend\.env.example` to `backend\.env` and set variables before launching (or export them in the shell):

```text
MODEL_ID=watersplash/waste-classification
MODEL_ENABLED=true
CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
OVERPASS_URL=https://overpass-api.de/api/interpreter
```

The backend currently reads operating-system environment variables; it does not automatically load `.env` files. Set variables in PowerShell with `$env:MODEL_ID="watersplash/waste-classification"`. The frontend reads `VITE_API_BASE_URL` from `frontend/.env`; the example sets `http://localhost:5000/api`.

Health check: `http://localhost:5000/api/health`. The model is ready only when the JSON property `model.ready` is `true`. First load requires network access to Hugging Face. If a proxy, firewall, package compatibility issue, or upstream model problem prevents loading, the API accurately remains unavailable.

## Run

Start backend in a PowerShell terminal from the project root:

```powershell
.venv\Scripts\Activate.ps1
python backend\app.py
```

Start frontend in a second terminal:

```powershell
cd frontend
npm run dev
```

Open **http://localhost:5173**. Backend health is at **http://localhost:5000/api/health**. You may also run `start.bat` after installing both sets of dependencies; it opens two visible terminals and keeps their errors visible.

## API

All responses are JSON.

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/api/health` | Backend and model readiness |
| POST | `/api/detect` | Multipart form with an `image` file |
| GET | `/api/recycling/<category>` | General sorting guide for a supported category |
| GET | `/api/recycling/nearby?lat=...&lon=...` | Recycling points within a radius (default 10 km, max 25 km) |

Example upload from PowerShell:

```powershell
curl.exe -F "image=@C:\path\to\bottle.jpg" http://localhost:5000/api/detect
```

Successful detection returns `category`, `confidence`, `model`, `inference`, and `guidance`. Missing or invalid files return 400, too-large uploads 413, unavailable model 503, unknown guidance category 404, and upstream nearby lookup failures 502. Images are decoded in memory and are not saved by the application.

## How recommendations and nearby results work

Guidance is a local curated mapping keyed by the model's category labels. It covers likely recyclability, basic preparation, reuse, and where relevant safety. Because a photo cannot reliably reveal resin, coatings, contamination, or local collection rules, advice remains provisional. Nearby points come from OpenStreetMap's Overpass API based on explicit browser geolocation permission. Results may be incomplete or stale; verify the facility and accepted materials before travelling. OpenStreetMap data is © OpenStreetMap contributors.

## Tests and build

From the project root:

```powershell
.venv\Scripts\python -m pytest -q
cd frontend
npm run build
```

The successful inference route is tested with a mocked classifier so backend tests do not need model weights. This checks integration and response shape, not model accuracy. The model-unavailable response is separately tested. The frontend production build checks bundling, not runtime API connectivity.

## Common issues

- **`Model is not ready`:** install requirements, verify internet access, restart the backend, then check `/api/health`. Model files download on first use.
- **Torch installation errors:** follow the official PyTorch install selector for your Python version and hardware, then reinstall other requirements.
- **Frontend cannot reach backend:** keep Flask running at port 5000 and check `frontend/.env` and the browser console.
- **CORS error:** add the exact frontend origin to `CORS_ORIGINS` and restart Flask.
- **Upload rejected:** use valid JPEG/PNG/WebP under 10 MB and no more than 25 million pixels.
- **No nearby results:** allow location permission, verify internet access, retry later, or open OpenStreetMap and search manually.
- **Port already in use:** stop the other process or edit the relevant startup port and API URL consistently.

## Limitations, safety, and privacy

- This is image classification for one dominant item; it does not locate multiple objects or inspect hidden material composition.
- Confidence is a raw model score and may be overconfident or wrong, especially for blurry images, unfamiliar packaging, and mixed materials.
- The upstream model card's accuracy statement is not independently audited here. Its license was not stated in the inspected model card; verify current upstream terms before redistribution.
- Recycling instructions are not jurisdiction-specific. Use local council/facility rules for the final decision.
- Nearby locations depend on browser permission, internet access, Overpass service availability, and mapped OpenStreetMap coverage.
- Uploads are processed in memory and not retained by this app. The nearby lookup sends coordinates to the configured Overpass endpoint. Avoid uploading sensitive images.
- No API credentials or database are required.

## Hackathon judge demo

1. Start both services and open `http://localhost:5173`.
2. Confirm `/api/health` reports `model.ready: true` before claiming live inference.
3. Upload a clear example from the supported categories and show the returned label, score, and guide.
4. Use location access to show mapped recycling points, if available.
5. Explain uncertainty and that local rules are authoritative.

Short presentation script: “EcoVision AI helps people make a better first decision about everyday waste. The user photographs one item, our image classifier suggests a category, and the app pairs that with practical preparation guidance and nearby mapped recycling points. The result is a helpful starting point, not a material test, and we direct people to local facility rules for the final decision.”

## Future improvements

- Test and calibrate the model on a documented, representative dataset.
- Add local council rule datasets and facility-specific accepted material lists.
- Improve location search with filters, distance calculations, and facility hours.
- Add optional offline model setup and multilingual guidance.
- Add an explicit human correction flow and privacy-preserving feedback process.
