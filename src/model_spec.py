"""Executable specification for Paper-1 Zi Wei latent-state architecture.

This module encodes structure only. It intentionally contains no empirical
weights, prediction probabilities, or claims of real-world validity.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Mapping, Optional, Sequence, Tuple


class EpistemicType(str, Enum):
    EXPLICIT = "EXPLICIT"
    INFERRED = "INFERRED"
    HYPOTHESIS = "HYPOTHESIS"
    IMPLEMENTATION = "IMPLEMENTATION"


class ModifierEffect(str, Enum):
    ENHANCE = "enhance"
    WEAKEN = "weaken"
    TRANSFORM = "transform"
    GATE = "gate"
    COUPLE = "couple"


class ObservationPathSupport(str, Enum):
    MULTI_PATH_SUPPORTED = "MULTI_PATH_SUPPORTED"
    SINGLE_PATH_SUPPORTED = "SINGLE_PATH_SUPPORTED"
    NO_DIRECT_PATH = "NO_DIRECT_PATH"
    DERIVED_ONLY = "DERIVED_ONLY"


@dataclass(frozen=True)
class StructuralSubstrate:
    yin_yang: Optional[str] = None
    element: Optional[str] = None
    relations: Tuple[str, ...] = ()


@dataclass(frozen=True)
class LatentComponent:
    dimension_id: str
    tendency: str
    strength_class: str
    evidence_rules: Tuple[str, ...] = ()


@dataclass(frozen=True)
class StarCore:
    star_id: str
    name: str
    substrate: StructuralSubstrate
    intrinsic: Tuple[LatentComponent, ...] = ()
    relational: Tuple[LatentComponent, ...] = ()
    contextual_sensitivity: str = "unknown"


@dataclass(frozen=True)
class StarSystemMode:
    system_no: int
    name: str
    mode_kind: str
    pole_a: str
    pole_b: str


@dataclass(frozen=True)
class ModifierOperator:
    modifier: str
    effect: ModifierEffect
    target_ids: Tuple[str, ...]
    source_status: EpistemicType
    context_required: bool = True


@dataclass(frozen=True)
class PalaceNode:
    palace_id: str
    name: str
    domain: str
    cross_dependencies: Tuple[str, ...] = ()


@dataclass
class NatalEssence:
    palace_id: str
    intrinsic_state: Dict[str, str] = field(default_factory=dict)
    relational_state: Dict[str, str] = field(default_factory=dict)
    active_modes: List[StarSystemMode] = field(default_factory=list)


@dataclass(frozen=True)
class TemporalInput:
    time_label: str
    astrological_layer: str
    active_systems: Tuple[str, ...] = ()
    transformations: Tuple[str, ...] = ()
    modifiers: Tuple[str, ...] = ()


@dataclass
class ReactionState:
    palace_id: str
    natal_essence: NatalEssence
    temporal_input: TemporalInput
    derived_state: Dict[str, str] = field(default_factory=dict)
    active_modes: List[StarSystemMode] = field(default_factory=list)


@dataclass(frozen=True)
class ProjectionResult:
    palace_id: str
    semantic_classes: Tuple[str, ...]
    provenance: Tuple[str, ...] = ()


@dataclass
class ModelGraph:
    palaces: Dict[str, PalaceNode]
    edges: Dict[str, Tuple[str, ...]]

    def neighbors(self, palace_id: str) -> Tuple[str, ...]:
        return self.edges.get(palace_id, ())


class Paper1Model:
    """Structure-preserving executable shell.

    The methods return symbolic objects rather than numeric predictions.
    """

    def __init__(self, graph: ModelGraph):
        self.graph = graph

    def build_natal_essence(
        self,
        palace_id: str,
        intrinsic_state: Mapping[str, str],
        relational_state: Mapping[str, str],
        active_modes: Sequence[StarSystemMode],
    ) -> NatalEssence:
        if palace_id not in self.graph.palaces:
            raise KeyError(f"Unknown palace: {palace_id}")
        return NatalEssence(
            palace_id=palace_id,
            intrinsic_state=dict(intrinsic_state),
            relational_state=dict(relational_state),
            active_modes=list(active_modes),
        )

    def react(
        self,
        essence: NatalEssence,
        temporal_input: TemporalInput,
        mode_updates: Sequence[StarSystemMode] = (),
    ) -> ReactionState:
        """Create a symbolic state-dependent reaction container.

        This intentionally does not implement numerical dynamics.
        """
        return ReactionState(
            palace_id=essence.palace_id,
            natal_essence=essence,
            temporal_input=temporal_input,
            derived_state={},
            active_modes=[*essence.active_modes, *mode_updates],
        )

    def project(
        self,
        reaction: ReactionState,
        semantic_classes: Sequence[str],
        provenance: Sequence[str] = (),
    ) -> ProjectionResult:
        return ProjectionResult(
            palace_id=reaction.palace_id,
            semantic_classes=tuple(semantic_classes),
            provenance=tuple(provenance),
        )


def classify_observation_path_support(
    independent_paths: int,
    coupled_only: bool = False,
    derived_from_existing: bool = False,
) -> ObservationPathSupport:
    """Heuristic source/output-path support audit.

    This is intentionally NOT a structural-observability test in the
    control-theoretic sense. It only records how many independent
    source-to-output paths are currently represented in the symbolic model.
    """
    if derived_from_existing:
        return ObservationPathSupport.DERIVED_ONLY
    if independent_paths <= 0:
        return ObservationPathSupport.NO_DIRECT_PATH
    if independent_paths == 1 or coupled_only:
        return ObservationPathSupport.SINGLE_PATH_SUPPORTED
    return ObservationPathSupport.MULTI_PATH_SUPPORTED


def classify_observability(*args, **kwargs):
    """Deprecated compatibility alias.

    Kept temporarily so historical callers fail softly during A1 migration.
    New code must use classify_observation_path_support().
    """
    return classify_observation_path_support(*args, **kwargs)
