"""
OR Batch Integrator — Merges expansion batches into master open_response_bank.json

Usage:
  python tools/question_generation/or_batch_integrator.py --batch 1
"""

import json
import sys
from pathlib import Path

REPO = Path(__file__).parent.parent.parent
OR_BANK = REPO / "knowledge" / "question-bank" / "open_response" / "open_response_bank.json"

def merge_batch(batch_number):
    """Merge expansion batch into master bank."""

    batch_file = REPO / "knowledge" / "question-bank" / "open_response" / f"or_batch_{batch_number:02d}_expansion.json"

    if not batch_file.exists():
        print(f"ERROR: Batch file not found: {batch_file}")
        return False

    # Load both files
    with open(OR_BANK, 'r', encoding='utf-8') as f:
        master = json.load(f)

    with open(batch_file, 'r', encoding='utf-8') as f:
        batch = json.load(f)

    # Count before
    count_before = len(master.get('items', []))

    # Merge items
    if 'items' not in master:
        master['items'] = []

    # Ensure each batch item has governance fields
    for item in batch['items']:
        if 'governance' not in item:
            item['governance'] = {
                'safe_for_examiner': False,
                'examiner_scoring_allowed': False,
                'training_item_only': True
            }

    master['items'].extend(batch['items'])

    count_after = len(master['items'])

    # Update metadata
    master['last_batch'] = batch_number
    master['total_items'] = count_after
    if 'batch_metadata' not in master:
        master['batch_metadata'] = {}

    master['batch_metadata'][f'batch_{batch_number}'] = {
        'batch_number': batch_number,
        'items_added': batch['batch_size'],
        'generated_at': batch['generated_at']
    }

    # Write back
    with open(OR_BANK, 'w', encoding='utf-8') as f:
        json.dump(master, f, indent=2, ensure_ascii=False)

    print(f"✓ Merged Batch {batch_number}")
    print(f"  Before: {count_before} items")
    print(f"  Added: {batch['batch_size']} items")
    print(f"  After: {count_after} items")

    return True

if __name__ == "__main__":
    batch_num = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    success = merge_batch(batch_num)
    sys.exit(0 if success else 1)
