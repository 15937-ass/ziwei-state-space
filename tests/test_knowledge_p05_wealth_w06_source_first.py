import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "knowledge" / "palaces" / "P05_wealth" / "w06"
STATE = ROOT / "knowledge" / "states" / "P05_WEALTH_STATE.yaml"
W05_GAP_LEDGER = ROOT / "knowledge" / "palaces" / "P05_wealth" / "w05" / "WEALTH_W05_SOURCE_GAP_CLOSURE_LEDGER_v0.1.json"


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_w06_source_first_census_and_boundary():
    data = read_json(BASE / "WEALTH_W06_SOURCE_READJUDICATION_501_600_v0.1.json")
    rows = data["records"]
    assert len(rows) == 62
    assert [r["projection_rule_id"] for r in rows] == [f"W06-{i}" for i in range(501, 563)]
    assert data["candidate_inputs"]["legacy_candidate_files_found"] == 0
    assert data["candidate_inputs"]["historical_candidates_reviewed"] == 0
    assert data["candidate_inputs"]["upper_id_window"] == "W06-501…W06-600"
    assert data["source_basis"]["sha256"] == "6bddb3cac2e4b4efcf265229cbda22904ab3394aeef832e338ee5939088e5c5c"
    assert rows[0]["source_location"] == "财帛宫printed_p82"
    assert all(r["source_location"] == "财帛宫printed_p83" for r in rows[1:25])
    assert all(r["source_location"] == "财帛宫printed_p84" for r in rows[25:54])
    assert rows[54]["source_location"] == "财帛宫printed_p84-85"
    assert all(r["source_location"] == "财帛宫printed_p85" for r in rows[55:])
    assert sum(r["canonical_promotion"] is True for r in rows) == 59
    assert {r["projection_rule_id"] for r in rows if r["canonical_promotion"] is False} == {"W06-540", "W06-542", "W06-559"}
    assert all(r["case_support_only"] is False for r in rows)
    assert all(r["archived_candidate_condition"] is None for r in rows)
    assert rows[0]["source_digest"].startswith("天府守财帛宫，不主富厚")
    assert rows[24]["source_digest"] == "巳亥天府亦最不喜会刑忌夹的天相，主受财政压力。"
    assert rows[25]["projection_rule_id"] == "W06-526"
    assert rows[-1]["source_digest"] == "太阴在十二宫，唯居巳亥守财帛宫主贵不主富，此点最宜再三注意。"
    assert "printed p84" in data["source_basis"]["note"]
    assert "8 太阴" in data["source_basis"]["note"]
    assert "printed p85" in data["source_basis"]["note"]
    assert "9 贪狼" in data["source_basis"]["note"]


def test_w06_temporal_scope_stays_natal_and_tracks_only_source_ordered_paths():
    data = read_json(BASE / "WEALTH_W06_SOURCE_TIME_SCOPE_501_600_v0.1.json")
    assert data["counts"] == {"non_natal_rows": 0, "year": 0, "decade": 0, "path_dependent_gate_rows": 4, "source_age_qualifier_rows": 0}
    assert data["exact_non_natal_ids"] == []
    assert data["decade_ids"] == []
    assert data["year_ids"] == []
    assert data["path_dependent_gate_ids"] == ["W06-535", "W06-546", "W06-547", "W06-555"]
    assert data["records"] == []
    assert {r["projection_rule_id"] for r in data["path_records"]} == {"W06-535", "W06-546", "W06-547", "W06-555"}
    assert all(r["time_layer"] == "NATAL" and r["no_numeric_generalization"] is True for r in data["path_records"] )
    assert data["source_age_qualifier_records"] == []


def test_w06_state_counts_and_source_gap_carry_forward():
    data = read_json(BASE / "WEALTH_W06_SOURCE_READJUDICATION_501_600_v0.1.json")
    s = data["summary"]
    assert s["direct_source_first_records_created"] == 62
    assert s["current_batch_records_created"] == 37
    assert s["canonical_promotions"] == 59
    assert s["reusable_projection_rules"] == 59
    assert s["case_support_only"] == 0
    assert s["cumulative_canonical_records_after_merge"] == 563
    assert s["cumulative_reusable_projection_rules_after_merge"] == 563
    assert s["cumulative_source_gap_supplement_records_after_merge"] == 4
    assert s["unresolved_source_uncertainty_count"] == 3
    assert s["source_coverage_gap_count"] == 3
    assert s["path_dependent_gate_count"] == 4
    assert s["open_source_gap_ids_current_batch"] == ["W06-SG-001", "W06-SG-002", "W06-SG-003"]
    gap_ledger = read_json(W05_GAP_LEDGER)
    gap = next(g for g in gap_ledger["entries"] if g["gap_id"] == "W05-SG-002")
    assert gap["status"] == "PARTIALLY_RESOLVED"
    assert "有是非词不达意讼" in gap["reason"]
    state = STATE.read_text(encoding="utf-8")
    assert "merged_rule_count: 566" in state
    assert "current_batch_rule_count: 37" in state
    assert "source_gap_supplement_record_count: 4" in state
    assert "source_coverage_gaps_remaining: 4" in state
    assert "W05-SG-002" in state and "PARTIALLY_RESOLVED" in state
    assert "source_uncertainty_count_current_batch: 3" in state
    assert "path_dependent_gate_count_current_batch: 4" in state
    assert "source_coverage_gap_count_current_batch: 3" in state
    assert "W06-SG-001" in state and "W06-SG-003" in state
    assert "printed p86" in state
    assert "No Product/runtime authorization is implied" in state

def test_w06_tianfu_structured_rules_preserve_source_branches_and_dependencies():
    data = read_json(BASE / "WEALTH_W06_SOURCE_READJUDICATION_501_600_v0.1.json")
    rows = {row["projection_rule_id"]: row for row in data["records"]}

    # Baseline storage/management ability is distinct from the source's wealth-formation gate.
    r501 = rows["W06-501"]
    assert "基础储财/理财能力不以见禄为条件" in r501["canonical_condition"]
    assert "成富局另须见禄（禄存或化禄均可）" in r501["canonical_condition"]
    assert "saving_and_management_without_automatic_wealth" in r501["canonical_target"]
    assert "wealth_formation_requires_lu_cun_or_hua_lu" in r501["canonical_target"]
    assert "不主富厚" in r501["source_digest"]

    # Direction remains unresolved until both named palaces are reviewed.
    r509 = rows["W06-509"]
    assert "命宫及福德宫" in r509["canonical_condition"]
    assert "骗人/受骗方向" in r509["canonical_condition"]
    assert "direction_unresolved" in r509["canonical_target"]
    assert "命宫及福德宫" in r509["source_digest"]

    # The quoted classic branch is preserved separately from this passage's entry gate.
    r511 = rows["W06-511"]
    assert "原文所引古诀分支" in r511["canonical_condition"]
    assert "不权则富" in r511["canonical_condition"]
    assert "加羊陀冲守则宜僧道" in r511["canonical_condition"]
    assert "入格条件：见禄、权、科及吉曜" in r511["canonical_condition"]
    assert "separately_from_entry_gate" in r511["canonical_target"]
    assert "日月夹财，不权则富，加羊陀冲守则宜僧道" in r511["source_digest"]

    # Preserve both stated branches without inventing a criterion for "good"/"bad nature".
    r513 = rows["W06-513"]
    assert "性质优良/不佳" in r513["canonical_condition"]
    assert "favorable_nature_may_be_yinhui_leader" in r513["canonical_target"]
    assert "unfavorable_nature_may_cause_incidents" in r513["canonical_target"]
    assert "nature_criteria_unspecified" in r513["canonical_target"]
    assert "性质优良者" in r513["source_digest"]
    assert "若性质不佳，则主生事端" in r513["source_digest"]

    # Preserve the source's qualitative cross-configuration comparison without numeric weights.
    r516 = rows["W06-516"]
    assert "financial_authority_greater_than_chouwei_tianfu" in r516["canonical_target"]
    assert "大于丑未宫天府" in r516["source_digest"]
    assert "no numeric weight or ratio is inferred" in r516["source_note"]

def test_w06_taiyin_source_gap_ledger_preserves_literal_ambiguities():
    data = read_json(BASE / "WEALTH_W06_SOURCE_GAPS_501_600_v0.1.json")
    ledger = read_json(BASE / "WEALTH_W06_SOURCE_GAP_CLOSURE_LEDGER_501_600_v0.1.json")
    assert data["gap_count"] == 3
    assert data["core_gap_count"] == 0
    gaps = {g["gap_id"]: g for g in data["gaps"]}
    assert set(gaps) == {"W06-SG-001", "W06-SG-002", "W06-SG-003"}
    assert all(g["status"] == "OPEN" and g["core_gap"] is False for g in gaps.values())
    assert "被绰或遗失" in gaps["W06-SG-001"]["source_claim"]
    assert "卯本太阴" in gaps["W06-SG-002"]["source_claim"]
    assert "性质不占时" in gaps["W06-SG-003"]["source_claim"]
    assert ledger["open_gap_count"] == 3
    assert ledger["fully_closed_gap_count"] == 0
    assert ledger["unresolved_prior_gap_ids"] == ["W05-SG-002"]
    assert ledger["shared_semantic_gaps"] == []


def test_w06_taiyin_source_order_and_literal_ambiguities_are_retained():
    data = read_json(BASE / "WEALTH_W06_SOURCE_READJUDICATION_501_600_v0.1.json")
    rows = {r["projection_rule_id"]: r for r in data["records"]}
    assert rows["W06-540"]["source_uncertainty"] is not None
    assert rows["W06-540"]["canonical_promotion"] is False
    assert rows["W06-542"]["source_uncertainty"] is not None
    assert rows["W06-542"]["canonical_promotion"] is False
    assert rows["W06-559"]["source_uncertainty"] is not None
    assert rows["W06-559"]["canonical_promotion"] is False
    assert "被绰或遗失" in rows["W06-540"]["source_digest"]
    assert "卯本太阴" in rows["W06-542"]["source_digest"]
    assert "性质不占时" in rows["W06-559"]["source_digest"]
    assert rows["W06-535"]["history_feedback"] == "PATH_DEPENDENT_GATE"
    assert rows["W06-546"]["history_feedback"] == "PATH_DEPENDENT_GATE"
    assert rows["W06-547"]["history_feedback"] == "PATH_DEPENDENT_GATE"
    assert rows["W06-555"]["history_feedback"] == "PATH_DEPENDENT_GATE"
    assert all(r["case_support_only"] is False for r in rows.values())

