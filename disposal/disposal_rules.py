import json
from pathlib import Path

# Locate the JSON file in the same folder as this Python file.
DATA_FILE = Path(__file__).with_name("disposal_data.json")


# Map common waste names to the categories in the JSON dataset.
CATEGORY_ALIASES = {
    "plastic bottle": "plastic",
    "plastic container": "plastic",
    "plastic waste": "plastic",
    "paper waste": "paper",
    "newspaper": "paper",
    "cardboard box": "cardboard",
    "cardboard waste": "cardboard",
    "glass bottle": "glass",
    "glass waste": "glass",
    "metal can": "metal",
    "aluminium can": "metal",
    "aluminum can": "metal",
    "metal waste": "metal",
    "batteries": "battery",
    "battery waste": "battery",
    "e-waste": "electronic",
    "e_waste": "electronic",
    "electronic waste": "electronic",
    "electronics": "electronic",
    "mobile phone": "electronic",
    "food waste": "organic",
    "food scraps": "organic",
    "organic waste": "organic",
    "general waste": "general",
    "mixed waste": "general",
}


def test_plastic(self):
    result = get_disposal_recommendation("Plastic Bottle")
    self.assertTrue(result["success"])
    self.assertEqual(result["category"], "Plastic Waste")

def get_disposal_recommendation(category):
    """Return disposal recommendations for a waste category."""

    # Check whether a category was provided.
    if category is None:
        return {
            "success": False,
            "category": None,
            "message": "No waste category provided.",
        }

    if not isinstance(category, str) or not category.strip():
        return {
            "success": False,
            "category": None,
            "message": "Please provide a valid waste category.",
        }

    # Normalize the category name.
    category_key = category.strip().lower()

    category_key = CATEGORY_ALIASES.get(
        category_key,
        category_key.replace("-", "_").replace(" ", "_"),
    )

    # Load the JSON dataset.
    try:
        waste_data = load_disposal_data()
    except (OSError, json.JSONDecodeError) as error:
        return {
            "success": False,
            "category": category,
            "message": "Could not load disposal data.",
            "error": str(error),
        }

    # Check whether the category exists.
    if category_key not in waste_data:
        return {
            "success": False,
            "category": category,
            "message": "Unknown waste category.",
        }

    details = waste_data[category_key]

    # Batteries and electronic waste generally require special collection.
    special_facility = details.get(
        "special_facility_required",
        category_key in ("battery", "electronic"),
    )

    ordinary_bin = details.get(
        "ordinary_bin",
        False
        if category_key in ("battery", "electronic")
        else "Depends on local rules",
    )

    # Return the recommendation.
    return {
        "success": True,
        "category": details.get("display_name", category),
        "category_key": category_key,
        "waste_type": details.get("waste_type", category_key),
        "recommended_action": details.get(
            "recommended_action",
            details.get(
                "disposal_method",
                "Follow local disposal guidance.",
            ),
        ),
        "collection_route": details.get(
            "collection_route",
            details.get("bin", "Check local collection options."),
        ),
        "bin": details.get("bin", "Check local rules."),
        "ordinary_bin": ordinary_bin,
        "special_facility_required": special_facility,
        "preparation": details.get("preparation", []),
        "recyclable": details.get("recyclable"),
        "environmental_impact": details.get("environmental_impact"),
        "safety": details.get(
            "safety",
            "Follow local waste-handling guidance.",
        ),
        "icon": details.get("icon", "♻️"),
        "tips": details.get("tips", []),
    }


# Allow this file to be tested independently.
if __name__ == "__main__":
    category = input("Enter waste category: ")
    result = get_disposal_recommendation(category)

    print(json.dumps(result, indent=2, ensure_ascii=False))