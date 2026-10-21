"""Fail-closed Knowledge -> Product Response Semantics adapter v0.1.

The adapter preserves Knowledge-owned semantic structure while making runtime
authorization an explicit Product decision.  Semantic compatibility, relation
binding, category membership, or activation review never imply executable
effects by themselves.

Product v0.4 invariant:
- Knowledge owns source interpretation.
- Product may consume semantic records and readiness metadata.
- runtime_effect_allowed is false unless explicit execution authorization exists.
- current Career Knowledge artifacts unlock zero runtime effects.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass
import copy
import json
from pathlib import Path
from typing import Any, Mapping, Sequence

from .knowledge_bundle import require_artifact_locked


ROOT = Path(__file__).resolve().parents[2]

RESPONSE_SCHEMA_PATH = (
    ROOT / "knowledge" / "response" / "RESPONSE_SEMANTICS_SCHEMA_v0.1.json"
)
RESPONSE_PILOT_PATH = (
    ROOT / "knowledge" / "response" / "RESPONSE_SEMANTICS_PILOT_v0.1.json"
)
RESPONSE_COMPATIBILITY_PATHS = (
    ROOT / "knowledge" / "wp07c" / "CAREER_RESPONSE_COMPATIBILITY_01_v0.1.json",
    ROOT / "knowledge" / "wp07c" / "CAREER_RESPONSE_COMPATIBILITY_02_v0.1.json",
    ROOT / "knowledge" / "wp07c" / "CAREER_RESPONSE_COMPATIBILITY_03_v0.1.json",
)
RESPONSE_COMPATIBILITY_CLOSURE_PATH = (
    ROOT
    / "knowledge"
    / "wp07c"
    / "CAREER_RESPONSE_COMPATIBILITY_CLOSURE_v0.1.json"
)
RELATION_BINDING_PATH = (
    ROOT / "knowledge" / "wp07c" / "CAREER_RELATION_BINDING_132_v0.1.json"
)
CATEGORY_REVIEW_PATH = (
    ROOT / "knowledge" / "wp07c" / "CAREER_CATEGORY_OPEN_59_v0.1.json"
)
ACTIVATION_CLOSURE_PATH = (
    ROOT
    / "knowledge"
    / "wp07c"
    / "CAREER_CONTEXTUAL_ACTIVATION_CLOSURE_251_v0.16.json"
)
CAREER_ORDINAL_CONSTRAINTS_PATH = (
    ROOT / "knowledge" / "wp08" / "CAREER_ORDINAL_CONSTRAINTS_v0.1.json"
)
CAREER_ORDINAL_RULE_LINKS_PATH = (
    ROOT / "knowledge" / "wp08" / "CAREER_ORDINAL_RULE_LINKS_v0.1.json"
)
CAREER_ORDINAL_BLOCKER_IMPACT_PATH = (
    ROOT / "knowledge" / "wp08" / "CAREER_ORDINAL_BLOCKER_IMPACT_v0.1.json"
)
CAREER_SEMANTIC_NORMALIZATION_PATH = (
    ROOT / "knowledge" / "wp08" / "CAREER_SEMANTIC_NORMALIZATION_36_v0.2.json"
)
CAREER_COMPILER_READINESS_CENSUS_PATH = (
    ROOT / "knowledge" / "wp08" / "CAREER_COMPILER_READINESS_CENSUS_26_v0.1.json"
)
CAREER_DEPENDENCY_IR_PATH = (
    ROOT / "knowledge" / "wp08" / "CAREER_DEPENDENCY_IR_3_v0.1.json"
)
CAREER_DIRECT_CONDITION_IR_PATH = (
    ROOT / "knowledge" / "wp08" / "CAREER_DIRECT_CONDITION_IR_9_v0.1.json"
)

KNOWLEDGE_EXECUTION_STATUSES = frozenset(
    {"LEXICAL_ONLY", "STRUCTURAL_ONLY", "SAFE_SYMBOLIC", "BLOCKED"}
)
PRODUCT_ALLOWED_USES = frozenset({"SEMANTIC_ONLY", "EXECUTABLE", "BLOCKED"})

CAREER_ADAPTER_STATUS_BY_READINESS = {
    "SOURCE_UNDERDETERMINED": "BLOCKED_SOURCE_UNDERDETERMINED",
    "DEPENDENCY_COMPILER_GATED": "BLOCKED_DEPENDENCY_COMPILER",
    "NORMALIZATION_DEFERRED": "BLOCKED_NORMALIZATION",
    "STRUCTURED_PATTERN_COMPILER_GATED": "BLOCKED_STRUCTURED_PATTERN_COMPILER",
    "MULTI_CLASS_BLOCKED": "BLOCKED_MULTIPLE",
}

CAREER_LOCAL_READY_STATUS_BY_COMPILER_BAND = {
    "DEPENDENCY_CONDITION_IR_READY": (
        "KNOWLEDGE_CONDITION_IR_READY_PENDING_PRODUCT_COMPILATION"
    ),
    "DIRECT_CONDITION_IR_READY": (
        "KNOWLEDGE_CONDITION_IR_READY_PENDING_PRODUCT_COMPILATION"
    ),
    "DEPENDENCY_EFFECTIVE_UNDERDETERMINED": (
        "LOCAL_STRUCTURE_NOT_CONDITION_IR_READY"
    ),
    "DIRECT_RELATION_OR_COMPOSITION_DEFERRED": (
        "LOCAL_STRUCTURE_NOT_CONDITION_IR_READY"
    ),
}

CAREER_ADAPTER_STATUSES = frozenset(
    {
        *CAREER_ADAPTER_STATUS_BY_READINESS.values(),
        *CAREER_LOCAL_READY_STATUS_BY_COMPILER_BAND.values(),
    }
)

FORBIDDEN_NUMERIC_FIELDS = frozenset(
    {
        "probability",
        "posterior",
        "learned_weight",
        "numeric_gain",
        "effect_weight",
        "confidence_score",
        "reward",
    }
)


def _read_json(path: Path) -> Any:
    require_artifact_locked(ROOT, path, "K_response")
    return json.loads(path.read_text(encoding="utf-8"))


def _deep(value: Any) -> Any:
    return copy.deepcopy(value)


def _tuple_of_objects(value: Any, path: str) -> tuple[dict[str, Any], ...]:
    if not isinstance(value, list):
        raise ValueError(f"{path} must be an array")
    out: list[dict[str, Any]] = []
    for index, item in enumerate(value):
        if not isinstance(item, dict):
            raise ValueError(f"{path}[{index}] must be an object")
        out.append(_deep(item))
    return tuple(out)


def _required_text(value: Any, path: str) -> str:
    text = str(value or "").strip()
    if not text:
        raise ValueError(f"{path} is required")
    return text


def _assert_no_forbidden_numeric_fields(value: Any, path: str = "root") -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            if key in FORBIDDEN_NUMERIC_FIELDS:
                raise ValueError(f"{path}.{key}: numeric/probability field is forbidden")
            _assert_no_forbidden_numeric_fields(child, f"{path}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            _assert_no_forbidden_numeric_fields(child, f"{path}[{index}]")


@dataclass(frozen=True)
class ResponseSemanticEnvelope:
    schema_version: str
    record_id: str
    term: str
    semantic_role: str
    members: tuple[dict[str, Any], ...]
    scope: dict[str, Any]
    activation: dict[str, Any]
    relation_constraints: tuple[dict[str, Any], ...]
    interaction: dict[str, Any]
    ordinal_constraints: tuple[dict[str, Any], ...]
    effect_targets: tuple[dict[str, Any], ...]
    provenance: tuple[dict[str, Any], ...]
    epistemic_status: str
    knowledge_execution_status: str
    allowed_use: str
    runtime_effect_allowed: bool
    authorization_ref: str | None
    blockers: tuple[str, ...]

    def __post_init__(self) -> None:
        if self.schema_version != "0.1":
            raise ValueError("ResponseSemanticEnvelope schema_version must be 0.1")
        if self.knowledge_execution_status not in KNOWLEDGE_EXECUTION_STATUSES:
            raise ValueError(
                f"{self.record_id}: unsupported Knowledge execution status"
            )
        if self.allowed_use not in PRODUCT_ALLOWED_USES:
            raise ValueError(f"{self.record_id}: unsupported Product allowed_use")
        if self.runtime_effect_allowed:
            if self.allowed_use != "EXECUTABLE":
                raise ValueError(
                    f"{self.record_id}: runtime effect requires EXECUTABLE allowed_use"
                )
            if not self.authorization_ref:
                raise ValueError(
                    f"{self.record_id}: runtime effect requires explicit authorization"
                )
            if self.knowledge_execution_status != "SAFE_SYMBOLIC":
                raise ValueError(
                    f"{self.record_id}: only SAFE_SYMBOLIC may be explicitly authorized"
                )
            if self.blockers:
                raise ValueError(
                    f"{self.record_id}: authorized runtime effect cannot retain blockers"
                )
        elif self.allowed_use == "EXECUTABLE":
            raise ValueError(
                f"{self.record_id}: EXECUTABLE allowed_use requires runtime authorization"
            )

    def semantic_payload(self) -> dict[str, Any]:
        """Return the Knowledge semantic fields without Product-derived metadata."""
        return {
            "schema_version": self.schema_version,
            "record_id": self.record_id,
            "term": self.term,
            "semantic_role": self.semantic_role,
            "members": [_deep(item) for item in self.members],
            "scope": _deep(self.scope),
            "activation": _deep(self.activation),
            "relation_constraints": [
                _deep(item) for item in self.relation_constraints
            ],
            "interaction": _deep(self.interaction),
            "ordinal_constraints": [
                _deep(item) for item in self.ordinal_constraints
            ],
            "effect_targets": [_deep(item) for item in self.effect_targets],
            "provenance": [_deep(item) for item in self.provenance],
            "epistemic_status": self.epistemic_status,
            "execution_status": self.knowledge_execution_status,
        }

    def to_dict(self) -> dict[str, Any]:
        payload = self.semantic_payload()
        payload.update(
            {
                "allowed_use": self.allowed_use,
                "runtime_effect_allowed": self.runtime_effect_allowed,
                "authorization_ref": self.authorization_ref,
                "blockers": list(self.blockers),
            }
        )
        return payload


@dataclass(frozen=True)
class CareerResponseDecision:
    source_rule_id: str
    compatibility_band: str
    knowledge_readiness_class: str
    compiler_readiness_band: str | None
    knowledge_condition_ir_ready: bool
    condition_ir_artifact: str | None
    compiler_readiness_blockers: tuple[str, ...]
    activation_status: str
    adapter_status: str
    blockers: tuple[str, ...]
    antecedent_mode: str
    antecedent_rule_ids: tuple[str, ...]
    relation_binding_dispositions: tuple[str, ...]
    category_membership_statuses: tuple[str, ...]
    condition_compiled: bool
    knowledge_execution_unlocked: bool
    runtime_effect_allowed: bool
    semantic_refs: tuple[str, ...]

    def __post_init__(self) -> None:
        if self.adapter_status not in CAREER_ADAPTER_STATUSES:
            raise ValueError(
                f"{self.source_rule_id}: unsupported adapter status {self.adapter_status}"
            )
        if self.runtime_effect_allowed:
            raise ValueError(
                f"{self.source_rule_id}: Career v0.1 may not authorize runtime effects"
            )
        if self.condition_compiled or self.knowledge_execution_unlocked:
            raise ValueError(
                f"{self.source_rule_id}: unexpected Knowledge execution unlock drift"
            )

    def to_dict(self) -> dict[str, Any]:
        return {
            "source_rule_id": self.source_rule_id,
            "compatibility_band": self.compatibility_band,
            "knowledge_readiness_class": self.knowledge_readiness_class,
            "compiler_readiness_band": self.compiler_readiness_band,
            "knowledge_condition_ir_ready": self.knowledge_condition_ir_ready,
            "condition_ir_artifact": self.condition_ir_artifact,
            "compiler_readiness_blockers": list(
                self.compiler_readiness_blockers
            ),
            "activation_status": self.activation_status,
            "adapter_status": self.adapter_status,
            "blockers": list(self.blockers),
            "antecedent_mode": self.antecedent_mode,
            "antecedent_rule_ids": list(self.antecedent_rule_ids),
            "relation_binding_dispositions": list(
                self.relation_binding_dispositions
            ),
            "category_membership_statuses": list(
                self.category_membership_statuses
            ),
            "condition_compiled": self.condition_compiled,
            "knowledge_execution_unlocked": self.knowledge_execution_unlocked,
            "runtime_effect_allowed": self.runtime_effect_allowed,
            "semantic_refs": list(self.semantic_refs),
        }


def _scope_blockers(
    record_scope: Mapping[str, Any],
    requested_scope: Mapping[str, Any] | None,
) -> tuple[str, ...]:
    if requested_scope is None:
        return ()

    blockers: list[str] = []
    for key in ("domain", "time_layer", "star_system", "palace"):
        expected = record_scope.get(key)
        if expected is None:
            continue
        actual = requested_scope.get(key)
        if actual != expected:
            blockers.append(f"SCOPE_MISMATCH:{key}")
    return tuple(blockers)


def adapt_response_semantics_record(
    record: Mapping[str, Any],
    *,
    authorization_ref: str | None = None,
    requested_scope: Mapping[str, Any] | None = None,
    application_term: str | None = None,
) -> ResponseSemanticEnvelope:
    """Adapt one Knowledge ResponseSemanticsRecord without changing semantics.

    SAFE_SYMBOLIC is necessary but not sufficient for runtime execution.
    Explicit authorization, explicit activation, matching local scope, and
    exact named-composite term application are additionally required.
    """

    required = {
        "schema_version",
        "record_id",
        "term",
        "semantic_role",
        "members",
        "scope",
        "activation",
        "relation_constraints",
        "interaction",
        "ordinal_constraints",
        "effect_targets",
        "provenance",
        "epistemic_status",
        "execution_status",
    }
    unknown = set(record) - required
    missing = required - set(record)
    if missing:
        raise ValueError(f"response record missing fields: {sorted(missing)}")
    if unknown:
        raise ValueError(f"response record has unsupported fields: {sorted(unknown)}")

    _assert_no_forbidden_numeric_fields(record)

    execution_status = _required_text(
        record.get("execution_status"), "response.execution_status"
    )
    if execution_status not in KNOWLEDGE_EXECUTION_STATUSES:
        raise ValueError(f"unsupported execution_status: {execution_status}")

    scope = record.get("scope")
    activation = record.get("activation")
    interaction = record.get("interaction")
    if not isinstance(scope, dict):
        raise ValueError("response.scope must be an object")
    if not isinstance(activation, dict):
        raise ValueError("response.activation must be an object")
    if not isinstance(interaction, dict):
        raise ValueError("response.interaction must be an object")

    record_id = _required_text(record.get("record_id"), "response.record_id")
    term = _required_text(record.get("term"), "response.term")
    semantic_role = _required_text(
        record.get("semantic_role"), "response.semantic_role"
    )

    blockers: list[str] = []
    allowed_use = "SEMANTIC_ONLY"

    if execution_status == "LEXICAL_ONLY":
        blockers.append("KNOWLEDGE_EXECUTION_STATUS:LEXICAL_ONLY")
    elif execution_status == "STRUCTURAL_ONLY":
        blockers.append("KNOWLEDGE_EXECUTION_STATUS:STRUCTURAL_ONLY")
    elif execution_status == "BLOCKED":
        blockers.append("KNOWLEDGE_EXECUTION_STATUS:BLOCKED")
        allowed_use = "BLOCKED"
    elif execution_status == "SAFE_SYMBOLIC":
        blockers.append("EXPLICIT_EXECUTION_AUTHORIZATION_REQUIRED")

    blockers.extend(_scope_blockers(scope, requested_scope))

    if activation.get("mode") == "UNSPECIFIED":
        blockers.append("ACTIVATION_UNSPECIFIED_NO_DEFAULT")

    if (
        semantic_role == "NAMED_COMPOSITE"
        and application_term is not None
        and application_term != term
    ):
        blockers.append("NAMED_COMPOSITE_NOT_GENERIC_SHORTHAND")

    runtime_effect_allowed = False
    normalized_auth = (
        str(authorization_ref).strip() if authorization_ref is not None else None
    )
    if normalized_auth == "":
        normalized_auth = None

    if normalized_auth is not None:
        blockers = [
            item
            for item in blockers
            if item != "EXPLICIT_EXECUTION_AUTHORIZATION_REQUIRED"
        ]
        if execution_status != "SAFE_SYMBOLIC":
            blockers.append("AUTHORIZATION_CANNOT_OVERRIDE_KNOWLEDGE_STATUS")
        if activation.get("mode") == "UNSPECIFIED":
            blockers.append("AUTHORIZATION_CANNOT_INVENT_ACTIVATION")

        local_scope_bound = any(
            scope.get(key) is not None
            for key in ("domain", "time_layer", "star_system", "palace")
        )
        if local_scope_bound and requested_scope is None:
            blockers.append("LOCAL_SCOPE_BINDING_REQUIRED")
        if any(item.startswith("SCOPE_MISMATCH:") for item in blockers):
            blockers.append("AUTHORIZATION_CANNOT_OVERRIDE_SCOPE")

        if semantic_role == "NAMED_COMPOSITE" and application_term is None:
            blockers.append("NAMED_COMPOSITE_APPLICATION_TERM_REQUIRED")
        if "NAMED_COMPOSITE_NOT_GENERIC_SHORTHAND" in blockers:
            blockers.append("AUTHORIZATION_CANNOT_GLOBALIZE_COMPOSITE")

        fatal = {
            "AUTHORIZATION_CANNOT_OVERRIDE_KNOWLEDGE_STATUS",
            "AUTHORIZATION_CANNOT_INVENT_ACTIVATION",
            "LOCAL_SCOPE_BINDING_REQUIRED",
            "AUTHORIZATION_CANNOT_OVERRIDE_SCOPE",
            "NAMED_COMPOSITE_APPLICATION_TERM_REQUIRED",
            "AUTHORIZATION_CANNOT_GLOBALIZE_COMPOSITE",
        }
        if not fatal.intersection(blockers) and not blockers:
            allowed_use = "EXECUTABLE"
            runtime_effect_allowed = True

    return ResponseSemanticEnvelope(
        schema_version=_required_text(
            record.get("schema_version"), "response.schema_version"
        ),
        record_id=record_id,
        term=term,
        semantic_role=semantic_role,
        members=_tuple_of_objects(record.get("members"), "response.members"),
        scope=_deep(scope),
        activation=_deep(activation),
        relation_constraints=_tuple_of_objects(
            record.get("relation_constraints"), "response.relation_constraints"
        ),
        interaction=_deep(interaction),
        ordinal_constraints=_tuple_of_objects(
            record.get("ordinal_constraints"), "response.ordinal_constraints"
        ),
        effect_targets=_tuple_of_objects(
            record.get("effect_targets"), "response.effect_targets"
        ),
        provenance=_tuple_of_objects(
            record.get("provenance"), "response.provenance"
        ),
        epistemic_status=_required_text(
            record.get("epistemic_status"), "response.epistemic_status"
        ),
        knowledge_execution_status=execution_status,
        allowed_use=allowed_use,
        runtime_effect_allowed=runtime_effect_allowed,
        authorization_ref=normalized_auth if runtime_effect_allowed else None,
        blockers=tuple(dict.fromkeys(blockers)),
    )


def load_response_pilot_records(
    path: Path = RESPONSE_PILOT_PATH,
) -> tuple[dict[str, Any], ...]:
    payload = _read_json(path)
    if payload.get("schema_version") != "0.1":
        raise ValueError("response pilot schema_version must be 0.1")
    raw = payload.get("records")
    if not isinstance(raw, list):
        raise ValueError("response pilot records must be an array")
    records = tuple(_deep(item) for item in raw)
    ids = [item.get("record_id") for item in records]
    if len(ids) != len(set(ids)):
        raise ValueError("response pilot record_id values must be unique")
    return records


def adapt_response_pilot_registry() -> tuple[ResponseSemanticEnvelope, ...]:
    return tuple(
        adapt_response_semantics_record(record)
        for record in load_response_pilot_records()
    )


def load_career_compatibility_records(
    paths: Sequence[Path] = RESPONSE_COMPATIBILITY_PATHS,
) -> tuple[dict[str, Any], ...]:
    records: list[dict[str, Any]] = []
    for path in paths:
        payload = _read_json(path)
        raw = payload.get("records")
        if not isinstance(raw, list):
            raise ValueError(f"{path.name}: records must be an array")
        records.extend(_deep(item) for item in raw)

    ids = [item.get("source_rule_id") for item in records]
    if len(records) != 251:
        raise ValueError(f"expected 251 Career compatibility rows, got {len(records)}")
    if len(set(ids)) != 251:
        raise ValueError("Career compatibility source_rule_id values must be unique")
    return tuple(records)


def load_career_ordinal_constraints(
    path: Path = CAREER_ORDINAL_CONSTRAINTS_PATH,
) -> tuple[dict[str, Any], ...]:
    payload = _read_json(path)
    if payload.get("schema_version") != "0.1":
        raise ValueError("Career ordinal registry schema_version must be 0.1")
    raw = payload.get("constraints")
    if not isinstance(raw, list):
        raise ValueError("Career ordinal constraints must be an array")
    constraints = tuple(_deep(item) for item in raw)
    ids = [item.get("constraint_id") for item in constraints]
    if len(constraints) != 130:
        raise ValueError(
            f"expected 130 Career ordinal constraints, got {len(constraints)}"
        )
    if len(set(ids)) != len(ids):
        raise ValueError("Career ordinal constraint_id values must be unique")

    for item in constraints:
        if item.get("product_execution_unlocked") is not False:
            raise ValueError(
                f"{item.get('constraint_id')}: ordinal execution unlock drift"
            )
        if item.get("transitive_closure_allowed") is not False:
            raise ValueError(
                f"{item.get('constraint_id')}: transitive ordinal closure is not allowed"
            )
        for key in ("numeric_gain", "numeric_value", "probability", "numeric_threshold"):
            if key in item and item.get(key) is not None:
                raise ValueError(
                    f"{item.get('constraint_id')}: {key} must remain null"
                )
    return constraints


def load_career_ordinal_rule_links(
    path: Path = CAREER_ORDINAL_RULE_LINKS_PATH,
) -> Mapping[str, Any]:
    payload = _read_json(path)
    if payload.get("schema_version") != "0.1":
        raise ValueError("Career ordinal rule-link schema_version must be 0.1")
    raw = payload.get("records")
    if not isinstance(raw, list):
        raise ValueError("Career ordinal rule-link records must be an array")
    if len(raw) != 130:
        raise ValueError(
            f"expected 130 Career ordinal rule links, got {len(raw)}"
        )
    ids = [item.get("constraint_id") for item in raw]
    if len(set(ids)) != len(ids):
        raise ValueError("Career ordinal rule-link constraint_id values must be unique")

    allowed_dispositions = {
        "DIRECT_ATOMIC_RULE",
        "MULTI_RULE_SHARED_SOURCE_SENTENCE",
        "METHODOLOGY_OR_CONTEXT_ONLY",
    }
    for item in raw:
        constraint_id = _required_text(
            item.get("constraint_id"), "ordinal_rule_link.constraint_id"
        )
        disposition = _required_text(
            item.get("disposition"), f"{constraint_id}.disposition"
        )
        if disposition not in allowed_dispositions:
            raise ValueError(
                f"{constraint_id}: unsupported ordinal rule-link disposition"
            )
        linked_rule_ids = item.get("linked_rule_ids")
        if not isinstance(linked_rule_ids, list) or not linked_rule_ids:
            raise ValueError(
                f"{constraint_id}: ordinal rule link requires linked_rule_ids"
            )

    return payload


def load_career_ordinal_blocker_impact(
    path: Path = CAREER_ORDINAL_BLOCKER_IMPACT_PATH,
) -> Mapping[str, Any]:
    payload = _read_json(path)
    if payload.get("schema_version") != "0.1":
        raise ValueError("Career ordinal blocker-impact schema_version must be 0.1")
    raw = payload.get("records")
    if not isinstance(raw, list):
        raise ValueError("Career ordinal blocker-impact records must be an array")
    if len(raw) != 130:
        raise ValueError(
            f"expected 130 Career ordinal blocker-impact rows, got {len(raw)}"
        )
    ids = [item.get("constraint_id") for item in raw]
    if len(set(ids)) != len(ids):
        raise ValueError(
            "Career ordinal blocker-impact constraint_id values must be unique"
        )

    allowed_impacts = {
        "NO_BLOCKER_REDUCTION",
        "QUALITATIVE_REFINEMENT_ONLY",
    }
    for item in raw:
        constraint_id = _required_text(
            item.get("constraint_id"), "ordinal_blocker_impact.constraint_id"
        )
        impact = _required_text(
            item.get("blocker_impact"), f"{constraint_id}.blocker_impact"
        )
        if impact not in allowed_impacts:
            raise ValueError(
                f"{constraint_id}: ordinal evidence unexpectedly resolves a blocker"
            )
        if item.get("execution_unlocked") is not False:
            raise ValueError(
                f"{constraint_id}: ordinal blocker impact unlock drift"
            )
        resolved = item.get("resolved_blockers")
        if not isinstance(resolved, list) or resolved:
            raise ValueError(
                f"{constraint_id}: ordinal evidence may not resolve blockers in v0.1"
            )

    summary = payload.get("summary")
    if not isinstance(summary, dict):
        raise ValueError("Career ordinal blocker-impact summary must be an object")
    if int(summary.get("blockers_resolved_by_ordinal_evidence", -1)) != 0:
        raise ValueError("ordinal blocker-impact summary reports blocker resolution")
    if int(summary.get("execution_unlocked", -1)) != 0:
        raise ValueError("ordinal blocker-impact summary reports execution unlock")

    return payload


def validate_career_ordinal_cross_artifacts() -> None:
    constraints = load_career_ordinal_constraints()
    links = load_career_ordinal_rule_links()
    impact = load_career_ordinal_blocker_impact()

    constraint_ids = {item["constraint_id"] for item in constraints}
    link_ids = {item["constraint_id"] for item in links["records"]}
    impact_ids = {item["constraint_id"] for item in impact["records"]}

    if constraint_ids != link_ids or constraint_ids != impact_ids:
        raise ValueError(
            "Career ordinal constraint/link/impact artifacts are not one-to-one"
        )


def load_career_semantic_normalization(
    path: Path = CAREER_SEMANTIC_NORMALIZATION_PATH,
) -> Mapping[str, Any]:
    payload = _read_json(path)
    if payload.get("schema_version") != "0.2":
        raise ValueError("Career semantic-normalization schema_version must be 0.2")
    raw = payload.get("records")
    if not isinstance(raw, list) or len(raw) != 36:
        raise ValueError("Career semantic-normalization artifact must contain 36 records")
    ids = [item.get("source_rule_id") for item in raw]
    if len(set(ids)) != 36:
        raise ValueError(
            "Career semantic-normalization source_rule_id values must be unique"
        )

    for item in raw:
        rule_id = _required_text(
            item.get("source_rule_id"),
            "semantic_normalization.source_rule_id",
        )
        if item.get("condition_compiled") is not False:
            raise ValueError(f"{rule_id}: normalization may not compile conditions")
        if item.get("execution_unlocked") is not False:
            raise ValueError(f"{rule_id}: normalization may not unlock execution")
        after = item.get("blockers_after")
        if not isinstance(after, list):
            raise ValueError(f"{rule_id}: blockers_after must be an array")
        if "SEMANTIC_NORMALIZATION_OR_QUANTIFIER_UNSPECIFIED" in after:
            raise ValueError(
                f"{rule_id}: generic normalization blocker should be refined"
            )

    summary = payload.get("summary")
    if not isinstance(summary, dict):
        raise ValueError("Career semantic-normalization summary must be an object")
    if int(summary.get("semantic_normalization_blockers_before", -1)) != 36:
        raise ValueError("semantic-normalization before-count drift")
    if int(summary.get("semantic_normalization_blockers_after", -1)) != 0:
        raise ValueError("generic semantic-normalization blocker remains")
    if int(summary.get("conditions_compiled", -1)) != 0:
        raise ValueError("semantic normalization unexpectedly compiled conditions")
    if int(summary.get("execution_unlocked", -1)) != 0:
        raise ValueError("semantic normalization unexpectedly unlocked execution")

    return payload


def load_activation_closure(
    path: Path = ACTIVATION_CLOSURE_PATH,
) -> Mapping[str, Any]:
    payload = _read_json(path)
    records = payload.get("records")
    if not isinstance(records, list) or len(records) != 251:
        raise ValueError("activation closure must contain exactly 251 records")
    ids = [item.get("source_rule_id") for item in records]
    if len(set(ids)) != 251:
        raise ValueError("activation closure source_rule_id values must be unique")
    return payload


def load_career_compiler_readiness_census(
    path: Path = CAREER_COMPILER_READINESS_CENSUS_PATH,
) -> Mapping[str, Any]:
    payload = _read_json(path)
    if payload.get("schema_version") != "0.1":
        raise ValueError("Career compiler-readiness census schema_version must be 0.1")
    raw = payload.get("records")
    if not isinstance(raw, list) or len(raw) != 26:
        raise ValueError("Career compiler-readiness census must contain 26 records")
    ids = [item.get("source_rule_id") for item in raw]
    if len(set(ids)) != 26:
        raise ValueError("Career compiler-readiness source_rule_id values must be unique")
    summary = payload.get("summary")
    if not isinstance(summary, dict):
        raise ValueError("Career compiler-readiness summary must be an object")
    expected_bands = {
        "DEPENDENCY_EFFECTIVE_UNDERDETERMINED": 11,
        "DEPENDENCY_CONDITION_IR_READY": 3,
        "DIRECT_CONDITION_IR_READY": 9,
        "DIRECT_RELATION_OR_COMPOSITION_DEFERRED": 3,
    }
    if summary.get("band_counts") != expected_bands:
        raise ValueError("Career compiler-readiness band census drift")
    if int(summary.get("total_knowledge_condition_ir_ready", -1)) != 12:
        raise ValueError("Career condition-IR-ready count drift")
    if int(summary.get("not_condition_ir_ready_despite_local_structure_ready", -1)) != 14:
        raise ValueError("Career local-ready/non-condition-IR count drift")
    if int(summary.get("conditions_compiled", -1)) != 0:
        raise ValueError("Career census unexpectedly reports Product compilation")
    if int(summary.get("execution_unlocked", -1)) != 0:
        raise ValueError("Career census unexpectedly reports execution unlock")
    return payload


def load_career_dependency_ir(
    path: Path = CAREER_DEPENDENCY_IR_PATH,
) -> Mapping[str, Any]:
    payload = _read_json(path)
    raw = payload.get("records")
    if payload.get("schema_version") != "0.1" or not isinstance(raw, list):
        raise ValueError("Career dependency IR artifact is malformed")
    if len(raw) != 3:
        raise ValueError("Career dependency IR must contain exactly 3 records")
    if any(item.get("product_condition_compiled") is not False for item in raw):
        raise ValueError("Career dependency IR unexpectedly compiled a Product condition")
    if any(item.get("runtime_authorized") is not False for item in raw):
        raise ValueError("Career dependency IR unexpectedly authorizes runtime")
    return payload


def load_career_direct_condition_ir(
    path: Path = CAREER_DIRECT_CONDITION_IR_PATH,
) -> Mapping[str, Any]:
    payload = _read_json(path)
    raw = payload.get("records")
    if payload.get("schema_version") != "0.1" or not isinstance(raw, list):
        raise ValueError("Career direct condition IR artifact is malformed")
    if len(raw) != 9:
        raise ValueError("Career direct condition IR must contain exactly 9 records")
    if any(item.get("product_condition_compiled") is not False for item in raw):
        raise ValueError("Career direct condition IR unexpectedly compiled a Product condition")
    if any(item.get("runtime_authorized") is not False for item in raw):
        raise ValueError("Career direct condition IR unexpectedly authorizes runtime")
    return payload


def validate_career_compiler_readiness_cross_artifacts() -> None:
    census = load_career_compiler_readiness_census()
    dependency = load_career_dependency_ir()
    direct = load_career_direct_condition_ir()

    census_ready = {
        item["source_rule_id"]
        for item in census["records"]
        if item["knowledge_condition_ir_ready"] is True
    }
    dependency_ids = {item["child_rule_id"] for item in dependency["records"]}
    direct_ids = {item["source_rule_id"] for item in direct["records"]}
    if census_ready != dependency_ids | direct_ids:
        raise ValueError("Career census/condition-IR ready sets do not match")
    if dependency_ids & direct_ids:
        raise ValueError("Career dependency/direct condition-IR sets overlap")

    direct_by_id = {
        item["source_rule_id"]: item for item in direct["records"]
    }
    for item in dependency["records"]:
        parent_id = item["parent_rule_id"]
        if parent_id not in direct_by_id:
            raise ValueError(
                f"{item['child_rule_id']}: dependency parent lacks direct condition IR"
            )
        if item.get("condition_reference") != f"RULE_CONDITION({parent_id})":
            raise ValueError(
                f"{item['child_rule_id']}: dependency condition-reference drift"
            )


def _index_records(
    records: Sequence[Mapping[str, Any]],
    *,
    key: str = "source_rule_id",
) -> dict[str, list[Mapping[str, Any]]]:
    out: dict[str, list[Mapping[str, Any]]] = defaultdict(list)
    for item in records:
        value = _required_text(item.get(key), key)
        out[value].append(item)
    return dict(out)


def build_career_response_decisions() -> tuple[CareerResponseDecision, ...]:
    compatibility = load_career_compatibility_records()
    activation_payload = load_activation_closure()
    activation_records = activation_payload["records"]
    compiler_payload = load_career_compiler_readiness_census()
    compiler_records = compiler_payload["records"]
    validate_career_compiler_readiness_cross_artifacts()

    relation_payload = _read_json(RELATION_BINDING_PATH)
    category_payload = _read_json(CATEGORY_REVIEW_PATH)
    relation_records = relation_payload.get("records")
    category_records = category_payload.get("records")
    if not isinstance(relation_records, list):
        raise ValueError("relation binding records must be an array")
    if not isinstance(category_records, list):
        raise ValueError("category review records must be an array")

    activation_by_id = {
        item["source_rule_id"]: item for item in activation_records
    }
    compiler_by_id = {
        item["source_rule_id"]: item for item in compiler_records
    }
    relation_by_id = _index_records(relation_records)
    category_by_id = _index_records(category_records)

    compatibility_ids = {item["source_rule_id"] for item in compatibility}
    activation_ids = set(activation_by_id)
    if compatibility_ids != activation_ids:
        missing_activation = sorted(compatibility_ids - activation_ids)
        missing_compat = sorted(activation_ids - compatibility_ids)
        raise ValueError(
            "Career compatibility/activation join mismatch: "
            f"missing_activation={missing_activation}, "
            f"missing_compatibility={missing_compat}"
        )

    decisions: list[CareerResponseDecision] = []
    for compat in sorted(compatibility, key=lambda item: item["source_rule_id"]):
        rule_id = compat["source_rule_id"]
        activation = activation_by_id[rule_id]
        readiness_class = _required_text(
            activation.get("readiness_class"),
            f"{rule_id}.readiness_class",
        )
        if (
            readiness_class != "LOCAL_STRUCTURE_READY"
            and readiness_class not in CAREER_ADAPTER_STATUS_BY_READINESS
        ):
            raise ValueError(
                f"{rule_id}: unsupported Knowledge readiness class {readiness_class}"
            )

        compiler_row = compiler_by_id.get(rule_id)
        if readiness_class == "LOCAL_STRUCTURE_READY":
            if compiler_row is None:
                raise ValueError(
                    f"{rule_id}: LOCAL_STRUCTURE_READY lacks compiler-readiness census row"
                )
            compiler_band = _required_text(
                compiler_row.get("compiler_readiness_band"),
                f"{rule_id}.compiler_readiness_band",
            )
            if compiler_band not in CAREER_LOCAL_READY_STATUS_BY_COMPILER_BAND:
                raise ValueError(
                    f"{rule_id}: unsupported compiler-readiness band {compiler_band}"
                )
            condition_ir_ready = bool(
                compiler_row.get("knowledge_condition_ir_ready", False)
            )
            condition_ir_artifact = compiler_row.get("condition_ir_artifact")
            if condition_ir_ready != (
                compiler_band
                in {
                    "DEPENDENCY_CONDITION_IR_READY",
                    "DIRECT_CONDITION_IR_READY",
                }
            ):
                raise ValueError(
                    f"{rule_id}: compiler band/condition-IR readiness mismatch"
                )
            if condition_ir_ready and not str(condition_ir_artifact or "").strip():
                raise ValueError(
                    f"{rule_id}: condition-IR-ready row lacks artifact reference"
                )
            compiler_blockers = [
                f"EFFECTIVE_PARENT_BLOCKER:{value}"
                for value in compiler_row.get("effective_parent_blockers", [])
            ]
            if not condition_ir_ready:
                compiler_blockers.append(
                    f"CONDITION_IR_NOT_READY:{compiler_band}"
                )
            adapter_status = CAREER_LOCAL_READY_STATUS_BY_COMPILER_BAND[
                compiler_band
            ]
        else:
            if compiler_row is not None:
                raise ValueError(
                    f"{rule_id}: compiler census must contain only LOCAL_STRUCTURE_READY rows"
                )
            compiler_band = None
            condition_ir_ready = False
            condition_ir_artifact = None
            compiler_blockers = []
            adapter_status = CAREER_ADAPTER_STATUS_BY_READINESS[
                readiness_class
            ]

        condition_compiled = bool(compat.get("condition_compiled", False))
        execution_unlocked = bool(compat.get("execution_unlocked", False))
        if condition_compiled or execution_unlocked:
            raise ValueError(
                f"{rule_id}: Knowledge execution drift requires a new reviewed Product contract"
            )

        relation_dispositions = tuple(
            sorted(
                {
                    _required_text(
                        row.get("row_binding_disposition"),
                        f"{rule_id}.row_binding_disposition",
                    )
                    for row in relation_by_id.get(rule_id, [])
                }
            )
        )
        category_statuses = tuple(
            sorted(
                {
                    _required_text(
                        row.get("membership_status"),
                        f"{rule_id}.membership_status",
                    )
                    for row in category_by_id.get(rule_id, [])
                }
            )
        )

        semantic_refs = [
            f"KNOWLEDGE:CAREER_RESPONSE_COMPATIBILITY:{rule_id}",
            f"KNOWLEDGE:CAREER_CONTEXTUAL_ACTIVATION:{rule_id}",
        ]
        if relation_dispositions:
            semantic_refs.append(f"KNOWLEDGE:CAREER_RELATION_BINDING:{rule_id}")
        if category_statuses:
            semantic_refs.append(f"KNOWLEDGE:CAREER_CATEGORY_REVIEW:{rule_id}")
        if compiler_row is not None:
            semantic_refs.append(
                f"KNOWLEDGE:CAREER_COMPILER_READINESS:{rule_id}"
            )
        if condition_ir_ready:
            if compiler_band == "DEPENDENCY_CONDITION_IR_READY":
                semantic_refs.append(
                    f"KNOWLEDGE:CAREER_DEPENDENCY_IR:{rule_id}"
                )
            else:
                semantic_refs.append(
                    f"KNOWLEDGE:CAREER_DIRECT_CONDITION_IR:{rule_id}"
                )

        decisions.append(
            CareerResponseDecision(
                source_rule_id=rule_id,
                compatibility_band=_required_text(
                    compat.get("compatibility_band"),
                    f"{rule_id}.compatibility_band",
                ),
                knowledge_readiness_class=readiness_class,
                compiler_readiness_band=compiler_band,
                knowledge_condition_ir_ready=condition_ir_ready,
                condition_ir_artifact=(
                    str(condition_ir_artifact)
                    if condition_ir_artifact is not None
                    else None
                ),
                compiler_readiness_blockers=tuple(compiler_blockers),
                activation_status=_required_text(
                    activation.get("activation_status"),
                    f"{rule_id}.activation_status",
                ),
                adapter_status=adapter_status,
                blockers=tuple(
                    _required_text(value, f"{rule_id}.blockers")
                    for value in activation.get("blockers", [])
                ),
                antecedent_mode=_required_text(
                    activation.get("antecedent_mode"),
                    f"{rule_id}.antecedent_mode",
                ),
                antecedent_rule_ids=tuple(
                    _required_text(value, f"{rule_id}.antecedent_rule_ids")
                    for value in activation.get("antecedent_rule_ids", [])
                ),
                relation_binding_dispositions=relation_dispositions,
                category_membership_statuses=category_statuses,
                condition_compiled=condition_compiled,
                knowledge_execution_unlocked=execution_unlocked,
                runtime_effect_allowed=False,
                semantic_refs=tuple(semantic_refs),
            )
        )

    return tuple(decisions)


def absence_evidence_ready(
    decision: CareerResponseDecision,
    *,
    closed_world_evidence_ref: str | None,
) -> bool:
    """Evaluate only the evidence-readiness precondition for source negation.

    This does not unlock execution.  It only prevents database-missing from
    being interpreted as source-supported absence.
    """

    if "CLOSED_WORLD_ABSENCE_EVIDENCE" not in decision.blockers:
        return True
    return bool(str(closed_world_evidence_ref or "").strip())


def audit_response_semantics_adapter_readiness() -> dict[str, Any]:
    pilot = adapt_response_pilot_registry()
    decisions = build_career_response_decisions()

    activation_payload = load_activation_closure()
    activation_summary = activation_payload.get("summary")
    if not isinstance(activation_summary, dict):
        raise ValueError("activation closure summary must be an object")

    compatibility_closure = _read_json(RESPONSE_COMPATIBILITY_CLOSURE_PATH)
    compatibility_summary = compatibility_closure.get("summary")
    if not isinstance(compatibility_summary, dict):
        raise ValueError("compatibility closure summary must be an object")

    relation_payload = _read_json(RELATION_BINDING_PATH)
    category_payload = _read_json(CATEGORY_REVIEW_PATH)
    ordinal_payload = _read_json(CAREER_ORDINAL_CONSTRAINTS_PATH)
    ordinal_constraints = load_career_ordinal_constraints()
    ordinal_links = load_career_ordinal_rule_links()
    ordinal_impact = load_career_ordinal_blocker_impact()
    semantic_normalization = load_career_semantic_normalization()
    compiler_readiness = load_career_compiler_readiness_census()
    dependency_ir = load_career_dependency_ir()
    direct_condition_ir = load_career_direct_condition_ir()
    validate_career_ordinal_cross_artifacts()
    validate_career_compiler_readiness_cross_artifacts()

    pilot_status_counts = Counter(
        item.knowledge_execution_status for item in pilot
    )
    adapter_status_counts = Counter(item.adapter_status for item in decisions)
    compatibility_counts = Counter(item.compatibility_band for item in decisions)

    runtime_authorized = sum(
        1 for item in decisions if item.runtime_effect_allowed
    )
    if runtime_authorized != 0:
        raise ValueError("real Career adapter unexpectedly authorized runtime effects")

    condition_compiled_count = sum(
        1 for item in decisions if item.condition_compiled
    )
    execution_unlocked_count = sum(
        1 for item in decisions if item.knowledge_execution_unlocked
    )

    unresolved_antecedent = int(
        activation_summary.get("unresolved_antecedent_reference_rows", -1)
    )
    explicit_antecedent = int(
        activation_summary.get("explicit_antecedent_dependency_rows", -1)
    )

    relation_coverage = relation_payload.get("coverage")
    category_coverage = category_payload.get("coverage")

    relation_count = (
        int(relation_coverage.get("reviewed"))
        if isinstance(relation_coverage, dict)
        and isinstance(relation_coverage.get("reviewed"), int)
        else len(relation_payload.get("records", []))
    )
    category_count = (
        int(category_coverage.get("reviewed"))
        if isinstance(category_coverage, dict)
        and isinstance(category_coverage.get("reviewed"), int)
        else len(category_payload.get("records", []))
    )

    response_gain_total = int(
        compatibility_summary.get("response_gain_total", -1)
    )

    return {
        "schema_version": "0.1",
        "artifact_id": "RESPONSE_SEMANTICS_ADAPTER_READINESS_V0_3",
        "knowledge_inputs": {
            "response_pilot": str(
                RESPONSE_PILOT_PATH.relative_to(ROOT)
            ),
            "career_response_compatibility_closure": str(
                RESPONSE_COMPATIBILITY_CLOSURE_PATH.relative_to(ROOT)
            ),
            "career_contextual_activation_closure": str(
                ACTIVATION_CLOSURE_PATH.relative_to(ROOT)
            ),
            "career_relation_binding": str(
                RELATION_BINDING_PATH.relative_to(ROOT)
            ),
            "career_category_review": str(
                CATEGORY_REVIEW_PATH.relative_to(ROOT)
            ),
            "career_ordinal_constraints": str(
                CAREER_ORDINAL_CONSTRAINTS_PATH.relative_to(ROOT)
            ),
            "career_ordinal_rule_links": str(
                CAREER_ORDINAL_RULE_LINKS_PATH.relative_to(ROOT)
            ),
            "career_ordinal_blocker_impact": str(
                CAREER_ORDINAL_BLOCKER_IMPACT_PATH.relative_to(ROOT)
            ),
            "career_semantic_normalization": str(
                CAREER_SEMANTIC_NORMALIZATION_PATH.relative_to(ROOT)
            ),
            "career_compiler_readiness_census": str(
                CAREER_COMPILER_READINESS_CENSUS_PATH.relative_to(ROOT)
            ),
            "career_dependency_ir": str(
                CAREER_DEPENDENCY_IR_PATH.relative_to(ROOT)
            ),
            "career_direct_condition_ir": str(
                CAREER_DIRECT_CONDITION_IR_PATH.relative_to(ROOT)
            ),
        },
        "response_pilot": {
            "total": len(pilot),
            "knowledge_execution_status_counts": dict(
                sorted(pilot_status_counts.items())
            ),
            "product_semantic_only": sum(
                1 for item in pilot if item.allowed_use == "SEMANTIC_ONLY"
            ),
            "product_blocked": sum(
                1 for item in pilot if item.allowed_use == "BLOCKED"
            ),
            "runtime_effects_authorized": sum(
                1 for item in pilot if item.runtime_effect_allowed
            ),
        },
        "career_ordinal_registry": {
            "total_constraints": len(ordinal_constraints),
            "relation_type_counts": _deep(
                ordinal_payload.get("relation_type_counts", {})
            ),
            "runtime_effects_authorized": sum(
                1
                for item in ordinal_constraints
                if item.get("product_execution_unlocked") is True
            ),
            "numericized_constraints": sum(
                1
                for item in ordinal_constraints
                if any(
                    item.get(key) is not None
                    for key in (
                        "numeric_gain",
                        "numeric_value",
                        "probability",
                        "numeric_threshold",
                    )
                    if key in item
                )
            ),
            "transitive_closure_authorized": sum(
                1
                for item in ordinal_constraints
                if item.get("transitive_closure_allowed") is True
            ),
        },
        "career_ordinal_rule_linking": {
            "constraints_dispositioned": int(
                ordinal_links.get("coverage", {}).get("constraints", -1)
            ),
            "linked_atomic_rule_ids": int(
                ordinal_links.get("coverage", {}).get(
                    "linked_atomic_rule_ids", -1
                )
            ),
            "link_disposition_counts": _deep(
                ordinal_links.get("disposition_counts", {})
            ),
            "blocker_impact_counts": _deep(
                ordinal_impact.get("summary", {}).get("impact_counts", {})
            ),
            "unique_activation_rules_touched": int(
                ordinal_impact.get("summary", {}).get(
                    "unique_activation_rules_touched", -1
                )
            ),
            "blockers_resolved_by_ordinal_evidence": int(
                ordinal_impact.get("summary", {}).get(
                    "blockers_resolved_by_ordinal_evidence", -1
                )
            ),
            "execution_unlocked": int(
                ordinal_impact.get("summary", {}).get(
                    "execution_unlocked", -1
                )
            ),
        },
        "career_semantic_normalization": {
            "target_rows": int(
                semantic_normalization.get("coverage", {}).get("target_rows", -1)
            ),
            "reviewed": int(
                semantic_normalization.get("coverage", {}).get("reviewed", -1)
            ),
            "remaining": int(
                semantic_normalization.get("coverage", {}).get("remaining", -1)
            ),
            "disposition_counts": _deep(
                semantic_normalization.get("summary", {}).get(
                    "disposition_counts", {}
                )
            ),
            "generic_blocker_before": int(
                semantic_normalization.get("summary", {}).get(
                    "semantic_normalization_blockers_before", -1
                )
            ),
            "generic_blocker_after": int(
                semantic_normalization.get("summary", {}).get(
                    "semantic_normalization_blockers_after", -1
                )
            ),
            "added_precise_blocker_counts": _deep(
                semantic_normalization.get("summary", {}).get(
                    "added_precise_blocker_counts", {}
                )
            ),
            "source_resolution_changes": int(
                semantic_normalization.get("summary", {}).get(
                    "source_resolution_changes", -1
                )
            ),
            "conditions_compiled": int(
                semantic_normalization.get("summary", {}).get(
                    "conditions_compiled", -1
                )
            ),
            "execution_unlocked": int(
                semantic_normalization.get("summary", {}).get(
                    "execution_unlocked", -1
                )
            ),
        },
        "career": {
            "total_rows": len(decisions),
            "compatibility_band_counts": dict(
                sorted(compatibility_counts.items())
            ),
            "response_gain_total": response_gain_total,
            "adapter_status_counts": dict(sorted(adapter_status_counts.items())),
            "knowledge_condition_ir_ready_pending_product_compilation": (
                adapter_status_counts[
                    "KNOWLEDGE_CONDITION_IR_READY_PENDING_PRODUCT_COMPILATION"
                ]
            ),
            "local_structure_not_condition_ir_ready": adapter_status_counts[
                "LOCAL_STRUCTURE_NOT_CONDITION_IR_READY"
            ],
            "compiler_readiness_band_counts": _deep(
                compiler_readiness.get("summary", {}).get("band_counts", {})
            ),
            "knowledge_condition_ir_ready_total": int(
                compiler_readiness.get("summary", {}).get(
                    "total_knowledge_condition_ir_ready", -1
                )
            ),
            "dependency_condition_ir_records": len(
                dependency_ir.get("records", [])
            ),
            "direct_condition_ir_records": len(
                direct_condition_ir.get("records", [])
            ),
            "runtime_effects_authorized": runtime_authorized,
            "condition_compiled_count": condition_compiled_count,
            "knowledge_execution_unlocked_count": execution_unlocked_count,
            "unresolved_antecedent_reference_rows": unresolved_antecedent,
            "explicit_antecedent_dependency_rows": explicit_antecedent,
            "closed_world_evidence_gated_rows": int(
                activation_summary.get("closed_world_evidence_gated_rows", -1)
            ),
            "rows_with_source_underdetermination": int(
                activation_summary.get("rows_with_source_underdetermination", -1)
            ),
            "relation_bound_rows": relation_count,
            "category_reviewed_rows": category_count,
            "unauthorized_unlock_count": 0,
        },
        "maturity": {
            "response_semantics_adapter": "IMPLEMENTED_V0_3_CONDITION_IR_AWARE",
            "semantic_preservation": "INTERNALLY_VALIDATABLE",
            "career_execution": "ZERO_UNLOCK_EXPECTED",
            "response_compiler": "NOT_IMPLEMENTED",
            "response_profile_tau": "NOT_IMPLEMENTED",
            "predictive_validity": "NOT_VALIDATED",
        },
        "decisions": [item.to_dict() for item in decisions],
    }


def validate_real_adapter_zero_unlock() -> None:
    pilot = adapt_response_pilot_registry()
    decisions = build_career_response_decisions()

    if any(item.runtime_effect_allowed for item in pilot):
        raise ValueError("real response pilot unexpectedly authorizes runtime effect")
    if any(item.runtime_effect_allowed for item in decisions):
        raise ValueError("real Career response row unexpectedly authorizes runtime effect")


def serialize_response_envelope(
    envelope: ResponseSemanticEnvelope,
) -> dict[str, Any]:
    return envelope.to_dict()
