import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "knowledge" / "wp07c" / "CAREER_RESPONSE_COMPATIBILITY_01_v0.1.json"


def _load():
    return json.loads(ARTIFACT.read_text(encoding="utf-8"))


def test_response_compatibility_01_exact_100_unique_records():
    data = _load()
    records = data["records"]
    ids = [row["source_rule_id"] for row in records]
    assert len(records) == 100
    assert len(set(ids)) == 100
    assert ids[0] == "CA01-057"
    assert ids[-1] == "CA04-382"


def test_response_compatibility_01_never_unlocks_execution():
    data = _load()
    assert data["summary"]["source_resolution_changes"] == 0
    assert data["summary"]["conditions_compiled"] == 0
    assert data["summary"]["execution_unlocked"] == 0
    for row in data["records"]:
        assert row["source_resolution_changed"] is False
        assert row["condition_compiled"] is False
        assert row["execution_unlocked"] is False


def test_response_compatibility_01_counts_partition_100():
    data = _load()
    counts = data["summary"]["compatibility_band_counts"]
    assert sum(counts.values()) == 100
    assert counts["RS1_RESPONSE_LAYER_COVERS_KNOWN_GROUP_SEMANTICS"] == 18
    assert counts["RS2_PARTIAL_RESPONSE_GAIN"] == 17
    assert counts["RS0_NO_DIRECT_RESPONSE_GAIN"] == 65


def test_generic_group_membership_never_creates_any_all_default():
    data = _load()
    for row in data["records"]:
        for token in row["token_assessments"]:
            if token["semantic_support"] == "MEMBERSHIP_KNOWN_ACTIVATION_UNSPECIFIED":
                assert "activation" not in token
                assert token["execution_effect"] == "NONE_AUTOMATIC"


def test_named_composite_semantics_stay_non_executable():
    data = _load()
    named = [
        token
        for row in data["records"]
        for token in row["token_assessments"]
        if token["semantic_support"] == "NAMED_COMPOSITE_PAIR_REQUIREMENT_KNOWN"
    ]
    assert named
    assert all(token["execution_effect"] == "RELATION_BINDING_STILL_REQUIRED" for token in named)


def test_local_fire_bell_candidate_is_not_promoted():
    data = _load()
    row = next(r for r in data["records"] if r["source_rule_id"] == "CA03-228")
    assert row["local_response_candidates"]
    candidate = row["local_response_candidates"][0]
    assert candidate["response_record_id"] == "RS-LOCAL-FIRE-BELL-JIMEN-JUMEN"
    assert candidate["status"] == "CANDIDATE_ONLY_NEEDS_CONTEXT_BINDING"
    assert row["execution_unlocked"] is False


def test_guardrails_hold():
    data = _load()
    g = data["guardrails"]
    assert g["historical_review_modified"] is False
    assert g["new_source_meaning_invented"] is False
    assert g["global_any_default"] is False
    assert g["global_all_default"] is False
    assert g["numeric_weights_added"] is False
    assert g["probabilities_added"] is False
    assert g["product_runtime_modified"] is False
