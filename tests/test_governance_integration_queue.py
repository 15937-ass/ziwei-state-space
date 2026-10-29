from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]


def test_parallel_build_serial_integration_protocol_is_recoverable():
    protocol = (ROOT / "governance/INTEGRATION_QUEUE_PROTOCOL_v1.md").read_text(encoding="utf-8")
    for marker in [
        "ACTIVE_BUILD",
        "READY_TO_INTEGRATE",
        "INTEGRATING",
        "Integration Lease",
        "Issue #888",
        "exact-head",
        "D0",
        "D1",
        "D2",
        "D3",
    ]:
        assert marker in protocol

    project = (ROOT / "PROJECT_STATE.yaml").read_text(encoding="utf-8")
    assert 'integration_protocol: "governance/INTEGRATION_QUEUE_PROTOCOL_v1.md"' in project
    assert "integration_ledger_issue: 888" in project


def test_integration_protocol_does_not_expand_knowledge_hard_wip():
    shards = json.loads((ROOT / "governance/KNOWLEDGE_SHARDS.json").read_text(encoding="utf-8"))
    assert shards["limits"]["core_wip"] == 1
    assert shards["limits"]["per_palace_wip"] == 1
    assert shards["limits"]["total_palace_wip"] == 4
    assert shards["limits"]["canonical_merge"] == "SERIAL_EXACT_HEAD"


def test_coordination_lease_is_not_a_lane_wip_replacement():
    governance = (ROOT / "GOVERNANCE.md").read_text(encoding="utf-8")
    assert "Integration Lease" in governance
    assert "does not consume a lane WIP slot" in governance
    assert "one active palace audit + one Knowledge Core unit + one Product unit" in governance
