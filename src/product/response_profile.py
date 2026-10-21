"""PL3-R decade/year ResponseProfile compiler v0.1.

This module creates the first explicit response intermediate (tau_t) while
preserving the project's epistemic boundaries:

NatalStateProfile N
+ TemporalEnvironmentProfile E_t (DECADE + YEAR)
+ active locked canonical response knowledge Kr
-> symbolic ResponseProfile tau_t

The active Product Knowledge lock currently contains no compiler-eligible
canonical Career temporal-reaction rule.  Therefore v0.1 deliberately emits an
auditable UNKNOWN/BLOCKED temporal-response disposition instead of inventing a
dynamic effect.  Matched NATAL Career projection descriptors are preserved as
source-semantic evidence only.

This module does not compute probability, learned/numeric magnitude, outcome,
personalization, or manifestation candidates.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Mapping

from .natal_prior import NatalStateProfile
from .temporal_environment import TemporalEnvironmentProfile


ROOT = Path(__file__).resolve().parents[2]

RESPONSE_PROFILE_SCHEMA_VERSION = "0.1"
RESPONSE_COMPILER_VERSION = "PL3R_DECADE_YEAR_RESPONSE_COMPILER_V0_1"
RESPONSE_DOMAIN = "career"
REQUIRED_TEMPORAL_LAYERS = frozenset({"DECADE", "YEAR"})
ALLOWED_DYNAMIC_EFFECTS = frozenset(
    {"ACTIVATE", "STRENGTHEN", "WEAKEN", "TRANSFORM", "GATE"}
)
CURRENT_TEMPORAL_KR_GATE_PATH = (
    "knowledge/wp07b/CAREER_TEMPORAL_REACTION_ELIGIBILITY_SUMMARY_v0.1.json"
)
UNKNOWN_NO_CANONICAL_TEMPORAL_RESPONSE_RULE = (
    "UNKNOWN_NO_CANONICAL_TEMPORAL_RESPONSE_RULE"
)


@dataclass(frozen=True)
class TemporalKrGate:
    active_bundle_id: str
    active_bundle_path: str
    k_response_source_commit: str
    gate_artifact_path: str
    gate_audit_id: str
    eligible_rule_count: int
    executable_pilot_emitted: bool
    production_registry_should_remain_empty: bool
    decision: str

    def __post_init__(self) -> None:
        if not self.active_bundle_id.strip():
            raise ValueError("TemporalKrGate.active_bundle_id is required")
        if not self.active_bundle_path.strip():
            raise ValueError("TemporalKrGate.active_bundle_path is required")
        if not self.k_response_source_commit.strip():
            raise ValueError("TemporalKrGate.k_response_source_commit is required")
        if self.gate_artifact_path != CURRENT_TEMPORAL_KR_GATE_PATH:
            raise ValueError("unexpected temporal Kr gate artifact")
        if not self.gate_audit_id.strip() or not self.decision.strip():
            raise ValueError("temporal Kr gate provenance is incomplete")
        if self.eligible_rule_count < 0:
            raise ValueError("eligible_rule_count cannot be negative")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class NatalResponseSemanticEvidence:
    source_rule_id: str
    projection_domain: str
    projection_target: str
    source_location: str
    source_span_ids: tuple[str, ...]
    compatibility_band: str
    semantic_status: str = "SOURCE_PROJECTION_SEMANTIC_ONLY"

    def __post_init__(self) -> None:
        for value, field in (
            (self.source_rule_id, "source_rule_id"),
            (self.projection_domain, "projection_domain"),
            (self.projection_target, "projection_target"),
            (self.source_location, "source_location"),
            (self.compatibility_band, "compatibility_band"),
        ):
            if not str(value).strip():
                raise ValueError(f"NatalResponseSemanticEvidence.{field} is required")
        if not self.source_span_ids:
            raise ValueError("NatalResponseSemanticEvidence.source_span_ids is required")
        if self.semantic_status != "SOURCE_PROJECTION_SEMANTIC_ONLY":
            raise ValueError("unsupported natal response semantic status")

    def to_dict(self) -> dict[str, Any]:
        return {
            "source_rule_id": self.source_rule_id,
            "projection_domain": self.projection_domain,
            "projection_target": self.projection_target,
            "source_location": self.source_location,
            "source_span_ids": list(self.source_span_ids),
            "compatibility_band": self.compatibility_band,
            "semantic_status": self.semantic_status,
        }


@dataclass(frozen=True)
class ResponseTemporalFactEvidence:
    layer: str
    fact: str
    provenance: str

    def __post_init__(self) -> None:
        if self.layer not in REQUIRED_TEMPORAL_LAYERS:
            raise ValueError(f"ResponseProfile v0.1 cannot consume {self.layer}")
        if not self.fact.strip() or not self.provenance.strip():
            raise ValueError("response temporal fact/provenance is required")

    def to_dict(self) -> dict[str, str]:
        return asdict(self)


@dataclass(frozen=True)
class ResponseProfile:
    schema_version: str
    profile_id: str
    compiler_version: str
    domain: str
    natal_profile_id: str
    temporal_profile_id: str
    knowledge_version: str
    target_label: str
    consumed_layers: tuple[str, ...]
    ignored_environment_layers: tuple[str, ...]
    natal_semantic_evidence: tuple[NatalResponseSemanticEvidence, ...]
    temporal_environment_evidence: tuple[ResponseTemporalFactEvidence, ...]
    dynamic_effects: tuple[Mapping[str, Any], ...]
    response_status: str
    response_status_reason: str
    conflicts: tuple[str, ...]
    temporal_kr_gate: TemporalKrGate
    runtime_effects_authorized: int = 0
    probability_used: bool = False
    numeric_magnitude_used: bool = False
    feedback_used: bool = False
    acquired_state_used: bool = False
    outcome_used: bool = False
    empirical_calibration_used: bool = False

    def __post_init__(self) -> None:
        if self.schema_version != RESPONSE_PROFILE_SCHEMA_VERSION:
            raise ValueError("ResponseProfile schema_version must be 0.1")
        if self.compiler_version != RESPONSE_COMPILER_VERSION:
            raise ValueError("ResponseProfile compiler_version mismatch")
        if self.domain != RESPONSE_DOMAIN:
            raise ValueError("ResponseProfile v0.1 is Career-only")
        if not self.profile_id.strip():
            raise ValueError("ResponseProfile.profile_id is required")
        if not self.natal_profile_id.strip() or not self.temporal_profile_id.strip():
            raise ValueError("ResponseProfile N/E lineage ids are required")
        if not self.knowledge_version.strip() or not self.target_label.strip():
            raise ValueError("ResponseProfile knowledge/target lineage is required")
        if set(self.consumed_layers) != REQUIRED_TEMPORAL_LAYERS:
            raise ValueError("ResponseProfile v0.1 must consume DECADE + YEAR exactly")
        if self.runtime_effects_authorized != 0:
            raise ValueError("v0.1 fail-closed profile cannot authorize runtime effects")
        if self.dynamic_effects:
            raise ValueError(
                "current locked temporal Kr has no executable Career dynamic effects"
            )
        forbidden = {
            "probability_used": self.probability_used,
            "numeric_magnitude_used": self.numeric_magnitude_used,
            "feedback_used": self.feedback_used,
            "acquired_state_used": self.acquired_state_used,
            "outcome_used": self.outcome_used,
            "empirical_calibration_used": self.empirical_calibration_used,
        }
        active = [name for name, value in forbidden.items() if value]
        if active:
            raise ValueError(
                "ResponseProfile v0.1 crossed a forbidden maturity boundary: "
                + ", ".join(active)
            )
        if self.response_status != UNKNOWN_NO_CANONICAL_TEMPORAL_RESPONSE_RULE:
            raise ValueError("v0.1 current-baseline response must remain explicit UNKNOWN")

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "profile_id": self.profile_id,
            "compiler_version": self.compiler_version,
            "domain": self.domain,
            "natal_profile_id": self.natal_profile_id,
            "temporal_profile_id": self.temporal_profile_id,
            "knowledge_version": self.knowledge_version,
            "target_label": self.target_label,
            "consumed_layers": list(self.consumed_layers),
            "ignored_environment_layers": list(self.ignored_environment_layers),
            "natal_semantic_evidence": [
                item.to_dict() for item in self.natal_semantic_evidence
            ],
            "temporal_environment_evidence": [
                item.to_dict() for item in self.temporal_environment_evidence
            ],
            "dynamic_effects": [dict(item) for item in self.dynamic_effects],
            "response_status": self.response_status,
            "response_status_reason": self.response_status_reason,
            "conflicts": list(self.conflicts),
            "temporal_kr_gate": self.temporal_kr_gate.to_dict(),
            "runtime_effects_authorized": self.runtime_effects_authorized,
            "probability_used": self.probability_used,
            "numeric_magnitude_used": self.numeric_magnitude_used,
            "feedback_used": self.feedback_used,
            "acquired_state_used": self.acquired_state_used,
            "outcome_used": self.outcome_used,
            "empirical_calibration_used": self.empirical_calibration_used,
            "maturity": {
                "response_profile_tau": "IMPLEMENTED_V0_1_FAIL_CLOSED",
                "canonical_temporal_response_content": "EMPTY_ON_ACTIVE_LOCK",
                "dynamic_response_execution": "BLOCKED_BY_CANONICAL_KR",
                "manifestation_m0": "NOT_IMPLEMENTED",
                "predictive_validity": "NOT_VALIDATED",
            },
        }


def _read_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path}: JSON root must be an object")
    return payload


def load_active_temporal_kr_gate(root: Path = ROOT) -> TemporalKrGate:
    """Verify the temporal Kr gate is actually part of the active Product lock."""

    lock_path = root / "product" / "PRODUCT_KNOWLEDGE.lock.json"
    lock = _read_json(lock_path)
    active_bundle_path = str(lock.get("active_bundle_path", "")).strip()
    active_bundle_id = str(lock.get("active_bundle_id", "")).strip()
    if not active_bundle_path or not active_bundle_id:
        raise ValueError("active Product Knowledge lock is incomplete")

    bundle = _read_json(root / active_bundle_path)
    if str(bundle.get("bundle_id", "")).strip() != active_bundle_id:
        raise ValueError("active Product Knowledge lock/bundle identity mismatch")

    components = bundle.get("components")
    if not isinstance(components, list):
        raise ValueError("active Product Knowledge bundle components are invalid")
    k_response = next(
        (
            item
            for item in components
            if isinstance(item, Mapping)
            and str(item.get("component_id", "")).strip() == "K_response"
        ),
        None,
    )
    if k_response is None:
        raise ValueError("active Product Knowledge bundle has no K_response component")

    artifacts = k_response.get("artifacts")
    if not isinstance(artifacts, list):
        raise ValueError("active K_response artifact registry is invalid")
    locked_paths = {
        str(item.get("path", "")).strip()
        for item in artifacts
        if isinstance(item, Mapping)
    }
    if CURRENT_TEMPORAL_KR_GATE_PATH not in locked_paths:
        raise ValueError("temporal Kr eligibility gate is not locked in active K_response")

    gate = _read_json(root / CURRENT_TEMPORAL_KR_GATE_PATH)
    result = TemporalKrGate(
        active_bundle_id=active_bundle_id,
        active_bundle_path=active_bundle_path,
        k_response_source_commit=str(k_response.get("source_commit", "")).strip(),
        gate_artifact_path=CURRENT_TEMPORAL_KR_GATE_PATH,
        gate_audit_id=str(gate.get("audit_id", "")).strip(),
        eligible_rule_count=int(gate.get("eligible_for_current_compiler", -1)),
        executable_pilot_emitted=bool(gate.get("executable_pilot_emitted", False)),
        production_registry_should_remain_empty=bool(
            gate.get("production_registry_should_remain_empty", False)
        ),
        decision=str(gate.get("decision", "")).strip(),
    )

    # v0.1 is intentionally bound to the audited zero-eligible baseline.  If a
    # future Knowledge promotion changes this, a new Product compiler migration
    # must explicitly review the new semantics instead of silently executing.
    if (
        result.eligible_rule_count != 0
        or result.executable_pilot_emitted
        or not result.production_registry_should_remain_empty
        or result.decision
        != "NO_ELIGIBLE_SOURCE_EXPLICIT_TEMPORAL_RULE_UNDER_CURRENT_CONTRACT"
    ):
        raise ValueError(
            "temporal Kr gate changed; explicit Product migration/review required"
        )
    return result


def _extract_natal_semantic_evidence(
    natal_evaluation: Mapping[str, Any],
    *,
    root: Path,
) -> tuple[NatalResponseSemanticEvidence, ...]:
    if str(natal_evaluation.get("schema_version", "")).strip() != "0.1":
        raise ValueError("Career natal evaluation schema_version must be 0.1")
    if (
        str(natal_evaluation.get("evaluator_version", "")).strip()
        != "PL3R_CAREER_CONDITION_EVALUATOR_V0_1"
    ):
        raise ValueError("Career natal evaluation must come from the governed v0.1 evaluator")
    scope = natal_evaluation.get("scope")
    if not isinstance(scope, Mapping):
        raise ValueError("Career natal evaluation scope is required")
    if (
        str(scope.get("domain", "")).strip() != RESPONSE_DOMAIN
        or str(scope.get("time_layer", "")).strip() != "NATAL"
        or bool(scope.get("temporal_environment_consumed", False))
    ):
        raise ValueError("Career natal evaluation scope is not the governed NATAL pilot")

    summary = natal_evaluation.get("summary")
    if not isinstance(summary, Mapping):
        raise ValueError("Career natal evaluation summary is required")
    if int(summary.get("conditions_evaluated", -1)) != 12:
        raise ValueError("Response compiler requires the exact 12-condition evaluator")
    if int(summary.get("runtime_effects_authorized", -1)) != 0:
        raise ValueError("natal evaluator may not authorize runtime response effects")
    if int(summary.get("response_profile_tau_generated", -1)) != 0:
        raise ValueError("natal evaluator must not pre-generate ResponseProfile tau")

    evaluations = natal_evaluation.get("evaluations")
    if not isinstance(evaluations, list) or len(evaluations) != 12:
        raise ValueError("Response compiler requires exactly 12 condition evaluations")

    condition_registry = _read_json(
        root / "product" / "CAREER_CONDITION_COMPILER_PILOT_v0.1.json"
    )
    compiled = condition_registry.get("compiled_conditions")
    if not isinstance(compiled, list) or len(compiled) != 12:
        raise ValueError("governed Career condition registry is invalid")
    governed_ids = {
        str(item.get("source_rule_id", "")).strip()
        for item in compiled
        if isinstance(item, Mapping)
    }
    effect_registry = _read_json(
        root / "product" / "CAREER_CONDITION_EFFECT_BINDING_PILOT_v0.1.json"
    )
    canonical_bindings_raw = effect_registry.get("bindings")
    if not isinstance(canonical_bindings_raw, list) or len(canonical_bindings_raw) != 12:
        raise ValueError("governed Career effect-binding registry is invalid")
    canonical_bindings = {
        str(item.get("source_rule_id", "")).strip(): item
        for item in canonical_bindings_raw
        if isinstance(item, Mapping)
    }
    if set(canonical_bindings) != governed_ids or len(governed_ids) != 12:
        raise ValueError("governed Career condition/effect registry IDs differ")

    out: list[NatalResponseSemanticEvidence] = []
    seen: set[str] = set()
    for row in evaluations:
        if not isinstance(row, Mapping):
            raise ValueError("Career condition evaluation row must be an object")
        rule_id = str(row.get("source_rule_id", "")).strip()
        if not rule_id or rule_id in seen:
            raise ValueError("Career condition evaluation IDs are invalid")
        seen.add(rule_id)
        if bool(row.get("runtime_effect_allowed", False)):
            raise ValueError(f"{rule_id}: natal evaluation attempted runtime authorization")
        matched = bool(row.get("matched", False))
        binding = row.get("effect_binding")
        if not matched:
            if binding is not None:
                raise ValueError(f"{rule_id}: unmatched condition cannot carry effect binding")
            continue
        if not isinstance(binding, Mapping):
            raise ValueError(f"{rule_id}: matched condition requires semantic effect binding")
        if bool(binding.get("runtime_effect_allowed", False)):
            raise ValueError(f"{rule_id}: effect binding attempted runtime authorization")
        canonical_binding = canonical_bindings.get(rule_id)
        if canonical_binding is None or dict(binding) != dict(canonical_binding):
            raise ValueError(f"{rule_id}: effect binding differs from governed registry")
        if str(binding.get("time_layer", "")).strip() != "NATAL":
            raise ValueError(f"{rule_id}: effect binding must remain NATAL")
        if (
            str(binding.get("binding_status", "")).strip()
            != "BOUND_SOURCE_PROJECTION_SEMANTIC_ONLY"
        ):
            raise ValueError(f"{rule_id}: unsupported effect binding status")
        spans = binding.get("source_span_ids")
        if not isinstance(spans, list) or not spans:
            raise ValueError(f"{rule_id}: source span provenance is required")
        out.append(
            NatalResponseSemanticEvidence(
                source_rule_id=rule_id,
                projection_domain=str(binding.get("projection_domain", "")).strip(),
                projection_target=str(binding.get("projection_target", "")).strip(),
                source_location=str(binding.get("source_location", "")).strip(),
                source_span_ids=tuple(str(item).strip() for item in spans),
                compatibility_band=str(binding.get("compatibility_band", "")).strip(),
            )
        )
    if seen != governed_ids:
        raise ValueError("Career condition evaluation IDs differ from governed registry")
    return tuple(sorted(out, key=lambda item: item.source_rule_id))


def _response_profile_id(payload: Mapping[str, Any]) -> str:
    raw = json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return "TAU-" + hashlib.sha256(raw).hexdigest()[:24]


def compile_decade_year_response_profile(
    natal_profile: NatalStateProfile,
    natal_evaluation: Mapping[str, Any],
    temporal_profile: TemporalEnvironmentProfile,
    *,
    repository_root: Path = ROOT,
) -> ResponseProfile:
    """Compile one deterministic, fail-closed Career ResponseProfile tau_t."""

    if temporal_profile.natal_profile_id != natal_profile.profile_id:
        raise ValueError("TemporalEnvironmentProfile does not belong to NatalStateProfile")
    if temporal_profile.knowledge_version != natal_profile.knowledge_version:
        raise ValueError("natal/temporal knowledge_version mismatch")

    missing = sorted(REQUIRED_TEMPORAL_LAYERS - set(temporal_profile.active_layers))
    if missing:
        raise ValueError(
            "ResponseProfile v0.1 requires temporal layer(s): " + ", ".join(missing)
        )

    # Under the currently locked Kr, any populated temporal reaction would be
    # an unauthorized execution path because the audited eligible count is zero.
    gate = load_active_temporal_kr_gate(Path(repository_root))
    if temporal_profile.reactions:
        raise ValueError(
            "active temporal Kr authorizes zero Career reaction rules; "
            "TemporalEnvironmentProfile.reactions must be empty"
        )

    natal_semantics = _extract_natal_semantic_evidence(
        natal_evaluation,
        root=Path(repository_root),
    )
    temporal_evidence = tuple(
        sorted(
            (
                ResponseTemporalFactEvidence(
                    layer=item.layer,
                    fact=item.fact,
                    provenance=item.provenance,
                )
                for item in temporal_profile.temporal_facts
                if item.layer in REQUIRED_TEMPORAL_LAYERS
            ),
            key=lambda item: (item.layer, item.fact, item.provenance),
        )
    )
    observed = {item.layer for item in temporal_evidence}
    missing_facts = sorted(REQUIRED_TEMPORAL_LAYERS - observed)
    if missing_facts:
        raise ValueError(
            "ResponseProfile v0.1 requires DECADE/YEAR temporal facts: "
            + ", ".join(missing_facts)
        )

    ignored_layers = tuple(
        sorted(set(temporal_profile.active_layers) - REQUIRED_TEMPORAL_LAYERS)
    )
    conflicts = tuple(sorted({str(item).strip() for item in temporal_profile.conflicts if str(item).strip()}))

    identity = {
        "compiler_version": RESPONSE_COMPILER_VERSION,
        "domain": RESPONSE_DOMAIN,
        "natal_profile_id": natal_profile.profile_id,
        "temporal_profile_id": temporal_profile.profile_id,
        "knowledge_version": natal_profile.knowledge_version,
        "target_label": temporal_profile.target_label,
        "consumed_layers": sorted(REQUIRED_TEMPORAL_LAYERS),
        "ignored_environment_layers": list(ignored_layers),
        "natal_semantic_evidence": [item.to_dict() for item in natal_semantics],
        "temporal_environment_evidence": [item.to_dict() for item in temporal_evidence],
        "dynamic_effects": [],
        "response_status": UNKNOWN_NO_CANONICAL_TEMPORAL_RESPONSE_RULE,
        "conflicts": list(conflicts),
        "temporal_kr_gate": gate.to_dict(),
    }
    profile_id = _response_profile_id(identity)

    return ResponseProfile(
        schema_version=RESPONSE_PROFILE_SCHEMA_VERSION,
        profile_id=profile_id,
        compiler_version=RESPONSE_COMPILER_VERSION,
        domain=RESPONSE_DOMAIN,
        natal_profile_id=natal_profile.profile_id,
        temporal_profile_id=temporal_profile.profile_id,
        knowledge_version=natal_profile.knowledge_version,
        target_label=temporal_profile.target_label,
        consumed_layers=tuple(sorted(REQUIRED_TEMPORAL_LAYERS)),
        ignored_environment_layers=ignored_layers,
        natal_semantic_evidence=natal_semantics,
        temporal_environment_evidence=temporal_evidence,
        dynamic_effects=(),
        response_status=UNKNOWN_NO_CANONICAL_TEMPORAL_RESPONSE_RULE,
        response_status_reason=(
            "Active locked K_response audit reports zero compiler-eligible canonical "
            "Career temporal-reaction rules; dynamic response remains UNKNOWN."
        ),
        conflicts=conflicts,
        temporal_kr_gate=gate,
    )
