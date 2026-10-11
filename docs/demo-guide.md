# EcoVision AI demo guide

## Start

From the project root, run `start.bat`, or start two terminals manually as shown in the root README. Open `http://localhost:5173`.

## Check the services

Open `http://localhost:5000/api/health`. A successful backend responds with `status: "ok"`; genuine inference is ready only if `model.ready` is `true`. The frontend header area also shows whether the backend and model are available.

## Demo sequence

1. Pick one item with a clear background and good light.
2. In **What are you throwing away?**, choose or take a JPEG, PNG, or WebP photo under 10 MB.
3. Select **Identify this item** and wait for the category and model confidence.
4. Read the category-specific disposal and preparation tips; note that local rules can differ.
5. Select **Use my location** and allow location access to list OpenStreetMap recycling points, or use **Pick a random city** to search a sample urban area.
6. Explain that this is image classification of one image, not object detection or material verification.

## Suitable sample categories

Use examples from the actual model card labels: battery, biological waste, cardboard, clothing, glass (green/white), metal, paper, plastic, and general trash. It also lists brown-grass and shoes. The displayed labels may use the model author's naming. Model performance on your photos is not independently verified here.

## Recovery

- If the model is not ready, make sure packages are installed and the computer can reach Hugging Face; restart the backend and wait for model loading.
- If the backend is offline, start it in its own terminal and read any startup error.
- If nearby lookup fails, allow location access or open OpenStreetMap manually and search for recycling points.
- If the photo is rejected, use a JPEG, PNG, or WebP below 10 MB.

## What is real or dependent

- Upload validation and backend image preprocessing are implemented.
- Classification is real Transformers inference when the configured model weights load. It is not simulated. It was not possible to verify genuine inference in this initial environment because dependencies and weights were absent.
- Recycling guidance is curated static advice and includes local-rule caveats; it does not come from a municipal authority.
- Nearby results are fetched from OpenStreetMap's Overpass service and depend on internet access, browser geolocation permission, and map coverage. Sample city searches still use live map data; they do not create fake center records.

## Backup presentation

If live inference cannot run, present the homepage, explain the intended end-to-end workflow, show `/api/health` accurately, and walk through the documented model classes and static recycling guidance. Do not show a fabricated prediction or claim that AI inference succeeded.
