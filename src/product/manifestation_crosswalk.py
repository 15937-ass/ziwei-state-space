"""Product #897 bounded Knowledge -> Product manifestation crosswalk pilot.

This module is deliberately non-production. It does not populate production
manifestation registries and it does not authorize routing. It provides
deterministic compatibility classification for the first accepted canonical
Knowledge checkpoint so interface gaps can be separated from Core semantic
gaps without silently coercing meaning.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Any, Iterable


CROSSWALK_DISPOSITIONS = frozenset(
    {"DIRECT", "LOSSY", "GAP_PRODUCT", "GAP_CORE", "HOLD"}
)


@dataclass(frozen=True)
class PilotVerdict:
    item_id: str
    crosswalk_disposition: str
    runtime_consumption_allowed: bool
    reason: str

    def __post_init__(self) -> None:
        if self.crosswalk_disposition not in CROSSWALK_DISPOSITIONS:
            raise ValueError(
                f"unsupported crosswalk disposition: {self.crosswalk_disposition}"
            )


def _axis_value(payload: Mapping[str, Any], key: str) -> str | None:
    axis = payload.get(key)
    if not isinstance(axis, Mapping):
        return None
    if axis.get("state") != "KNOWN":
        return None
    value = axis.get("value")
    return str(value).strip() if value is not None else None


def classify_node_crosswalk(node: Mapping[str, Any]) -> PilotVerdict:
    """Classify compatibility with the current PL3-M node adapter."""

    node_id = str(node.get("manifestation_id") or "").strip()
    if not node_id:
        raise ValueError("manifestation_id is required")

    output_kind = _axis_value(node, "output_kind")
    event_specificity = _axis_value(node, "event_specificity")

    if (
        output_kind == "SCENE_OR_CONTEXT"
        and event_specificity == "SCENE_NOT_OBSERVED_EVENT"
    ):
        return PilotVerdict(
            item_id=node_id,
            crosswalk_disposition="LOSSY",
            runtime_consumption_allowed=False,
            reason=(
                "Current Product can represent a coarse SCENE_LEVEL node, but it "
                "cannot losslessly retain SCENE_NOT_OBSERVED_EVENT plus all "
                "normalization and negative-boundary metadata. Research-only "
                "crosswalk is possible; promotion is not."
            ),
        )

    return PilotVerdict(
        item_id=node_id,
        crosswalk_disposition="GAP_PRODUCT",
        runtime_consumption_allowed=False,
        reason=(
            "Current Product node contract lacks a lossless representation for "
            f"output_kind={output_kind!r} and event_specificity={event_specificity!r}."
        ),
    )


def classify_mapping_crosswalk(mapping: Mapping[str, Any]) -> PilotVerdict:
    """Classify one canonical mapping without authorizing execution."""

    mapping_id = str(mapping.get("mapping_id") or "").strip()
    if not mapping_id:
        raise ValueError("mapping_id is required")

    conditions = mapping.get("conditions")
    if not isinstance(conditions, Mapping):
        raise ValueError(f"{mapping_id}: conditions must be an object")

    unresolved = conditions.get("unresolved_semantics") or []
    readiness = str(mapping.get("execution_readiness") or "").strip()
    if unresolved or readiness == "BLOCKED_SEMANTIC":
        return PilotVerdict(
            item_id=mapping_id,
            crosswalk_disposition="HOLD",
            runtime_consumption_allowed=False,
            reason=(
                "Knowledge intentionally preserves unresolved trigger semantics; "
                "Product must not choose an interpretation."
            ),
        )

    prerequisites = conditions.get("real_world_prerequisites") or []
    if prerequisites or readiness == "BLOCKED_EXTERNAL_PREREQUISITE":
        return PilotVerdict(
            item_id=mapping_id,
            crosswalk_disposition="GAP_PRODUCT",
            runtime_consumption_allowed=False,
            reason=(
                "Knowledge meaning is clear, and Product already has an A_t/actions "
                "container, but the current manifestation mapping/router contract "
                "has no governed action-prerequisite predicate binding."
            ),
        )

    output_kind = _axis_value(mapping, "output_kind")
    event_specificity = _axis_value(mapping, "event_specificity")
    if (
        output_kind == "SCENE_OR_CONTEXT"
        and event_specificity == "SCENE_NOT_OBSERVED_EVENT"
    ):
        return PilotVerdict(
            item_id=mapping_id,
            crosswalk_disposition="LOSSY",
            runtime_consumption_allowed=False,
            reason=(
                "A scene-level Product representation is possible only if the "
                "scene/not-observed-event distinction and explicit negative "
                "person-injury/illness boundary remain attached as retained loss "
                "and abstention metadata. Current production registry does not "
                "carry that full contract."
            ),
        )

    return PilotVerdict(
        item_id=mapping_id,
        crosswalk_disposition="GAP_PRODUCT",
        runtime_consumption_allowed=False,
        reason="Current Product mapping contract is not lossless for this mapping.",
    )


def runtime_consumption_allowed(mapping: Mapping[str, Any]) -> bool:
    """Honor Knowledge execution/product gates exactly; never infer permission."""

    return bool(mapping.get("executable")) and bool(mapping.get("product_consumable"))


def flatten_field_paths(payload: Mapping[str, Any]) -> tuple[str, ...]:
    """Return deterministic field paths for coverage auditing.

    Arrays are represented at the array path. Object members inside arrays use
    the [] marker, for example conditions.real_world_prerequisites[].text.
    """

    out: set[str] = set()

    def walk(value: Any, prefix: str) -> None:
        if isinstance(value, Mapping):
            if prefix and not value:
                out.add(prefix)
            for key in sorted(value):
                path = f"{prefix}.{key}" if prefix else str(key)
                child = value[key]
                if isinstance(child, Mapping):
                    walk(child, path)
                elif isinstance(child, Sequence) and not isinstance(
                    child, (str, bytes)
                ):
                    out.add(path)
                    for item in child:
                        if isinstance(item, Mapping):
                            walk(item, path + "[]")
                else:
                    out.add(path)
            return
        if prefix:
            out.add(prefix)

    walk(payload, "")
    return tuple(sorted(out))


def missing_crosswalk_fields(
    records: Iterable[Mapping[str, Any]],
    classified_paths: Iterable[str],
) -> tuple[str, ...]:
    classified = set(classified_paths)
    observed: set[str] = set()
    for record in records:
        observed.update(flatten_field_paths(record))
    return tuple(sorted(observed - classified))
