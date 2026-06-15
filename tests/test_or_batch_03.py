"""
OR Batch 3 Validation Tests

Validates that Batch 3 (25 items) meets WSET L3 OR standards.
Confirms 100+ OR items total objective achievement.
"""

import json
from pathlib import Path

REPO = Path(__file__).parent.parent
OR_BANK = REPO / "knowledge" / "question-bank" / "open_response" / "open_response_bank.json"

def test_batch_03_item_count():
    """Verify 106 items exist (81 prior + 25 batch 3)."""
    with open(OR_BANK, 'r', encoding='utf-8') as f:
        data = json.load(f)

    assert len(data['items']) >= 106, f"Expected at least 106 items, got {len(data['items'])}"

def test_batch_03_exceeds_100_target():
    """Verify OR bank exceeds 100 items target."""
    with open(OR_BANK, 'r', encoding='utf-8') as f:
        data = json.load(f)

    assert len(data['items']) >= 100, f"Target not met: {len(data['items'])} < 100"

def test_batch_03_unique_ids():
    """Verify no duplicate IDs."""
    with open(OR_BANK, 'r', encoding='utf-8') as f:
        data = json.load(f)

    ids = [item['item_id'] for item in data['items']]
    assert len(ids) == len(set(ids)), "Duplicate IDs found"

def test_batch_03_governance_clean():
    """Verify all items have safe_for_examiner=False."""
    with open(OR_BANK, 'r', encoding='utf-8') as f:
        data = json.load(f)

    violations = [
        item for item in data['items']
        if item.get('governance', {}).get('safe_for_examiner') != False
    ]

    assert len(violations) == 0, f"Governance violations found in {len(violations)} items"

def test_batch_03_command_verb_coverage():
    """Verify 8 command verbs are present in Batch 3 items."""
    with open(OR_BANK, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Check only Batch 3 items (OR_082 to OR_106)
    batch_3_items = [
        item for item in data['items']
        if 'OR_082' <= item['item_id'] <= 'OR_106'
    ]
    verbs = set(item.get('command_verb', '') for item in batch_3_items if 'command_verb' in item)
    expected = {
        'describe', 'explain', 'compare', 'assess',
        'evaluate', 'discuss', 'recommend', 'identify_and_explain'
    }

    assert verbs == expected, f"Batch 3 missing verbs: {expected - verbs}"

def test_batch_03_ra_distribution():
    """Verify RA1-RA5 all present in Batch 3 items."""
    with open(OR_BANK, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Check only Batch 3 items (OR_082 to OR_106)
    batch_3_items = [
        item for item in data['items']
        if 'OR_082' <= item['item_id'] <= 'OR_106'
    ]
    ras = set(item.get('ra_id', '') for item in batch_3_items)
    expected = {'RA1', 'RA2', 'RA3', 'RA4', 'RA5'}

    assert ras == expected, f"Batch 3 missing RAs: {expected - ras}"

def test_batch_03_required_fields():
    """Verify Batch 3 items have required fields."""
    with open(OR_BANK, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Check only Batch 3 items (OR_082 to OR_106)
    batch_3_items = [
        item for item in data['items']
        if 'OR_082' <= item['item_id'] <= 'OR_106'
    ]
    required_fields = {
        'item_id', 'question_text', 'command_verb',
        'ra_id', 'topic', 'expected_concepts', 'response_depth_target'
    }

    for item in batch_3_items:
        missing = required_fields - set(item.keys())
        assert len(missing) == 0, f"Item {item.get('item_id')} missing fields: {missing}"

def test_batch_03_causal_chains_valid():
    """Verify causal_chain_target references are valid for Batch 3."""
    import os

    # Load all valid causal chain IDs from filesystem
    causal_chains_dir = REPO / "knowledge" / "knowledge-map" / "causal-chains"
    valid_chains = set()

    for chain_file in causal_chains_dir.glob('*.json'):
        # Extract chain_id from filename (e.g., HC_ALTITUDE_TEMPERATURE.json)
        chain_id = chain_file.stem.upper()
        valid_chains.add(chain_id)

    with open(OR_BANK, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Check only Batch 3 items (OR_082 to OR_106)
    batch_3_items = [
        item for item in data['items']
        if 'OR_082' <= item['item_id'] <= 'OR_106'
    ]

    for item in batch_3_items:
        chains = item.get('causal_chain_target', [])
        for chain in chains:
            assert chain in valid_chains, f"Item {item['item_id']}: Unknown causal chain: {chain}"

def test_batch_03_no_empty_concepts():
    """Verify Batch 3 items have non-empty expected_concepts."""
    with open(OR_BANK, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Check only Batch 3 items
    batch_3_items = [item for item in data['items'] if item['item_id'] >= 'OR_082']
    empty_concepts = [
        item for item in batch_3_items
        if not item.get('expected_concepts') or len(item['expected_concepts']) == 0
    ]

    assert len(empty_concepts) == 0, f"{len(empty_concepts)} items have empty concepts"

if __name__ == '__main__':
    test_batch_03_item_count()
    test_batch_03_exceeds_100_target()
    test_batch_03_unique_ids()
    test_batch_03_governance_clean()
    test_batch_03_command_verb_coverage()
    test_batch_03_ra_distribution()
    test_batch_03_required_fields()
    test_batch_03_causal_chains_valid()
    test_batch_03_no_empty_concepts()
    print("✅ All OR Batch 3 tests passed")
    print("✅ OR Expansion Program COMPLETE: 106 items (exceeded 100+ target)")
