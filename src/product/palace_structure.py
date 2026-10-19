"""Deterministic palace-structure resolver for PL2-G.

The resolver consumes the approved WP05 palace ontology and a normalized chart
snapshot. It does not infer palace relations from free-form source text and it
does not create new traditional semantics.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Mapping

from .condition_atoms import fact_from_atom


_STAR_FIELDS = ("major_stars", "minor_stars", "adjective_stars")

# Product transport labels, not additions to the canonical Knowledge ontology.
# Match exact pinned engine/version/adapter tuples; never guess unknown labels.
_PINNED_ENGINE_PALACE_ALIASES = {
    ("iztro-js", "2.6.1", "0.2"): {"仆役": "P08"},
    ("x-iztro-rust", "0.6.1", "0.2"): {"仆役": "P08"},
}


def _label_variants(label: str) -> tuple[str, ...]:
    text = str(label).strip()
    if not text:
        return ()
    out = {text}
    if text.endswith("宫") and len(text) > 1:
        out.add(text[:-1])
    return tuple(sorted(out))


@dataclass(frozen=True)
class PalaceOntologyEntry:
    palace_id: str
    canonical_name: str
    aliases: tuple[str, ...]
    opposite_palace_id: str
    triad_palace_ids: tuple[str, str]
    source_basis: str
    status: str


@dataclass(frozen=True)
class PalaceOntology:
    entries: Mapping[str, PalaceOntologyEntry]
    label_to_id: Mapping[str, str]

    def entry(self, palace_id: str) -> PalaceOntologyEntry:
        try:
            return self.entries[palace_id]
        except KeyError as exc:
            raise ValueError(f"unknown palace_id: {palace_id}") from exc

    def resolve_label(self, label: str) -> str | None:
        for candidate in _label_variants(label):
            palace_id = self.label_to_id.get(candidate)
            if palace_id:
                return palace_id
        return None


@dataclass(frozen=True)
class ResolvedPalace:
    palace_id: str
    canonical_name: str
    observed_name: str
    branch: str
    raw: Mapping[str, Any]


@dataclass(frozen=True)
class ResolvedPalaceStructure:
    ontology: PalaceOntology
    palaces: Mapping[str, ResolvedPalace]

    def palace(self, palace_id: str) -> ResolvedPalace:
        try:
            return self.palaces[palace_id]
        except KeyError as exc:
            raise ValueError(f"snapshot missing palace_id: {palace_id}") from exc

    def opposite_of(self, palace_id: str) -> str:
        return self.ontology.entry(palace_id).opposite_palace_id

    def triads_of(self, palace_id: str) -> tuple[str, str]:
        return self.ontology.entry(palace_id).triad_palace_ids

    def sanfang_sizheng_of(self, palace_id: str) -> tuple[str, str, str, str]:
        entry = self.ontology.entry(palace_id)
        return (
            palace_id,
            *entry.triad_palace_ids,
            entry.opposite_palace_id,
        )

    def relation_between(self, source: str, target: str) -> str | None:
        if source == target:
            return "SELF"
        entry = self.ontology.entry(source)
        if target == entry.opposite_palace_id:
            return "OPPOSITE"
        if target in entry.triad_palace_ids:
            return "TRIAD"
        return None

    def runtime_facts(self) -> frozenset[str]:
        """Emit palace-local facts plus explicit ontology relation facts."""

        facts: set[str] = set()
        for palace_id in sorted(self.palaces):
            palace = self.palaces[palace_id]
            facts.add(fact_from_atom("PALACE_PRESENT", palace=palace_id))
            facts.add(
                fact_from_atom(
                    "BRANCH_PRESENT",
                    palace=palace_id,
                    branch=palace.branch,
                )
            )

            for field in _STAR_FIELDS:
                stars = palace.raw.get(field, [])
                if not isinstance(stars, list):
                    raise ValueError(f"{palace_id}.{field} must be a list")
                for star in stars:
                    if not isinstance(star, Mapping):
                        continue
                    name = str(star.get("name", "")).strip()
                    if not name:
                        continue
                    facts.add(
                        fact_from_atom(
                            "PALACE_HAS_STAR",
                            palace=palace_id,
                            star=name,
                        )
                    )
                    mutagen = str(star.get("mutagen") or "").strip()
                    if mutagen:
                        facts.add(
                            fact_from_atom(
                                "TRANSFORMATION_PRESENT",
                                palace=palace_id,
                                mutagen=mutagen,
                            )
                        )
                        facts.add(
                            fact_from_atom(
                                "TRANSFORMATION_PRESENT",
                                palace=palace_id,
                                star=name,
                                mutagen=mutagen,
                            )
                        )

            entry = self.ontology.entry(palace_id)
            facts.add(
                fact_from_atom(
                    "PALACE_RELATION",
                    source=palace_id,
                    target=entry.opposite_palace_id,
                    relation="OPPOSITE",
                )
            )
            for target in entry.triad_palace_ids:
                facts.add(
                    fact_from_atom(
                        "PALACE_RELATION",
                        source=palace_id,
                        target=target,
                        relation="TRIAD",
                    )
                )

        return frozenset(facts)


def _split_aliases(value: str) -> tuple[str, ...]:
    text = str(value or "").strip()
    if not text:
        return ()
    return tuple(
        sorted(
            {
                item.strip()
                for item in text.replace("|", ";").split(";")
                if item.strip()
            }
        )
    )


def load_palace_ontology(path: str | Path) -> PalaceOntology:
    with Path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    return compile_palace_ontology(rows)


def compile_palace_ontology(
    rows: Iterable[Mapping[str, Any]],
) -> PalaceOntology:
    raw_rows = [dict(row) for row in rows]
    if len(raw_rows) != 12:
        raise ValueError(f"palace ontology must contain 12 rows, got {len(raw_rows)}")

    id_by_name: dict[str, str] = {}
    canonical_by_id: dict[str, str] = {}
    aliases_by_id: dict[str, tuple[str, ...]] = {}
    source_by_id: dict[str, str] = {}
    status_by_id: dict[str, str] = {}
    raw_relation_names: dict[str, tuple[str, str, str]] = {}

    for row in raw_rows:
        palace_id = str(row.get("palace_id", "")).strip()
        canonical = str(row.get("canonical_name", "")).strip()
        status = str(row.get("status", "")).strip()
        if not palace_id or not canonical:
            raise ValueError("palace ontology requires palace_id and canonical_name")
        if palace_id in canonical_by_id:
            raise ValueError(f"duplicate palace_id: {palace_id}")
        if status != "ACTIVE":
            raise ValueError(f"{palace_id}: only ACTIVE ontology rows can execute")

        aliases = _split_aliases(str(row.get("legacy_alias", "")))
        labels = {canonical, *aliases}
        for label in labels:
            for variant in _label_variants(label):
                previous = id_by_name.get(variant)
                if previous and previous != palace_id:
                    raise ValueError(
                        f"ambiguous palace label {variant!r}: {previous} vs {palace_id}"
                    )
                id_by_name[variant] = palace_id

        canonical_by_id[palace_id] = canonical
        aliases_by_id[palace_id] = aliases
        source_by_id[palace_id] = str(row.get("source_basis", "")).strip()
        status_by_id[palace_id] = status
        raw_relation_names[palace_id] = (
            str(row.get("opposite_palace", "")).strip(),
            str(row.get("triad_palace_1", "")).strip(),
            str(row.get("triad_palace_2", "")).strip(),
        )

    entries: dict[str, PalaceOntologyEntry] = {}
    for palace_id in sorted(canonical_by_id):
        opposite_name, triad_1_name, triad_2_name = raw_relation_names[palace_id]
        relation_names = (opposite_name, triad_1_name, triad_2_name)
        if not all(relation_names):
            raise ValueError(f"{palace_id}: opposite and two triad palaces are required")

        resolved: list[str] = []
        for name in relation_names:
            target = None
            for variant in _label_variants(name):
                target = id_by_name.get(variant)
                if target:
                    break
            if not target:
                raise ValueError(f"{palace_id}: unknown relation palace {name!r}")
            resolved.append(target)

        opposite_id, triad_1_id, triad_2_id = resolved
        if palace_id in resolved:
            raise ValueError(f"{palace_id}: relation cannot point to itself")
        if len(set(resolved)) != 3:
            raise ValueError(f"{palace_id}: opposite/triad targets must be distinct")

        entries[palace_id] = PalaceOntologyEntry(
            palace_id=palace_id,
            canonical_name=canonical_by_id[palace_id],
            aliases=aliases_by_id[palace_id],
            opposite_palace_id=opposite_id,
            triad_palace_ids=tuple(sorted((triad_1_id, triad_2_id))),
            source_basis=source_by_id[palace_id],
            status=status_by_id[palace_id],
        )

    for palace_id, entry in entries.items():
        opposite = entries[entry.opposite_palace_id]
        if opposite.opposite_palace_id != palace_id:
            raise ValueError(
                f"opposite relation is not symmetric: "
                f"{palace_id} -> {entry.opposite_palace_id}"
            )

        expected_triad = {palace_id, *entry.triad_palace_ids}
        for triad_id in entry.triad_palace_ids:
            triad_entry = entries[triad_id]
            actual = {triad_id, *triad_entry.triad_palace_ids}
            if actual != expected_triad:
                raise ValueError(
                    f"triad relation is not closed: {palace_id} / {triad_id}"
                )

    return PalaceOntology(
        entries=dict(sorted(entries.items())),
        label_to_id=dict(sorted(id_by_name.items())),
    )


def _palace_mapping(snapshot: Mapping[str, Any]) -> Mapping[str, Any]:
    chart = snapshot.get("chart")
    if isinstance(chart, Mapping) and isinstance(chart.get("palaces"), Mapping):
        return chart["palaces"]

    natal = snapshot.get("natal")
    if isinstance(natal, Mapping) and isinstance(natal.get("palaces"), Mapping):
        return natal["palaces"]

    raise ValueError("snapshot has no chart/natal palaces mapping")


def resolve_palace_structure(
    snapshot: Mapping[str, Any],
    ontology: PalaceOntology,
    *,
    extra_aliases: Mapping[str, str] | None = None,
) -> ResolvedPalaceStructure:
    """Bind a normalized snapshot to the canonical 12-palace ontology.

    Pinned exporter transport labels are explicit Product compatibility aliases.
    extra_aliases remains the caller's explicit hook. Neither changes the
    ontology or raw input, and conflicting aliases fail closed.
    """

    raw_palaces = _palace_mapping(snapshot)
    if len(raw_palaces) != 12:
        raise ValueError(f"snapshot must contain 12 palaces, got {len(raw_palaces)}")

    engine = snapshot.get("engine")
    engine_key = (
        tuple(engine.get(field) for field in ("name", "version", "adapter_version"))
        if isinstance(engine, Mapping)
        else ()
    )
    # Invalid metadata is rejected by the service's structural gate. A direct
    # resolver caller must not turn unhashable values into a runtime TypeError.
    pinned_aliases = (
        _PINNED_ENGINE_PALACE_ALIASES.get(engine_key, {})
        if all(isinstance(value, str) for value in engine_key)
        else {}
    )
    explicit_aliases: dict[str, str] = {}
    for aliases in (pinned_aliases, extra_aliases or {}):
        for label, palace_id in aliases.items():
            if palace_id not in ontology.entries:
                raise ValueError(f"extra alias {label!r} targets unknown {palace_id}")
            for variant in _label_variants(label):
                existing = ontology.resolve_label(variant) or explicit_aliases.get(variant)
                if existing and existing != palace_id:
                    raise ValueError(
                        f"adapter alias {label!r} conflicts with palace mapping: "
                        f"{existing} vs {palace_id}"
                    )
                explicit_aliases[variant] = palace_id

    resolved: dict[str, ResolvedPalace] = {}
    branches: set[str] = set()

    for raw_key, raw_palace in raw_palaces.items():
        if not isinstance(raw_palace, Mapping):
            raise ValueError(f"palace {raw_key!r} must be a mapping")

        observed_name = str(raw_palace.get("name", "")).strip()
        candidates = [observed_name, str(raw_key).strip()]
        ids: set[str] = set()

        for candidate in candidates:
            if not candidate:
                continue
            palace_id = ontology.resolve_label(candidate)
            if palace_id:
                ids.add(palace_id)
                continue
            for variant in _label_variants(candidate):
                if variant in explicit_aliases:
                    ids.add(explicit_aliases[variant])

        if not ids:
            raise ValueError(
                f"cannot map snapshot palace name/key to ontology: "
                f"name={observed_name!r}, key={str(raw_key)!r}"
            )
        if len(ids) != 1:
            raise ValueError(
                f"ambiguous snapshot palace mapping for "
                f"name={observed_name!r}, key={str(raw_key)!r}: {sorted(ids)}"
            )

        palace_id = next(iter(ids))
        if palace_id in resolved:
            raise ValueError(f"snapshot maps multiple palaces to {palace_id}")

        branch = str(raw_palace.get("branch", "")).strip()
        if not branch:
            raise ValueError(f"{palace_id}: branch is required")
        if branch in branches:
            raise ValueError(f"duplicate palace branch in snapshot: {branch}")
        branches.add(branch)

        resolved[palace_id] = ResolvedPalace(
            palace_id=palace_id,
            canonical_name=ontology.entry(palace_id).canonical_name,
            observed_name=observed_name or str(raw_key).strip(),
            branch=branch,
            raw=raw_palace,
        )

    missing = sorted(set(ontology.entries) - set(resolved))
    if missing:
        raise ValueError("snapshot missing canonical palaces: " + ", ".join(missing))

    return ResolvedPalaceStructure(
        ontology=ontology,
        palaces=dict(sorted(resolved.items())),
    )
