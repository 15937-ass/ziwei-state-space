import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "knowledge" / "wp07c" / "CAREER_RESPONSE_COMPATIBILITY_02_v0.1.json"
INPUT_REVIEW = ROOT / "knowledge" / "wp07c" / "CAREER_GROUP_LEXICON_REVIEW_02_v0.1.json"


def _load(path=ARTIFACT):
    return json.loads(path.read_text(encoding="utf-8"))


def test_response_compatibility_02_exact_100_unique_records():
    data = _load()
    records = data["records"]
    ids = [row["source_rule_id"] for row in records]
    assert len(records) == 100
    assert len(set(ids)) == 100
    assert ids[0] == "CA04-383"
    assert ids[-1] == "CA07-691"
    assert data["scope"]["cumulative_classified"] == 200
    assert data["scope"]["remaining_after_batch"] == 51


def test_response_compatibility_02_counts_partition_100():
    data = _load()
    counts = data["summary"]["compatibility_band_counts"]
    assert sum(counts.values()) == 100
    assert counts["RS1_RESPONSE_LAYER_COVERS_KNOWN_GROUP_SEMANTICS"] == 22
    assert counts["RS2_PARTIAL_RESPONSE_GAIN"] == 10
    assert counts["RS0_NO_DIRECT_RESPONSE_GAIN"] == 68


def test_compatibility_records_preserve_source_review_identity():
    data = _load()
    source = _load(INPUT_REVIEW)
    source_by_id = {row["source_rule_id"]: row for row in source["records"]}
    assert set(source_by_id) == {row["source_rule_id"] for row in data["records"]}
    for row in data["records"]:
        original = source_by_id[row["source_rule_id"]]
        assert row["source_condition_text"] == original["source_condition_text"]
        assert row["source_location"] == original["source_location"]
        assert row["source_span_ids"] == original["source_span_ids"]
        assert row["review_artifact"] == original["review_artifact"]
        assert row["prior_dependency_class"] == original["dependency_class"]


def test_no_execution_unlock_or_source_resolution_change():
    data = _load()
    assert data["summary"]["source_resolution_changes"] == 0
    assert data["summary"]["conditions_compiled"] == 0
    assert data["summary"]["execution_unlocked"] == 0
    for row in data["records"]:
        assert row["source_resolution_changed"] is False
        assert row["condition_compiled"] is False
        assert row["execution_unlocked"] is False


def test_explicit_member_lists_are_local_only():
    data = _load()
    rows = [
        (row, token)
        for row in data["records"]
        for token in row["token_assessments"]
        if token["semantic_support"] == "EXPLICIT_MEMBER_LIST_BOTH_LOCAL"
    ]
    assert len(rows) == 3
    assert {token['token'] for _, token in rows} == {'左辅右弼', '文昌文曲'}
    assert all(token['activation'] == 'EXPLICIT_AND_LOCAL_CLAUSE' for _, token in rows)
    assert all(token['execution_effect'] == 'LOCAL_ONLY' for _, token in rows)


def test_fire_bell_simultaneity_is_clause_local_not_global_default():
    data = _load()
    row = next(r for r in data["records"] if r["source_rule_id"] == "CA05-429")
    semantics = row['local_clause_semantics']
    local = next(s for s in semantics if s['operator'] == 'GROUP_SIMULTANEITY_LOCAL')
    assert local['group'] == '火铃'
    assert local['activation_hint'] == 'ALL_MEMBERS_IN_THIS_CLAUSE_ONLY'
    token = next(t for t in row['token_assessments'] if t['token'] == '火铃')
    assert token['semantic_support'] == 'MEMBERSHIP_KNOWN_ACTIVATION_UNSPECIFIED'


def test_explicit_or_necessity_and_negation_are_clause_scoped():
    data = _load()
    counts = data["summary"]["local_clause_operator_counts"]
    assert counts['OR'] == 6
    assert counts['NECESSARY'] == 2
    assert counts['NEGATION'] == 10
    for row in data['records']:
        for op in row['local_clause_semantics']:
            assert op.get('scope', 'SOURCE_CLAUSE_ONLY') == 'SOURCE_CLAUSE_ONLY' or op['operator'] == 'GROUP_SIMULTANEITY_LOCAL'


def test_severity_is_not_numericized():
    data = _load()
    severity = [
        token
        for row in data['records']
        for token in row['token_assessments']
        if token['semantic_support'] == 'SEVERITY_LITERAL_UNNUMERICIZED'
    ]
    assert len(severity) == 2
    assert all(token['execution_effect'] == 'BLOCKED_NO_NUMERICIZATION' for token in severity)
    assert data["guardrails"]["severity_numericized"] is False


def test_guardrails_hold():
    data = _load()
    g = data["guardrails"]
    assert g["historical_review_modified"] is False
    assert g["new_source_meaning_invented"] is False
    assert g["explicit_clause_operator_globalized"] is False
    assert g["global_any_default"] is False
    assert g["global_all_default"] is False
    assert g["numeric_weights_added"] is False
    assert g["probabilities_added"] is False
    assert g["product_runtime_modified"] is False
