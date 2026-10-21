import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "knowledge" / "palaces" / "P01_life" / "wp05"


def _rows():
    with (BASE / "LIFE_SOURCE_GAP_SUPPLEMENT_PP5_9_v0.1.csv").open(
        encoding="utf-8", newline=""
    ) as f:
        return list(csv.DictReader(f))


def test_gap_supplement_census_and_provenance():
    rows = _rows()
    assert len(rows) == 77
    assert len({r["projection_rule_id"] for r in rows}) == len(rows)
    assert all(r["projection_rule_id"].startswith("P01-SG-") for r in rows)
    assert all(r["source_id"] == "SRC-ZZ-003" for r in rows)
    assert all(r["canonical_promotion"] == "true" for r in rows)
    assert all(r["source_epistemic"] == "EXPLICIT" for r in rows)
    assert all(r["source_gap_id"].startswith("P01-SRC-GAP-") for r in rows)


def test_all_prior_gap_ids_closed_without_duplicate_021():
    ledger = json.loads(
        (BASE / "LIFE_SOURCE_GAP_CLOSURE_LEDGER_PP5_9_v0.1.json").read_text(
            encoding="utf-8"
        )
    )
    entries = {e["gap_id"]: e for e in ledger["entries"]}
    assert len(entries) == 21
    assert all(f"P01-SRC-GAP-{i:03d}" in entries for i in range(1, 22))
    assert all(entries[f"P01-SRC-GAP-{i:03d}"]["status"] != "UNRESOLVED" for i in range(1, 22))
    assert entries["P01-SRC-GAP-021"]["status"] == "ALREADY_COVERED_BY_CANONICAL_RULE"
    assert entries["P01-SRC-GAP-021"]["rule_ids"] == ["P02-200"]
    assert ledger["unresolved_prior_gap_ids"] == []


def test_source_scope_and_cross_palace_constraints():
    rows = {r["projection_rule_id"]: r for r in _rows()}
    assert rows["P01-SG-001"]["cross_palace_dependency"] == "夫妻宫太阳"
    assert rows["P01-SG-021"]["projection_mode"] == "STATE_EXPRESSION"
    assert rows["P01-SG-054"]["cross_palace_dependency"] == ""
    assert "独立落点" in rows["P01-SG-054"]["notes"]
    assert rows["P01-SG-011"]["archived_primary_time_layer"] == "DECADE"
    assert rows["P01-SG-014"]["archived_primary_time_layer"] == "YEAR"
    assert rows["P01-SG-015"]["archived_primary_time_layer"] == "DECADE_YEAR"
    assert rows["P01-SG-026"]["opposite_palace_dependency"] == ""
    assert "日月全璧" in rows["P01-SG-026"]["source_literal_claim"]
    assert "殉/陡" in rows["P01-SG-027"]["source_text_uncertainty"]
    assert rows["P01-SG-028"]["case_support_only"] == "true"
    assert rows["P01-SG-032"]["archived_primary_time_layer"] == "DECADE_YEAR"
    assert rows["P01-SG-046"]["case_support_only"] == "true"
    assert rows["P01-SG-047"]["case_support_only"] == "true"


def test_historical_and_event_claims_are_bounded():
    rows = _rows()
    cases = [r for r in rows if r["case_support_only"] == "true"]
    assert len(cases) == 13
    case_ids = {r["projection_rule_id"] for r in cases}
    assert {"P01-SG-001", "P01-SG-007", "P01-SG-022", "P01-SG-023"} <= case_ids
    assert {"P01-SG-037", "P01-SG-038", "P01-SG-039", "P01-SG-046", "P01-SG-047"} <= case_ids
    assert all(r["event_specificity"] == "CONCRETE_EVENT" for r in cases)


def test_time_scope_sidecar_preserves_generic_and_multi_layer_language():
    data = json.loads(
        (BASE / "LIFE_SOURCE_GAP_TIME_SCOPE_PP5_9_v0.1.json").read_text(
            encoding="utf-8"
        )
    )
    records = data["records"]
    assert len(records) == 77
    by_id = {r["projection_rule_id"]: r for r in records}
    assert by_id["P01-SG-015"]["source_time_layers"] == ["DECADE", "YEAR"]
    assert by_id["P01-SG-026"]["source_time_layers"] == ["NATAL"]
    assert by_id["P01-SG-032"]["source_time_layers"] == ["DECADE", "YEAR"]
    assert by_id["P01-SG-018"]["source_time_layers"] == []
    assert by_id["P01-SG-018"]["scope_status"] == "SOURCE_TEMPORAL_LAYER_UNSPECIFIED"
    assert by_id["P01-SG-011"]["source_time_expression"] == "大运"
    assert by_id["P01-SG-015"]["source_time_expression"] == "流年大运"
    assert by_id["P01-SG-030"]["source_time_expression"] == "大限流年"
    assert by_id["P01-SG-043"]["source_time_expression"] == "运限流年"
    assert by_id["P01-SG-048"]["source_time_expression"] == "人生枢纽"
    assert by_id["P01-SG-077"]["source_time_expression"] == "大运流年"
    assert by_id["P01-SG-050"]["source_time_layers"] == ["YEAR"]


def test_summary_has_no_new_shared_semantics():
    data = json.loads(
        (BASE / "LIFE_SOURCE_GAP_SUMMARY_PP5_9_v0.1.json").read_text(
            encoding="utf-8"
        )
    )
    s = data["summary"]
    assert s["new_canonical_records"] == 77
    assert s["case_support_only"] == 13
    assert s["cumulative_canonical_records_after_merge"] == 277
    assert s["cumulative_reusable_projection_rules_after_merge"] == 213
    assert s["cumulative_case_support_only_after_merge"] == 64
    assert s["new_primitive_qi"] == 0
    assert s["new_memory_type"] == 0
    assert s["new_independent_time_scale"] == 0
    assert s["numeric_weight"] == 0
    assert s["probability"] == 0
    assert data["shared_semantic_gaps"] == []
    assert data["human_gate_required"] is False
