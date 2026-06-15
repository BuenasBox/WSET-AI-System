import copy
import unittest

from tools.question_generation.sba_gap_closure import (
    SAFE_GOVERNANCE,
    validate_batch_payload,
)


def _valid_record():
    return {
        "question_id": "858",
        "question_text": (
            "Un productor mantiene las uvas sanas en la vid hasta que se congelan. "
            "¿Qué resultado explica mejor la concentración del mosto prensado?"
        ),
        "question_type": "theory",
        "expected_topics": ["RA1", "sweet_winemaking", "icewine_concentration"],
        "expected_causal_links": [
            "agua congelada queda en el prensado -> mosto con más azúcar y acidez"
        ],
        "expected_keywords": ["Icewine", "congelación", "prensado", "concentración"],
        "expected_reasoning_type": "cause_effect",
        "difficulty": "intermediate",
        "source_type": "SBA gap closure batch 1 | official study-guide grounding",
        "safe_for_examiner": False,
        "options": {
            "A": "El agua congelada queda en la prensa y el mosto resulta más concentrado.",
            "B": "La congelación convierte el ácido en azúcar antes del prensado.",
            "C": "El hielo aumenta el rendimiento de mosto y diluye la acidez.",
            "D": "La fermentación se detiene antes de comenzar por falta de levaduras.",
        },
        "correct_answer_letter": "A",
        "correct_answer_text": (
            "El agua congelada queda en la prensa y el mosto resulta más concentrado."
        ),
        "source_support": {
            "source_ids": ["official_wset_white_and_sweet_winemaking"],
            "source_files": [
                "knowledge/official-wset/study-guide/wset_markdown/"
                "seccion_5_section_2_factors_affecting_the_style_quality_and_price_of_w/"
                "5-5_8_white_and_sweet_winemaking.md"
            ],
            "support_rationale": "La fuente describe la concentración por congelación y prensado.",
        },
        "enrichment": {
            "causal_chain_candidate": {
                "candidate_id": "CC_CAND_ICEWINE_CONCENTRATION",
                "cause": "Las uvas se congelan de forma natural en la vid.",
                "mechanism": "Durante el prensado, parte del agua permanece como hielo.",
                "effect": "Se obtiene poco mosto con azúcar, acidez y sabor concentrados.",
            },
            "feedback_profile": {
                "correct_rationale": "La separación física del agua como hielo concentra el mosto.",
                "distractor_rationales": {
                    "A": "Es la relación causal correcta.",
                    "B": "La congelación no transforma ácido en azúcar.",
                    "C": "El rendimiento disminuye en vez de aumentar.",
                    "D": "La concentración ocurre durante el prensado, antes de fermentar.",
                },
                "remediation_recommendation": "Reconstruya la secuencia congelación, prensado y concentración.",
            },
            "micro_drill_candidate": {
                "prompt": "¿Qué componente queda retenido principalmente como hielo?",
                "answer": "Agua",
            },
            "misconception_linkage_candidate": {
                "misconception_id": "MC_ICEWINE_NOBLE_01",
                "target_error": "Confundir congelación natural con concentración por botrytis.",
            },
        },
        "governance": copy.deepcopy(SAFE_GOVERNANCE),
    }


class BatchContractTests(unittest.TestCase):
    def test_valid_batch_passes(self):
        records = []
        for offset in range(47):
            record = _valid_record()
            record["question_id"] = str(858 + offset)
            record["question_text"] += f" Caso {offset + 1}."
            record["options"]["A"] += f" Caso {offset + 1}."
            record["correct_answer_text"] = record["options"]["A"]
            records.append(record)
        payload = {
            "schema_version": "sba_gap_closure_batch_v1",
            "batch_id": "SBA_BATCH_1",
            "records": records,
            "governance": copy.deepcopy(SAFE_GOVERNANCE),
        }
        self.assertEqual(validate_batch_payload(payload), [])

    def test_rejects_identification_only_stem(self):
        records = []
        for offset in range(47):
            record = _valid_record()
            record["question_id"] = str(858 + offset)
            record["question_text"] += f" Caso {offset + 1}."
            record["options"]["A"] += f" Caso {offset + 1}."
            record["correct_answer_text"] = record["options"]["A"]
            records.append(record)
        records[0]["question_text"] = "¿Qué uva se utiliza en este vino?"
        payload = {
            "schema_version": "sba_gap_closure_batch_v1",
            "batch_id": "SBA_BATCH_1",
            "records": records,
            "governance": copy.deepcopy(SAFE_GOVERNANCE),
        }
        self.assertTrue(
            any("identification-only" in error for error in validate_batch_payload(payload))
        )

    def test_rejects_missing_enrichment_candidate(self):
        records = []
        for offset in range(47):
            record = _valid_record()
            record["question_id"] = str(858 + offset)
            record["question_text"] += f" Caso {offset + 1}."
            record["options"]["A"] += f" Caso {offset + 1}."
            record["correct_answer_text"] = record["options"]["A"]
            records.append(record)
        del records[0]["enrichment"]["micro_drill_candidate"]
        payload = {
            "schema_version": "sba_gap_closure_batch_v1",
            "batch_id": "SBA_BATCH_1",
            "records": records,
            "governance": copy.deepcopy(SAFE_GOVERNANCE),
        }
        self.assertTrue(
            any("micro_drill_candidate" in error for error in validate_batch_payload(payload))
        )

    def test_rejects_unsafe_governance(self):
        records = []
        for offset in range(47):
            record = _valid_record()
            record["question_id"] = str(858 + offset)
            record["question_text"] += f" Caso {offset + 1}."
            record["options"]["A"] += f" Caso {offset + 1}."
            record["correct_answer_text"] = record["options"]["A"]
            records.append(record)
        records[0]["governance"]["safe_for_examiner"] = True
        payload = {
            "schema_version": "sba_gap_closure_batch_v1",
            "batch_id": "SBA_BATCH_1",
            "records": records,
            "governance": copy.deepcopy(SAFE_GOVERNANCE),
        }
        self.assertTrue(
            any("governance" in error for error in validate_batch_payload(payload))
        )


if __name__ == "__main__":
    unittest.main()
