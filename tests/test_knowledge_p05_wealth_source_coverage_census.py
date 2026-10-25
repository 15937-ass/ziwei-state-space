import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CENSUS = ROOT / "knowledge/palaces/P05_wealth/coverage/WEALTH_P05_SOURCE_COVERAGE_CENSUS_P69_P92_v0.1.json"
STATE = ROOT / "knowledge/states/P05_WEALTH_STATE.yaml"
W10 = ROOT / "knowledge/palaces/P05_wealth/w10/WEALTH_W10_LIANZHEN_SOURCE_READJUDICATION_P81_P82_v0.1.json"
TIME = ROOT / "knowledge/palaces/P05_wealth/w10/WEALTH_W10_LIANZHEN_SOURCE_TIME_SCOPE_P81_P82_v0.1.json"
GAPS = ROOT / "knowledge/palaces/P05_wealth/w10/WEALTH_W10_LIANZHEN_SOURCE_GAPS_P81_P82_v0.1.json"
SOURCE_HASH = "6bddb3cac2e4b4efcf265229cbda22904ab3394aeef832e338ee5939088e5c5c"

def load(path):
    return json.loads(path.read_text(encoding="utf-8"))

def test_source_hash_and_printed_boundary_are_explicit():
    data = load(CENSUS)
    assert data["source_basis"]["source_id"] == "SRC-ZZ-003"
    assert data["source_basis"]["sha256"] == SOURCE_HASH
    assert data["source_basis"]["boundary_literals"]["start"] == "财帛宫"
    assert data["source_basis"]["boundary_literals"]["stop"] == "疾厄宫"
    assert data["source_basis"]["printed_span"].startswith("p69")
    assert "p92" in data["source_basis"]["printed_span"]
    pages = data["physical_page_map"]
    assert pages[0] == {"physical_pdf_page": 35, "printed_pages": "69–70"}
    assert pages[-1] == {"physical_pdf_page": 47, "printed_pages": "93–94"}

def test_source_first_counts_reconcile_without_quota_filling():
    data = load(CENSUS)
    counts = data["record_census"]
    assert counts["source_first_review_records"] == 844
    assert counts["source_first_canonical_promotions"] == 827
    assert counts["source_first_unpromoted"] == 17
    assert counts["p81_supplement_records"] == 4
    assert counts["total_records_accounted"] == 848
    assert counts["total_canonical_reusable_records"] == 831
    assert counts["case_support_only_records"] == 0
    expected_held = {"W06-540", "W06-542", "W06-559", "W06-596", "W08-761", "W08-766", "W08-767", "W08-820", "W09-865", "W09-881", "W09-882", "W09-904", "W09-909", "W10-925", "W10-926", "W10-929", "W10-953"}
    assert set(counts["unpromoted_rule_ids"]) == expected_held
    assert len(counts["unpromoted_dispositions"]) == 17
    batches = data["accepted_batches"]
    assert len(batches) == 15
    assert sum(b["source_first_review_records"] for b in batches) == 844
    assert sum(b["unpromoted_records"] for b in batches) == 17
    assert sum(b["supplement_records"] for b in batches) == 4
    assert len({b["batch_id"] for b in batches}) == len(batches)

def test_all_26_explicit_residual_gap_ids_are_retained_separately():
    ledger = load(CENSUS)["explicit_residual_gap_ledger"]
    expected = ({"W05-SG-002"} | {f"W06-SG-{i:03d}" for i in range(1, 6)} | {f"W08-SG-{i:03d}" for i in range(1, 6)} | {f"W09-SG-{i:03d}" for i in range(6, 17)} | {f"W10-SG-{i:03d}" for i in range(1, 5)})
    assert ledger["explicit_gap_id_count"] == 26
    assert set(ledger["gap_ids"]) == expected
    assert ledger["status_counts"] == {"PARTIALLY_RESOLVED": 1, "OPEN": 25}
    assert all(g["disposition"].startswith("RETAINED_") for g in ledger["gaps"])

def test_eight_w01_w02_record_uncertainties_are_not_double_counted():
    rows = load(CENSUS)["record_level_uncertainties"]
    assert rows["count"] == 8
    assert set(rows["rule_ids"]) == {"W01-047", "W01-056", "W01-069", "W01-074", "W01-076", "W01-077", "W02-138", "W02-139"}
    assert all(r["status"] == "PRESERVED_RECORD_LEVEL_UNCERTAINTY" for r in rows["entries"])

def test_lianzheng_tail_is_accounted_with_explicit_residual_ambiguities():
    data = load(CENSUS)
    disposition = data["disposition"]
    assert disposition["source_span_coverage"] == "COMPLETE_WITH_EXPLICIT_RESIDUAL_AMBIGUITIES"
    assert disposition["uncovered_source_spans"] == 0
    assert disposition["total_open_coverage_items"] == 26
    assert disposition["next_palace_ready"] is True
    assert "After PR #780 is accepted and merged" in disposition["next_step"]
    gap = data["uncovered_source_spans"][0]
    assert gap["gap_id"] == "P05-COV-GAP-001"
    assert gap["status"] == "CLOSED_BY_SOURCE_FIRST_REVIEW"
    assert "W10-923…W10-963" in gap["closure_evidence"]["record_ids"]
    assert "7 天府" in gap["end_boundary"]

def test_w10_source_first_records_and_four_holds_reconcile():
    data = load(W10)
    assert data["source_basis"]["sha256"] == SOURCE_HASH
    assert len(data["records"]) == 41
    assert len({r["projection_rule_id"] for r in data["records"]}) == 41
    assert sum(r["canonical_promotion"] for r in data["records"]) == 37
    assert {r["projection_rule_id"] for r in data["records"] if not r["canonical_promotion"]} == {"W10-925", "W10-926", "W10-929", "W10-953"}
    assert all(r["time_layer"] in {"NATAL", "YEAR"} for r in data["records"])
    assert "畅顺耳" in next(r["source_digest"] for r in data["records"] if r["projection_rule_id"] == "W10-925")
    assert "至少" in next(r["source_digest"] for r in data["records"] if r["projection_rule_id"] == "W10-926")
    assert next(r["source_digest"] for r in data["records"] if r["projection_rule_id"] == "W10-923") == "丑未宫『廉贞，七杀』同度，在未宫为『雄宿乾元格』，若得禄则可成富格，唯仍须历艰辛。"
    assert next(r["source_digest"] for r in data["records"] if r["projection_rule_id"] == "W10-925") == "唯财源不如在未宫之畅顺耳。"
    assert next(r["source_digest"] for r in data["records"] if r["projection_rule_id"] == "W10-941") == "若同时见煞刑耗曜，且主词讼。"
    assert next(r["source_digest"] for r in data["records"] if r["projection_rule_id"] == "W10-943") == "卯酉宫『廉贞破军』同度，财源不稳定。"
    assert next(r["source_digest"] for r in data["records"] if r["projection_rule_id"] == "W10-944") == "若破军化禄，往往须兼行兼职。"
    assert "破军化禄" in next(r["canonical_condition"] for r in data["records"] if r["projection_rule_id"] == "W10-944")
    assert "二者任一化禄" in next(r["canonical_condition"] for r in data["records"] if r["projection_rule_id"] == "W10-956")
    assert "与火铃同度" in next(r["canonical_condition"] for r in data["records"] if r["projection_rule_id"] == "W10-956")
    assert data["summary"]["cumulative_reusable_projection_rules_after_merge"] == 831

def test_w10_time_scope_preserves_only_the_explicit_year_condition():
    sidecar = load(TIME)
    assert sidecar["year_ids"] == ["W10-948"]
    assert sidecar["decade_ids"] == []
    assert sidecar["counts"]["year"] == 1
    assert sidecar["counts"]["decade"] == 0
    assert sidecar["source_time_phrase_records"][0]["source_time_phrase"] == "流年命宫或财帛宫见煞忌刑劫之年为克应"
    assert sidecar["source_time_phrase_records"][0]["scope_status"] == "EXPLICIT_YEAR_RESPONSE_CONDITION"
    assert all(r["no_numeric_generalization"] for r in sidecar["path_records"])

def test_w10_local_source_gaps_are_open_and_not_core_gaps():
    gaps = load(GAPS)
    assert gaps["gap_count"] == 4
    assert gaps["core_gap_count"] == 0
    assert {g["gap_id"] for g in gaps["gaps"]} == {"W10-SG-001", "W10-SG-002", "W10-SG-003", "W10-SG-004"}
    assert all(g["status"] == "OPEN" and g["core_gap"] is False for g in gaps["gaps"])

def test_state_cache_tracks_active_p05_tail_audit_without_authorizing_product():
    state = STATE.read_text(encoding="utf-8")
    assert 'status: "ACTIVE"' in state
    assert "active_issue: 777" in state
    assert 'active_branch: "knowledge/p05-777-source-first-lianzhen-tail-p81-p82"' in state
    assert "merged_rule_count: 794" in state
    assert "reviewed_rule_count: 844" in state
    assert "source_coverage_gaps_remaining: 26" in state
    assert "P05-COV-GAP-001" in state
    assert "SOURCE_SPAN_ACCOUNTED_PENDING_ACCEPTANCE" in state
    assert "No Product/runtime authorization is implied" in state
