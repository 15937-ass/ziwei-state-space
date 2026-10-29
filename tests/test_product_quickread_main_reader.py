import csv
import io
import json
from urllib.parse import unquote, urlsplit

import pytest
import src.product.quickread_main_reader as main_reader

from src.product.quickread_capability import QuickReadRequest, QuickReadScopeSlot
from src.product.quickread_main_reader import (
    API_ROOT,
    MainKnowledgeUnavailable,
    RAW_ROOT,
    _git_blob_sha,
    _is_direct_visual_review_note,
    _supported_source_ledger,
    _default_runtime_domains,
    load_latest_main_knowledge,
)


MAIN_SHA = "a" * 40
TREE_SHA = "b" * 40
REGISTRY_SOURCE = """\
def load_default_natal_domain_registry(repository_root, *, additional_providers=()):
    wealth = load_default_wealth_natal_provider(repository_root)
    extras = tuple(additional_providers)
    return NatalDomainProviderRegistry(providers=(_WealthProviderAdapter(wealth), *extras))
"""
WEALTH_RUNTIME_SOURCE = """\
DEFAULT_WEALTH_BATCH_PATHS = ("product/PL2C_WEALTH_PILOT_v0.1.json",)
DEFAULT_WEALTH_PROJECTION_PATH = "validation/wp05/W01_wealth_projection_review_001_100.csv"
DEFAULT_PALACE_ONTOLOGY_PATH = "knowledge/wp05/palace_ontology_v0.1.csv"
"""


def _slot(domain="relationship", layer="NATAL", kind="NATAL_STRUCTURE", namespaces=None):
    if namespaces is None:
        namespaces = ("CANONICAL",) if layer == "NATAL" else (
            ("CANONICAL", "TEMPORAL")
            if any(word in kind.upper() for word in ("RESPONSE", "MANIFESTATION"))
            else ("TEMPORAL",)
        )
    return QuickReadScopeSlot(
        slot_id=f"{domain}_{layer.lower()}",
        domain=domain,
        temporal_layer=layer,
        capability_kind=kind,
        required_namespaces=namespaces,
    )


def _request(domain="relationship", layer="NATAL", kind="NATAL_STRUCTURE", namespaces=None):
    slot = _slot(domain, layer, kind, namespaces)
    return QuickReadRequest(
        question="简单看看夫妻宫感情倾向",
        target_id="SYNTHETIC-CHART-001",
        requested_slots=(slot,),
        mode="SOURCE_FIRST",
    )


def _ledger(records=None, *, status="SOURCE_REVIEW_COMPLETE"):
    if records is None:
        records = [
            {
                "projection_rule_id": "P03S-201",
                "canonical_condition": "太阳巨门见辅佐诸吉；女命。",
                "canonical_projection_domain": "relationship",
                "canonical_projection_target": "spousal status tendency",
                "source_location": "SRC-ZZ-003 printed p37 / PDF physical p19",
                "source_note": "直接目视核对批准原扫描图；文字提取仅用于定位。",
                "canonical_promotion": True,
                "case_support_only": False,
                "source_condition_normalized": True,
                "source_span_changed": False,
                "source_condition_uncertainty": None,
                "primary_time_layer": "NATAL",
            },
            {
                "projection_rule_id": "P03S-204",
                "canonical_condition": "夫妻年龄差。",
                "canonical_projection_domain": "relationship",
                "canonical_projection_target": "age gap",
                "source_location": "SRC-ZZ-003 printed p37",
                "source_note": "直接目视核对批准原扫描图。",
                "canonical_promotion": True,
                "case_support_only": True,
                "source_condition_normalized": True,
                "source_span_changed": False,
                "source_condition_uncertainty": None,
                "primary_time_layer": "NATAL",
            },
            {
                "projection_rule_id": "P03S-MISSING-CASE-STATUS",
                "canonical_condition": "缺少案例范围标记的条件。",
                "canonical_projection_domain": "relationship",
                "canonical_projection_target": "unscoped target",
                "source_location": "SRC-ZZ-003 printed p37a",
                "source_note": "直接目视核对批准原扫描图。",
                "canonical_promotion": True,
                "source_condition_normalized": True,
                "source_span_changed": False,
                "source_condition_uncertainty": None,
                "primary_time_layer": "NATAL",
            },
            {
                "projection_rule_id": "P03S-MISSING-SPAN-STATUS",
                "canonical_condition": "缺少来源跨度状态的条件。",
                "canonical_projection_domain": "relationship",
                "canonical_projection_target": "uncertain target",
                "source_location": "SRC-ZZ-003 printed p37b",
                "source_note": "直接目视核对批准原扫描图。",
                "canonical_promotion": True,
                "case_support_only": False,
                "source_condition_normalized": True,
                "source_condition_uncertainty": None,
                "primary_time_layer": "NATAL",
            },
            {
                "projection_rule_id": "P03S-HELD",
                "canonical_condition": "待复核条件。",
                "canonical_projection_domain": "relationship",
                "canonical_projection_target": "held target",
                "source_location": "SRC-ZZ-003 printed p38",
                "source_note": "直接目视核对批准原扫描图。",
                "canonical_promotion": False,
                "case_support_only": False,
                "source_condition_normalized": True,
                "source_span_changed": False,
                "source_condition_uncertainty": None,
                "primary_time_layer": "NATAL",
            },
            {
                "projection_rule_id": "P03S-HOLD-DISPOSITION",
                "canonical_condition": "显式保留的待决条件。",
                "canonical_projection_domain": "relationship",
                "canonical_projection_target": "held target",
                "source_location": "SRC-ZZ-003 printed p38a",
                "source_note": "直接目视核对批准原扫描图。",
                "canonical_promotion": True,
                "disposition": "HOLD_UNRESOLVED",
                "case_support_only": False,
                "source_condition_normalized": True,
                "source_span_changed": False,
                "source_condition_uncertainty": None,
                "primary_time_layer": "NATAL",
            },
            {
                "projection_rule_id": "P03S-UNCERTAIN",
                "canonical_condition": "有疑点的条件。",
                "canonical_projection_domain": "relationship",
                "canonical_projection_target": "uncertain target",
                "source_location": "SRC-ZZ-003 printed p38",
                "source_note": "直接目视核对批准原扫描图。",
                "canonical_promotion": True,
                "case_support_only": False,
                "source_condition_normalized": True,
                "source_span_changed": False,
                "source_condition_uncertainty": "source phrase unresolved",
                "primary_time_layer": "NATAL",
            },
            {
                "projection_rule_id": "P03S-WRONG-LAYER",
                "canonical_condition": "流年层级未明。",
                "canonical_projection_domain": "relationship",
                "canonical_projection_target": "yearly target",
                "source_location": "SRC-ZZ-003 printed p39",
                "source_note": "直接目视核对批准原扫描图。",
                "canonical_promotion": True,
                "case_support_only": False,
                "source_condition_normalized": True,
                "source_span_changed": False,
                "source_condition_uncertainty": None,
                "primary_time_layer": "YEAR",
            },
            {
                "projection_rule_id": "P03S-NO-PROVENANCE",
                "canonical_condition": "仅有历史索引标记的条件。",
                "canonical_projection_domain": "relationship",
                "canonical_projection_target": "unverified target",
                "source_location": "SRC-ZZ-003 printed p40",
                "source_note": "历史索引标记，不是直接目视核对。",
                "canonical_promotion": True,
                "case_support_only": False,
                "source_condition_normalized": True,
                "source_span_changed": False,
                "source_condition_uncertainty": None,
                "primary_time_layer": "NATAL",
            },
        ]
    return {
        "schema_version": "0.1",
        "artifact_id": "KB-WP05-P03-SOURCE-READJUDICATION-SYNTHETIC",
        "lane": "KNOWLEDGE_ONLY",
        "shard": "P03",
        "palace": "夫妻宫",
        "status": status,
        "source_basis": {
            "source_id": "SRC-ZZ-003",
            "verification_method": "DIRECT_PDF_VISUAL_REVIEW",
        },
        "records": records,
    }


def _wealth_fixture():
    provider = {
        "schema_version": "0.1",
        "provider_id": "PL3N_WEALTH_W01_PROVIDER",
        "domain_id": "wealth",
        "time_layer": "NATAL",
        "projection_source": "validation/wp05/W01_wealth_projection_review_001_100.csv",
        "batch_paths": ["product/PL2C_WEALTH_PILOT_v0.1.json"],
        "expected_executable_rules": 1,
        "knowledge_version": "W01+SYNTHETIC-1",
    }
    batch = {
        "schema_version": "0.1",
        "palace_id": "P05",
        "policy": {
            "source_review_required": "SOURCE_SPAN_VERIFIED",
            "case_support_only_allowed": False,
            "normalization_verified": True,
        },
        "rules": {
            "W01-001": {
                "expected_condition": "财帛宫见化禄",
                "expected_projection_target": "income modifier",
                "condition": {"all_of": []},
            }
        },
    }
    csv_text = (
        "projection_rule_id,source_id,source_location,palace_id,time_layer,condition,"
        "projection_domain,projection_target,projection_mode,review_status,"
        "source_span_verified,case_support_only,history_feedback\n"
        "W01-001,SRC-ZZ-003,财帛宫printed_p69,P05,NATAL,财帛宫见化禄,"
        "resource,income_modifier,FUNCTIONAL_PROJECTION,SOURCE_SPAN_VERIFIED,true,false,\n"
    )
    return provider, batch, csv_text


def _transport(artifacts, *, tree_truncated=False, bad_blob_paths=()):
    raw = {path: value.encode("utf-8") if isinstance(value, str) else value for path, value in artifacts.items()}
    tree = []
    for path, content in raw.items():
        sha = _git_blob_sha(content)
        if path in bad_blob_paths:
            sha = "c" * 40
        tree.append({"path": path, "type": "blob", "sha": sha, "size": len(content)})
    calls = []

    def fetch(url, timeout, max_bytes):
        calls.append(url)
        if url == f"{API_ROOT}/commits/main":
            return json.dumps({"sha": MAIN_SHA}).encode()
        if url == f"{API_ROOT}/git/trees/{MAIN_SHA}?recursive=1":
            return json.dumps({"sha": TREE_SHA, "truncated": tree_truncated, "tree": tree}).encode()
        prefix = f"{RAW_ROOT}/{MAIN_SHA}/"
        if url.startswith(prefix):
            path = unquote(url[len(prefix):])
            if path not in raw:
                raise AssertionError(f"unexpected raw artifact request: {path}")
            return raw[path]
        raise AssertionError(f"unexpected URL: {url}")

    return fetch, calls


def _base_artifacts():
    ledger_path = (
        "knowledge/palaces/P03_spouse/wp05/"
        "SPOUSE_SP03_SOURCE_READJUDICATION_100_v0.1.json"
    )
    return {
        "src/product/natal_domain_registry.py": REGISTRY_SOURCE,
        "src/product/natal_domain_providers.py": WEALTH_RUNTIME_SOURCE,
        ledger_path: json.dumps(_ledger(), ensure_ascii=False),
    }, ledger_path


def test_reads_one_immutable_main_snapshot_and_retrieves_only_reusable_source_records():
    artifacts, ledger_path = _base_artifacts()
    fetch, calls = _transport(artifacts)
    bundle = load_latest_main_knowledge(_request(), fetch_bytes=fetch)

    assert bundle.manifest.main_sha == MAIN_SHA
    assert bundle.reader_report["source_of_truth"] == "GitHub main only"
    assert any("No LLM/model API call" in item and "GitHub API requests" in item for item in bundle.reader_report["limitations"])
    assert bundle.reader_report["loaded_source_ledger_paths"] == [ledger_path]
    assert len(bundle.evidence_items) == 1
    assert bundle.evidence_items[0].evidence_id.endswith("P03S-201:relationship_natal")
    assert bundle.evidence_items[0].lane == "SOURCE"
    assert bundle.evidence_items[0].epistemic_label == "SOURCE_GROUNDED"
    assert bundle.evidence_items[0].source_refs[0].allowed_use == "SEMANTIC_ONLY"
    assert bundle.evidence_items[0].source_refs[0].review_status == "SOURCE_SPAN_VERIFIED"
    assert bundle.reader_report["aggregate_source_ledger_counts"]["excluded_case_only"] == 2
    assert bundle.reader_report["aggregate_source_ledger_counts"]["excluded_not_promoted"] == 2
    assert bundle.reader_report["aggregate_source_ledger_counts"]["excluded_uncertain_or_unverified"] == 2
    assert bundle.reader_report["aggregate_source_ledger_counts"]["excluded_layer_mismatch"] == 1
    assert bundle.reader_report["aggregate_source_ledger_counts"]["excluded_missing_provenance"] == 1
    assert all(MAIN_SHA in call for call in calls if call.startswith(RAW_ROOT))
    payload = bundle.build_payload()
    assert payload["versions"]["main_sha"] == MAIN_SHA


def test_discovers_but_does_not_auto_enable_opt_in_career_provider():
    artifacts, _ = _base_artifacts()
    artifacts["product/PL3N_CAREER_DOMAIN_PROVIDER_v0.1.json"] = json.dumps(
        {
            "schema_version": "0.1",
            "status": "CANONICAL_READY",
            "provider_id": "CAREER-SYNTHETIC",
            "domain_id": "career",
            "time_layer": "NATAL",
            "knowledge_version": "CAREER-SYNTHETIC-1",
            "rules": {
                "CA01-001": {
                    "expected_source_id": "SRC-ZZ-003",
                    "expected_source_location": "事业宫printed_p133",
                    "expected_review_status": "SOURCE_SPAN_VERIFIED",
                }
            },
        }
    )
    fetch, _ = _transport(artifacts)
    bundle = load_latest_main_knowledge(_request("career"), fetch_bytes=fetch)

    assert bundle.providers[0].domain_id == "career"
    assert bundle.providers[0].activation_mode == "OPT_IN_OR_NOT_DEFAULT"
    assert bundle.providers[0].rule_count == 1
    record = bundle.manifest.records[0]
    assert record.runtime_status == "NOT_AVAILABLE"
    assert "not auto-enabled" in record.reason


def test_default_wealth_provider_is_counted_only_after_main_inputs_reconcile(tmp_path, monkeypatch):
    artifacts, _ = _base_artifacts()
    provider, batch, csv_text = _wealth_fixture()
    artifacts["product/PL3N_WEALTH_DOMAIN_PROVIDER_v0.1.json"] = json.dumps(provider)
    artifacts["product/PL2C_WEALTH_PILOT_v0.1.json"] = json.dumps(batch)
    artifacts["validation/wp05/W01_wealth_projection_review_001_100.csv"] = csv_text
    artifacts["knowledge/wp05/palace_ontology_v0.1.csv"] = "palace_id,palace_name\nP05,财帛宫\n"
    fetch, _ = _transport(artifacts)
    monkeypatch.setattr(main_reader, "_default_checkout_matches_main", lambda root, sha: True)
    for path, artifact_content in artifacts.items():
        target = tmp_path / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(artifact_content, encoding="utf-8")
    bundle = load_latest_main_knowledge(
        _request("wealth"),
        fetch_bytes=fetch,
        repository_root=tmp_path,
    )

    assert bundle.reader_report["local_runtime_matches_main"] is True
    record = bundle.manifest.records[0]
    assert record.runtime_status == "AVAILABLE"
    assert record.runtime_rule_ids == ("W01-001",)
    assert record.runtime_source_refs[0].source_id == "SRC-ZZ-003"
    assert bundle.providers[0].activation_mode == "DEFAULT_RUNTIME"
    # The reader discovers capability; it does not pretend the chart runtime ran.
    assert bundle.evidence_items == ()
    payload = bundle.build_payload()
    assert payload["coverage"]["runtime_capable_slot_count"] == 1
    assert payload["coverage"]["runtime_evidenced_slot_count"] == 0


def test_rejects_a_truncated_main_tree_instead_of_using_partial_knowledge():
    artifacts, _ = _base_artifacts()
    fetch, _ = _transport(artifacts, tree_truncated=True)
    with pytest.raises(MainKnowledgeUnavailable, match="truncated"):
        load_latest_main_knowledge(_request(), fetch_bytes=fetch)


def test_rejects_blob_mismatch_instead_of_using_unverified_file_content():
    artifacts, ledger_path = _base_artifacts()
    fetch, _ = _transport(artifacts, bad_blob_paths=(ledger_path,))
    with pytest.raises(MainKnowledgeUnavailable, match="blob SHA mismatch"):
        load_latest_main_knowledge(_request(), fetch_bytes=fetch)


def test_default_runtime_registry_parser_fails_closed_and_reads_explicit_default_domains():
    assert _default_runtime_domains(REGISTRY_SOURCE) == ("wealth",)
    assert _default_runtime_domains("def unrelated():\n    return None\n") == ()


def test_runtime_capability_is_not_asserted_when_local_product_code_differs_from_main(tmp_path, monkeypatch):
    artifacts, _ = _base_artifacts()
    provider, batch, csv_text = _wealth_fixture()
    artifacts["product/PL3N_WEALTH_DOMAIN_PROVIDER_v0.1.json"] = json.dumps(provider)
    artifacts["product/PL2C_WEALTH_PILOT_v0.1.json"] = json.dumps(batch)
    artifacts["validation/wp05/W01_wealth_projection_review_001_100.csv"] = csv_text
    artifacts["knowledge/wp05/palace_ontology_v0.1.csv"] = "palace_id,palace_name\\nP05,财帛宫\\n"
    fetch, _ = _transport(artifacts)
    monkeypatch.setattr(main_reader, "_default_checkout_matches_main", lambda root, sha: False)
    for path in ("src/product/natal_domain_registry.py", "src/product/natal_domain_providers.py"):
        target = tmp_path / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text("stale local runtime", encoding="utf-8")

    bundle = load_latest_main_knowledge(
        _request("wealth"),
        fetch_bytes=fetch,
        repository_root=tmp_path,
    )
    assert bundle.reader_report["local_runtime_matches_main"] is False
    assert bundle.manifest.records[0].runtime_status == "NOT_AVAILABLE"
    assert "not at the exact main SHA" in bundle.manifest.records[0].reason


def test_pending_exact_head_source_ledger_is_not_consumed():
    artifacts, ledger_path = _base_artifacts()
    artifacts[ledger_path] = json.dumps(
        _ledger(status="SOURCE_REVIEW_COMPLETE_PENDING_EXACT_HEAD_VALIDATION"),
        ensure_ascii=False,
    )
    fetch, _ = _transport(artifacts)
    bundle = load_latest_main_knowledge(_request(), fetch_bytes=fetch)

    assert bundle.reader_report["aggregate_source_ledger_counts"]["ledger_files_discovered"] == 1
    assert bundle.reader_report["aggregate_source_ledger_counts"]["ledger_files_accepted"] == 0
    assert bundle.evidence_items == ()
    assert bundle.manifest.records[0].source_status == "NOT_AVAILABLE"


def test_latest_provider_version_is_selected_without_lexical_order_guessing():
    artifacts, _ = _base_artifacts()
    for version, provider_id in (("0.1", "CAREER-OLD"), ("0.2", "CAREER-NEW")):
        artifacts[f"product/PL3N_CAREER_DOMAIN_PROVIDER_v{version}.json"] = json.dumps(
            {
                "schema_version": "0.1",
                "status": "CANONICAL_READY",
                "provider_id": provider_id,
                "domain_id": "career",
                "time_layer": "NATAL",
                "knowledge_version": f"CAREER-{version}",
                "rules": {
                    "CA01-001": {
                        "expected_source_id": "SRC-ZZ-003",
                        "expected_source_location": "事业宫printed_p133",
                        "expected_review_status": "SOURCE_SPAN_VERIFIED",
                    }
                },
            }
        )
    fetch, _ = _transport(artifacts)
    bundle = load_latest_main_knowledge(_request("career"), fetch_bytes=fetch)

    assert len(bundle.providers) == 1
    assert bundle.providers[0].provider_id == "CAREER-NEW"
    assert bundle.reader_report["superseded_provider_paths"] == [
        "product/PL3N_CAREER_DOMAIN_PROVIDER_v0.1.json"
    ]


def test_runtime_input_files_must_match_the_pinned_main_tree(tmp_path, monkeypatch):
    artifacts, _ = _base_artifacts()
    provider, batch, csv_text = _wealth_fixture()
    artifacts["product/PL3N_WEALTH_DOMAIN_PROVIDER_v0.1.json"] = json.dumps(provider)
    artifacts["product/PL2C_WEALTH_PILOT_v0.1.json"] = json.dumps(batch)
    artifacts["validation/wp05/W01_wealth_projection_review_001_100.csv"] = csv_text
    artifacts["knowledge/wp05/palace_ontology_v0.1.csv"] = "palace_id,palace_name\\nP05,财帛宫\\n"
    fetch, _ = _transport(artifacts)
    monkeypatch.setattr(main_reader, "_default_checkout_matches_main", lambda root, sha: True)
    for path, artifact_content in artifacts.items():
        target = tmp_path / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(artifact_content, encoding="utf-8")
    stale_csv = tmp_path / "validation/wp05/W01_wealth_projection_review_001_100.csv"
    stale_csv.write_text("stale local CSV", encoding="utf-8")

    bundle = load_latest_main_knowledge(
        _request("wealth"), fetch_bytes=fetch, repository_root=tmp_path
    )
    assert bundle.reader_report["local_runtime_matches_main"] is True
    assert bundle.reader_report["runtime_inputs_match_main"]["wealth"] is False
    assert bundle.manifest.records[0].runtime_status == "NOT_AVAILABLE"
    assert "input files do not match" in bundle.manifest.records[0].reason


def test_direct_visual_review_note_accepts_main_variants_and_rejects_negation():
    assert _is_direct_visual_review_note("直接目视核对批准原扫描图")
    assert _is_direct_visual_review_note("直接目视检查原扫描图")
    assert _is_direct_visual_review_note("Direct visual review of the original scan.")
    assert not _is_direct_visual_review_note("历史索引标记，不是直接目视核对。")
    assert not _is_direct_visual_review_note("Direct visual review was not performed.")


def test_default_first_pass_source_budget_is_twenty_items_per_slot():
    base = _ledger()["records"][0]
    records = []
    for index in range(25):
        record = dict(base)
        record["projection_rule_id"] = f"P03S-DEFAULT-{index:03d}"
        record["canonical_condition"] = f"来源条件 {index}"
        record["canonical_projection_target"] = f"target {index}"
        records.append(record)
    artifacts, _ = _base_artifacts()
    ledger_path = next(path for path in artifacts if "SOURCE_READJUDICATION" in path)
    artifacts[ledger_path] = json.dumps(_ledger(records=records), ensure_ascii=False)
    fetch, _ = _transport(artifacts)

    bundle = load_latest_main_knowledge(_request(), fetch_bytes=fetch)

    assert len(bundle.evidence_items) == 20
    assert bundle.reader_report["source_batch_limit_per_slot"] == 20
    assert bundle.reader_report["source_items_total_eligible_by_slot"]["relationship_natal"] == 25
    assert bundle.reader_report["source_items_remaining_after_batch_by_slot"]["relationship_natal"] == 5
    assert bundle.reader_report["continuation"]["has_more"] is True


def test_source_batch_limit_is_first_pass_budget_and_reports_continuation():
    base = _ledger()["records"][0]
    records = []
    for index in range(15):
        record = dict(base)
        record["projection_rule_id"] = f"P03S-LIMIT-{index:03d}"
        record["canonical_condition"] = f"来源条件 {index}"
        record["canonical_projection_target"] = f"target {index}"
        records.append(record)
    artifacts, _ = _base_artifacts()
    ledger_path = next(path for path in artifacts if "SOURCE_READJUDICATION" in path)
    artifacts[ledger_path] = json.dumps(_ledger(records=records), ensure_ascii=False)
    fetch, _ = _transport(artifacts)

    first = load_latest_main_knowledge(
        _request(), fetch_bytes=fetch, source_items_per_slot=5
    )
    assert len(first.evidence_items) == 5
    assert first.reader_report["aggregate_source_ledger_counts"]["records_eligible_pre_batch"] == 15
    assert first.reader_report["source_batch_limit_per_slot"] == 5
    assert first.reader_report["source_items_total_eligible_by_slot"]["relationship_natal"] == 15
    assert first.reader_report["source_items_already_seen_by_slot"]["relationship_natal"] == 0
    assert first.reader_report["source_items_selected_this_batch_by_slot"]["relationship_natal"] == 5
    assert first.reader_report["source_items_remaining_after_batch_by_slot"]["relationship_natal"] == 10
    assert first.reader_report["continuation"]["has_more"] is True
    assert len(first.reader_report["continuation"]["seen_evidence_ids"]) == 5


def test_continuation_progressively_reads_new_source_evidence_without_duplicates():
    base = _ledger()["records"][0]
    records = []
    for index in range(13):
        record = dict(base)
        record["projection_rule_id"] = f"P03S-PAGE-{index:03d}"
        record["canonical_condition"] = f"来源条件 {index}"
        record["canonical_projection_target"] = f"target {index}"
        records.append(record)
    artifacts, _ = _base_artifacts()
    ledger_path = next(path for path in artifacts if "SOURCE_READJUDICATION" in path)
    artifacts[ledger_path] = json.dumps(_ledger(records=records), ensure_ascii=False)
    fetch, _ = _transport(artifacts)

    first = load_latest_main_knowledge(
        _request(), fetch_bytes=fetch, source_items_per_slot=5
    )
    second = load_latest_main_knowledge(
        _request(),
        fetch_bytes=fetch,
        source_items_per_slot=5,
        continuation=first.reader_report["continuation"],
    )
    third = load_latest_main_knowledge(
        _request(),
        fetch_bytes=fetch,
        source_items_per_slot=5,
        continuation=second.reader_report["continuation"],
    )

    first_ids = {item.evidence_id for item in first.evidence_items}
    second_ids = {item.evidence_id for item in second.evidence_items}
    third_ids = {item.evidence_id for item in third.evidence_items}
    assert len(first_ids) == 5
    assert len(second_ids) == 5
    assert len(third_ids) == 3
    assert first_ids.isdisjoint(second_ids)
    assert first_ids.isdisjoint(third_ids)
    assert second_ids.isdisjoint(third_ids)
    assert second.reader_report["source_items_already_seen_by_slot"]["relationship_natal"] == 5
    assert second.reader_report["source_items_remaining_after_batch_by_slot"]["relationship_natal"] == 3
    assert third.reader_report["source_items_already_seen_by_slot"]["relationship_natal"] == 10
    assert third.reader_report["source_items_remaining_after_batch_by_slot"]["relationship_natal"] == 0
    assert third.reader_report["continuation"]["has_more"] is False
    assert len(third.reader_report["continuation"]["seen_evidence_ids"]) == 13


def test_continuation_fails_closed_when_main_snapshot_changes():
    artifacts, _ = _base_artifacts()
    fetch, _ = _transport(artifacts)
    stale = {
        "main_sha": "0" * 40,
        "requested_slot_ids": ["relationship_natal"],
        "seen_evidence_ids": [],
    }
    with pytest.raises(MainKnowledgeUnavailable, match="continuation is stale"):
        load_latest_main_knowledge(
            _request(),
            fetch_bytes=fetch,
            continuation=stale,
        )


def test_continuation_rejects_scope_mismatch_before_retrieval():
    artifacts, _ = _base_artifacts()
    fetch, _ = _transport(artifacts)
    wrong_scope = {
        "main_sha": MAIN_SHA,
        "requested_slot_ids": ["career_natal"],
        "seen_evidence_ids": [],
    }
    with pytest.raises(ValueError, match="requested scope"):
        load_latest_main_knowledge(
            _request(),
            fetch_bytes=fetch,
            continuation=wrong_scope,
        )


def test_source_ledger_with_unsupported_verification_method_is_not_counted_as_accepted():
    artifact = _ledger()
    artifact["source_basis"]["verification_method"] = "HISTORICAL_INDEX_ONLY"
    assert _supported_source_ledger(artifact) is False

    artifacts, ledger_path = _base_artifacts()
    artifacts[ledger_path] = json.dumps(artifact, ensure_ascii=False)
    fetch, _ = _transport(artifacts)
    bundle = load_latest_main_knowledge(_request(), fetch_bytes=fetch)

    counts = bundle.reader_report["aggregate_source_ledger_counts"]
    assert counts["ledger_files_discovered"] == 1
    assert counts["ledger_files_accepted"] == 0
    assert bundle.reader_report["loaded_source_ledger_paths"] == []
    assert bundle.evidence_items == ()
