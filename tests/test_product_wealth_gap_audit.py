from pathlib import Path

from src.product.wealth_gap_audit import (
    READINESS_CLASSES,
    load_wealth_gap_audit,
    validate_wealth_gap_audit,
)
from src.product.wealth_pilot import (
    compose_wealth_registries,
    load_pilot_registry,
    load_projection_rows,
)

ROOT = Path(__file__).resolve().parents[1]
W01 = ROOT / "validation/wp05/W01_wealth_projection_review_001_100.csv"
B01 = ROOT / "product/PL2C_WEALTH_PILOT_v0.1.json"
B02 = ROOT / "product/PL2F_WEALTH_NORMALIZATION_BATCH2_v0.1.json"
B03 = ROOT / "product/PL2H_WEALTH_CROSS_PALACE_BATCH_v0.1.json"
AUDIT = ROOT / "product/PL2I_WEALTH_STRUCTURE_COVERAGE_GAP_AUDIT_v0.1.csv"


def _summary():
    rows = load_projection_rows(W01)
    registry = compose_wealth_registries(
        load_pilot_registry(B01),
        load_pilot_registry(B02),
        load_pilot_registry(B03),
    )
    audit = load_wealth_gap_audit(AUDIT)
    return rows, registry, audit, validate_wealth_gap_audit(
        rows,
        registry["rules"].keys(),
        audit,
    )


def test_gap_audit_covers_exactly_all_72_pending_rules():
    _, _, audit, summary = _summary()
    assert len(audit) == 72
    assert summary.total_pending == 72
    assert summary.immediately_ready == 21
    assert summary.counts == {
        "LOCAL_ATOM_READY": 14,
        "CROSS_PALACE_READY": 7,
        "NEEDS_STRUCTURE_PRIMITIVE": 16,
        "NEEDS_TEMPORAL_STATE": 14,
        "NEEDS_PATH_HISTORY": 0,
        "NEEDS_VALENCE_MODEL": 5,
        "ANTECEDENT_DEPENDENT": 10,
        "NORMALIZATION_AMBIGUOUS": 6,
    }
    assert set(summary.counts) == set(READINESS_CLASSES)


def test_no_executable_rule_is_reaudited_as_pending():
    _, registry, audit, _ = _summary()
    audit_ids = {row.projection_rule_id for row in audit}
    assert not audit_ids.intersection(registry["rules"])


def test_all_non_natal_pending_rules_are_temporal_blocked():
    _, _, audit, _ = _summary()
    non_natal = [row for row in audit if row.time_layer != "NATAL"]
    assert len(non_natal) == 13
    assert {row.readiness_class for row in non_natal} == {
        "NEEDS_TEMPORAL_STATE"
    }


def test_natal_temporal_guard_is_explicitly_identified():
    _, _, audit, _ = _summary()
    row = next(x for x in audit if x.projection_rule_id == "W01-089")
    assert row.time_layer == "NATAL"
    assert row.readiness_class == "NEEDS_TEMPORAL_STATE"


def test_ready_rows_have_no_hidden_secondary_blockers():
    _, _, audit, _ = _summary()
    ready = [
        row
        for row in audit
        if row.readiness_class in {"LOCAL_ATOM_READY", "CROSS_PALACE_READY"}
    ]
    assert len(ready) == 21
    assert all(row.secondary_blockers == () for row in ready)


def test_path_history_count_is_zero_because_w01_has_no_history_feedback():
    rows, _, _, summary = _summary()
    assert not any(row.get("history_feedback") for row in rows)
    assert summary.counts["NEEDS_PATH_HISTORY"] == 0
