"""Bounded engineering checks; synthetic results are not Ziwei rule acceptance."""

import copy
import hashlib
import json
from dataclasses import replace
from pathlib import Path

import pytest

from product.experiments.spatiotemporal_v01.probe import (
    FIXTURE, ROOT, FactView, Occupancy, Scope, Verdict, digest, evaluate,
    fixture_view, logical, make_report, permutation, replay, stable, transform,
)
from src.product.condition_atoms import fact_from_atom


def board():
    return Occupancy(("TEST-A", "TEST-B"),
                     tuple((int(i == 0), int(i == 11)) for i in range(12)),
                     ("KNOWN",) * 12)


def atom(star="TEST-A", layer="YEAR"):
    return fact_from_atom("STAR_PRESENT", layer=layer, star=star)


def scope():
    return Scope("test-snapshot", "TEST-TARGET", "YEAR")


@pytest.mark.parametrize("offset", range(12))
def test_index_matrix_equivalence_inverse_and_input_immutability(offset):
    original = board()
    before = stable(original.__dict__)
    result = transform(original, offset, matrix=True)
    assert result == transform(original, offset)
    assert transform(result, -offset, matrix=True) == original
    assert stable(original.__dict__) == before
    assert all(sum(row) == 1 for row in permutation(offset))
    assert all(sum(col) == 1 for col in zip(*permutation(offset)))


@pytest.mark.parametrize("a", range(12))
@pytest.mark.parametrize("b", range(12))
def test_all_cyclic_compositions(a, b):
    assert transform(transform(board(), a, matrix=True), b, matrix=True) == transform(board(), a + b)


def test_independent_anchor_defines_direction_and_wraparound():
    result = transform(board(), 1, matrix=True)
    assert result.rows[1] == (1, 0)  # slot 0 -> slot 1
    assert result.rows[0] == (0, 1)  # slot 11 -> slot 0
    assert transform(board(), 0) == board()


@pytest.mark.parametrize("state", ["UNKNOWN", "MISSING", "CONFLICT"])
@pytest.mark.parametrize("matrix", [False, True])
def test_unknown_and_conflict_zero_cells_are_not_absence(state, matrix):
    states = list(board().states)
    states[3] = state
    partial = replace(board(), states=tuple(states))
    result = transform(partial, 4, matrix=matrix)
    assert result.lookup(7, "TEST-A") == Verdict("UNKNOWN", (state,))
    assert result.lookup(6, "TEST-A").truth == "FALSE"


@pytest.mark.parametrize("rows,states", [(((0, 0),) * 11, ("KNOWN",) * 12),
    (((2, 0),) * 12, ("KNOWN",) * 12), (((1, 0),) * 12, ("UNKNOWN",) * 12)])
def test_malformed_or_unresolved_positive_occupancy_rejected(rows, states):
    with pytest.raises(ValueError):
        Occupancy(("TEST-A", "TEST-B"), rows, states)


@pytest.mark.parametrize("a,b,and_expected,or_expected", [
    ("TRUE", "TRUE", "TRUE", "TRUE"), ("TRUE", "FALSE", "FALSE", "TRUE"),
    ("TRUE", "UNKNOWN", "UNKNOWN", "TRUE"), ("FALSE", "TRUE", "FALSE", "TRUE"),
    ("FALSE", "FALSE", "FALSE", "FALSE"), ("FALSE", "UNKNOWN", "FALSE", "UNKNOWN"),
    ("UNKNOWN", "TRUE", "UNKNOWN", "TRUE"), ("UNKNOWN", "FALSE", "FALSE", "UNKNOWN"),
    ("UNKNOWN", "UNKNOWN", "UNKNOWN", "UNKNOWN"),
])
def test_complete_three_valued_and_or_table(a, b, and_expected, or_expected):
    operands = [Verdict(a, ("A",)), Verdict(b, ("B",))]
    assert logical("AND", operands).truth == and_expected
    assert logical("OR", operands).truth == or_expected
    assert logical("AND", operands).reasons == ("A", "B")


@pytest.mark.parametrize("value,expected", [("TRUE", "FALSE"), ("FALSE", "TRUE"), ("UNKNOWN", "UNKNOWN")])
def test_three_valued_negation(value, expected):
    assert logical("NOT", [Verdict(value, ())]).truth == expected


def test_absence_requires_explicit_scope_complete_or_negative_evidence():
    s, a = scope(), atom()
    assert FactView().lookup(s, a).truth == "UNKNOWN"
    assert FactView(negative=[(s, a)]).lookup(s, a).truth == "FALSE"
    assert FactView(complete=[(s, "STAR_PRESENT")]).lookup(s, a).truth == "FALSE"
    conflict = FactView(positive=[(s, a)], negative=[(s, a)]).lookup(s, a)
    assert conflict == Verdict("UNKNOWN", ("CONFLICT",))


@pytest.mark.parametrize("other", [Scope("other-snapshot", "TEST-TARGET", "YEAR"),
                                    Scope("test-snapshot", "other-target", "YEAR")])
def test_target_and_snapshot_identity_prevent_fact_leakage(other):
    view = FactView(positive=[(scope(), atom())], complete=[(scope(), "STAR_PRESENT")])
    assert view.lookup(other, atom()).truth == "UNKNOWN"


def test_layer_binding_is_required_and_multi_layer_rules_are_not_silently_enabled():
    with pytest.raises(ValueError, match="layer differs"):
        FactView(positive=[(scope(), atom(layer="DECADE"))])
    with pytest.raises(ValueError, match="layer differs"):
        evaluate("TEST-MIXED", scope(), FactView(), all_of=[atom(layer="DECADE")])


def test_guard_provenance_replays_and_changed_evidence_changes_execution_identity():
    s, a, b = scope(), atom(), atom("TEST-B")
    view = FactView(positive=[(s, a)], negative=[(s, b)])
    result = evaluate("TEST-TRACE", s, view, all_of=[a], none_of=[b])
    assert result["verdict"]["truth"] == "TRUE"
    assert result == replay(json.loads(json.dumps(result)))
    assert result == evaluate("TEST-TRACE", s, view, all_of=[a], none_of=[b])
    changed = evaluate("TEST-TRACE", s, FactView(positive=[(s, a)]), all_of=[a], none_of=[b])
    assert changed["verdict"]["truth"] == "UNKNOWN"
    assert changed["execution_id"] != result["execution_id"]
    assert all(t["input_id"] for t in result["trace"])
    assert result["canonical_accepted"] is result["runtime_effect_allowed"] is False


def test_or_branch_can_be_true_with_unknown_other_branch_but_records_missingness():
    s, a, b = scope(), atom(), atom("TEST-B")
    result = evaluate("TEST-OR", s, FactView(positive=[(s, a)]), any_of=[[a, b]])
    assert result["verdict"]["truth"] == "TRUE"
    assert "MISSING_WITHOUT_COMPLETENESS" in result["verdict"]["reasons"]


def test_only_explicit_test_rules_with_conditions_run():
    for rule, kwargs in [("CANONICAL-ID", {"all_of": [atom()]}), ("TEST-EMPTY", {})]:
        with pytest.raises(ValueError):
            evaluate(rule, scope(), FactView(), **kwargs)


def test_replay_rejects_changed_policy_or_code_and_detects_trace_tampering():
    record = evaluate("TEST-REPLAY", scope(), FactView(positive=[(scope(), atom())]), all_of=[atom()])
    for field in ("policy", "implementation_sha256"):
        changed = copy.deepcopy(record)
        changed[field] = "different-version"
        with pytest.raises(ValueError, match="same experimental policy"):
            replay(changed)
    changed = copy.deepcopy(record)
    changed["trace"][0]["positive"] = False
    assert replay(changed) != record


def test_accepted_fixture_preserves_scope_transformations_without_star_join():
    snapshot = json.loads((ROOT / FIXTURE).read_text())
    before = copy.deepcopy(snapshot)
    view = fixture_view(snapshot)
    s = Scope(digest(snapshot), "T-DEMO", "YEAR")
    unbound = fact_from_atom("TRANSFORMATION_PRESENT", layer="YEAR", mutagen="科")
    bound = fact_from_atom("TRANSFORMATION_PRESENT", layer="YEAR", star="天马", palace_name="命宫", mutagen="科")
    assert view.lookup(s, unbound).truth == "TRUE"
    assert view.lookup(s, bound).truth == "UNKNOWN"
    assert len({item[0].layer for item in view.positive}) == 6
    assert snapshot == before


def test_explicit_star_binding_survives_without_cross_layer_merging():
    snapshot = json.loads((ROOT / FIXTURE).read_text())
    snapshot["temporal"][0]["scopes"]["yearly"]["stars"][0][0]["mutagen"] = "忌"
    view = fixture_view(snapshot)
    s = Scope(digest(snapshot), "T-DEMO", "YEAR")
    bound = fact_from_atom("TRANSFORMATION_PRESENT", layer="YEAR", star="天马", palace_name="命宫", mutagen="忌")
    assert view.lookup(s, bound).truth == "TRUE"
    d = replace(s, layer="DECADE")
    decade_bound = fact_from_atom("TRANSFORMATION_PRESENT", layer="DECADE", star="天马", palace_name="命宫", mutagen="忌")
    assert view.lookup(d, decade_bound).truth == "UNKNOWN"


def test_checked_in_report_is_reproducible_and_fixture_matches_manifest():
    directory = ROOT / "product/experiments/spatiotemporal_v01"
    report = make_report()
    assert report == json.loads((directory / "COMPARISON_REPORT_v0.1.json").read_text())
    manifest = json.loads((directory / "fixture_manifest_v0.1.json").read_text())
    for item in manifest["inputs"]:
        raw = (ROOT / item["path"]).read_bytes()
        assert hashlib.sha256(raw).hexdigest() == item["sha256"]
        assert hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest() == item["git_blob_sha"]
    assert all(report["checks"].values())
    assert report["decision"] == "KEEP_INDEX_BASELINE_NO_PRODUCTION_MIGRATION"
    assert report["fixture"]["scope_slots"] == 2 and report["fixture"]["natal_empty"] is True
    assert report["canonical_accepted"] is report["runtime_effect_allowed"] is False
