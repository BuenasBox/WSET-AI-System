"""
SAT Wine Loader — Discovery and loading of training wines
Provides access to wine inventory and individual wine records
"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Any


WINE_DIR = Path(__file__).parent.parent / "knowledge" / "sat-framework" / "wines"
INVENTORY_FILE = WINE_DIR / "wine_inventory_v1.json"


def load_wine_inventory() -> Dict[str, Any]:
    """Load the master wine inventory."""
    if not INVENTORY_FILE.exists():
        raise FileNotFoundError(f"Wine inventory not found: {INVENTORY_FILE}")

    with open(INVENTORY_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def load_wine_by_id(wine_id: str) -> Optional[Dict[str, Any]]:
    """Load a single wine by its ID (e.g., SAT_WINE_001)."""
    inventory = load_wine_inventory()

    # Find wine record in inventory
    wine_record = None
    for wine in inventory.get("wines", []):
        if wine["wine_id"] == wine_id:
            wine_record = wine
            break

    if not wine_record:
        return None

    # Load wine file
    wine_file = WINE_DIR / wine_record["file"]
    if not wine_file.exists():
        return None

    with open(wine_file, "r", encoding="utf-8") as f:
        return json.load(f)


def load_all_wines() -> List[Dict[str, Any]]:
    """Load all wines."""
    inventory = load_wine_inventory()
    wines = []

    for wine_record in inventory.get("wines", []):
        wine = load_wine_by_id(wine_record["wine_id"])
        if wine:
            wines.append(wine)

    return wines


def get_wines_by_priority(priority: int) -> List[Dict[str, Any]]:
    """Get all wines of a specific priority level."""
    inventory = load_wine_inventory()
    wines = []

    for wine_record in inventory.get("wines", []):
        if wine_record["priority"] == priority:
            wine = load_wine_by_id(wine_record["wine_id"])
            if wine:
                wines.append(wine)

    return wines


def get_wines_by_grape(grape_variety: str) -> List[Dict[str, Any]]:
    """Get all wines of a specific grape variety."""
    inventory = load_wine_inventory()
    wines = []

    grape_lower = grape_variety.lower()
    for wine_record in inventory.get("wines", []):
        if grape_lower in wine_record["grape_variety"].lower():
            wine = load_wine_by_id(wine_record["wine_id"])
            if wine:
                wines.append(wine)

    return wines


def get_wines_by_examination_value(value: str) -> List[Dict[str, Any]]:
    """Get wines by examination value (Very High, High, Medium-High)."""
    inventory = load_wine_inventory()
    wines = []

    for wine_record in inventory.get("wines", []):
        if wine_record["examination_value"] == value:
            wine = load_wine_by_id(wine_record["wine_id"])
            if wine:
                wines.append(wine)

    return wines


def get_inventory_summary() -> Dict[str, Any]:
    """Get summary statistics about the wine inventory."""
    inventory = load_wine_inventory()
    wines = inventory.get("wines", [])

    priority_counts = {1: 0, 2: 0, 3: 0}
    exam_counts = {}
    grapes = set()
    countries = set()

    for wine in wines:
        priority_counts[wine["priority"]] += 1
        exam_value = wine["examination_value"]
        exam_counts[exam_value] = exam_counts.get(exam_value, 0) + 1
        grapes.add(wine["grape_variety"])
        countries.add(wine["country"])

    return {
        "total_wines": len(wines),
        "wines_by_priority": priority_counts,
        "wines_by_examination_value": exam_counts,
        "unique_grapes": len(grapes),
        "grape_varieties": sorted(grapes),
        "unique_countries": len(countries),
        "countries": sorted(countries)
    }


if __name__ == "__main__":
    # CLI usage for debugging
    print("SAT Wine Loader — Inventory Summary")
    print("=" * 50)

    try:
        summary = get_inventory_summary()
        print(f"Total Wines: {summary['total_wines']}")
        print(f"By Priority: {summary['wines_by_priority']}")
        print(f"By Examination Value: {summary['wines_by_examination_value']}")
        print(f"Unique Grapes: {summary['unique_grapes']}")
        print(f"Unique Countries: {summary['unique_countries']}")

        print("\nFirst Wine Sample:")
        wine = load_wine_by_id("SAT_WINE_001")
        if wine:
            print(f"  ID: {wine['id']}")
            print(f"  Variety: {wine['grape_variety']}")
            print(f"  Region: {wine['region']}")
            print(f"  Examination Value: {wine['examination_value']}")
    except Exception as e:
        print(f"Error: {e}")
