from pathlib import Path

from src.product.wealth_blocker_refresh import (
    load_wealth_blocker_refresh,
    validate_wealth_blocker_refresh,
)
from src.product.wealth_pilot import (
    compose_wealth_registries,
    load_pilot_registry,
    load_projection_rows,
)

ROOT = Path(__file__).resolve().parents[1]
W01 = ROOT / "validation/wp05/W01_wealth_projection_review_001_100.csv"
REFRESH = ROOT / "product/PL2K_WEALTH_BLOCKER_REFRESH_v0.1.csv"
BATCHES = [
    ROOT / "product/PL2C_WEALTH_PILOT_v0.1.json",
    ROOT / "product/PL2F_WEALTH_NORMALIZATION_BATCH2_v0.1.json",
    ROOT / "product/PL2H_WEALTH_CROSS_PALACE_BATCH_v0.1.json",
    ROOT / "product/PL2J_WEALTH_READY_BATCH1_v0.1.json",
    ROOT / "product/PL2J2_WEALTH_READY_BATCH2_v0.1.json",
]


def _state():
    rows = load_projection_rows(W01)
    registry = compose_wealth_registries(
        *(load_pilot_registry(path) for path in BATCHES)
    )
    pending = {
        row["projection_rule_id"]
        for row in rows
        if row["projection_rule_id"] not in registry["rules"]
    }
    refresh = load_wealth_blocker_refresh(REFRESH)
    counts = validate_wealth_blocker_refresh(
        refresh,
        expected_pending_rule_ids=pending,
    )
    return rows, registry, pending, refresh, counts


def test_refresh_matches_exactly_49_100_executable_state():
    rows, registry, pending, refresh, counts = _state()
    assert len(rows) == 100
    assert len(registry["rules"]) == 49
    assert len(pending) == 51
    assert len(refresh) == 51
    assert counts == {
        "ANTECEDENT_ENGINEERING": 10,
        "DEFER_PL3_TEMPORAL": 14,
        "HUMAN_GATE_REQUIRED": 8,
        "SOURCE_NORMALIZATION_REQUIRED": 15,
        "STRUCTURE_SOURCE_BACKED": 4,
    }


def test_ready_backlog_is_zero():
    _, _, _, refresh, _ = _state()
    assert not any(
        row.primary_blocker in {"LOCAL_ATOM_READY", "CROSS_PALACE_READY"}
        for row in refresh
    )


def test_valence_rules_are_human_gated():
    _, _, _, refresh, _ = _state()
    by_id = {row.projection_rule_id: row for row in refresh}
    for rule_id in {"W01-016", "W01-017", "W01-022", "W01-023", "W01-035"}:
        assert by_id[rule_id].route_class == "HUMAN_GATE_REQUIRED"
        assert by_id[rule_id].human_gate_status == "YES"


def test_baiguan_runtime_definition_is_human_gated():
    _, _, _, refresh, _ = _state()
    by_id = {row.projection_rule_id: row for row in refresh}
    for rule_id in {"W01-095", "W01-096", "W01-098"}:
        assert by_id[rule_id].route_class == "HUMAN_GATE_REQUIRED"
        assert "百官朝拱" in by_id[rule_id].support_basis


def test_source_backed_structure_candidates_are_bounded():
    _, _, _, refresh, _ = _state()
    source_backed = {
        row.projection_rule_id
        for row in refresh
        if row.route_class == "STRUCTURE_SOURCE_BACKED"
    }
    assert source_backed == {"W01-024", "W01-043", "W01-050", "W01-057"}


def test_temporal_rules_stay_out_of_pl2():
    _, _, _, refresh, _ = _state()
    temporal = [
        row for row in refresh
        if row.route_class == "DEFER_PL3_TEMPORAL"
    ]
    assert len(temporal) == 14
    assert all(
        row.recommended_work_unit == "PRODUCT_PL3_TEMPORAL_STATE"
        for row in temporal
    )


def test_next_no_gate_engineering_family_is_antecedent_linking():
    _, _, _, refresh, _ = _state()
    antecedent = [
        row for row in refresh
        if row.route_class == "ANTECEDENT_ENGINEERING"
    ]
    assert len(antecedent) == 10
    assert all(row.human_gate_status == "NO" for row in antecedent)
    assert all(
        row.recommended_work_unit == "PRODUCT_PL2M_ANTECEDENT_LINKING_V0_1"
        for row in antecedent
    )
