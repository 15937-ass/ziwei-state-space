"""Safe executable Rule IR for the product layer.

PL2 refuses to guess executable semantics from free-form traditional text.
A rule becomes executable only when provenance and normalization are verified
and every non-trivial condition has an explicit structured representation.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from enum import Enum
from typing import Any, Iterable, Mapping, Sequence

from .condition_atoms import CompiledCondition


_ALLOWED_REVIEW = {"SOURCE_SPAN_VERIFIED", "HUMAN_VERIFIED"}
_ALLOWED_NORMALIZATION = {"SOURCE_PRESERVING", "INFERRED", "IMPLEMENTATION"}
_NO_CONDITION = {"", "无", "none", "null", "n/a", "not_applicable"}


class CompileDisposition(str, Enum):
    EXECUTABLE = "EXECUTABLE"
    BLOCKED_PROVENANCE = "BLOCKED_PROVENANCE"
    BLOCKED_NORMALIZATION = "BLOCKED_NORMALIZATION"
    NEEDS_CONDITION_NORMALIZATION = "NEEDS_CONDITION_NORMALIZATION"
    INVALID = "INVALID"


@dataclass(frozen=True)
class CompileIssue:
    rule_id: str
    disposition: CompileDisposition
    reason: str


@dataclass(frozen=True)
class RuleIR:
    rule_id: str
    school: str
    source_work: str
    source_location: str
    review_status: str
    source_epistemic: str
    normalization_epistemic: str
    subject: str
    context: str
    required_facts: tuple[str, ...]
    any_of_facts: tuple[tuple[str, ...], ...]
    forbidden_facts: tuple[str, ...]
    antecedent_rule_ids: tuple[str, ...]
    time_scopes: tuple[str, ...]
    palace_scopes: tuple[str, ...]
    topic_scopes: tuple[str, ...]
    operator: str
    target_type: str
    target_state: str
    state_change: str
    valence: str
    conflict_group: str
    evidence_text: str

    @property
    def source_pointer(self) -> str:
        return f"{self.source_work}::{self.source_location}"

    def condition(self) -> CompiledCondition:
        return CompiledCondition(
            all_of=self.required_facts,
            any_of=self.any_of_facts,
            none_of=self.forbidden_facts,
        )


@dataclass(frozen=True)
class RuntimeState:
    facts: frozenset[str]
    latent_states: Mapping[str, Any]
    time_scope: str = ""
    palace_scope: str = ""


@dataclass(frozen=True)
class ActiveRuleNode:
    rule_id: str
    school: str
    source_pointer: str
    review_status: str
    matched_conditions: tuple[str, ...]
    matched_antecedents: tuple[str, ...]
    operator: str
    target_state: str
    before_state: Any
    after_state: Mapping[str, Any]
    conflict_group: str
    evidence_status: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ActiveRuleGraph:
    nodes: tuple[ActiveRuleNode, ...]
    conflict_groups: Mapping[str, tuple[str, ...]]

    def to_dict(self) -> dict[str, Any]:
        return {
            "nodes": [node.to_dict() for node in self.nodes],
            "conflict_groups": {
                key: list(value) for key, value in sorted(self.conflict_groups.items())
            },
        }


@dataclass(frozen=True)
class CompilationReport:
    executable: tuple[RuleIR, ...]
    issues: tuple[CompileIssue, ...]

    def counts(self) -> dict[str, int]:
        out = {item.value: 0 for item in CompileDisposition}
        out[CompileDisposition.EXECUTABLE.value] = len(self.executable)
        for issue in self.issues:
            out[issue.disposition.value] += 1
        return out


def _truthy(value: Any) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def _parse_scope(value: Any) -> tuple[str, ...]:
    if value is None:
        return ()
    if isinstance(value, (list, tuple, set)):
        return tuple(sorted({str(v).strip() for v in value if str(v).strip()}))
    text = str(value).strip()
    if not text or text in {"[]", "{}"}:
        return ()
    try:
        parsed = json.loads(text)
    except (TypeError, ValueError, json.JSONDecodeError):
        parsed = None
    if isinstance(parsed, list):
        return tuple(sorted({str(v).strip() for v in parsed if str(v).strip()}))
    return tuple(sorted({part.strip() for part in text.split("|") if part.strip()}))


def _required(row: Mapping[str, Any], key: str) -> str:
    value = str(row.get(key, "")).strip()
    if not value:
        raise ValueError(f"{key} is required")
    return value


def compile_rule_row(
    row: Mapping[str, Any],
    *,
    condition_atoms: Sequence[str] | None = None,
    condition_spec: CompiledCondition | None = None,
) -> tuple[RuleIR | None, CompileIssue | None]:
    """Compile one reviewed rule without interpreting free-form condition text."""

    rule_id = str(row.get("rule_id", "")).strip() or "<missing-rule-id>"

    try:
        school = _required(row, "school")
        source_work = _required(row, "source_work")
        source_location = _required(row, "source_location")
        operator = _required(row, "operator")
        target_type = _required(row, "target_type")
        target_state = _required(row, "target_normalized")
    except ValueError as exc:
        return None, CompileIssue(rule_id, CompileDisposition.INVALID, str(exc))

    review_status = str(row.get("review_status", "")).strip()
    source_verified = _truthy(row.get("source_span_verified", False))
    if review_status not in _ALLOWED_REVIEW or not source_verified:
        return None, CompileIssue(
            rule_id,
            CompileDisposition.BLOCKED_PROVENANCE,
            "executable rules require SOURCE_SPAN_VERIFIED/HUMAN_VERIFIED and source_span_verified=true",
        )

    normalization_epistemic = str(row.get("normalization_epistemic", "")).strip()
    normalization_verified = _truthy(row.get("normalization_verified", False))
    if (
        normalization_epistemic not in _ALLOWED_NORMALIZATION
        or not normalization_verified
    ):
        return None, CompileIssue(
            rule_id,
            CompileDisposition.BLOCKED_NORMALIZATION,
            "executable rules require verified non-hypothetical normalization",
        )

    source_epistemic = str(row.get("source_epistemic", "")).strip()
    if source_epistemic == "UNRESOLVED_SOURCE":
        return None, CompileIssue(
            rule_id,
            CompileDisposition.BLOCKED_PROVENANCE,
            "UNRESOLVED_SOURCE cannot execute",
        )

    subject = str(row.get("subject", "")).strip()
    required_facts: set[str] = set()
    if subject:
        required_facts.add(f"subject:{subject}")

    any_of_facts: tuple[tuple[str, ...], ...] = ()
    forbidden_facts: tuple[str, ...] = ()

    condition = str(row.get("condition", "")).strip()
    has_free_condition = condition.lower() not in _NO_CONDITION and condition not in _NO_CONDITION
    if has_free_condition:
        if condition_spec is not None:
            required_facts.update(condition_spec.all_of)
            any_of_facts = condition_spec.any_of
            forbidden_facts = condition_spec.none_of
        else:
            atoms = tuple(
                sorted(
                    {
                        str(atom).strip()
                        for atom in (condition_atoms or ())
                        if str(atom).strip()
                    }
                )
            )
            if not atoms:
                return None, CompileIssue(
                    rule_id,
                    CompileDisposition.NEEDS_CONDITION_NORMALIZATION,
                    "free-form condition is not parsed heuristically; explicit condition atoms are required",
                )
            required_facts.update(atoms)

    ir = RuleIR(
        rule_id=rule_id,
        school=school,
        source_work=source_work,
        source_location=source_location,
        review_status=review_status,
        source_epistemic=source_epistemic,
        normalization_epistemic=normalization_epistemic,
        subject=subject,
        context=str(row.get("context", "")).strip(),
        required_facts=tuple(sorted(required_facts)),
        any_of_facts=any_of_facts,
        forbidden_facts=forbidden_facts,
        antecedent_rule_ids=_parse_scope(row.get("antecedent_rule_ids")),
        time_scopes=_parse_scope(row.get("time_scope")),
        palace_scopes=_parse_scope(row.get("palace_scope")),
        topic_scopes=_parse_scope(row.get("topic_scope")),
        operator=operator,
        target_type=target_type,
        target_state=target_state,
        state_change=str(row.get("state_change", "")).strip(),
        valence=str(row.get("valence", "")).strip(),
        conflict_group=str(row.get("conflict_group", "")).strip(),
        evidence_text=str(row.get("evidence_text", "")).strip(),
    )
    return ir, None


def compile_rule_rows(
    rows: Iterable[Mapping[str, Any]],
    *,
    condition_registry: Mapping[str, Sequence[str] | CompiledCondition] | None = None,
) -> CompilationReport:
    executable: list[RuleIR] = []
    issues: list[CompileIssue] = []
    registry = condition_registry or {}

    for row in rows:
        rule_id = str(row.get("rule_id", "")).strip()
        condition_value = registry.get(rule_id)
        if isinstance(condition_value, CompiledCondition):
            ir, issue = compile_rule_row(row, condition_spec=condition_value)
        else:
            ir, issue = compile_rule_row(row, condition_atoms=condition_value)

        if ir is not None:
            executable.append(ir)
        if issue is not None:
            issues.append(issue)

    return CompilationReport(
        executable=tuple(sorted(executable, key=lambda r: r.rule_id)),
        issues=tuple(sorted(issues, key=lambda x: (x.rule_id, x.disposition.value))),
    )


class RuleRuntime:
    """Deterministic matcher over already-compiled RuleIR.

    Antecedent dependencies are explicit engineering links between executable
    rules. They never create chart facts and are never inferred from prose.
    """

    def __init__(self, rules: Iterable[RuleIR]):
        by_id: dict[str, RuleIR] = {}
        for rule in rules:
            if rule.rule_id in by_id:
                raise ValueError(f"duplicate rule_id: {rule.rule_id}")
            by_id[rule.rule_id] = rule
        self._by_id = by_id
        self._rules = tuple(by_id[key] for key in sorted(by_id))
        self._validate_antecedents()

    def _validate_antecedents(self) -> None:
        for rule in self._rules:
            missing = sorted(set(rule.antecedent_rule_ids) - set(self._by_id))
            if missing:
                raise ValueError(
                    f"{rule.rule_id}: missing antecedent rule(s): {', '.join(missing)}"
                )
            if rule.rule_id in rule.antecedent_rule_ids:
                raise ValueError(f"{rule.rule_id}: self antecedent is not allowed")

        visit_state: dict[str, int] = {}

        def visit(rule_id: str, trail: tuple[str, ...]) -> None:
            state = visit_state.get(rule_id, 0)
            if state == 2:
                return
            if state == 1:
                cycle = " -> ".join(trail + (rule_id,))
                raise ValueError(f"antecedent cycle detected: {cycle}")
            visit_state[rule_id] = 1
            rule = self._by_id[rule_id]
            for antecedent in rule.antecedent_rule_ids:
                visit(antecedent, trail + (rule_id,))
            visit_state[rule_id] = 2

        for rule_id in sorted(self._by_id):
            visit(rule_id, ())

    def match(
        self,
        chart_state: RuntimeState,
        temporal_state: RuntimeState | None = None,
        question_scope: str = "",
    ) -> ActiveRuleGraph:
        temporal = temporal_state or RuntimeState(frozenset(), {})
        all_facts = frozenset(set(chart_state.facts) | set(temporal.facts))
        time_scope = temporal.time_scope or chart_state.time_scope
        palace_scope = temporal.palace_scope or chart_state.palace_scope

        candidates: dict[str, tuple[RuleIR, CompiledCondition]] = {}
        for rule in self._rules:
            if rule.time_scopes and time_scope not in rule.time_scopes:
                continue
            if rule.palace_scopes and palace_scope not in rule.palace_scopes:
                continue
            if rule.topic_scopes and question_scope not in rule.topic_scopes:
                continue
            condition = rule.condition()
            if condition.matches(all_facts):
                candidates[rule.rule_id] = (rule, condition)

        active_ids: set[str] = set()
        while True:
            changed = False
            for rule_id in sorted(candidates):
                if rule_id in active_ids:
                    continue
                rule, _ = candidates[rule_id]
                if set(rule.antecedent_rule_ids).issubset(active_ids):
                    active_ids.add(rule_id)
                    changed = True
            if not changed:
                break

        nodes: list[ActiveRuleNode] = []
        conflicts: dict[str, list[str]] = {}
        for rule_id in sorted(active_ids):
            rule, condition = candidates[rule_id]
            before = chart_state.latent_states.get(
                rule.target_state,
                temporal.latent_states.get(rule.target_state),
            )
            node = ActiveRuleNode(
                rule_id=rule.rule_id,
                school=rule.school,
                source_pointer=rule.source_pointer,
                review_status=rule.review_status,
                matched_conditions=condition.matched_facts(all_facts),
                matched_antecedents=tuple(rule.antecedent_rule_ids),
                operator=rule.operator,
                target_state=rule.target_state,
                before_state=before,
                after_state={
                    "operator": rule.operator,
                    "state_change": rule.state_change,
                    "valence": rule.valence,
                },
                conflict_group=rule.conflict_group,
                evidence_status=f"{rule.source_epistemic}/{rule.normalization_epistemic}",
            )
            nodes.append(node)
            if rule.conflict_group:
                conflicts.setdefault(rule.conflict_group, []).append(rule.rule_id)

        return ActiveRuleGraph(
            nodes=tuple(nodes),
            conflict_groups={
                key: tuple(sorted(ids))
                for key, ids in sorted(conflicts.items())
                if len(ids) > 1
            },
        )
