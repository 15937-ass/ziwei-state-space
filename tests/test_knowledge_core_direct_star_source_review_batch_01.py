import csv
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = ROOT / "knowledge/core/direct-star-source-review/DIRECT_STAR_SOURCE_REVIEW_BATCH_01_v0.1.csv"
REPORT_PATH = ROOT / "knowledge/core/direct-star-source-review/DIRECT_STAR_SOURCE_REVIEW_BATCH_01_v0.1.md"
EVIDENCE_PATH = ROOT / "validation/knowledge/core/direct-star-source-review/DIRECT_STAR_SOURCE_REVIEW_BATCH_01_EVIDENCE.md"

EXPECTED_IDS = {
    "ZZ-ZW-015", "ZZ-ZW-018", "ZZ-ZW-X01", "ZZ-ZW-X05",
    "ZZ-TJ-002", "ZZ-TJ-005", "ZZ-TJ-X01",
    "ZZ-TY-002", "ZZ-TY-009", "ZZ-TY-010", "ZZ-TY-016",
    "ZZ-TY-017", "ZZ-TY-018", "ZZ-TY-X02",
    "ZZ-WQ-003", "ZZ-WQ-004", "ZZ-WQ-005", "ZZ-WQ-006",
    "ZZ-WQ-019", "ZZ-WQ-024",
    "ZZ-TT-002", "ZZ-TT-004", "ZZ-TT-005", "ZZ-TT-006",
    "ZZ-TT-X01", "ZZ-TT-X02",
    "ZZ-LZ-003", "ZZ-LZ-Y01",
    "ZZ-TF-002", "ZZ-TF-003", "ZZ-TF-004", "ZZ-TF-005", "ZZ-TF-006",
}

def load_rows():
    with CSV_PATH.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))

class TestDirectStarSourceReviewBatch01(unittest.TestCase):
    def test_exact_unique_rule_coverage(self):
        rows = load_rows()
        ids = [row["rule_id"] for row in rows]
        self.assertEqual(len(rows), 33)
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(set(ids), EXPECTED_IDS)

    def test_each_row_has_source_provenance_and_visual_span_status(self):
        rows = load_rows()
        for row in rows:
            with self.subTest(rule_id=row["rule_id"]):
                self.assertIn(row["source_id"], {"SRC-ZZ-001", "SRC-ZZ-002"})
                self.assertTrue(row["source_location"])
                self.assertTrue(row["source_pdf_page"])
                self.assertTrue(row["source_printed_page"])
                self.assertEqual(row["source_span_status"], "VERIFIED_VISUAL_SCAN")
                self.assertTrue(row["literal_source_span"])
                self.assertTrue(row["current_core_references"])

    def test_source_and_normalization_epistemic_and_scope_fields_stay_separate(self):
        rows = load_rows()
        preserved_fields = {
            "canonical_condition", "canonical_time_scope", "canonical_palace_scope",
            "canonical_prerequisite_rule_ids", "canonical_excludes_rule_ids",
            "canonical_conflicts_with_rule_ids", "canonical_operator",
            "canonical_state_change", "canonical_valence",
            "canonical_applicability_scope", "modality_scope_ambiguity",
        }
        for row in rows:
            with self.subTest(rule_id=row["rule_id"]):
                self.assertEqual(row["source_epistemic"], "EXPLICIT")
                self.assertEqual(row["normalization_epistemic_before"], "UNRESOLVED")
                self.assertEqual(row["normalization_epistemic_after"], "UNRESOLVED")
                self.assertEqual(row["canonical_source_span_verified_before"], "false")
                self.assertEqual(row["canonical_source_span_verified_after"], "false")
                self.assertTrue(preserved_fields.issubset(row.keys()))
                self.assertEqual(row["modality_scope_ambiguity"], row["condition_scope_assessment"])

    def test_roles_and_tiers_are_separate_and_valid(self):
        rows = load_rows()
        valid_roles = {"INTRINSIC", "RELATIONAL", "CONDITIONAL", "UNRESOLVED_OTHER"}
        valid_tiers = {"DIRECT_STAR", "SAME_STAR_MODIFIER", "SYSTEM_CONTEXT", "PROJECTION"}
        for row in rows:
            with self.subTest(rule_id=row["rule_id"]):
                self.assertIn(row["claim_role"], valid_roles)
                self.assertIn(row["current_evidence_tier"], valid_tiers)
                self.assertIn(row["proposed_evidence_tier"], valid_tiers)

    def test_normalization_remains_unresolved_and_artifacts_are_noncanonical(self):
        rows = load_rows()
        for row in rows:
            with self.subTest(rule_id=row["rule_id"]):
                self.assertEqual(row["normalization_epistemic_before"], "UNRESOLVED")
                self.assertEqual(row["normalization_epistemic_after"], "UNRESOLVED")
                self.assertEqual(row["proposal_status"], "PROPOSAL_ONLY_NOT_CANONICAL")
        report = REPORT_PATH.read_text(encoding="utf-8")
        evidence = EVIDENCE_PATH.read_text(encoding="utf-8")
        self.assertIn("PROPOSAL_ONLY_NOT_CANONICAL", report)
        self.assertIn("本轮不做 canonical 修改", report)
        self.assertIn("PROPOSAL_ONLY_NOT_CANONICAL", evidence)
        self.assertIn("Product", evidence)

    def test_repeated_reference_is_not_duplicated_as_a_source_rule(self):
        rows = load_rows()
        by_id = {row["rule_id"]: row for row in rows}
        self.assertIn("STAR-WQ.intrinsic_signature:QI-05", by_id["ZZ-WQ-004"]["current_core_references"])
        self.assertIn("STAR-WQ.intrinsic_signature:QI-08", by_id["ZZ-WQ-004"]["current_core_references"])
        self.assertIn("OVERLAP_WITH_ZZ_TY_010", by_id["ZZ-TY-X02"]["core_use_assessment"])
        self.assertEqual(sum(row["rule_id"] == "ZZ-WQ-004" for row in rows), 1)

    def test_report_and_evidence_keep_noncanonical_boundaries(self):
        report = REPORT_PATH.read_text(encoding="utf-8")
        evidence = EVIDENCE_PATH.read_text(encoding="utf-8")
        self.assertIn("ZZ-TJ-002", report)
        self.assertIn("ZZ-TY-X02", report)
        self.assertIn("ZZ-WQ-024", report)
        self.assertIn("ZZ-TF-006", report)
        self.assertIn("没有修改 canonical", evidence)
        self.assertIn("UNKNOWN", evidence)
        self.assertIn("未授权", evidence)

if __name__ == "__main__":
    unittest.main()
