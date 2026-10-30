import pytest

from src.product.detailed_read import (
    CROSS_DOMAIN_CHECKS,
    DELIVERY_STAGES,
    DetailedReadSession,
    NATAL_DOMAIN_ORDER,
    VERBALIZER_INSTRUCTIONS,
    build_detailed_read_plan,
    continuation_for_detailed_slot,
)
from src.product.quickread_capability import (
    CapabilityManifest,
    CapabilityRecord,
    QuickReadEvidenceItem,
)
from src.product.quickread_main_reader import (
    DOMAIN_PALACE,
    MainKnowledgeBundle,
    MainKnowledgeUnavailable,
    _normalize_domain,
    _palace_code,
)


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
    assert _normalize_domain("children") == "children"
    assert _normalize_domain("子女宫") == "children"
    assert _palace_code("children") == "P04"
    # Adding P04 must not break normalization/scanning for existing domains.
    assert _palace_code("wealth") == "P05"
    assert _palace_code("career") == "P09"


def test_plan_serialization_exposes_private_chat_delivery_contract():
    payload = build_detailed_read_plan("详批", "chart-001").to_dict()
    assert payload["reading_mode"] == "DETAILED_READ"
    assert payload["retrieval_batches"][0]["stage_id"] == "stage_1_overview"
    assert payload["delivery"]["multi_turn_preferred"] is True
    assert len(payload["delivery"]["stages"]) == 5
    assert payload["delivery"]["stages"][-1]["stage_id"] == "stage_5_synthesis"
    assert payload["delivery"]["mechanical_twelve_palace_output"] is False
    assert payload["delivery"]["final_summary_theme_count"] == {"min": 3, "max": 5}

def _session_bundle(
    request,
    *,
    main_sha=MAIN_SHA,
    has_more=False,
    seen_evidence_ids=(),
    excluded_case_only=0,
    runtime_status="NOT_AVAILABLE",
    source_status="NOT_AVAILABLE",
):
    slot = request.requested_slots[0]
    record = CapabilityRecord(
        slot=slot,
        runtime_status=runtime_status,
        source_status=source_status,
        reason="Synthetic test preserves the supplied capability status.",
    )
    manifest = CapabilityManifest(
        main_sha=main_sha,
        knowledge_version="SYNTHETIC-KNOWLEDGE",
        runtime_version="SYNTHETIC-RUNTIME",
        records=(record,),
    )
    return MainKnowledgeBundle(
        request=request,
        manifest=manifest,
        evidence_items=(),
        providers=(),
        reader_report={
            "main_sha": main_sha,
            "continuation": {
                "main_sha": main_sha,
                "requested_slot_ids": [slot.slot_id],
                "seen_evidence_ids": list(seen_evidence_ids),
                "has_more": has_more,
            },
            "slots": [
                {
                    "slot_id": slot.slot_id,
                    "domain": slot.domain,
                    "temporal_layer": slot.temporal_layer,
                    "runtime_status": runtime_status,
                    "source_status": source_status,
                    "runtime_rule_count": 0,
                    "source_evidence_total_eligible": 0,
                    "source_evidence_selected_this_batch": 0,
                    "source_evidence_already_seen": len(seen_evidence_ids),
                    "source_evidence_remaining_after_batch": 2 if has_more else 0,
                    "reason": "No accepted evidence in this synthetic fixture.",
                }
            ],
            "aggregate_source_ledger_counts": {
                "excluded_case_only": excluded_case_only,
                "excluded_not_promoted": 0,
                "excluded_uncertain_or_unverified": 0,
                "excluded_layer_mismatch": 0,
                "excluded_missing_provenance": 0,
            },
        },
    )


def test_session_runs_all_twelve_domains_on_one_main_snapshot():
    calls = []

    def loader(request, **kwargs):
        calls.append((request.requested_slots[0].slot_id, kwargs))
        expected = kwargs.get("expected_main_sha")
        if expected is not None and expected != MAIN_SHA:
            raise MainKnowledgeUnavailable("synthetic stale session")
        return _session_bundle(request)

    plan = build_detailed_read_plan("完整详批", "chart-001")
    session = DetailedReadSession(plan, loader=loader)
    result = session.run_all_stages()

    assert session.main_sha == MAIN_SHA
    assert len(calls) == 12
    assert calls[0][1]["expected_main_sha"] is None
    assert all(call[1]["expected_main_sha"] == MAIN_SHA for call in calls[1:])
    assert result["session_status"] == "NATAL_INSPECTION_COMPLETE"
    assert result["natal_domain_count_required"] == 12
    assert result["natal_domain_count_inspected"] == 12
    assert len(result["coverage"]) == 12
    assert all(item["inspection_status"] == "INSPECTED" for item in result["coverage"])
    assert {item["main_sha"] for item in result["coverage"]} == {MAIN_SHA}


def test_session_rejects_a_loader_that_returns_a_different_main_snapshot():
    calls = 0

    def loader(request, **kwargs):
        nonlocal calls
        calls += 1
        sha = MAIN_SHA if calls <= 4 else "b" * 40
        return _session_bundle(request, main_sha=sha)

    plan = build_detailed_read_plan("完整详批", "chart-001")
    session = DetailedReadSession(plan, loader=loader)
    batches = plan.retrieval_batches()
    session.run_stage(batches[0]["stage_id"])

    next_stage = next(
        batch
        for batch in batches[1:]
        if any(
            slot_id not in session.slot_batches
            for slot_id in batch["slot_ids"]
        )
    )
    with pytest.raises(MainKnowledgeUnavailable, match="mixed main snapshots"):
        session.run_stage(next_stage["stage_id"])


def test_quickread_upgrade_requires_the_same_chart_target():
    plan = build_detailed_read_plan("继续详批", "chart-001")
    cursor = {
        "main_sha": MAIN_SHA,
        "requested_slot_ids": ["relationship_natal"],
        "seen_evidence_ids": ["SOURCE:relationship:rule-1"],
    }
    with pytest.raises(ValueError, match="same chart target_id"):
        DetailedReadSession(
            plan,
            previous_quickread_continuation=cursor,
            previous_quickread_target_id="chart-002",
        )


def test_quickread_cursor_is_reused_only_for_its_slot_but_pins_new_slots():
    calls = []

    def loader(request, **kwargs):
        slot_id = request.requested_slots[0].slot_id
        calls.append((slot_id, kwargs))
        return _session_bundle(request)

    plan = build_detailed_read_plan("简批升级详批", "chart-001")
    cursor = {
        "main_sha": MAIN_SHA,
        "requested_slot_ids": ["relationship_natal"],
        "seen_evidence_ids": ["SOURCE:relationship:rule-1"],
    }
    session = DetailedReadSession(
        plan,
        loader=loader,
        previous_quickread_continuation=cursor,
        previous_quickread_target_id="chart-001",
    )
    session.run_all_stages()

    relationship_call = next(item for item in calls if item[0] == "relationship_natal")
    assert relationship_call[1]["continuation"] == {
        "main_sha": MAIN_SHA,
        "requested_slot_ids": ["relationship_natal"],
        "seen_evidence_ids": ["SOURCE:relationship:rule-1"],
    }
    assert all(item[1]["expected_main_sha"] == MAIN_SHA for item in calls)
    assert all(
        item[1]["continuation"] is None
        for item in calls
        if item[0] != "relationship_natal"
    )


def test_model_supplement_is_counted_separately_from_runtime_and_source():
    def loader(request, **kwargs):
        return _session_bundle(request, excluded_case_only=2)

    plan = build_detailed_read_plan("完整详批", "chart-001")
    session = DetailedReadSession(plan, loader=loader)
    session.run_stage(plan.retrieval_batches()[0]["stage_id"])
    session.add_model_supplement(
        QuickReadEvidenceItem(
            evidence_id="MODEL:life:001",
            slot_id="life_natal",
            lane="MODEL_SUPPLEMENT",
            claim="仅作解释性补充，不构成来源结论。",
            epistemic_label="MODEL_SUPPLEMENT",
            uncertainty="没有被当前接受的运行或来源证据独立验证。",
        )
    )

    result = session.to_dict()
    life = next(item for item in result["coverage"] if item["slot_id"] == "life_natal")
    assert len(result["evidence"]["runtime"]) == 0
    assert len(result["evidence"]["source"]) == 0
    assert len(result["evidence"]["model_supplement"]) == 1
    assert life["runtime_evidence_count"] == 0
    assert life["source_evidence_count"] == 0
    assert life["model_supplement_count"] == 1
    assert result["excluded_evidence_counts"]["excluded_case_support_only"] == 8


def test_model_supplement_cannot_stand_in_for_an_uninspected_domain():
    def loader(request, **kwargs):
        return _session_bundle(request)

    plan = build_detailed_read_plan("完整详批", "chart-001")
    session = DetailedReadSession(plan, loader=loader)
    session.run_stage(plan.retrieval_batches()[0]["stage_id"])
    item = QuickReadEvidenceItem(
        evidence_id="MODEL:children:001",
        slot_id="children_natal",
        lane="MODEL_SUPPLEMENT",
        claim="未被证据覆盖的模型补充。",
        epistemic_label="MODEL_SUPPLEMENT",
        uncertainty="该补充没有被当前接受证据验证。",
    )
    with pytest.raises(ValueError, match="uninspected domain"):
        session.add_model_supplement(item)


def test_slot_continuation_keeps_the_session_pin_and_seen_evidence_cursor():
    calls = []

    def loader(request, **kwargs):
        slot_id = request.requested_slots[0].slot_id
        continuation = kwargs.get("continuation")
        calls.append((slot_id, kwargs))
        has_more = slot_id == "life_natal" and continuation is None
        seen = () if continuation is None else ("SOURCE:life:rule-1",)
        return _session_bundle(
            request,
            has_more=has_more,
            seen_evidence_ids=seen,
        )

    plan = build_detailed_read_plan("完整详批", "chart-001")
    session = DetailedReadSession(plan, loader=loader)
    session.run_stage(plan.retrieval_batches()[0]["stage_id"])
    before = session.slot_report("life_natal")
    assert before["batch_count"] == 1

    after = session.continue_slot("life_natal")
    assert after["batch_count"] == 2
    life_calls = [item for item in calls if item[0] == "life_natal"]
    assert len(life_calls) == 2
    assert life_calls[1][1]["expected_main_sha"] == MAIN_SHA
    assert life_calls[1][1]["continuation"]["main_sha"] == MAIN_SHA
    assert life_calls[1][1]["continuation"]["requested_slot_ids"] == ["life_natal"]


def test_running_a_completed_stage_is_idempotent():
    calls = []

    def loader(request, **kwargs):
        calls.append(request.requested_slots[0].slot_id)
        return _session_bundle(request)

    plan = build_detailed_read_plan("完整详批", "chart-001")
    session = DetailedReadSession(plan, loader=loader)
    stage_id = plan.retrieval_batches()[0]["stage_id"]
    session.run_stage(stage_id)
    first_count = len(calls)
    repeated = session.run_stage(stage_id)

    assert len(calls) == first_count
    assert repeated["completed"] is True

def test_unknown_capability_status_is_preserved_instead_of_becoming_available():
    def loader(request, **kwargs):
        return _session_bundle(
            request,
            runtime_status="UNKNOWN",
            source_status="UNKNOWN",
        )

    plan = build_detailed_read_plan("完整详批", "chart-001")
    session = DetailedReadSession(plan, loader=loader)
    session.run_stage(plan.retrieval_batches()[0]["stage_id"])
    life = next(
        item for item in session.to_dict()["coverage"]
        if item["slot_id"] == "life_natal"
    )

    assert life["runtime_status"] == "UNKNOWN"
    assert life["source_status"] == "UNKNOWN"
    assert life["runtime_evidence_count"] == 0
    assert life["source_evidence_count"] == 0

