"""Adapter from PL1 normalized horoscope snapshots into PL3-T facts.

The adapter is intentionally lossless with respect to the normalized temporal
scope payload and intentionally non-semantic: it does not decide whether a
temporal configuration is favorable, activating, or event-producing.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any, Iterable, Mapping, Sequence

from .condition_atoms import fact_from_atom
from .temporal_environment import TemporalEnvironmentProfile, TemporalFact, build_temporal_environment_profile
from .natal_prior import NatalStateProfile


SCOPE_TO_LAYER = {
    "decadal": "DECADE",
    "age": "SMALL_LIMIT",
    "yearly": "YEAR",
    "monthly": "MONTH",
    "daily": "DAY",
    "hourly": "HOUR",
}

REQUIRED_SCOPE_KEYS = (
    "index",
    "name",
    "stem",
    "branch",
    "palace_names",
    "mutagen",
    "nominal_age",
    "stars",
)


@dataclass(frozen=True)
class TemporalAssetBundle:
    target_id: str
    solar_date: str
    lunar_date: str
    time_index: int | None
    engine_name: str
    engine_version: str
    adapter_version: str
    temporal_facts: tuple[TemporalFact, ...]
    condition_facts: tuple[str, ...]

    @property
    def target_label(self) -> str:
        if self.target_id:
            return self.target_id
        if self.time_index is None:
            return self.solar_date
        return f"{self.solar_date}#time_index={self.time_index}"


def _required_text(value: Any, field: str) -> str:
    text = str(value or "").strip()
    if not text:
        raise ValueError(f"{field} is required")
    return text


def _stable_json(value: Any) -> str:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )


def _as_sequence(value: Any, field: str) -> Sequence[Any]:
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes)):
        raise ValueError(f"{field} must be an array")
    return value


def _scope_facts(
    *,
    scope_key: str,
    scope: Mapping[str, Any],
    provenance: str,
) -> tuple[list[TemporalFact], set[str]]:
    if scope_key not in SCOPE_TO_LAYER:
        raise ValueError(f"unsupported normalized scope: {scope_key}")
    layer = SCOPE_TO_LAYER[scope_key]

    missing = [key for key in REQUIRED_SCOPE_KEYS if key not in scope]
    if missing:
        raise ValueError(
            f"normalized temporal scope {scope_key} missing keys: {', '.join(missing)}"
        )

    facts: list[TemporalFact] = []
    condition_facts: set[str] = {
        fact_from_atom("TIME_LAYER", layer=layer),
    }
    branch_value = str(scope.get("branch") or "").strip()
    if branch_value:
        condition_facts.add(
            fact_from_atom("BRANCH_PRESENT", layer=layer, branch=branch_value)
        )
    scalar_keys = ("index", "name", "stem", "branch", "nominal_age")
    for key in scalar_keys:
        value = scope.get(key)
        if value is None:
            continue
        facts.append(
            TemporalFact(
                layer=layer,
                fact=f"scope.{key}={_stable_json(value)}",
                provenance=provenance,
            )
        )

    palace_names = _as_sequence(
        scope.get("palace_names"), f"scopes.{scope_key}.palace_names"
    )
    for index, value in enumerate(palace_names):
        facts.append(
            TemporalFact(
                layer=layer,
                fact=f"palace_names[{index}]={_stable_json(value)}",
                provenance=provenance,
            )
        )
        palace_name = str(value or "").strip()
        if palace_name:
            condition_facts.add(
                fact_from_atom(
                    "PALACE_PRESENT",
                    layer=layer,
                    palace_name=palace_name,
                    palace_index=str(index),
                )
            )

    mutagen = _as_sequence(scope.get("mutagen"), f"scopes.{scope_key}.mutagen")
    for index, value in enumerate(mutagen):
        facts.append(
            TemporalFact(
                layer=layer,
                fact=f"mutagen[{index}]={_stable_json(value)}",
                provenance=provenance,
            )
        )
        mutagen_value = str(value or "").strip()
        if mutagen_value:
            condition_facts.add(
                fact_from_atom(
                    "TRANSFORMATION_PRESENT",
                    layer=layer,
                    mutagen=mutagen_value,
                )
            )

    stars = _as_sequence(scope.get("stars"), f"scopes.{scope_key}.stars")
    for palace_index, group in enumerate(stars):
        group_seq = _as_sequence(
            group, f"scopes.{scope_key}.stars[{palace_index}]"
        )
        for star_index, star in enumerate(group_seq):
            if not isinstance(star, Mapping):
                raise ValueError(
                    f"scopes.{scope_key}.stars[{palace_index}][{star_index}] "
                    "must be an object"
                )
            facts.append(
                TemporalFact(
                    layer=layer,
                    fact=(
                        f"stars[{palace_index}][{star_index}]="
                        f"{_stable_json(dict(star))}"
                    ),
                    provenance=provenance,
                )
            )
            star_name = str(star.get("name") or "").strip()
            if star_name:
                condition_facts.add(
                    fact_from_atom("STAR_PRESENT", layer=layer, star=star_name)
                )
                palace_name = (
                    str(palace_names[palace_index] or "").strip()
                    if palace_index < len(palace_names)
                    else ""
                )
                if palace_name:
                    condition_facts.add(
                        fact_from_atom(
                            "PALACE_HAS_STAR",
                            layer=layer,
                            palace_name=palace_name,
                            star=star_name,
                        )
                    )
                    # Preserve a star-bound transformation only when PL1 explicitly
                    # attaches the mutagen to this star object. The scope-level
                    # mutagen list above is intentionally not joined to stars.
                    star_mutagen = str(star.get("mutagen") or "").strip()
                    if star_mutagen:
                        condition_facts.add(
                            fact_from_atom(
                                "TRANSFORMATION_PRESENT",
                                layer=layer,
                                palace_name=palace_name,
                                star=star_name,
                                mutagen=star_mutagen,
                            )
                        )

    return facts, condition_facts


def adapt_normalized_temporal_snapshot(
    full_snapshot: Mapping[str, Any],
    temporal_snapshot: Mapping[str, Any],
) -> TemporalAssetBundle:
    """Convert one PL1 normalized horoscope snapshot into PL3-T facts."""

    engine = full_snapshot.get("engine")
    if not isinstance(engine, Mapping):
        raise ValueError("full snapshot engine must be an object")

    engine_name = _required_text(engine.get("name"), "engine.name")
    engine_version = _required_text(engine.get("version"), "engine.version")
    adapter_version = _required_text(
        engine.get("adapter_version"), "engine.adapter_version"
    )

    target = temporal_snapshot.get("target")
    scopes = temporal_snapshot.get("scopes")
    if not isinstance(target, Mapping):
        raise ValueError("temporal target must be an object")
    if not isinstance(scopes, Mapping):
        raise ValueError("temporal scopes must be an object")

    target_id = _required_text(target.get("target_id"), "target.target_id")
    solar_date = _required_text(
        temporal_snapshot.get("solar_date"), "temporal.solar_date"
    )
    lunar_date = _required_text(
        temporal_snapshot.get("lunar_date"), "temporal.lunar_date"
    )

    raw_time_index = target.get("time_index")
    time_index = int(raw_time_index) if raw_time_index is not None else None

    provenance_root = (
        f"PL1:{engine_name}:{engine_version}:adapter={adapter_version}:target={target_id}"
    )

    facts: list[TemporalFact] = []
    condition_facts: set[str] = set()
    for scope_key in SCOPE_TO_LAYER:
        scope = scopes.get(scope_key)
        if not isinstance(scope, Mapping):
            raise ValueError(f"temporal scopes missing object: {scope_key}")
        scope_facts, scope_condition_facts = _scope_facts(
            scope_key=scope_key,
            scope=scope,
            provenance=f"{provenance_root}:scope={scope_key}",
        )
        facts.extend(scope_facts)
        condition_facts.update(scope_condition_facts)

    yearly_dec = temporal_snapshot.get("yearly_dec_stars")
    if yearly_dec is not None:
        if not isinstance(yearly_dec, Mapping):
            raise ValueError("yearly_dec_stars must be an object or null")
        for key in ("suiqian12", "jiangqian12"):
            values = _as_sequence(
                yearly_dec.get(key), f"yearly_dec_stars.{key}"
            )
            for index, value in enumerate(values):
                facts.append(
                    TemporalFact(
                        layer="YEAR",
                        fact=f"yearly_dec.{key}[{index}]={_stable_json(value)}",
                        provenance=f"{provenance_root}:yearly_dec",
                    )
                )
                tag_value = str(value or "").strip()
                if tag_value:
                    condition_facts.add(
                        fact_from_atom(
                            "TAG_PRESENT",
                            layer="YEAR",
                            tag_system=key,
                            tag=tag_value,
                            index=str(index),
                        )
                    )

    return TemporalAssetBundle(
        target_id=target_id,
        solar_date=solar_date,
        lunar_date=lunar_date,
        time_index=time_index,
        engine_name=engine_name,
        engine_version=engine_version,
        adapter_version=adapter_version,
        temporal_facts=tuple(
            sorted(
                facts,
                key=lambda item: (item.layer, item.fact, item.provenance),
            )
        ),
        condition_facts=tuple(sorted(condition_facts)),
    )


def find_temporal_snapshot(
    full_snapshot: Mapping[str, Any],
    *,
    target_id: str,
) -> Mapping[str, Any]:
    temporal = full_snapshot.get("temporal")
    if not isinstance(temporal, Sequence) or isinstance(temporal, (str, bytes)):
        raise ValueError("full snapshot temporal must be an array")

    matches = []
    for item in temporal:
        if not isinstance(item, Mapping):
            raise ValueError("full snapshot temporal items must be objects")
        target = item.get("target")
        if isinstance(target, Mapping) and str(target.get("target_id", "")).strip() == target_id:
            matches.append(item)

    if not matches:
        raise ValueError(f"target_id not found in normalized temporal snapshot: {target_id}")
    if len(matches) > 1:
        raise ValueError(f"target_id is not unique in normalized temporal snapshot: {target_id}")
    return matches[0]


def adapt_target_from_full_snapshot(
    full_snapshot: Mapping[str, Any],
    *,
    target_id: str,
) -> TemporalAssetBundle:
    return adapt_normalized_temporal_snapshot(
        full_snapshot,
        find_temporal_snapshot(full_snapshot, target_id=target_id),
    )


def build_temporal_environment_from_assets(
    natal_profile: NatalStateProfile,
    bundle: TemporalAssetBundle,
    *,
    reactions: Iterable[Any] = (),
    conflicts: Iterable[str] = (),
    event_relative_context: Iterable[Any] = (),
) -> TemporalEnvironmentProfile:
    """Convenience bridge from validated PL1 assets to the PL3-T core."""

    return build_temporal_environment_profile(
        natal_profile,
        target_label=bundle.target_label,
        temporal_facts=bundle.temporal_facts,
        reactions=reactions,
        conflicts=conflicts,
        event_relative_context=event_relative_context,
    )
