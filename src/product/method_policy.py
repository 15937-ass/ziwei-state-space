"""Method Policy π v0.1: deterministic CBR + fail-closed symbolic planner.

This module is intentionally narrower than a Ziwei inference engine.  It learns
how to choose auditable next actions from source-reviewed procedural material
without creating canonical Ziwei truth, probabilities, hidden reasoning, or
expert conclusions.

Key Product v0.4 invariant:
- source MethodPattern records may remain SEMANTIC_ONLY;
- runtime procedural actions are permitted only through the separate
  METHOD_POLICY_EXECUTION_RULES_v0.1 derived adapter;
- source/chart references are not machine-readable facts.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
import json
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

from src.product.expert_case_corpus import (
    BASE_DIR as WANG_BASE_DIR,
    build_blind_case_view,
    load_wang_case_bundles,
    load_wang_loco_manifest,
    load_wang_method_patterns,
)
from src.product.expert_method_contracts import (
    EXPERT_ACTIONS,
    CaseBundle,
    InferenceTrace,
    MethodPattern,
    compile_inference_trace,
)


SCHEMA_VERSION = "0.1"
POLICY_VERSION = "METHOD_POLICY_V0_1_CBR_HEURISTIC_SYMBOLIC"

ROOT = Path(__file__).resolve().parents[2]
EXECUTION_RULES_PATH = ROOT / "product" / "METHOD_POLICY_EXECUTION_RULES_v0.1.json"

EVIDENCE_STATUSES = frozenset(
    {
        "MATERIALIZED_FACT",
        "SOURCE_REFERENCE_ONLY",
        "MISSING",
        "BLOCKED",
    }
)

EXECUTION_DISPOSITIONS = frozenset(
    {
        "POLICY_EXECUTABLE_DERIVED",
        "BLOCKED_CONTEXT_BINDING",
        "DEFER_TO_SYMBOLIC_ADAPTER",
    }
)

PATTERN_READINESS = frozenset(
    {
        "NOT_TARGETED",
        "BLOCKED_DISPOSITION",
        "BLOCKED_REFERENCE_ONLY",
        "BLOCKED_MISSING_EVIDENCE",
        "BLOCKED_EVIDENCE",
        "EXECUTABLE_READY",
    }
)

REPLAY_READINESS = frozenset(
    {
        "RETRIEVAL_READY",
        "ACTION_SELECTION_READY",
        "FULL_EXPERT_REPLAY_READY",
    }
)

SOURCE_REFERENCE_PREFIXES = (
    "SOURCE_CHART:",
    "WANG-ANXING-TUIDUAN:",
    "PROJECT_SOURCE:",
)

FORBIDDEN_RETRIEVAL_FIELDS = frozenset(
    {
        "source",
        "source_subject_label",
        "expert_reasoning_graph",
        "expert_conclusion_refs",
        "outcome_refs",
        "expert_prose",
        "biography",
    }
)


@dataclass(frozen=True)
class EvidenceItem:
    evidence_id: str
    kind: str
    status: str
    refs: tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.evidence_id.strip():
            raise ValueError("EvidenceItem.evidence_id is required")
        if not self.kind.strip():
            raise ValueError("EvidenceItem.kind is required")
        if self.status not in EVIDENCE_STATUSES:
            raise ValueError(f"unsupported evidence status: {self.status}")
        if self.status in {"MATERIALIZED_FACT", "SOURCE_REFERENCE_ONLY"} and not self.refs:
            raise ValueError(
                f"{self.evidence_id}: {self.status} evidence requires refs"
            )


@dataclass(frozen=True)
class RetrievalHit:
    case_id: str
    person_group_id: str
    target_domains: tuple[str, ...]
    match_reasons: tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.case_id.strip():
            raise ValueError("RetrievalHit.case_id is required")
        if not self.person_group_id.strip():
            raise ValueError("RetrievalHit.person_group_id is required")
        if not self.target_domains:
            raise ValueError("RetrievalHit.target_domains cannot be empty")
        if not self.match_reasons:
            raise ValueError("RetrievalHit.match_reasons cannot be empty")

    def to_dict(self) -> dict[str, Any]:
        return {
            "case_id": self.case_id,
            "person_group_id": self.person_group_id,
            "target_domains": list(self.target_domains),
            "match_reasons": list(self.match_reasons),
        }


@dataclass(frozen=True)
class ExecutionRule:
    pattern_id: str
    disposition: str
    target_domains: tuple[str, ...]
    required_evidence_kinds: tuple[str, ...]
    allowed_actions: tuple[str, ...]
    blocker: str | None
    rationale: str

    def __post_init__(self) -> None:
        if not self.pattern_id.strip():
            raise ValueError("ExecutionRule.pattern_id is required")
        if self.disposition not in EXECUTION_DISPOSITIONS:
            raise ValueError(
                f"{self.pattern_id}: unsupported disposition {self.disposition}"
            )
        for action in self.allowed_actions:
            if action not in EXPERT_ACTIONS:
                raise ValueError(
                    f"{self.pattern_id}: unsupported allowed action {action}"
                )
        if self.disposition == "POLICY_EXECUTABLE_DERIVED":
            if not self.target_domains:
                raise ValueError(
                    f"{self.pattern_id}: executable rule needs target_domains"
                )
            if not self.required_evidence_kinds:
                raise ValueError(
                    f"{self.pattern_id}: executable rule needs evidence kinds"
                )
            if not self.allowed_actions:
                raise ValueError(
                    f"{self.pattern_id}: executable rule needs allowed_actions"
                )
        elif self.allowed_actions:
            raise ValueError(
                f"{self.pattern_id}: blocked/deferred rule cannot allow actions"
            )


@dataclass(frozen=True)
class PatternAssessment:
    pattern_id: str
    readiness: str
    disposition: str
    missing_evidence_kinds: tuple[str, ...]
    reference_only_evidence_kinds: tuple[str, ...]
    blockers: tuple[str, ...]

    def __post_init__(self) -> None:
        if self.readiness not in PATTERN_READINESS:
            raise ValueError(
                f"{self.pattern_id}: unsupported readiness {self.readiness}"
            )

    @property
    def executable(self) -> bool:
        return self.readiness == "EXECUTABLE_READY"

    def to_dict(self) -> dict[str, Any]:
        return {
            "pattern_id": self.pattern_id,
            "readiness": self.readiness,
            "disposition": self.disposition,
            "missing_evidence_kinds": list(self.missing_evidence_kinds),
            "reference_only_evidence_kinds": list(
                self.reference_only_evidence_kinds
            ),
            "blockers": list(self.blockers),
            "executable": self.executable,
        }


@dataclass(frozen=True)
class MethodPolicyRun:
    trace: InferenceTrace
    retrieved_cases: tuple[RetrievalHit, ...]
    pattern_assessments: tuple[PatternAssessment, ...]
    selected_pattern_id: str | None
    blockers: tuple[str, ...]

    @property
    def completed(self) -> bool:
        return self.trace.final_status == "COMPLETED"

    def to_dict(self) -> dict[str, Any]:
        return {
            "trace": self.trace.to_dict(),
            "retrieved_cases": [item.to_dict() for item in self.retrieved_cases],
            "pattern_assessments": [
                item.to_dict() for item in self.pattern_assessments
            ],
            "selected_pattern_id": self.selected_pattern_id,
            "blockers": list(self.blockers),
            "completed": self.completed,
        }


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _as_text_tuple(value: Any, path: str) -> tuple[str, ...]:
    if value is None:
        return ()
    if not isinstance(value, list):
        raise ValueError(f"{path} must be an array")
    out: list[str] = []
    for index, item in enumerate(value):
        text = str(item or "").strip()
        if not text:
            raise ValueError(f"{path}[{index}] cannot be empty")
        out.append(text)
    return tuple(out)


def load_execution_rules(
    path: Path = EXECUTION_RULES_PATH,
) -> dict[str, ExecutionRule]:
    payload = _read_json(path)
    if payload.get("schema_version") != SCHEMA_VERSION:
        raise ValueError("execution-rule schema_version must be 0.1")
    if payload.get("artifact_id") != "METHOD_POLICY_EXECUTION_RULES_V0_1":
        raise ValueError("unexpected execution-rule artifact_id")

    raw = payload.get("dispositions")
    if not isinstance(raw, list):
        raise ValueError("execution-rule dispositions must be an array")

    rules: dict[str, ExecutionRule] = {}
    for index, item in enumerate(raw):
        if not isinstance(item, dict):
            raise ValueError(f"dispositions[{index}] must be an object")
        rule = ExecutionRule(
            pattern_id=str(item.get("pattern_id") or "").strip(),
            disposition=str(item.get("disposition") or "").strip(),
            target_domains=_as_text_tuple(
                item.get("target_domains"), f"dispositions[{index}].target_domains"
            ),
            required_evidence_kinds=_as_text_tuple(
                item.get("required_evidence_kinds"),
                f"dispositions[{index}].required_evidence_kinds",
            ),
            allowed_actions=_as_text_tuple(
                item.get("allowed_actions"),
                f"dispositions[{index}].allowed_actions",
            ),
            blocker=(
                str(item["blocker"]).strip()
                if item.get("blocker") is not None
                else None
            ),
            rationale=str(item.get("rationale") or "").strip(),
        )
        if rule.pattern_id in rules:
            raise ValueError(f"duplicate execution rule: {rule.pattern_id}")
        rules[rule.pattern_id] = rule

    return rules


def validate_execution_rule_coverage(
    patterns: Sequence[MethodPattern],
    rules: Mapping[str, ExecutionRule],
) -> None:
    pattern_ids = {item.pattern_id for item in patterns}
    if set(rules) != pattern_ids:
        missing = sorted(pattern_ids - set(rules))
        extra = sorted(set(rules) - pattern_ids)
        raise ValueError(
            "execution-rule coverage mismatch: "
            f"missing={missing}, extra={extra}"
        )

    for pattern in patterns:
        if pattern.allowed_use != "SEMANTIC_ONLY":
            raise ValueError(
                f"{pattern.pattern_id}: source MethodPattern should remain SEMANTIC_ONLY"
            )
        rule = rules[pattern.pattern_id]
        if rule.target_domains != pattern.target_domains:
            raise ValueError(
                f"{pattern.pattern_id}: derived target scope must match source pattern"
            )
        if rule.required_evidence_kinds != pattern.required_evidence_kinds:
            raise ValueError(
                f"{pattern.pattern_id}: derived evidence kinds must match source pattern"
            )
        if rule.disposition == "POLICY_EXECUTABLE_DERIVED":
            if rule.allowed_actions != pattern.action_sequence:
                raise ValueError(
                    f"{pattern.pattern_id}: derived actions must exactly match source action sequence"
                )


def classify_source_ref_status(ref: str) -> str:
    text = str(ref or "").strip()
    if not text:
        return "MISSING"
    if text.startswith("MATERIALIZED_FACT:"):
        return "MATERIALIZED_FACT"
    if text.startswith(SOURCE_REFERENCE_PREFIXES):
        return "SOURCE_REFERENCE_ONLY"
    return "SOURCE_REFERENCE_ONLY"


def build_reference_only_evidence(case: CaseBundle) -> tuple[EvidenceItem, ...]:
    """Build a conservative evidence view for current Wang v0.1 cases.

    The source pointers are useful audit locators, but no chart facts have yet
    been materialized from them.  This function must therefore never emit
    MATERIALIZED_FACT for the current Wang corpus.
    """

    refs: list[str] = []
    if case.chart_snapshot_ref:
        refs.append(case.chart_snapshot_ref)
    refs.extend(case.available_information_refs)

    unique_refs = tuple(dict.fromkeys(refs))
    if not unique_refs:
        return (
            EvidenceItem(
                evidence_id=f"EVIDENCE:{case.case_id}:TARGET_CHART",
                kind="TARGET_CHART",
                status="MISSING",
                refs=(),
            ),
        )

    statuses = {classify_source_ref_status(ref) for ref in unique_refs}
    if statuses == {"MATERIALIZED_FACT"}:
        status = "MATERIALIZED_FACT"
    elif "BLOCKED" in statuses:
        status = "BLOCKED"
    else:
        status = "SOURCE_REFERENCE_ONLY"

    return (
        EvidenceItem(
            evidence_id=f"EVIDENCE:{case.case_id}:TARGET_CHART",
            kind="TARGET_CHART",
            status=status,
            refs=unique_refs,
        ),
    )


def _fold_for_case(
    manifest: Mapping[str, Any],
    case_id: str,
) -> Mapping[str, Any]:
    folds = manifest.get("folds")
    if not isinstance(folds, list):
        raise ValueError("LOCO manifest folds must be an array")
    matches = [item for item in folds if item.get("held_out_case_id") == case_id]
    if len(matches) != 1:
        raise ValueError(f"{case_id}: expected exactly one LOCO fold")
    return matches[0]


def retrieve_same_domain_cases(
    held_out_case: CaseBundle,
    fold: Mapping[str, Any],
    bundles: Sequence[CaseBundle],
) -> tuple[RetrievalHit, ...]:
    """Deterministic metadata-only CBR.

    v0.1 deliberately returns only exact target-domain matches.  It uses no
    expert graph, conclusion, outcome, source identity, biography, learned
    vector, or numeric similarity score.
    """

    if fold.get("held_out_case_id") != held_out_case.case_id:
        raise ValueError("fold/held-out case mismatch")
    if fold.get("held_out_person_group_id") != held_out_case.person_group_id:
        raise ValueError("fold/held-out person group mismatch")

    retrieval_ids_raw = fold.get("retrieval_case_ids")
    if not isinstance(retrieval_ids_raw, list):
        raise ValueError("fold retrieval_case_ids must be an array")
    retrieval_ids = tuple(str(item) for item in retrieval_ids_raw)

    by_id = {item.case_id: item for item in bundles}
    held_domains = set(held_out_case.target.domains)

    hits: list[RetrievalHit] = []
    for case_id in sorted(retrieval_ids):
        if case_id not in by_id:
            raise ValueError(f"unknown retrieval case: {case_id}")
        case = by_id[case_id]
        if case.person_group_id == held_out_case.person_group_id:
            raise ValueError("held-out person_group_id leaked into retrieval set")

        candidate_domains = set(case.target.domains)
        if held_domains == candidate_domains:
            hits.append(
                RetrievalHit(
                    case_id=case.case_id,
                    person_group_id=case.person_group_id,
                    target_domains=case.target.domains,
                    match_reasons=("EXACT_TARGET_DOMAIN",),
                )
            )

    return tuple(hits)


def retrieval_payload(hits: Sequence[RetrievalHit]) -> dict[str, Any]:
    """Return the only CBR payload permitted to the v0.1 planner."""

    return {
        "retrieval_version": "CBR_METADATA_ONLY_V0_1",
        "hits": [item.to_dict() for item in hits],
    }


def _evidence_status_by_kind(
    evidence: Sequence[EvidenceItem],
) -> dict[str, set[str]]:
    out: dict[str, set[str]] = {}
    for item in evidence:
        out.setdefault(item.kind, set()).add(item.status)
    return out


def assess_pattern(
    pattern: MethodPattern,
    rule: ExecutionRule,
    *,
    target_domains: Sequence[str],
    evidence: Sequence[EvidenceItem],
) -> PatternAssessment:
    if pattern.pattern_id != rule.pattern_id:
        raise ValueError("pattern/execution rule mismatch")

    target_set = set(target_domains)
    if not target_set.intersection(pattern.target_domains):
        return PatternAssessment(
            pattern_id=pattern.pattern_id,
            readiness="NOT_TARGETED",
            disposition=rule.disposition,
            missing_evidence_kinds=(),
            reference_only_evidence_kinds=(),
            blockers=(),
        )

    if rule.disposition != "POLICY_EXECUTABLE_DERIVED":
        blockers = (rule.blocker or rule.disposition,)
        return PatternAssessment(
            pattern_id=pattern.pattern_id,
            readiness="BLOCKED_DISPOSITION",
            disposition=rule.disposition,
            missing_evidence_kinds=(),
            reference_only_evidence_kinds=(),
            blockers=blockers,
        )

    status_by_kind = _evidence_status_by_kind(evidence)
    missing: list[str] = []
    reference_only: list[str] = []
    blocked: list[str] = []

    for kind in rule.required_evidence_kinds:
        statuses = status_by_kind.get(kind)
        if not statuses:
            missing.append(kind)
        elif "MATERIALIZED_FACT" in statuses:
            continue
        elif "SOURCE_REFERENCE_ONLY" in statuses:
            reference_only.append(kind)
        elif "BLOCKED" in statuses:
            blocked.append(kind)
        else:
            missing.append(kind)

    if blocked:
        readiness = "BLOCKED_EVIDENCE"
        blockers = tuple(f"BLOCKED_EVIDENCE:{kind}" for kind in blocked)
    elif reference_only:
        readiness = "BLOCKED_REFERENCE_ONLY"
        blockers = tuple(
            f"MATERIALIZATION_REQUIRED:{kind}" for kind in reference_only
        )
    elif missing:
        readiness = "BLOCKED_MISSING_EVIDENCE"
        blockers = tuple(f"MISSING_EVIDENCE:{kind}" for kind in missing)
    else:
        readiness = "EXECUTABLE_READY"
        blockers = ()

    return PatternAssessment(
        pattern_id=pattern.pattern_id,
        readiness=readiness,
        disposition=rule.disposition,
        missing_evidence_kinds=tuple(missing),
        reference_only_evidence_kinds=tuple(reference_only),
        blockers=blockers,
    )


def assess_patterns(
    patterns: Sequence[MethodPattern],
    rules: Mapping[str, ExecutionRule],
    *,
    target_domains: Sequence[str],
    evidence: Sequence[EvidenceItem],
) -> tuple[PatternAssessment, ...]:
    validate_execution_rule_coverage(patterns, rules)
    return tuple(
        assess_pattern(
            pattern,
            rules[pattern.pattern_id],
            target_domains=target_domains,
            evidence=evidence,
        )
        for pattern in sorted(patterns, key=lambda item: item.pattern_id)
    )


def _all_evidence_refs(evidence: Sequence[EvidenceItem]) -> tuple[str, ...]:
    refs: list[str] = []
    for item in evidence:
        refs.extend(item.refs)
    return tuple(dict.fromkeys(refs))


def _evidence_refs_for_kinds(
    evidence: Sequence[EvidenceItem],
    kinds: Iterable[str],
) -> tuple[str, ...]:
    kind_set = set(kinds)
    refs: list[str] = []
    for item in evidence:
        if item.kind in kind_set and item.status == "MATERIALIZED_FACT":
            refs.extend(item.refs)
    return tuple(dict.fromkeys(refs))


def _build_trace(
    *,
    case_id: str,
    steps: list[dict[str, Any]],
    final_status: str,
    output_refs: Sequence[str] = (),
) -> InferenceTrace:
    payload = {
        "schema_version": "0.1",
        "trace_id": f"TRACE:{POLICY_VERSION}:{case_id}",
        "case_id": case_id,
        "policy_version": POLICY_VERSION,
        "mode": "BLIND",
        "steps": steps,
        "final_status": final_status,
        "output_refs": list(output_refs),
    }
    return compile_inference_trace(payload)


def run_method_policy(
    *,
    case_id: str,
    target_domains: Sequence[str],
    evidence: Sequence[EvidenceItem],
    retrieved_cases: Sequence[RetrievalHit],
    patterns: Sequence[MethodPattern],
    execution_rules: Mapping[str, ExecutionRule],
) -> MethodPolicyRun:
    """Run deterministic π v0.1.

    The planner executes only derived procedural rules that pass:
    target scope, source action-sequence equality, and fully materialized
    required evidence.  It never emits canonical semantic conclusions.
    """

    target_tuple = tuple(str(item) for item in target_domains)
    if not target_tuple:
        raise ValueError("method policy target_domains cannot be empty")

    assessments = assess_patterns(
        patterns,
        execution_rules,
        target_domains=target_tuple,
        evidence=evidence,
    )
    ready_ids = sorted(
        item.pattern_id for item in assessments if item.executable
    )

    blockers: list[str] = []
    all_refs = _all_evidence_refs(evidence)

    if ready_ids:
        selected_id = ready_ids[0]
        pattern_by_id = {item.pattern_id: item for item in patterns}
        pattern = pattern_by_id[selected_id]
        rule = execution_rules[selected_id]

        materialized_refs = _evidence_refs_for_kinds(
            evidence, rule.required_evidence_kinds
        )
        if not materialized_refs:
            raise ValueError(
                f"{selected_id}: executable policy rule lacks materialized refs"
            )

        steps: list[dict[str, Any]] = []
        for ordinal, action in enumerate(rule.allowed_actions, start=1):
            steps.append(
                {
                    "step_id": f"S{ordinal}",
                    "ordinal": ordinal,
                    "action": action,
                    "evidence_refs": list(materialized_refs),
                    "canonical_rule_refs": [],
                    "temporal_layer": None,
                    "palace_targets": [],
                    "domain_targets": list(target_tuple),
                    "verifier_status": "VERIFIED",
                    "verifier_refs": [
                        f"POLICY_EXECUTION_RULE:{selected_id}",
                        "POLICY_STRUCTURAL_VERIFIER:V0_1",
                    ],
                }
            )

        if not steps or steps[-1]["action"] not in {"STOP", "ABSTAIN"}:
            ordinal = len(steps) + 1
            steps.append(
                {
                    "step_id": f"S{ordinal}",
                    "ordinal": ordinal,
                    "action": "STOP",
                    "evidence_refs": list(materialized_refs),
                    "canonical_rule_refs": [],
                    "temporal_layer": None,
                    "palace_targets": [],
                    "domain_targets": list(target_tuple),
                    "verifier_status": "VERIFIED",
                    "verifier_refs": [
                        f"POLICY_EXECUTION_RULE:{selected_id}",
                        "POLICY_STRUCTURAL_VERIFIER:V0_1",
                    ],
                }
            )

        trace = _build_trace(
            case_id=case_id,
            steps=steps,
            final_status="COMPLETED",
            output_refs=(f"METHOD_POLICY_PATH:{selected_id}",),
        )
        return MethodPolicyRun(
            trace=trace,
            retrieved_cases=tuple(retrieved_cases),
            pattern_assessments=assessments,
            selected_pattern_id=selected_id,
            blockers=(),
        )

    selected_id = None

    reference_only = [
        item for item in evidence if item.status == "SOURCE_REFERENCE_ONLY"
    ]
    if reference_only:
        blockers.append("MATERIALIZED_BLIND_EVIDENCE_REQUIRED")
    if any(item.status == "BLOCKED" for item in evidence):
        blockers.append("BLOCKED_EVIDENCE_PRESENT")
    if any(item.status == "MISSING" for item in evidence) or not evidence:
        blockers.append("BLIND_EVIDENCE_MISSING")

    targeted = [
        item
        for item in assessments
        if item.readiness != "NOT_TARGETED"
    ]
    if not targeted:
        blockers.append("NO_EXECUTABLE_PATTERN_FOR_TARGET_SCOPE")
    else:
        blockers.extend(
            blocker
            for item in targeted
            for blocker in item.blockers
        )

    blockers = list(dict.fromkeys(blockers))
    if not blockers:
        blockers.append("NO_EXECUTABLE_POLICY_PATH")

    inspect_refs = list(all_refs) or [f"EVIDENCE_MISSING:{case_id}"]
    steps = [
        {
            "step_id": "S1",
            "ordinal": 1,
            "action": "INSPECT",
            "evidence_refs": inspect_refs,
            "canonical_rule_refs": [],
            "temporal_layer": None,
            "palace_targets": [],
            "domain_targets": list(target_tuple),
            "verifier_status": "UNVERIFIED",
            "verifier_refs": [],
        },
        {
            "step_id": "S2",
            "ordinal": 2,
            "action": "ABSTAIN",
            "evidence_refs": [f"POLICY_BLOCKER:{item}" for item in blockers],
            "canonical_rule_refs": [],
            "temporal_layer": None,
            "palace_targets": [],
            "domain_targets": list(target_tuple),
            "verifier_status": "VERIFIED",
            "verifier_refs": [
                "POLICY_STRUCTURAL_VERIFIER:FAIL_CLOSED_V0_1"
            ],
        },
    ]

    trace = _build_trace(
        case_id=case_id,
        steps=steps,
        final_status="ABSTAINED",
        output_refs=tuple(f"POLICY_BLOCKER:{item}" for item in blockers),
    )
    return MethodPolicyRun(
        trace=trace,
        retrieved_cases=tuple(retrieved_cases),
        pattern_assessments=assessments,
        selected_pattern_id=selected_id,
        blockers=tuple(blockers),
    )


def run_wang_fold(
    held_out_case_id: str,
) -> MethodPolicyRun:
    bundles = load_wang_case_bundles()
    by_id = {item.case_id: item for item in bundles}
    if held_out_case_id not in by_id:
        raise ValueError(f"unknown Wang case: {held_out_case_id}")

    case = by_id[held_out_case_id]
    manifest = load_wang_loco_manifest()
    fold = _fold_for_case(manifest, held_out_case_id)
    hits = retrieve_same_domain_cases(case, fold, bundles)
    evidence = build_reference_only_evidence(case)
    patterns = load_wang_method_patterns()
    rules = load_execution_rules()

    return run_method_policy(
        case_id=case.case_id,
        target_domains=case.target.domains,
        evidence=evidence,
        retrieved_cases=hits,
        patterns=patterns,
        execution_rules=rules,
    )


def audit_wang_method_policy_readiness() -> dict[str, Any]:
    bundles = load_wang_case_bundles()
    by_id = {item.case_id: item for item in bundles}
    manifest = load_wang_loco_manifest()
    patterns = load_wang_method_patterns()
    rules = load_execution_rules()
    validate_execution_rule_coverage(patterns, rules)

    fold_rows: list[dict[str, Any]] = []
    retrieval_ready_count = 0
    action_selection_ready_count = 0
    full_replay_ready_count = 0

    for fold in manifest["folds"]:
        case_id = fold["held_out_case_id"]
        case = by_id[case_id]
        blind = build_blind_case_view(case)
        evidence = build_reference_only_evidence(case)
        hits = retrieve_same_domain_cases(case, fold, bundles)
        run = run_method_policy(
            case_id=case.case_id,
            target_domains=case.target.domains,
            evidence=evidence,
            retrieved_cases=hits,
            patterns=patterns,
            execution_rules=rules,
        )

        retrieval_ready = bool(hits)
        action_selection_ready = bool(run.trace.steps)
        full_replay_ready = run.trace.final_status == "COMPLETED"

        retrieval_ready_count += int(retrieval_ready)
        action_selection_ready_count += int(action_selection_ready)
        full_replay_ready_count += int(full_replay_ready)

        fold_rows.append(
            {
                "fold_id": fold["fold_id"],
                "held_out_case_id": case.case_id,
                "held_out_person_group_id": case.person_group_id,
                "target_domains": list(case.target.domains),
                "blind_view_fields": sorted(blind.keys()),
                "evidence_statuses": [
                    {
                        "evidence_id": item.evidence_id,
                        "kind": item.kind,
                        "status": item.status,
                        "refs": list(item.refs),
                    }
                    for item in evidence
                ],
                "retrieval_hits": [item.to_dict() for item in hits],
                "pattern_assessments": [
                    item.to_dict() for item in run.pattern_assessments
                ],
                "retrieval_ready": retrieval_ready,
                "action_selection_ready": action_selection_ready,
                "full_expert_replay_ready": full_replay_ready,
                "trace_final_status": run.trace.final_status,
                "blockers": list(run.blockers),
            }
        )

    return {
        "schema_version": "0.1",
        "artifact_id": "WANG_METHOD_POLICY_READINESS_V0_1",
        "policy_version": POLICY_VERSION,
        "corpus_id": manifest["corpus_id"],
        "fold_count": len(fold_rows),
        "summary": {
            "retrieval_ready": retrieval_ready_count,
            "action_selection_ready": action_selection_ready_count,
            "full_expert_replay_ready": full_replay_ready_count,
            "reference_only_fold_count": sum(
                1
                for row in fold_rows
                if any(
                    item["status"] == "SOURCE_REFERENCE_ONLY"
                    for item in row["evidence_statuses"]
                )
            ),
            "recommended_next_dependency": (
                "WANG_BLIND_EVIDENCE_MATERIALIZATION_V0_1"
                if full_replay_ready_count < len(fold_rows)
                else None
            ),
        },
        "folds": fold_rows,
        "maturity": {
            "deterministic_cbr": "IMPLEMENTED",
            "heuristic_symbolic_planner": "IMPLEMENTED_V0_1",
            "canonical_verifier_boundary": "IMPLEMENTED_V0_1",
            "wang_machine_expert_replay": (
                "READY"
                if full_replay_ready_count == len(fold_rows)
                else "NOT_READY"
            ),
            "method_fidelity": "NOT_VALIDATED",
            "predictive_validity": "NOT_VALIDATED",
        },
    }


def validate_retrieval_payload(payload: Mapping[str, Any]) -> None:
    serialized = json.dumps(payload, ensure_ascii=False).lower()
    for key in FORBIDDEN_RETRIEVAL_FIELDS:
        if key.lower() in serialized:
            raise ValueError(f"forbidden retrieval content exposed: {key}")

    if payload.get("retrieval_version") != "CBR_METADATA_ONLY_V0_1":
        raise ValueError("unexpected retrieval payload version")
    hits = payload.get("hits")
    if not isinstance(hits, list):
        raise ValueError("retrieval payload hits must be an array")
    for index, hit in enumerate(hits):
        if set(hit) != {
            "case_id",
            "person_group_id",
            "target_domains",
            "match_reasons",
        }:
            raise ValueError(
                f"retrieval hit {index} contains unsupported fields"
            )


def serialize_policy_run(run: MethodPolicyRun) -> dict[str, Any]:
    return run.to_dict()
