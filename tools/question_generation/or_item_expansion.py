"""Phase P2.4: Open Response Item Expansion

Creates 10-15 new curated OR items and expands lab_payload from 26 to 35-40.
Items are pedagogically diverse, covering all command verbs and core WSET topics.
"""

from __future__ import annotations

import json
import re
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
LAB_PAYLOAD_PATH = REPO_ROOT / "frontend" / "open-response-lab" / "lab_payload.js"


def load_current_payload() -> dict:
    """Load the current lab_payload."""
    content = LAB_PAYLOAD_PATH.read_text(encoding="utf-8")
    match = re.search(r"window\.OPEN_RESPONSE_LAB_PAYLOAD\s*=\s*(\{.*?\});", content, re.DOTALL)
    if not match:
        return {}
    return json.loads(match.group(1))


# Curated expansion items for P2.4
# Each represents a different command verb and core WSET topic
EXPANSION_ITEMS = [
    {
        "source_question_id": "2001",
        "stem": "Compare the climates and resulting wine styles of Sancerre (Loire Valley) and Pouilly-Fumé.",
        "topic": "Loire white wines",
        "RA": "RA2",
        "command_verb": "compare",
        "expected_concepts": ["climate", "terroir", "wine style", "Loire Valley"]
    },
    {
        "source_question_id": "2002",
        "stem": "Assess the quality of a wine that shows: pale gold color, lemon/green fruit on the nose, crisp acidity, medium body, and a clean, dry finish.",
        "topic": "wine assessment",
        "RA": "RA1",
        "command_verb": "assess",
        "expected_concepts": ["quality", "color", "aroma", "acidity", "body"]
    },
    {
        "source_question_id": "2003",
        "stem": "How does the use of whole-bunch fermentation in red wine production affect the final wine's structure and flavor profile?",
        "topic": "fermentation",
        "RA": "RA2",
        "command_verb": "how",
        "expected_concepts": ["fermentation", "structure", "tannin", "flavor"]
    },
    {
        "source_question_id": "2004",
        "stem": "Justify why small oak barrels are preferred over large oak vats for aging premium red Burgundy.",
        "topic": "oak aging",
        "RA": "RA2",
        "command_verb": "justify",
        "expected_concepts": ["oak", "aging", "oak influence", "Burgundy"]
    },
    {
        "source_question_id": "2005",
        "stem": "Evaluate the significance of vintage variation in establishing a Bordeaux wine's classification and market price.",
        "topic": "vintage",
        "RA": "RA3",
        "command_verb": "evaluate",
        "expected_concepts": ["vintage", "classification", "weather", "quality"]
    },
    {
        "source_question_id": "2006",
        "stem": "Describe the typical sensory characteristics of a premium, dry Riesling from the Mosel region.",
        "topic": "Riesling",
        "RA": "RA1",
        "command_verb": "describe",
        "expected_concepts": ["Riesling", "Mosel", "color", "aroma", "acidity", "body"]
    },
    {
        "source_question_id": "2007",
        "stem": "Why is temperature control during fermentation critical for producing white wines with preserved fruit character and lower alcohol levels?",
        "topic": "fermentation control",
        "RA": "RA2",
        "command_verb": "why",
        "expected_concepts": ["temperature", "fermentation", "alcohol", "fruit"]
    },
    {
        "source_question_id": "2008",
        "stem": "Discuss the contrasting approaches to oak use in red Bordeaux versus Burgundy, considering the influence of terroir on winemaking decisions.",
        "topic": "regional winemaking",
        "RA": "RA3",
        "command_verb": "discuss",
        "expected_concepts": ["oak", "Bordeaux", "Burgundy", "terroir", "winemaking"]
    },
    {
        "source_question_id": "2009",
        "stem": "Identify and explain the significance of malolactic fermentation in transforming the acidity and flavor profile of red wines.",
        "topic": "malolactic fermentation",
        "RA": "RA2",
        "command_verb": "identify and explain",
        "expected_concepts": ["malolactic", "acidity", "flavor", "fermentation"]
    },
    {
        "source_question_id": "2010",
        "stem": "Outline the main factors that determine the potential for aging in premium white Burgundy wines.",
        "topic": "aging potential",
        "RA": "RA2",
        "command_verb": "outline",
        "expected_concepts": ["aging", "acidity", "structure", "alcohol", "oak"]
    },
    {
        "source_question_id": "2011",
        "stem": "State the primary purpose of acid addition during winemaking in regions where grapes do not achieve sufficient natural acidity.",
        "topic": "winemaking adjustments",
        "RA": "RA1",
        "command_verb": "state",
        "expected_concepts": ["acidity", "winemaking", "ripeness"]
    },
    {
        "source_question_id": "2012",
        "stem": "List the main grape varieties used in the production of premium Sherry, and identify which category (fino, amontillado, oloroso) they are associated with.",
        "topic": "Sherry",
        "RA": "RA1",
        "command_verb": "list",
        "expected_concepts": ["Sherry", "grape variety", "fermentation", "fortification"]
    },
    {
        "source_question_id": "2013",
        "stem": "Explain how the altitude of a vineyard influences grape ripening, sugar accumulation, and the final alcohol level in the wine.",
        "topic": "altitude",
        "RA": "RA1",
        "command_verb": "explain",
        "expected_concepts": ["altitude", "temperature", "ripening", "sugar", "alcohol"]
    },
    {
        "source_question_id": "2014",
        "stem": "Compare the production methods and resulting characteristics of sparkling wines made using the Traditional Method versus the Charmat Method.",
        "topic": "sparkling wine",
        "RA": "RA2",
        "command_verb": "compare",
        "expected_concepts": ["sparkling wine", "fermentation", "method", "bubbles"]
    },
    {
        "source_question_id": "2015",
        "stem": "Evaluate the impact of climate change on WSET Level 3 growing regions, considering ripening patterns, acidity levels, and wine style evolution.",
        "topic": "climate change",
        "RA": "RA3",
        "command_verb": "evaluate",
        "expected_concepts": ["climate", "ripening", "acidity", "style", "regions"]
    },
]


def create_or_items_from_expansion() -> list[dict]:
    """Create OR item entries from expansion templates."""
    items = []

    for item_data in EXPANSION_ITEMS:
        q_id = item_data["source_question_id"]
        item = {
            "item_id": f"open_response_{q_id}",
            "source_question_id": str(q_id),
            "stem": item_data["stem"],
            "topic": item_data["topic"],
            "RA": item_data["RA"],
            "command_verb": item_data["command_verb"],
            "expected_concepts": item_data["expected_concepts"],
            "evaluation_config": {
                "verb_definition_key": item_data["command_verb"],
                "requires_causal_chain": "explain" in item_data["command_verb"].lower(),
                "structure_rules": {},
                "required_signals": [],
                "forbidden_signals": [],
                "source": "phase_p2_4_expansion"
            }
        }
        items.append(item)

    return items


def expand_payload(new_items: list[dict]) -> dict:
    """Add new items to the existing payload."""
    payload = load_current_payload()

    # Get existing item IDs to avoid duplicates
    existing_ids = {item.get("item_id") for item in payload.get("items", [])}

    # Filter out duplicates
    unique_new_items = [item for item in new_items if item["item_id"] not in existing_ids]

    # Add to items
    payload["items"].extend(unique_new_items)

    # Update pool size
    payload["pool_size"] = len(payload["items"])

    # Note expansion in metadata
    if "expansion_history" not in payload:
        payload["expansion_history"] = []

    payload["expansion_history"].append({
        "phase": "P2.4",
        "items_added": len(unique_new_items),
        "new_pool_size": payload["pool_size"],
        "timestamp": "phase_p2_4_expansion"
    })

    return payload


def save_expanded_payload(payload: dict, output_path: Path = LAB_PAYLOAD_PATH) -> None:
    """Save the expanded payload."""
    js_code = f"window.OPEN_RESPONSE_LAB_PAYLOAD = {json.dumps(payload, indent=2)};\n"
    output_path.write_text(js_code, encoding="utf-8")


if __name__ == "__main__":
    print("[P2.4] Expanding OR items...")

    new_items = create_or_items_from_expansion()
    print(f"[P2.4] Created {len(new_items)} new curated items")

    payload = expand_payload(new_items)

    save_expanded_payload(payload)

    current = load_current_payload()
    print(f"[OK] Payload expanded: {len(current['items'])} total items (was 26, now +{len(new_items)})")
    print(f"[OK] Pool size: {current['pool_size']}")
