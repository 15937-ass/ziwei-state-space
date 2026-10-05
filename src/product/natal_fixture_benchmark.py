"""Deterministic PL3-N fixture benchmark.

Fixtures are synthetic product-contract cases. They verify rule/runtime
composition and regressions; they are not empirical prediction accuracy data.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

from .natal_domain_registry import load_default_natal_domain_registry


PALACE_BRANCHES: Mapping[str, str] = {
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


@dataclass(frozen=True)
class NatalFixture:
    fixture_id: str
    stars_by_palace: Mapping[str, tuple[Mapping[str, str], ...]]
    expected_active_rules_all: tuple[str, ...]
    expected_inactive_rules: tuple[str, ...]
    expected_structure_contains: tuple[str, ...]
    forbidden_structure_contains: tuple[str, ...]
    expected_baiguan_statuses: tuple[str, ...]


@dataclass(frozen=True)
class NatalFixtureResult:
    fixture_id: str
    profile_id: str
    active_rule_ids: tuple[str, ...]
    named_structure_facts: tuple[str, ...]
    baiguan_statuses: tuple[str, ...]


def _normalize_star(value: Mapping[str, Any]) -> dict[str, Any]:
    name = str(value.get("name", "")).strip()
    if not name:
        raise ValueError("fixture star requires name")
    mutagen = str(value.get("mutagen") or "").strip() or None
    return {
        "name": name,
        "brightness": None,
        "mutagen": mutagen,
        "type": None,
        "scope": None,
    }


def load_natal_fixtures(path: str | Path) -> tuple[NatalFixture, ...]:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if payload.get("schema_version") != "0.1":
        raise ValueError("natal fixture schema_version must be 0.1")
    rows = payload.get("fixtures")
    if not isinstance(rows, list) or not rows:
        raise ValueError("natal fixture document requires fixtures")

    out = []
    seen: set[str] = set()
    for row in rows:
        fixture_id = str(row.get("fixture_id", "")).strip()
        if not fixture_id or fixture_id in seen:
            raise ValueError("fixture_id must be unique and non-empty")
        seen.add(fixture_id)

        raw_stars = row.get("stars_by_palace", {})
        if not isinstance(raw_stars, Mapping):
            raise ValueError(f"{fixture_id}: stars_by_palace must be a mapping")
        unknown_palaces = sorted(set(raw_stars) - set(PALACE_BRANCHES))
        if unknown_palaces:
            raise ValueError(
                f"{fixture_id}: unknown palace labels: {', '.join(unknown_palaces)}"
            )

        stars_by_palace = {
            palace: tuple(dict(star) for star in stars)
            for palace, stars in raw_stars.items()
        }
        out.append(
            NatalFixture(
                fixture_id=fixture_id,
                stars_by_palace=stars_by_palace,
                expected_active_rules_all=tuple(
                    sorted(set(row.get("expected_active_rules_all", [])))
                ),
                expected_inactive_rules=tuple(
                    sorted(set(row.get("expected_inactive_rules", [])))
                ),
                expected_structure_contains=tuple(
                    sorted(set(row.get("expected_structure_contains", [])))
                ),
                forbidden_structure_contains=tuple(
                    sorted(set(row.get("forbidden_structure_contains", [])))
                ),
                expected_baiguan_statuses=tuple(
                    sorted(set(row.get("expected_baiguan_statuses", [])))
                ),
            )
        )
    return tuple(out)


def snapshot_from_fixture(fixture: NatalFixture) -> dict[str, Any]:
    palaces: dict[str, Any] = {}
    for palace_name, branch in PALACE_BRANCHES.items():
        stars = [
            _normalize_star(star)
            for star in fixture.stars_by_palace.get(palace_name, ())
        ]
        palaces[branch] = {
            "name": palace_name[:-1],
            "stem": "甲",
            "branch": branch,
            "is_body_palace": False,
            "major_stars": stars,
            "minor_stars": [],
            "adjective_stars": [],
        }
    return {
        "schema_version": "0.2",
        "engine": {
            "name": "pl3n-fixture",
            "version": "0.1",
            "adapter_version": "0.2",
        },
        "input": {"fixture_id": fixture.fixture_id},
        "natal": {"palaces": palaces},
    }


def run_natal_fixture(
    repository_root: str | Path,
    fixture: NatalFixture,
) -> NatalFixtureResult:
    registry = load_default_natal_domain_registry(repository_root)
    profile = registry.build_profile(snapshot_from_fixture(fixture))
    active = tuple(
        sorted(
            {
                rule.rule_id
                for domain in profile.domains
                for rule in domain.active_rules
            }
        )
    )
    statuses = tuple(
        sorted(profile.activation_status for profile in profile.baiguan_profiles)
    )
    return NatalFixtureResult(
        fixture_id=fixture.fixture_id,
        profile_id=profile.profile_id,
        active_rule_ids=active,
        named_structure_facts=profile.named_structure_facts,
        baiguan_statuses=statuses,
    )


def validate_natal_fixture(
    fixture: NatalFixture,
    result: NatalFixtureResult,
) -> None:
    active = set(result.active_rule_ids)
    missing = sorted(set(fixture.expected_active_rules_all) - active)
    if missing:
        raise AssertionError(
            f"{fixture.fixture_id}: missing expected active rules {missing}"
        )

    forbidden_rules = sorted(set(fixture.expected_inactive_rules).intersection(active))
    if forbidden_rules:
        raise AssertionError(
            f"{fixture.fixture_id}: forbidden rules activated {forbidden_rules}"
        )

    structure_blob = "\n".join(result.named_structure_facts)
    missing_structures = [
        token
        for token in fixture.expected_structure_contains
        if token not in structure_blob
    ]
    if missing_structures:
        raise AssertionError(
            f"{fixture.fixture_id}: missing structures {missing_structures}"
        )

    forbidden_structures = [
        token
        for token in fixture.forbidden_structure_contains
        if token in structure_blob
    ]
    if forbidden_structures:
        raise AssertionError(
            f"{fixture.fixture_id}: forbidden structures present {forbidden_structures}"
        )

    expected_statuses = set(fixture.expected_baiguan_statuses)
    if expected_statuses and not expected_statuses.issubset(set(result.baiguan_statuses)):
        raise AssertionError(
            f"{fixture.fixture_id}: expected Baiguan statuses "
            f"{sorted(expected_statuses)}, got {list(result.baiguan_statuses)}"
        )


def run_natal_fixture_benchmark(
    repository_root: str | Path,
    fixture_path: str | Path,
) -> tuple[NatalFixtureResult, ...]:
    results = []
    for fixture in load_natal_fixtures(fixture_path):
        result = run_natal_fixture(repository_root, fixture)
        validate_natal_fixture(fixture, result)
        results.append(result)
    return tuple(results)
