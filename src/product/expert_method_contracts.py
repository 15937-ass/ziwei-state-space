"""Product v0.4 expert-method case contracts.

These contracts represent auditable expert demonstrations and machine replay
traces. They deliberately do not store hidden chain-of-thought, create
canonical Ziwei rules, add probabilities, or promote case conclusions/outcomes
to source truth.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Mapping, Sequence


SCHEMA_VERSION = "0.1"

EXPERT_ACTIONS = frozenset(
    {
        "INSPECT",
        "CLASSIFY",
        "ACTIVATE",
        "COMPARE",
        "REFINE",
        "CROSS_CHECK",
        "REJECT",
        "CONFIRM",
        "ABSTAIN",
        "STOP",
    }
)

TERMINAL_ACTIONS = frozenset({"ABSTAIN", "STOP"})

EDGE_RELATIONS = frozenset(
    {
        "NEXT",
        "DEPENDS_ON",
        "REFINES",
        "CONFIRMS",
        "CONTRADICTS",
        "BRANCHES_TO",
    }
)

TEMPORAL_LAYERS = frozenset(
    {"NATAL", "DECADE", "SMALL_LIMIT", "YEAR", "MONTH", "DAY", "HOUR"}
)

EPISTEMIC_STATUSES = frozenset(
    {
        "SOURCE_EXPLICIT",
        "SOURCE_DEMONSTRATED",
        "RECONSTRUCTED",
        "INDUCED",
        "EMPIRICALLY_VALIDATED",
    }
)

ALLOWED_USES = frozenset(
    {
        "EXECUTABLE",
        "SEMANTIC_ONLY",
        "RETRIEVAL_ONLY",
        "CASE_SUPPORT_ONLY",
        "BLOCKED",
    }
)

CASE_ALLOWED_USES = frozenset({"RETRIEVAL_ONLY", "CASE_SUPPORT_ONLY", "BLOCKED"})

SCHOOL_COMPATIBILITY_BANDS = frozenset(
    {
        "IDENTICAL",
        "SEMANTIC_EQUIVALENT",
        "PROCEDURAL_COMPATIBLE",
        "SCHOOL_SPECIFIC",
        "CONFLICTING",
        "UNKNOWN",
    }
)

METHOD_TRANSFER_BANDS = frozenset(
    {"IDENTICAL", "SEMANTIC_EQUIVALENT", "PROCEDURAL_COMPATIBLE"}
)

REVIEW_STATUSES = frozenset(
    {
        "MODEL_EXTRACTED",
        "MODEL_SELF_REVIEWED",
        "SOURCE_SPAN_VERIFIED",
        "HUMAN_VERIFIED",
    }
)

TRACE_MODES = frozenset({"BLIND", "EXPERT_REPLAY", "DEVELOPMENT"})
TRACE_FINAL_STATUSES = frozenset({"COMPLETED", "ABSTAINED", "FAILED"})
VERIFIER_STATUSES = frozenset({"VERIFIED", "REJECTED", "UNVERIFIED"})

FORBIDDEN_HIDDEN_REASONING_KEYS = frozenset(
    {
        "chain_of_thought",
        "hidden_reasoning",
        "private_reasoning",
        "internal_reasoning",
        "cot",
        "scratchpad",
        "analysis_trace",
    }
)


def _normalize_key(value: Any) -> str:
    return str(value).strip().lower().replace("-", "_").replace(" ", "_")


def _reject_hidden_reasoning(value: Any, path: str = "payload") -> None:
    if isinstance(value, Mapping):
        for key, child in value.items():
            if _normalize_key(key) in FORBIDDEN_HIDDEN_REASONING_KEYS:
                raise ValueError(
                    f"{path}.{key}: hidden/free-form chain-of-thought fields are forbidden"
                )
            _reject_hidden_reasoning(child, f"{path}.{key}")
    elif isinstance(value, Sequence) and not isinstance(value, (str, bytes)):
        for index, child in enumerate(value):
            _reject_hidden_reasoning(child, f"{path}[{index}]")


def _object(value: Any, path: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise ValueError(f"{path} must be an object")
    return value


def _array(value: Any, path: str) -> Sequence[Any]:
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes)):
        raise ValueError(f"{path} must be an array")
    return value


def _strict_keys(
    value: Mapping[str, Any],
    *,
    allowed: set[str] | frozenset[str],
    path: str,
) -> None:
    extras = sorted(set(value) - set(allowed))
    if extras:
        raise ValueError(f"{path} contains unsupported fields: {', '.join(extras)}")


def _required_text(value: Any, path: str) -> str:
    text = str(value or "").strip()
    if not text:
        raise ValueError(f"{path} is required")
    return text


def _optional_text(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _text_tuple(value: Any, path: str) -> tuple[str, ...]:
    if value is None:
        return ()
    raw = _array(value, path)
    out: list[str] = []
    seen: set[str] = set()
    for index, item in enumerate(raw):
        text = _required_text(item, f"{path}[{index}]")
        if text not in seen:
            out.append(text)
            seen.add(text)
    return tuple(out)


def _ordered_text_tuple(value: Any, path: str) -> tuple[str, ...]:
    if value is None:
        return ()
    raw = _array(value, path)
    return tuple(
        _required_text(item, f"{path}[{index}]")
        for index, item in enumerate(raw)
    )


def _enum(value: Any, allowed: frozenset[str], path: str) -> str:
    text = _required_text(value, path)
    if text not in allowed:
        raise ValueError(f"{path} has unsupported value: {text}")
    return text


def _optional_temporal_layer(value: Any, path: str) -> str | None:
    text = _optional_text(value)
    if text is None:
        return None
    if text not in TEMPORAL_LAYERS:
        raise ValueError(f"{path} has unsupported temporal layer: {text}")
    return text


def _serialize(value: Any) -> Any:
    if isinstance(value, tuple):
        return [_serialize(item) for item in value]
    if hasattr(value, "__dataclass_fields__"):
        return {key: _serialize(item) for key, item in asdict(value).items()}
    if isinstance(value, dict):
        return {key: _serialize(item) for key, item in value.items()}
    return value


@dataclass(frozen=True)
class CaseSource:
    source_id: str
    school: str
    author: str
    artifact_ref: str
    artifact_type: str
    source_span_refs: tuple[str, ...]
    review_status: str

    def __post_init__(self) -> None:
        for value, field in (
            (self.source_id, "source_id"),
            (self.school, "school"),
            (self.author, "author"),
            (self.artifact_ref, "artifact_ref"),
            (self.artifact_type, "artifact_type"),
        ):
            if not value.strip():
                raise ValueError(f"CaseSource.{field} is required")
        if not self.source_span_refs:
            raise ValueError("CaseSource.source_span_refs cannot be empty")
        if self.review_status not in REVIEW_STATUSES:
            raise ValueError(f"unsupported source review_status: {self.review_status}")


@dataclass(frozen=True)
class CaseTarget:
    question_ref: str
    domains: tuple[str, ...]
    target_time_label: str | None = None

    def __post_init__(self) -> None:
        if not self.question_ref.strip():
            raise ValueError("CaseTarget.question_ref is required")
        if not self.domains:
            raise ValueError("CaseTarget.domains cannot be empty")


@dataclass(frozen=True)
class ReasoningNode:
    node_id: str
    action: str
    evidence_refs: tuple[str, ...]
    canonical_rule_refs: tuple[str, ...]
    temporal_layer: str | None
    palace_targets: tuple[str, ...]
    domain_targets: tuple[str, ...]
    source_span_refs: tuple[str, ...]
    epistemic_status: str
    allowed_use: str

    def __post_init__(self) -> None:
        if not self.node_id.strip():
            raise ValueError("ReasoningNode.node_id is required")
        if self.action not in EXPERT_ACTIONS:
            raise ValueError(f"unsupported expert action: {self.action}")
        if self.temporal_layer is not None and self.temporal_layer not in TEMPORAL_LAYERS:
            raise ValueError(f"unsupported temporal layer: {self.temporal_layer}")
        if self.epistemic_status not in EPISTEMIC_STATUSES:
            raise ValueError(f"unsupported epistemic_status: {self.epistemic_status}")
        if self.allowed_use not in ALLOWED_USES:
            raise ValueError(f"unsupported allowed_use: {self.allowed_use}")
        if not (
            self.evidence_refs
            or self.canonical_rule_refs
            or self.source_span_refs
        ):
            raise ValueError(
                f"{self.node_id}: auditable reasoning node requires evidence/rule/source refs"
            )


@dataclass(frozen=True)
class ReasoningEdge:
    edge_id: str
    source: str
    target: str
    relation: str

    def __post_init__(self) -> None:
        if not self.edge_id.strip():
            raise ValueError("ReasoningEdge.edge_id is required")
        if not self.source.strip() or not self.target.strip():
            raise ValueError("ReasoningEdge source and target are required")
        if self.relation not in EDGE_RELATIONS:
            raise ValueError(f"unsupported reasoning edge relation: {self.relation}")


@dataclass(frozen=True)
class ExpertReasoningGraph:
    graph_id: str
    nodes: tuple[ReasoningNode, ...]
    edges: tuple[ReasoningEdge, ...]

    def __post_init__(self) -> None:
        if not self.graph_id.strip():
            raise ValueError("ExpertReasoningGraph.graph_id is required")
        if not self.nodes:
            raise ValueError("ExpertReasoningGraph.nodes cannot be empty")

        node_ids = [item.node_id for item in self.nodes]
        if len(node_ids) != len(set(node_ids)):
            raise ValueError("ExpertReasoningGraph contains duplicate node_id")
        edge_ids = [item.edge_id for item in self.edges]
        if len(edge_ids) != len(set(edge_ids)):
            raise ValueError("ExpertReasoningGraph contains duplicate edge_id")

        known = set(node_ids)
        adjacency: dict[str, list[str]] = {node_id: [] for node_id in node_ids}
        for edge in self.edges:
            if edge.source not in known or edge.target not in known:
                raise ValueError(
                    f"{edge.edge_id}: reasoning edge endpoint does not exist"
                )
            adjacency[edge.source].append(edge.target)

        terminal_ids = {
            item.node_id for item in self.nodes if item.action in TERMINAL_ACTIONS
        }
        for terminal_id in terminal_ids:
            if adjacency[terminal_id]:
                raise ValueError(
                    f"{terminal_id}: STOP/ABSTAIN nodes must be terminal"
                )

        visiting: set[str] = set()
        visited: set[str] = set()

        def visit(node_id: str) -> None:
            if node_id in visiting:
                raise ValueError("ExpertReasoningGraph must be acyclic")
            if node_id in visited:
                return
            visiting.add(node_id)
            for child in adjacency[node_id]:
                visit(child)
            visiting.remove(node_id)
            visited.add(node_id)

        for node_id in node_ids:
            visit(node_id)

    def to_dict(self) -> dict[str, Any]:
        return _serialize(self)


@dataclass(frozen=True)
class CaseBundle:
    schema_version: str
    case_id: str
    person_group_id: str
    source: CaseSource
    chart_snapshot_ref: str | None
    input_refs: tuple[str, ...]
    target: CaseTarget
    available_information_refs: tuple[str, ...]
    expert_reasoning_graph: ExpertReasoningGraph
    expert_conclusion_refs: tuple[str, ...]
    outcome_refs: tuple[str, ...]
    epistemic_status: str
    allowed_use: str

    def __post_init__(self) -> None:
        if self.schema_version != SCHEMA_VERSION:
            raise ValueError(f"CaseBundle schema_version must be {SCHEMA_VERSION}")
        if not self.case_id.strip():
            raise ValueError("CaseBundle.case_id is required")
        if not self.person_group_id.strip():
            raise ValueError("CaseBundle.person_group_id is required")
        if not self.input_refs:
            raise ValueError("CaseBundle.input_refs cannot be empty")
        if not self.available_information_refs:
            raise ValueError(
                "CaseBundle.available_information_refs cannot be empty"
            )
        if self.epistemic_status not in EPISTEMIC_STATUSES:
            raise ValueError(f"unsupported case epistemic_status: {self.epistemic_status}")
        if self.allowed_use not in CASE_ALLOWED_USES:
            raise ValueError(
                "expert cases cannot be canonical executable truth; "
                f"unsupported case allowed_use: {self.allowed_use}"
            )

    def to_dict(self) -> dict[str, Any]:
        return _serialize(self)


@dataclass(frozen=True)
class TraceStep:
    step_id: str
    ordinal: int
    action: str
    evidence_refs: tuple[str, ...]
    canonical_rule_refs: tuple[str, ...]
    temporal_layer: str | None
    palace_targets: tuple[str, ...]
    domain_targets: tuple[str, ...]
    verifier_status: str
    verifier_refs: tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.step_id.strip():
            raise ValueError("TraceStep.step_id is required")
        if self.ordinal < 1:
            raise ValueError("TraceStep.ordinal must be >= 1")
        if self.action not in EXPERT_ACTIONS:
            raise ValueError(f"unsupported trace action: {self.action}")
        if self.temporal_layer is not None and self.temporal_layer not in TEMPORAL_LAYERS:
            raise ValueError(f"unsupported temporal layer: {self.temporal_layer}")
        if self.verifier_status not in VERIFIER_STATUSES:
            raise ValueError(f"unsupported verifier_status: {self.verifier_status}")
        if self.verifier_status == "VERIFIED" and not self.verifier_refs:
            raise ValueError("VERIFIED trace step requires verifier_refs")


@dataclass(frozen=True)
class InferenceTrace:
    schema_version: str
    trace_id: str
    case_id: str
    policy_version: str
    mode: str
    steps: tuple[TraceStep, ...]
    final_status: str
    output_refs: tuple[str, ...]

    def __post_init__(self) -> None:
        if self.schema_version != SCHEMA_VERSION:
            raise ValueError(f"InferenceTrace schema_version must be {SCHEMA_VERSION}")
        for value, field in (
            (self.trace_id, "trace_id"),
            (self.case_id, "case_id"),
            (self.policy_version, "policy_version"),
        ):
            if not value.strip():
                raise ValueError(f"InferenceTrace.{field} is required")
        if self.mode not in TRACE_MODES:
            raise ValueError(f"unsupported trace mode: {self.mode}")
        if self.final_status not in TRACE_FINAL_STATUSES:
            raise ValueError(f"unsupported trace final_status: {self.final_status}")
        if not self.steps:
            raise ValueError("InferenceTrace.steps cannot be empty")

        step_ids = [item.step_id for item in self.steps]
        if len(step_ids) != len(set(step_ids)):
            raise ValueError("InferenceTrace contains duplicate step_id")

        ordinals = [item.ordinal for item in self.steps]
        if ordinals != list(range(1, len(self.steps) + 1)):
            raise ValueError("InferenceTrace ordinals must be contiguous from 1")

        for step in self.steps[:-1]:
            if step.action in TERMINAL_ACTIONS:
                raise ValueError("STOP/ABSTAIN trace action must be the final step")

        final_action = self.steps[-1].action
        if self.final_status == "COMPLETED" and final_action != "STOP":
            raise ValueError("COMPLETED trace must end with STOP")
        if self.final_status == "ABSTAINED" and final_action != "ABSTAIN":
            raise ValueError("ABSTAINED trace must end with ABSTAIN")

    def to_dict(self) -> dict[str, Any]:
        return _serialize(self)


@dataclass(frozen=True)
class MethodPattern:
    schema_version: str
    pattern_id: str
    label: str
    maturity: str
    allowed_use: str
    school_scope: tuple[str, ...]
    source_case_refs: tuple[str, ...]
    source_span_refs: tuple[str, ...]
    action_sequence: tuple[str, ...]
    required_evidence_kinds: tuple[str, ...]
    target_domains: tuple[str, ...]
    review_status: str

    def __post_init__(self) -> None:
        if self.schema_version != SCHEMA_VERSION:
            raise ValueError(f"MethodPattern schema_version must be {SCHEMA_VERSION}")
        if not self.pattern_id.strip() or not self.label.strip():
            raise ValueError("MethodPattern pattern_id and label are required")
        if self.maturity not in EPISTEMIC_STATUSES:
            raise ValueError(f"unsupported method maturity: {self.maturity}")
        if self.allowed_use not in ALLOWED_USES:
            raise ValueError(f"unsupported method allowed_use: {self.allowed_use}")
        if not self.school_scope:
            raise ValueError("MethodPattern.school_scope cannot be empty")
        if not self.action_sequence:
            raise ValueError("MethodPattern.action_sequence cannot be empty")
        for action in self.action_sequence:
            if action not in EXPERT_ACTIONS:
                raise ValueError(f"unsupported method action: {action}")
        for action in self.action_sequence[:-1]:
            if action in TERMINAL_ACTIONS:
                raise ValueError("terminal method action may only appear last")
        if self.review_status not in REVIEW_STATUSES:
            raise ValueError(f"unsupported method review_status: {self.review_status}")

        if self.maturity == "SOURCE_EXPLICIT" and not self.source_span_refs:
            raise ValueError("SOURCE_EXPLICIT method requires source_span_refs")
        if self.maturity in {
            "SOURCE_DEMONSTRATED",
            "RECONSTRUCTED",
            "INDUCED",
        } and not self.source_case_refs:
            raise ValueError(f"{self.maturity} method requires source_case_refs")

    def to_dict(self) -> dict[str, Any]:
        return _serialize(self)


@dataclass(frozen=True)
class SchoolCompatibility:
    schema_version: str
    compatibility_id: str
    source_school: str
    target_school: str
    band: str
    artifact_refs: tuple[str, ...]
    source_span_refs: tuple[str, ...]
    review_status: str
    canonical_merge_allowed: bool = False

    def __post_init__(self) -> None:
        if self.schema_version != SCHEMA_VERSION:
            raise ValueError(
                f"SchoolCompatibility schema_version must be {SCHEMA_VERSION}"
            )
        for value, field in (
            (self.compatibility_id, "compatibility_id"),
            (self.source_school, "source_school"),
            (self.target_school, "target_school"),
        ):
            if not value.strip():
                raise ValueError(f"SchoolCompatibility.{field} is required")
        if self.band not in SCHOOL_COMPATIBILITY_BANDS:
            raise ValueError(f"unsupported school compatibility band: {self.band}")
        if not self.artifact_refs:
            raise ValueError("SchoolCompatibility.artifact_refs cannot be empty")
        if self.review_status not in REVIEW_STATUSES:
            raise ValueError(
                f"unsupported compatibility review_status: {self.review_status}"
            )
        if self.canonical_merge_allowed:
            raise ValueError(
                "cross-school compatibility may not mutate canonical school truth"
            )

    @property
    def method_transfer_allowed(self) -> bool:
        return self.band in METHOD_TRANSFER_BANDS

    def to_dict(self) -> dict[str, Any]:
        out = _serialize(self)
        out["method_transfer_allowed"] = self.method_transfer_allowed
        return out


def _compile_case_source(raw: Any) -> CaseSource:
    value = _object(raw, "case_bundle.source")
    _strict_keys(
        value,
        allowed={
            "source_id",
            "school",
            "author",
            "artifact_ref",
            "artifact_type",
            "source_span_refs",
            "review_status",
        },
        path="case_bundle.source",
    )
    return CaseSource(
        source_id=_required_text(value.get("source_id"), "case_bundle.source.source_id"),
        school=_required_text(value.get("school"), "case_bundle.source.school"),
        author=_required_text(value.get("author"), "case_bundle.source.author"),
        artifact_ref=_required_text(
            value.get("artifact_ref"), "case_bundle.source.artifact_ref"
        ),
        artifact_type=_required_text(
            value.get("artifact_type"), "case_bundle.source.artifact_type"
        ),
        source_span_refs=_text_tuple(
            value.get("source_span_refs"), "case_bundle.source.source_span_refs"
        ),
        review_status=_enum(
            value.get("review_status"),
            REVIEW_STATUSES,
            "case_bundle.source.review_status",
        ),
    )


def _compile_case_target(raw: Any) -> CaseTarget:
    value = _object(raw, "case_bundle.target")
    _strict_keys(
        value,
        allowed={"question_ref", "domains", "target_time_label"},
        path="case_bundle.target",
    )
    return CaseTarget(
        question_ref=_required_text(
            value.get("question_ref"), "case_bundle.target.question_ref"
        ),
        domains=_text_tuple(value.get("domains"), "case_bundle.target.domains"),
        target_time_label=_optional_text(value.get("target_time_label")),
    )


def _compile_reasoning_node(raw: Any, index: int) -> ReasoningNode:
    path = f"expert_reasoning_graph.nodes[{index}]"
    value = _object(raw, path)
    _strict_keys(
        value,
        allowed={
            "node_id",
            "action",
            "evidence_refs",
            "canonical_rule_refs",
            "temporal_layer",
            "palace_targets",
            "domain_targets",
            "source_span_refs",
            "epistemic_status",
            "allowed_use",
        },
        path=path,
    )
    return ReasoningNode(
        node_id=_required_text(value.get("node_id"), f"{path}.node_id"),
        action=_enum(value.get("action"), EXPERT_ACTIONS, f"{path}.action"),
        evidence_refs=_text_tuple(value.get("evidence_refs"), f"{path}.evidence_refs"),
        canonical_rule_refs=_text_tuple(
            value.get("canonical_rule_refs"), f"{path}.canonical_rule_refs"
        ),
        temporal_layer=_optional_temporal_layer(
            value.get("temporal_layer"), f"{path}.temporal_layer"
        ),
        palace_targets=_text_tuple(
            value.get("palace_targets"), f"{path}.palace_targets"
        ),
        domain_targets=_text_tuple(
            value.get("domain_targets"), f"{path}.domain_targets"
        ),
        source_span_refs=_text_tuple(
            value.get("source_span_refs"), f"{path}.source_span_refs"
        ),
        epistemic_status=_enum(
            value.get("epistemic_status"),
            EPISTEMIC_STATUSES,
            f"{path}.epistemic_status",
        ),
        allowed_use=_enum(
            value.get("allowed_use"), ALLOWED_USES, f"{path}.allowed_use"
        ),
    )


def _compile_reasoning_edge(raw: Any, index: int) -> ReasoningEdge:
    path = f"expert_reasoning_graph.edges[{index}]"
    value = _object(raw, path)
    _strict_keys(
        value,
        allowed={"edge_id", "source", "target", "relation"},
        path=path,
    )
    return ReasoningEdge(
        edge_id=_required_text(value.get("edge_id"), f"{path}.edge_id"),
        source=_required_text(value.get("source"), f"{path}.source"),
        target=_required_text(value.get("target"), f"{path}.target"),
        relation=_enum(value.get("relation"), EDGE_RELATIONS, f"{path}.relation"),
    )


def compile_expert_reasoning_graph(raw: Any) -> ExpertReasoningGraph:
    _reject_hidden_reasoning(raw, "expert_reasoning_graph")
    value = _object(raw, "expert_reasoning_graph")
    _strict_keys(
        value,
        allowed={"graph_id", "nodes", "edges"},
        path="expert_reasoning_graph",
    )
    nodes_raw = _array(value.get("nodes"), "expert_reasoning_graph.nodes")
    edges_raw = _array(value.get("edges", []), "expert_reasoning_graph.edges")
    return ExpertReasoningGraph(
        graph_id=_required_text(
            value.get("graph_id"), "expert_reasoning_graph.graph_id"
        ),
        nodes=tuple(
            _compile_reasoning_node(item, index)
            for index, item in enumerate(nodes_raw)
        ),
        edges=tuple(
            _compile_reasoning_edge(item, index)
            for index, item in enumerate(edges_raw)
        ),
    )


def compile_case_bundle(payload: Mapping[str, Any]) -> CaseBundle:
    """Compile one expert case without promoting it to canonical truth."""

    _reject_hidden_reasoning(payload, "case_bundle")
    value = _object(payload, "case_bundle")
    _strict_keys(
        value,
        allowed={
            "schema_version",
            "case_id",
            "person_group_id",
            "source",
            "chart_snapshot_ref",
            "input_refs",
            "target",
            "available_information_refs",
            "expert_reasoning_graph",
            "expert_conclusion_refs",
            "outcome_refs",
            "epistemic_status",
            "allowed_use",
        },
        path="case_bundle",
    )
    expert_graph = compile_expert_reasoning_graph(
        value.get("expert_reasoning_graph")
    )
    executable_case_nodes = [
        node.node_id
        for node in expert_graph.nodes
        if node.allowed_use not in CASE_ALLOWED_USES
    ]
    if executable_case_nodes:
        raise ValueError(
            "expert case reasoning nodes cannot become canonical executable truth: "
            + ", ".join(executable_case_nodes)
        )

    return CaseBundle(
        schema_version=_required_text(
            value.get("schema_version"), "case_bundle.schema_version"
        ),
        case_id=_required_text(value.get("case_id"), "case_bundle.case_id"),
        person_group_id=_required_text(
            value.get("person_group_id"), "case_bundle.person_group_id"
        ),
        source=_compile_case_source(value.get("source")),
        chart_snapshot_ref=_optional_text(value.get("chart_snapshot_ref")),
        input_refs=_text_tuple(value.get("input_refs"), "case_bundle.input_refs"),
        target=_compile_case_target(value.get("target")),
        available_information_refs=_text_tuple(
            value.get("available_information_refs"),
            "case_bundle.available_information_refs",
        ),
        expert_reasoning_graph=expert_graph,
        expert_conclusion_refs=_text_tuple(
            value.get("expert_conclusion_refs"),
            "case_bundle.expert_conclusion_refs",
        ),
        outcome_refs=_text_tuple(
            value.get("outcome_refs", []), "case_bundle.outcome_refs"
        ),
        epistemic_status=_enum(
            value.get("epistemic_status"),
            EPISTEMIC_STATUSES,
            "case_bundle.epistemic_status",
        ),
        allowed_use=_enum(
            value.get("allowed_use"), ALLOWED_USES, "case_bundle.allowed_use"
        ),
    )


def _compile_trace_step(raw: Any, index: int) -> TraceStep:
    path = f"inference_trace.steps[{index}]"
    value = _object(raw, path)
    _strict_keys(
        value,
        allowed={
            "step_id",
            "ordinal",
            "action",
            "evidence_refs",
            "canonical_rule_refs",
            "temporal_layer",
            "palace_targets",
            "domain_targets",
            "verifier_status",
            "verifier_refs",
        },
        path=path,
    )
    ordinal = value.get("ordinal")
    if not isinstance(ordinal, int) or isinstance(ordinal, bool):
        raise ValueError(f"{path}.ordinal must be an integer")
    return TraceStep(
        step_id=_required_text(value.get("step_id"), f"{path}.step_id"),
        ordinal=ordinal,
        action=_enum(value.get("action"), EXPERT_ACTIONS, f"{path}.action"),
        evidence_refs=_text_tuple(value.get("evidence_refs"), f"{path}.evidence_refs"),
        canonical_rule_refs=_text_tuple(
            value.get("canonical_rule_refs"), f"{path}.canonical_rule_refs"
        ),
        temporal_layer=_optional_temporal_layer(
            value.get("temporal_layer"), f"{path}.temporal_layer"
        ),
        palace_targets=_text_tuple(
            value.get("palace_targets"), f"{path}.palace_targets"
        ),
        domain_targets=_text_tuple(
            value.get("domain_targets"), f"{path}.domain_targets"
        ),
        verifier_status=_enum(
            value.get("verifier_status"),
            VERIFIER_STATUSES,
            f"{path}.verifier_status",
        ),
        verifier_refs=_text_tuple(
            value.get("verifier_refs"), f"{path}.verifier_refs"
        ),
    )


def compile_inference_trace(payload: Mapping[str, Any]) -> InferenceTrace:
    """Compile a machine replay trace, kept separate from expert evidence."""

    _reject_hidden_reasoning(payload, "inference_trace")
    value = _object(payload, "inference_trace")
    _strict_keys(
        value,
        allowed={
            "schema_version",
            "trace_id",
            "case_id",
            "policy_version",
            "mode",
            "steps",
            "final_status",
            "output_refs",
        },
        path="inference_trace",
    )
    steps_raw = _array(value.get("steps"), "inference_trace.steps")
    return InferenceTrace(
        schema_version=_required_text(
            value.get("schema_version"), "inference_trace.schema_version"
        ),
        trace_id=_required_text(value.get("trace_id"), "inference_trace.trace_id"),
        case_id=_required_text(value.get("case_id"), "inference_trace.case_id"),
        policy_version=_required_text(
            value.get("policy_version"), "inference_trace.policy_version"
        ),
        mode=_enum(value.get("mode"), TRACE_MODES, "inference_trace.mode"),
        steps=tuple(
            _compile_trace_step(item, index)
            for index, item in enumerate(steps_raw)
        ),
        final_status=_enum(
            value.get("final_status"),
            TRACE_FINAL_STATUSES,
            "inference_trace.final_status",
        ),
        output_refs=_text_tuple(
            value.get("output_refs", []), "inference_trace.output_refs"
        ),
    )


def compile_method_pattern(payload: Mapping[str, Any]) -> MethodPattern:
    _reject_hidden_reasoning(payload, "method_pattern")
    value = _object(payload, "method_pattern")
    _strict_keys(
        value,
        allowed={
            "schema_version",
            "pattern_id",
            "label",
            "maturity",
            "allowed_use",
            "school_scope",
            "source_case_refs",
            "source_span_refs",
            "action_sequence",
            "required_evidence_kinds",
            "target_domains",
            "review_status",
        },
        path="method_pattern",
    )
    actions = _ordered_text_tuple(
        value.get("action_sequence"), "method_pattern.action_sequence"
    )
    return MethodPattern(
        schema_version=_required_text(
            value.get("schema_version"), "method_pattern.schema_version"
        ),
        pattern_id=_required_text(
            value.get("pattern_id"), "method_pattern.pattern_id"
        ),
        label=_required_text(value.get("label"), "method_pattern.label"),
        maturity=_enum(
            value.get("maturity"), EPISTEMIC_STATUSES, "method_pattern.maturity"
        ),
        allowed_use=_enum(
            value.get("allowed_use"), ALLOWED_USES, "method_pattern.allowed_use"
        ),
        school_scope=_text_tuple(
            value.get("school_scope"), "method_pattern.school_scope"
        ),
        source_case_refs=_text_tuple(
            value.get("source_case_refs", []), "method_pattern.source_case_refs"
        ),
        source_span_refs=_text_tuple(
            value.get("source_span_refs", []), "method_pattern.source_span_refs"
        ),
        action_sequence=actions,
        required_evidence_kinds=_text_tuple(
            value.get("required_evidence_kinds", []),
            "method_pattern.required_evidence_kinds",
        ),
        target_domains=_text_tuple(
            value.get("target_domains", []), "method_pattern.target_domains"
        ),
        review_status=_enum(
            value.get("review_status"),
            REVIEW_STATUSES,
            "method_pattern.review_status",
        ),
    )


def compile_school_compatibility(payload: Mapping[str, Any]) -> SchoolCompatibility:
    _reject_hidden_reasoning(payload, "school_compatibility")
    value = _object(payload, "school_compatibility")
    _strict_keys(
        value,
        allowed={
            "schema_version",
            "compatibility_id",
            "source_school",
            "target_school",
            "band",
            "artifact_refs",
            "source_span_refs",
            "review_status",
            "canonical_merge_allowed",
        },
        path="school_compatibility",
    )
    canonical_merge_allowed = value.get("canonical_merge_allowed", False)
    if not isinstance(canonical_merge_allowed, bool):
        raise ValueError("school_compatibility.canonical_merge_allowed must be boolean")
    return SchoolCompatibility(
        schema_version=_required_text(
            value.get("schema_version"), "school_compatibility.schema_version"
        ),
        compatibility_id=_required_text(
            value.get("compatibility_id"),
            "school_compatibility.compatibility_id",
        ),
        source_school=_required_text(
            value.get("source_school"), "school_compatibility.source_school"
        ),
        target_school=_required_text(
            value.get("target_school"), "school_compatibility.target_school"
        ),
        band=_enum(
            value.get("band"),
            SCHOOL_COMPATIBILITY_BANDS,
            "school_compatibility.band",
        ),
        artifact_refs=_text_tuple(
            value.get("artifact_refs"), "school_compatibility.artifact_refs"
        ),
        source_span_refs=_text_tuple(
            value.get("source_span_refs", []),
            "school_compatibility.source_span_refs",
        ),
        review_status=_enum(
            value.get("review_status"),
            REVIEW_STATUSES,
            "school_compatibility.review_status",
        ),
        canonical_merge_allowed=canonical_merge_allowed,
    )


def compile_contract_fixture(payload: Mapping[str, Any]) -> dict[str, Any]:
    """Compile the four v0.1 contract objects from one deterministic fixture."""

    _reject_hidden_reasoning(payload, "fixture")
    value = _object(payload, "fixture")
    _strict_keys(
        value,
        allowed={
            "case_bundle",
            "inference_trace",
            "method_pattern",
            "school_compatibility",
        },
        path="fixture",
    )
    return {
        "case_bundle": compile_case_bundle(
            _object(value.get("case_bundle"), "fixture.case_bundle")
        ),
        "inference_trace": compile_inference_trace(
            _object(value.get("inference_trace"), "fixture.inference_trace")
        ),
        "method_pattern": compile_method_pattern(
            _object(value.get("method_pattern"), "fixture.method_pattern")
        ),
        "school_compatibility": compile_school_compatibility(
            _object(
                value.get("school_compatibility"),
                "fixture.school_compatibility",
            )
        ),
    }
