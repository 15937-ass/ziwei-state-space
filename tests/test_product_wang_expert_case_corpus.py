import copy
import json
from collections import Counter
from pathlib import Path

import pytest

from src.product.expert_case_corpus import (
    BASE_DIR,
    BLIND_FORBIDDEN_FIELDS,
    BLIND_VISIBLE_FIELDS,
    build_blind_case_view,
    load_wang_case_bundles,
    load_wang_inventory,
    load_wang_loco_manifest,
    load_wang_method_patterns,
    validate_wang_case_bundles,
    validate_wang_expert_corpus,
    validate_wang_loco_manifest,
    validate_wang_source_inventory,
)


EXPECTED_SOURCE_LABELS = [
    "谭仪",
    "某女士",
    "诸葛亮",
    "某女士",
    "曾国藩",
    "陈公博",
    "杨森",
    "某女士",
    "蒋介石",
    "某男士",
    "宋子文",
    "某男士",
    "李纯",
    "某女童",
    "秦桧",
    "某女士",
    "慈禧",
    "某男士",
    "于佑任",
    "某男士",
    "黄金荣",
    "某男士",
    "汪精卫",
    "某男士",
]

EXPECTED_DOMAINS = {
    "PARENTS",
    "LIFE",
    "SIBLINGS",
    "SPOUSE",
    "CHILDREN",
    "WEALTH",
    "HEALTH",
    "TRAVEL",
    "FRIENDS",
    "CAREER",
    "PROPERTY",
    "FORTUNE_VIRTUE",
}


def test_wang_corpus_end_to_end_validation():
    report = validate_wang_expert_corpus()

    assert report["inventory"]["case_count"] == 24
    assert report["inventory"]["palace_topic_count"] == 12
    assert report["cases"]["case_count"] == 24
    assert report["cases"]["source_demonstrated_nodes"] == 72
    assert report["cases"]["reconstructed_nodes"] == 0
    assert report["methods"]["method_pattern_count"] == 6
    assert report["loco"]["fold_count"] == 24
    assert report["loco"]["held_out_once_count"] == 24


def test_source_inventory_matches_24_case_toc_order():
    inventory = load_wang_inventory()
    cases = inventory["cases"]

    assert [item["sequence"] for item in cases] == list(range(1, 25))
    assert [item["source_subject_label"] for item in cases] == EXPECTED_SOURCE_LABELS

    counts = Counter(item["domain"] for item in cases)
    assert set(counts) == EXPECTED_DOMAINS
    assert set(counts.values()) == {2}

    assert cases[0]["source_page_start"] == 7
    assert cases[-1]["source_page_end"] == 25
    assert inventory["source"]["toc_span_ref"] == "WANG-ANXING-TUIDUAN:P1:TOC"


def test_all_24_case_files_exist_and_compile():
    paths = sorted((BASE_DIR / "cases").glob("wang_case_*.json"))
    assert len(paths) == 24

    bundles = load_wang_case_bundles()
    assert len(bundles) == 24
    assert [case.case_id for case in bundles] == [
        f"WANG-CASE-{index:03d}" for index in range(1, 25)
    ]


def test_case_graphs_are_minimal_source_demonstrated_not_reconstructed():
    for case in load_wang_case_bundles():
        graph = case.expert_reasoning_graph
        assert [node.action for node in graph.nodes] == [
            "INSPECT",
            "CLASSIFY",
            "STOP",
        ]
        assert all(
            node.epistemic_status == "SOURCE_DEMONSTRATED"
            for node in graph.nodes
        )
        assert all(node.allowed_use == "CASE_SUPPORT_ONLY" for node in graph.nodes)
        assert case.epistemic_status == "SOURCE_DEMONSTRATED"
        assert case.allowed_use == "CASE_SUPPORT_ONLY"


def test_blind_view_excludes_expert_answer_outcome_and_source_identity():
    inventory = load_wang_inventory()
    labels_by_id = {
        item["case_id"]: item["source_subject_label"]
        for item in inventory["cases"]
    }

    for case in load_wang_case_bundles():
        blind = build_blind_case_view(case)

        assert set(blind) == set(BLIND_VISIBLE_FIELDS)
        assert not (set(blind) & BLIND_FORBIDDEN_FIELDS)

        serialized = json.dumps(blind, ensure_ascii=False)
        assert labels_by_id[case.case_id] not in serialized
        assert "expert_reasoning_graph" not in serialized
        assert "expert_conclusion_refs" not in serialized
        assert "outcome_refs" not in serialized


def test_case_files_do_not_embed_source_subject_labels():
    inventory = load_wang_inventory()
    named_labels = {
        item["source_subject_label"]
        for item in inventory["cases"]
        if item["subject_visibility"] == "PUBLIC_HISTORICAL"
    }

    for path in sorted((BASE_DIR / "cases").glob("wang_case_*.json")):
        raw = path.read_text(encoding="utf-8")
        for label in named_labels:
            assert label not in raw


def test_available_information_never_contains_conclusion_or_outcome():
    for case in load_wang_case_bundles():
        assert not (
            set(case.available_information_refs)
            & (set(case.expert_conclusion_refs) | set(case.outcome_refs))
        )


def test_method_patterns_are_source_explicit_and_not_executable():
    patterns = load_wang_method_patterns()
    assert [item.pattern_id for item in patterns] == [
        "WT-METHOD-001",
        "WT-METHOD-002",
        "WT-METHOD-003",
        "WT-METHOD-004",
        "WT-METHOD-005",
        "WT-METHOD-006",
    ]
    assert all(item.maturity == "SOURCE_EXPLICIT" for item in patterns)
    assert all(item.allowed_use == "SEMANTIC_ONLY" for item in patterns)
    assert all(item.source_span_refs for item in patterns)
    assert all("ZHONGZHOU" in item.school_scope for item in patterns)


def test_loco_has_24_deterministic_holdouts_and_23_training_cases_each():
    bundles = load_wang_case_bundles()
    manifest = load_wang_loco_manifest()
    folds = manifest["folds"]

    assert [fold["fold_id"] for fold in folds] == [
        f"WANG-LOCO-{index:03d}" for index in range(1, 25)
    ]
    assert [fold["held_out_case_id"] for fold in folds] == [
        f"WANG-CASE-{index:03d}" for index in range(1, 25)
    ]
    assert all(len(fold["train_case_ids"]) == 23 for fold in folds)
    assert all(len(fold["retrieval_case_ids"]) == 23 for fold in folds)

    by_id = {case.case_id: case for case in bundles}
    for fold in folds:
        held = fold["held_out_case_id"]
        held_group = fold["held_out_person_group_id"]
        assert held not in fold["train_case_ids"]
        assert held not in fold["retrieval_case_ids"]
        assert all(
            by_id[case_id].person_group_id != held_group
            for case_id in fold["train_case_ids"]
        )


def test_loco_validator_rejects_held_out_case_in_training_set():
    bundles = load_wang_case_bundles()
    manifest = copy.deepcopy(load_wang_loco_manifest())
    first = manifest["folds"][0]
    first["train_case_ids"][0] = first["held_out_case_id"]

    with pytest.raises(ValueError, match="train set is not exact leave-one-out"):
        validate_wang_loco_manifest(bundles, manifest)


def test_source_inventory_validator_rejects_unverified_span():
    inventory = copy.deepcopy(load_wang_inventory())
    inventory["cases"][0]["extraction_status"] = "MODEL_EXTRACTED"

    with pytest.raises(ValueError, match="source span must be verified"):
        validate_wang_source_inventory(inventory)


def test_case_bundle_validator_rejects_domain_drift_from_inventory():
    bundles = list(load_wang_case_bundles())
    inventory = copy.deepcopy(load_wang_inventory())

    inventory["cases"][0]["domain"] = "WRONG_DOMAIN"

    with pytest.raises(ValueError, match="domain mismatch"):
        validate_wang_case_bundles(tuple(bundles), inventory)


def test_no_probability_or_learned_weight_fields_in_case_payloads():
    forbidden = {
        "probability",
        "posterior",
        "weight",
        "learned_weight",
        "confidence_score",
        "reward",
    }

    for path in sorted((BASE_DIR / "cases").glob("wang_case_*.json")):
        payload = json.loads(path.read_text(encoding="utf-8"))

        def walk(value):
            if isinstance(value, dict):
                for key, child in value.items():
                    assert key not in forbidden
                    walk(child)
            elif isinstance(value, list):
                for child in value:
                    walk(child)

        walk(payload)


def test_no_hidden_reasoning_fields_in_wang_product_corpus():
    forbidden = {
        "chain_of_thought",
        "hidden_reasoning",
        "private_reasoning",
        "internal_reasoning",
        "cot",
        "scratchpad",
        "analysis_trace",
    }

    for path in [
        BASE_DIR / "CASE_SOURCE_INVENTORY_v0.1.json",
        BASE_DIR / "METHOD_PATTERNS_v0.1.json",
        BASE_DIR / "LOCO_FOLDS_v0.1.json",
        *sorted((BASE_DIR / "cases").glob("wang_case_*.json")),
    ]:
        payload = json.loads(path.read_text(encoding="utf-8"))

        def walk(value):
            if isinstance(value, dict):
                for key, child in value.items():
                    assert key not in forbidden
                    walk(child)
            elif isinstance(value, list):
                for child in value:
                    walk(child)

        walk(payload)
