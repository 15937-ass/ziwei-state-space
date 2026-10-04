"""Typed condition atoms for PL2 executable knowledge.

This module defines an engineering representation only. It does not infer
traditional Zi Wei semantics from source text and it does not auto-create
condition atoms from free-form prose.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any, Mapping


ALLOWED_ATOM_TYPES = frozenset(
    {
        "SUBJECT_PRESENT",
        "STAR_PRESENT",
        "TRANSFORMATION_PRESENT",
        "PALACE_PRESENT",
        "PALACE_HAS_STAR",
        "PALACE_RELATION",
        "STRUCTURE_PRESENT",
        "BRANCH_PRESENT",
        "TIME_LAYER",
        "MODE_PRESENT",
        "TAG_PRESENT",
    }
)


@dataclass(frozen=True)
class ConditionAtom:
    atom_type: str
    args: tuple[tuple[str, str], ...]

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "ConditionAtom":
        atom_type = str(value.get("atom_type", "")).strip()
        if atom_type not in ALLOWED_ATOM_TYPES:
            raise ValueError(f"unsupported atom_type: {atom_type or '<empty>'}")

        raw_args = value.get("args")
        if not isinstance(raw_args, Mapping) or not raw_args:
            raise ValueError("ConditionAtom.args must be a non-empty mapping")

        normalized: list[tuple[str, str]] = []
        for key, raw in raw_args.items():
            k = str(key).strip()
            v = str(raw).strip()
            if not k or not v:
                raise ValueError("ConditionAtom args require non-empty keys and values")
            normalized.append((k, v))

        return cls(atom_type=atom_type, args=tuple(sorted(normalized)))

    def canonical(self) -> str:
        payload = {
            "args": {key: value for key, value in self.args},
            "type": self.atom_type,
        }
        return "atom:" + json.dumps(
            payload,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )


@dataclass(frozen=True)
class CompiledCondition:
    all_of: tuple[str, ...] = ()
    any_of: tuple[tuple[str, ...], ...] = ()
    none_of: tuple[str, ...] = ()

    def matches(self, facts: frozenset[str]) -> bool:
        if not set(self.all_of).issubset(facts):
            return False
        for group in self.any_of:
            if not set(group).intersection(facts):
                return False
        if set(self.none_of).intersection(facts):
            return False
        return True

    def matched_facts(self, facts: frozenset[str]) -> tuple[str, ...]:
        if not self.matches(facts):
            return ()
        matched = set(self.all_of)
        for group in self.any_of:
            matched.update(set(group).intersection(facts))
        return tuple(sorted(matched))


def _compile_atom(value: Mapping[str, Any]) -> str:
    return ConditionAtom.from_mapping(value).canonical()


def compile_condition_spec(spec: Mapping[str, Any]) -> CompiledCondition:
    """Compile a structured boolean condition into canonical fact keys.

    Semantics:
    - all_of: every atom must be present.
    - any_of: each nested group requires at least one present atom.
    - none_of: none of the atoms may be present.

    No free-form text parsing occurs here.
    """

    all_raw = spec.get("all_of", [])
    any_raw = spec.get("any_of", [])
    none_raw = spec.get("none_of", [])

    if not isinstance(all_raw, list):
        raise ValueError("all_of must be a list")
    if not isinstance(any_raw, list):
        raise ValueError("any_of must be a list of atom lists")
    if not isinstance(none_raw, list):
        raise ValueError("none_of must be a list")

    all_of = tuple(sorted({_compile_atom(atom) for atom in all_raw}))

    any_groups: list[tuple[str, ...]] = []
    for group in any_raw:
        if not isinstance(group, list) or not group:
            raise ValueError("each any_of group must be a non-empty list")
        compiled = tuple(sorted({_compile_atom(atom) for atom in group}))
        any_groups.append(compiled)

    none_of = tuple(sorted({_compile_atom(atom) for atom in none_raw}))

    overlap = set(all_of).intersection(none_of)
    if overlap:
        raise ValueError("condition cannot require and forbid the same atom")

    return CompiledCondition(
        all_of=all_of,
        any_of=tuple(sorted(any_groups)),
        none_of=none_of,
    )


def compile_condition_registry(document: Mapping[str, Any]) -> dict[str, CompiledCondition]:
    version = str(document.get("schema_version", "")).strip()
    if version != "0.1":
        raise ValueError("condition registry schema_version must be 0.1")

    rules = document.get("rules")
    if not isinstance(rules, Mapping):
        raise ValueError("condition registry rules must be a mapping")

    out: dict[str, CompiledCondition] = {}
    for raw_rule_id, spec in rules.items():
        rule_id = str(raw_rule_id).strip()
        if not rule_id:
            raise ValueError("condition registry rule_id must be non-empty")
        if rule_id in out:
            raise ValueError(f"duplicate rule_id in condition registry: {rule_id}")
        if not isinstance(spec, Mapping):
            raise ValueError(f"condition spec for {rule_id} must be a mapping")
        out[rule_id] = compile_condition_spec(spec)
    return out


def fact_from_atom(atom_type: str, **args: str) -> str:
    """Build a canonical runtime fact without exposing serialization details."""
    return ConditionAtom.from_mapping({"atom_type": atom_type, "args": args}).canonical()
