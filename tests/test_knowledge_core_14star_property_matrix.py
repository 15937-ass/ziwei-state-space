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


def matrix_records(data):
    columns = data["matrix"]["columns"]
    return [dict(zip(columns, row)) for row in data["matrix"]["rows"]]


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
        self.assertEqual(len(matrix_records(data)), 430)

    def test_source_and_normalization_epistemic_are_separate_and_unresolved_is_preserved(self):
        data = load_data()
        rows = matrix_records(data)
        self.assertTrue(all("source_epistemic" in r for r in rows))
        self.assertTrue(all("normalization_epistemic" in r for r in rows))
        self.assertTrue(all(r["source_epistemic"] == "EXPLICIT" for r in rows))
        self.assertTrue(all(r["normalization_epistemic"] == "UNRESOLVED" for r in rows))
        self.assertTrue(all(r["claim_role_status"] == "RESEARCH_CANDIDATE_FROM_EXISTING_STRUCTURED_FIELDS_NOT_SOURCE_ADJUDICATED" for r in rows))

    def test_provenance_conditions_and_source_locators_are_preserved(self):
        data = load_data()
        rows = matrix_records(data)
        self.assertTrue(all(r["source_id"] in {"SRC-ZZ-001", "SRC-ZZ-002"} for r in rows))
        self.assertTrue(all(r["source_location"] for r in rows))
        self.assertTrue(all("condition" in r for r in rows))
        self.assertTrue(all("time_scope" in r for r in rows))
        self.assertTrue(all("palace_scope" in r for r in rows))
        self.assertTrue(all("prerequisite_rule_ids" in r for r in rows))
        self.assertTrue(all("source_span_verified" in r for r in rows))
        self.assertTrue(all("case_support_only_status" in r for r in rows))

    def test_report_includes_structural_fit_ambiguity_overlap_conflict_and_counterexample(self):
        data = load_data()
        cases = {case["category"]: case for case in data["representative_case_audit"]}
        self.assertIn("STRUCTURALLY_ALIGNED_CANDIDATE_NOT_ACCEPTED", cases)
        self.assertIn("MULTI_TARGET_PROJECTION_AMBIGUITY", cases)
        self.assertIn("QI_QR_OVERLAP_CANDIDATE", cases)
        self.assertIn("APPARENT_CONFLICT_CONDITIONALLY_DISTINGUISHED", cases)
        self.assertIn("COUNTEREXAMPLE_TO_MANDATORY_COMPLETE_INTRINSIC_VECTOR", cases)
        self.assertEqual(data["source_corpus"]["explicit_conflict_link_rows"], 0)
        self.assertEqual(cases["STRUCTURALLY_ALIGNED_CANDIDATE_NOT_ACCEPTED"]["rule_ids"], ["ZZ-TF-002"])
        self.assertEqual(cases["APPARENT_CONFLICT_CONDITIONALLY_DISTINGUISHED"]["rule_ids"], ["ZZ-ZW-003", "ZZ-ZW-004"])
        report = REPORT_PATH.read_text(encoding="utf-8")
        for rule_id in ["ZZ-TF-002", "ZZ-ZW-013", "ZZ-WQ-020", "ZZ-ZW-003", "ZZ-ZW-004", "ZZ-ZW-002"]:
            self.assertIn(rule_id, report)
        self.assertIn("不等于已经通过人工来源复核", report)
        self.assertIn("不证明紫微没有任何内在性质", report)

    def test_qi_qr_coverage_counts_match_matrix_rows(self):
        data = load_data()
        rows = matrix_records(data)
        dimensions = data["dimensions"]
        qi_qr_links = [row["existing_qi_qr_evidence_links"] for row in rows]

        self.assertEqual(sum(bool(links) for links in qi_qr_links), dimensions["records_with_existing_qi_qr_evidence_link"])
        self.assertEqual(sum(not links for links in qi_qr_links), dimensions["records_without_existing_qi_qr_evidence_link"])
        self.assertEqual(
            sum(len({link[0] for link in links}) > 1 for links in qi_qr_links),
            dimensions["records_with_multiple_qi_qr_dimensions"],
        )
        self.assertEqual(
            sum(len(row["candidate_mapping_targets"]) > 1 for row in rows),
            dimensions["records_with_multiple_candidate_targets"],
        )
        self.assertEqual(sum(bool(row["overlap_flags"]) for row in rows), dimensions["records_with_overlap_flags"])
        self.assertEqual(dimensions["records_with_existing_qi_qr_evidence_link"], 129)
        self.assertEqual(dimensions["records_without_existing_qi_qr_evidence_link"], 301)
        self.assertEqual(dimensions["records_with_multiple_qi_qr_dimensions"], 12)
        self.assertEqual(dimensions["records_with_multiple_candidate_targets"], 15)
        self.assertEqual(dimensions["records_with_overlap_flags"], 149)

    def test_candidate_targets_are_not_promoted_to_accepted_mappings(self):
        data = load_data()
        for row in matrix_records(data):
            self.assertFalse(row["canonicalization_authorized"])
            self.assertFalse(row["product_consumption_authorized"])
            self.assertIn(row["mapping_status"], {
                "MULTIPLE_EVIDENCE_TARGETS_REVIEW_REQUIRED",
                "EXISTING_EVIDENCE_REFERENCE_REVIEW_REQUIRED",
                "NO_EXPLICIT_EXISTING_QI_QR_EVIDENCE_LINK_FOUND",
            })

    def test_pr710_output_kind_crosswalk_keeps_gaps_and_overlaps_visible(self):
        data = load_data()
        crosswalk = data["pr710_crosswalk"]
        roles = {r["research_claim_role"] for r in crosswalk}
        self.assertIn("intrinsic_property_candidate", roles)
        self.assertIn("evaluation_component", roles)
        self.assertTrue(any(r["status"] == "MANY_TO_MANY" for r in crosswalk))
        self.assertTrue(any(r["status"] == "GAP_OR_OUTSIDE_CURRENT_OUTPUT_KIND" for r in crosswalk))
        self.assertTrue(any(r["research_claim_role"] == "causal_or_explanatory_relation" for r in crosswalk))

    def test_pr710_event_specificity_is_not_assumed_to_be_an_ordinal_scale(self):
        data = load_data()
        axis = data["pr710_event_specificity_audit"]
        self.assertFalse(axis["candidate_values_form_ordinal_scale"])
        self.assertTrue(data["methodology"]["event_specificity_axis_review_required"])
        self.assertIn("PROCESS_SEQUENCE_NOT_SINGLE_EVENT", axis["candidate_values"])
        self.assertIn("SCENE_NOT_OBSERVED_EVENT", axis["candidate_values"])
        self.assertFalse(axis["canonical_change_authorized"])
        self.assertEqual(
            {row["value"] for row in data["pr710_event_specificity_value_audit"]},
            set(axis["candidate_values"]),
        )
        self.assertEqual(
            {row["value"] for row in data["pr710_output_kind_value_audit"]},
            set(data["pr710_candidate_axes"]["output_kind_values"]),
        )
        self.assertFalse(data["pr710_event_specificity_audit"]["not_applicable_is_candidate_value"])

    def test_no_false_claim_of_independent_held_out_validation(self):
        data = load_data()
        self.assertEqual(data["methodology"]["holdout_status"], "NOT_PERFORMED_NO_LEAKAGE_FREE_HOLDOUT")
        self.assertIn("blinded", data["methodology"]["holdout_reason"])

    def test_csv_and_json_row_counts_match(self):
        data = load_data()
        with CSV_PATH.open(encoding="utf-8", newline="") as f:
            rows = list(csv.DictReader(f))
        self.assertEqual(len(rows), len(matrix_records(data)))
        self.assertEqual(len(rows), 430)


if __name__ == "__main__":
    unittest.main()
