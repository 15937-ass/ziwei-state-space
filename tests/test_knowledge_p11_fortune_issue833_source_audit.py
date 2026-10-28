import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WP = ROOT / "knowledge/palaces/P11_fortune/wp05"


def data():
    return json.loads((WP / "FORTUNE_FD02_SOURCE_AUDIT_v0.1.json").read_text())


def test_continuous_ids_counts_and_accepted_prior_do_not_lose_held_evidence():
    d = data()
    rows = d["records"]
    assert [r["projection_rule_id"] for r in rows] == [f"P11S-{i:03}" for i in range(80, 153)]
    old_bytes = (ROOT / d["accepted_prior"]["path"]).read_bytes()
    assert hashlib.sha256(old_bytes).hexdigest() == d["accepted_prior"]["sha256"]
    old = json.loads(old_bytes)
    assert d["accepted_prior"]["source_gap_ids"] == [g["gap_id"] for g in old["source_coverage_gaps"]]
    assert len(d["accepted_prior"]["source_gap_ids"]) == 9
    accepted = [r for r in rows if r["canonical_promotion"]]
    assert len(accepted) == 60
    assert sum(r["case_support_only"] for r in accepted) == 12
    assert sum(not r["case_support_only"] for r in accepted) == 48
    for key in d["cumulative"]:
        assert d["cumulative"][key] == old["summary"][key] + d["summary"][key]
    assert d["cumulative"]["source_atoms_reviewed"] == 152
    assert d["cumulative"]["source_records_added"] == 124
    assert d["cumulative"]["held"] == 28


def test_source_paragraphs_and_page_halves_exclude_ziwei_and_wuqu():
    d = data()
    assert {r["source_anchor"] for r in d["records"]} == {f"T{i:02}" for i in range(1, 19)} | {f"S{i:02}" for i in range(1, 16)}
    assert [(x["printed_page"], x["pdf_physical_page"], x["half"]) for x in d["source_section_inventory"]] == [(168, 84, "RIGHT"), (169, 85, "LEFT")]
    assert all(r["printed_page"] in [168, 169] and r["pdf_physical_page"] == (r["printed_page"] + 1) // 2 for r in d["records"])
    assert "武曲" in d["next_source_anchor"]
    assert len(d["records"]) + len(d["source_coverage_gaps"]) + len(d["source_section_inventory"]) == d["summary"]["durable_review_object_count"] == 80


def test_literally_damaged_conditions_and_unspecified_subjects_stay_held():
    d = data()
    rows = {r["projection_rule_id"]: r for r in d["records"]}
    affected = [i for g in d["source_coverage_gaps"] for i in g["affected_record_ids"]]
    assert len(affected) == len(set(affected)) == 13
    assert set(affected) == {i for i, r in rows.items() if not r["canonical_promotion"]}
    for i in affected:
        assert rows[i]["normalization_epistemic"] == "UNRESOLVED"
        assert not rows[i]["normalization_verified"]
    assert any("如火铃" in r["source_span"] and not r["canonical_promotion"] for r in rows.values())
    assert any("阿度" in r["source_span"] and not r["canonical_promotion"] for r in rows.values())
    assert any("命宫若又不" in r["source_span"] and r["case_support_only"] and not r["canonical_promotion"] for r in rows.values())
    assert any("文曲化忌是否必须并取未定" in r["condition"] and not r["canonical_promotion"] for r in rows.values())


def test_night_day_and_star_specific_transformations_are_not_conflated():
    rows = data()["records"]
    night = [r for r in rows if r["source_anchor"] == "S04"]
    day = [r for r in rows if r["source_anchor"] == "S05"]
    assert all("夜生" in r["condition"] for r in night)
    assert all("日生" in r["condition"] for r in day)
    assert "丑未" in night[0]["condition"]
    assert "不擅加" in day[-1]["normalized_claim"] and "巨门化忌" in day[-1]["normalized_claim"]
    moon_sun = [r for r in rows if r["source_anchor"] == "S09"]
    assert "太阳化忌" in moon_sun[1]["condition"]
    assert "太阴化忌" in moon_sun[2]["condition"]
    assert any(r["source_anchor"] == "T15" and "太阴化禄" in r["condition"] for r in rows)


def test_clinical_sexual_and_specific_identity_claims_never_become_runtime():
    rows = data()["records"]
    for r in rows:
        if r["source_anchor"] in {"T10", "T12", "T16", "T17", "S14", "S15"}:
            assert r["case_support_only"] and r["case_support_reason"]
        assert r["source_epistemic"] in {"EXPLICIT", "UNRESOLVED_SOURCE", "INFERRED_FROM_SOURCE"}
        assert r["review_status"] == "SOURCE_SPAN_VERIFIED"
        assert r["scene_id"] == "mental_enjoyment"
        assert r["source_span_verified"] and r["reviewer_id"] and r["reviewed_at"]
        assert not r["executable"] and not r["canonical_mapping_approved"]
        assert r["primary_time_layer"] == r["time_layer"] == "NATAL"
        assert r["source_time_expression"] is None
    assert all(data()["execution_boundary"][k] == 0 for k in ["history_feedback", "conditions_compiled", "execution_unlocked", "canonical_mapping_promotions", "new_independent_time_scale", "numeric_weight", "probability", "decay"])
