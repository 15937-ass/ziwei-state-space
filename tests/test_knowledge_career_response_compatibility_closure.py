import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
B1 = ROOT / "knowledge/wp07c/CAREER_RESPONSE_COMPATIBILITY_01_v0.1.json"
B2 = ROOT / "knowledge/wp07c/CAREER_RESPONSE_COMPATIBILITY_02_v0.1.json"
B3 = ROOT / "knowledge/wp07c/CAREER_RESPONSE_COMPATIBILITY_03_v0.1.json"
CLOSURE = ROOT / "knowledge/wp07c/CAREER_RESPONSE_COMPATIBILITY_CLOSURE_v0.1.json"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_response_compatibility_closure_exact_251():
    batches = [load(B1), load(B2), load(B3)]
    ids = [r["source_rule_id"] for b in batches for r in b["records"]]
    assert [len(b["records"]) for b in batches] == [100, 100, 51]
    assert len(ids) == 251
    assert len(set(ids)) == 251
    assert ids[0] == "CA01-057"
    assert ids[-1] == "CA09-887"


def test_response_compatibility_closure_never_unlocks():
    batches = [load(B1), load(B2), load(B3)]
    for row in [r for b in batches for r in b["records"]]:
        assert row["source_resolution_changed"] is False
        assert row["condition_compiled"] is False
        assert row["execution_unlocked"] is False


def test_closure_summary_and_priority_are_derived():
    closure = load(CLOSURE)
    batches = [load(B1), load(B2), load(B3)]
    rows = [r for b in batches for r in b["records"]]
    bands = {}
    blockers = {}
    for row in rows:
        bands[row["compatibility_band"]] = bands.get(row["compatibility_band"], 0) + 1
        for blocker in row["remaining_blockers"]:
            blockers[blocker] = blockers.get(blocker, 0) + 1
    assert closure["coverage"]["total"] == 251
    assert closure["coverage"]["unique_source_rule_ids"] == 251
    assert closure["summary"]["compatibility_band_counts"] == bands
    assert closure["summary"]["remaining_blocker_counts"] == blockers
    assert closure["summary"]["next_workstream_priority"][0]["workstream"] == "RELATION_SCOPE_SEMANTICS"


def test_final_batch_guardrails():
    b3 = load(B3)
    closure = load(CLOSURE)
    assert b3["summary"]["compatibility_band_counts"] == {
        "RS0_NO_DIRECT_RESPONSE_GAIN": 29,
        "RS1_RESPONSE_LAYER_COVERS_KNOWN_GROUP_SEMANTICS": 15,
        "RS2_PARTIAL_RESPONSE_GAIN": 7,
    }
    assert b3["summary"]["source_resolution_changes"] == 0
    assert b3["summary"]["conditions_compiled"] == 0
    assert b3["summary"]["execution_unlocked"] == 0
    assert closure["guardrails"]["global_any_default"] is False
    assert closure["guardrails"]["global_all_default"] is False
    assert closure["guardrails"]["automatic_execution_unlock"] is False
