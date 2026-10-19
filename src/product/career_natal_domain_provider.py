"""Canonical Career natal provider entry point.

The provider is opt-in so the existing default registry remains backward
compatible and Wealth-only.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping

from .registry_driven_natal_provider import (
    RegistryDrivenNatalDomainProvider,
    load_registry_driven_natal_provider,
)


DEFAULT_CAREER_PROVIDER_REGISTRY_PATH = (
    "product/PL3N_CAREER_DOMAIN_PROVIDER_v0.1.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError(f"{path}: expected a JSON object")
    return value


def _validate_mapping_handoff(
    repository_root: str | Path,
    registry: Mapping[str, Any],
) -> None:
    """Ensure the Product registry is a faithful executable rendering of the reviewed mapping."""

    root = Path(repository_root).resolve()
    mapping_meta = registry.get("source_mapping")
    if not isinstance(mapping_meta, Mapping):
        raise ValueError("Career provider registry requires source_mapping provenance")

    relative_path = str(mapping_meta.get("path", "")).strip()
    if not relative_path:
        raise ValueError("Career provider source_mapping.path is required")
    mapping_path = (root / relative_path).resolve()
    if not mapping_path.is_relative_to(root):
        raise ValueError("Career provider source mapping must remain inside repository root")

    mapping = _load_json(mapping_path)
    expected_status = mapping_meta.get("mapping_status")
    if not isinstance(expected_status, str) or expected_status not in {
        "SOURCE_GROUNDED_MAPPING_COMPLETE_NOT_EXECUTABLE",
        "SOURCE_GROUNDED_STAR_PRESENCE_MAPPING_COMPLETE_NOT_EXECUTABLE",
    }:
        raise ValueError("Career provider mapping_status is not an approved reviewed mapping status")
    if str(mapping.get("schema_version", "")).strip() != str(
        mapping_meta.get("schema_version", "")
    ).strip():
        raise ValueError("Career provider source mapping schema_version mismatch")
    if str(mapping.get("audit_id", "")).strip() != str(
        mapping_meta.get("audit_id", "")
    ).strip():
        raise ValueError("Career provider source mapping audit_id mismatch")
    if str(mapping.get("status", "")).strip() != expected_status:
        raise ValueError("Career provider source mapping must remain a reviewed non-executable mapping")
    if str(mapping_meta.get("mapping_status", "")).strip() != expected_status:
        raise ValueError("Career provider registry mapping_status mismatch")

    scope = mapping.get("scope")
    mappings = mapping.get("mappings")
    rules = registry.get("rules")
    if not isinstance(scope, Mapping) or not isinstance(mappings, list) or not isinstance(rules, Mapping):
        raise ValueError("Career provider source mapping has invalid scope, mappings, or rules")

    nominated_ids = {
        str(item).strip()
        for item in scope.get("nominated_source_rule_ids", [])
        if str(item).strip()
    }
    mapping_by_id = {
        str(item.get("source_rule_id", "")).strip(): item
        for item in mappings
        if isinstance(item, Mapping) and str(item.get("source_rule_id", "")).strip()
    }
    selected = mapping_meta.get("selected_rule_ids", sorted(nominated_ids))
    if (not isinstance(selected, list) or not selected
        or any(not isinstance(item, str) or not item for item in selected)
        or len(selected) != len(set(selected))):
        raise ValueError("Career mapping selected_rule_ids must be a nonempty unique list")
    selected_ids = set(selected)
    if (len(mapping_by_id) != len(mappings) or nominated_ids != set(mapping_by_id)
        or not selected_ids <= nominated_ids or selected_ids != set(rules)):
        raise ValueError("Career provider rules must exactly match nominated source mapping IDs")

    for rule_id in sorted(selected_ids):
        source_map = mapping_by_id[rule_id]
        product_rule = rules[rule_id]
        if not isinstance(product_rule, Mapping):
            raise ValueError(f"{rule_id}: Product registry rule must be an object")
        required_readiness = mapping_meta.get("required_execution_readiness")
        readiness = source_map.get("execution_readiness")
        if (required_readiness is not None and readiness != required_readiness) or (
            isinstance(readiness, str) and readiness.startswith("BLOCKED_")
        ):
            raise ValueError(f"{rule_id}: source mapping execution readiness is blocked or mismatched")
        if expected_status == "SOURCE_GROUNDED_STAR_PRESENCE_MAPPING_COMPLETE_NOT_EXECUTABLE":
            modality = source_map.get("source_modality_note")
            if not isinstance(modality, str) or not modality.strip():
                raise ValueError(f"{rule_id}: source modality note is required")
            if product_rule.get("expected_source_modality_note") != modality:
                raise ValueError(f"{rule_id}: Product/source mapping drift in source modality note")
        provenance = source_map.get("source_provenance")
        projection = source_map.get("expected_projection")
        if not isinstance(provenance, Mapping) or not isinstance(projection, Mapping):
            raise ValueError(f"{rule_id}: source mapping lacks provenance or projection")
        if (
            provenance.get("review_status") != "SOURCE_SPAN_VERIFIED"
            or provenance.get("source_span_verified") is not True
            or provenance.get("time_layer") != "NATAL"
            or provenance.get("case_support_only") is not False
            or source_map.get("mapping_status") != "MAPPED_EXISTING_ATOM"
            or source_map.get("executable_registry_entry") is not False
        ):
            raise ValueError(f"{rule_id}: source mapping provenance is not eligible for Product compilation")

        comparisons = (
            (product_rule.get("expected_source_id"), provenance.get("source_id"), "source_id"),
            (product_rule.get("expected_source_location"), provenance.get("source_location"), "source_location"),
            (product_rule.get("expected_review_status"), provenance.get("review_status"), "review_status"),
            (product_rule.get("expected_condition"), source_map.get("source_condition_text"), "condition text"),
            (product_rule.get("condition"), source_map.get("condition"), "condition atoms"),
            (product_rule.get("expected_projection_domain"), projection.get("projection_domain"), "projection_domain"),
            (product_rule.get("expected_projection_target"), projection.get("projection_target"), "projection_target"),
            (product_rule.get("expected_projection_mode"), projection.get("projection_mode"), "projection_mode"),
        )
        for actual, expected, field_name in comparisons:
            if actual != expected:
                raise ValueError(f"{rule_id}: Product/source mapping drift in {field_name}")


def load_career_source_mappings(
    repository_root: str | Path, registry: Mapping[str, Any]
) -> dict[str, Any]:
    """Validate disjoint, explicit mapping handoffs and return selected source rows."""
    additional = registry.get("additional_source_mappings", [])
    if not isinstance(additional, list):
        raise ValueError("Career additional_source_mappings must be a list")
    rules = registry.get("rules")
    if not isinstance(rules, Mapping):
        raise ValueError("Career rules must be an object")
    result = {}
    for meta in [registry.get("source_mapping"), *additional]:
        if not isinstance(meta, Mapping):
            raise ValueError("Career source mapping metadata must be an object")
        root = Path(repository_root).resolve()
        mapping_path = (root / str(meta.get("path", ""))).resolve()
        if not mapping_path.is_relative_to(root):
            raise ValueError("Career provider source mapping must remain inside repository root")
        mapping = _load_json(mapping_path)
        selected = meta.get("selected_rule_ids", mapping.get("scope", {}).get("nominated_source_rule_ids", []))
        if not isinstance(selected, list) or any(not isinstance(i, str) for i in selected):
            raise ValueError("Career selected_rule_ids must be a string list")
        if set(selected) & set(result):
            raise ValueError("Career source mapping selections must be disjoint")
        subregistry = dict(registry, source_mapping=meta,
                           rules={i: rules[i] for i in selected if i in rules})
        _validate_mapping_handoff(repository_root, subregistry)
        result.update({item["source_rule_id"]: item for item in mapping["mappings"]
                       if item["source_rule_id"] in selected})
    if set(result) != set(rules):
        raise ValueError("Career mappings must cover every Product rule exactly once")
    return result


def load_default_career_natal_provider(
    repository_root: str | Path,
) -> RegistryDrivenNatalDomainProvider:
    """Load the source-pinned Career NATAL provider."""

    root = Path(repository_root)
    registry_path = root / DEFAULT_CAREER_PROVIDER_REGISTRY_PATH
    registry = _load_json(registry_path)
    load_career_source_mappings(root, registry)
    return load_registry_driven_natal_provider(
        root,
        DEFAULT_CAREER_PROVIDER_REGISTRY_PATH,
    )
