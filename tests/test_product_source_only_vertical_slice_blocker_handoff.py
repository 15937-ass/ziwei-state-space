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


def test_historical_knowledge_snapshot_is_validated_without_pinning_mutable_state_caches():
    # The handoff is a dated historical snapshot. Current Knowledge state caches
    # are mutable recovery pointers and must follow live Issues/PRs, per
    # governance/RECOVERY_PRECEDENCE_v1.md; they are not snapshot source inputs.
    report = _report()
    snapshot = report["live_knowledge_work_snapshot"]

    assert snapshot["as_of_date"] == "2026-10-22"
    assert snapshot["coordinator_current_known_live_work"] == {}
    assert snapshot["matching_open_knowledge_issues"] == []
    assert snapshot["matching_open_knowledge_prs"] == []
    for shard in snapshot["shard_execution"].values():
        assert shard["status"] == "ACTIVE_NO_ACTIVE_WORK"
        assert shard["active_issue"] is None
        assert shard["active_pr"] is None

    mutable_paths = {
        "knowledge/KNOWLEDGE_STATE.yaml",
        "knowledge/states/CORE_STATE.yaml",
        "knowledge/states/P09_CAREER_STATE.yaml",
        "knowledge/states/P10_PROPERTY_STATE.yaml",
    }
    source_paths = {item["path"] for item in report["source_artifacts"]}
    assert not mutable_paths.intersection(source_paths)

def test_product_recovery_state_is_snapshot_metadata_not_a_mutable_pinned_input():
    report = _report()
    snapshot = report["product_recovery_state_snapshot"]

    assert snapshot["path"] == "product/PRODUCT_STATE.yaml"
    assert report["snapshot_main_commit"] == "f10c68a6e22539f352a37dfe817a7889afcbca07"
    assert snapshot["snapshot_date"] == "2026-10-22"
    assert snapshot["snapshot_main_commit"] == report["snapshot_main_commit"]
    assert snapshot["state_cache_as_main_commit"] == "83077d1d35d92561b0440f91fda645f41ff43496"
    assert snapshot["next_work_unit_at_snapshot"] == "PRODUCT_SOURCE_ONLY_VERTICAL_SLICE_BLOCKER_HANDOFF"
    assert snapshot["state_cache_as_of_product_merge"] == "83077d1d35d92561b0440f91fda645f41ff43496"
    assert snapshot["active_issue_at_snapshot"] is None
    assert snapshot["active_pr_at_snapshot"] is None
    assert "git_blob_sha" not in snapshot
    assert all(source.get("git_blob_sha") for source in report["source_artifacts"])
    assert not any(
        source["path"] == "product/PRODUCT_STATE.yaml"
        for source in report["source_artifacts"]
    )


def test_product_recovery_state_cache_tracks_main_freshness_and_product_checkpoint():
    state = (ROOT / "product" / "PRODUCT_STATE.yaml").read_text(encoding="utf-8")

    assert 'state_cache_as_of_main_commit: "3407150866a5ace99552daa674356b92610f080e"' in state
    assert 'state_cache_as_of_product_merge: "085e65c509fc5f9fed8230d00d2fc07a0e01b79b"' in state
    assert 'state_cache_snapshot_date: "2026-10-23"' in state
    assert 'next_work_unit: "PRODUCT_KIB_UPDATE_AFTER_NEXT_ACCEPTED_COMPILER_READY_SOURCE_ARTIFACT"' in state
    assert "last_completed_product_issue: 696" in state
    assert "last_completed_product_pr: 698" in state

def test_all_recovery_state_caches_are_snapshotted_not_pinned_as_sources():
    report = _report()
    mutable_paths = {
        "product/PRODUCT_STATE.yaml",
        "knowledge/KNOWLEDGE_STATE.yaml",
        "knowledge/states/CORE_STATE.yaml",
        "knowledge/states/P09_CAREER_STATE.yaml",
        "knowledge/states/P10_PROPERTY_STATE.yaml",
    }
    source_paths = {item["path"] for item in report["source_artifacts"]}
    assert not mutable_paths.intersection(source_paths)

    snapshot = report["live_knowledge_work_snapshot"]
    assert snapshot["as_of_date"] == "2026-10-22"
    assert snapshot["snapshot_main_commit"] == "f10c68a6e22539f352a37dfe817a7889afcbca07"
    assert snapshot["recovery_state_paths"] == {
        "coordinator": "knowledge/KNOWLEDGE_STATE.yaml",
        "shards": {
            "CORE": "knowledge/states/CORE_STATE.yaml",
            "P09": "knowledge/states/P09_CAREER_STATE.yaml",
            "P10": "knowledge/states/P10_PROPERTY_STATE.yaml",
        },
    }
    assert "mutable recovery pointers" in snapshot["recovery_state_note"]
