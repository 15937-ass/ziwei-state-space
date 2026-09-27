from pathlib import Path

from src.audit_repository import (
    audit_modifier_catalog,
    audit_review_fields,
    audit_rule_catalog,
    composite_condition_score,
    effective_sixty_system_rows,
    outcome_operator_candidates,
    semantic_duplicate_candidates,
)


def v03():
    return {
        "source_epistemic": "EXPLICIT",
        "normalization_epistemic": "UNRESOLVED",
        "review_status": "MODEL_SELF_REVIEWED",
        "reviewer_type": "MODEL",
        "reviewer_id": "legacy-gpt-pipeline",
        "reviewed_at": "",
        "source_span_verified": "false",
        "normalization_verified": "false",
        "normalization_rationale": "",
    }


def test_illegal_rule_target_type_is_p0():
    rows = [{
        "rule_id": "R-1",
        "target_type": "inference_rule",
        "operator": "condition",
        "state_change": "none",
        "valence": "not_applicable",
        "source_location": "p1",
        **v03(),
    }]
    findings = audit_rule_catalog(Path("x.csv"), rows)
    assert any(f.severity == "P0" and f.field == "target_type" for f in findings)


def test_illegal_modifier_operator_is_p0():
    rows = [{
        "operator_rule_id": "M-1",
        "operator_type": "time_scale_effect",
        "source_location": "p2",
        **v03(),
    }]
    findings = audit_modifier_catalog(Path("m.csv"), rows)
    assert any(f.severity == "P0" and f.field == "operator_type" for f in findings)


def test_v03_review_fields_are_required():
    findings = audit_review_fields(Path("x.csv"), [{"rule_id": "R-0"}])
    assert any(f.severity == "P0" and f.field == "source_epistemic" for f in findings)


def test_model_review_is_not_source_verification():
    row = {"rule_id": "R-0", **v03()}
    assert not audit_review_fields(Path("x.csv"), [row])
    assert row["source_span_verified"] == "false"


def test_verified_status_requires_verified_source_span():
    row = {"rule_id": "R-0", **v03()}
    row["review_status"] = "SOURCE_SPAN_VERIFIED"
    findings = audit_review_fields(Path("x.csv"), [row])
    assert any(f.field == "source_span_verified" for f in findings)


def test_implementation_normalization_requires_rationale():
    row = {"rule_id": "R-0", **v03()}
    row["normalization_epistemic"] = "IMPLEMENTATION"
    findings = audit_review_fields(Path("x.csv"), [row])
    assert any(f.field == "normalization_rationale" for f in findings)


def test_composite_condition_is_only_review_heuristic():
    assert composite_condition_score("A或B/C、D") >= 2
    assert composite_condition_score("单一条件") == 0


def test_outcome_directional_operator_is_layer_review_candidate():
    rows = [{
        "rule_id": "R-2",
        "target_type": "outcome_descriptor",
        "operator": "enhance",
        "source_location": "p3",
    }]
    findings = outcome_operator_candidates(Path("x.csv"), rows)
    assert findings
    assert findings[0].severity == "P1"


def test_system_sidecar_applies_non_destructive_override(tmp_path):
    canonical = tmp_path / "knowledge/rules/systems"
    review = tmp_path / "knowledge/review"
    migration = tmp_path / "knowledge/migrations"
    canonical.mkdir(parents=True)
    review.mkdir(parents=True)
    migration.mkdir(parents=True)

    (canonical / "sixty_systems_canonical_v0.1.csv").write_text(
        "rule_id,source_location,target_type,operator,state_change,valence,condition\n"
        "R-1,p1,inference_rule,condition,none,not_applicable,x\n",
        encoding="utf-8",
    )
    (review / "sixty_systems_review_v0.3.csv").write_text(
        "rule_id,source_epistemic,normalization_epistemic,review_status,reviewer_type,"
        "reviewer_id,reviewed_at,source_span_verified,normalization_verified,normalization_rationale\n"
        "R-1,EXPLICIT,IMPLEMENTATION,MODEL_SELF_REVIEWED,MODEL,legacy-gpt-pipeline,,false,false,repair\n",
        encoding="utf-8",
    )
    (migration / "a0_sixty_systems_schema_overrides_v0.1.csv").write_text(
        "rule_id,field,old_value,new_value,normalization_epistemic,rationale\n"
        "R-1,target_type,inference_rule,structural_relation,IMPLEMENTATION,repair\n",
        encoding="utf-8",
    )

    rows, findings = effective_sixty_system_rows(tmp_path)
    assert not findings
    assert rows[0]["target_type"] == "structural_relation"


def test_semantic_duplicate_is_p1_review_candidate_not_auto_delete():
    rows = [
        {
            "rule_id": "R-A",
            "system_no": "51",
            "condition": "日月吉化吉会",
            "target_literal": "两类皆佳，但情感型偏安逸，物欲型偏奔波",
            "source_location": "p140",
        },
        {
            "rule_id": "R-B",
            "system_no": "51",
            "condition": "日月吉化吉会",
            "target_literal": "两类皆佳，但情感型偏安逸、物欲型偏奔波",
            "source_location": "p140",
        },
    ]
    findings = semantic_duplicate_candidates(Path("systems.csv"), rows)
    assert len(findings) == 2
    assert all(f.severity == "P1" for f in findings)
    assert all(f.category == "semantic_duplicate_candidate" for f in findings)
