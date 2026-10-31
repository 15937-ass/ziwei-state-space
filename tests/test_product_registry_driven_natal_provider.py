import csv
import json
from pathlib import Path

import pytest

from src.product.natal_domain_providers import DEFAULT_PALACE_ONTOLOGY_PATH
from src.product.natal_domain_registry import load_default_natal_domain_registry
from src.product.palace_structure import load_palace_ontology
from src.product.registry_driven_natal_provider import (
    RegistryDrivenNatalDomainProvider,
    load_registry_driven_natal_provider,
)
from src.product.symbolic_inference_pipeline import run_symbolic_inference

ROOT = Path(__file__).resolve().parents[1]
ONTOLOGY_PATH = ROOT / DEFAULT_PALACE_ONTOLOGY_PATH
ASSET_PATH = ROOT / "product/PL3T_TEMPORAL_ASSET_FIXTURE_v0.1.json"
PRODUCTION_REACTION_REGISTRY = ROOT / "product/PL3T_TEMPORAL_REACTION_REGISTRY_v0.1.json"

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


def _snapshot(stars_by_palace=None):
    full = json.loads(ASSET_PATH.read_text(encoding="utf-8"))
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
    full["natal"] = {"palaces": palaces}
    return full


def _source_row(**overrides):
    row = {
        "projection_rule_id": "CA-TEST-001",
        "source_id": "SRC-TEST-ONLY",
        "source_location": "fixture page 1",
        "palace_id": "P09",
        "time_layer": "NATAL",
        "condition": "事业宫见紫微",
        "projection_domain": "career_structure",
        "projection_target": "career_management",
        "projection_mode": "FUNCTIONAL_PROJECTION",
        "review_status": "SOURCE_SPAN_VERIFIED",
        "source_span_verified": "true",
        "case_support_only": "false",
        "history_feedback": "",
    }
    row.update(overrides)
    return row


def _registry(**overrides):
    registry = {
        "schema_version": "0.1",
        "status": "TEST_FIXTURE_ONLY",
        "provider_id": "PL3N_TEST_CAREER_PROVIDER",
        "domain_id": "career",
        "palace_id": "P09",
        "palace_name": "事业宫",
        "time_layer": "NATAL",
        "topic_scope": "事业",
        "knowledge_version": "TEST_ONLY_CAREER_RULES_1",
        "rules": {
            "CA-TEST-001": {
                "expected_source_id": "SRC-TEST-ONLY",
                "expected_source_location": "fixture page 1",
                "expected_review_status": "SOURCE_SPAN_VERIFIED",
                "expected_condition": "事业宫见紫微",
                "expected_projection_domain": "career_structure",
                "expected_projection_target": "career_management",
                "expected_projection_mode": "FUNCTIONAL_PROJECTION",
                "condition": {
                    "all_of": [
                        {
                            "atom_type": "PALACE_HAS_STAR",
                            "args": {"palace": "P09", "star": "紫微"},
                        }
                    ]
                },
            }
        },
    }
    registry.update(overrides)
    return registry


def _provider(row=None, registry=None):
    return RegistryDrivenNatalDomainProvider(
        projection_rows=[row or _source_row()],
        registry=registry or _registry(),
        palace_ontology=load_palace_ontology(ONTOLOGY_PATH),
    )


def test_registry_driven_provider_executes_only_explicit_test_rule_and_traces_source():
    provider = _provider()
    evidence = provider.build_domain_evidence(
        _snapshot({"事业宫": [_star("紫微")]}),
        question="事业本命结构",
    )

    assert provider.domain_id == "career"
    assert provider.executable_rule_count == 1
    assert [item.rule_id for item in evidence.active_rules] == ["CA-TEST-001"]
    assert evidence.active_rules[0].source_id == "SRC-TEST-ONLY"
    assert evidence.active_rules[0].source_location == "fixture page 1"
    assert evidence.active_rules[0].review_status == "SOURCE_SPAN_VERIFIED"
    assert '"projection_target":"career_management"' in evidence.projection_payloads[0]


def test_registry_driven_provider_does_not_activate_rule_when_condition_is_absent():
    evidence = _provider().build_domain_evidence(_snapshot())

    assert evidence.active_rules == ()
    assert evidence.confidence_band == "INSUFFICIENT_EVIDENCE"
    assert evidence.projection_payloads == ()


@pytest.mark.parametrize(
    "overrides,match",
    [
        ({"case_support_only": "true"}, "CASE_SUPPORT_ONLY cannot execute"),
        ({"source_span_verified": "false"}, "verified source provenance"),
        ({"time_layer": "YEAR"}, "NATAL rows only"),
        ({"palace_id": "P05"}, "does not match provider palace"),
        ({"source_id": "SRC-DRIFT"}, "canonical source drift in source_id"),
        ({"source_location": "changed page"}, "canonical source drift in source_location"),
        ({"review_status": "HUMAN_VERIFIED"}, "canonical source drift in review_status"),
        ({"projection_domain": "changed-domain"}, "canonical source drift in projection_domain"),
        ({"condition": "changed source text"}, "canonical source drift in condition"),
    ],
)
def test_registry_driven_provider_fails_closed_on_source_row_blockers(overrides, match):
    with pytest.raises(ValueError, match=match):
        _provider(row=_source_row(**overrides))


def test_registry_driven_provider_rejects_unknown_atoms_and_unconditional_rules():
    unknown = _registry()
    unknown["rules"]["CA-TEST-001"]["condition"] = {
        "all_of": [{"atom_type": "UNAPPROVED_ATOM", "args": {"value": "x"}}]
    }
    with pytest.raises(ValueError, match="unsupported atom_type"):
        _provider(registry=unknown)

    unconditional = _registry()
    unconditional["rules"]["CA-TEST-001"]["condition"] = {}
    with pytest.raises(ValueError, match="at least one positive atom"):
        _provider(registry=unconditional)


def test_default_registry_remains_wealth_only_until_provider_is_explicitly_added():
    default = load_default_natal_domain_registry(ROOT)
    assert default.domain_ids == ("wealth",)

    provider = _provider()
    extended = load_default_natal_domain_registry(
        ROOT,
        additional_providers=(provider,),
    )
    assert extended.domain_ids == ("career", "wealth")
    profile = extended.build_profile(
        _snapshot({"事业宫": [_star("紫微")]}),
        selected_domains=("career",),
    )
    assert [item.domain_id for item in profile.domains] == ["career"]
    assert [item.rule_id for item in profile.domains[0].active_rules] == ["CA-TEST-001"]


def test_test_only_career_provider_is_explicitly_blocked_in_end_to_end_run():
    snapshot = json.loads(ASSET_PATH.read_text(encoding="utf-8"))
    snapshot["natal"] = _snapshot({"事业宫": [_star("紫微")]} )["natal"]
    provider = _provider()
    registry = load_default_natal_domain_registry(
        ROOT,
        additional_providers=(provider,),
    )
    reaction_document = json.loads(
        PRODUCTION_REACTION_REGISTRY.read_text(encoding="utf-8")
    )

    result = run_symbolic_inference(
        snapshot,
        target_id="T-DEMO",
        question="本命事业结构及目标时间层",
        domain_registry=registry,
        reaction_registry_document=reaction_document,
        selected_domains=("career",),
        selected_temporal_layers=("DECADE", "YEAR"),
    )

    assert result.selected_temporal_layers == ("DECADE", "YEAR")
    assert result.temporal_profile.active_layers == ("DECADE", "YEAR")
    assert result.status == "TEST_FIXTURE_ONLY"
    assert set(result.blockers) == {
        "NON_CANONICAL_NATAL_DOMAIN_PROVIDER",
        "PRODUCTION_TEMPORAL_REACTION_REGISTRY_EMPTY",
    }
    assert [item.rule_id for item in result.natal_profile.domains[0].active_rules] == [
        "CA-TEST-001"
    ]
    conclusion = result.evidence_package.to_dict()["conclusion"]
    assert conclusion["status"] == "PARTIAL"
    assert conclusion["canonical_rule_ids"] == ["CA-TEST-001"]
    assert "NON_CANONICAL_NATAL_DOMAIN_PROVIDER" in conclusion["unknowns"]


def test_registry_loader_requires_canonical_ready_status_and_reads_source_files(tmp_path):
    row = _source_row()
    source_path = tmp_path / "career.csv"
    with source_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row))
        writer.writeheader()
        writer.writerow(row)

    registry = _registry(
        status="CANONICAL_READY",
        projection_sources=["career.csv"],
        palace_ontology=str(ONTOLOGY_PATH),
    )
    registry_path = tmp_path / "provider.json"
    registry_path.write_text(json.dumps(registry, ensure_ascii=False), encoding="utf-8")

    provider = load_registry_driven_natal_provider(tmp_path, registry_path)
    assert provider.executable_rule_count == 1

    registry["status"] = "PENDING_REVIEW"
    registry_path.write_text(json.dumps(registry, ensure_ascii=False), encoding="utf-8")
    with pytest.raises(ValueError, match="must be CANONICAL_READY"):
        load_registry_driven_natal_provider(tmp_path, registry_path)
