import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WP = ROOT / "knowledge/palaces/P11_fortune/wp05"


def data():
    return json.loads((WP / "FORTUNE_FD03_SOURCE_AUDIT_v0.1.json").read_text())


def test_fd03_ids_counts_and_all_previous_source_evidence_are_preserved():
    d = data()
    assert [r["projection_rule_id"] for r in d["records"]] == [f"P11S-{i:03}" for i in range(153, 222)]
    accepted = [r for r in d["records"] if r["canonical_promotion"]]
    assert len(accepted) == 57
    assert sum(r["case_support_only"] for r in accepted) == 13
    assert sum(not r["case_support_only"] for r in accepted) == 44
    old_gap_ids = []
    for p in d["accepted_prior"]:
        b = (ROOT / p["path"]).read_bytes()
        assert hashlib.sha256(b).hexdigest() == p["sha256"]
        assert p["gap_ids"] == [g["gap_id"] for g in json.loads(b)["source_coverage_gaps"]]
        old_gap_ids.extend(p["gap_ids"])
    assert len(old_gap_ids) == len(set(old_gap_ids)) == 14
    old = json.loads((WP / "FORTUNE_FD02_SOURCE_AUDIT_v0.1.json").read_text())
    for key in d["cumulative"]:
        assert d["cumulative"][key] == old["cumulative"][key] + d["summary"][key]
    assert d["cumulative"]["source_atoms_reviewed"] == 221
    assert d["cumulative"]["source_records_added"] == 181
    assert d["cumulative"]["held"] == 40


def test_fd03_page_and_paragraph_coverage_stops_before_lianzhen():
    d = data()
    assert {r["source_anchor"] for r in d["records"]} == {f"W{i:02}" for i in range(1, 19)} | {f"C{i:02}" for i in range(1, 18)}
    assert [(p["printed_page"], p["pdf_physical_page"], p["half"]) for p in d["source_section_inventory"]] == [(170, 85, "RIGHT"), (171, 86, "LEFT")]
    assert "6 廉贞" in d["source_basis"]["batch_end"]
    assert len(d["records"]) + len(d["source_coverage_gaps"]) + len(d["source_section_inventory"]) == d["summary"]["durable_review_object_count"] == 76
    assert "廉贞" in d["next_source_anchor"]


def test_literal_and_scope_gaps_cannot_silently_promote():
    d = data()
    rows = {r["projection_rule_id"]: r for r in d["records"]}
    affected = [i for g in d["source_coverage_gaps"] for i in g["affected_record_ids"]]
    assert len(affected) == len(set(affected)) == 12
    assert set(affected) == {i for i, r in rows.items() if not r["canonical_promotion"]}
    for i in affected:
        assert rows[i]["normalization_epistemic"] == "UNRESOLVED"
        assert not rows[i]["normalization_verified"]
    assert any("富屋贵人" in r["source_span"] and not r["canonical_promotion"] for r in rows.values())
    assert any("不叮" in r["source_span"] and not r["canonical_promotion"] for r in rows.values())
    assert any(r["source_anchor"] == "C17" and not r["canonical_promotion"] and "未指明" in r["condition"] for r in rows.values())


def test_negatives_and_counterexamples_keep_conditions_and_case_boundaries():
    rows = data()["records"]
    assert any(r["source_anchor"] == "W02" and set(r["cross_palace_dependency"]) == {"疾厄宫", "命宫"} and r["case_support_only"] for r in rows)
    assert any(r["source_anchor"] == "C07" and "不允许" in r["normalized_claim"] and "一概" in r["normalized_claim"] and not r["canonical_promotion"] for r in rows)
    for r in rows:
        if any(k in r["source_span"] for k in ["自闭症", "弱智", "同性恋", "偏食"]):
            assert r["case_support_only"]
    transformations = [r["condition"] for r in rows if r["source_anchor"] == "C10"]
    assert any("巨门化忌" in x for x in transformations)
    assert any("天同化忌" in x for x in transformations)
    assert any("巨门化禄" in x for x in transformations)
    assert any("天同化禄" in x for x in transformations)


def test_source_contract_and_runtime_boundaries_remain_separate():
    d = data()
    for r in d["records"]:
        assert r["source_id"] == "SRC-ZZ-003"
        assert r["scene_id"] == "mental_enjoyment"
        assert r["source_epistemic"] in {"EXPLICIT", "UNRESOLVED_SOURCE", "INFERRED_FROM_SOURCE"}
        assert r["review_status"] == "SOURCE_SPAN_VERIFIED" and r["source_span_verified"]
        assert r["reviewer_type"] == "MODEL" and r["reviewer_id"] and r["reviewed_at"]
        assert r["primary_time_layer"] == "NATAL" and r["source_time_expression"] is None
        assert not r["executable"] and not r["canonical_mapping_approved"]
    for k in ["history_feedback", "conditions_compiled", "execution_unlocked", "canonical_mapping_promotions", "new_primitive_qi", "new_independent_time_scale", "probability", "numeric_weight", "decay"]:
        assert d["execution_boundary"][k] == 0
