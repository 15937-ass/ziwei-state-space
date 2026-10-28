import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "knowledge/palaces/P11_fortune/wp05/FORTUNE_FD01_SOURCE_AUDIT_v0.1.json"


def data():
    return json.loads(PATH.read_text(encoding="utf-8"))


def test_fortune_atoms_reconcile_with_source_dispositions_and_v03_provenance():
    d = data()
    rows = d["records"]
    assert [r["projection_rule_id"] for r in rows] == [f"P11S-{i:03}" for i in range(1, 80)]
    accepted = [r for r in rows if r["canonical_promotion"]]
    held = [r for r in rows if not r["canonical_promotion"]]
    assert len(accepted) == d["summary"]["source_records_added"] == 64
    assert len(held) == d["summary"]["held"] == 15
    assert sum(r["case_support_only"] for r in accepted) == 11
    assert sum(not r["case_support_only"] for r in accepted) == 53
    assert len(rows) + len(d["source_section_inventory"]) + len(d["source_coverage_gaps"]) + len(d["temporal_scope_residuals"]) == d["summary"]["durable_review_object_count"] == 100
    for r in rows:
        assert r["scene_id"] == "mental_enjoyment"
        assert r["source_id"] == "SRC-ZZ-003"
        assert r["source_epistemic"] in {"EXPLICIT", "INFERRED_FROM_SOURCE", "UNRESOLVED_SOURCE"}
        assert r["review_status"] == "SOURCE_SPAN_VERIFIED"
        assert r["source_span_verified"] and r["reviewer_type"] == "MODEL"
        assert r["reviewer_id"] and r["reviewed_at"] and r["source_span"]
        assert r["normalization_epistemic"] in {"SOURCE_PRESERVING", "UNRESOLVED"}
        assert r["pdf_physical_page"] == (r["printed_page"] + 1) // 2


def test_body_page_numbers_and_partial_chapter_coverage_override_toc():
    d = data()
    b = d["source_basis"]
    assert b["attachment_sha256"] == "6bddb3cac2e4b4efcf265229cbda22904ab3394aeef832e338ee5939088e5c5c"
    assert b["full_section_printed_pages"] == list(range(166, 177))
    assert b["page_mapping"]["166"] == 83
    assert b["page_mapping"]["176"] == 88
    assert "p177" in b["boundary_note"]
    inventory = d["source_section_inventory"]
    assert len(inventory) == 11
    assert inventory[0]["half"] == "RIGHT"
    assert inventory[2]["source_content_review_status"] == "ZIWEI_END_ONLY_TIANJI_AND_REMAINDER_NOT_REVIEWED"
    assert all(r["source_content_review_status"] == "NOT_SOURCE_REVIEWED_IN_THIS_BATCH" for r in inventory[3:])
    assert {r["source_anchor"] for r in d["records"]} == {f"G{i:02}" for i in range(1, 13)} | {f"Z{i:02}" for i in range(1, 27)}
    assert "2 天机" in d["next_source_anchor"]


def test_diagnosis_and_specific_identity_assertions_remain_case_only():
    rows = {r["projection_rule_id"]: r for r in data()["records"]}
    for i in [5, 11, 14, 15, 16, 31, 49, 60, 63, 66, 70, 74]:
        r = rows[f"P11S-{i:03}"]
        assert r["case_support_only"]
        assert r["case_support_reason"]
        assert not r["executable"] and not r["canonical_mapping_approved"]
    assert "自闭症" in rows["P11S-015"]["source_span"]
    assert "诊断" in rows["P11S-015"]["normalized_claim"]


def test_unresolved_source_terms_and_antecedents_cannot_be_promoted():
    d = data()
    rows = {r["projection_rule_id"]: r for r in d["records"]}
    gaps = d["source_coverage_gaps"]
    assert len(gaps) == 9
    affected = [i for g in gaps for i in g["affected_record_ids"]]
    assert len(affected) == len(set(affected)) == 15
    assert set(affected) == {i for i, r in rows.items() if not r["canonical_promotion"]}
    for i in affected:
        assert rows[i]["normalization_epistemic"] == "UNRESOLVED"
        assert not rows[i]["normalization_verified"]
    assert "大野" in rows["P11S-025"]["source_span"]
    assert "紫破天府" in rows["P11S-044"]["source_span"]
    assert "有利忌夹" in rows["P11S-057"]["source_span"]
    assert "紫相七杀" in rows["P11S-067"]["source_span"]
    assert "关陀" in rows["P11S-076"]["source_span"]
    scoped = set(gaps[-1]["affected_record_ids"])
    assert scoped == {f"P11S-{i:03}" for i in [42, 43, 53, 54, 55, 63, 64]}
    assert all("是否必要并取未定" in rows[i]["condition"] for i in scoped)
    assert gaps[0]["core_gap"] and gaps[0]["normalized_term"] is None


def test_cross_palace_and_sequential_conditions_are_not_dropped():
    rows = {r["projection_rule_id"]: r for r in data()["records"]}
    for i, palace in [(22, "夫妻宫"), (23, "财帛宫"), (24, "迁移宫")]:
        r = rows[f"P11S-{i:03}"]
        assert "福德星曜不吉但三方星曜好" in r["condition"]
        assert palace in r["cross_palace_dependency"]
    assert "必须见禄" in rows["P11S-069"]["source_span"]
    assert "已见禄" in rows["P11S-070"]["condition"]
    assert rows["P11S-062"]["opposite_palace_dependency"] == "对宫破军"
    assert "上文" in rows["P11S-027"]["normalized_claim"]


def test_method_time_language_does_not_become_period_rules_or_runtime():
    d = data()
    rows = {r["projection_rule_id"]: r for r in d["records"]}
    for i in [17, 21, 79]:
        assert rows[f"P11S-{i:03}"]["primary_time_layer"] is None
    assert rows["P11S-021"]["source_time_expression"] == "大运流年"
    assert all(r["primary_time_layer"] in {None, "NATAL"} for r in rows.values())
    assert d["temporal_scope_residuals"][0]["assigned_time_layer"] is None
    assert all(not r["executable"] and not r["canonical_mapping_approved"] and r["history_feedback"] == 0 for r in rows.values())
    for key in ["history_feedback", "conditions_compiled", "execution_unlocked", "canonical_mapping_promotions", "new_primitive_qi", "new_independent_time_scale", "numeric_weight", "probability", "decay"]:
        assert d["execution_boundary"][key] == 0
    assert not d["execution_boundary"]["product_runtime_authorized"]
