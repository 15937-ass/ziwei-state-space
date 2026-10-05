"""PL3-S minimal discrete Bayesian belief interface v0.1.

This module updates a PERSONAL acquired-state belief using an explicitly
versioned probabilistic observation model.  It is not a manifestation
probability model and it never reads/writes canonical Zi Wei rule truth.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from typing import Any, Mapping, Sequence

from .acquired_state import ACQUIRED_STATE_DOMAINS, AcquiredStateProfile
from .longitudinal_observation import CONFIDENCE_LEVELS


BELIEF_MODEL_STATUSES = frozenset({"TEST_ONLY", "CALIBRATED"})
BELIEF_PARAMETER_LAYERS = frozenset({"EMPIRICAL", "PERSONAL", "TEST_FIXTURE"})
BELIEF_UPDATE_STATUSES = frozenset(
    {"UPDATED", "NO_USABLE_EVIDENCE", "ZERO_EVIDENCE_MASS"}
)
EVIDENCE_USE_STATUSES = frozenset(
    {
        "USED",
        "SKIPPED_MISSING",
        "SKIPPED_CONFLICT",
        "SKIPPED_CONFIDENCE",
        "SKIPPED_UNMODELLED_VALUE",
    }
)

_PROB_TOL = 1e-9


def _required_text(value: Any, field: str) -> str:
    text = str(value or "").strip()
    if not text:
        raise ValueError(f"{field} is required")
    return text


def _probability(value: Any, field: str) -> float:
    if isinstance(value, bool):
        raise ValueError(f"{field} must be numeric probability")
    try:
        number = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{field} must be numeric probability") from exc
    if not (0.0 <= number <= 1.0) or not math.isfinite(number):
        raise ValueError(f"{field} must be finite in [0,1]")
    return number


def _likelihood_vector(
    raw: Mapping[str, Any],
    *,
    expected: set[str],
    field: str,
) -> tuple[tuple[str, float], ...]:
    keys = {str(key).strip() for key in raw}
    if keys != expected:
        raise ValueError(
            f"{field} keys must exactly match hypotheses: "
            f"expected={sorted(expected)}, got={sorted(keys)}"
        )
    return tuple(
        sorted(
            (
                str(key).strip(),
                _probability(value, f"{field}.{key}"),
            )
            for key, value in raw.items()
        )
    )


def _normalize_distribution(
    raw: Mapping[str, Any],
    *,
    expected: set[str],
    field: str,
) -> tuple[tuple[str, float], ...]:
    keys = {str(key).strip() for key in raw}
    if keys != expected:
        raise ValueError(
            f"{field} keys must exactly match hypotheses: "
            f"expected={sorted(expected)}, got={sorted(keys)}"
        )
    values = tuple(
        sorted(
            (
                str(key).strip(),
                _probability(value, f"{field}.{key}"),
            )
            for key, value in raw.items()
        )
    )
    total = sum(value for _, value in values)
    if abs(total - 1.0) > _PROB_TOL:
        raise ValueError(f"{field} probabilities must sum to 1, got {total}")
    return values


@dataclass(frozen=True)
class BeliefEvidenceChannel:
    evidence_id: str
    domain: str
    key: str
    accepted_confidences: tuple[str, ...]
    likelihoods: Mapping[str, tuple[tuple[str, float], ...]]

    def __post_init__(self) -> None:
        if self.domain not in ACQUIRED_STATE_DOMAINS:
            raise ValueError(f"unsupported evidence domain: {self.domain}")
        if not self.key.strip():
            raise ValueError("BeliefEvidenceChannel.key is required")
        if not self.accepted_confidences:
            raise ValueError("accepted_confidences cannot be empty")
        unknown = sorted(set(self.accepted_confidences) - set(CONFIDENCE_LEVELS))
        if unknown:
            raise ValueError(
                "unsupported accepted confidence values: " + ", ".join(unknown)
            )
        if not self.likelihoods:
            raise ValueError("BeliefEvidenceChannel.likelihoods cannot be empty")


@dataclass(frozen=True)
class DiscreteBeliefModel:
    schema_version: str
    model_id: str
    model_version: str
    domain: str
    state_key: str
    hypotheses: tuple[str, ...]
    prior: tuple[tuple[str, float], ...]
    evidence_channels: tuple[BeliefEvidenceChannel, ...]
    parameter_layer: str
    parameter_source: str
    model_status: str

    def __post_init__(self) -> None:
        if self.schema_version != "0.1":
            raise ValueError("DiscreteBeliefModel schema_version must be 0.1")
        if self.domain not in ACQUIRED_STATE_DOMAINS:
            raise ValueError(f"unsupported belief domain: {self.domain}")
        if self.parameter_layer not in BELIEF_PARAMETER_LAYERS:
            raise ValueError(f"unsupported parameter layer: {self.parameter_layer}")
        if self.model_status not in BELIEF_MODEL_STATUSES:
            raise ValueError(f"unsupported belief model status: {self.model_status}")
        if self.model_status == "CALIBRATED" and self.parameter_layer == "TEST_FIXTURE":
            raise ValueError("CALIBRATED model cannot use TEST_FIXTURE parameters")
        if self.parameter_layer == "TEST_FIXTURE" and self.model_status != "TEST_ONLY":
            raise ValueError("TEST_FIXTURE parameters require TEST_ONLY status")


@dataclass(frozen=True)
class EvidenceUse:
    evidence_id: str
    domain: str
    key: str
    status: str
    observed_value: str | None
    fact_ids: tuple[str, ...]
    reason: str

    def __post_init__(self) -> None:
        if self.status not in EVIDENCE_USE_STATUSES:
            raise ValueError(f"unsupported evidence use status: {self.status}")


@dataclass(frozen=True)
class BeliefUpdateResult:
    schema_version: str
    model_id: str
    model_version: str
    state_id: str
    belief_domain: str
    belief_state_key: str
    status: str
    prior: tuple[tuple[str, float], ...]
    posterior: tuple[tuple[str, float], ...]
    evidence_use: tuple[EvidenceUse, ...]
    parameter_layer: str
    parameter_source: str

    def __post_init__(self) -> None:
        if self.schema_version != "0.1":
            raise ValueError("BeliefUpdateResult schema_version must be 0.1")
        if self.status not in BELIEF_UPDATE_STATUSES:
            raise ValueError(f"unsupported belief update status: {self.status}")

    def posterior_dict(self) -> dict[str, float]:
        return dict(self.posterior)

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "model_id": self.model_id,
            "model_version": self.model_version,
            "state_id": self.state_id,
            "belief_domain": self.belief_domain,
            "belief_state_key": self.belief_state_key,
            "status": self.status,
            "prior": dict(self.prior),
            "posterior": dict(self.posterior),
            "evidence_use": [asdict(item) for item in self.evidence_use],
            "parameter_layer": self.parameter_layer,
            "parameter_source": self.parameter_source,
        }


def compile_discrete_belief_model(
    payload: Mapping[str, Any],
) -> DiscreteBeliefModel:
    if str(payload.get("schema_version", "")).strip() != "0.1":
        raise ValueError("belief model schema_version must be 0.1")

    model_id = _required_text(payload.get("model_id"), "model_id")
    model_version = _required_text(payload.get("model_version"), "model_version")
    domain = _required_text(payload.get("domain"), "domain")
    state_key = _required_text(payload.get("state_key"), "state_key")
    parameter_layer = _required_text(
        payload.get("parameter_layer"), "parameter_layer"
    )
    parameter_source = _required_text(
        payload.get("parameter_source"), "parameter_source"
    )
    model_status = _required_text(payload.get("model_status"), "model_status")

    raw_hypotheses = payload.get("hypotheses")
    if not isinstance(raw_hypotheses, Sequence) or isinstance(
        raw_hypotheses, (str, bytes)
    ):
        raise ValueError("hypotheses must be an array")
    hypotheses = tuple(
        sorted({str(item).strip() for item in raw_hypotheses if str(item).strip()})
    )
    if len(hypotheses) < 2:
        raise ValueError("belief model requires at least two hypotheses")
    hypothesis_set = set(hypotheses)

    raw_prior = payload.get("prior")
    if not isinstance(raw_prior, Mapping):
        raise ValueError("prior must be an object")
    prior = _normalize_distribution(
        raw_prior,
        expected=hypothesis_set,
        field="prior",
    )

    raw_channels = payload.get("evidence_channels")
    if not isinstance(raw_channels, Sequence) or isinstance(
        raw_channels, (str, bytes)
    ):
        raise ValueError("evidence_channels must be an array")

    channels: list[BeliefEvidenceChannel] = []
    seen_ids: set[str] = set()
    for index, item in enumerate(raw_channels):
        if not isinstance(item, Mapping):
            raise ValueError(f"evidence_channels[{index}] must be an object")
        evidence_id = _required_text(
            item.get("evidence_id"),
            f"evidence_channels[{index}].evidence_id",
        )
        if evidence_id in seen_ids:
            raise ValueError(f"duplicate evidence_id: {evidence_id}")
        seen_ids.add(evidence_id)

        accepted_raw = item.get(
            "accepted_confidences", ["HIGH", "MEDIUM", "LOW"]
        )
        if not isinstance(accepted_raw, Sequence) or isinstance(
            accepted_raw, (str, bytes)
        ):
            raise ValueError(
                f"evidence_channels[{index}].accepted_confidences must be an array"
            )
        accepted = tuple(
            sorted(
                {
                    str(value).strip()
                    for value in accepted_raw
                    if str(value).strip()
                }
            )
        )

        raw_likelihoods = item.get("likelihoods")
        if not isinstance(raw_likelihoods, Mapping) or not raw_likelihoods:
            raise ValueError(
                f"evidence_channels[{index}].likelihoods must be a non-empty object"
            )

        by_value: dict[str, tuple[tuple[str, float], ...]] = {}
        for observed_value, distribution in raw_likelihoods.items():
            value_key = str(observed_value)
            if not isinstance(distribution, Mapping):
                raise ValueError(
                    f"{evidence_id}.likelihoods.{value_key} must be an object"
                )
            by_value[value_key] = _likelihood_vector(
                distribution,
                expected=hypothesis_set,
                field=f"{evidence_id}.likelihoods.{value_key}",
            )

        # Each hypothesis must define a proper categorical observation model.
        for hypothesis in hypotheses:
            total = sum(dict(dist)[hypothesis] for dist in by_value.values())
            if abs(total - 1.0) > _PROB_TOL:
                raise ValueError(
                    f"{evidence_id}: likelihood P(value|{hypothesis}) "
                    f"must sum to 1 across modelled values, got {total}"
                )

        channels.append(
            BeliefEvidenceChannel(
                evidence_id=evidence_id,
                domain=_required_text(
                    item.get("domain"),
                    f"evidence_channels[{index}].domain",
                ),
                key=_required_text(
                    item.get("key"),
                    f"evidence_channels[{index}].key",
                ),
                accepted_confidences=accepted,
                likelihoods=dict(sorted(by_value.items())),
            )
        )

    return DiscreteBeliefModel(
        schema_version="0.1",
        model_id=model_id,
        model_version=model_version,
        domain=domain,
        state_key=state_key,
        hypotheses=hypotheses,
        prior=prior,
        evidence_channels=tuple(
            sorted(channels, key=lambda item: item.evidence_id)
        ),
        parameter_layer=parameter_layer,
        parameter_source=parameter_source,
        model_status=model_status,
    )


def _scalar_key(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if value is None:
        return "null"
    return str(value)


def update_discrete_belief(
    state: AcquiredStateProfile,
    model: DiscreteBeliefModel,
) -> BeliefUpdateResult:
    """Compute one discrete posterior from available unambiguous state facts.

    Missing/conflicted/unsupported evidence is skipped, never imputed.
    """

    assertions_by_key: dict[tuple[str, str], list[Any]] = {}
    for fact in state.assertions:
        assertions_by_key.setdefault((fact.domain, fact.key), []).append(fact)

    conflicted_keys = {
        (item.domain, item.key) for item in state.conflicts
    }
    missing_keys = {
        (item.domain, item.key) for item in state.missingness
    }

    posterior = dict(model.prior)
    evidence_use: list[EvidenceUse] = []
    used_count = 0

    for channel in model.evidence_channels:
        key = (channel.domain, channel.key)
        facts = tuple(
            sorted(
                assertions_by_key.get(key, []),
                key=lambda item: item.fact_id,
            )
        )

        if key in conflicted_keys:
            evidence_use.append(
                EvidenceUse(
                    evidence_id=channel.evidence_id,
                    domain=channel.domain,
                    key=channel.key,
                    status="SKIPPED_CONFLICT",
                    observed_value=None,
                    fact_ids=tuple(item.fact_id for item in facts),
                    reason="UNRESOLVED_STATE_CONFLICT",
                )
            )
            continue

        if key in missing_keys or not facts:
            evidence_use.append(
                EvidenceUse(
                    evidence_id=channel.evidence_id,
                    domain=channel.domain,
                    key=channel.key,
                    status="SKIPPED_MISSING",
                    observed_value=None,
                    fact_ids=tuple(item.fact_id for item in facts),
                    reason="MISSING_OR_UNOBSERVED_STATE",
                )
            )
            continue

        if len(facts) != 1:
            evidence_use.append(
                EvidenceUse(
                    evidence_id=channel.evidence_id,
                    domain=channel.domain,
                    key=channel.key,
                    status="SKIPPED_CONFLICT",
                    observed_value=None,
                    fact_ids=tuple(item.fact_id for item in facts),
                    reason="MULTIPLE_UNRESOLVED_ASSERTIONS",
                )
            )
            continue

        fact = facts[0]
        if fact.confidence not in channel.accepted_confidences:
            evidence_use.append(
                EvidenceUse(
                    evidence_id=channel.evidence_id,
                    domain=channel.domain,
                    key=channel.key,
                    status="SKIPPED_CONFIDENCE",
                    observed_value=_scalar_key(fact.value),
                    fact_ids=(fact.fact_id,),
                    reason="CONFIDENCE_NOT_ACCEPTED_BY_MODEL",
                )
            )
            continue

        observed = _scalar_key(fact.value)
        likelihood = channel.likelihoods.get(observed)
        if likelihood is None:
            evidence_use.append(
                EvidenceUse(
                    evidence_id=channel.evidence_id,
                    domain=channel.domain,
                    key=channel.key,
                    status="SKIPPED_UNMODELLED_VALUE",
                    observed_value=observed,
                    fact_ids=(fact.fact_id,),
                    reason="OBSERVED_VALUE_NOT_IN_LIKELIHOOD_TABLE",
                )
            )
            continue

        likelihood_dict = dict(likelihood)
        unnormalized = {
            hypothesis: posterior[hypothesis] * likelihood_dict[hypothesis]
            for hypothesis in model.hypotheses
        }
        mass = sum(unnormalized.values())
        if mass <= 0.0:
            evidence_use.append(
                EvidenceUse(
                    evidence_id=channel.evidence_id,
                    domain=channel.domain,
                    key=channel.key,
                    status="USED",
                    observed_value=observed,
                    fact_ids=(fact.fact_id,),
                    reason="ZERO_TOTAL_EVIDENCE_MASS",
                )
            )
            return BeliefUpdateResult(
                schema_version="0.1",
                model_id=model.model_id,
                model_version=model.model_version,
                state_id=state.state_id,
                belief_domain=model.domain,
                belief_state_key=model.state_key,
                status="ZERO_EVIDENCE_MASS",
                prior=model.prior,
                posterior=tuple(sorted(posterior.items())),
                evidence_use=tuple(evidence_use),
                parameter_layer=model.parameter_layer,
                parameter_source=model.parameter_source,
            )

        posterior = {
            hypothesis: unnormalized[hypothesis] / mass
            for hypothesis in model.hypotheses
        }
        used_count += 1
        evidence_use.append(
            EvidenceUse(
                evidence_id=channel.evidence_id,
                domain=channel.domain,
                key=channel.key,
                status="USED",
                observed_value=observed,
                fact_ids=(fact.fact_id,),
                reason="BAYES_UPDATE_APPLIED",
            )
        )

    status = "UPDATED" if used_count else "NO_USABLE_EVIDENCE"
    return BeliefUpdateResult(
        schema_version="0.1",
        model_id=model.model_id,
        model_version=model.model_version,
        state_id=state.state_id,
        belief_domain=model.domain,
        belief_state_key=model.state_key,
        status=status,
        prior=model.prior,
        posterior=tuple(sorted(posterior.items())),
        evidence_use=tuple(evidence_use),
        parameter_layer=model.parameter_layer,
        parameter_source=model.parameter_source,
    )
