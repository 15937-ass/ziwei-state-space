import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HANDOFF_PATH = (
    ROOT / "product" / "PRODUCT_SOURCE_ONLY_VERTICAL_SLICE_BLOCKER_HANDOFF_V0_1.json"
)


def _json(relative_path):
    return json.loads((ROOT / relative_path).read_text(encoding="utf-8"))


def _git_blob_sha(raw):
    header = b"blob " + str(len(raw)).encode("ascii") + b"\0"
    return hashlib.sha1(header + raw).hexdigest()


def _report():
    return json.loads(HANDOFF_PATH.read_text(encoding="utf-8"))


def test_handoff_snapshot_pins_every_source_artifact():
    report = _report()
    assert report["source_artifacts"]
    for source in report["source_artifacts"]:
        raw = (ROOT / source["path"]).read_bytes()
        assert _git_blob_sha(raw) == source["git_blob_sha"], source["path"]


def test_active_lock_and_bundle_are_not_confused_with_historical_impact_report():
    report = _report()
    lock = _json("product/PRODUCT_KNOWLEDGE.lock.json")
    bundle = _json("product/PRODUCT_KNOWLEDGE_BUNDLE_V0_3.json")
    impact = _json("product/PRODUCT_KNOWLEDGE_IMPACT_V0_1.json")

    assert lock["active_bundle_id"] == "KIB-PRODUCT-20261021-V0_3"
    assert lock["promotion_state"] == "ACTIVE"
    assert lock["auto_refresh"] is False
    assert bundle["bundle_id"] == lock["active_bundle_id"]
    assert report["active_product_knowledge"]["lock"]["active_bundle_id"] == lock["active_bundle_id"]
    assert impact["active_bundle_id"] != lock["active_bundle_id"]
    assert report["active_product_knowledge"]["impact_report_caveat"][
        "use_for_current_promotion_decision"
    ] is False


def test_active_components_match_the_handoff_snapshot():
    report = _report()
    bundle = _json("product/PRODUCT_KNOWLEDGE_BUNDLE_V0_3.json")
    components = {item["component_id"]: item for item in bundle["components"]}

    assert components["K_response"]["coverage_status"] == (
        report["active_product_knowledge"]["bundle_components"]["K_response"]["coverage_status"]
    )
    assert len(components["K_response"]["artifacts"]) == 22
    assert components["K_manifest"]["coverage_status"] == "EMPTY_NOT_READY"
    assert components["K_manifest"]["artifacts"] == []
    assert report["active_product_knowledge"]["bundle_components"]["K_manifest"][
        "artifact_count"
    ] == 0


def test_all_three_production_registries_remain_blocked_and_empty():
    report = _report()
    reaction = _json("product/PL3T_TEMPORAL_REACTION_REGISTRY_v0.1.json")
    ontology = _json("product/PL3M_MANIFESTATION_ONTOLOGY_REGISTRY_v0.1.json")
    mapping = _json("product/PL3M_MANIFESTATION_MAPPING_REGISTRY_v0.1.json")

    assert reaction["status"] == "EMPTY_UNTIL_KB_WP07B_STRUCTURED_NORMALIZATION"
    assert reaction["rules"] == []
    assert ontology["registry_status"] == "EMPTY_PENDING_KB_WP06B"
    assert ontology["nodes"] == []
    assert mapping["registry_status"] == "EMPTY_PENDING_KB_WP06C"
    assert mapping["mappings"] == []

    by_id = {item["dependency_id"]: item for item in report["dependencies"]}
    assert by_id["KB-WP07B"]["product_disposition"] == "BLOCKED"
    assert by_id["KB-WP06B"]["product_disposition"] == "BLOCKED"
    assert by_id["KB-WP06C"]["product_disposition"] == "BLOCKED"
    assert all(item["live_knowledge_issue"] is None for item in by_id.values())
    assert all(item["live_knowledge_pr"] is None for item in by_id.values())


def test_temporal_eligibility_audits_are_not_promoted_to_reaction_specs():
    report = _report()
    career = _json(
        "knowledge/wp07b/CAREER_TEMPORAL_REACTION_ELIGIBILITY_SUMMARY_v0.1.json"
    )
    property_audit = _json(
        "knowledge/palaces/P10_property/wp07b/PROPERTY_TEMPORAL_REACTION_ELIGIBILITY_SUMMARY_v0.1.json"
    )

    assert career["candidates_audited"] == 9
    assert career["eligible_for_current_compiler"] == 0
    assert career["blocked"] == 8
    assert career["case_support_only_excluded"] == 1
    assert career["production_registry_should_remain_empty"] is True
    assert property_audit["census"]["candidates_audited"] == 35
    assert property_audit["census"]["eligible_for_current_compiler"] == 0
    assert property_audit["census"]["blocked_reusable"] == 19
    assert property_audit["census"]["case_support_only_excluded"] == 16
    assert report["dependencies"][0]["accepted_specification_available"] is False


def test_live_knowledge_snapshot_is_explicit_and_does_not_invent_issue_numbers():
    report = _report()
    snapshot = report["live_knowledge_work_snapshot"]
    assert snapshot["coordinator_current_known_live_work"] == {}
    assert snapshot["matching_open_knowledge_issues"] == []
    assert snapshot["matching_open_knowledge_prs"] == []
    assert snapshot["excluded_hits"][0]["issue"] == 655
    assert snapshot["excluded_hits"][1]["issue"] == 544
    for shard in snapshot["shard_execution"].values():
        assert shard["status"] == "ACTIVE_NO_ACTIVE_WORK"
        assert shard["active_issue"] is None
        assert shard["active_pr"] is None


def test_promotion_contract_requires_explicit_candidate_validation_and_lock_update():
    report = _report()
    steps = report["downstream_promotion_contract"]["ordered_steps"]
    assert "Build an explicit candidate KIB from active KIB-PRODUCT-20261021-V0_3; do not use Knowledge main as an implicit active dependency." in steps
    assert any("semantic-impact report" in step for step in steps)
    assert any("promotion gate" in step for step in steps)
    assert report["downstream_promotion_contract"]["current_impact_policy"][
        "active_lock_auto_refresh"
    ] is False
    assert report["downstream_promotion_contract"]["active_lock_mutated_by_handoff"] is False


def test_forecast_ledger_and_predictive_claims_remain_gated():
    report = _report()
    assert report["vertical_slice_gate"]["status"] == "GATED"
    assert report["vertical_slice_gate"]["forecast_ledger_activation"] == "DO_NOT_ACTIVATE"
    boundary = report["benchmark_claim_boundary"]
    assert boundary["canonical_fidelity_score"] is None
    assert boundary["expert_method_fidelity_score"] is None
    assert boundary["full_expert_replay_ready"] == "0/24"
    assert boundary["full_source_chart_equivalence_verified"] is False
    assert boundary["predictive_validity"] == "NOT_EVALUATED"
