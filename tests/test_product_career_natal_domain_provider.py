import json
from pathlib import Path

import pytest

from src.product.career_natal_domain_provider import (
    _validate_mapping_handoff,
    load_default_career_natal_provider,
)
from src.product.career_inference_service import run_career_inference
from src.product.career_inference_report import (
    _load_temporal_blocker_diagnostics,
    build_career_inference_report,
)
from src.product.event_relative_window import MigrationFirstThreeYearsInput
from src.product.natal_domain_registry import load_default_natal_domain_registry
from src.product.symbolic_inference_pipeline import run_symbolic_inference

ROOT = Path(__file__).resolve().parents[1]
ASSET_PATH = ROOT / "product/PL3T_TEMPORAL_ASSET_FIXTURE_v0.2.json"
REACTION_REGISTRY_PATH = ROOT / "product/PL3T_TEMPORAL_REACTION_REGISTRY_v0.1.json"
MAPPING_PATH = ROOT / "knowledge/wp07a/CAREER_NATAL_ATOMIZATION_MAP_v0.1.json"
REGISTRY_PATH = ROOT / "product/PL3N_CAREER_DOMAIN_PROVIDER_v0.1.json"

BRANCH = {
    "命宫": "酉",
    "兄弟宫": "戌",
    "夫妻宫": "未",
    "子女宫": "申",
    "财帛宫": "巳",
    "疾厄宫": "午",
    "迁移宫": "卯",
    "交友宫": "辰",
    "事业宫": "丑",
    "田宅宫": "寅",
    "福德宫": "亥",
    "父母宫": "子",
}


def _star(name, mutagen=None):
    return {
        "name": name,
        "brightness": None,
        "mutagen": mutagen,
        "type": None,
        "scope": None,
    }


def _natal(stars_by_palace=None):
    stars_by_palace = stars_by_palace or {}
    palaces = {}
    for palace_name, branch in BRANCH.items():
        palaces[branch] = {
            "name": palace_name[:-1],
            "stem": "甲",
            "branch": branch,
            "is_body_palace": False,
            "major_stars": list(stars_by_palace.get(palace_name, [])),
            "minor_stars": [],
            "adjective_stars": [],
        }
    return {"natal": {"palaces": palaces}}


def _full_snapshot(stars_by_palace=None):
    snapshot = json.loads(ASSET_PATH.read_text(encoding="utf-8"))
    snapshot["natal"] = _natal(stars_by_palace)["natal"]
    return snapshot


@pytest.fixture(scope="module")
def provider():
    return load_default_career_natal_provider(ROOT)


def test_canonical_career_provider_is_opt_in_and_has_one_hundred_ninety_pinned_rules(provider):
    assert provider.domain_id == "career"
    assert provider.is_test_only is False
    assert provider.executable_rule_count == 190
    assert {rule.rule_id for rule in provider._executable_rules} == {
        "CA04-347", "CA04-349", "CA09-852",
        "CA01-066", "CA02-188", "CA03-255", "CA01-023",
        "CA01-047", "CA01-050", "CA01-083", "CA01-087", "CA01-088", "CA01-089", "CA01-093", "CA01-095",
        "CA01-026", "CA01-027", "CA01-031", "CA01-032", "CA01-033", "CA01-034", "CA01-042", "CA01-044",
        "CA04-327", "CA05-469", "CA07-671", "CA07-672", "CA07-673", "CA08-765",
        "CA01-052", "CA01-053", "CA01-054", "CA01-055", "CA01-070", "CA01-071", "CA01-078",
        "CA02-155", "CA02-160", "CA03-252", "CA03-254", "CA03-279", "CA03-283", "CA03-285",
        "CA01-067", "CA01-068", "CA01-072", "CA01-076", "CA01-077", "CA01-084",
        "CA02-102", "CA02-103", "CA02-104", "CA02-105", "CA02-109", "CA02-110",
        "CA02-111", "CA02-112", "CA02-114", "CA02-119", "CA02-120", "CA02-122",
        "CA02-124", "CA02-128",
        "CA02-130", "CA02-131", "CA02-132", "CA02-137", "CA02-138", "CA02-142", "CA02-143", "CA02-144",
        "CA02-146", "CA02-151", "CA02-153", "CA02-159", "CA02-161", "CA02-162", "CA02-163", "CA02-165",
        "CA02-172", "CA02-173", "CA02-174", "CA02-183", "CA02-190", "CA02-191", "CA02-192", "CA02-193",
        "CA02-195", "CA02-196", "CA02-200", "CA03-201", "CA03-202", "CA03-203", "CA03-207", "CA03-208",
        "CA03-209", "CA03-210", "CA03-220", "CA03-221", "CA03-222", "CA03-223", "CA03-226", "CA03-227",
        "CA03-232",
        "CA03-241", "CA03-249", "CA03-250", "CA03-253", "CA03-266", "CA03-272", "CA03-284", "CA03-291",
        "CA03-292", "CA03-293", "CA03-294", "CA03-295", "CA03-296", "CA03-297", "CA03-299", "CA03-300",
        "CA04-306", "CA04-307", "CA04-308", "CA04-310", "CA04-315", "CA04-318", "CA04-319", "CA04-322",
        "CA04-329", "CA04-330", "CA04-334", "CA04-336", "CA04-338", "CA04-341",
        "CA04-351", "CA04-352", "CA04-361", "CA04-364", "CA04-369", "CA04-370", "CA04-371",
        "CA04-380", "CA04-381", "CA04-387", "CA04-389", "CA04-395", "CA04-396", "CA04-398",
        "CA04-399", "CA04-400", "CA05-401", "CA05-406", "CA05-407", "CA05-408", "CA05-421",
        "CA05-425", "CA05-426", "CA05-427", "CA05-428", "CA05-430", "CA05-431", "CA05-432",
        "CA05-434", "CA05-440", "CA05-444",
        "CA05-446", "CA05-449", "CA05-452", "CA05-453", "CA05-454", "CA05-455", "CA05-461",
        "CA05-463", "CA05-468", "CA05-476", "CA05-478", "CA05-479", "CA05-498",
        "CA06-503", "CA06-504", "CA06-505", "CA06-513", "CA06-514", "CA06-515", "CA06-518",
        "CA06-524", "CA06-525", "CA06-528", "CA06-530", "CA06-534",
    }

    default = load_default_natal_domain_registry(ROOT)
    assert default.domain_ids == ("wealth",)

    expanded = load_default_natal_domain_registry(
        ROOT,
        additional_providers=(provider,),
    )
    assert expanded.domain_ids == ("career", "wealth")
    assert expanded.test_only_domain_ids == ()


@pytest.mark.parametrize(
    "star_name,mutagen,expected_rules,transformation_rule",
    [
        ("武曲", "科", ["CA04-336", "CA04-338", "CA04-341", "CA04-347"], "CA04-347"),
        ("武曲", "忌", ["CA04-336", "CA04-338", "CA04-341", "CA04-349", "CA04-352"], "CA04-349"),
        ("破军", "禄", ["CA09-852"], "CA09-852"),
    ],
)
def test_exact_star_bound_transformation_coexists_with_applicable_general_rules(
    provider, star_name, mutagen, expected_rules, transformation_rule
):
    evidence = provider.build_domain_evidence(
        _natal({"事业宫": [_star(star_name, mutagen)]}),
        question="事业原局结构",
    )

    active_ids = {rule.rule_id for rule in evidence.active_rules}
    assert set(expected_rules) <= active_ids
    active = next(rule for rule in evidence.active_rules if rule.rule_id == transformation_rule)
    assert active.source_id == "SRC-ZZ-003"
    assert active.review_status == "SOURCE_SPAN_VERIFIED"
    assert active.source_location in {
        "事业宫printed_p140",
        "事业宫printed_p141",
        "事业宫printed_p154",
    }


def test_transformation_rules_fail_closed_while_general_wuqu_rules_still_apply(provider):
    missing = provider.build_domain_evidence(
        _natal({"事业宫": [_star("武曲")]}),
        question="事业原局结构",
    )
    wrong_star = provider.build_domain_evidence(
        _natal({"事业宫": [_star("天同", "科")]}),
        question="事业原局结构",
    )
    wrong_palace = provider.build_domain_evidence(
        _natal({"命宫": [_star("武曲", "科")]}),
        question="事业原局结构",
    )

    missing_ids = {rule.rule_id for rule in missing.active_rules}
    assert {"CA04-336", "CA04-338", "CA04-341"} <= missing_ids
    assert "CA04-347" not in missing_ids
    assert "CA04-349" not in missing_ids
    assert "CA04-352" not in missing_ids
    wrong_star_ids = {rule.rule_id for rule in wrong_star.active_rules}
    assert {"CA04-347", "CA04-349", "CA04-352"}.isdisjoint(wrong_star_ids)
    assert {"CA04-398", "CA04-399", "CA05-406", "CA05-421"} <= wrong_star_ids
    assert wrong_palace.active_rules == ()


def test_product_registry_matches_the_reviewed_mapping_without_mutating_it():
    registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    mapping = json.loads(MAPPING_PATH.read_text(encoding="utf-8"))
    mapping_by_id = {item["source_rule_id"]: item for item in mapping["mappings"]}

    assert registry["status"] == "CANONICAL_READY"
    assert registry["source_mapping"]["mapping_status"] == (
        "SOURCE_GROUNDED_MAPPING_COMPLETE_NOT_EXECUTABLE"
    )
    assert set(registry["source_mapping"]["selected_rule_ids"]) == set(mapping["scope"]["nominated_source_rule_ids"])
    assert set(mapping_by_id) <= set(registry["rules"])

    for rule_id in mapping_by_id:
        product_rule = registry["rules"][rule_id]
        source_mapping = mapping_by_id[rule_id]
        expected = source_mapping["expected_projection"]
        assert product_rule["expected_condition"] == source_mapping["source_condition_text"]
        assert product_rule["condition"] == source_mapping["condition"]
        assert product_rule["expected_source_id"] == source_mapping["source_provenance"]["source_id"]
        assert product_rule["expected_source_location"] == source_mapping["source_provenance"]["source_location"]
        assert product_rule["expected_review_status"] == source_mapping["source_provenance"]["review_status"]
        assert product_rule["expected_projection_domain"] == expected["projection_domain"]
        assert product_rule["expected_projection_target"] == expected["projection_target"]
        assert product_rule["expected_projection_mode"] == expected["projection_mode"]
        assert source_mapping["executable_registry_entry"] is False


def test_end_to_end_career_natal_trace_is_canonical_but_temporal_result_remains_partial(provider):
    snapshot = _full_snapshot({"事业宫": [_star("武曲", "科")]})
    domain_registry = load_default_natal_domain_registry(
        ROOT,
        additional_providers=(provider,),
    )
    reaction_registry = json.loads(
        REACTION_REGISTRY_PATH.read_text(encoding="utf-8")
    )

    result = run_symbolic_inference(
        snapshot,
        target_id="T-DEMO",
        question="事业本命结构及所选大限、流年环境",
        domain_registry=domain_registry,
        reaction_registry_document=reaction_registry,
        selected_domains=("career",),
        selected_temporal_layers=("DECADE", "YEAR"),
    )

    assert result.status == "PARTIAL_TEMPORAL_REGISTRY_EMPTY"
    assert result.blockers == ("PRODUCTION_TEMPORAL_REACTION_REGISTRY_EMPTY",)
    assert result.selected_temporal_layers == ("DECADE", "YEAR")
    assert result.natal_profile.domains[0].domain_id == "career"
    active_ids = {rule.rule_id for rule in result.natal_profile.domains[0].active_rules}
    assert {"CA04-336", "CA04-338", "CA04-341", "CA04-347"} <= active_ids
    assert result.temporal_profile.active_layers == ("DECADE", "YEAR")

    conclusion = result.evidence_package.to_dict()["conclusion"]
    assert conclusion["status"] == "PARTIAL"
    assert {"CA04-336", "CA04-338", "CA04-341", "CA04-347"} <= set(
        conclusion["canonical_rule_ids"]
    )
    assert conclusion["temporal_reaction_rule_ids"] == []
    assert "PRODUCTION_TEMPORAL_REACTION_REGISTRY_EMPTY" in conclusion["unknowns"]
    assert "NO_REAL_WORLD_EVENT_CLAIM" in conclusion["limitations"]
    assert "NO_NUMERIC_PROBABILITY_OR_MAGNITUDE_ESTIMATED" in conclusion["limitations"]
    assert any(
        ref["namespace"] == "CANONICAL"
        and ref["rule_id"] == "CA04-347"
        and ref["source_id"] == "SRC-ZZ-003"
        for ref in conclusion["evidence_refs"]
    )


def test_career_mapping_handoff_validator_rejects_product_mapping_drift(tmp_path):
    registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    mapping = json.loads(MAPPING_PATH.read_text(encoding="utf-8"))

    mapping_dir = tmp_path / "knowledge" / "wp07a"
    mapping_dir.mkdir(parents=True)
    (mapping_dir / MAPPING_PATH.name).write_text(
        json.dumps(mapping, ensure_ascii=False),
        encoding="utf-8",
    )
    registry["source_mapping"]["path"] = str(
        Path("knowledge") / "wp07a" / MAPPING_PATH.name
    )
    registry["rules"] = {i: registry["rules"][i] for i in registry["source_mapping"]["selected_rule_ids"]}
    registry["rules"]["CA04-347"]["expected_projection_target"] = "drifted_target"

    with pytest.raises(ValueError, match="drift in projection_target"):
        _validate_mapping_handoff(tmp_path, registry)


def test_high_level_career_service_uses_production_registry_and_defaults_to_decade_year():
    result = run_career_inference(
        ROOT,
        _full_snapshot({"事业宫": [_star("破军", "禄")]}),
        target_id="T-DEMO",
        question="事业本命结构及大限、流年环境",
    )

    assert result.selected_domains == ("career",)
    assert result.selected_temporal_layers == ("DECADE", "YEAR")
    assert result.status == "PARTIAL_TEMPORAL_REGISTRY_EMPTY"
    assert result.blockers == ("PRODUCTION_TEMPORAL_REACTION_REGISTRY_EMPTY",)
    assert [rule.rule_id for rule in result.natal_profile.domains[0].active_rules] == [
        "CA09-852"
    ]
    conclusion = result.evidence_package.to_dict()["conclusion"]
    assert conclusion["selected_domains"] == ["career"]
    assert conclusion["selected_temporal_layers"] == ["DECADE", "YEAR"]
    assert conclusion["canonical_rule_ids"] == ["CA09-852"]
    assert conclusion["temporal_reaction_rule_ids"] == []


def test_approved_migration_window_flows_through_service_and_report_without_changing_reaction_status():
    run = run_career_inference(
        ROOT,
        _full_snapshot({"事业宫": [_star("武曲", "科")]}),
        target_id="T-DEMO",
        question="事业本命结构及大限、流年环境",
        migration_window=MigrationFirstThreeYearsInput(
            confirmed_distant_settlement=True,
            years_since_distant_relocation=2,
            travel_only=False,
            trigger_provenance="OBS-RELOCATION-001",
        ),
    )
    report = build_career_inference_report(ROOT, run)

    assert run.status == "PARTIAL_TEMPORAL_REGISTRY_EMPTY"
    assert run.blockers == ("PRODUCTION_TEMPORAL_REACTION_REGISTRY_EMPTY",)
    assert run.temporal_profile.external_event_trigger_used is True
    assert run.temporal_profile.active_layers == ("DECADE", "YEAR")
    context = report["temporal"]["event_relative_context"]
    assert len(context) == 1
    assert context[0]["context_id"] == "MIGRATION_FIRST_THREE_YEARS"
    assert context[0]["status"] == "ACTIVE"
    assert context[0]["source"]["source_id"] == "SRC-ZZ-003"
    assert context[0]["trigger_provenance"] == "OBS-RELOCATION-001"
    assert "projection_priority:migration_palace:primary" in context[0]["routing_facts"]
    assert report["temporal"]["matched_reaction_rule_ids"] == []
    assert report["real_world_event_prediction_supported"] is False
    assert "EVENT_RELATIVE_CONTEXT_IS_NOT_A_TEMPORAL_REACTION" in report["limitations"]


@pytest.mark.parametrize(
    "years,travel_only,expected_status",
    [
        (None, False, "INSUFFICIENT"),
        (4, False, "INACTIVE"),
        (2, True, "INACTIVE"),
    ],
)
def test_migration_window_non_active_cases_remain_context_only(years, travel_only, expected_status):
    run = run_career_inference(
        ROOT,
        _full_snapshot(),
        target_id="T-DEMO",
        question="迁移事件相对窗口测试",
        migration_window=MigrationFirstThreeYearsInput(
            confirmed_distant_settlement=True,
            years_since_distant_relocation=years,
            travel_only=travel_only,
            trigger_provenance="OBS-RELOCATION-002",
        ),
    )
    report = build_career_inference_report(ROOT, run)

    assert run.status == "PARTIAL_TEMPORAL_REGISTRY_EMPTY"
    assert run.temporal_profile.event_relative_context[0].status == expected_status
    assert report["temporal"]["event_relative_context"][0]["status"] == expected_status
    assert report["temporal"]["matched_reaction_rule_ids"] == []
    assert report["real_world_event_prediction_supported"] is False


def test_career_inference_report_is_chinese_traceable_and_preserves_partial_status():
    run = run_career_inference(
        ROOT,
        _full_snapshot({"事业宫": [_star("武曲", "忌")]}),
        target_id="T-DEMO",
        question="事业本命结构及大限、流年环境",
    )
    report = build_career_inference_report(ROOT, run)

    assert report["status"] == "PARTIAL_TEMPORAL_REGISTRY_EMPTY"
    assert "正式时间反应规则库为空" in report["status_message_zh"]
    active_ids = {item["rule_id"] for item in report["natal"]["active_rules"]}
    assert {"CA04-336", "CA04-338", "CA04-341", "CA04-349", "CA04-352"} <= active_ids
    assert report["natal"]["active_rule_count"] == len(report["natal"]["active_rules"])
    active = next(item for item in report["natal"]["active_rules"] if item["rule_id"] == "CA04-349")
    assert active["condition"] == "武曲化忌"
    assert active["source"]["source_id"] == "SRC-ZZ-003"
    assert active["source"]["source_location"] == "事业宫printed_p141"
    assert active["projection"]["target"] == "technical_skill_work_scene_preferred"
    assert report["temporal"]["active_layers"] == ["DECADE", "YEAR"]
    assert report["temporal"]["matched_reaction_rule_ids"] == []
    assert report["temporal"]["has_temporal_reaction_evidence"] is False
    assert report["real_world_event_prediction_supported"] is False
    assert "REAL_WORLD_EVENT_PREDICTION_NOT_ESTABLISHED" in report["limitations"]

    readiness = report["temporal"]["readiness_diagnostics"]
    assert readiness["diagnostic_set_id"] == "PL3T_TEMPORAL_BLOCKERS_V0_1"
    assert readiness["new_temporal_rule_activation_allowed"] is False
    assert [
        item["code"] for item in readiness["active_blockers"]
    ] == ["PRODUCTION_TEMPORAL_REACTION_REGISTRY_EMPTY"]
    assert len(readiness["unresolved_gaps"]) == 6
    assert all(
        item["activation_allowed"] is False
        for item in readiness["unresolved_gaps"]
    )


def test_temporal_blocker_diagnostics_reject_any_activation_permission(tmp_path):
    document = json.loads(
        (ROOT / "product/PL3T_TEMPORAL_BLOCKERS_v0.1.json").read_text(
            encoding="utf-8"
        )
    )
    document["items"][0]["activation_allowed"] = True
    path = tmp_path / "unsafe-diagnostics.json"
    path.write_text(json.dumps(document, ensure_ascii=False), encoding="utf-8")

    with pytest.raises(ValueError, match="activation_allowed must remain false"):
        _load_temporal_blocker_diagnostics(path)


def test_product_registry_keeps_temporal_and_event_claims_disabled():
    registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    guardrails = registry["guardrails"]

    assert guardrails["free_text_rule_generation_allowed"] is False
    assert guardrails["case_support_only_allowed"] is False
    assert guardrails["time_layer_other_than_natal_allowed"] is False
    assert guardrails["numeric_probability_allowed"] is False
    assert guardrails["universal_valence_allowed"] is False
    assert guardrails["event_manifestation_inference_allowed"] is False
    assert guardrails["default_registry_activation"] is False
