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
    / "CAREER_CONTEXTUAL_ACTIVATION_CLOSURE_251_v0.2.json"
)

KNOWLEDGE_EXECUTION_STATUSES = frozenset(
    {"LEXICAL_ONLY", "STRUCTURAL_ONLY", "SAFE_SYMBOLIC", "BLOCKED"}
)
PRODUCT_ALLOWED_USES = frozenset({"SEMANTIC_ONLY", "EXECUTABLE", "BLOCKED"})

CAREER_ADAPTER_STATUS_BY_READINESS = {
    "LOCAL_STRUCTURE_READY": "SEMANTIC_ONLY_PENDING_COMPILATION",
    "SOURCE_UNDERDETERMINED": "BLOCKED_SOURCE_UNDERDETERMINED",
    "DEPENDENCY_COMPILER_GATED": "BLOCKED_DEPENDENCY_COMPILER",
    "NORMALIZATION_DEFERRED": "BLOCKED_NORMALIZATION",
    "MULTI_CLASS_BLOCKED": "BLOCKED_MULTIPLE",
}

CAREER_ADAPTER_STATUSES = frozenset(CAREER_ADAPTER_STATUS_BY_READINESS.values())

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
        if readiness_class not in CAREER_ADAPTER_STATUS_BY_READINESS:
            raise ValueError(
                f"{rule_id}: unsupported Knowledge readiness class {readiness_class}"
            )

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

        decisions.append(
            CareerResponseDecision(
                source_rule_id=rule_id,
                compatibility_band=_required_text(
                    compat.get("compatibility_band"),
                    f"{rule_id}.compatibility_band",
                ),
                knowledge_readiness_class=readiness_class,
                activation_status=_required_text(
                    activation.get("activation_status"),
                    f"{rule_id}.activation_status",
                ),
                adapter_status=CAREER_ADAPTER_STATUS_BY_READINESS[
                    readiness_class
                ],
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
        "artifact_id": "RESPONSE_SEMANTICS_ADAPTER_READINESS_V0_1",
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
        "career": {
            "total_rows": len(decisions),
            "compatibility_band_counts": dict(
                sorted(compatibility_counts.items())
            ),
            "response_gain_total": response_gain_total,
            "adapter_status_counts": dict(sorted(adapter_status_counts.items())),
            "semantic_only_pending_compilation": adapter_status_counts[
                "SEMANTIC_ONLY_PENDING_COMPILATION"
            ],
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
            "response_semantics_adapter": "IMPLEMENTED_V0_1",
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
