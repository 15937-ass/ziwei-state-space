"""PL3-M empirical manifestation probability interface v0.1.

This layer attaches a calibrated *population/cohort empirical* probability to a
source-supported manifestation possibility.  It deliberately does not implement
or store canonical traditional probabilities, and it is separate from a
personalized posterior.
"""

from __future__ import annotations

import math
from dataclasses import asdict, dataclass
from typing import Any, Mapping, Protocol, Sequence

from .manifestation_context import ManifestationRoutingContext
from .manifestation_router import SourceSupportedPossibility


PROBABILITY_REGISTRY_STATUSES = frozenset(
    {
        "EMPTY_PENDING_PL5_CALIBRATION",
        "TEST_ONLY",
        "CALIBRATED_READY",
    }
)

PROBABILITY_MODEL_STATUSES = frozenset({"TEST_ONLY", "CALIBRATED"})
EMPIRICAL_PARAMETER_LAYERS = frozenset(
    {"EMPIRICAL_POPULATION", "EMPIRICAL_COHORT", "TEST_FIXTURE"}
)

PROBABILITY_RESULT_STATUSES = frozenset(
    {
        "ESTIMATED",
        "NOT_CALIBRATED",
        "MODEL_NOT_AVAILABLE",
        "PLUGIN_NOT_AVAILABLE",
        "PLUGIN_ABSTAIN",
        "ABSTAIN_CONTEXT_MODE",
        "ABSTAIN_CONTEXT_QUALITY",
    }
)


def _required_text(value: Any, field: str) -> str:
    text = str(value or "").strip()
    if not text:
        raise ValueError(f"{field} is required")
    return text


def _optional_text(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _text_tuple(
    value: Any,
    field: str,
    *,
    allow_empty: bool = False,
) -> tuple[str, ...]:
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes)):
        raise ValueError(f"{field} must be an array")
    out = tuple(sorted({str(item).strip() for item in value if str(item).strip()}))
    if not allow_empty and not out:
        raise ValueError(f"{field} cannot be empty")
    return out


def _probability(value: Any, field: str) -> float:
    if isinstance(value, bool):
        raise ValueError(f"{field} must be numeric")
    try:
        number = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{field} must be numeric") from exc
    if not math.isfinite(number) or not (0.0 <= number <= 1.0):
        raise ValueError(f"{field} must be finite in [0,1]")
    return number


@dataclass(frozen=True)
class ProbabilityModelDescriptor:
    model_id: str
    model_version: str
    manifestation_id: str
    target_ontology_version: str
    predictor_family: str
    parameter_layer: str
    model_status: str
    calibration_dataset_version: str | None
    calibration_metrics_ref: str | None
    allowed_context_modes: tuple[str, ...]
    requires_personal_context: bool

    def __post_init__(self) -> None:
        if self.parameter_layer not in EMPIRICAL_PARAMETER_LAYERS:
            raise ValueError(
                f"unsupported empirical parameter layer: {self.parameter_layer}"
            )
        if self.model_status not in PROBABILITY_MODEL_STATUSES:
            raise ValueError(
                f"unsupported probability model status: {self.model_status}"
            )
        invalid_modes = sorted(
            set(self.allowed_context_modes) - {"BLIND", "PERSONALIZED"}
        )
        if invalid_modes:
            raise ValueError(
                "unsupported allowed_context_modes: " + ", ".join(invalid_modes)
            )
        if not self.allowed_context_modes:
            raise ValueError("allowed_context_modes cannot be empty")

        if self.model_status == "CALIBRATED":
            if self.parameter_layer == "TEST_FIXTURE":
                raise ValueError(
                    "CALIBRATED model cannot use TEST_FIXTURE parameter layer"
                )
            if not self.calibration_dataset_version:
                raise ValueError(
                    "CALIBRATED model requires calibration_dataset_version"
                )
            if not self.calibration_metrics_ref:
                raise ValueError(
                    "CALIBRATED model requires calibration_metrics_ref"
                )
        elif self.parameter_layer != "TEST_FIXTURE":
            raise ValueError(
                "TEST_ONLY probability model must use TEST_FIXTURE parameter layer"
            )


@dataclass(frozen=True)
class ProbabilityModelRegistry:
    schema_version: str
    registry_status: str
    registry_version: str | None
    models: tuple[ProbabilityModelDescriptor, ...]
    blocked_reason: str | None = None

    def __post_init__(self) -> None:
        if self.schema_version != "0.1":
            raise ValueError("ProbabilityModelRegistry schema_version must be 0.1")
        if self.registry_status not in PROBABILITY_REGISTRY_STATUSES:
            raise ValueError(
                f"unsupported probability registry status: {self.registry_status}"
            )
        if self.registry_status == "EMPTY_PENDING_PL5_CALIBRATION":
            if self.models:
                raise ValueError(
                    "EMPTY_PENDING_PL5_CALIBRATION registry must contain zero models"
                )
            if self.registry_version is not None:
                raise ValueError(
                    "pending probability registry cannot claim registry_version"
                )
        elif self.registry_status == "CALIBRATED_READY":
            if not self.models:
                raise ValueError("CALIBRATED_READY registry requires models")
            if not self.registry_version:
                raise ValueError(
                    "CALIBRATED_READY registry requires registry_version"
                )
            if any(item.model_status != "CALIBRATED" for item in self.models):
                raise ValueError(
                    "CALIBRATED_READY registry can contain CALIBRATED models only"
                )
        elif self.registry_status == "TEST_ONLY":
            if any(item.model_status != "TEST_ONLY" for item in self.models):
                raise ValueError(
                    "TEST_ONLY registry can contain TEST_ONLY models only"
                )

        targets = [item.manifestation_id for item in self.models]
        if len(targets) != len(set(targets)):
            raise ValueError(
                "v0.1 probability registry allows only one model per manifestation_id; "
                "cohort/model selection requires a later explicit selector contract"
            )

    def by_manifestation(self) -> dict[str, ProbabilityModelDescriptor]:
        return {item.manifestation_id: item for item in self.models}


class PopulationProbabilityPlugin(Protocol):
    """External calibrated model adapter. Implementations arrive in PL5."""

    def predict(
        self,
        model: ProbabilityModelDescriptor,
        context: ManifestationRoutingContext,
        possibility: SourceSupportedPossibility,
    ) -> float | None:
        ...


@dataclass(frozen=True)
class EmpiricalProbabilityResult:
    schema_version: str
    namespace: str
    status: str
    manifestation_id: str
    source_possibility_mapping_id: str
    context_id: str
    probability: float | None
    model_id: str | None
    model_version: str | None
    predictor_family: str | None
    parameter_layer: str | None
    calibration_dataset_version: str | None
    calibration_metrics_ref: str | None
    is_personalized_posterior: bool = False

    def __post_init__(self) -> None:
        if self.schema_version != "0.1":
            raise ValueError("EmpiricalProbabilityResult schema_version must be 0.1")
        if self.namespace != "EMPIRICALLY_CALIBRATED_PROBABILITY":
            raise ValueError(
                "population/cohort probability must use "
                "EMPIRICALLY_CALIBRATED_PROBABILITY namespace"
            )
        if self.status not in PROBABILITY_RESULT_STATUSES:
            raise ValueError(f"unsupported probability result status: {self.status}")
        if self.is_personalized_posterior:
            raise ValueError(
                "EmpiricalProbabilityResult cannot masquerade as personalized posterior"
            )
        if self.status == "ESTIMATED":
            if self.probability is None:
                raise ValueError("ESTIMATED result requires probability")
            _probability(self.probability, "probability")
            if not self.model_id or not self.model_version:
                raise ValueError("ESTIMATED result requires model identity")
            if self.parameter_layer not in {
                "EMPIRICAL_POPULATION",
                "EMPIRICAL_COHORT",
                "TEST_FIXTURE",
            }:
                raise ValueError("ESTIMATED result requires empirical parameter layer")
        elif self.probability is not None:
            raise ValueError(
                f"{self.status} result must keep probability=null"
            )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def compile_probability_model_registry(
    payload: Mapping[str, Any],
) -> ProbabilityModelRegistry:
    if str(payload.get("schema_version", "")).strip() != "0.1":
        raise ValueError("probability model registry schema_version must be 0.1")

    registry_status = _required_text(
        payload.get("registry_status"), "registry_status"
    )
    if registry_status not in PROBABILITY_REGISTRY_STATUSES:
        raise ValueError(
            f"unsupported probability registry status: {registry_status}"
        )

    raw_models = payload.get("models")
    if not isinstance(raw_models, Sequence) or isinstance(
        raw_models, (str, bytes)
    ):
        raise ValueError("probability model registry models must be an array")

    models: list[ProbabilityModelDescriptor] = []
    seen_ids: set[str] = set()
    for index, row in enumerate(raw_models):
        if not isinstance(row, Mapping):
            raise ValueError(f"models[{index}] must be an object")

        model_id = _required_text(
            row.get("model_id"), f"models[{index}].model_id"
        )
        if model_id in seen_ids:
            raise ValueError(f"duplicate probability model_id: {model_id}")
        seen_ids.add(model_id)

        models.append(
            ProbabilityModelDescriptor(
                model_id=model_id,
                model_version=_required_text(
                    row.get("model_version"), f"{model_id}.model_version"
                ),
                manifestation_id=_required_text(
                    row.get("manifestation_id"),
                    f"{model_id}.manifestation_id",
                ),
                target_ontology_version=_required_text(
                    row.get("target_ontology_version"),
                    f"{model_id}.target_ontology_version",
                ),
                predictor_family=_required_text(
                    row.get("predictor_family"),
                    f"{model_id}.predictor_family",
                ),
                parameter_layer=_required_text(
                    row.get("parameter_layer"),
                    f"{model_id}.parameter_layer",
                ),
                model_status=_required_text(
                    row.get("model_status"), f"{model_id}.model_status"
                ),
                calibration_dataset_version=_optional_text(
                    row.get("calibration_dataset_version")
                ),
                calibration_metrics_ref=_optional_text(
                    row.get("calibration_metrics_ref")
                ),
                allowed_context_modes=_text_tuple(
                    row.get("allowed_context_modes"),
                    f"{model_id}.allowed_context_modes",
                ),
                requires_personal_context=bool(
                    row.get("requires_personal_context", False)
                ),
            )
        )

    return ProbabilityModelRegistry(
        schema_version="0.1",
        registry_status=registry_status,
        registry_version=_optional_text(payload.get("registry_version")),
        blocked_reason=_optional_text(payload.get("blocked_reason")),
        models=tuple(sorted(models, key=lambda item: item.model_id)),
    )


def _empty_result(
    *,
    status: str,
    possibility: SourceSupportedPossibility,
    context: ManifestationRoutingContext,
    model: ProbabilityModelDescriptor | None = None,
) -> EmpiricalProbabilityResult:
    return EmpiricalProbabilityResult(
        schema_version="0.1",
        namespace="EMPIRICALLY_CALIBRATED_PROBABILITY",
        status=status,
        manifestation_id=possibility.manifestation_id,
        source_possibility_mapping_id=possibility.mapping_id,
        context_id=context.context_id,
        probability=None,
        model_id=model.model_id if model else None,
        model_version=model.model_version if model else None,
        predictor_family=model.predictor_family if model else None,
        parameter_layer=model.parameter_layer if model else None,
        calibration_dataset_version=(
            model.calibration_dataset_version if model else None
        ),
        calibration_metrics_ref=model.calibration_metrics_ref if model else None,
    )


def evaluate_empirical_manifestation_probability(
    possibility: SourceSupportedPossibility,
    context: ManifestationRoutingContext,
    registry: ProbabilityModelRegistry,
    *,
    plugin: PopulationProbabilityPlugin | None = None,
) -> EmpiricalProbabilityResult:
    """Attach an empirical probability only when a calibrated plugin exists."""

    if possibility.probability_status != "UNKNOWN":
        raise ValueError(
            "source-supported possibility must enter empirical layer with "
            "probability_status=UNKNOWN"
        )

    if registry.registry_status == "EMPTY_PENDING_PL5_CALIBRATION":
        return _empty_result(
            status="NOT_CALIBRATED",
            possibility=possibility,
            context=context,
        )

    model = registry.by_manifestation().get(possibility.manifestation_id)
    if model is None:
        return _empty_result(
            status="MODEL_NOT_AVAILABLE",
            possibility=possibility,
            context=context,
        )

    if context.mode not in model.allowed_context_modes:
        return _empty_result(
            status="ABSTAIN_CONTEXT_MODE",
            possibility=possibility,
            context=context,
            model=model,
        )

    if model.requires_personal_context:
        if (
            context.mode != "PERSONALIZED"
            or context.personalization_readiness != "READY"
        ):
            return _empty_result(
                status="ABSTAIN_CONTEXT_QUALITY",
                possibility=possibility,
                context=context,
                model=model,
            )

    if plugin is None:
        return _empty_result(
            status="PLUGIN_NOT_AVAILABLE",
            possibility=possibility,
            context=context,
            model=model,
        )

    value = plugin.predict(model, context, possibility)
    if value is None:
        return _empty_result(
            status="PLUGIN_ABSTAIN",
            possibility=possibility,
            context=context,
            model=model,
        )

    probability = _probability(value, "plugin probability")
    return EmpiricalProbabilityResult(
        schema_version="0.1",
        namespace="EMPIRICALLY_CALIBRATED_PROBABILITY",
        status="ESTIMATED",
        manifestation_id=possibility.manifestation_id,
        source_possibility_mapping_id=possibility.mapping_id,
        context_id=context.context_id,
        probability=probability,
        model_id=model.model_id,
        model_version=model.model_version,
        predictor_family=model.predictor_family,
        parameter_layer=model.parameter_layer,
        calibration_dataset_version=model.calibration_dataset_version,
        calibration_metrics_ref=model.calibration_metrics_ref,
    )
