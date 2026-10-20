"""Wang Tingzhi expert-case corpus loader and LOCO validation.

This module consumes Product #431 expert-method contracts and the Product #441
source-structured corpus.  It deliberately exposes a blind-safe view that
omits expert reasoning, conclusions, outcomes and source subject labels.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import asdict
import json
from pathlib import Path
from typing import Any, Mapping

from src.product.expert_method_contracts import (
    CaseBundle,
    MethodPattern,
    compile_case_bundle,
    compile_method_pattern,
)


CORPUS_ID = "WANG_TINGZHI_ANXING_TUIDUAN_24_V0_1"
EXPECTED_CASE_COUNT = 24
EXPECTED_PALACE_TOPIC_COUNT = 12

BASE_DIR = (
    Path(__file__).resolve().parents[2]
    / "product"
    / "expert_cases"
    / "wang_tingzhi"
)
INVENTORY_PATH = BASE_DIR / "CASE_SOURCE_INVENTORY_v0.1.json"
METHOD_PATTERNS_PATH = BASE_DIR / "METHOD_PATTERNS_v0.1.json"
LOCO_PATH = BASE_DIR / "LOCO_FOLDS_v0.1.json"
CASES_DIR = BASE_DIR / "cases"

BLIND_VISIBLE_FIELDS = (
    "case_id",
    "person_group_id",
    "chart_snapshot_ref",
    "input_refs",
    "target",
    "available_information_refs",
)

BLIND_FORBIDDEN_FIELDS = frozenset(
    {
        "source",
        "source_subject_label",
        "expert_reasoning_graph",
        "expert_conclusion_refs",
        "outcome_refs",
    }
)


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_wang_inventory(path: Path = INVENTORY_PATH) -> Mapping[str, Any]:
    payload = _read_json(path)
    if payload.get("schema_version") != "0.1":
        raise ValueError("Wang inventory schema_version must be 0.1")
    if payload.get("corpus_id") != CORPUS_ID:
        raise ValueError("unexpected Wang inventory corpus_id")
    cases = payload.get("cases")
    if not isinstance(cases, list):
        raise ValueError("Wang inventory cases must be an array")
    return payload


def load_wang_case_bundles(cases_dir: Path = CASES_DIR) -> tuple[CaseBundle, ...]:
    paths = sorted(cases_dir.glob("wang_case_*.json"))
    bundles = tuple(compile_case_bundle(_read_json(path)) for path in paths)
    return bundles


def load_wang_method_patterns(
    path: Path = METHOD_PATTERNS_PATH,
) -> tuple[MethodPattern, ...]:
    payload = _read_json(path)
    if payload.get("schema_version") != "0.1":
        raise ValueError("Wang method-pattern schema_version must be 0.1")
    raw_patterns = payload.get("method_patterns")
    if not isinstance(raw_patterns, list):
        raise ValueError("method_patterns must be an array")
    return tuple(compile_method_pattern(item) for item in raw_patterns)


def load_wang_loco_manifest(path: Path = LOCO_PATH) -> Mapping[str, Any]:
    payload = _read_json(path)
    if payload.get("schema_version") != "0.1":
        raise ValueError("Wang LOCO schema_version must be 0.1")
    if payload.get("corpus_id") != CORPUS_ID:
        raise ValueError("unexpected Wang LOCO corpus_id")
    return payload


def build_blind_case_view(case: CaseBundle) -> dict[str, Any]:
    """Return only information legal before revealing the expert answer.

    The view intentionally excludes source identity details, expert graph,
    conclusion refs and outcome refs.  Case/person IDs are pseudonymous IDs in
    the Wang v0.1 corpus and therefore do not reveal historical subject names.
    """

    target = asdict(case.target)
    return {
        "case_id": case.case_id,
        "person_group_id": case.person_group_id,
        "chart_snapshot_ref": case.chart_snapshot_ref,
        "input_refs": list(case.input_refs),
        "target": {
            "question_ref": target["question_ref"],
            "domains": list(target["domains"]),
            "target_time_label": target["target_time_label"],
        },
        "available_information_refs": list(case.available_information_refs),
    }


def validate_wang_source_inventory(
    inventory: Mapping[str, Any],
) -> dict[str, Any]:
    cases = inventory["cases"]
    if len(cases) != EXPECTED_CASE_COUNT:
        raise ValueError(
            f"Wang source inventory must contain {EXPECTED_CASE_COUNT} cases"
        )

    case_ids = [item.get("case_id") for item in cases]
    if len(set(case_ids)) != EXPECTED_CASE_COUNT:
        raise ValueError("Wang source inventory case_id values must be unique")

    person_groups = [item.get("person_group_id") for item in cases]
    if len(set(person_groups)) != EXPECTED_CASE_COUNT:
        raise ValueError(
            "Wang v0.1 source inventory person_group_id values must be unique"
        )

    domains = Counter(item.get("domain") for item in cases)
    if len(domains) != EXPECTED_PALACE_TOPIC_COUNT:
        raise ValueError("Wang source inventory must cover 12 palace topics")
    if set(domains.values()) != {2}:
        raise ValueError("each Wang palace topic must contain exactly two cases")

    sequences = [item.get("sequence") for item in cases]
    if sequences != list(range(1, EXPECTED_CASE_COUNT + 1)):
        raise ValueError("Wang source inventory sequence must be 1..24")

    for item in cases:
        if item.get("extraction_status") != "SOURCE_SPAN_VERIFIED":
            raise ValueError(
                f"{item.get('case_id')}: source span must be verified"
            )
        if item.get("graph_status") != "MINIMAL_SOURCE_DEMONSTRATED":
            raise ValueError(
                f"{item.get('case_id')}: graph status must remain minimal/source-demonstrated"
            )
        start = item.get("source_page_start")
        end = item.get("source_page_end")
        if not isinstance(start, int) or not isinstance(end, int) or start > end:
            raise ValueError(f"{item.get('case_id')}: invalid page range")
        for key in (
            "chart_span_ref",
            "reasoning_span_ref",
            "conclusion_span_ref",
            "outcome_span_ref",
        ):
            value = item.get(key)
            if not isinstance(value, str) or not value.startswith(
                "WANG-ANXING-TUIDUAN:"
            ):
                raise ValueError(
                    f"{item.get('case_id')}: invalid source span {key}"
                )

    return {
        "case_count": len(cases),
        "palace_topic_count": len(domains),
        "domain_counts": dict(sorted(domains.items())),
    }


def validate_wang_case_bundles(
    bundles: tuple[CaseBundle, ...],
    inventory: Mapping[str, Any],
) -> dict[str, Any]:
    if len(bundles) != EXPECTED_CASE_COUNT:
        raise ValueError(f"expected {EXPECTED_CASE_COUNT} Wang CaseBundles")

    inventory_by_id = {item["case_id"]: item for item in inventory["cases"]}
    bundle_ids = [item.case_id for item in bundles]
    if set(bundle_ids) != set(inventory_by_id):
        raise ValueError("CaseBundle IDs do not match the source inventory")

    reconstructed_nodes = 0
    source_demonstrated_nodes = 0

    for case in bundles:
        source_item = inventory_by_id[case.case_id]
        if case.allowed_use != "CASE_SUPPORT_ONLY":
            raise ValueError(f"{case.case_id}: case must remain CASE_SUPPORT_ONLY")
        if case.source.author != "王亭之":
            raise ValueError(f"{case.case_id}: unexpected source author")
        if case.source.school != "ZHONGZHOU":
            raise ValueError(f"{case.case_id}: unexpected school")
        if case.source.review_status != "SOURCE_SPAN_VERIFIED":
            raise ValueError(f"{case.case_id}: source review is not verified")
        if case.person_group_id != source_item["person_group_id"]:
            raise ValueError(f"{case.case_id}: person_group_id mismatch")
        if case.target.domains != (source_item["domain"],):
            raise ValueError(f"{case.case_id}: domain mismatch")
        if set(case.available_information_refs) & (
            set(case.expert_conclusion_refs) | set(case.outcome_refs)
        ):
            raise ValueError(f"{case.case_id}: blind leakage detected")

        blind_view = build_blind_case_view(case)
        if set(blind_view) != set(BLIND_VISIBLE_FIELDS):
            raise ValueError(f"{case.case_id}: blind view field drift")
        if set(blind_view) & BLIND_FORBIDDEN_FIELDS:
            raise ValueError(f"{case.case_id}: forbidden blind field exposed")

        blind_serialized = json.dumps(blind_view, ensure_ascii=False)
        subject_label = source_item["source_subject_label"]
        if subject_label and subject_label in blind_serialized:
            raise ValueError(
                f"{case.case_id}: source subject label leaks into blind view"
            )

        for node in case.expert_reasoning_graph.nodes:
            if node.epistemic_status == "RECONSTRUCTED":
                reconstructed_nodes += 1
            elif node.epistemic_status == "SOURCE_DEMONSTRATED":
                source_demonstrated_nodes += 1
            if node.allowed_use != "CASE_SUPPORT_ONLY":
                raise ValueError(
                    f"{case.case_id}/{node.node_id}: case node may not be executable"
                )

    return {
        "case_count": len(bundles),
        "source_demonstrated_nodes": source_demonstrated_nodes,
        "reconstructed_nodes": reconstructed_nodes,
    }


def validate_wang_method_patterns(
    patterns: tuple[MethodPattern, ...],
) -> dict[str, Any]:
    if not patterns:
        raise ValueError("Wang method-pattern corpus cannot be empty")

    pattern_ids = [item.pattern_id for item in patterns]
    if len(pattern_ids) != len(set(pattern_ids)):
        raise ValueError("Wang method pattern IDs must be unique")

    for item in patterns:
        if item.maturity != "SOURCE_EXPLICIT":
            raise ValueError(
                f"{item.pattern_id}: v0.1 method patterns must be SOURCE_EXPLICIT"
            )
        if item.allowed_use != "SEMANTIC_ONLY":
            raise ValueError(
                f"{item.pattern_id}: source method remains SEMANTIC_ONLY in v0.1"
            )
        if "ZHONGZHOU" not in item.school_scope:
            raise ValueError(f"{item.pattern_id}: school scope must include Zhongzhou")
        if not item.source_span_refs:
            raise ValueError(f"{item.pattern_id}: source span required")

    return {"method_pattern_count": len(patterns)}


def validate_wang_loco_manifest(
    bundles: tuple[CaseBundle, ...],
    manifest: Mapping[str, Any],
) -> dict[str, Any]:
    case_by_id = {case.case_id: case for case in bundles}
    case_ids = tuple(sorted(case_by_id))
    folds = manifest.get("folds")
    if not isinstance(folds, list):
        raise ValueError("Wang LOCO folds must be an array")
    if manifest.get("case_count") != EXPECTED_CASE_COUNT:
        raise ValueError("Wang LOCO case_count must be 24")
    if manifest.get("fold_count") != EXPECTED_CASE_COUNT:
        raise ValueError("Wang LOCO fold_count must be 24")
    excluded_resources = manifest.get("blind_excluded_resources")
    if not isinstance(excluded_resources, list) or not {
        "CASE_SOURCE_INVENTORY_v0.1.json",
        "SOURCE_SUBJECT_LABEL_MAPPING",
        "EXPERT_CASE_PROSE",
        "EXPERT_REASONING_GRAPH",
        "EXPERT_CONCLUSIONS",
        "SOURCE_OUTCOMES",
        "EXTERNAL_BIOGRAPHICAL_KNOWLEDGE",
    }.issubset(set(excluded_resources)):
        raise ValueError("Wang LOCO blind excluded-resource policy is incomplete")
    if len(folds) != EXPECTED_CASE_COUNT:
        raise ValueError("Wang LOCO must contain 24 folds")

    held_out_ids: list[str] = []
    blind_aliases: list[str] = []

    for fold in folds:
        held_id = fold.get("held_out_case_id")
        held_group = fold.get("held_out_person_group_id")
        if held_id not in case_by_id:
            raise ValueError(f"unknown held-out case: {held_id}")
        if held_group != case_by_id[held_id].person_group_id:
            raise ValueError(f"{held_id}: held-out person group mismatch")
        held_out_ids.append(held_id)

        alias = fold.get("blind_alias")
        if not isinstance(alias, str) or not alias.startswith("WANG-BLIND-"):
            raise ValueError(f"{held_id}: invalid blind alias")
        blind_aliases.append(alias)

        train_ids = fold.get("train_case_ids")
        retrieval_ids = fold.get("retrieval_case_ids")
        if not isinstance(train_ids, list) or not isinstance(retrieval_ids, list):
            raise ValueError(f"{held_id}: train/retrieval IDs must be arrays")

        expected_train = set(case_ids) - {held_id}
        if set(train_ids) != expected_train:
            raise ValueError(f"{held_id}: train set is not exact leave-one-out")
        if set(retrieval_ids) != expected_train:
            raise ValueError(f"{held_id}: retrieval set is not exact leave-one-out")

        for train_id in train_ids:
            if case_by_id[train_id].person_group_id == held_group:
                raise ValueError(
                    f"{held_id}: held-out person_group_id leaked into training"
                )

        visible = fold.get("blind_visible_fields")
        hidden = fold.get("hidden_fields")
        if visible != list(BLIND_VISIBLE_FIELDS):
            raise ValueError(f"{held_id}: blind visible-field policy drift")
        if not isinstance(hidden, list) or not {
            "source_subject_label",
            "expert_reasoning_graph",
            "expert_conclusion_refs",
            "outcome_refs",
        }.issubset(set(hidden)):
            raise ValueError(f"{held_id}: blind hidden-field policy incomplete")

    if set(held_out_ids) != set(case_ids):
        raise ValueError("every Wang case must be held out exactly once")
    if len(held_out_ids) != len(set(held_out_ids)):
        raise ValueError("a Wang case is held out more than once")
    if len(blind_aliases) != len(set(blind_aliases)):
        raise ValueError("Wang blind aliases must be unique")

    return {
        "fold_count": len(folds),
        "held_out_once_count": len(set(held_out_ids)),
    }


def validate_wang_expert_corpus() -> dict[str, Any]:
    inventory = load_wang_inventory()
    bundles = load_wang_case_bundles()
    patterns = load_wang_method_patterns()
    manifest = load_wang_loco_manifest()

    return {
        "inventory": validate_wang_source_inventory(inventory),
        "cases": validate_wang_case_bundles(bundles, inventory),
        "methods": validate_wang_method_patterns(patterns),
        "loco": validate_wang_loco_manifest(bundles, manifest),
    }
