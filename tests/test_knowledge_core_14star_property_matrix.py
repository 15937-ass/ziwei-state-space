import csv
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
JSON_PATH = ROOT / "knowledge/core/14star-property-matrix/14STAR_PROPERTY_MATRIX_QIQR_AUDIT_v0.1.json"
CSV_PATH = ROOT / "knowledge/core/14star-property-matrix/14STAR_PROPERTY_MATRIX_QIQR_AUDIT_v0.1.csv"
REPORT_PATH = ROOT / "knowledge/core/14star-property-matrix/14STAR_PROPERTY_MATRIX_QIQR_AUDIT_v0.1.md"


def load_data():
    return json.loads(JSON_PATH.read_text(encoding="utf-8"))


class TestFourteenStarPropertyMatrix(unittest.TestCase):
    def test_proposal_only_and_no_canonical_or_product_authority(self):
        data = load_data()
        self.assertEqual(data["status"], "PROPOSAL_ONLY_NOT_CANONICAL")
        self.assertFalse(data["methodology"]["canonicalization_authorized"])
        self.assertFalse(data["methodology"]["product_consumption_authorized"])
        self.assertFalse(data["methodology"]["new_qi_qr_primitive_authorized"])
        self.assertEqual(data["methodology"]["probability_status"], "UNKNOWN")
        self.assertFalse(data["methodology"]["empirical_validity_claim"])

    def test_all_fourteen_stars_and_all_source_rule_ids_are_covered(self):
        data = load_data()
        self.assertEqual(data["star_cores"]["star_count"], 14)
        self.assertEqual(data["source_corpus"]["record_count"], 430)
        self.assertEqual(data["source_corpus"]["unique_rule_ids"], 430)
        self.assertEqual(len(data["source_corpus"]["subject_counts"]), 14)
        self.assertTrue(all(count > 0 for _, count in data["source_corpus"]["subject_counts"]))

    def test_source_and_normalization_epistemic_are_separate_and_unresolved_is_preserved(self):
        data = load_data()
        rows = data["records"]
        self.assertTrue(all("source_epistemic" in r for r in rows))
        self.assertTrue(all("normalization_epistemic" in r for r in rows))
        self.assertTrue(all(r["source_epistemic"] == "EXPLICIT" for r in rows))
        self.assertTrue(all(r["normalization_epistemic"] == "UNRESOLVED" for r in rows))
        self.assertTrue(all(r["claim_role_status"] == "RESEARCH_CANDIDATE_FROM_EXISTING_STRUCTURED_FIELDS_NOT_SOURCE_ADJUDICATED" for r in rows))

    def test_provenance_conditions_and_source_locators_are_preserved(self):
        data = load_data()
        rows = data["records"]
        self.assertTrue(all(r["source_id"] in {"SRC-ZZ-001", "SRC-ZZ-002"} for r in rows))
        self.assertTrue(all(r["source_location"] for r in rows))
        self.assertTrue(all("condition" in r for r in rows))
        self.assertTrue(all("time_scope" in r for r in rows))
        self.assertTrue(all("palace_scope" in r for r in rows))
        self.assertTrue(all("prerequisite_rule_ids" in r for r in rows))
        self.assertTrue(all("source_span_verified" in r for r in rows))
        self.assertTrue(all("case_support_only_status" in r for r in rows))

    def test_candidate_targets_are_not_promoted_to_accepted_mappings(self):
        data = load_data()
        for row in data["records"]:
            self.assertFalse(row["canonicalization_authorized"])
            self.assertFalse(row["product_consumption_authorized"])
            self.assertIn(row["mapping_status"], {
                "MULTIPLE_EVIDENCE_TARGETS_REVIEW_REQUIRED",
                "EXISTING_EVIDENCE_REFERENCE_REVIEW_REQUIRED",
                "NO_EXPLICIT_EXISTING_QI_QR_EVIDENCE_LINK_FOUND",
            })

    def test_pr710_taxonomy_crosswalk_keeps_gaps_and_overlaps_visible(self):
        data = load_data()
        crosswalk = data["pr710_crosswalk"]
        roles = {r["research_claim_role"] for r in crosswalk}
        self.assertIn("intrinsic_property_candidate", roles)
        self.assertIn("evaluation_component", roles)
        self.assertTrue(any(r["status"] == "MANY_TO_MANY" for r in crosswalk))
        self.assertTrue(any(r["status"] == "GAP_OR_OUTSIDE_CURRENT_OUTPUT_KIND" for r in crosswalk))
        self.assertTrue(any("specificity" in r["risk"].lower() or "具体" in r["risk"] for r in crosswalk) or any("event_specificity" in r["research_claim_role"] for r in crosswalk))

    def test_no_false_claim_of_independent_held_out_validation(self):
        data = load_data()
        self.assertEqual(data["methodology"]["holdout_status"], "NOT_PERFORMED_NO_LEAKAGE_FREE_HOLDOUT")
        self.assertIn("blinded", data["methodology"]["holdout_reason"])

    def test_csv_and_json_row_counts_match(self):
        data = load_data()
        with CSV_PATH.open(encoding="utf-8", newline="") as f:
            rows = list(csv.DictReader(f))
        self.assertEqual(len(rows), len(data["records"]))
        self.assertEqual(len(rows), 430)

