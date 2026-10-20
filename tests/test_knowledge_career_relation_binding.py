import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "knowledge/relation/RELATION_BINDING_SEMANTICS_v0.1.json"
REL_V02 = ROOT / "knowledge/wp07c/CAREER_RELATION_COMPATIBILITY_132_v0.2.json"
BIND = ROOT / "knowledge/wp07c/CAREER_RELATION_BINDING_132_v0.1.json"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def by_id(data, rule_id):
    return next(row for row in data["records"] if row["source_rule_id"] == rule_id)


def test_relation_surface_v02_exact_132_and_complete_occurrences():
    data = load(REL_V02)
    assert len(data["records"]) == 132
    assert len({r["source_rule_id"] for r in data["records"]}) == 132
    assert data["summary"]["complete_surface_relation_occurrences"] == 150
    assert data["summary"]["excluded_named_pattern_internal_occurrences"] == 1
    assert data["summary"]["classification_counts"] == {
        "R1_CANONICAL_RELATION_OR_SCOPE_DEFINED": 104,
        "R2_COMPRESSED_GENERIC_MEETING_GEOMETRY_UNSPECIFIED": 27,
        "R3_SOURCE_RECHECK_REQUIRED": 1,
    }


def test_relation_surface_v02_repairs_compound_secondary_relations():
    data = load(REL_V02)
    expected = {
        "CA02-141": ["同度", "见"],
        "CA03-290": ["同度", "会"],
        "CA04-345": ["同度", "见"],
        "CA04-358": ["三方", "见"],
        "CA09-871": ["见", "见"],
    }
    for rule_id, surfaces in expected.items():
        assert [a["surface_relation"] for a in by_id(data, rule_id)["relation_atoms"]] == surfaces


def test_named_pattern_internal_chaogong_is_not_promoted():
    data = load(REL_V02)
    row = by_id(data, "CA05-471")
    assert [a["surface_relation"] for a in row["relation_atoms"]] == ["会"]
    excluded = row["excluded_internal_relation_surfaces"]
    assert len(excluded) == 1
    assert excluded[0]["surface_relation"] == "朝拱"
    assert excluded[0]["containing_structured_pattern"] == "百官朝拱"


def test_binding_exact_132_rules_and_142_claims():
    data = load(BIND)
    assert len(data["records"]) == 132
    assert len({r["source_rule_id"] for r in data["records"]}) == 132
    claims = [c for r in data["records"] for c in r["relation_claims"]]
    assert len(claims) == 142
    assert data["coverage"]["relation_claims"] == 142
    assert data["summary"]["polarity_counts"] == {"AFFIRMATIVE": 139, "NEGATED": 3}


def test_group_symbol_binding_never_default_expands_members():
    data = load(BIND)
    row = by_id(data, "CA02-116")
    claim = row["relation_claims"][0]
    node = claim["target_nodes"][0]
    assert claim["source_relation_surfaces"] == ["同度"]
    assert claim["relation_semantics"][0]["palace_offset_constraint"] == [0]
    assert node["target_surface"] == "火铃"
    assert node["node_type"] == "GROUP_SYMBOL_NODE"
    assert node["members"] == ["火星", "铃星"]
    assert node["expansion_policy"] == "NO_MEMBER_EXPANSION"
    assert claim["member_realization"] == "DEFERRED_UNLESS_SOURCE_EXPLICIT"


def test_relation_local_binding_excludes_unrelated_additive_or_emphasis_conditions():
    data = load(BIND)
    cases = {
        "CA01-081": "桃花",
        "CA07-628": "空劫",
        "CA09-840": "辅佐吉曜",
        "CA08-800": "煞曜",
    }
    for rule_id, target in cases.items():
        claim = by_id(data, rule_id)["relation_claims"][0]
        assert claim["target_source_expression"] == target
    assert "昌曲" not in by_id(data, "CA01-081")["relation_claims"][0]["target_source_expression"]
    assert "昌曲" not in by_id(data, "CA07-628")["relation_claims"][0]["target_source_expression"]
    assert "火铃" not in by_id(data, "CA08-800")["relation_claims"][0]["target_source_expression"]


def test_explicit_member_sets_are_local_only():
    data = load(BIND)
    for rule_id in ("CA05-419", "CA06-582", "CA07-638", "CA07-699"):
        claim = by_id(data, rule_id)["relation_claims"][0]
        node = next(n for n in claim["target_nodes"] if n["node_type"] == "EXPLICIT_MEMBER_SET")
        assert node["expansion_policy"] == "EXPLICIT_MEMBERS_LOCAL_ONLY"
        assert claim["member_realization"] == "EXPLICIT_MEMBERS_LOCAL_ONLY"


def test_named_composites_and_generic_shorthand_keep_integrity():
    data = load(BIND)
    composite = by_id(data, "CA02-181")["relation_claims"][0]["target_nodes"][0]
    assert composite["node_type"] == "NAMED_COMPOSITE_NODE"
    assert composite["target_surface"] == "龙池凤阁"
    assert composite["expansion_policy"] == "PRESERVE_COMPOSITE_INTEGRITY"

    generic = by_id(data, "CA07-697")["relation_claims"][0]["target_nodes"][0]
    assert generic["node_type"] == "GENERIC_SHORTHAND_NODE"
    assert generic["target_surface"] == "禄马"
    assert generic["expansion_policy"] == "NO_NAMED_COMPOSITE_INHERITANCE"


def test_structured_pattern_stays_a_node_not_flat_members():
    data = load(BIND)
    claim = by_id(data, "CA05-471")["relation_claims"][0]
    pattern = next(n for n in claim["target_nodes"] if n["node_type"] == "STRUCTURED_PATTERN_NODE")
    assert pattern["target_surface"] == "百官朝拱"
    assert pattern["expansion_policy"] == "NEVER_FLATTEN_TO_RELATION_MEMBERS"
    assert "紫微" in claim["target_source_expression"]


def test_compound_clause_graph_constraints():
    data = load(BIND)
    c1 = by_id(data, "CA04-358")["relation_claims"][0]
    assert c1["source_relation_surfaces"] == ["三方", "见"]
    assert c1["relation_composition"] == "THREE_DIRECTIONS_SCOPE_RESTRICTS_VISIBILITY"
    assert c1["effective_constraint"]["palace_offset_constraint"] == [0, 4, 8]

    c2 = by_id(data, "CA07-602")["relation_claims"][0]
    assert c2["source_relation_surfaces"] == ["同度", "相对"]
    assert c2["effective_constraint"]["palace_offset_constraint"] == [0, 6]

    row = by_id(data, "CA09-871")
    assert len(row["relation_claims"]) == 2
    assert [c["polarity"] for c in row["relation_claims"]] == ["AFFIRMATIVE", "NEGATED"]
    assert [c["relation_semantics"][0]["source_start"] for c in row["relation_claims"]] == [2, 7]


def test_relation_surface_bundle_does_not_distribute_geometry_per_target():
    data = load(BIND)
    for rule_id in ("CA08-799", "CA09-804"):
        claim = by_id(data, rule_id)["relation_claims"][0]
        assert claim["binding_resolution"] == "BOUND_RELATION_SURFACE_BUNDLE"
        assert claim["source_relation_surfaces"] == ["朝拱", "同会"]
        assert [n["target_surface"] for n in claim["target_nodes"]] == ["辅弼", "魁钺", "三台八座"]
        assert claim["effective_constraint"]["operator"] == "RELATION_SURFACE_BUNDLE"
        assert claim["effective_constraint"]["palace_offset_constraint"] is None


def test_relation_target_can_be_bound_while_geometry_remains_source_recheck():
    data = load(BIND)
    claim = by_id(data, "CA06-549")["relation_claims"][0]
    assert claim["target_nodes"][0]["target_surface"] == "火铃"
    assert claim["binding_resolution"] == "TARGET_BOUND_SOURCE_RELATION_RECHECK"
    assert claim["effective_constraint"]["operator"] == "SOURCE_RECHECK_REQUIRED"


def test_relation_polarity_is_clause_local_not_left_context_wide():
    data = load(BIND)
    assert by_id(data, "CA05-459")["relation_claims"][0]["polarity"] == "NEGATED"
    assert by_id(data, "CA09-816")["relation_claims"][0]["polarity"] == "NEGATED"
    assert by_id(data, "CA06-533")["relation_claims"][0]["polarity"] == "AFFIRMATIVE"
    assert by_id(data, "CA09-840")["relation_claims"][0]["polarity"] == "AFFIRMATIVE"


def test_source_literal_nodes_preserve_binding_without_inventing_semantics():
    data = load(BIND)
    literal_claims = [
        c for r in data["records"] for c in r["relation_claims"]
        if any(n["node_type"] == "SOURCE_LITERAL_EXPRESSION_NODE" for n in c["target_nodes"])
    ]
    assert len(literal_claims) == 25
    for claim in literal_claims:
        for node in claim["target_nodes"]:
            if node["node_type"] == "SOURCE_LITERAL_EXPRESSION_NODE":
                assert node["expansion_policy"] == "SEMANTIC_NORMALIZATION_DEFERRED"


def test_schema_invariant_separates_binding_from_member_realization():
    schema = load(SCHEMA)
    assert schema["clause_model"]["invariant"] == "RELATION_CLAIM_NEVER_IMPLIES_MEMBER_REALIZATION_UNLESS_SOURCE_EXPLICIT_SET"
    assert schema["guardrails"]["global_any_or_all_inferred"] is False
    assert schema["guardrails"]["group_member_geometry_distributed_by_default"] is False
    assert schema["guardrails"]["category_closed_by_default"] is False


def test_no_execution_unlock_or_hidden_runtime_change():
    data = load(BIND)
    assert data["summary"]["source_resolution_changes"] == 0
    assert data["summary"]["conditions_compiled"] == 0
    assert data["summary"]["execution_unlocked"] == 0
    for row in data["records"]:
        assert row["source_resolution_changed"] is False
        assert row["condition_compiled"] is False
        assert row["execution_unlocked"] is False
        for claim in row["relation_claims"]:
            for node in claim["target_nodes"]:
                assert "distance" not in node
    guard = data["guardrails"]
    assert guard["product_runtime_modified"] is False
    assert guard["numeric_weights_added"] is False
    assert guard["probabilities_added"] is False
