"""Independent source-stage closure: coverage can close while semantics remain held."""
import hashlib
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "knowledge/palaces/P02_siblings/census/issue_934/P02_CHAPTER_CENSUS_MANIFEST_v0.2.json"
VERDICT = ROOT / "knowledge/palaces/P02_siblings/handoff/issue_928/INDEPENDENT_STAGE_CLOSURE_VERDICT_v0.1.json"
STATE = ROOT / "knowledge/states/P02_SIBLINGS_STATE.yaml"


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_source_stage_closure_is_not_semantic_or_runtime_completion():
    verdict = read(VERDICT)
    state = STATE.read_text(encoding="utf-8")
    assert verdict["verdict"] == "SOURCE_AUDIT_STAGE_CLOSED_WITH_RETAINED_HOLDS"
    assert verdict["stage_closure_authorized"] is True
    assert verdict["whole_chapter_complete"] is True
    assert verdict["all_semantics_resolved"] is False
    assert verdict["completion_scope"] == "BOUNDED_SOURCE_STAGE_ONLY_NOT_SEMANTIC_OR_EMPIRICAL_COMPLETION"
    assert verdict["history_feedback"] == 0
    assert verdict["conditions_compiled"] == 0
    assert verdict["execution_unlocked"] == 0
    assert verdict["formal_mapping_authorized"] is False
    assert verdict["runtime_authorized"] is False
    assert verdict["empirical_validity_claim"] is False
    assert "whole_chapter_complete: true" in state
    assert "all_semantics_resolved: false" in state
    assert "conditions_compiled: 0" in state
    assert "execution_unlocked: 0" in state
    assert "单独核对依赖与实时槽位" in state


def test_source_ids_gap_links_held_index_and_page_coverage_reconcile():
    manifest = read(MANIFEST)
    ledgers = []
    for pin in manifest["frozen_source_ledgers"]:
        path = ROOT / pin["path"]
        assert sha256(path) == pin["sha256"]
        ledgers.append(read(path))

    checkpoints = []
    for pin in manifest["checkpoints"]:
        path = ROOT / pin["path"]
        assert sha256(path) == pin["sha256"]
        checkpoints.append(read(path))

    records = [row for ledger in ledgers for row in ledger["records"]]
    ids = [row["projection_rule_id"] for row in records]
    assert ids == [f"P02S-{n:03d}" for n in range(1, 425)]
    accepted = [row for row in records if row["canonical_promotion"]]
    held = [row for row in records if not row["canonical_promotion"]]
    assert (len(records), len(accepted), len(held)) == (424, 284, 140)
    assert sum(not row["case_support_only"] for row in accepted) == 180
    assert sum(row["case_support_only"] for row in accepted) == 104
    assert all(not row["executable"] and not row["canonical_mapping_approved"] and not row["history_feedback"] for row in records)

    gaps = [gap for ledger in ledgers for gap in ledger["source_coverage_gaps"]]
    affected = [record_id for gap in gaps for record_id in gap["affected_record_ids"]]
    assert len(gaps) == len({gap["gap_id"] for gap in gaps}) == 49
    assert Counter(affected) == Counter(row["projection_rule_id"] for row in held)

    held_indexes = [row for checkpoint in checkpoints if checkpoint.get("role", "").startswith("HELD_ACCOUNTING") for row in checkpoint["records"]]
    held_by_id = {row["projection_rule_id"]: row for row in held}
    assert len(held_indexes) == len({row["record_id"] for row in held_indexes}) == 140
    for item in held_indexes:
        source = held_by_id[item["record_id"]]
        assert item["primary_gap_id"] == source["gap_id"]
        assert item["source_condition_verbatim"] == source["condition"]
        assert item["source_claim_verbatim"] == source["literal_claim"]
        assert item["original_notes"] == source["notes"]
        assert not item["effective_executable"]
        assert not item["effective_normalization_authorized"]
        assert not item["canonical_promotion_by_census"]
    assert sum(bool(item["raw_unresolved_fields_nonnull"]) for item in held_indexes) == 45

    coverage = [checkpoint for checkpoint in checkpoints if checkpoint.get("kind") == "SOURCE_COVERAGE"]
    anchors = [anchor for checkpoint in coverage for anchor in checkpoint["owned_anchors"]]
    owner_ids = [record_id for anchor in anchors for record_id in anchor["record_ids"]]
    page_slice_count = sum(item["paragraph_slice_count"] for checkpoint in coverage for item in checkpoint["page_slices"])
    assert len(anchors) == len({anchor["qualified_anchor_id"] for anchor in anchors}) == 151
    assert Counter(owner_ids) == Counter(ids)
    assert page_slice_count == 155
    assert len(manifest["sections"]) == 14
    assert len(manifest["cross_page_links"]) == 4
    assert all(boundary["direct_visual_verified"] for boundary in manifest["source_basis"]["negative_boundaries"])


def test_w13_erratum_and_source_atom_are_both_preserved_correctly():
    manifest = read(MANIFEST)
    physical14 = read(ROOT / "knowledge/palaces/P02_siblings/census/issue_934/P02_SOURCE_COVERAGE_PHYSICAL_14_v0.2.json")
    erratum = read(ROOT / "knowledge/palaces/P02_siblings/census/issue_934/W13_CENSUS_EVIDENCE_ERRATUM_v0.1.json")
    repair_verdict = read(ROOT / "validation/knowledge/palaces/P02_siblings/issue_934/INDEPENDENT_RECHECK_VERDICT.json")
    for links in (manifest["cross_page_links"], physical14["continuations"]):
        w13 = next(item for item in links if item["qualified_anchor_id"] == "SB04:W13")
        assert w13["left_tail"] == "为武曲、破"
        assert w13["right_head"] == "军、七杀躔兄弟宫之年"
    assert erratum["corrected_value"] == "为武曲、破"
    for path, expected in repair_verdict["reviewed_file_sha256"].items():
        assert sha256(ROOT / path) == expected

    source = read(ROOT / "knowledge/palaces/P02_siblings/wp05/SIBLINGS_SB04_WUQU_SOURCE_AUDIT_v0.1.json")
    row = next(item for item in source["records"] if item["projection_rule_id"] == "P02S-167")
    assert row["condition"] == "不利之克应，为武曲、破军、七杀躔兄弟宫之年"
    assert row["time_layer"] == "YEAR"
    assert row["gap_id"] == "P02-SB04-GAP-C01"
    assert not row["canonical_promotion"] and not row["executable"]


def test_primary_core_gaps_remain_fail_closed_and_unmigrated():
    ledgers = {
        "SB06": read(ROOT / "knowledge/palaces/P02_siblings/wp05/SIBLINGS_SB06_LIANZHEN_SOURCE_AUDIT_v0.1.json"),
        "SB11": read(ROOT / "knowledge/palaces/P02_siblings/wp05/SIBLINGS_SB11_QISHA_POJUN_SOURCE_AUDIT_v0.1.json"),
    }
    by_id = {row["projection_rule_id"]: row for ledger in ledgers.values() for row in ledger["records"]}
    for record_id in ("P02S-261", "P02S-414", "P02S-416", "P02S-417"):
        row = by_id[record_id]
        assert row["disposition"] == "HELD_FAIL_CLOSED"
        assert not row["canonical_promotion"]
        assert not row["canonical_mapping_approved"]
        assert not row["executable"]
    assert by_id["P02S-261"]["gap_id"] == "P02-SB06-GAP-G01"
    assert {by_id[key]["gap_id"] for key in ("P02S-414", "P02S-416", "P02S-417")} == {"P02-SB11-GAP-C04"}
