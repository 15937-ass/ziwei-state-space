import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "knowledge" / "response" / "RESPONSE_SEMANTICS_SCHEMA_v0.1.json"
PILOT_PATH = ROOT / "knowledge" / "response" / "RESPONSE_SEMANTICS_PILOT_v0.1.json"


def _load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_response_semantics_schema_and_pilot_parse():
    schema = _load(SCHEMA_PATH)
    pilot = _load(PILOT_PATH)
    assert schema["title"] == "Zhongzhou Response Semantics Record v0.1"
    assert pilot["schema_version"] == "0.1"
    assert pilot["records"]


def test_record_ids_unique_and_provenance_present():
    pilot = _load(PILOT_PATH)
    records = pilot["records"]
    ids = [record["record_id"] for record in records]
    assert len(ids) == len(set(ids))
    for record in records:
        assert record["provenance"]
        assert all(item["artifact"] and item["locator"] for item in record["provenance"])


def test_lexical_membership_does_not_create_any_or_all_default():
    pilot = _load(PILOT_PATH)
    lexical = [
        record
        for record in pilot["records"]
        if record["semantic_role"] in {"LEXICAL_GROUP", "SCOPED_CATEGORY"}
    ]
    assert lexical
    for record in lexical:
        assert record["activation"]["mode"] == "UNSPECIFIED"
        assert record["interaction"]["type"] == "UNSPECIFIED"


def test_named_composites_can_encode_source_specific_pair_semantics():
    pilot = _load(PILOT_PATH)
    by_term = {record["term"]: record for record in pilot["records"]}
    assert by_term["三台八座"]["activation"]["mode"] == "PAIR_REQUIRED"
    assert by_term["龙池凤阁"]["activation"]["mode"] == "PAIR_REQUIRED"
    assert by_term["禄马交驰"]["activation"]["mode"] == "ALL_MEMBERS"
    assert by_term["禄马交驰"]["relation_constraints"][0]["relation"] == "SAME_PALACE_OR_OPPOSITION"


def test_fire_bell_keeps_generic_shorthand_unresolved_but_local_order_available():
    pilot = _load(PILOT_PATH)
    by_id = {record["record_id"]: record for record in pilot["records"]}
    generic = by_id["RS-GROUP-FIRE-BELL"]
    local = by_id["RS-LOCAL-FIRE-BELL-JIMEN-JUMEN"]

    assert generic["activation"]["mode"] == "UNSPECIFIED"
    assert generic["execution_status"] == "LEXICAL_ONLY"

    assert local["activation"]["mode"] == "SINGLE_MEMBER_VALID"
    assert local["relation_constraints"][0]["relation"] == "同度"
    assert local["ordinal_constraints"][0]["lhs"] == "铃星同度"
    assert local["ordinal_constraints"][0]["rhs"] == "火星同度"
    assert local["interaction"]["type"] == "UNSPECIFIED"


def test_career_kewen_is_scoped_and_heterogeneous():
    pilot = _load(PILOT_PATH)
    record = next(r for r in pilot["records"] if r["record_id"] == "RS-SCOPED-CAREER-KEWEN")
    assert record["scope"]["domain"] == "事业宫"
    assert record["scope"]["palace"] == "事业宫"
    assert any(member["type"] == "TRANSFORMATION_OPERATOR" for member in record["members"])


def test_no_numeric_weights_or_probabilities_in_pilot():
    pilot = _load(PILOT_PATH)
    forbidden = {
        "probability",
        "probabilities",
        "numeric_weight",
        "weight",
        "learned_gain",
        "magnitude_value",
    }

    def walk(value):
        if isinstance(value, dict):
            for key, child in value.items():
                assert key not in forbidden
                walk(child)
        elif isinstance(value, list):
            for child in value:
                walk(child)

    walk(pilot)
    assert pilot["guardrails"]["numeric_weights_added"] is False
    assert pilot["guardrails"]["probabilities_added"] is False
    assert pilot["guardrails"]["product_runtime_modified"] is False


def test_pilot_records_follow_schema_required_fields_and_enums():
    schema = _load(SCHEMA_PATH)
    pilot = _load(PILOT_PATH)
    required = set(schema["required"])
    role_enum = set(schema["properties"]["semantic_role"]["enum"])
    activation_enum = set(
        schema["properties"]["activation"]["properties"]["mode"]["enum"]
    )
    interaction_enum = set(
        schema["properties"]["interaction"]["properties"]["type"]["enum"]
    )
    execution_enum = set(schema["properties"]["execution_status"]["enum"])

    for record in pilot["records"]:
        assert required <= set(record)
        assert record["semantic_role"] in role_enum
        assert record["activation"]["mode"] in activation_enum
        assert record["interaction"]["type"] in interaction_enum
        assert record["execution_status"] in execution_enum


def test_unspecified_semantics_are_not_mislabelled_as_source_explicit():
    pilot = _load(PILOT_PATH)
    for record in pilot["records"]:
        if record["activation"]["mode"] == "UNSPECIFIED":
            assert record["activation"]["source_status"] != "EXPLICIT"
        if record["interaction"]["type"] == "UNSPECIFIED":
            assert record["interaction"]["source_status"] != "EXPLICIT"
