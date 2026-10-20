import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ONTOLOGY = ROOT / "knowledge/relation/RELATION_SEMANTICS_v0.1.json"
MAP = ROOT / "knowledge/wp07c/CAREER_RELATION_COMPATIBILITY_132_v0.1.json"
B1 = ROOT / "knowledge/wp07c/CAREER_RESPONSE_COMPATIBILITY_01_v0.1.json"
B2 = ROOT / "knowledge/wp07c/CAREER_RESPONSE_COMPATIBILITY_02_v0.1.json"
B3 = ROOT / "knowledge/wp07c/CAREER_RESPONSE_COMPATIBILITY_03_v0.1.json"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_relation_ontology_core_source_mappings():
    data = load(ONTOLOGY)
    lex = {row["surface"]: row for row in data["lexicon"]}
    assert lex["同度"]["canonical_geometry"] == "SAME_PALACE"
    assert lex["拱照"]["canonical_geometry"] == "OPPOSITION"
    assert lex["朝拱"]["canonical_geometry"] == "OPPOSITION"
    assert lex["会照"]["canonical_geometry"] == "TRINE_ASPECT"
    assert lex["相夹"]["canonical_geometry"] == "FLANKING"
    assert lex["见"]["relation_operator" if "relation_operator" in lex["见"] else "operator"] == "FOUR_DIRECTIONS_VISIBILITY"


def test_relation_ontology_compresses_meeting_family():
    data = load(ONTOLOGY)
    lex = {row["surface"]: row for row in data["lexicon"]}
    for surface in ("会", "同会", "会合"):
        assert lex[surface]["operator"] == "MEETING_GENERIC"
        assert lex[surface]["canonical_geometry"] == "UNSPECIFIED"


def test_career_relation_map_exact_132_unique():
    data = load(MAP)
    records = data["records"]
    assert len(records) == 132
    assert len({row["source_rule_id"] for row in records}) == 132
    assert data["coverage"]["relation_residual_total"] == 132
    assert data["coverage"]["unique_source_rule_ids"] == 132


def test_career_relation_map_matches_response_residual_set():
    mapped = load(MAP)
    batches = [load(B1), load(B2), load(B3)]
    expected = {
        row["source_rule_id"]
        for batch in batches
        for row in batch["records"]
        if "RELATION_SCOPE_SEMANTICS" in row["remaining_blockers"]
    }
    actual = {row["source_rule_id"] for row in mapped["records"]}
    assert actual == expected


def test_relation_compression_counts_are_locked():
    data = load(MAP)
    assert data["summary"]["classification_counts"] == {
        "R1_CANONICAL_RELATION_OR_SCOPE_DEFINED": 105,
        "R2_COMPRESSED_GENERIC_MEETING_GEOMETRY_UNSPECIFIED": 26,
        "R3_SOURCE_RECHECK_REQUIRED": 1,
    }
    assert data["summary"]["raw_relation_marker_count"] == 157
    assert data["summary"]["deduped_relation_atom_count"] == 145
    assert data["summary"]["observed_surface_vocabulary_count"] == 9


def test_jian_is_scope_not_exact_geometry():
    data = load(MAP)
    atoms = [
        atom
        for row in data["records"]
        for atom in row["relation_atoms"]
        if atom["surface_relation"] == "见"
    ]
    assert len(atoms) == 54
    for atom in atoms:
        assert atom["relation_operator"] == "FOUR_DIRECTIONS_VISIBILITY"
        assert atom["canonical_geometry"] == "UNSPECIFIED_WITHIN_SCOPE"
        assert set(atom["allowed_geometry"]) == {"SAME_PALACE", "TRINE_ASPECT", "OPPOSITION"}


def test_chaogong_is_opposition_but_named_patterns_are_guarded():
    ontology = load(ONTOLOGY)
    lex = {row["surface"]: row for row in ontology["lexicon"]}
    assert lex["朝拱"]["canonical_geometry"] == "OPPOSITION"
    assert lex["朝拱"]["guard"] == "NAMED_PATTERN_PHRASES_REMAIN_STRUCTURED"
    assert ontology["normalization_rules"]["named_pattern_guard"] is True


def test_meeting_family_does_not_invent_geometry():
    data = load(MAP)
    atoms = [
        atom
        for row in data["records"]
        for atom in row["relation_atoms"]
        if atom["surface_relation"] in {"会", "同会", "会合"}
    ]
    assert atoms
    for atom in atoms:
        assert atom["relation_operator"] == "MEETING_GENERIC"
        assert atom["canonical_geometry"] == "UNSPECIFIED"


def test_only_zhaoshe_routes_source_recheck():
    data = load(MAP)
    rows = [r for r in data['records'] if r['relation_classification'] == 'R3_SOURCE_RECHECK_REQUIRED']
    assert [r['source_rule_id'] for r in rows] == ['CA06-549']
    assert any(a['surface_relation'] == '照射' for a in rows[0]['relation_atoms'])


def test_relation_map_preserves_provenance_and_never_unlocks():
    data = load(MAP)
    batches = [load(B1), load(B2), load(B3)]
    original = {r['source_rule_id']: r for b in batches for r in b['records']}
    for row in data['records']:
        src = original[row['source_rule_id']]
        assert row['source_condition_text'] == src['source_condition_text']
        assert row['source_location'] == src['source_location']
        assert row['source_span_ids'] == src['source_span_ids']
        assert row['review_artifact'] == src['review_artifact']
        assert row['source_resolution_changed'] is False
        assert row['condition_compiled'] is False
        assert row['execution_unlocked'] is False


def test_relation_guardrails_hold():
    data = load(MAP)
    g = data['guardrails']
    assert g['source_surface_preserved'] is True
    assert g['named_pattern_flattened'] is False
    assert g['meeting_generic_geometry_invented'] is False
    assert g['source_resolution_changed'] is False
    assert g['condition_compiled'] is False
    assert g['execution_unlocked'] is False
    assert g['product_runtime_modified'] is False
    assert g['numeric_weights_added'] is False
    assert g['probabilities_added'] is False
