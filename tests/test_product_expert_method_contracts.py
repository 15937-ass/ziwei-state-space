import copy
import json
from pathlib import Path

import pytest

from src.product.expert_method_contracts import (
    CaseBundle,
    ExpertReasoningGraph,
    InferenceTrace,
    MethodPattern,
    SchoolCompatibility,
    compile_case_bundle,
    compile_contract_fixture,
    compile_expert_reasoning_graph,
    compile_inference_trace,
    compile_method_pattern,
    compile_school_compatibility,
)


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "product" / "EXPERT_METHOD_SYNTHETIC_FIXTURE_v0.1.json"


def _load():
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


def test_synthetic_fixture_compiles_all_contracts():
    compiled = compile_contract_fixture(_load())

    assert isinstance(compiled["case_bundle"], CaseBundle)
    assert isinstance(
        compiled["case_bundle"].expert_reasoning_graph, ExpertReasoningGraph
    )
    assert isinstance(compiled["inference_trace"], InferenceTrace)
    assert isinstance(compiled["method_pattern"], MethodPattern)
    assert isinstance(compiled["school_compatibility"], SchoolCompatibility)

    assert compiled["case_bundle"].case_id == "SYNTHETIC-METHOD-CASE-001"
    assert compiled["case_bundle"].outcome_refs == ()
    assert compiled["inference_trace"].case_id == compiled["case_bundle"].case_id
    assert compiled["school_compatibility"].method_transfer_allowed is True
    assert compiled["school_compatibility"].canonical_merge_allowed is False


def test_case_outcome_is_optional_for_method_training():
    payload = _load()["case_bundle"]
    payload.pop("outcome_refs")

    case = compile_case_bundle(payload)
    assert case.outcome_refs == ()
    assert case.allowed_use == "CASE_SUPPORT_ONLY"


def test_blind_available_information_cannot_contain_expert_conclusion():
    payload = _load()["case_bundle"]
    payload["available_information_refs"].append("SPAN:CASE-001:CONCLUSION")

    with pytest.raises(ValueError, match="cannot contain expert conclusions/outcomes"):
        compile_case_bundle(payload)


def test_blind_available_information_cannot_contain_outcome():
    payload = _load()["case_bundle"]
    payload["outcome_refs"] = ["OUTCOME:SYNTHETIC-001"]
    payload["available_information_refs"].append("OUTCOME:SYNTHETIC-001")

    with pytest.raises(ValueError, match="cannot contain expert conclusions/outcomes"):
        compile_case_bundle(payload)


def test_case_bundle_cannot_be_marked_executable():
    payload = _load()["case_bundle"]
    payload["allowed_use"] = "EXECUTABLE"

    with pytest.raises(ValueError, match="cannot be canonical executable truth"):
        compile_case_bundle(payload)


def test_case_graph_node_cannot_silently_become_executable_truth():
    payload = _load()["case_bundle"]
    payload["expert_reasoning_graph"]["nodes"][0]["allowed_use"] = "EXECUTABLE"

    with pytest.raises(ValueError, match="cannot become canonical executable truth"):
        compile_case_bundle(payload)


def test_hidden_chain_of_thought_field_is_rejected_anywhere():
    payload = _load()["case_bundle"]
    payload["expert_reasoning_graph"]["nodes"][1]["chain_of_thought"] = (
        "forbidden free-form internal reasoning"
    )

    with pytest.raises(ValueError, match="chain-of-thought"):
        compile_case_bundle(payload)


def test_unknown_probability_field_fails_closed():
    payload = _load()["case_bundle"]
    payload["probability"] = 0.9

    with pytest.raises(ValueError, match="unsupported fields"):
        compile_case_bundle(payload)


def test_reasoning_graph_rejects_duplicate_node_ids():
    graph = _load()["case_bundle"]["expert_reasoning_graph"]
    graph["nodes"][1]["node_id"] = graph["nodes"][0]["node_id"]

    with pytest.raises(ValueError, match="duplicate node_id"):
        compile_expert_reasoning_graph(graph)


def test_reasoning_graph_rejects_unknown_edge_endpoint():
    graph = _load()["case_bundle"]["expert_reasoning_graph"]
    graph["edges"][0]["target"] = "MISSING-NODE"

    with pytest.raises(ValueError, match="endpoint does not exist"):
        compile_expert_reasoning_graph(graph)


def test_reasoning_graph_must_be_acyclic():
    graph = _load()["case_bundle"]["expert_reasoning_graph"]
    graph["edges"].append(
        {
            "edge_id": "E-CYCLE",
            "source": "N4",
            "target": "N2",
            "relation": "NEXT",
        }
    )

    with pytest.raises(ValueError, match="acyclic"):
        compile_expert_reasoning_graph(graph)


def test_stop_and_abstain_nodes_must_be_terminal():
    graph = _load()["case_bundle"]["expert_reasoning_graph"]
    graph["edges"].append(
        {
            "edge_id": "E-AFTER-STOP",
            "source": "N5",
            "target": "N1",
            "relation": "NEXT",
        }
    )

    with pytest.raises(ValueError, match="must be terminal"):
        compile_expert_reasoning_graph(graph)


def test_machine_inference_trace_is_separate_from_expert_graph():
    payload = _load()
    case = compile_case_bundle(payload["case_bundle"])
    trace = compile_inference_trace(payload["inference_trace"])

    assert isinstance(case.expert_reasoning_graph, ExpertReasoningGraph)
    assert isinstance(trace, InferenceTrace)
    assert case.expert_reasoning_graph.graph_id != trace.trace_id
    assert trace.mode == "EXPERT_REPLAY"
    assert trace.steps[-1].action == "STOP"


def test_completed_trace_must_end_with_stop():
    trace = _load()["inference_trace"]
    trace["steps"][-1]["action"] = "CONFIRM"

    with pytest.raises(ValueError, match="must end with STOP"):
        compile_inference_trace(trace)


def test_terminal_trace_action_cannot_appear_before_final_step():
    trace = _load()["inference_trace"]
    trace["steps"][1]["action"] = "ABSTAIN"

    with pytest.raises(ValueError, match="must be the final step"):
        compile_inference_trace(trace)


def test_verified_trace_step_requires_verifier_reference():
    trace = _load()["inference_trace"]
    trace["steps"][0]["verifier_refs"] = []

    with pytest.raises(ValueError, match="requires verifier_refs"):
        compile_inference_trace(trace)


def test_trace_step_requires_auditable_reference():
    trace = _load()["inference_trace"]
    step = trace["steps"][0]
    step["verifier_status"] = "UNVERIFIED"
    step["verifier_refs"] = []
    step["evidence_refs"] = []
    step["canonical_rule_refs"] = []

    with pytest.raises(ValueError, match="auditable trace step"):
        compile_inference_trace(trace)


def test_method_pattern_preserves_order_and_repeated_actions():
    pattern = _load()["method_pattern"]
    pattern["action_sequence"] = [
        "INSPECT",
        "CROSS_CHECK",
        "INSPECT",
        "STOP",
    ]

    compiled = compile_method_pattern(pattern)
    assert compiled.action_sequence == (
        "INSPECT",
        "CROSS_CHECK",
        "INSPECT",
        "STOP",
    )


def test_source_demonstrated_method_requires_case_provenance():
    pattern = _load()["method_pattern"]
    pattern["source_case_refs"] = []

    with pytest.raises(ValueError, match="requires source_case_refs"):
        compile_method_pattern(pattern)


def test_source_explicit_method_requires_source_span():
    pattern = _load()["method_pattern"]
    pattern["maturity"] = "SOURCE_EXPLICIT"
    pattern["source_span_refs"] = []

    with pytest.raises(ValueError, match="requires source_span_refs"):
        compile_method_pattern(pattern)


def test_school_compatibility_band_is_bounded():
    payload = _load()["school_compatibility"]
    payload["band"] = "SAME_ENOUGH"

    with pytest.raises(ValueError, match="unsupported school compatibility band"):
        compile_school_compatibility(payload)


def test_cross_school_compatibility_cannot_enable_canonical_merge():
    payload = _load()["school_compatibility"]
    payload["canonical_merge_allowed"] = True

    with pytest.raises(ValueError, match="may not mutate canonical school truth"):
        compile_school_compatibility(payload)


def test_conflicting_school_material_disables_method_transfer():
    payload = _load()["school_compatibility"]
    payload["band"] = "CONFLICTING"

    compiled = compile_school_compatibility(payload)
    assert compiled.method_transfer_allowed is False
    assert compiled.canonical_merge_allowed is False


def test_contract_serialization_contains_no_hidden_reasoning_field():
    compiled = compile_contract_fixture(_load())
    serialized = json.dumps(
        {
            "case": compiled["case_bundle"].to_dict(),
            "trace": compiled["inference_trace"].to_dict(),
            "method": compiled["method_pattern"].to_dict(),
            "compat": compiled["school_compatibility"].to_dict(),
        },
        ensure_ascii=False,
        sort_keys=True,
    ).lower()

    for forbidden in (
        "chain_of_thought",
        "hidden_reasoning",
        "private_reasoning",
        "internal_reasoning",
        "scratchpad",
        "analysis_trace",
    ):
        assert forbidden not in serialized


def test_combined_fixture_requires_trace_case_binding():
    payload = _load()
    payload["inference_trace"]["case_id"] = "OTHER-CASE"

    with pytest.raises(ValueError, match="must match case_bundle.case_id"):
        compile_contract_fixture(payload)


def test_fixture_is_not_mutated_by_compilers():
    payload = _load()
    before = copy.deepcopy(payload)
    compile_contract_fixture(payload)
    assert payload == before
