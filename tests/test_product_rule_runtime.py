import pytest

from src.product.condition_atoms import compile_condition_spec, fact_from_atom
from src.product.rule_runtime import (
    CompileDisposition,
    RuleRuntime,
    RuntimeState,
    compile_rule_row,
    compile_rule_rows,
)


def _row(**overrides):
    row = {
        "rule_id": "ZZ-TEST-001",
        "school": "中州派",
        "source_work": "测试来源",
        "source_location": "p1",
        "subject": "紫微",
        "context": "general",
        "condition": "无",
        "time_scope": '["natal"]',
        "palace_scope": '["命宫"]',
        "topic_scope": "事业|财帛",
        "operator": "enhance",
        "target_type": "qi_state",
        "target_normalized": "领导力",
        "state_change": "increase",
        "valence": "context_dependent",
        "source_epistemic": "EXPLICIT",
        "normalization_epistemic": "SOURCE_PRESERVING",
        "review_status": "SOURCE_SPAN_VERIFIED",
        "source_span_verified": "true",
        "normalization_verified": "true",
        "evidence_text": "test",
    }
    row.update(overrides)
    return row


def test_unverified_rule_is_not_executable():
    ir, issue = compile_rule_row(_row(source_span_verified="false"))
    assert ir is None
    assert issue.disposition is CompileDisposition.BLOCKED_PROVENANCE


def test_free_text_condition_requires_explicit_atoms():
    row = _row(condition="文昌文曲会合")
    ir, issue = compile_rule_row(row)
    assert ir is None
    assert issue.disposition is CompileDisposition.NEEDS_CONDITION_NORMALIZATION

    ir, issue = compile_rule_row(
        row,
        condition_atoms=("star:文昌", "star:文曲", "relation:会合"),
    )
    assert issue is None
    assert ir is not None
    assert "relation:会合" in ir.required_facts


def test_structured_condition_can_use_any_and_none():
    row = _row(condition="结构化条件")
    condition = compile_condition_spec(
        {
            "all_of": [
                {"atom_type": "PALACE_PRESENT", "args": {"palace": "P05"}}
            ],
            "any_of": [
                [
                    {"atom_type": "STAR_PRESENT", "args": {"star": "武曲"}},
                    {"atom_type": "STAR_PRESENT", "args": {"star": "天府"}},
                ]
            ],
            "none_of": [
                {"atom_type": "TAG_PRESENT", "args": {"tag": "QUARANTINED"}}
            ],
        }
    )
    ir, issue = compile_rule_row(row, condition_spec=condition)
    assert issue is None
    runtime = RuleRuntime([ir])

    facts = frozenset(
        {
            "subject:紫微",
            fact_from_atom("PALACE_PRESENT", palace="P05"),
            fact_from_atom("STAR_PRESENT", star="武曲"),
        }
    )
    graph = runtime.match(
        RuntimeState(
            facts=facts,
            latent_states={},
            time_scope="natal",
            palace_scope="命宫",
        ),
        question_scope="事业",
    )
    assert [node.rule_id for node in graph.nodes] == ["ZZ-TEST-001"]

    blocked = frozenset(
        set(facts) | {fact_from_atom("TAG_PRESENT", tag="QUARANTINED")}
    )
    graph = runtime.match(
        RuntimeState(
            facts=blocked,
            latent_states={},
            time_scope="natal",
            palace_scope="命宫",
        ),
        question_scope="事业",
    )
    assert graph.nodes == ()


def test_compilation_report_is_deterministic_and_counts_blocks():
    report = compile_rule_rows(
        [
            _row(rule_id="B"),
            _row(rule_id="A", normalization_verified="false"),
        ]
    )
    assert [r.rule_id for r in report.executable] == ["B"]
    assert report.counts()["EXECUTABLE"] == 1
    assert report.counts()["BLOCKED_NORMALIZATION"] == 1


def test_runtime_matches_scope_and_preserves_trace():
    ir, issue = compile_rule_row(_row())
    assert issue is None
    runtime = RuleRuntime([ir])

    graph = runtime.match(
        RuntimeState(
            facts=frozenset({"subject:紫微"}),
            latent_states={"领导力": "BASELINE"},
            time_scope="natal",
            palace_scope="命宫",
        ),
        question_scope="事业",
    )

    assert [n.rule_id for n in graph.nodes] == ["ZZ-TEST-001"]
    node = graph.nodes[0]
    assert node.before_state == "BASELINE"
    assert node.source_pointer == "测试来源::p1"
    assert node.after_state["operator"] == "enhance"


def test_runtime_does_not_match_wrong_scope():
    ir, _ = compile_rule_row(_row())
    runtime = RuleRuntime([ir])
    graph = runtime.match(
        RuntimeState(
            facts=frozenset({"subject:紫微"}),
            latent_states={},
            time_scope="year",
            palace_scope="命宫",
        ),
        question_scope="事业",
    )
    assert graph.nodes == ()


def test_runtime_rejects_duplicate_rule_ids():
    ir, _ = compile_rule_row(_row())
    with pytest.raises(ValueError):
        RuleRuntime([ir, ir])


def test_conflicts_are_exposed_not_silently_resolved():
    a, _ = compile_rule_row(_row(rule_id="A", conflict_group="CG-1"))
    b, _ = compile_rule_row(_row(rule_id="B", conflict_group="CG-1", operator="weaken"))
    runtime = RuleRuntime([a, b])
    graph = runtime.match(
        RuntimeState(
            facts=frozenset({"subject:紫微"}),
            latent_states={},
            time_scope="natal",
            palace_scope="命宫",
        ),
        question_scope="事业",
    )
    assert graph.conflict_groups == {"CG-1": ("A", "B")}
