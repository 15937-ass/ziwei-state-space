import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "knowledge/core/wp06b/ONTOLOGY_CAPABILITY_COMPARISON_FIXTURE_v0.1.json"
PATH_EARLY = "validation/wp05/CA01_career_projection_review_001_100.csv"
PATH_LATE = "validation/wp05/CA05_career_projection_review_401_500.csv"
PATH_WEALTH = "validation/wp05/W01_wealth_projection_review_001_100.csv"
PATH_MIGRATION = "knowledge/palaces/P07_migration/wp05/MIGRATION_M01_SOURCE_READJUDICATION_100_v0.1.json"
ONTOLOGY = ROOT / "product/PL3M_MANIFESTATION_ONTOLOGY_REGISTRY_v0.1.json"
MAPPING = ROOT / "product/PL3M_MANIFESTATION_MAPPING_REGISTRY_v0.1.json"


def data():
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


def csv_index(path):
    with (ROOT / path).open(encoding="utf-8", newline="") as f:
        return {r["projection_rule_id"]: r for r in csv.DictReader(f)}


def test_fixture_is_nonproduction_and_does_not_select_a_root():
    d = data()
    assert d["status"] == "NON_PRODUCTION_DESIGN_FIXTURE_NOT_CANONICAL"
    assert d["main_base_sha"] == "3407150866a5ace99552daa674356b92610f080e"
    assert len(d["source_records"]) == d["source_record_count"] == 36
    assert d["source_set_counts"] == {"P09_CA01": 9, "P09_CA05": 9, "P05_W01": 9, "P07_M01": 9}
    assert len({r["rule_id"] for r in d["source_records"]}) == 36
    assert len(d["synthetic_design_controls"]) == 5
    assert all(c["source_backed"] is False for c in d["synthetic_design_controls"])
    assert d["guardrails"] == {
        "root_option_selected": False,
        "accepted_root_id": None,
        "ontology_node_ids_assigned": False,
        "production_ontology_registry_unchanged": True,
        "production_mapping_registry_unchanged": True,
        "product_consumption_authorized": False,
        "probability_status": "UNKNOWN",
        "runtime_eligible": False,
    }


def test_fixture_records_match_accepted_main_source_rows():
    d = data()
    indexes = {
        PATH_EARLY: csv_index(PATH_EARLY),
        PATH_LATE: csv_index(PATH_LATE),
        PATH_WEALTH: csv_index(PATH_WEALTH),
    }
    migration = json.loads((ROOT / PATH_MIGRATION).read_text(encoding="utf-8"))
    indexes[PATH_MIGRATION] = {r["projection_rule_id"]: r for r in migration["records"]}
    for item in d["source_records"]:
        src = indexes[item["source_path"]][item["rule_id"]]
        assert item["source_id"] == "SRC-ZZ-003"
        assert item["ontology_node_id"] is None
        assert item["probability_status"] == "UNKNOWN"
        assert item["runtime_eligible"] is False
        assert item["projection_mode"] == src["projection_mode"]
        if item["source_path"] == PATH_MIGRATION:
            assert src["canonical_promotion"] is True
            assert src["disposition"] == "DIRECT_SOURCE_RECHECK_CONFIRMED"
            assert item["source_verified"] is True
            assert item["projection_target"] == src["canonical_projection_target"]
            assert item["projection_domain"] == src["canonical_projection_domain"]
        else:
            assert src["review_status"] == "SOURCE_SPAN_VERIFIED"
            assert src["source_span_verified"].lower() == "true"
            assert item["source_verified"] is True
            assert item["projection_target"] == src["projection_target"]
            assert item["projection_domain"] == src["projection_domain"]


def test_fixture_contains_required_boundary_types():
    d = data()
    tags = {tag for item in d["source_records"] for tag in item["design_tags"]}
    assert {
        "PROCESS_PATTERN",
        "ACTION_CONDITIONED_OUTCOME",
        "OCCUPATIONAL_SCENE_NOT_PERSONAL_INJURY_EVENT",
        "DIRECTIONAL_OR_MOBILITY_AXIS_NOT_COMPLETED_MIGRATION_EVENT",
        "CROSS_PALACE_RELATION_NOT_AUTOMATIC_MANIFESTATION",
        "DOMAIN_BOUNDARY_NOT_AUTOMATIC_MANIFESTATION",
        "TEMPORAL_SCOPE",
        "CASE_ONLY_EVENT_CANDIDATE",
    } <= tags
    by_id = {item["rule_id"]: item for item in d["source_records"]}
    assert by_id["CA01-045"]["design_tags"].count("ANTECEDENT_RULES_CA01_042_CA01_044") == 1
    assert by_id["CA05-469"]["case_support_only"] is False
    assert by_id["CA05-493"]["case_support_only"] is True
    assert by_id["M01-006"]["projection_target"] == "home_vs_away_development_axis"


def test_synthetic_controls_keep_missing_conflict_unknown_and_misclassification_distinct():
    d = data()
    controls = {c["control_type"]: c for c in d["synthetic_design_controls"]}
    assert set(controls) == {
        "MISSING_PREREQUISITE",
        "CONFLICTING_EVIDENCE",
        "UNKNOWN",
        "LIKELY_MISCLASSIFICATION",
        "CASE_ONLY_PROMOTION",
    }
    assert controls["MISSING_PREREQUISITE"]["source_backed"] is False
    assert controls["CONFLICTING_EVIDENCE"]["source_backed"] is False
    assert controls["UNKNOWN"]["source_backed"] is False
    assert controls["LIKELY_MISCLASSIFICATION"]["input_record_ref"] == "CA05-469"
    assert controls["LIKELY_MISCLASSIFICATION"]["proposed_invalid_mapping"] == "PERSONAL_INJURY_EVENT"
    assert controls["CASE_ONLY_PROMOTION"]["input_record_ref"] == "CA05-493"


def test_production_registries_remain_empty():
    ontology = json.loads(ONTOLOGY.read_text(encoding="utf-8"))
    mapping = json.loads(MAPPING.read_text(encoding="utf-8"))
    assert ontology["nodes"] == []
    assert ontology["registry_status"] == "EMPTY_PENDING_KB_WP06B"
    assert mapping["mappings"] == []
    assert mapping["registry_status"] == "EMPTY_PENDING_KB_WP06C"
