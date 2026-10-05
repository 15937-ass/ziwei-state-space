"""PL3-S minimal discrete Bayesian state-belief interface v0.1.

No production prior or likelihood is bundled here. Numeric Bayesian updating is
permitted only when every numeric parameter comes from an explicit empirical
calibration artifact. Synthetic parameters are accepted only behind an explicit
test-only flag so unit tests can verify the arithmetic without creating product
defaults.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation, getcontext
from typing import Any, Mapping, Sequence

from .state_quality import StateQualityReport


getcontext().prec = 40

PARAMETER_PROVENANCE_TYPES = frozenset(
    {"EMPIRICAL_CALIBRATION", "TEST_ONLY_SYNTHETIC"}
)
BELIEF_STATUSES = frozenset({"CALIBRATED_POSTERIOR", "HELD_QUALITY_GATE"})


def _required_text(value: Any, field: str) -> str:
    text = str(value or "").strip()
    if not text:
        raise ValueError(f"{field} is required")
    return text


def _decimal(value: Any, field: str) -> Decimal:
    try:
        result = Decimal(str(value))
    except (InvalidOperation, ValueError) as exc:
        raise ValueError(f"{field} must be a decimal number") from exc
    if not result.is_finite():
        raise ValueError(f"{field} must be finite")
    return result


def _probability(value: Any, field: str) -> Decimal:
    result = _decimal(value, field)
    if result < 0 or result > 1:
        raise ValueError(f"{field} must be between 0 and 1")
    return result


def _normalized_distribution(
    values: Mapping[str, Any],
    *,
    field: str,
) -> tuple[tuple[str, Decimal], ...]:
    if not isinstance(values, Mapping) or not values:
        raise ValueError(f"{field} must be a non-empty object")
    rows = tuple(
        sorted(
            (
                _required_text(key, f"{field}.hypothesis"),
                _probability(value, f"{field}.{key}"),
            )
            for key, value in values.items()
        )
    )
    if sum((value for _, value in rows), Decimal("0")) != Decimal("1"):
        raise ValueError(f"{field} must sum exactly to 1")
    if any(value == 0 for _, value in rows):
        raise ValueError(
            f"{field} cannot contain zero-mass hypotheses in v0.1; "
            "remove impossible hypotheses explicitly"
        )
    return rows


@dataclass(frozen=True)
class BayesianParameterProvenance:
    provenance_type: str
    artifact_id: str
    artifact_version: str
    parameter_set_id: str

    def __post_init__(self) -> None:
        if self.provenance_type not in PARAMETER_PROVENANCE_TYPES:
            raise ValueError(
                f"unsupported Bayesian parameter provenance: {self.provenance_type}"
            )
        _required_text(self.artifact_id, "BayesianParameterProvenance.artifact_id")
        _required_text(
            self.artifact_version, "BayesianParameterProvenance.artifact_version"
        )
        _required_text(
            self.parameter_set_id, "BayesianParameterProvenance.parameter_set_id"
        )


@dataclass(frozen=True)
class DiscreteStatePrior:
    belief_id: str
    domain: str
    key: str
    distribution: tuple[tuple[str, Decimal], ...]
    provenance: BayesianParameterProvenance

    def __post_init__(self) -> None:
        _required_text(self.belief_id, "DiscreteStatePrior.belief_id")
        _required_text(self.domain, "DiscreteStatePrior.domain")
        _required_text(self.key, "DiscreteStatePrior.key")
        if not self.distribution:
            raise ValueError("DiscreteStatePrior.distribution cannot be empty")


@dataclass(frozen=True)
class DiscreteObservationLikelihood:
    evidence_id: str
    domain: str
    key: str
    likelihood_by_hypothesis: tuple[tuple[str, Decimal], ...]
    provenance: BayesianParameterProvenance

    def __post_init__(self) -> None:
        _required_text(self.evidence_id, "DiscreteObservationLikelihood.evidence_id")
        _required_text(self.domain, "DiscreteObservationLikelihood.domain")
        _required_text(self.key, "DiscreteObservationLikelihood.key")


@dataclass(frozen=True)
class DiscreteStateBelief:
    schema_version: str
    belief_id: str
    domain: str
    key: str
    status: str
    distribution: tuple[tuple[str, str], ...]
    prior_belief_id: str
    evidence_id: str
    state_id: str
    requirement_id: str
    parameter_artifact_ids: tuple[str, ...]

    def __post_init__(self) -> None:
        if self.schema_version != "0.1":
            raise ValueError("DiscreteStateBelief schema_version must be 0.1")
        if self.status not in BELIEF_STATUSES:
            raise ValueError(f"unsupported belief status: {self.status}")

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "belief_id": self.belief_id,
            "domain": self.domain,
            "key": self.key,
            "status": self.status,
            "distribution": {
                hypothesis: probability
                for hypothesis, probability in self.distribution
            },
            "prior_belief_id": self.prior_belief_id,
            "evidence_id": self.evidence_id,
            "state_id": self.state_id,
            "requirement_id": self.requirement_id,
            "parameter_artifact_ids": list(self.parameter_artifact_ids),
        }


def compile_discrete_state_prior(
    document: Mapping[str, Any],
    *,
    allow_test_only: bool = False,
) -> DiscreteStatePrior:
    provenance_raw = document.get("provenance")
    if not isinstance(provenance_raw, Mapping):
        raise ValueError("prior provenance is required")
    provenance = BayesianParameterProvenance(
        provenance_type=_required_text(
            provenance_raw.get("provenance_type"), "prior.provenance_type"
        ),
        artifact_id=_required_text(
            provenance_raw.get("artifact_id"), "prior.artifact_id"
        ),
        artifact_version=_required_text(
            provenance_raw.get("artifact_version"), "prior.artifact_version"
        ),
        parameter_set_id=_required_text(
            provenance_raw.get("parameter_set_id"), "prior.parameter_set_id"
        ),
    )
    if provenance.provenance_type == "TEST_ONLY_SYNTHETIC" and not allow_test_only:
        raise ValueError("synthetic Bayesian parameters are test-only and fail closed")

    return DiscreteStatePrior(
        belief_id=_required_text(document.get("belief_id"), "prior.belief_id"),
        domain=_required_text(document.get("domain"), "prior.domain"),
        key=_required_text(document.get("key"), "prior.key"),
        distribution=_normalized_distribution(
            document.get("distribution"), field="prior.distribution"
        ),
        provenance=provenance,
    )


def compile_observation_likelihood(
    document: Mapping[str, Any],
    *,
    allow_test_only: bool = False,
) -> DiscreteObservationLikelihood:
    provenance_raw = document.get("provenance")
    if not isinstance(provenance_raw, Mapping):
        raise ValueError("likelihood provenance is required")
    provenance = BayesianParameterProvenance(
        provenance_type=_required_text(
            provenance_raw.get("provenance_type"), "likelihood.provenance_type"
        ),
        artifact_id=_required_text(
            provenance_raw.get("artifact_id"), "likelihood.artifact_id"
        ),
        artifact_version=_required_text(
            provenance_raw.get("artifact_version"), "likelihood.artifact_version"
        ),
        parameter_set_id=_required_text(
            provenance_raw.get("parameter_set_id"), "likelihood.parameter_set_id"
        ),
    )
    if provenance.provenance_type == "TEST_ONLY_SYNTHETIC" and not allow_test_only:
        raise ValueError("synthetic Bayesian parameters are test-only and fail closed")

    raw = document.get("likelihood_by_hypothesis")
    if not isinstance(raw, Mapping) or not raw:
        raise ValueError("likelihood_by_hypothesis must be a non-empty object")
    likelihoods = tuple(
        sorted(
            (
                _required_text(key, "likelihood hypothesis"),
                _probability(value, f"likelihood.{key}"),
            )
            for key, value in raw.items()
        )
    )
    return DiscreteObservationLikelihood(
        evidence_id=_required_text(document.get("evidence_id"), "evidence_id"),
        domain=_required_text(document.get("domain"), "likelihood.domain"),
        key=_required_text(document.get("key"), "likelihood.key"),
        likelihood_by_hypothesis=likelihoods,
        provenance=provenance,
    )


def _quality_requirement(
    report: StateQualityReport,
    requirement_id: str,
):
    rows = [
        item
        for item in report.requirements
        if item.requirement_id == requirement_id
    ]
    if len(rows) != 1:
        raise ValueError(
            f"quality report must contain exactly one requirement_id={requirement_id}"
        )
    return rows[0]


def bayesian_state_update(
    *,
    prior: DiscreteStatePrior,
    evidence: DiscreteObservationLikelihood,
    quality_report: StateQualityReport,
    requirement_id: str,
) -> DiscreteStateBelief:
    """Perform one calibrated categorical Bayes update.

    This function has no default numeric parameters. Both the prior and the
    likelihood must be externally calibrated/provenanced.
    """

    requirement = _quality_requirement(quality_report, requirement_id)
    if requirement.domain != prior.domain or requirement.key != prior.key:
        raise ValueError("quality requirement does not match prior domain/key")
    if evidence.domain != prior.domain or evidence.key != prior.key:
        raise ValueError("likelihood does not match prior domain/key")
    if requirement.status != "AVAILABLE":
        raise ValueError(
            f"Bayesian update held by state quality gate: {requirement.status}"
        )

    prior_map = dict(prior.distribution)
    likelihood_map = dict(evidence.likelihood_by_hypothesis)
    if set(prior_map) != set(likelihood_map):
        raise ValueError("prior and likelihood hypothesis sets must match exactly")

    unnormalized = {
        hypothesis: prior_map[hypothesis] * likelihood_map[hypothesis]
        for hypothesis in sorted(prior_map)
    }
    denominator = sum(unnormalized.values(), Decimal("0"))
    if denominator == 0:
        raise ValueError("Bayesian evidence has zero marginal likelihood")

    posterior = tuple(
        (
            hypothesis,
            str((unnormalized[hypothesis] / denominator).normalize()),
        )
        for hypothesis in sorted(unnormalized)
    )
    id_payload = {
        "prior_belief_id": prior.belief_id,
        "evidence_id": evidence.evidence_id,
        "state_id": quality_report.state_id,
        "requirement_id": requirement_id,
        "posterior": posterior,
        "prior_parameter_set": prior.provenance.parameter_set_id,
        "likelihood_parameter_set": evidence.provenance.parameter_set_id,
    }
    raw = json.dumps(
        id_payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    belief_id = "BELIEF-" + hashlib.sha256(raw).hexdigest()[:24]

    return DiscreteStateBelief(
        schema_version="0.1",
        belief_id=belief_id,
        domain=prior.domain,
        key=prior.key,
        status="CALIBRATED_POSTERIOR",
        distribution=posterior,
        prior_belief_id=prior.belief_id,
        evidence_id=evidence.evidence_id,
        state_id=quality_report.state_id,
        requirement_id=requirement_id,
        parameter_artifact_ids=tuple(
            sorted(
                {
                    prior.provenance.artifact_id,
                    evidence.provenance.artifact_id,
                }
            )
        ),
    )
