import copy
import json
from pathlib import Path

from src.product.acquired_state import compile_acquired_state
from src.product.state_quality import (
    audit_acquired_state_quality,
    compile_state_requirements,
)

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "product/PL3S_ACQUIRED_STATE_FIXTURE_v0.1.json"
REQ = ROOT / "product/PL3S_STATE_QUALITY_REQUIREMENTS_FIXTURE_v0.1.json"


def _state():
    return compile_acquired_state(
        json.loads(STATE.read_text(encoding="utf-8"))
    )


def _requirements():
    return compile_state_requirements(
        json.loads(REQ.read_text(encoding="utf-8"))
    )


def test_quality_audit_marks_available_and_explicit_missing():
    report = audit_acquired_state_quality(_state(), _requirements())
    by_id = {item.requirement_id: item for item in report.requirements}
    assert by_id["REQ-CAREER-STATUS"].status == "AVAILABLE"
    assert by_id["REQ-RESOURCE-LIQUIDITY"].status == "MISSING"
    assert (
        by_id["REQ-RESOURCE-LIQUIDITY"].missingness_reason
        == "NOT_ASKED"
    )
    assert report.readiness == "PARTIAL_MISSING"


def test_withheld_is_flagged_as_mnar_risk_not_declared_mnar_truth():
    payload = json.loads(STATE.read_text(encoding="utf-8"))
    payload["missingness"][0]["reason"] = "WITHHELD"
    state = compile_acquired_state(payload)
    report = audit_acquired_state_quality(state, _requirements())
    assert report.mnar_risk_keys == ("RESOURCE:liquid_asset_level",)
    audit = report.missingness_audit[0]
    assert audit.audit_class == "WITHHELD_MNAR_RISK"


def test_conflict_blocks_requirement_without_auto_resolution():
    payload = json.loads(STATE.read_text(encoding="utf-8"))
    base = copy.deepcopy(payload["assertions"][0])
    base["fact_id"] = "SF-CAREER-ALT"
    base["value"] = "UNEMPLOYED"
    payload["assertions"].append(base)
    payload["conflicts"] = [
        {
            "conflict_id": "CF-CAREER-001",
            "domain": "CAREER",
            "key": "employment_status",
            "fact_ids": ["SF-CAREER-001", "SF-CAREER-ALT"],
            "status": "UNRESOLVED",
        }
    ]
    state = compile_acquired_state(payload)
    report = audit_acquired_state_quality(state, _requirements())
    by_id = {item.requirement_id: item for item in report.requirements}
    assert by_id["REQ-CAREER-STATUS"].status == "CONFLICTED"
    assert report.readiness == "CONFLICTED"


def test_requirement_controls_accepted_confidence_without_numeric_weight():
    payload = json.loads(STATE.read_text(encoding="utf-8"))
    payload["assertions"][0]["confidence"] = "LOW"
    state = compile_acquired_state(payload)
    report = audit_acquired_state_quality(state, _requirements())
    by_id = {item.requirement_id: item for item in report.requirements}
    assert by_id["REQ-CAREER-STATUS"].status == "INSUFFICIENT_CONFIDENCE"
    assert "SF-CAREER-001" in report.low_confidence_fact_ids


def test_no_requirements_is_ready_for_empty_declared_contract():
    report = audit_acquired_state_quality(_state(), ())
    assert report.readiness == "READY"
