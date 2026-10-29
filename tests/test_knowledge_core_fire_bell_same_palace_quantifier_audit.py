import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "knowledge/core/lexical-semantics/FIRE_BELL_SAME_PALACE_QUANTIFIER_SOURCE_AUDIT_v0.1.json"

def load():
    return json.loads(AUDIT.read_text(encoding="utf-8"))

def test_exact_phrase_source_verdict_is_either_but_non_executable():
    d = load()
    assert d["source_verdict"] == "EXACT_PHRASE_SUPPORTS_EITHER_MEMBER_READING"
    assert d["migration_verdict"] == "SHARED_EITHER_QUANTIFIER_CANDIDATE_REQUIRES_HUMAN_GATE"
    c = d["exact_phrase_contract"]
    assert c["phrase"] == "火铃同度"
    assert c["descriptive_minimum"] == "EITHER_MEMBER_SAME_PALACE"
    assert c["members"] == ["火星同度", "铃星同度"]
    assert c["both_required"] is False
    assert c["executable"] is False
    assert c["canonical_migration_authorized"] is False

def test_independent_evidence_contains_equivalence_decomposition_and_negative_control():
    d = load()
    types = {row["evidence_type"] for row in d["evidence"]}
    assert "DIRECT_SAME_CONTEXT_EQUIVALENCE" in types
    assert "UMBRELLA_DECOMPOSITION" in types
    assert "NAMED_MEMBER_BRANCHES" in types
    assert "NEGATIVE_CONTROL_EXPLICIT_TWO_OBJECT_WORDING" in types
    assert all(row["source_id"].startswith("SRC-ZZ-") for row in d["evidence"])

def test_p02_gap_is_source_clarified_but_migration_stays_gated():
    d = load()
    gaps = {row["gap_id"]: row for row in d["gap_dispositions"]}
    p02 = gaps["P02-SB11-GAP-C04"]
    assert p02["source_level_disposition"] == "SOURCE_QUANTIFIER_CLARIFIED_EITHER_MEMBER"
    assert p02["canonical_migration_status"] == "PENDING_HUMAN_GATE"
    assert p02["executable"] is False

def test_bare_fire_bell_kmm_hold_is_not_silently_resolved():
    d = load()
    gaps = {row["gap_id"]: row for row in d["gap_dispositions"]}
    kmm = gaps["KMM-000001"]
    assert kmm["source_level_disposition"] == "NO_DISPOSITION"
    assert kmm["canonical_migration_status"] == "REMAINS_HOLD"
    assert kmm["executable"] is False
    assert "bare 火铃" in d["out_of_scope_families"]
    assert "bare 火铃 == EITHER(火星,铃星)" in d["forbidden_inferences"]

def test_relation_families_do_not_inherit_same_palace_quantifier():
    d = load()
    out = set(d["out_of_scope_families"])
    assert {"火铃夹","火铃同会","火铃会照","各安一火、一铃 split placement"} <= out
    forbidden = set(d["forbidden_inferences"])
    assert "火铃夹 inherits 火铃同度 quantifier" in forbidden
    assert "火铃同会/会照 inherits 火铃同度 geometry" in forbidden

def test_human_gate_is_only_for_migration_not_source_audit():
    d = load()
    hg = d["human_gate"]
    assert hg["gate_candidate_id"] == "HG-CORE-FIRE-BELL-SAME-PALACE-EITHER-01"
    assert hg["required_now_for_audit"] is False
    assert hg["required_before_migration"] is True

def test_no_runtime_palace_or_canonical_mutation_in_audit():
    g = load()["guardrails"]
    assert g["product_modified"] is False
    assert g["runtime_modified"] is False
    assert g["palace_ledger_modified"] is False
    assert g["canonical_kmn_kmm_modified"] is False
    assert g["probability_added"] is False
    assert g["cross_school_sources_added"] is False
