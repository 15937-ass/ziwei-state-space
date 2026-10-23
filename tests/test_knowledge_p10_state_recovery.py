import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "knowledge/states/P10_PROPERTY_STATE.yaml"
COMPOUND_MAP = (
    ROOT
    / "knowledge/palaces/P10_property/wp07a/PROPERTY_SAME_PALACE_COMPOUND_STAR_MAP_01_v0.1.json"
)
RELATION_MAP = (
    ROOT
    / "knowledge/palaces/P10_property/wp07a/PROPERTY_RELATION_CROSS_PALACE_MAP_01_v0.1.json"
)

EXPECTED_COMPOUND_IDS = [
    "TP01-071",
    "TP01-072",
    "TP01-097",
    "TP02-121",
    "TP02-126",
    "TP02-160",
    "TP02-186",
    "TP03-226",
    "TP03-227",
    "TP04-306",
    "TP04-310",
    "TP04-311",
    "TP04-340",
]


def _json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def _condition_atoms(condition):
    atoms = list(condition.get("all_of", []))
    for alternative in condition.get("alternatives", []):
        atoms.extend(alternative)
    return atoms


def test_p10_state_cache_matches_merged_acceptance_checkpoint():
    state = STATE.read_text(encoding="utf-8")
    assert 'status: "ACTIVE_NO_ACTIVE_WORK"' in state
    assert "active_issue: null" in state
    assert "active_branch: null" in state
    assert "active_pr: null" in state
    assert (
        'canonical_checkpoint: "PROPERTY_P10_CANONICAL_358_OF_358_ON_MAIN; '
        'NATAL_TRANSFORMATION_MAP_6_OF_6_MERGED; '
        'DIRECT_STAR_PRESENCE_MAP_5_OF_5_MERGED; '
        'DIRECT_STAR_PRESENCE_REMAINDER_6_OF_6_MERGED; '
        'RELATION_CROSS_PALACE_MAP_3_OF_3_MERGED; '
        'SAME_PALACE_COMPOUND_STAR_MAP_13_OF_13_MERGED"'
    ) in state
    assert "PR #616 merged at 83db2c351e09cff686527530823e44fda6ec1808" in state
    assert "PR #661 at ec61c8872ec1e407bf8372e2f2ef67bd225c3661" in state
    assert "PR #660 merged at 6523a0a07051ebe8416dd6d074bf4c6e157aa217" in state
    assert 'snapshot_date: "2026-10-23"' in state
    assert (
        'snapshot_main_commit: "6523a0a07051ebe8416dd6d074bf4c6e157aa217"'
    ) in state
    assert 'cache_semantics: "MUTABLE_RECOVERY_POINTER"' in state
    assert "unresolved Tianfu treasury-state dependency is not inferred" in state
    assert "no Product runtime authorization" in state
    assert 'same_palace_compound_star_mapping:' in state
    assert (
        'artifact: "knowledge/palaces/P10_property/wp07a/PROPERTY_SAME_PALACE_COMPOUND_STAR_MAP_01_v0.1.json"'
    ) in state
    assert 'audit_id: "KB-WP07A-PROPERTY-SAME-PALACE-COMPOUND-STAR-MAP-01"' in state
    assert 'status: "MAPPING_COMPLETE_13_OF_13_NOT_PRODUCTION"' in state
    assert all(rule_id in state for rule_id in EXPECTED_COMPOUND_IDS)
    assert 'execution_readiness: "STATIC_CANDIDATE_NON_EXECUTABLE"' in state
    assert "executable_registry_entry: false" in state
    assert 'unresolved_tianfu_treasury_state: "UNRESOLVED_NOT_INFERRED"' in state


def test_p10_same_palace_compound_map_has_exact_13_source_verified_rows():
    mapping = _json(COMPOUND_MAP)
    assert mapping["status"] == "MAPPING_COMPLETE_13_OF_13_NOT_PRODUCTION"
    assert mapping["scope"]["nominated_source_rule_ids"] == EXPECTED_COMPOUND_IDS
    assert [row["source_rule_id"] for row in mapping["mappings"]] == EXPECTED_COMPOUND_IDS
    assert len(mapping["mappings"]) == 13
    assert "not executable rules" in mapping["scope"]["mapping_boundary"]
    assert mapping["validation"]["mapped_rows"] == 13
    assert mapping["validation"]["executable_rule_created"] is False
    assert mapping["validation"]["production_registry_modified"] is False
    assert mapping["validation"]["tianfu_state_not_inferred"] is True

    for row in mapping["mappings"]:
        provenance = row["source_provenance"]
        assert provenance["source_span_verified"] is True
        assert provenance["review_status"] == "SOURCE_SPAN_VERIFIED"
        assert provenance["time_layer"] == "NATAL"
        assert provenance["case_support_only"] is False
        assert provenance["history_feedback"] is None
        expected_mapping_status = (
            "MAPPED_GEOMETRY_WITH_EXPLICIT_UNRESOLVED_STATE_DEPENDENCY"
            if row["source_rule_id"] == "TP02-126"
            else "MAPPED_EXISTING_ATOMS"
        )
        assert row["mapping_status"] == expected_mapping_status
        assert row["condition_atom_types"] == ["PALACE_HAS_STAR"]
        assert row["execution_readiness"] in {
            "STATIC_COMPOUND_CANDIDATE_NOT_EXECUTABLE",
            "STATIC_COMPOUND_CANDIDATE_WITH_UNRESOLVED_STATE_NOT_EXECUTABLE",
        }
        assert row["executable_registry_entry"] is False
        atoms = _condition_atoms(row["condition"])
        assert atoms
        assert all(atom["atom_type"] == "PALACE_HAS_STAR" for atom in atoms)
        assert all(atom["args"]["palace"] == "P10" for atom in atoms)


def test_p10_compound_map_preserves_explicit_variants_and_unresolved_tianfu_state():
    mapping = _json(COMPOUND_MAP)
    by_id = {row["source_rule_id"]: row for row in mapping["mappings"]}

    fire_bell = by_id["TP02-121"]["condition"]["alternatives"]
    assert [[atom["args"]["star"] for atom in branch] for branch in fire_bell] == [
        ["火星"],
        ["铃星"],
    ]

    tianfu_dependency = by_id["TP02-126"]["source_context"][
        "unresolved_state_dependency"
    ]
    assert tianfu_dependency["state_representable_by_current_approved_atoms"] is False
    assert tianfu_dependency["do_not_infer_from_missing_TRANSFORMATION_PRESENT"] is True
    assert by_id["TP02-126"]["executable_registry_entry"] is False

    alternatives = by_id["TP04-340"]["condition"]["alternatives"]
    assert [[atom["args"]["star"] for atom in branch] for branch in alternatives] == [
        ["廉贞"],
        ["武曲"],
    ]


def test_p10_relation_mapping_remains_bounded_and_non_executable():
    mapping = _json(RELATION_MAP)
    assert mapping["status"] == "MAPPING_COMPLETE_3_OF_3_NOT_PRODUCTION"
    assert mapping["scope"]["nominated_source_rule_ids"] == [
        "TP01-027",
        "TP02-129",
        "TP02-163",
    ]
    assert len(mapping["mappings"]) == 3
    assert all(
        row["source_provenance"]["source_span_verified"] is True
        and row["source_provenance"]["time_layer"] == "NATAL"
        and row["source_provenance"]["case_support_only"] is False
        and row["executable_registry_entry"] is False
        for row in mapping["mappings"]
    )
    assert "does not determine Tianfu treasury state" in mapping["scope"]["mapping_boundary"]
