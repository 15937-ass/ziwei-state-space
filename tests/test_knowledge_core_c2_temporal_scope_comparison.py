"""Core C2: accepted-evidence comparison is provenance-pinned and non-executable."""

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "knowledge/core/temporal/C2_SOURCE_SPECIFIC_TEMPORAL_SCOPE_COMPARISON_v0.1.json"


def _audit():
    return json.loads(AUDIT.read_text(encoding="utf-8"))


def _git_blob_sha(path):
    data = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\\0" + data).hexdigest()


def test_c2_pinned_accepted_inputs_and_three_exact_ids():
    audit = _audit()
    assert audit["accepted_main_sha"] == "fb3968aaae7f5bfaa29486334c2d115e17406193"
    assert [r["rule_id"] for r in audit["records"]] == [
        "CA06-580", "CA06-600", "TP02-175"
    ]
    assert audit["invariants"]["record_count"] == 3
    for item in audit["pinned_inputs"]:
        assert _git_blob_sha(ROOT / item["path"]) == item["sha"]


def test_c2_matches_previously_accepted_source_review_surfaces():
    audit = _audit()
    gap = json.loads(
        (ROOT / "knowledge/core/wp07b/GAP006_GROUP_FAVORABILITY_SOURCE_AUDIT_v0.1.json")
        .read_text(encoding="utf-8")
    )
    accepted = {r["rule_id"]: r for r in gap["evidence"]}
    for row in audit["records"]:
        source = accepted[row["rule_id"]]
        assert row["source_audit_evidence_id"] == source["id"]
        assert row["source_surface_from_accepted_audit"] == source["source_surface"]
        assert str(row["source_printed_page"]) in source["source_location"]
        assert source["executable"] is False


def test_c2_preserves_distinct_temporal_surfaces_and_legacy_non_authority():
    a, b, c = _audit()["records"]
    assert a["surface_type"] == "JUXTAPOSED_DECADE_YEAR_PERIOD_VALENCE"
    assert a["source_literal_or"] is False
    assert b["source_literal_or"] is True and b["natal_context_rule_id"] == "CA06-599"
    assert c["source_literal_and"] is True
    assert c["named_source_time_layers"] == ["YEAR", "SMALL_LIMIT"]
    assert all(not row["legacy_normalization_is_source_proof"] for row in (a, b, c))
    assert all(row["unknown"] for row in (a, b, c))


def test_c2_source_not_recertified_and_all_product_runtime_gates_closed():
    audit = _audit()
    source = audit["source"]
    assert source["original_scan_independently_viewed_this_unit"] is False
    assert source["source_recertified_this_unit"] is False
    assert audit["next_source_review"]["status"] == "NOT_INDEPENDENTLY_VISUALLY_REVERIFIED"
    assert all(not row["executable"] and not row["product_consumable"]
               for row in audit["records"])
    flags = audit["invariants"]
    assert flags["universal_deca_year_composition"] == "UNKNOWN_HOLD"
    assert not flags["shared_operator_added"]
    assert not flags["new_time_scale_added"]
    assert not flags["runtime_authority_added"]
    assert not flags["kib_lock_registry_modified"]
    assert not flags["human_gate_required_now"]
    assert audit["product_availability"]["decade_admission_authorized"] is False
    assert audit["product_availability"]["year_admission_authorized"] is False
