"""Product Knowledge candidate impact and promotion gate v0.1.

Implements Proposal #491 Phase 3.

The module never mutates the active Product Knowledge lock. It only:
- constructs an explicit candidate KIB from an accepted active bundle;
- compares active and candidate semantics deterministically;
- propagates bounded downstream invalidation;
- evaluates whether supplied validation evidence is sufficient for promotion.

Knowledge main is not treated as an implicit active Product dependency.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping, Sequence

from .knowledge_bundle import (
    KnowledgeLockError,
    SUPPORTED_COMPONENTS,
    compute_artifact_digest,
    compute_bundle_semantic_digest,
    compute_component_semantic_digest,
    compute_semantic_digest,
    validate_bundle_structure,
)


IMPACT_CLASSES = (
    "NO_RUNTIME_EFFECT",
    "PROVENANCE_REVALIDATION",
    "READINESS_REBUILD",
    "SYMBOLIC_RECOMPILE",
    "METHOD_REPLAY",
    "MANIFESTATION_REBUILD",
    "DATASET_REMATERIALIZE",
    "RETRAIN_OR_RECALIBRATE",
    "MIGRATION_REQUIRED",
)

DIRECT_SEMANTIC_ACTION = {
    "K_signal": "SYMBOLIC_RECOMPILE",
    "K_response": "READINESS_REBUILD",
    "K_manifest": "MANIFESTATION_REBUILD",
    "K_method": "METHOD_REPLAY",
}

DEPENDENCY_PROPAGATION = {
    "K_signal": (
        ("NATAL_ESSENCE", "SYMBOLIC_RECOMPILE", "DIRECT"),
        ("RESPONSE_PROFILE_TAU", "SYMBOLIC_RECOMPILE", "IF_PRESENT"),
        ("MANIFESTATION_M0", "MANIFESTATION_REBUILD", "IF_PRESENT"),
        ("EMPIRICAL_DATASET", "DATASET_REMATERIALIZE", "IF_PRESENT"),
        ("CALIBRATED_MODEL", "RETRAIN_OR_RECALIBRATE", "IF_PRESENT"),
    ),
    "K_response": (
        ("RESPONSE_READINESS", "READINESS_REBUILD", "DIRECT"),
        ("RESPONSE_PROFILE_TAU", "SYMBOLIC_RECOMPILE", "IF_PRESENT"),
        ("MANIFESTATION_M0", "MANIFESTATION_REBUILD", "IF_PRESENT"),
        ("EMPIRICAL_DATASET", "DATASET_REMATERIALIZE", "IF_PRESENT"),
        ("CALIBRATED_MODEL", "RETRAIN_OR_RECALIBRATE", "IF_PRESENT"),
    ),
    "K_manifest": (
        ("MANIFESTATION_M0", "MANIFESTATION_REBUILD", "DIRECT"),
        ("EMPIRICAL_DATASET", "DATASET_REMATERIALIZE", "IF_PRESENT"),
        ("CALIBRATED_MODEL", "RETRAIN_OR_RECALIBRATE", "IF_PRESENT"),
    ),
    "K_method": (
        ("METHOD_POLICY_PI", "METHOD_REPLAY", "DIRECT"),
        ("EXPERT_METHOD_REPLAY", "METHOD_REPLAY", "IF_PRESENT"),
    ),
}

VALIDATION_BY_ACTION = {
    "NO_RUNTIME_EFFECT": (),
    "PROVENANCE_REVALIDATION": ("LOCK_REVERIFY",),
    "READINESS_REBUILD": ("READINESS_REGRESSION",),
    "SYMBOLIC_RECOMPILE": ("CANONICAL_FIDELITY_REGRESSION",),
    "METHOD_REPLAY": ("METHOD_REPLAY_REGRESSION",),
    "MANIFESTATION_REBUILD": ("MANIFESTATION_FIDELITY_REGRESSION",),
    "DATASET_REMATERIALIZE": ("DATASET_LINEAGE_VALIDATION",),
    "RETRAIN_OR_RECALIBRATE": ("MODEL_VALIDATION",),
    "MIGRATION_REQUIRED": (),
}


class KnowledgeImpactError(ValueError):
    """Raised when candidate construction or impact comparison is unsafe."""


def _artifact_map(component: Mapping[str, Any]) -> dict[str, Mapping[str, Any]]:
    return {
        str(item["path"]): item
        for item in component.get("artifacts", ())
    }


def _component_map(bundle: Mapping[str, Any]) -> dict[str, Mapping[str, Any]]:
    return {
        str(item["component_id"]): item
        for item in bundle.get("components", ())
    }


def _artifact_type_for(path: str) -> str:
    suffix = Path(path).suffix.lower()
    if suffix == ".json":
        return "JSON"
    if suffix in {".csv", ".tsv", ".txt", ".md", ".yaml", ".yml"}:
        return "TEXT"
    return "BINARY"


def _candidate_artifact_spec(
    active_artifacts: Mapping[str, Mapping[str, Any]],
    spec: Mapping[str, Any],
) -> dict[str, Any]:
    path = str(spec.get("path", "")).strip()
    if not path:
        raise KnowledgeImpactError("candidate artifact path is required")

    active = active_artifacts.get(path)
    contract = str(spec.get("semantic_contract") or "").strip()
    if not contract:
        if active is None:
            raise KnowledgeImpactError(
                f"{path}: new candidate artifact requires explicit semantic_contract"
            )
        contract = str(active["semantic_contract"])

    artifact_type = str(
        spec.get("artifact_type")
        or (active or {}).get("artifact_type")
        or _artifact_type_for(path)
    )
    return {
        "path": path,
        "artifact_type": artifact_type,
        "semantic_contract": contract,
    }


def build_candidate_bundle(
    repository_root: str | Path,
    active_bundle: Mapping[str, Any],
    *,
    bundle_id: str,
    source_commit: str,
    component_overrides: Mapping[str, Mapping[str, Any]] | None = None,
) -> dict[str, Any]:
    """Build an explicit candidate bundle from current repository bytes.

    Unchanged components reuse the active artifact inventory. A caller may
    replace a component inventory explicitly through component_overrides.
    New artifact paths must provide an explicit semantic contract.

    The function is pure with respect to Product state: it never writes or
    promotes PRODUCT_KNOWLEDGE.lock.json.
    """

    root = Path(repository_root).resolve()
    try:
        validate_bundle_structure(active_bundle)
    except KnowledgeLockError as exc:
        raise KnowledgeImpactError(
            f"active bundle is invalid and cannot seed a candidate: {exc}"
        ) from exc

    candidate_id = str(bundle_id).strip()
    candidate_commit = str(source_commit).strip()
    if not candidate_id:
        raise KnowledgeImpactError("candidate bundle_id is required")
    if not candidate_commit:
        raise KnowledgeImpactError("candidate source_commit is required")

    overrides = dict(component_overrides or {})
    unknown = set(overrides) - SUPPORTED_COMPONENTS
    if unknown:
        raise KnowledgeImpactError(
            f"unknown candidate component override(s): {sorted(unknown)}"
        )

    active_components = _component_map(active_bundle)
    candidate_components: list[dict[str, Any]] = []

    for component_id in sorted(SUPPORTED_COMPONENTS):
        active_component = active_components[component_id]
        override = overrides.get(component_id, {})
        active_artifacts = _artifact_map(active_component)

        if "artifacts" in override:
            raw_specs = override["artifacts"]
            if not isinstance(raw_specs, Sequence) or isinstance(
                raw_specs, (str, bytes)
            ):
                raise KnowledgeImpactError(
                    f"{component_id}.artifacts override must be an array"
                )
            specs = [
                _candidate_artifact_spec(active_artifacts, item)
                for item in raw_specs
            ]
        else:
            specs = [
                {
                    "path": str(item["path"]),
                    "artifact_type": str(
                        item.get("artifact_type")
                        or _artifact_type_for(str(item["path"]))
                    ),
                    "semantic_contract": str(item["semantic_contract"]),
                }
                for item in active_component["artifacts"]
            ]

        seen_paths: set[str] = set()
        artifacts: list[dict[str, Any]] = []
        for spec in specs:
            relative = str(spec["path"])
            if relative in seen_paths:
                raise KnowledgeImpactError(
                    f"{component_id}: duplicate candidate artifact {relative}"
                )
            seen_paths.add(relative)
            path = (root / relative).resolve()
            if not path.is_relative_to(root):
                raise KnowledgeImpactError(
                    f"{component_id}: artifact path escapes repository: {relative}"
                )
            if not path.is_file():
                raise KnowledgeImpactError(
                    f"{component_id}: candidate artifact is missing: {relative}"
                )
            contract = str(spec["semantic_contract"])
            try:
                semantic_digest = compute_semantic_digest(path, contract)
            except KnowledgeLockError as exc:
                raise KnowledgeImpactError(
                    f"{component_id}.{relative}: {exc}"
                ) from exc
            artifacts.append(
                {
                    "path": relative,
                    "artifact_type": str(spec["artifact_type"]),
                    "artifact_digest": compute_artifact_digest(path),
                    "semantic_contract": contract,
                    "semantic_digest": semantic_digest,
                }
            )

        artifacts.sort(key=lambda item: item["path"])
        candidate_component = {
            "component_id": component_id,
            "contract_version": str(
                override.get(
                    "contract_version",
                    active_component["contract_version"],
                )
            ),
            "coverage_status": str(
                override.get(
                    "coverage_status",
                    active_component["coverage_status"],
                )
            ),
            "source_commit": candidate_commit,
            "artifacts": artifacts,
            "component_semantic_digest": compute_component_semantic_digest(
                artifacts
            ),
        }
        candidate_components.append(candidate_component)

    bundle = {
        "schema_version": "0.1",
        "bundle_id": candidate_id,
        "source_commit": candidate_commit,
        "status": "CANDIDATE",
        "candidate_from_bundle_id": str(active_bundle["bundle_id"]),
        "auto_refresh": False,
        "components": candidate_components,
        "bundle_semantic_digest": compute_bundle_semantic_digest(
            candidate_components
        ),
    }
    validate_bundle_structure(bundle)
    return bundle


def _invalid_candidate_report(
    active_bundle: Mapping[str, Any],
    candidate_bundle: Mapping[str, Any],
    reason: str,
) -> dict[str, Any]:
    return {
        "schema_version": "0.1",
        "status": "BLOCKED",
        "active_bundle_id": str(active_bundle.get("bundle_id", "")),
        "candidate_bundle_id": str(candidate_bundle.get("bundle_id", "")),
        "overall_impact": "MIGRATION_REQUIRED",
        "component_impacts": [],
        "direct_actions": ["MIGRATION_REQUIRED"],
        "downstream_invalidations": [],
        "blockers": [reason],
    }


def compare_bundles(
    active_bundle: Mapping[str, Any],
    candidate_bundle: Mapping[str, Any],
) -> dict[str, Any]:
    """Compare active and candidate KIBs without using source_commit as semantics."""

    try:
        validate_bundle_structure(active_bundle)
    except KnowledgeLockError as exc:
        raise KnowledgeImpactError(f"active bundle invalid: {exc}") from exc

    try:
        validate_bundle_structure(candidate_bundle)
    except KnowledgeLockError as exc:
        return _invalid_candidate_report(
            active_bundle,
            candidate_bundle,
            f"CANDIDATE_BUNDLE_INVALID: {exc}",
        )

    active_components = _component_map(active_bundle)
    candidate_components = _component_map(candidate_bundle)
    component_impacts: list[dict[str, Any]] = []
    direct_actions: set[str] = set()
    downstream: dict[tuple[str, str], dict[str, str]] = {}
    blockers: list[str] = []

    for component_id in sorted(SUPPORTED_COMPONENTS):
        active = active_components[component_id]
        candidate = candidate_components[component_id]
        active_artifacts = _artifact_map(active)
        candidate_artifacts = _artifact_map(candidate)

        contract_changed = (
            str(active["contract_version"])
            != str(candidate["contract_version"])
        )
        coverage_changed = (
            str(active["coverage_status"])
            != str(candidate["coverage_status"])
        )

        artifact_deltas: list[dict[str, Any]] = []
        semantic_changed = coverage_changed
        exact_changed = False
        migration_required = contract_changed

        for path in sorted(set(active_artifacts) | set(candidate_artifacts)):
            before = active_artifacts.get(path)
            after = candidate_artifacts.get(path)
            if before is None:
                semantic_changed = True
                exact_changed = True
                artifact_deltas.append(
                    {
                        "path": path,
                        "change_type": "ADDED",
                        "artifact_digest_before": None,
                        "artifact_digest_after": after["artifact_digest"],
                        "semantic_digest_before": None,
                        "semantic_digest_after": after["semantic_digest"],
                    }
                )
                continue
            if after is None:
                semantic_changed = True
                exact_changed = True
                artifact_deltas.append(
                    {
                        "path": path,
                        "change_type": "REMOVED",
                        "artifact_digest_before": before["artifact_digest"],
                        "artifact_digest_after": None,
                        "semantic_digest_before": before["semantic_digest"],
                        "semantic_digest_after": None,
                    }
                )
                continue

            semantic_contract_changed = (
                str(before["semantic_contract"])
                != str(after["semantic_contract"])
            )
            artifact_type_changed = (
                str(before.get("artifact_type", ""))
                != str(after.get("artifact_type", ""))
            )
            if semantic_contract_changed or artifact_type_changed:
                migration_required = True

            same_exact = (
                str(before["artifact_digest"])
                == str(after["artifact_digest"])
            )
            same_semantic = (
                str(before["semantic_digest"])
                == str(after["semantic_digest"])
            )

            if not same_exact:
                exact_changed = True
            if not same_semantic:
                semantic_changed = True

            if (
                semantic_contract_changed
                or artifact_type_changed
                or not same_exact
                or not same_semantic
            ):
                if semantic_contract_changed or artifact_type_changed:
                    change_type = "CONTRACT"
                elif not same_semantic:
                    change_type = "SEMANTIC"
                else:
                    change_type = "EXACT_ONLY"
                artifact_deltas.append(
                    {
                        "path": path,
                        "change_type": change_type,
                        "artifact_digest_before": before["artifact_digest"],
                        "artifact_digest_after": after["artifact_digest"],
                        "semantic_digest_before": before["semantic_digest"],
                        "semantic_digest_after": after["semantic_digest"],
                        "semantic_contract_before": before["semantic_contract"],
                        "semantic_contract_after": after["semantic_contract"],
                    }
                )

        if migration_required:
            primary_action = "MIGRATION_REQUIRED"
            blockers.append(f"{component_id}: incompatible contract change")
        elif semantic_changed:
            primary_action = DIRECT_SEMANTIC_ACTION[component_id]
        elif exact_changed:
            primary_action = "PROVENANCE_REVALIDATION"
        else:
            primary_action = "NO_RUNTIME_EFFECT"

        direct_actions.add(primary_action)

        if primary_action in {
            "READINESS_REBUILD",
            "SYMBOLIC_RECOMPILE",
            "METHOD_REPLAY",
            "MANIFESTATION_REBUILD",
        }:
            for artifact, action, applicability in DEPENDENCY_PROPAGATION[
                component_id
            ]:
                downstream[(artifact, action)] = {
                    "artifact": artifact,
                    "action": action,
                    "applicability": applicability,
                    "trigger_component": component_id,
                }

        component_impacts.append(
            {
                "component_id": component_id,
                "primary_action": primary_action,
                "contract_changed": contract_changed,
                "coverage_changed": coverage_changed,
                "artifact_set_changed": set(active_artifacts)
                != set(candidate_artifacts),
                "exact_changed": exact_changed,
                "semantic_changed": semantic_changed,
                "artifact_deltas": artifact_deltas,
            }
        )

    if "MIGRATION_REQUIRED" in direct_actions:
        overall = "MIGRATION_REQUIRED"
        status = "BLOCKED"
    elif direct_actions == {"NO_RUNTIME_EFFECT"}:
        overall = "NO_RUNTIME_EFFECT"
        status = "READY_FOR_VALIDATION"
    else:
        precedence = [
            "RETRAIN_OR_RECALIBRATE",
            "DATASET_REMATERIALIZE",
            "MANIFESTATION_REBUILD",
            "METHOD_REPLAY",
            "SYMBOLIC_RECOMPILE",
            "READINESS_REBUILD",
            "PROVENANCE_REVALIDATION",
            "NO_RUNTIME_EFFECT",
        ]
        overall = next(
            action for action in precedence if action in direct_actions
        )
        status = "READY_FOR_VALIDATION"

    return {
        "schema_version": "0.1",
        "status": status,
        "active_bundle_id": str(active_bundle["bundle_id"]),
        "candidate_bundle_id": str(candidate_bundle["bundle_id"]),
        "active_source_commit": str(active_bundle["source_commit"]),
        "candidate_source_commit": str(candidate_bundle["source_commit"]),
        "source_commit_changed": str(active_bundle["source_commit"])
        != str(candidate_bundle["source_commit"]),
        "overall_impact": overall,
        "component_impacts": component_impacts,
        "direct_actions": sorted(direct_actions),
        "downstream_invalidations": sorted(
            downstream.values(),
            key=lambda item: (item["artifact"], item["action"]),
        ),
        "blockers": blockers,
    }


def required_validations(impact_report: Mapping[str, Any]) -> list[str]:
    gates: set[str] = set()
    for action in impact_report.get("direct_actions", ()):
        for gate in VALIDATION_BY_ACTION.get(str(action), ()):
            gates.add(gate)
    return sorted(gates)


def evaluate_promotion_gate(
    impact_report: Mapping[str, Any],
    *,
    candidate_verification: Mapping[str, Any],
    validation_results: Mapping[str, str] | None = None,
) -> dict[str, Any]:
    """Return PROMOTABLE/BLOCKED; never mutate the active Product lock."""

    validations = {
        str(key): str(value).upper()
        for key, value in (validation_results or {}).items()
    }
    required = required_validations(impact_report)
    missing = [
        gate for gate in required if validations.get(gate) != "PASS"
    ]
    blockers = list(impact_report.get("blockers", ()))

    if str(candidate_verification.get("status", "")) != "PASS":
        blockers.append("CANDIDATE_BUNDLE_VERIFICATION_FAILED")
    if "MIGRATION_REQUIRED" in impact_report.get("direct_actions", ()):
        blockers.append("MIGRATION_REQUIRED")
    for gate in missing:
        blockers.append(f"VALIDATION_REQUIRED:{gate}")

    status = "PROMOTABLE" if not blockers else "BLOCKED"
    recommendation = (
        "SKIP_NO_RUNTIME_EFFECT"
        if status == "PROMOTABLE"
        and impact_report.get("overall_impact") == "NO_RUNTIME_EFFECT"
        else (
            "EXPLICIT_LOCK_PROMOTION_ALLOWED"
            if status == "PROMOTABLE"
            else "DO_NOT_PROMOTE"
        )
    )

    return {
        "schema_version": "0.1",
        "status": status,
        "recommendation": recommendation,
        "candidate_bundle_id": impact_report.get("candidate_bundle_id"),
        "required_validations": required,
        "supplied_validation_results": validations,
        "blockers": sorted(set(blockers)),
        "active_lock_mutated": False,
    }
