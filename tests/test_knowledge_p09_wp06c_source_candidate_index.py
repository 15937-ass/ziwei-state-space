import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX_PATH = ROOT / "knowledge/palaces/P09_career/wp06c/P09_WP06C_SOURCE_CANDIDATE_INDEX_v0.1.json"
CA01_CSV = ROOT / "validation/wp05/CA01_career_projection_review_001_100.csv"
CA05_CSV = ROOT / "validation/wp05/CA05_career_projection_review_401_500.csv"
CONTEXT_MAP = ROOT / "knowledge/wp07a/CAREER_CONTEXT_MAP_CA01_035_043_045_v0.1.json"
FIRE_BELL_EVIDENCE = ROOT / "knowledge/wp07a/CAREER_FIRE_BELL_SOURCE_EVIDENCE_v0.1.json"
DIRECT_TRANSFORM_AUDIT = ROOT / "knowledge/wp07a/CAREER_DIRECT_TRANSFORM_AUDIT_CA04_CA09_v0.1.md"

ALLOWED_EVIDENCE_TIERS = {
    "EXPLICIT", "TRANSPARENT_INFERENCE", "CASE_SUPPORT_ONLY", "HYPOTHESIS"
}
FORBIDDEN_NUMERIC_SEMANTICS = {
    "probability", "frequency", "weight", "score", "posterior",
    "likelihood", "hazard", "odds"
}


def _all_keys(value):
    if isinstance(value, dict):
        for key, nested in value.items():
            yield key.lower()
            yield from _all_keys(nested)
    elif isinstance(value, list):
        for nested in value:
            yield from _all_keys(nested)


def _csv_rows(path):
    with path.open(encoding="utf-8", newline="") as handle:
        return {row["projection_rule_id"]: row for row in csv.DictReader(handle)}


def test_wp06c_p09_candidate_index_is_fail_closed_and_source_linked():
    payload = json.loads(INDEX_PATH.read_text(encoding="utf-8"))
    assert payload["artifact_id"] == "KB-WP06C-P09-SOURCE-CANDIDATE-INDEX"
    assert payload["status"] == "CANDIDATE_ONLY_NOT_CANONICAL"
    assert payload["dependencies"]["wp06b_issue"] == 672
    assert payload["dependencies"]["human_gate_status"] == "FUTURE_GATE_NOT_APPROVED_BY_THIS_ARTIFACT"
    assert payload["invariants"]["candidate_only"] is True
    assert payload["invariants"]["canonical_mapping"] is False
    assert payload["invariants"]["ontology_node_ids_assigned"] is False
    assert payload["invariants"]["executable"] is False
    assert payload["invariants"]["product_consumable"] is False
    assert payload["invariants"]["probability_status"] == "UNKNOWN"
    assert set(payload["evidence_tier_vocabulary"]) == ALLOWED_EVIDENCE_TIERS
    assert payload["source_scan_review"]["attachment_sha256"] == payload["source_attachment_sha256"]
    assert payload["source_scan_review"]["verification_method"] == "DIRECT_PDF_VISUAL_REVIEW"
    assert payload["source_scan_review"]["verified_pdf_pages"] == [67, 72]
    assert payload["source_scope"]["pdf_pages"] == [67, 72]

    candidates = payload["candidates"]
    assert len(candidates) == 3
    assert len({item["candidate_id"] for item in candidates}) == len(candidates)
    assert len({item["source_rule_id"] for item in candidates}) == len(candidates)

    rows = {}
    rows.update(_csv_rows(CA01_CSV))
    rows.update(_csv_rows(CA05_CSV))
    assert set(item["source_rule_id"] for item in candidates) == {
        "CA01-035", "CA01-045", "CA05-469"
    }

    for item in candidates:
        row = rows[item["source_rule_id"]]
        assert item["source"]["source_span_verified"] is True
        assert item["source"]["review_status"] == "SOURCE_SPAN_VERIFIED"
        assert item["source"]["source_epistemic"] == "EXPLICIT"
        assert item["source"]["case_support_only"] is False
        assert item["source"]["time_layer"] == "NATAL"
        assert item["source"]["source_location"] == row["source_location"]
        assert item["source_condition_text"] == row["condition"]
        assert item["normalized_projection"]["projection_domain"] == row["projection_domain"]
        assert item["normalized_projection"]["projection_target"] == row["projection_target"]
        assert item["normalized_projection"]["projection_mode"] == row["projection_mode"]
        assert item["mapping_evidence_tier"] in ALLOWED_EVIDENCE_TIERS
        assert item["ontology_node_id"] is None
        assert item["probability_status"] == "UNKNOWN"
        assert item["executable"] is False
        assert item["product_consumable"] is False
        assert item["source_span_ids"] == [f"ZZ003-P{item['source']['printed_page']}"]
        assert item["evidence_refs"]

        # Probability/frequency/weight semantics are not permitted in candidate content.
        lowered = set(_all_keys(item))
        assert not (lowered & FORBIDDEN_NUMERIC_SEMANTICS)

    context = json.loads(CONTEXT_MAP.read_text(encoding="utf-8"))
    context_by_id = {item["source_rule_id"]: item for item in context["mappings"]}
    ca01_035 = next(item for item in candidates if item["source_rule_id"] == "CA01-035")
    source_035 = context_by_id["CA01-035"]
    assert ca01_035["source_anchor_phrase"] in source_035["source_anchor_phrase"]
    assert ca01_035["condition_status"] == "BLOCKED_SHORTHAND_QUANTIFIER_UNRESOLVED"
    assert "经艰苦而始能底定事业" in ca01_035["source_anchor_phrase"]
    assert source_035["source_context"]["resolution_status"] == "INSUFFICIENT_SOURCE_IN_REVIEWED_PASSAGE"
    fire_bell = json.loads(FIRE_BELL_EVIDENCE.read_text(encoding="utf-8"))
    assert any(
        evidence["evidence_id"] == "FB08"
        and evidence["source_span_verified"] is True
        for evidence in fire_bell["evidence"]
    )

    ca01_045 = next(item for item in candidates if item["source_rule_id"] == "CA01-045")
    source_045 = context_by_id["CA01-045"]
    assert ca01_045["source_anchor_phrase"] in source_045["source_anchor_phrase"]
    assert ca01_045["source_context"]["inherited_source_rule_ids"] == ["CA01-042", "CA01-044"]
    assert ca01_045["source_context"]["action_prerequisite_status"] == (
        "EXPLICIT_IN_SOURCE_BUT_NOT_REPRESENTED_BY_APPROVED_CHART_FACTS"
    )
    assert ca01_045["condition_status"] == "BLOCKED_NON_CHART_ACTION_PREREQUISITE"
    assert ca01_045["source_anchor_phrase"] == "勉强求变"
    assert "结果反而陷入困境" in source_045["source_anchor_phrase"]

    ca05_469 = next(item for item in candidates if item["source_rule_id"] == "CA05-469")
    audit = DIRECT_TRANSFORM_AUDIT.read_text(encoding="utf-8")
    assert "CA05-469" in audit
    assert "不是疾病或伤害预测" in audit
    assert ca05_469["source"]["pdf_page"] == 72
    assert ca05_469["source_anchor_phrase"] is None
    assert "血光象义引申至职业场景" in ca05_469["source_paraphrase"]
    assert ca05_469["candidate_scope"] == "CAREER_SCENE_NOT_OBSERVED_EVENT"
    assert ca05_469["mapping_status"] == "EXCLUDED_FROM_EVENT_MAPPING"
    assert ca05_469["ontology_node_id"] is None
