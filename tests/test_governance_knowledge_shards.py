from pathlib import Path
import json

from tools.validate_governance import (
    classify_knowledge_branch,
    knowledge_shard_bad_paths,
)

ROOT = Path(__file__).resolve().parents[1]


def _contracts():
    lane = json.loads((ROOT / "governance/PATH_OWNERSHIP.json").read_text(encoding="utf-8"))
    shards = json.loads((ROOT / "governance/KNOWLEDGE_SHARDS.json").read_text(encoding="utf-8"))
    return lane, shards


def test_classifies_core_and_palace():
    _, shards = _contracts()
    assert classify_knowledge_branch("knowledge/core-600-shared-relation", shards) == ("CORE", None)
    assert classify_knowledge_branch("knowledge/p03-601-spouse-001-100", shards) == ("PALACE", "P03")
    assert classify_knowledge_branch("knowledge/p12-602-parents-001-100", shards) == ("PALACE", "P12")


def test_rejects_legacy_or_invalid_new_knowledge_branch():
    _, shards = _contracts()
    for branch in [
        "knowledge/601-spouse-001-100",
        "knowledge/p13-601-invalid",
        "knowledge/p03-noissue",
        "knowledge/525-property-tp03-canonical",
    ]:
        try:
            classify_knowledge_branch(branch, shards)
        except ValueError:
            pass
        else:
            raise AssertionError(f"branch should be rejected: {branch}")


def test_palace_worker_accepts_own_paths_only():
    lane, shards = _contracts()
    branch = "knowledge/p03-601-spouse-001-100"
    own = [
        "knowledge/palaces/P03_spouse/batch_001.json",
        "validation/knowledge/palaces/P03_spouse/issue_601/evidence.md",
        "tests/test_knowledge_p03_batch_001.py",
        "knowledge/states/P03_SPOUSE_STATE.yaml",
    ]
    assert knowledge_shard_bad_paths(branch, own, lane, shards) == []

    cross = [
        "knowledge/palaces/P05_wealth/batch_001.json",
        "knowledge/states/P05_WEALTH_STATE.yaml",
        "knowledge/KNOWLEDGE_STATE.yaml",
        "knowledge/core/shared_relation.json",
    ]
    assert knowledge_shard_bad_paths(branch, cross, lane, shards) == cross


def test_core_can_write_shared_but_not_palace_artifacts():
    lane, shards = _contracts()
    branch = "knowledge/core-602-relation-semantics"
    shared = [
        "knowledge/core/relation_semantics_v2.json",
        "knowledge/KB_SCHEMA.md",
        "knowledge/REVIEW_SCHEMA_v0.3.md",
        "knowledge/KNOWLEDGE_STATE.yaml",
        "knowledge/states/CORE_STATE.yaml",
        "validation/knowledge/core/issue_602/evidence.md",
        "tests/test_knowledge_core_relation.py",
    ]
    assert knowledge_shard_bad_paths(branch, shared, lane, shards) == []
    palace = [
        "knowledge/palaces/P03_spouse/batch_001.json",
        "knowledge/KB_SCHEMA.md",
        "knowledge/REVIEW_SCHEMA_v0.3.md",
    ]
    assert knowledge_shard_bad_paths(branch, palace, lane, shards) == palace

    # Core receives only the two explicit shared-schema paths, not a broad
    # permission to edit arbitrary root-level Knowledge documentation.
    assert knowledge_shard_bad_paths(
        branch, ["knowledge/UNRELATED_SCHEMA.md"], lane, shards
    ) == ["knowledge/UNRELATED_SCHEMA.md"]


def test_established_property_and_career_roots_remain_shard_local():
    lane, shards = _contracts()
    assert knowledge_shard_bad_paths(
        "knowledge/p10-603-property-tp04",
        [
            "knowledge/wp05/property/PROPERTY_TP04_SOURCE_READJUDICATION_100_v0.1.json",
            "validation/wp05/TP04_property_projection_review_301_400.csv",
            "tests/test_knowledge_property_tp04_canonical.py",
            "knowledge/states/P10_PROPERTY_STATE.yaml",
        ],
        lane,
        shards,
    ) == []
    assert knowledge_shard_bad_paths(
        "knowledge/p09-604-career-gap",
        [
            "knowledge/wp08/CAREER_NEW_GAP_v0.1.md",
            "validation/wp05/CA09_CAREER_PROJECTION_REVIEW.md",
            "tests/test_knowledge_career_gap.py",
            "knowledge/states/P09_CAREER_STATE.yaml",
        ],
        lane,
        shards,
    ) == []


