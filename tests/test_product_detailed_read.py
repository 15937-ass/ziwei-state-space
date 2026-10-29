import pytest

from src.product.detailed_read import (
    CROSS_DOMAIN_CHECKS,
    DELIVERY_STAGES,
    NATAL_DOMAIN_ORDER,
    VERBALIZER_INSTRUCTIONS,
    build_detailed_read_plan,
    continuation_for_detailed_slot,
)
from src.product.quickread_main_reader import DOMAIN_PALACE


MAIN_SHA = "a" * 40


def test_full_plan_covers_exactly_twelve_unique_natal_domains():
    plan = build_detailed_read_plan("给我完整详批", "chart-001")
    assert len(plan.natal_slots) == 12
    assert tuple(slot.domain for slot in plan.natal_slots) == NATAL_DOMAIN_ORDER
    assert len({slot.slot_id for slot in plan.natal_slots}) == 12
    assert all(slot.temporal_layer == "NATAL" for slot in plan.natal_slots)
    assert all(slot.required_namespaces == ("CANONICAL",) for slot in plan.natal_slots)
    assert plan.temporal_slots == ()


def test_sections_reuse_domains_but_retrieval_identity_stays_atomic():
    plan = build_detailed_read_plan("详批", "chart-001")
    section_domains = [domain for section in plan.sections for domain in section.domains]
    assert section_domains.count("life") > 1
    assert section_domains.count("career") > 1
    assert len(plan.retrieval_slots) == 12
    assert len({slot.slot_id for slot in plan.retrieval_slots}) == 12


def test_user_facing_sections_cover_all_twelve_domains():
    plan = build_detailed_read_plan("详批", "chart-001")
    covered = {domain for section in plan.sections for domain in section.domains}
    assert covered == set(NATAL_DOMAIN_ORDER)


def test_delivery_stages_cover_all_named_sections_before_final_synthesis():
    plan = build_detailed_read_plan("详批", "chart-001")
    staged = {
        section_id
        for stage in DELIVERY_STAGES
        for section_id in stage["section_ids"]
    }
    assert staged == {section.section_id for section in plan.sections}


def test_retrieval_batches_are_staged_and_cover_every_slot_once():
    plan = build_detailed_read_plan("详批", "chart-001")
    batches = plan.retrieval_batches()
    assert batches[0]["stage_id"] == "stage_1_overview"
    assert batches[0]["slot_ids"] == (
        "life_natal",
        "fortune_natal",
        "career_natal",
        "migration_natal",
    )
    flattened = [slot_id for batch in batches for slot_id in batch["slot_ids"]]
    assert len(flattened) == 12
    assert set(flattened) == {slot.slot_id for slot in plan.natal_slots}
    assert len(flattened) == len(set(flattened))


def test_temporal_retrieval_is_deferred_to_stage_four():
    plan = build_detailed_read_plan(
        "详批 2028 年",
        "chart-001",
        temporal_layers=("YEAR",),
        temporal_domains=("career", "relationship"),
    )
    stage_four = next(
        batch for batch in plan.retrieval_batches()
        if batch["stage_id"] == "stage_4_environment_health_time"
    )
    assert "career_year" in stage_four["slot_ids"]
    assert "relationship_year" in stage_four["slot_ids"]


def test_atomic_request_uses_existing_quickread_contract():
    plan = build_detailed_read_plan("详批", "chart-001", mode="SOURCE_FIRST")
    request = plan.request_for_slot("relationship_natal")
    assert request.mode == "SOURCE_FIRST"
    assert request.target_id == "chart-001"
    assert len(request.requested_slots) == 1
    assert request.requested_slots[0].domain == "relationship"
    assert request.min_chars == 240
    assert request.max_chars == 900


def test_temporal_slots_are_opt_in_and_require_temporal_namespace():
    plan = build_detailed_read_plan(
        "详批 2028 年",
        "chart-001",
        temporal_layers=("YEAR",),
        temporal_domains=("career", "relationship"),
    )
    assert len(plan.temporal_slots) == 2
    assert {slot.slot_id for slot in plan.temporal_slots} == {
        "career_year",
        "relationship_year",
    }
    assert all(slot.required_namespaces == ("CANONICAL", "TEMPORAL") for slot in plan.temporal_slots)


def test_temporal_layer_validation_is_fail_closed():
    with pytest.raises(ValueError, match="unsupported DetailedRead temporal layers"):
        build_detailed_read_plan("详批", "chart-001", temporal_layers=("MONTH",))


def test_quickread_continuation_can_upgrade_only_an_already_seen_slot():
    previous = {
        "main_sha": MAIN_SHA,
        "requested_slot_ids": ["relationship_natal", "career_natal"],
        "seen_evidence_ids": [
            "SOURCE:x:rule-1:relationship_natal",
            "SOURCE:y:rule-2:career_natal",
        ],
    }
    relationship = continuation_for_detailed_slot(previous, "relationship_natal")
    assert relationship == {
        "main_sha": MAIN_SHA,
        "requested_slot_ids": ["relationship_natal"],
        "seen_evidence_ids": previous["seen_evidence_ids"],
    }
    assert continuation_for_detailed_slot(previous, "wealth_natal") is None


def test_continuation_requires_a_valid_main_pin():
    with pytest.raises(ValueError, match="40-character Git SHA"):
        continuation_for_detailed_slot(
            {
                "main_sha": "bad",
                "requested_slot_ids": ["relationship_natal"],
                "seen_evidence_ids": [],
            },
            "relationship_natal",
        )


def test_detailed_read_contract_requires_cross_domain_and_cautious_synthesis():
    ids = {item["check_id"] for item in CROSS_DOMAIN_CHECKS}
    assert {
        "career_wealth",
        "relationship_inner_state",
        "family_boundaries",
        "social_boundaries",
        "mobility_outcome",
        "health_caution",
    }.issubset(ids)
    joined = "\n".join(VERBALIZER_INSTRUCTIONS)
    assert "not a promise of strong conclusions" in joined
    assert "mechanical twelve-palace recital" in joined
    assert "non-diagnostic" in joined
    assert "Specific decade/year claims require" in joined


def test_children_domain_is_part_of_quickread_reader_discovery_surface():
    assert DOMAIN_PALACE["children"] == ("P04", "children")
    assert DOMAIN_PALACE["子女宫"] == ("P04", "children")


def test_plan_serialization_exposes_private_chat_delivery_contract():
    payload = build_detailed_read_plan("详批", "chart-001").to_dict()
    assert payload["reading_mode"] == "DETAILED_READ"
    assert payload["retrieval_batches"][0]["stage_id"] == "stage_1_overview"
    assert payload["delivery"]["multi_turn_preferred"] is True
    assert len(payload["delivery"]["stages"]) == 5
    assert payload["delivery"]["stages"][-1]["stage_id"] == "stage_5_synthesis"
    assert payload["delivery"]["mechanical_twelve_palace_output"] is False
    assert payload["delivery"]["final_summary_theme_count"] == {"min": 3, "max": 5}
