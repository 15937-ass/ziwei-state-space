"""PL3-M personalized manifestation posterior interface v0.1.

This layer is the Level-3 manifestation namespace:
    P(M | source-supported possibility, population baseline, personal context/history)

It deliberately does not implement a production statistical model.  Production
personalized posteriors remain unavailable until a released PL5-C hierarchical /
individual calibration model exists.

The interface enforces:
- PERSONALIZED context only;
- READY personal-context quality;
- a separately calibrated population/cohort baseline;
- explicit model provenance;
- namespace separation from canonical possibility and population probability.
"""

from __future__ import annotations

import math
from dataclasses import asdict, dataclass
from typing import Any, Mapping, Protocol, Sequence

from .manifestation_context import ManifestationRoutingContext
from .manifestation_probability import EmpiricalProbabilityResult
from .manifestation_router import SourceSupportedPossibility


PERSONAL_POSTERIOR_REGISTRY_STATUSES = frozenset(
    {
        "EMPTY_PENDING_PL5C_CALIBRATION",
        "TEST_ONLY",
        "CALIBRATED_READY",
    }
)

PERSONAL_POSTERIOR_MODEL_STATUSES = frozenset({"TEST_ONLY", "CALIBRATED"})

PERSONAL_POSTERIOR_PARAMETER_LAYERS = frozenset(
    {
        "EMPIRICAL_HIERARCHICAL_PERSONAL",
        "TEST_FIXTURE",
    }
)

PERSONAL_POSTERIOR_RESULT_STATUSES = frozenset(
    {
        "ESTIMATED",
        "NOT_CALIBRATED",
        "MODEL_NOT_AVAILABLE",
        "POPULATION_BASELINE_NOT_AVAILABLE",
        "POPULATION_MODEL_MISMATCH",
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
class PersonalizedPosteriorModelDescriptor:
    model_id: str
    model_version: str
    manifestation_id: str
    target_ontology_version: str
    update_family: str
    parameter_layer: str
    model_status: str
    population_model_id: str
    calibration_dataset_version: str | None
    calibration_metrics_ref: str | None

    def __post_init__(self) -> None:
        if self.parameter_layer not in PERSONAL_POSTERIOR_PARAMETER_LAYERS:
            raise ValueError(
                f"unsupported personalized posterior parameter layer: {self.parameter_layer}"
            )
        if self.model_status not in PERSONAL_POSTERIOR_MODEL_STATUSES:
            raise ValueError(
                f"unsupported personalized posterior model status: {self.model_status}"
            )
        if self.model_status == "CALIBRATED":
            if self.parameter_layer == "TEST_FIXTURE":
                raise ValueError(
                    "CALIBRATED personalized model cannot use TEST_FIXTURE parameters"
                )
            if not self.calibration_dataset_version:
                raise ValueError(
                    "CALIBRATED personalized model requires calibration_dataset_version"
                )
            if not self.calibration_metrics_ref:
                raise ValueError(
                    "CALIBRATED personalized model requires calibration_metrics_ref"
                )
        elif self.parameter_layer != "TEST_FIXTURE":
            raise ValueError(
                "TEST_ONLY personalized model must use TEST_FIXTURE parameter layer"
            )


@dataclass(frozen=True)
class PersonalizedPosteriorRegistry:
    schema_version: str
    registry_status: str
    registry_version: str | None
    models: tuple[PersonalizedPosteriorModelDescriptor, ...]
    blocked_reason: str | None = None

    def __post_init__(self) -> None:
        if self.schema_version != "0.1":
            raise ValueError(
                "PersonalizedPosteriorRegistry schema_version must be 0.1"
            )
        if self.registry_status not in PERSONAL_POSTERIOR_REGISTRY_STATUSES:
            raise ValueError(
                f"unsupported personalized posterior registry status: {self.registry_status}"
            )

        if self.registry_status == "EMPTY_PENDING_PL5C_CALIBRATION":
            if self.models:
                raise ValueError(
                    "EMPTY_PENDING_PL5C_CALIBRATION registry must contain zero models"
                )
            if self.registry_version is not None:
                raise ValueError(
                    "pending personalized posterior registry cannot claim registry_version"
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
                "v0.1 personalized registry allows only one model per manifestation_id"
            )

    def by_manifestation(self) -> dict[str, PersonalizedPosteriorModelDescriptor]:
        return {item.manifestation_id: item for item in self.models}


class PersonalizedPosteriorPlugin(Protocol):
    """External PL5-C adapter for hierarchical/individual posterior updating."""

    def predict(
        self,
        model: PersonalizedPosteriorModelDescriptor,
        context: ManifestationRoutingContext,
        possibility: SourceSupportedPossibility,
        population_baseline: EmpiricalProbabilityResult,
    ) -> float | None:
        ...


@dataclass(frozen=True)
class PersonalizedPosteriorResult:
    schema_version: str
    namespace: str
    status: str
    manifestation_id: str
    source_possibility_mapping_id: str
    context_id: str
    person_key: str | None
    posterior_probability: float | None
    population_probability: float | None
    population_model_id: str | None
    population_model_version: str | None
    personalization_model_id: str | None
    personalization_model_version: str | None
    update_family: str | None
    parameter_layer: str | None
    calibration_dataset_version: str | None
    calibration_metrics_ref: str | None
    uses_individual_history: bool

    def __post_init__(self) -> None:
        if self.schema_version != "0.1":
            raise ValueError(
                "PersonalizedPosteriorResult schema_version must be 0.1"
            )
        if self.namespace != "PERSONALIZED_POSTERIOR":
            raise ValueError(
                "personalized manifestation posterior must use PERSONALIZED_POSTERIOR namespace"
            )
        if self.status not in PERSONAL_POSTERIOR_RESULT_STATUSES:
            raise ValueError(
                f"unsupported personalized posterior result status: {self.status}"
            )

        if self.status == "ESTIMATED":
            if self.posterior_probability is None:
                raise ValueError("ESTIMATED personalized posterior requires probability")
            _probability(
                self.posterior_probability,
                "posterior_probability",
            )
            if self.population_probability is None:
                raise ValueError(
                    "ESTIMATED personalized posterior requires population baseline"
                )
            _probability(self.population_probability, "population_probability")
            if not self.person_key:
                raise ValueError(
                    "ESTIMATED personalized posterior requires person_key"
                )
            if not self.personalization_model_id or not self.personalization_model_version:
                raise ValueError(
                    "ESTIMATED personalized posterior requires personalization model identity"
                )
            if not self.uses_individual_history:
                raise ValueError(
                    "ESTIMATED personalized posterior must declare individual-history use"
                )
        elif self.posterior_probability is not None:
            raise ValueError(
                f"{self.status} result must keep posterior_probability=null"
            )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def compile_personalized_posterior_registry(
    payload: Mapping[str, Any],
) -> PersonalizedPosteriorRegistry:
    if str(payload.get("schema_version", "")).strip() != "0.1":
        raise ValueError(
            "personalized posterior registry schema_version must be 0.1"
        )

    registry_status = _required_text(
        payload.get("registry_status"),
        "registry_status",
    )
    if registry_status not in PERSONAL_POSTERIOR_REGISTRY_STATUSES:
        raise ValueError(
            f"unsupported personalized posterior registry status: {registry_status}"
        )

    raw_models = payload.get("models")
    if not isinstance(raw_models, Sequence) or isinstance(raw_models, (str, bytes)):
        raise ValueError("personalized posterior registry models must be an array")

    models: list[PersonalizedPosteriorModelDescriptor] = []
    seen_ids: set[str] = set()

    for index, row in enumerate(raw_models):
        if not isinstance(row, Mapping):
            raise ValueError(f"models[{index}] must be an object")

        model_id = _required_text(
            row.get("model_id"),
            f"models[{index}].model_id",
        )
        if model_id in seen_ids:
            raise ValueError(f"duplicate personalized posterior model_id: {model_id}")
        seen_ids.add(model_id)

        models.append(
            PersonalizedPosteriorModelDescriptor(
                model_id=model_id,
                model_version=_required_text(
                    row.get("model_version"),
                    f"{model_id}.model_version",
                ),
                manifestation_id=_required_text(
                    row.get("manifestation_id"),
                    f"{model_id}.manifestation_id",
                ),
                target_ontology_version=_required_text(
                    row.get("target_ontology_version"),
                    f"{model_id}.target_ontology_version",
                ),
                update_family=_required_text(
                    row.get("update_family"),
                    f"{model_id}.update_family",
                ),
                parameter_layer=_required_text(
                    row.get("parameter_layer"),
                    f"{model_id}.parameter_layer",
                ),
                model_status=_required_text(
                    row.get("model_status"),
                    f"{model_id}.model_status",
                ),
                population_model_id=_required_text(
                    row.get("population_model_id"),
                    f"{model_id}.population_model_id",
                ),
                calibration_dataset_version=_optional_text(
                    row.get("calibration_dataset_version")
                ),
                calibration_metrics_ref=_optional_text(
                    row.get("calibration_metrics_ref")
                ),
            )
        )

    return PersonalizedPosteriorRegistry(
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
    population_baseline: EmpiricalProbabilityResult | None = None,
    model: PersonalizedPosteriorModelDescriptor | None = None,
) -> PersonalizedPosteriorResult:
    return PersonalizedPosteriorResult(
        schema_version="0.1",
        namespace="PERSONALIZED_POSTERIOR",
        status=status,
        manifestation_id=possibility.manifestation_id,
        source_possibility_mapping_id=possibility.mapping_id,
        context_id=context.context_id,
        person_key=context.person_key,
        posterior_probability=None,
        population_probability=(
            population_baseline.probability if population_baseline else None
        ),
        population_model_id=(
            population_baseline.model_id if population_baseline else None
        ),
        population_model_version=(
            population_baseline.model_version if population_baseline else None
        ),
        personalization_model_id=model.model_id if model else None,
        personalization_model_version=model.model_version if model else None,
        update_family=model.update_family if model else None,
        parameter_layer=model.parameter_layer if model else None,
        calibration_dataset_version=(
            model.calibration_dataset_version if model else None
        ),
        calibration_metrics_ref=model.calibration_metrics_ref if model else None,
        uses_individual_history=False,
    )


def _validate_population_baseline_alignment(
    possibility: SourceSupportedPossibility,
    context: ManifestationRoutingContext,
    population_baseline: EmpiricalProbabilityResult,
) -> None:
    if population_baseline.namespace != "EMPIRICALLY_CALIBRATED_PROBABILITY":
        raise ValueError(
            "population baseline must come from EMPIRICALLY_CALIBRATED_PROBABILITY namespace"
        )
    if population_baseline.manifestation_id != possibility.manifestation_id:
        raise ValueError("population baseline manifestation_id mismatch")
    if (
        population_baseline.source_possibility_mapping_id
        != possibility.mapping_id
    ):
        raise ValueError("population baseline source possibility mismatch")
    if population_baseline.context_id != context.context_id:
        raise ValueError("population baseline context_id mismatch")


def evaluate_personalized_manifestation_posterior(
    possibility: SourceSupportedPossibility,
    context: ManifestationRoutingContext,
    population_baseline: EmpiricalProbabilityResult,
    registry: PersonalizedPosteriorRegistry,
    *,
    plugin: PersonalizedPosteriorPlugin | None = None,
) -> PersonalizedPosteriorResult:
    """Estimate a personal manifestation posterior only behind all PL3-M gates."""

    if possibility.probability_status != "UNKNOWN":
        raise ValueError(
            "source-supported possibility must enter personalized layer with probability_status=UNKNOWN"
        )

    _validate_population_baseline_alignment(
        possibility,
        context,
        population_baseline,
    )

    if context.mode != "PERSONALIZED":
        return _empty_result(
            status="ABSTAIN_CONTEXT_MODE",
            possibility=possibility,
            context=context,
            population_baseline=population_baseline,
        )

    if (
        context.personalization_readiness != "READY"
        or not context.person_key
        or not context.acquired_state_id
    ):
        return _empty_result(
            status="ABSTAIN_CONTEXT_QUALITY",
            possibility=possibility,
            context=context,
            population_baseline=population_baseline,
        )

    if registry.registry_status == "EMPTY_PENDING_PL5C_CALIBRATION":
        return _empty_result(
            status="NOT_CALIBRATED",
            possibility=possibility,
            context=context,
            population_baseline=population_baseline,
        )

    model = registry.by_manifestation().get(possibility.manifestation_id)
    if model is None:
        return _empty_result(
            status="MODEL_NOT_AVAILABLE",
            possibility=possibility,
            context=context,
            population_baseline=population_baseline,
        )

    if (
        population_baseline.status != "ESTIMATED"
        or population_baseline.probability is None
        or not population_baseline.model_id
        or not population_baseline.model_version
    ):
        return _empty_result(
            status="POPULATION_BASELINE_NOT_AVAILABLE",
            possibility=possibility,
            context=context,
            population_baseline=population_baseline,
            model=model,
        )

    if population_baseline.model_id != model.population_model_id:
        return _empty_result(
            status="POPULATION_MODEL_MISMATCH",
            possibility=possibility,
            context=context,
            population_baseline=population_baseline,
            model=model,
        )

    if plugin is None:
        return _empty_result(
            status="PLUGIN_NOT_AVAILABLE",
            possibility=possibility,
            context=context,
            population_baseline=population_baseline,
            model=model,
        )

    value = plugin.predict(
        model,
        context,
        possibility,
        population_baseline,
    )
    if value is None:
        return _empty_result(
            status="PLUGIN_ABSTAIN",
            possibility=possibility,
            context=context,
            population_baseline=population_baseline,
            model=model,
        )

    posterior_probability = _probability(
        value,
        "plugin posterior_probability",
    )

    return PersonalizedPosteriorResult(
        schema_version="0.1",
        namespace="PERSONALIZED_POSTERIOR",
        status="ESTIMATED",
        manifestation_id=possibility.manifestation_id,
        source_possibility_mapping_id=possibility.mapping_id,
        context_id=context.context_id,
        person_key=context.person_key,
        posterior_probability=posterior_probability,
        population_probability=population_baseline.probability,
        population_model_id=population_baseline.model_id,
        population_model_version=population_baseline.model_version,
        personalization_model_id=model.model_id,
        personalization_model_version=model.model_version,
        update_family=model.update_family,
        parameter_layer=model.parameter_layer,
        calibration_dataset_version=model.calibration_dataset_version,
        calibration_metrics_ref=model.calibration_metrics_ref,
        uses_individual_history=True,
    )
