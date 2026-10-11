import math
import requests
from flask import Blueprint, jsonify, request, current_app
from services.recycling_assistant import get_guidance, CATEGORIES

recycling_bp = Blueprint("recycling", __name__)

@recycling_bp.get("/recycling/<category>")
def guidance(category):
    result = get_guidance(category)
    if result is None:
        return jsonify({"error": "Unsupported waste category."}), 404
    return jsonify(result)

@recycling_bp.get("/recycling/nearby")
def nearby():
    try:
        lat, lon = float(request.args["lat"]), float(request.args["lon"])
        radius = min(max(int(request.args.get("radius", 10000)), 500), 25000)
    except (KeyError, ValueError, TypeError):
        return jsonify({"error": "Provide valid latitude and longitude."}), 400
    if not (-90 <= lat <= 90 and -180 <= lon <= 180):
        return jsonify({"error": "Coordinates are outside valid ranges."}), 400
    query = f"[out:json][timeout:15];(node(around:{radius},{lat},{lon})[amenity=recycling];way(around:{radius},{lat},{lon})[amenity=recycling];relation(around:{radius},{lat},{lon})[amenity=recycling];node(around:{radius},{lat},{lon})[recycling];way(around:{radius},{lat},{lon})[recycling];);out center tags;"
    try:
        response = requests.post(current_app.config["OVERPASS_URL"], data={"data": query}, timeout=20, headers={"User-Agent": "EcoVisionAI/1.0 student project"})
        response.raise_for_status()
        places = response.json().get("elements", [])
    except (requests.RequestException, ValueError):
        return jsonify({"error": "Nearby search is temporarily unavailable. Try the OpenStreetMap link instead."}), 502
    centers = []
    for place in places:
        tags = place.get("tags", {})
        point = place.get("center", place)
        point_lat, point_lon = point.get("lat"), point.get("lon")
        if point_lat is None or point_lon is None: continue
        dlat, dlon = math.radians(point_lat - lat), math.radians(point_lon - lon)
        a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat)) * math.cos(math.radians(point_lat)) * math.sin(dlon / 2) ** 2
        distance = int(6371000 * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a)))
        centers.append({"name": tags.get("name", tags.get("operator", "Recycling point")), "type": tags.get("recycling", "recycling"), "lat": point_lat, "lon": point_lon, "distance_m": distance, "address": ", ".join(filter(None, [tags.get("addr:street"), tags.get("addr:city")]))})
    centers.sort(key=lambda center: center["distance_m"])
    centers = centers[:30]
    return jsonify({"centers": centers, "count": len(centers), "source": "OpenStreetMap contributors", "radius_m": radius})
