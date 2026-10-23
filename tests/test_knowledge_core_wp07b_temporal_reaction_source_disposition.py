import csv
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "knowledge/core/WP07B_TEMPORAL_REACTION_SOURCE_DISPOSITION_v0.1.json"
CAREER = ROOT / "knowledge/wp07b/CAREER_TEMPORAL_REACTION_ELIGIBILITY_v0.1.csv"
PROPERTY = ROOT / "knowledge/palaces/P10_property/wp07b/PROPERTY_TEMPORAL_REACTION_ELIGIBILITY_v0.1.csv"


def _json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def _printed_page(source_location: str) -> int:
    match = re.search(r"printed_p(\d+)", source_location)
    assert match, source_location
    return int(match.group(1))


def test_wp07b_disposition_covers_exactly_the_current_eligibility_ledgers():
    artifact = _json(ARTIFACT)
    career = _csv(CAREER)
    property_rows = _csv(PROPERTY)
    rows = artifact["candidate_dispositions"]

    assert artifact["schema_version"] == "0.1"
    assert artifact["artifact_id"] == "KB-WP07B-SOURCE-REACTION-CONTRACT-01"
    assert len(career) == 9
    assert len(property_rows) == 35
    assert len(rows) == 44

    by_id = {row["candidate_id"]: row for row in rows}
    assert len(by_id) == 44
    assert set(by_id) == {
        row["candidate_id"] for row in career + property_rows
    }

    for shard_rows, source_path, shard in (
        (career, "knowledge/wp07b/CAREER_TEMPORAL_REACTION_ELIGIBILITY_v0.1.csv", "P09"),
        (property_rows, "knowledge/palaces/P10_property/wp07b/PROPERTY_TEMPORAL_REACTION_ELIGIBILITY_v0.1.csv", "P10"),
    ):
        for source in shard_rows:
            row = by_id[source["candidate_id"]]
            assert row["shard"] == shard
            assert row["source_id"] == source["source_id"] == "SRC-ZZ-003"
            assert row["source_location"] == source["source_location"]
            assert row["declared_time_layer"] == source["declared_time_layer"]
            assert row["source_time_scope"] == source["source_time_scope"]
            assert row["original_eligibility_status"] == source["eligibility_status"]
            assert row["original_blocking_reasons"] == [
                part for part in source["blocking_reasons"].split("|") if part
            ]
            assert row["scan_locator"]["printed_page"] == _printed_page(source["source_location"])
            assert row["scan_locator"]["source_scan_pdf_page_1based"] == (
                _printed_page(source["source_location"]) + 1
            ) // 2
            assert row["source_span_refs"][0]["path"] == source_path
            assert row["source_span_refs"][0]["candidate_id"] == source["candidate_id"]
            assert row["runtime_eligible"] is False
            assert row["normalization_decision"] == "NOT_EMITTED"


def test_wp07b_disposition_partition_is_explicit_and_fail_closed():
    artifact = _json(ARTIFACT)
    rows = artifact["candidate_dispositions"]
    counts = artifact["counts"]

    assert counts["career"] == {
        "total": 9,
        "eligible": 0,
        "blocked_reusable": 8,
        "excluded_case_support_only": 1,
    }
    assert counts["property"] == {
        "total": 35,
        "eligible": 0,
        "blocked_reusable": 19,
        "excluded_case_support_only": 16,
    }
    assert counts["combined"]["total"] == 44
    assert counts["combined"]["eligible"] == 0
    assert counts["combined"]["blocked_reusable"] == 27
    assert counts["combined"]["excluded_case_support_only"] == 17
    assert counts["combined"]["executable_pilot_emitted"] == 0
    assert sum(row["disposition"] == "BLOCKED_CURRENT_CONTRACT" for row in rows) == 27
    assert sum(row["disposition"] == "EXCLUDED_CASE_SUPPORT_ONLY" for row in rows) == 17
    assert all(row["runtime_eligible"] is False for row in rows)


def test_ca04_350_reassessment_retires_only_the_stale_adapter_blocker():
    artifact = _json(ARTIFACT)
    row = next(item for item in artifact["candidate_dispositions"] if item["candidate_id"] == "CA04-350")

    assert row["disposition"] == "BLOCKED_CURRENT_CONTRACT"
    assert "STAR_MUTAGEN_BINDING_GAP" in row["original_blocking_reasons"]
    assert "STAR_MUTAGEN_BINDING_GAP" not in row["current_blockers"]
    assert "REAL_WORLD_COMMERCE_CONTEXT_UNTYPED" in row["current_blockers"]
    assert "SOURCE_SCOPE_REQUIRES_EXPLICIT_LAYER_NORMALIZATION" in row["current_blockers"]
    assert "CONTEXT_DEPENDENT_COMMERCE_GATE" in row["current_contract_reassessment"]


def test_near_ready_property_rows_do_not_invent_natal_or_temporal_facts():
    artifact = _json(ARTIFACT)
    rows = {item["candidate_id"]: item for item in artifact["candidate_dispositions"]}

    for candidate_id in ("TP03-245", "TP03-246"):
        row = rows[candidate_id]
        assert row["disposition"] == "BLOCKED_CURRENT_CONTRACT"
        assert "REQUIRED_NATAL_ANTECEDENT_ABSENT_IN_SOURCE" in row["current_blockers"]
        assert "vacuous PALACE_PRESENT(P10)" in row["current_contract_reassessment"]

    for candidate_id in ("TP04-307", "TP04-308"):
        row = rows[candidate_id]
        assert row["disposition"] == "BLOCKED_CURRENT_CONTRACT"
        assert "STAR_MUTAGEN_BINDING_RUNTIME_REQUIRES_PALACE_NAME" in row["current_blockers"]
        assert "SOURCE_DOES_NOT_SPECIFY_TEMPORAL_PALACE_NAME" in row["current_blockers"]


def test_no_executable_spec_or_product_authorization_is_created():
    artifact = _json(ARTIFACT)

    assert artifact["counts"]["combined"]["executable_pilot_emitted"] == 0
    assert artifact["review_method"]["no_product_writes"] is True
    assert all(item["normalization_decision"] == "NOT_EMITTED" for item in artifact["candidate_dispositions"])
