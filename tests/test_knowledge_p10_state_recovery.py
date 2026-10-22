import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "knowledge/states/P10_PROPERTY_STATE.yaml"
MAP = ROOT / "knowledge/palaces/P10_property/wp07a/PROPERTY_RELATION_CROSS_PALACE_MAP_01_v0.1.json"


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
        'RELATION_CROSS_PALACE_MAP_3_OF_3_MERGED"'
    ) in state
    assert "PR #616 merged at 83db2c351e09cff686527530823e44fda6ec1808" in state
    assert "no Product runtime authorization" in state


def test_p10_relation_mapping_remains_bounded_and_non_executable():
    mapping = json.loads(MAP.read_text(encoding="utf-8"))
    assert mapping["status"] == "MAPPING_COMPLETE_3_OF_3_NOT_PRODUCTION"
    assert mapping["scope"]["nominated_source_rule_ids"] == [
        "TP01-027", "TP02-129", "TP02-163"
    ]
    assert len(mapping["mappings"]) == 3
    assert all(
        row["source_provenance"]["source_span_verified"] is True
        and row["source_provenance"]["time_layer"] == "NATAL"
        and row["source_provenance"]["case_support_only"] is False
        for row in mapping["mappings"]
    )
    assert "does not determine Tianfu treasury state" in mapping["scope"]["mapping_boundary"]
