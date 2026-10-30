import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "knowledge/core/lexical-semantics/FIRE_BELL_SAME_PALACE_CANONICAL_LEXICAL_CONTRACT_v0.1.json"
HANDOFF = ROOT / "knowledge/core/lexical-semantics/P02_SB11_GAP_C04_CONSUMER_HANDOFF_v0.1.json"
RELATION = ROOT / "knowledge/relation/RELATION_SEMANTICS_v0.1.json"
PAIR = ROOT / "knowledge/wp08/CAREER_PAIR_CLOSED_GROUP_CONTEXTUAL_63_v0.1.json"
KMM1 = ROOT / "knowledge/core/wp06c/canonical_mappings/KMM-000001.json"
P02 = ROOT / "knowledge/palaces/P02_siblings/wp05/SIBLINGS_SB11_QISHA_POJUN_SOURCE_AUDIT_v0.1.json"

def load(path):
    return json.loads(path.read_text(encoding="utf-8"))

def test_exact_surface_contract_is_narrow_and_human_gate_approved():
    d = load(CONTRACT)
    assert d["status"] == "CANONICAL_SHARED_LEXICAL_SEMANTIC_NO_RUNTIME_UNLOCK"
    assert d["human_gate"]["decision"] == "APPROVED"
    assert d["source_scope"]["school"] == "中州派"
    assert d["source_scope"]["exact_surface"] == "火铃同度"
    assert d["source_scope"]["surface_match_mode"] == "EXACT_CONTIGUOUS_LEXEME_PINNED_BY_CONSUMER"
    assert d["source_scope"]["automatic_text_discovery"] is False

def test_pair_membership_reused_without_changing_generic_activation_default():
    d = load(CONTRACT)
    assert d["pair_identity"]["members"] == ["火星", "铃星"]
    assert d["pair_identity"]["generic_activation_default_required"] == "CONTEXTUAL_UNRESOLVED"
    assert d["pair_identity"]["generic_activation_default_modified"] is False
    pair = load(PAIR)
    fam = {x["family_id"]: x for x in pair["family_contracts"]}
    assert fam["PAIR_HUO_LING"]["members"] == ["火星", "铃星"]
    assert fam["PAIR_HUO_LING"]["activation_default"] == "CONTEXTUAL_UNRESOLVED"
    assert fam["PAIR_HUO_LING"]["universal_any_supported"] is False
    assert fam["PAIR_HUO_LING"]["universal_all_supported"] is False

def test_same_palace_relation_is_reused_not_redefined():
    d = load(CONTRACT)
    r = d["relation_identity"]
    assert r["source_surface"] == "同度"
    assert r["operator"] == "EXACT_GEOMETRY"
    assert r["canonical_geometry"] == "SAME_PALACE"
    assert r["relation_redefined"] is False
    rel = load(RELATION)
    lex = {x["surface"]: x for x in rel["lexicon"]}
    assert lex["同度"]["operator"] == "EXACT_GEOMETRY"
    assert lex["同度"]["canonical_geometry"] == "SAME_PALACE"
    assert lex["同度"]["palace_offset_constraint"] == [0]

def test_member_realization_is_inclusive_either_not_xor_or_both_requirement():
    q = load(CONTRACT)["member_realization"]
    assert q["quantifier"] == "ANY_MEMBER_AT_LEAST_ONE"
    assert q["minimum_satisfied_members"] == 1
    assert q["member_count"] == 2
    assert q["both_required"] is False
    assert q["both_forbidden"] is False
    assert q["exclusive_or"] is False
    assert q["inclusive_either"] is True

def test_contextual_anchor_must_be_preserved_not_invented():
    a = load(CONTRACT)["contextual_anchor"]
    assert a["required"] is True
    assert a["inferred_by_contract"] is False
    assert load(CONTRACT)["relation_identity"]["relation_role"] == "PAIR_MEMBER_TO_CONTEXTUAL_SOURCE_ANCHOR"

def test_bare_fire_bell_and_other_relation_families_remain_outside_contract():
    d = load(CONTRACT)
    nd = {x.get("surface", x.get("mapping_id")): x["status"] for x in d["explicit_non_dispositions"]}
    assert nd["火铃"] == "CONTEXTUAL_UNRESOLVED"
    assert nd["火铃夹"] == "OUT_OF_SCOPE_SEPARATE_GEOMETRY_FAMILY"
    assert nd["火铃同会"] == "OUT_OF_SCOPE_SEPARATE_RELATION_FAMILY"
    assert nd["火铃会照"] == "OUT_OF_SCOPE_SEPARATE_RELATION_FAMILY"
    assert nd["各安一火、一铃"] == "OUT_OF_SCOPE_SPLIT_PLACEMENT_WORDING"

def test_kmm000001_remains_hold_and_is_not_rewritten_by_exact_surface_decision():
    d = load(CONTRACT)
    nd = {x.get("surface", x.get("mapping_id")): x for x in d["explicit_non_dispositions"]}
    assert nd["KMM-000001"]["status"] == "REMAINS_HOLD"
    k = load(KMM1)
    assert k["conditions"]["source_condition_text"] == "事业宫见火铃"
    assert "UNRESOLVED_FIRE_BELL_TRIGGER_QUANTIFIER" in k["execution_blockers"]
    assert k["execution_readiness"] == "BLOCKED_SEMANTIC"
    assert k["executable"] is False

def test_p02_handoff_resolves_only_core_quantifier_dimension():
    h = load(HANDOFF)
    g = h["gap"]
    assert g["gap_id"] == "P02-SB11-GAP-C04"
    assert g["core_disposition"] == "CORE_SEMANTIC_RESOLVED_PENDING_PALACE_OWNED_MIGRATION"
    assert g["resolved_value"] == "INCLUSIVE_EITHER__ANY_MEMBER_AT_LEAST_ONE"
    assert g["affected_record_ids"] == ["P02S-414", "P02S-416", "P02S-417"]
    assert h["consumer_requirements"]["must_preserve_case_support_only"] is True
    assert h["consumer_requirements"]["may_auto_unlock_execution"] is False
    assert h["consumer_requirements"]["may_auto_promote_event_claims"] is False

def test_historical_p02_records_are_not_mutated_or_unlocked_by_core():
    p = load(P02)
    rows = {x["projection_rule_id"]: x for x in p["records"]}
    for rid in ("P02S-414", "P02S-416", "P02S-417"):
        r = rows[rid]
        assert r["gap_id"] == "P02-SB11-GAP-C04"
        assert r["case_support_only"] is True
        assert r["disposition"] == "HELD_FAIL_CLOSED"
        assert r["canonical_condition"] is None
        assert r["executable"] is False

def test_no_runtime_product_probability_or_generic_or_authority():
    d = load(CONTRACT)
    c = d["canonical_semantics"]
    assert c["source_condition_compilation_authorized_for_exact_surface"] is False
    assert c["executable_predicate_authorized"] is False
    assert c["product_consumable"] is False
    assert c["runtime_authorized"] is False
    g = d["guardrails"]
    assert g["generic_pair_default_changed"] is False
    assert g["generic_or_operator_created"] is False
    assert g["p02_historical_ledger_modified"] is False
    assert g["canonical_kmm_modified"] is False
    assert g["product_modified"] is False
    assert g["runtime_modified"] is False
    assert g["kib_modified"] is False
    assert g["probability_added"] is False
    assert g["numeric_score_added"] is False
    assert g["event_certainty_added"] is False
