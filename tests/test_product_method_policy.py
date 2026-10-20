import copy
import json
from pathlib import Path

import pytest

from src.product.expert_case_corpus import (
    load_wang_case_bundles,
    load_wang_loco_manifest,
    load_wang_method_patterns,
)
from src.product.expert_method_contracts import compile_inference_trace
from src.product.method_policy import (
    EVIDENCE_STATUSES,
    EvidenceItem,
    POLICY_VERSION,
    assess_patterns,
    audit_wang_method_policy_readiness,
    build_reference_only_evidence,
    classify_source_ref_status,
    load_execution_rules,
    retrieval_payload,
    retrieve_same_domain_cases,
    run_method_policy,
    run_wang_fold,
    validate_execution_rule_coverage,
    validate_retrieval_payload,
)


ROOT = Path(__file__).resolve().parents[1]
SYNTHETIC = ROOT / "product" / "METHOD_POLICY_SYNTHETIC_FIXTURE_v0.1.json"
READINESS = ROOT / "product" / "WANG_METHOD_POLICY_READINESS_v0.1.json"
EXECUTION_RULES = ROOT / "product" / "METHOD_POLICY_EXECUTION_RULES_v0.1.json"


def _load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def _fold(case_id):
    manifest = load_wang_loco_manifest()
    return next(
        item for item in manifest["folds"]
        if item["held_out_case_id"] == case_id
    )


def _case(case_id):
    return next(
        item for item in load_wang_case_bundles()
        if item.case_id == case_id
    )


def test_source_refs_are_not_materialized_facts():
    assert classify_source_ref_status("SOURCE_CHART:WANG-CASE-001") == "SOURCE_REFERENCE_ONLY"
    assert (
        classify_source_ref_status(
            "WANG-ANXING-TUIDUAN:P7:CASE-001:CHART"
        )
        == "SOURCE_REFERENCE_ONLY"
    )
    assert classify_source_ref_status("") == "MISSING"
    assert (
        classify_source_ref_status("MATERIALIZED_FACT:SYNTHETIC:X")
        == "MATERIALIZED_FACT"
    )


def test_wang_case_evidence_is_reference_only():
    for case in load_wang_case_bundles():
        evidence = build_reference_only_evidence(case)
        assert evidence
        assert {item.status for item in evidence} == {"SOURCE_REFERENCE_ONLY"}
        assert all(item.status in EVIDENCE_STATUSES for item in evidence)


def test_execution_adapter_covers_all_source_method_patterns_without_mutating_them():
    patterns = load_wang_method_patterns()
    rules = load_execution_rules()

    validate_execution_rule_coverage(patterns, rules)

    assert set(rules) == {item.pattern_id for item in patterns}
    assert all(item.allowed_use == "SEMANTIC_ONLY" for item in patterns)

    assert rules["WT-METHOD-001"].disposition == "POLICY_EXECUTABLE_DERIVED"
    assert rules["WT-METHOD-002"].disposition == "POLICY_EXECUTABLE_DERIVED"
    assert rules["WT-METHOD-003"].disposition == "BLOCKED_CONTEXT_BINDING"
    assert rules["WT-METHOD-004"].disposition == "POLICY_EXECUTABLE_DERIVED"
    assert rules["WT-METHOD-005"].disposition == "DEFER_TO_SYMBOLIC_ADAPTER"
    assert rules["WT-METHOD-006"].disposition == "DEFER_TO_SYMBOLIC_ADAPTER"


def test_execution_adapter_has_no_probability_or_learned_weight_fields():
    payload = _load(EXECUTION_RULES)
    serialized = json.dumps(payload, ensure_ascii=False).lower()

    for forbidden in (
        '"probability"',
        '"posterior"',
        '"learned_weight"',
        '"reward"',
        '"confidence_score"',
    ):
        assert forbidden not in serialized


def test_loco_retrieval_returns_only_same_domain_training_case():
    bundles = load_wang_case_bundles()
    by_id = {item.case_id: item for item in bundles}

    for case in bundles:
        fold = _fold(case.case_id)
        hits = retrieve_same_domain_cases(case, fold, bundles)

        assert len(hits) == 1
        hit = hits[0]
        assert hit.case_id in fold["retrieval_case_ids"]
        assert hit.case_id != case.case_id
        assert hit.person_group_id != case.person_group_id
        assert hit.target_domains == case.target.domains
        assert hit.match_reasons == ("EXACT_TARGET_DOMAIN",)
        assert by_id[hit.case_id].target.domains == case.target.domains


def test_cbr_payload_exposes_no_expert_answer_or_source_identity_fields():
    bundles = load_wang_case_bundles()
    case = bundles[0]
    hits = retrieve_same_domain_cases(case, _fold(case.case_id), bundles)
    payload = retrieval_payload(hits)

    validate_retrieval_payload(payload)

    serialized = json.dumps(payload, ensure_ascii=False).lower()
    for forbidden in (
        "expert_reasoning_graph",
        "expert_conclusion_refs",
        "outcome_refs",
        "source_subject_label",
        "expert_prose",
        "biography",
    ):
        assert forbidden not in serialized


def test_cbr_ranking_is_deterministic():
    bundles = load_wang_case_bundles()
    case = bundles[0]
    fold = _fold(case.case_id)

    first = retrieve_same_domain_cases(case, fold, bundles)
    second = retrieve_same_domain_cases(case, fold, tuple(reversed(bundles)))

    assert first == second


def test_cbr_rejects_person_group_leakage():
    bundles = list(load_wang_case_bundles())
    held = bundles[0]
    fold = copy.deepcopy(_fold(held.case_id))

    leaked = next(
        item for item in bundles if item.case_id == fold["retrieval_case_ids"][0]
    )
    object.__setattr__(leaked, "person_group_id", held.person_group_id)

    with pytest.raises(ValueError, match="person_group_id leaked"):
        retrieve_same_domain_cases(held, fold, tuple(bundles))


def test_real_wang_fold_fails_closed_instead_of_inventing_chart_facts():
    run = run_wang_fold("WANG-CASE-001")

    assert run.trace.policy_version == POLICY_VERSION
    assert run.trace.final_status == "ABSTAINED"
    assert [step.action for step in run.trace.steps] == ["INSPECT", "ABSTAIN"]
    assert "MATERIALIZED_BLIND_EVIDENCE_REQUIRED" in run.blockers
    assert run.selected_pattern_id is None

    # Machine trace remains Product #431 contract-valid.
    compile_inference_trace(run.trace.to_dict())


def test_all_real_wang_folds_fail_closed_until_evidence_is_materialized():
    for index in range(1, 25):
        run = run_wang_fold(f"WANG-CASE-{index:03d}")
        assert run.trace.final_status == "ABSTAINED"
        assert run.trace.steps[-1].action == "ABSTAIN"
        assert "MATERIALIZED_BLIND_EVIDENCE_REQUIRED" in run.blockers


def test_synthetic_materialized_fixture_produces_non_abstaining_path():
    fixture = _load(SYNTHETIC)
    request = fixture["request"]
    patterns = load_wang_method_patterns()
    rules = load_execution_rules()

    evidence = tuple(
        EvidenceItem(
            evidence_id=item["evidence_id"],
            kind=item["kind"],
            status=item["status"],
            refs=tuple(item["refs"]),
        )
        for item in request["evidence"]
    )

    run = run_method_policy(
        case_id=request["case_id"],
        target_domains=request["target_domains"],
        evidence=evidence,
        retrieved_cases=(),
        patterns=patterns,
        execution_rules=rules,
    )

    expected = fixture["expected"]
    assert run.selected_pattern_id == expected["selected_pattern_id"]
    assert run.trace.final_status == expected["final_status"]
    assert [step.action for step in run.trace.steps] == expected["actions"]
    assert run.blockers == ()
    compile_inference_trace(run.trace.to_dict())


def test_reference_only_required_evidence_blocks_executable_pattern():
    patterns = load_wang_method_patterns()
    rules = load_execution_rules()
    evidence = (
        EvidenceItem(
            evidence_id="E1",
            kind="PARENTS_PALACE",
            status="SOURCE_REFERENCE_ONLY",
            refs=("SOURCE_CHART:X:PARENTS",),
        ),
        EvidenceItem(
            evidence_id="E2",
            kind="PROPERTY_PALACE",
            status="SOURCE_REFERENCE_ONLY",
            refs=("SOURCE_CHART:X:PROPERTY",),
        ),
    )

    assessments = assess_patterns(
        patterns,
        rules,
        target_domains=("GLOBAL_PROFILE",),
        evidence=evidence,
    )
    by_id = {item.pattern_id: item for item in assessments}

    assert by_id["WT-METHOD-001"].readiness == "BLOCKED_REFERENCE_ONLY"
    assert by_id["WT-METHOD-001"].executable is False


def test_blocked_and_symbolic_patterns_never_execute_in_method_policy():
    patterns = load_wang_method_patterns()
    rules = load_execution_rules()

    # Even fully materialized symbolic inputs do not turn WT-METHOD-005/006
    # into π actions; they are deferred to a symbolic adapter.
    evidence = (
        EvidenceItem(
            evidence_id="B1",
            kind="BORROWED_PALACE",
            status="MATERIALIZED_FACT",
            refs=("MATERIALIZED_FACT:SYN:BORROWED",),
        ),
        EvidenceItem(
            evidence_id="B2",
            kind="OPPOSITE_PALACE",
            status="MATERIALIZED_FACT",
            refs=("MATERIALIZED_FACT:SYN:OPPOSITE",),
        ),
        EvidenceItem(
            evidence_id="B3",
            kind="STAR_SYSTEM",
            status="MATERIALIZED_FACT",
            refs=("MATERIALIZED_FACT:SYN:STAR_SYSTEM",),
        ),
        EvidenceItem(
            evidence_id="B4",
            kind="PAIRED_STAR_IDENTITY",
            status="MATERIALIZED_FACT",
            refs=("MATERIALIZED_FACT:SYN:PAIR",),
        ),
        EvidenceItem(
            evidence_id="B5",
            kind="RELATIVE_POSITION",
            status="MATERIALIZED_FACT",
            refs=("MATERIALIZED_FACT:SYN:POSITION",),
        ),
    )

    assessments = assess_patterns(
        patterns,
        rules,
        target_domains=("SYMBOLIC_INFERENCE",),
        evidence=evidence,
    )
    by_id = {item.pattern_id: item for item in assessments}

    assert by_id["WT-METHOD-005"].readiness == "BLOCKED_DISPOSITION"
    assert by_id["WT-METHOD-006"].readiness == "BLOCKED_DISPOSITION"
    assert by_id["WT-METHOD-005"].executable is False
    assert by_id["WT-METHOD-006"].executable is False


def test_wang_readiness_audit_matches_versioned_artifact():
    generated = audit_wang_method_policy_readiness()
    stored = _load(READINESS)

    assert generated["schema_version"] == stored["schema_version"]
    assert generated["artifact_id"] == stored["artifact_id"]
    assert generated["policy_version"] == stored["policy_version"]
    assert generated["corpus_id"] == stored["corpus_id"]

    summary = generated["summary"]
    stored_summary = stored["summary"]

    assert summary["retrieval_ready"] == stored_summary["retrieval_ready"] == 24
    assert (
        summary["action_selection_ready"]
        == stored_summary["action_selection_ready"]
        == 24
    )
    assert (
        summary["full_expert_replay_ready"]
        == stored_summary["full_expert_replay_ready"]
        == 0
    )
    assert summary["reference_only_fold_count"] == 24
    assert (
        summary["recommended_next_dependency"]
        == "WANG_BLIND_EVIDENCE_MATERIALIZATION_V0_1"
    )


def test_readiness_artifact_has_one_same_domain_hit_per_fold_and_zero_full_replay():
    payload = _load(READINESS)
    assert payload["summary"]["fold_count"] == 24
    assert len(payload["folds"]) == 24

    for row in payload["folds"]:
        assert len(row["retrieval_hits"]) == 1
        assert row["retrieval_ready"] is True
        assert row["action_selection_ready"] is True
        assert row["full_expert_replay_ready"] is False
        assert row["trace_expected"] == ["INSPECT", "ABSTAIN"]
        assert "MATERIALIZED_BLIND_EVIDENCE_REQUIRED" in row["blockers"]


def test_policy_outputs_contain_no_probability_or_hidden_reasoning_fields():
    generated = audit_wang_method_policy_readiness()
    serialized = json.dumps(generated, ensure_ascii=False).lower()

    for forbidden in (
        "chain_of_thought",
        "hidden_reasoning",
        "private_reasoning",
        "internal_reasoning",
        "scratchpad",
        '"probability"',
        '"posterior"',
        '"learned_weight"',
        '"reward"',
    ):
        assert forbidden not in serialized
