"""Bounded source-backed structure primitives for product inference.

These predicates encode only structures already supported by reviewed project
assets. They do not provide a generic traditional-pattern parser.
"""

from __future__ import annotations

from typing import Any, Mapping

from .condition_atoms import fact_from_atom
from .palace_structure import ResolvedPalace, ResolvedPalaceStructure


BRANCH_ORDER = ("子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥")

FLANKING_PAIRS: Mapping[str, tuple[str, str]] = {
    "KUI_YUE_FLANK": ("天魁", "天钺"),
    "FU_BI_FLANK": ("左辅", "右弼"),
    "CHANG_QU_FLANK": ("文昌", "文曲"),
    "YANG_TUO_FLANK": ("擎羊", "陀罗"),
}

SOURCE_BACKED_STRUCTURES = frozenset(
    {
        *FLANKING_PAIRS,
        "LU_MA_JIAO_CHI",
        "LU_STACK",
    }
)

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


def _has_mutagen(palace: ResolvedPalace, mutagen: str) -> bool:
    for field in _STAR_FIELDS:
        stars = palace.raw.get(field, [])
        if not isinstance(stars, list):
            raise ValueError(f"{palace.palace_id}.{field} must be a list")
        for star in stars:
            if not isinstance(star, Mapping):
                continue
            if str(star.get("mutagen") or "").strip() == mutagen:
                return True
    return False


def _branch_index(branch: str) -> int:
    try:
        return BRANCH_ORDER.index(branch)
    except ValueError as exc:
        raise ValueError(f"unsupported earthly branch for structure resolver: {branch!r}") from exc


def adjacent_palaces(
    structure: ResolvedPalaceStructure,
    palace_id: str,
) -> tuple[ResolvedPalace, ResolvedPalace]:
    """Return the two branch-adjacent palaces around one target palace."""

    target = structure.palace(palace_id)
    index = _branch_index(target.branch)
    left_branch = BRANCH_ORDER[(index - 1) % len(BRANCH_ORDER)]
    right_branch = BRANCH_ORDER[(index + 1) % len(BRANCH_ORDER)]

    by_branch = {palace.branch: palace for palace in structure.palaces.values()}
    if set(by_branch) != set(BRANCH_ORDER):
        raise ValueError("resolved chart must contain each of the 12 earthly branches exactly once")
    return by_branch[left_branch], by_branch[right_branch]


def is_flanked_by(
    structure: ResolvedPalaceStructure,
    palace_id: str,
    first_star: str,
    second_star: str,
) -> bool:
    """True only when the two named stars occupy opposite adjacent sides."""

    left, right = adjacent_palaces(structure, palace_id)
    left_stars = _star_names(left)
    right_stars = _star_names(right)
    return (
        (first_star in left_stars and second_star in right_stars)
        or (second_star in left_stars and first_star in right_stars)
    )


def _same_or_opposite_split(
    structure: ResolvedPalaceStructure,
    palace_id: str,
    *,
    first_present,
    second_present,
) -> bool:
    """Require the target palace to participate in a same/opposite pair.

    This deliberately does not count a pair located entirely in the opposite
    palace as a structure of the target palace.
    """

    target = structure.palace(palace_id)
    opposite = structure.palace(structure.opposite_of(palace_id))
    if first_present(target) and second_present(target):
        return True
    return (
        first_present(target) and second_present(opposite)
    ) or (
        second_present(target) and first_present(opposite)
    )


def has_lu_ma_jiao_chi(
    structure: ResolvedPalaceStructure,
    palace_id: str,
) -> bool:
    """Source-bounded 禄马交驰: 禄存 and 天马 are same-palace or opposite."""

    return _same_or_opposite_split(
        structure,
        palace_id,
        first_present=lambda palace: "禄存" in _star_names(palace),
        second_present=lambda palace: "天马" in _star_names(palace),
    )


def has_lu_stack(
    structure: ResolvedPalaceStructure,
    palace_id: str,
) -> bool:
    """Source-bounded natal 叠禄: 化禄 and 禄存 are same-palace or opposite."""

    return _same_or_opposite_split(
        structure,
        palace_id,
        first_present=lambda palace: _has_mutagen(palace, "禄"),
        second_present=lambda palace: "禄存" in _star_names(palace),
    )


def source_backed_structure_facts(
    structure: ResolvedPalaceStructure,
) -> frozenset[str]:
    """Emit only the explicitly approved v0.1 named structure facts."""

    facts: set[str] = set()
    for palace_id in sorted(structure.palaces):
        for structure_id, pair in sorted(FLANKING_PAIRS.items()):
            if is_flanked_by(structure, palace_id, *pair):
                facts.add(
                    fact_from_atom(
                        "STRUCTURE_PRESENT",
                        palace=palace_id,
                        structure=structure_id,
                    )
                )

        if has_lu_ma_jiao_chi(structure, palace_id):
            facts.add(
                fact_from_atom(
                    "STRUCTURE_PRESENT",
                    palace=palace_id,
                    structure="LU_MA_JIAO_CHI",
                )
            )
        if has_lu_stack(structure, palace_id):
            facts.add(
                fact_from_atom(
                    "STRUCTURE_PRESENT",
                    palace=palace_id,
                    structure="LU_STACK",
                )
            )

    return frozenset(facts)
