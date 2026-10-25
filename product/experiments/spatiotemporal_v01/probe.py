"""TEST_ONLY engineering comparison. No production module imports this probe.

Slot numbers and 0/1 entries encode a synthetic ring, never qi or event strength.
The three-valued policy below is experimental, not a shared Knowledge contract.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

from src.product.condition_atoms import compile_condition_spec, fact_from_atom
from src.product.temporal_asset_adapter import (
    SCOPE_TO_LAYER,
    adapt_target_from_full_snapshot,
)

ROOT = Path(__file__).resolve().parents[3]
FIXTURE = "product/PL3T_TEMPORAL_ASSET_FIXTURE_v0.1.json"
STATUS = "TEST_ONLY_NOT_CANONICAL"
POLICY = "TEST-THREE-VALUED-01"
STATES = frozenset({"KNOWN", "UNKNOWN", "MISSING", "CONFLICT"})


def stable(value) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def digest(value) -> str:
    return hashlib.sha256(stable(value).encode()).hexdigest()


def permutation(offset: int) -> tuple[tuple[int, ...], ...]:
    """Positive offset moves source slot i to destination (i+offset) mod 12."""
    if type(offset) is not int:
        raise ValueError("offset must be an integer")
    return tuple(tuple(int(src == (dest - offset) % 12) for src in range(12))
                 for dest in range(12))


@dataclass(frozen=True)
class Occupancy:
    columns: tuple[str, ...]
    rows: tuple[tuple[int, ...], ...]
    states: tuple[str, ...]

    def __post_init__(self):
        if not self.columns or len(set(self.columns)) != len(self.columns):
            raise ValueError("columns must be nonempty and unique")
        if len(self.rows) != 12 or len(self.states) != 12:
            raise ValueError("synthetic coordinate frame requires exactly 12 slots")
        for row, state in zip(self.rows, self.states):
            if state not in STATES or len(row) != len(self.columns):
                raise ValueError("invalid row state or shape")
            if any(type(v) is not int or v not in (0, 1) for v in row):
                raise ValueError("occupancy entries must be structural 0/1")
            if state != "KNOWN" and any(row):
                raise ValueError("unresolved row must not assert positive occupancy")

    def lookup(self, slot: int, column: str) -> "Verdict":
        if type(slot) is not int or slot not in range(12):
            raise ValueError("slot outside explicit frame")
        index = self.columns.index(column)
        state = self.states[slot]
        if state != "KNOWN":
            return Verdict("UNKNOWN", (state,))
        return Verdict("TRUE" if self.rows[slot][index] else "FALSE", ("KNOWN_SLOT",))


def transform(board: Occupancy, offset: int, *, matrix: bool = False) -> Occupancy:
    if type(offset) is not int:
        raise ValueError("offset must be an integer")
    if matrix:
        p = permutation(offset)
        rows = tuple(tuple(sum(p[d][s] * board.rows[s][c] for s in range(12))
                           for c in range(len(board.columns))) for d in range(12))
    else:
        rows = tuple(board.rows[(d - offset) % 12] for d in range(12))
    states = tuple(board.states[(d - offset) % 12] for d in range(12))
    return Occupancy(board.columns, rows, states)


@dataclass(frozen=True, order=True)
class Scope:
    snapshot_sha256: str
    target_id: str
    layer: str

    def __post_init__(self):
        if not self.snapshot_sha256 or not self.target_id or self.layer not in SCOPE_TO_LAYER.values():
            raise ValueError("scope requires snapshot, target and an existing temporal layer")


@dataclass(frozen=True)
class Verdict:
    truth: str
    reasons: tuple[str, ...]


def logical(op: str, values: Iterable[Verdict]) -> Verdict:
    items = tuple(values)
    truths = tuple(v.truth for v in items)
    if any(t not in {"TRUE", "FALSE", "UNKNOWN"} for t in truths):
        raise ValueError("unsupported truth value")
    if op == "NOT":
        if len(items) != 1:
            raise ValueError("NOT takes one operand")
        result = {"TRUE": "FALSE", "FALSE": "TRUE", "UNKNOWN": "UNKNOWN"}[truths[0]]
    elif op == "AND":
        result = "FALSE" if "FALSE" in truths else "UNKNOWN" if "UNKNOWN" in truths else "TRUE"
    elif op == "OR":
        result = "TRUE" if "TRUE" in truths else "UNKNOWN" if "UNKNOWN" in truths else "FALSE"
    else:
        raise ValueError("unsupported logical operator")
    return Verdict(result, tuple(sorted({r for v in items for r in v.reasons})))


def atom_type(atom: str, scope: Scope) -> str:
    if not atom.startswith("atom:"):
        raise ValueError("typed atom required")
    payload = json.loads(atom[5:])
    if payload["args"].get("layer") != scope.layer:
        raise ValueError("atom layer differs from explicit query scope")
    return payload["type"]


class FactView:
    def __init__(self, positive=(), negative=(), complete=()):
        self.positive = frozenset(positive)
        self.negative = frozenset(negative)
        # Only an explicit TEST_ONLY completeness assertion permits absence -> FALSE.
        self.complete = frozenset(complete)
        for scope, atom in self.positive | self.negative:
            atom_type(atom, scope)

    def lookup(self, scope: Scope, atom: str) -> Verdict:
        kind = atom_type(atom, scope)
        key = (scope, atom)
        if key in self.positive and key in self.negative:
            return Verdict("UNKNOWN", ("CONFLICT",))
        if key in self.positive:
            return Verdict("TRUE", ("EXPLICIT_PRESENT",))
        if key in self.negative:
            return Verdict("FALSE", ("EXPLICIT_NEGATIVE",))
        if (scope, kind) in self.complete:
            return Verdict("FALSE", ("TEST_ONLY_COMPLETE_PREDICATE",))
        return Verdict("UNKNOWN", ("MISSING_WITHOUT_COMPLETENESS",))


def evaluate(rule_id: str, scope: Scope, view: FactView, *, all_of=(), any_of=(), none_of=()):
    if not rule_id.startswith("TEST-"):
        raise ValueError("only TEST- rules may execute in this isolated probe")
    all_of, none_of = tuple(all_of), tuple(none_of)
    groups = tuple(tuple(g) for g in any_of)
    if not all_of and not none_of and not groups:
        raise ValueError("test rule must declare a condition")
    if any(not g for g in groups):
        raise ValueError("empty OR group")
    # One explicitly bound layer per rule in v0.1. Cross-layer execution is deferred.
    atoms = tuple(sorted(set(all_of) | set(none_of) | {a for g in groups for a in g}))
    traces = []
    for atom in atoms:
        value = view.lookup(scope, atom)
        present, negative = (scope, atom) in view.positive, (scope, atom) in view.negative
        traces.append({"atom": atom, **asdict(value), "positive": present,
                       "negative": negative, "predicate_complete":
                       (scope, atom_type(atom, scope)) in view.complete,
                       "input_id": digest([asdict(scope), atom, present, negative,
                                            (scope, atom_type(atom, scope)) in view.complete])})
    values = {t["atom"]: Verdict(t["truth"], tuple(t["reasons"])) for t in traces}
    result = logical("AND", [*(values[a] for a in all_of),
                             *(logical("OR", (values[a] for a in g)) for g in groups),
                             *(logical("NOT", [values[a]]) for a in none_of)])
    payload = {"status": STATUS, "policy": POLICY, "rule_id": rule_id,
               "implementation_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
               "scope": asdict(scope), "all_of": list(all_of),
               "any_of": [list(g) for g in groups], "none_of": list(none_of),
               "verdict": asdict(result), "trace": traces,
               "canonical_accepted": False, "runtime_effect_allowed": False}
    return json.loads(stable({**payload, "execution_id": digest(payload)}))


def replay(record):
    if (record["policy"] != POLICY or record["implementation_sha256"] !=
            hashlib.sha256(Path(__file__).read_bytes()).hexdigest()):
        raise ValueError("replay requires the same experimental policy and code version")
    scope = Scope(**record["scope"])
    view = FactView([(scope, t["atom"]) for t in record["trace"] if t["positive"]],
                    [(scope, t["atom"]) for t in record["trace"] if t["negative"]],
                    [(scope, atom_type(t["atom"], scope)) for t in record["trace"]
                     if t["predicate_complete"]])
    return evaluate(record["rule_id"], scope, view, all_of=record["all_of"],
                    any_of=record["any_of"], none_of=record["none_of"])


def fixture_view(snapshot):
    snapshot_sha = digest(snapshot)
    facts = []
    for target in snapshot["temporal"]:
        target_id = target["target"]["target_id"]
        bundle = adapt_target_from_full_snapshot(snapshot, target_id=target_id)
        for atom in bundle.condition_facts:
            layer = json.loads(atom[5:])["args"]["layer"]
            facts.append((Scope(snapshot_sha, target_id, layer), atom))
    # The accepted demo has two slots and an empty natal object: no completeness claim.
    return FactView(facts)


def make_report():
    raw = (ROOT / FIXTURE).read_bytes()
    snapshot = json.loads(raw)
    before = stable(snapshot)
    view = fixture_view(snapshot)
    scope = Scope(digest(snapshot), "T-DEMO", "YEAR")
    present = fact_from_atom("STAR_PRESENT", layer="YEAR", star="天马")
    missing = fact_from_atom("STAR_PRESENT", layer="YEAR", star="TEST-MISSING")
    scope_mutagen = fact_from_atom("TRANSFORMATION_PRESENT", layer="YEAR", mutagen="科")
    unsupported_join = fact_from_atom("TRANSFORMATION_PRESENT", layer="YEAR",
                                     palace_name="命宫", star="天马", mutagen="科")
    baseline = compile_condition_spec({"none_of": [{"atom_type": "STAR_PRESENT",
                    "args": {"layer": "YEAR", "star": "TEST-MISSING"}}]})
    bundle = adapt_target_from_full_snapshot(snapshot, target_id="T-DEMO")
    rules = [evaluate("TEST-PRESENT", scope, view, all_of=[present]),
             evaluate("TEST-ABSENT-NEGATION", scope, view, none_of=[missing]),
             evaluate("TEST-SCOPE-TRANSFORMATION", scope, view, all_of=[scope_mutagen]),
             evaluate("TEST-NO-INVENTED-STAR-JOIN", scope, view, all_of=[unsupported_join])]
    board = Occupancy(("TEST-A", "TEST-B"), tuple((int(i == 0), int(i == 11))
                      for i in range(12)), ("KNOWN",) * 12)
    equal = all(transform(board, k) == transform(board, k, matrix=True) for k in range(12))
    inverses = all(transform(transform(board, k, matrix=True), -k, matrix=True) == board
                   for k in range(12))
    compositions = all(transform(transform(board, a, matrix=True), b, matrix=True)
                       == transform(board, a + b, matrix=True)
                       for a in range(12) for b in range(12))
    return {"status": STATUS, "policy": POLICY,
            "implementation_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "fixture": {"path": FIXTURE, "sha256": hashlib.sha256(raw).hexdigest(),
                        "git_blob_sha": hashlib.sha1(b"blob " + str(len(raw)).encode()
                                                    + b"\0" + raw).hexdigest(),
                        "kind": "ACCEPTED_SYNTHETIC_ENGINEERING_DEMO",
                        "scope_slots": 2, "natal_empty": not bool(snapshot["natal"])},
            "checks": {"all_12_offsets_agree": equal, "all_12_inverses": inverses,
                       "all_144_compositions": compositions, "input_unchanged": before == stable(snapshot),
                       "all_traces_replay": all(replay(r) == r for r in rules)},
            "baseline_observation": {"missing_none_of_returns": baseline.matches(frozenset(bundle.condition_facts)),
                       "experimental_missing_none_of": rules[1]["verdict"]["truth"],
                       "production_bug_claimed": False},
            "operation_counts_per_12_by_2_view": {"index_row_lookups": 12,
                       "dense_matrix_multiply_terms": 288, "timing_benchmark": "NOT_RUN"},
            "rules": rules,
            "decision": "KEEP_INDEX_BASELINE_NO_PRODUCTION_MIGRATION",
            "not_evaluated": ["real_chart_coordinate_mapping", "full_natal_occupancy",
                              "canonical_cross_layer_reaction_semantics", "predictive_validity",
                              "rule_authoring_cost_in_real_corpus", "runtime_performance"],
            "next_core_questions": ["predicate completeness / negation contract",
                                    "cross-layer binding and temporal-instance contract"],
            "canonical_accepted": False, "runtime_effect_allowed": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="write TEST_ONLY comparison JSON")
    args = parser.parse_args()
    report = json.dumps(make_report(), ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.write_text(report, encoding="utf-8")
    else:
        print(report, end="")


if __name__ == "__main__":
    main()
