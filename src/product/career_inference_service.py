"""Product entry point for canonical Career NATAL + selected temporal context."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable, Mapping, Any

from .canonical_chart_contract import validate_canonical_production_chart_snapshot
from .career_natal_domain_provider import load_default_career_natal_provider
from .event_relative_window import (
    MIGRATION_WINDOW_ID,
    MigrationFirstThreeYearsInput,
    resolve_migration_first_three_years,
)
from .full_chart_snapshot_contract import validate_normalized_full_chart_snapshot
from .natal_domain_registry import load_default_natal_domain_registry
from .symbolic_inference_pipeline import SymbolicInferenceRun, run_symbolic_inference
from .temporal_environment import EventRelativeContextEvidence


DEFAULT_TEMPORAL_REACTION_REGISTRY_PATH = (
    "product/PL3T_TEMPORAL_REACTION_REGISTRY_v0.1.json"
)
DEFAULT_CAREER_TEMPORAL_LAYERS = ("DECADE", "YEAR")


def run_career_inference(
    repository_root: str | Path,
    normalized_snapshot: Mapping[str, Any],
    *,
    target_id: str,
    question: str,
    selected_temporal_layers: Iterable[str] = DEFAULT_CAREER_TEMPORAL_LAYERS,
    temporal_conflicts: Iterable[str] = (),
    event_relative_context: Iterable[EventRelativeContextEvidence] = (),
    migration_window: MigrationFirstThreeYearsInput | None = None,
) -> SymbolicInferenceRun:
    """Run the canonical Career provider with explicitly selected time layers.

    This wrapper intentionally uses the production temporal registry and never
    substitutes a test fixture. If no canonical temporal reactions are present,
    the underlying pipeline returns an explicit partial result.
    """

    validation = validate_normalized_full_chart_snapshot(
        normalized_snapshot,
        target_id=target_id,
    )
    if not validation.ok:
        raise ValueError(
            "invalid normalized full-chart snapshot: "
            + "; ".join(validation.errors)
        )

    canonical_validation = validate_canonical_production_chart_snapshot(
        normalized_snapshot
    )
    if not canonical_validation.ok:
        raise ValueError(
            "non-canonical production chart snapshot: "
            + "; ".join(canonical_validation.errors)
        )

    root = Path(repository_root)
    career_provider = load_default_career_natal_provider(root)
    domain_registry = load_default_natal_domain_registry(
        root,
        additional_providers=(career_provider,),
    )

    reaction_path = root / DEFAULT_TEMPORAL_REACTION_REGISTRY_PATH
    with reaction_path.open("r", encoding="utf-8") as handle:
        reaction_registry = json.load(handle)
    if not isinstance(reaction_registry, Mapping):
        raise ValueError("production temporal reaction registry must be a JSON object")

    relative_context_items = list(event_relative_context)
    if migration_window is not None:
        if any(item.context_id == MIGRATION_WINDOW_ID for item in relative_context_items):
            raise ValueError(
                f"event_relative_context already contains {MIGRATION_WINDOW_ID}"
            )
        resolution = resolve_migration_first_three_years(migration_window)
        relative_context_items.append(resolution.evidence)

    return run_symbolic_inference(
        normalized_snapshot,
        target_id=target_id,
        question=question,
        domain_registry=domain_registry,
        reaction_registry_document=reaction_registry,
        selected_domains=("career",),
        selected_temporal_layers=selected_temporal_layers,
        temporal_conflicts=temporal_conflicts,
        event_relative_context=tuple(relative_context_items),
    )
