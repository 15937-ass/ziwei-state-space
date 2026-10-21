"""Product entry point for canonical Career NATAL + selected temporal context."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Mapping, Any

from .career_natal_domain_provider import load_default_career_natal_provider
from .event_relative_window import (
    MIGRATION_WINDOW_ID,
    MigrationFirstThreeYearsInput,
    resolve_migration_first_three_years,
)
from .full_chart_snapshot_contract import validate_normalized_full_chart_snapshot
from .natal_domain_registry import load_default_natal_domain_registry
from .palace_structure import load_palace_ontology
from .response_condition_evaluator import evaluate_career_conditions
from .response_profile import ResponseProfile, compile_decade_year_response_profile
from .symbolic_inference_pipeline import SymbolicInferenceRun, run_symbolic_inference
from .temporal_environment import EventRelativeContextEvidence


DEFAULT_TEMPORAL_REACTION_REGISTRY_PATH = (
    "product/PL3T_TEMPORAL_REACTION_REGISTRY_v0.1.json"
)
DEFAULT_CAREER_TEMPORAL_LAYERS = ("DECADE", "YEAR")
DEFAULT_CAREER_PALACE_ONTOLOGY_PATH = "knowledge/wp05/palace_ontology_v0.1.csv"


@dataclass(frozen=True)
class CareerResponseRun:
    """One deterministic Career N -> E -> tau execution bundle."""

    schema_version: str
    symbolic_run: SymbolicInferenceRun
    natal_condition_evaluation: Mapping[str, Any]
    response_profile: ResponseProfile

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "symbolic_run": self.symbolic_run.to_dict(),
            "natal_condition_evaluation": dict(self.natal_condition_evaluation),
            "response_profile": self.response_profile.to_dict(),
        }


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



def run_career_response_profile(
    repository_root: str | Path,
    normalized_snapshot: Mapping[str, Any],
    *,
    target_id: str,
    question: str,
    selected_temporal_layers: Iterable[str] = DEFAULT_CAREER_TEMPORAL_LAYERS,
    temporal_conflicts: Iterable[str] = (),
    event_relative_context: Iterable[EventRelativeContextEvidence] = (),
    migration_window: MigrationFirstThreeYearsInput | None = None,
) -> CareerResponseRun:
    """Run the first production-shaped Career N -> E -> tau vertical slice.

    The underlying symbolic service remains the source for N and E_t. The
    governed 12-condition evaluator supplies NATAL response semantics, and the
    v0.1 ResponseProfile compiler then combines those with DECADE + YEAR E_t.

    With the current active temporal Kr gate, tau is intentionally UNKNOWN
    rather than populated with an invented dynamic response.
    """

    root = Path(repository_root)
    symbolic = run_career_inference(
        root,
        normalized_snapshot,
        target_id=target_id,
        question=question,
        selected_temporal_layers=selected_temporal_layers,
        temporal_conflicts=temporal_conflicts,
        event_relative_context=event_relative_context,
        migration_window=migration_window,
    )
    ontology = load_palace_ontology(root / DEFAULT_CAREER_PALACE_ONTOLOGY_PATH)
    natal_evaluation = evaluate_career_conditions(
        normalized_snapshot,
        ontology,
    )
    response_profile = compile_decade_year_response_profile(
        symbolic.natal_profile,
        natal_evaluation,
        symbolic.temporal_profile,
        repository_root=root,
    )
    return CareerResponseRun(
        schema_version="0.1",
        symbolic_run=symbolic,
        natal_condition_evaluation=natal_evaluation,
        response_profile=response_profile,
    )
