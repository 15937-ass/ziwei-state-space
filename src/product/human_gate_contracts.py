"""PL2-Q contracts for Human-Gate-approved structures and projections.

This module implements representation contracts only. It deliberately does not:
- assign numeric palace valence;
- invent effect magnitudes;
- promote partial 百官 evidence into a complete 百官朝拱 predicate;
- turn structural states into real-world event predictions.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

from .palace_structure import ResolvedPalace, ResolvedPalaceStructure
from .structure_primitives import adjacent_palaces, is_flanked_by


PATTERN_STATUSES = frozenset({"FORMED", "BROKEN", "UNFORMED", "UNKNOWN"})
PATTERN_SCALES = frozenset({"LARGE", "NOT_LARGE", "UNKNOWN"})
INTEGRITY_DIRECTIONS = frozenset(
    {"PRESERVED", "DEGRADED", "TRANSFORMED", "UNRESOLVED"}
)
VALENCE_STATES = frozenset(
    {"FAVORABLE", "UNFAVORABLE", "MIXED", "UNRESOLVED"}
)
CONFIDENCE_STATES = frozenset(
    {"HIGH", "MEDIUM", "LOW", "CONFLICTED", "INSUFFICIENT_EVIDENCE"}
)
BAIGUAN_ACTIVATION_STATUSES = frozenset(
    {"EXPLICIT_TEMPLATE_MATCH", "PARTIAL_SUPPORT", "CONFLICTED", "ABSENT", "UNKNOWN"}
)

BAIGUAN_COMPONENT_FAMILIES: Mapping[str, tuple[str, ...]] = {
    "ORTHODOX_SUPPORT": ("天府", "天相"),
    "ASSISTANT_SUPPORT": ("左辅", "右弼", "天魁", "天钺"),
    "AUXILIARY_SUPPORT": ("文昌", "文曲", "禄存", "天马"),
    "MINOR_ATTENDANTS": (
        "三台",
        "八座",
        "恩光",
        "天贵",
        "台辅",
        "封诰",
        "龙池",
        "凤阁",
        "天福",
        "天寿",
    ),
}
BAIGUAN_EXPLICIT_EXCLUSIONS = frozenset({"化禄", "化权", "化科"})

_STAR_FIELDS = ("major_stars", "minor_stars", "adjective_stars")


def _star_names(palace: ResolvedPalace) -> frozenset[str]:
    names: set[str] = set()
    for field in _STAR_FIELDS:
        stars = palace.raw.get(field, [])
        if not isinstance(stars, list):
            raise ValueError(f"{palace.palace_id}.{field} must be a list")
        for star in stars:
            if not isinstance(star, Mapping):
                continue
            name = str(star.get("name", "")).strip()
            if name:
                names.add(name)
    return frozenset(names)


@dataclass(frozen=True)
class PatternAssessment:
    """Non-numeric pattern representation approved by HG_PL2N."""

    pattern_id: str
    status: str = "UNKNOWN"
    scale: str = "UNKNOWN"
    integrity_direction: str = "UNRESOLVED"
    magnitude_status: str = "UNIDENTIFIED"
    evidence_rule_ids: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.pattern_id.strip():
            raise ValueError("pattern_id is required")
        if self.status not in PATTERN_STATUSES:
            raise ValueError(f"unsupported pattern status: {self.status}")
        if self.scale not in PATTERN_SCALES:
            raise ValueError(f"unsupported pattern scale: {self.scale}")
        if self.integrity_direction not in INTEGRITY_DIRECTIONS:
            raise ValueError(
                f"unsupported integrity direction: {self.integrity_direction}"
            )
        if self.magnitude_status != "UNIDENTIFIED":
            raise ValueError("PL2-Q does not permit identified numeric pattern magnitude")


@dataclass(frozen=True)
class ContextualValence:
    """Question/domain-specific semantic projection; never a universal palace score."""

    palace_id: str
    domain: str
    target: str
    state: str
    evidence_rule_ids: tuple[str, ...]
    confidence: str

    def __post_init__(self) -> None:
        if not self.palace_id.strip() or not self.domain.strip() or not self.target.strip():
            raise ValueError("palace_id, domain and target are required")
        if self.state not in VALENCE_STATES:
            raise ValueError(f"unsupported contextual valence state: {self.state}")
        if self.confidence not in CONFIDENCE_STATES:
            raise ValueError(f"unsupported confidence state: {self.confidence}")
        if self.state != "UNRESOLVED" and not self.evidence_rule_ids:
            raise ValueError("resolved contextual valence requires rule evidence")


@dataclass(frozen=True)
class BaiguanComponentEvidence:
    family: str
    star: str
    palace_id: str
    relation: str
    source_scope: str

    def __post_init__(self) -> None:
        if self.family not in BAIGUAN_COMPONENT_FAMILIES:
            raise ValueError(f"unsupported Baiguan component family: {self.family}")
        if self.star not in BAIGUAN_COMPONENT_FAMILIES[self.family]:
            raise ValueError(f"{self.star} is not a member of {self.family}")


@dataclass(frozen=True)
class BaiguanQualityGuard:
    component_star: str
    palace_id: str
    guard_id: str
    state: str
    source_scope: str


@dataclass(frozen=True)
class BaiguanSupportProfile:
    """Evidence profile only; not a truth predicate for 百官朝拱."""

    anchor_star: str
    anchor_palace_id: str
    components: tuple[BaiguanComponentEvidence, ...]
    quality_guards: tuple[BaiguanQualityGuard, ...]
    activation_status: str
    activation_criterion: str = "DEFERRED_NO_UNIVERSAL_THRESHOLD"

    def __post_init__(self) -> None:
        if self.anchor_star != "紫微":
            raise ValueError("PL2-Q v0.1 Baiguan profile is scoped to 紫微 only")
        if self.activation_status not in BAIGUAN_ACTIVATION_STATUSES:
            raise ValueError(
                f"unsupported Baiguan activation status: {self.activation_status}"
            )
        if self.activation_status == "EXPLICIT_TEMPLATE_MATCH":
            raise ValueError(
                "PL2-Q v0.1 cannot emit EXPLICIT_TEMPLATE_MATCH until "
                "BAIGUAN_ACTIVATION_CRITERION is source-frozen"
            )


def _component_family(star: str) -> str | None:
    for family, members in BAIGUAN_COMPONENT_FAMILIES.items():
        if star in members:
            return family
    return None


def _relation_to_anchor(
    structure: ResolvedPalaceStructure,
    anchor_palace_id: str,
    palace_id: str,
) -> str | None:
    relation = structure.relation_between(anchor_palace_id, palace_id)
    if relation:
        return relation

    left, right = adjacent_palaces(structure, anchor_palace_id)
    if palace_id == left.palace_id:
        return "FLANK_LEFT"
    if palace_id == right.palace_id:
        return "FLANK_RIGHT"
    return None


def _quality_guards(
    structure: ResolvedPalaceStructure,
    components: tuple[BaiguanComponentEvidence, ...],
) -> tuple[BaiguanQualityGuard, ...]:
    guards: list[BaiguanQualityGuard] = []

    for component in components:
        palace = structure.palace(component.palace_id)
        stars = _star_names(palace)

        if component.star == "天府" and {"地空", "天空"}.intersection(stars):
            guards.append(
                BaiguanQualityGuard(
                    component_star="天府",
                    palace_id=component.palace_id,
                    guard_id="TIANFU_EMPTY_TREASURY_SAME_PALACE",
                    state="DEGRADED_OR_INEFFECTIVE",
                    source_scope="SRC-ZZ-002:十四正曜·紫微·百官朝拱",
                )
            )

        if component.star == "天相" and is_flanked_by(
            structure,
            component.palace_id,
            "擎羊",
            "陀罗",
        ):
            guards.append(
                BaiguanQualityGuard(
                    component_star="天相",
                    palace_id=component.palace_id,
                    guard_id="TIANXIANG_YANG_TUO_FLANK",
                    state="DEGRADED",
                    source_scope="SRC-ZZ-002:十四正曜·紫微·百官朝拱",
                )
            )

    return tuple(sorted(guards, key=lambda item: (item.palace_id, item.guard_id)))


def build_baiguan_support_profile(
    structure: ResolvedPalaceStructure,
    anchor_palace_id: str,
) -> BaiguanSupportProfile:
    """Inventory source-listed 百官 evidence around one 紫微 anchor.

    Relation inventory is intentionally broader than a qualification predicate:
    finding a listed member in SELF/TRIAD/OPPOSITE/FLANK relation records
    evidence but does not assert that the complete named structure is formed.
    """

    anchor = structure.palace(anchor_palace_id)
    if "紫微" not in _star_names(anchor):
        return BaiguanSupportProfile(
            anchor_star="紫微",
            anchor_palace_id=anchor_palace_id,
            components=(),
            quality_guards=(),
            activation_status="UNKNOWN",
        )

    components: list[BaiguanComponentEvidence] = []
    for palace_id in sorted(structure.palaces):
        relation = _relation_to_anchor(structure, anchor_palace_id, palace_id)
        if relation is None:
            continue
        for star in sorted(_star_names(structure.palace(palace_id))):
            family = _component_family(star)
            if family is None:
                continue
            components.append(
                BaiguanComponentEvidence(
                    family=family,
                    star=star,
                    palace_id=palace_id,
                    relation=relation,
                    source_scope="SRC-ZZ-002:十四正曜·紫微·百官朝拱",
                )
            )

    component_tuple = tuple(
        sorted(components, key=lambda item: (item.family, item.star, item.palace_id))
    )
    guards = _quality_guards(structure, component_tuple)

    if not component_tuple:
        status = "ABSENT"
    elif guards:
        status = "CONFLICTED"
    else:
        status = "PARTIAL_SUPPORT"

    return BaiguanSupportProfile(
        anchor_star="紫微",
        anchor_palace_id=anchor_palace_id,
        components=component_tuple,
        quality_guards=guards,
        activation_status=status,
    )


def find_baiguan_support_profiles(
    structure: ResolvedPalaceStructure,
) -> tuple[BaiguanSupportProfile, ...]:
    """Return one evidence profile for each natal 紫微 anchor."""

    profiles = []
    for palace_id in sorted(structure.palaces):
        if "紫微" in _star_names(structure.palace(palace_id)):
            profiles.append(build_baiguan_support_profile(structure, palace_id))
    return tuple(profiles)
