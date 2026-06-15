"""
OR Batch 1 Validation Tests

Validates that Batch 1 (25 items) meets WSET L3 OR standards.
"""

import json
from pathlib import Path

REPO = Path(__file__).parent.parent
OR_BANK = REPO / "knowledge" / "question-bank" / "open_response" / "open_response_bank.json"

def test_batch_01_item_count():
    """Verify 56 items exist (31 base + 25 batch 1)."""
    with open(OR_BANK, 'r', encoding='utf-8') as f:
        data = json.load(f)

    assert len(data['items']) >= 56, f"Expected at least 56 items, got {len(data['items'])}"

def test_batch_01_unique_ids():
    """Verify no duplicate IDs."""
    with open(OR_BANK, 'r', encoding='utf-8') as f:
        data = json.load(f)

    ids = [item['item_id'] for item in data['items']]
    assert len(ids) == len(set(ids)), "Duplicate IDs found"

def test_batch_01_governance_clean():
    """Verify all items have safe_for_examiner=False."""
    with open(OR_BANK, 'r', encoding='utf-8') as f:
        data = json.load(f)

    violations = [
        item for item in data['items']
        if item.get('governance', {}).get('safe_for_examiner') != False
    ]

    assert len(violations) == 0, f"Governance violations found in {len(violations)} items"

def test_batch_01_command_verb_coverage():
    """Verify 8 command verbs are present in Batch 1 items."""
    with open(OR_BANK, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Check only Batch 1 items (OR_032 to OR_056)
    batch_1_items = [
        item for item in data['items']
        if 'OR_032' <= item['item_id'] <= 'OR_056'
    ]
    verbs = set(item.get('command_verb', '') for item in batch_1_items if 'command_verb' in item)
    expected = {
        'describe', 'explain', 'compare', 'assess',
        'evaluate', 'discuss', 'recommend', 'identify_and_explain'
    }

    assert verbs == expected, f"Batch 1 missing verbs: {expected - verbs}"

def test_batch_01_ra_distribution():
    """Verify RA1-RA5 all present in Batch 1 items."""
    with open(OR_BANK, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Check only Batch 1 items (OR_032 to OR_056)
    batch_1_items = [
        item for item in data['items']
        if 'OR_032' <= item['item_id'] <= 'OR_056'
    ]
    ras = set(item.get('ra_id', '') for item in batch_1_items)
    expected = {'RA1', 'RA2', 'RA3', 'RA4', 'RA5'}

    assert ras == expected, f"Batch 1 missing RAs: {expected - ras}"

def test_batch_01_required_fields():
    """Verify Batch 1 items have required fields."""
    with open(OR_BANK, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Check only Batch 1 items (OR_032 to OR_056)
    batch_1_items = [
        item for item in data['items']
        if 'OR_032' <= item['item_id'] <= 'OR_056'
    ]
    required_fields = {
        'item_id', 'question_text', 'command_verb',
        'ra_id', 'topic', 'expected_concepts', 'response_depth_target'
    }

    for item in batch_1_items:
        missing = required_fields - set(item.keys())
        assert len(missing) == 0, f"Item {item.get('item_id')} missing fields: {missing}"

def test_batch_01_causal_chains_valid():
    """Verify causal_chain_target references are valid for Batch 1."""
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

    # Check only Batch 1 items (OR_032 to OR_056)
    batch_1_items = [
        item for item in data['items']
        if 'OR_032' <= item['item_id'] <= 'OR_056'
    ]

    for item in batch_1_items:
        chains = item.get('causal_chain_target', [])
        for chain in chains:
            assert chain in valid_chains, f"Item {item['item_id']}: Unknown causal chain: {chain}"

def test_batch_01_no_empty_concepts():
    """Verify all items have non-empty expected_concepts."""
    with open(OR_BANK, 'r', encoding='utf-8') as f:
        data = json.load(f)

    empty_concepts = [
        item for item in data['items']
        if not item.get('expected_concepts') or len(item['expected_concepts']) == 0
    ]

    assert len(empty_concepts) == 0, f"{len(empty_concepts)} items have empty concepts"

if __name__ == '__main__':
    test_batch_01_item_count()
    test_batch_01_unique_ids()
    test_batch_01_governance_clean()
    test_batch_01_command_verb_coverage()
    test_batch_01_ra_distribution()
    test_batch_01_required_fields()
    test_batch_01_causal_chains_valid()
    test_batch_01_no_empty_concepts()
    print("✅ All OR Batch 1 tests passed")
