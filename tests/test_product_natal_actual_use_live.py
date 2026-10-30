"""Live, bounded actual-use validation for one source-exact NATAL case.

This test is intentionally opt-in. The normal repository suite remains offline and
deterministic; the dedicated workflow runs this test against accepted GitHub main.
"""
from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path

import pytest

from src.product.detailed_read import DetailedReadSession, build_detailed_read_plan

FIXTURE_ID = "WANG-CASE-012"


def _load_json(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def test_live_natal_actual_use_wang_case_012() -> None:
    if os.getenv("ZIWEI_RUN_LIVE_NATAL_ACTUAL_USE") != "1":
        pytest.skip("live accepted-main validation is run by its dedicated GitHub workflow")

    accepted_main = Path(os.environ["ZIWEI_ACCEPTED_MAIN_CHECKOUT"]).resolve()
    main_sha = subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=accepted_main, text=True
    ).strip()
    clean_status = subprocess.check_output(
        ["git", "status", "--porcelain", "--untracked-files=all"],
        cwd=accepted_main,
        text=True,
    ).strip()
    assert not clean_status, "accepted-main checkout must be clean"

    case = _load_json(
        accepted_main / "product/expert_cases/wang_tingzhi/cases/wang_case_012.json"
    )
    materialization = _load_json(
        accepted_main / "product/expert_cases/wang_tingzhi/FULL_CHART_MATERIALIZATION_V0_1B.json"
    )
    materialized_case = next(
        item for item in materialization["cases"] if item["case_id"] == FIXTURE_ID
    )
    source_chart_ref = materialized_case["source_provenance"]["source_chart_span_ref"]
    anchor = materialized_case["target_anchor_verification"]
    candidate_set = materialized_case["source_candidate_set"]

    # The fixture is source-exact and has one target anchor, but remains
    # CASE_SUPPORT_ONLY; only the verified target anchor enters chart context.
    assert case["allowed_use"] == "CASE_SUPPORT_ONLY"
    assert case["source"]["review_status"] == "SOURCE_SPAN_VERIFIED"
    assert case["target"]["domains"] == ["WEALTH"]
    assert materialized_case["source_status"] == "SOURCE_EXACT"
    assert candidate_set["source_candidate_count"] == 1
    assert candidate_set["anchor_match_count"] == 1
    assert anchor["status"] == "UNIQUE_ANCHOR_MATCH_RECONFIRMED"
    assert anchor["target_palace_identity_match"] is True
    assert anchor["observed_target_palace"] == "财帛"
    assert anchor["observed_target_branch"] == "巳"
    assert anchor["observed_target_main_stars"] == ["天梁"]
    assert materialized_case["full_source_chart_equivalence_verified"] is False

    chart_context = {
        "fixture_id": FIXTURE_ID,
        "source_chart_span_ref": source_chart_ref,
        "target_domain": "WEALTH",
        "target_palace": anchor["observed_target_palace"],
        "target_branch": anchor["observed_target_branch"],
        "target_main_stars": anchor["observed_target_main_stars"],
        "target_anchor_status": anchor["status"],
        "case_allowed_use": case["allowed_use"],
        "full_source_chart_equivalence_verified": False,
    }

    plan = build_detailed_read_plan(
        "WANG-CASE-012 actual source-case use: inspect NATAL evidence retrieval and gaps",
        FIXTURE_ID,
        mode="SOURCE_FIRST",
    )
    session = DetailedReadSession(plan)
    result = session.run_all_stages(
        source_items_per_slot=20,
        timeout_seconds=20.0,
        repository_root=accepted_main,
    )

    assert session.main_sha == main_sha
    assert result["main_sha"] == main_sha
    assert result["session_status"] == "NATAL_INSPECTION_COMPLETE"
    assert result["natal_domain_count_required"] == 12
    assert result["natal_domain_count_inspected"] == 12
    assert len(result["coverage"]) == 12
    assert all(item["inspection_status"] == "INSPECTED" for item in result["coverage"])

    wealth_bundle = session.slot_batches["wealth_natal"][0]
    wealth_record = wealth_bundle.manifest.records[0]
    assert wealth_record.runtime_status == "AVAILABLE"
    assert wealth_record.runtime_rule_ids
    assert wealth_record.runtime_source_refs
    # Bind only the verified wealth target anchor; no raw birth data or identity.
    wealth_payload = wealth_bundle.build_payload(chart_context=chart_context)
    assert isinstance(wealth_payload, dict)

    relationship_bundle = session.slot_batches["relationship_natal"][0]
    relationship_record = relationship_bundle.manifest.records[0]
    assert relationship_record.source_status == "AVAILABLE"
    assert relationship_bundle.evidence_items

    source_items = result["evidence"]["source"]
    assert source_items, "at least one accepted SOURCE lane item must be retrieved"
    assert all(
        ref["allowed_use"] != "CASE_SUPPORT_ONLY"
        for item in source_items
        for ref in item["source_refs"]
    ), "case-support-only material must not be returned as canonical SOURCE evidence"
    assert result["evidence"]["runtime"] == [], "capability discovery is not runtime execution"
    assert result["evidence"]["model_supplement"] == []

    checks = result["cross_domain_checks"]
    assert checks, "cross-domain check instructions must be emitted"
    guardrails = result["guardrails"]
    assert guardrails["one_main_snapshot_for_all_slots"] is True
    assert guardrails["case_support_only_and_unpromoted_records_excluded"] is True
    assert guardrails["runtime_execution_performed"] is False
    assert guardrails["unsupported_domains_filled_from_model_memory"] is False

    report = {
        "schema_version": "0.1",
        "validation_id": "PRODUCT_NATAL_ACTUAL_USE_WANG_CASE_012_V0_1",
        "status": "PASS_WITH_LIMITATIONS",
        "main_sha": main_sha,
        "fixture": {
            "case_id": FIXTURE_ID,
            "source_chart_span_ref": source_chart_ref,
            "source_status": materialized_case["source_status"],
            "allowed_use": case["allowed_use"],
            "target_domain": "WEALTH",
            "target_anchor": chart_context,
            "full_source_chart_equivalence_verified": False,
        },
        "natal_domain_count_required": result["natal_domain_count_required"],
        "natal_domain_count_inspected": result["natal_domain_count_inspected"],
        "domain_coverage": result["coverage"],
        "wealth_runtime_capability": {
            "status": wealth_record.runtime_status,
            "rule_count": len(wealth_record.runtime_rule_ids),
            "source_ref_count": len(wealth_record.runtime_source_refs),
            "runtime_execution_performed": False,
        },
        "relationship_source_retrieval": {
            "status": relationship_record.source_status,
            "evidence_count": len(relationship_bundle.evidence_items),
        },
        "total_source_evidence_count": len(source_items),
        "cross_domain_checks": checks,
        "cross_domain_adjudication_performed": False,
        "guardrails": guardrails,
        "limitations": [
            "The historical case remains CASE_SUPPORT_ONLY and is not promoted into canonical knowledge.",
            "The pinned-engine chart reconstruction has target-anchor verification only; full-source-chart equivalence is not established.",
            "The reader retrieves accepted evidence and capability manifests; it does not execute chart-specific runtime rules.",
            "Cross-domain checks are emitted as structured instructions; this validation does not claim automatic cross-domain adjudication.",
            "No expert replay completeness, probability, causal inference, or prospective predictive validity is evaluated.",
        ],
    }

    report_path = (
        Path(__file__).resolve().parents[1]
        / "validation/product/issue_966/ACTUAL_USE_VALIDATION_V0_1.json"
    )
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print("ACTUAL_USE_VALIDATION_REPORT=" + json.dumps(report, ensure_ascii=False, sort_keys=True))
