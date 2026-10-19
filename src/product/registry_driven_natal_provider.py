"""Registry-driven PL3-N provider for bounded, source-verified natal domains.

This provider executes only rules explicitly selected in a Product-owned
normalization registry. It does not infer condition atoms from source prose.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Mapping

from .condition_atoms import compile_condition_spec
from .evidence_bridge import graph_to_evidence_package
from .natal_prior import NatalDomainEvidence
from .palace_structure import (
    PalaceOntology,
    load_palace_ontology,
    resolve_palace_structure,
)
from .rule_runtime import RuleIR, RuleRuntime, RuntimeState, compile_rule_row
from .structure_primitives import source_backed_structure_facts
from .wealth_pilot import load_projection_rows


_ALLOWED_REVIEW_STATUSES = frozenset({"SOURCE_SPAN_VERIFIED", "HUMAN_VERIFIED"})


def _truthy(value: Any) -> bool:
    return str(value or "").strip().lower() in {"1", "true", "yes", "y"}


def _engine_version(snapshot: Mapping[str, Any]) -> str:
    engine = snapshot.get("engine", {})
    if not isinstance(engine, Mapping):
        return ""
    return ":".join(
        value
        for value in (
            str(engine.get("name", "")).strip(),
            str(engine.get("version", "")).strip(),
        )
        if value
    )


@dataclass
class RegistryDrivenNatalDomainProvider:
    """Execute one domain's explicit normalized registry against a chart snapshot."""

    projection_rows: list[dict[str, str]]
    registry: Mapping[str, Any]
    palace_ontology: PalaceOntology
    _executable_rules: tuple[RuleIR, ...] = field(init=False, repr=False)
    _runtime: RuleRuntime = field(init=False, repr=False)

    def __post_init__(self) -> None:
        if str(self.registry.get("schema_version", "")).strip() != "0.1":
            raise ValueError("domain provider registry schema_version must be 0.1")
        for key in ("provider_id", "domain_id", "palace_id", "palace_name", "topic_scope", "knowledge_version"):
            if not str(self.registry.get(key, "")).strip():
                raise ValueError(f"domain provider registry requires {key}")
        if str(self.registry.get("time_layer", "")).strip() != "NATAL":
            raise ValueError("PL3-N domain provider accepts NATAL rules only")

        rules = self.registry.get("rules")
        if not isinstance(rules, Mapping) or not rules:
            raise ValueError("domain provider registry requires a non-empty rules mapping")

        row_index: dict[str, Mapping[str, str]] = {}
        for row in self.projection_rows:
            rule_id = str(row.get("projection_rule_id", "")).strip()
            if not rule_id:
                raise ValueError("projection row missing projection_rule_id")
            if rule_id in row_index:
                raise ValueError(f"duplicate projection_rule_id: {rule_id}")
            row_index[rule_id] = row

        palace_id = str(self.registry["palace_id"]).strip()
        palace_name = str(self.registry["palace_name"]).strip()
        topic_scope = str(self.registry["topic_scope"]).strip()
        executable: list[RuleIR] = []

        for raw_rule_id in sorted(rules):
            rule_id = str(raw_rule_id).strip()
            if not rule_id:
                raise ValueError("registry rule_id must be non-empty")
            spec = rules[raw_rule_id]
            if not isinstance(spec, Mapping):
                raise ValueError(f"{rule_id}: registry rule spec must be an object")

            source = row_index.get(rule_id)
            if source is None:
                raise ValueError(f"{rule_id}: selected rule missing from projection source")

            review_status = str(source.get("review_status", "")).strip()
            if review_status not in _ALLOWED_REVIEW_STATUSES or not _truthy(
                source.get("source_span_verified")
            ):
                raise ValueError(
                    f"{rule_id}: executable rule requires verified source provenance"
                )
            if _truthy(source.get("case_support_only")):
                raise ValueError(f"{rule_id}: CASE_SUPPORT_ONLY cannot execute")
            if str(source.get("time_layer", "")).strip() != "NATAL":
                raise ValueError(f"{rule_id}: PL3-N provider accepts NATAL rows only")
            if str(source.get("palace_id", "")).strip() != palace_id:
                raise ValueError(
                    f"{rule_id}: source palace {source.get('palace_id')!r} "
                    f"does not match provider palace {palace_id!r}"
                )

            checks = {
                "condition": "expected_condition",
                "projection_target": "expected_projection_target",
                "projection_mode": "expected_projection_mode",
            }
            for source_field, registry_field in checks.items():
                expected = str(spec.get(registry_field, "")).strip()
                actual = str(source.get(source_field, "")).strip()
                if not expected:
                    raise ValueError(
                        f"{rule_id}: registry requires {registry_field}"
                    )
                if actual != expected:
                    raise ValueError(
                        f"{rule_id}: canonical source drift in {source_field}: "
                        f"{actual!r} != {expected!r}"
                    )

            condition_document = spec.get("condition")
            if not isinstance(condition_document, Mapping):
                raise ValueError(f"{rule_id}: explicit structured condition is required")
            condition = compile_condition_spec(condition_document)
            normalized_row = {
                "rule_id": rule_id,
                "school": str(self.registry.get("school", "中州派")).strip() or "中州派",
                "source_work": str(source.get("source_id", "")).strip(),
                "source_location": str(source.get("source_location", "")).strip(),
                "subject": palace_name,
                "context": str(self.registry.get("domain_id", "")).strip(),
                "condition": str(source.get("condition", "")).strip(),
                "time_scope": json.dumps(["NATAL"], ensure_ascii=False),
                "palace_scope": json.dumps([palace_id], ensure_ascii=False),
                "topic_scope": json.dumps([topic_scope], ensure_ascii=False),
                "operator": "projection",
                "target_type": str(source.get("projection_domain", "")).strip(),
                "target_normalized": str(source.get("projection_target", "")).strip(),
                "state_change": str(source.get("projection_mode", "")).strip(),
                "valence": "",
                "source_epistemic": "WP05_SOURCE_SPAN_VERIFIED",
                "normalization_epistemic": "IMPLEMENTATION",
                "review_status": review_status,
                "source_span_verified": source.get("source_span_verified", ""),
                "normalization_verified": "true",
                "evidence_text": str(source.get("condition", "")).strip(),
                "antecedent_rule_ids": spec.get("antecedent_rule_ids", []),
            }
            if not normalized_row["source_work"] or not normalized_row["source_location"]:
                raise ValueError(f"{rule_id}: source_id and source_location are required")
            if not normalized_row["target_type"] or not normalized_row["target_normalized"]:
                raise ValueError(
                    f"{rule_id}: projection_domain and projection_target are required"
                )
            if not normalized_row["state_change"]:
                raise ValueError(f"{rule_id}: projection_mode is required")

            ir, issue = compile_rule_row(normalized_row, condition_spec=condition)
            if issue is not None or ir is None:
                reason = issue.reason if issue is not None else "unknown compile failure"
                raise ValueError(f"{rule_id}: executable compilation failed: {reason}")
            executable.append(ir)

        executable_rules = tuple(sorted(executable, key=lambda item: item.rule_id))
        runtime = RuleRuntime(executable_rules)
        object.__setattr__(self, "_executable_rules", executable_rules)
        object.__setattr__(self, "_runtime", runtime)

    @property
    def domain_id(self) -> str:
        return str(self.registry["domain_id"]).strip()

    @property
    def knowledge_version(self) -> str:
        return str(self.registry["knowledge_version"]).strip()

    @property
    def executable_rule_count(self) -> int:
        return len(self._executable_rules)

    def build_domain_evidence(
        self,
        snapshot: Mapping[str, Any],
        *,
        question: str = "",
    ) -> NatalDomainEvidence:
        structure = resolve_palace_structure(snapshot, self.palace_ontology)
        facts = set(structure.runtime_facts())
        facts.update(source_backed_structure_facts(structure))
        frozen_facts = frozenset(facts)
        palace_id = str(self.registry["palace_id"]).strip()
        topic_scope = str(self.registry["topic_scope"]).strip()
        state = RuntimeState(
            facts=frozen_facts,
            latent_states={},
            time_scope="NATAL",
            palace_scope=palace_id,
        )
        graph = self._runtime.match(
            state,
            question_scope=topic_scope,
        )

        selected_ids = {rule.rule_id for rule in self._executable_rules}
        eligible_rows = [
            row
            for row in self.projection_rows
            if str(row.get("palace_id", "")).strip() == palace_id
            and str(row.get("time_layer", "")).strip() == "NATAL"
            and not _truthy(row.get("case_support_only"))
            and str(row.get("review_status", "")).strip() in _ALLOWED_REVIEW_STATUSES
            and _truthy(row.get("source_span_verified"))
        ]
        pending = max(0, len({row["projection_rule_id"] for row in eligible_rows}) - len(selected_ids))
        coverage = {
            "EXECUTABLE": len(selected_ids),
            "NORMALIZATION_PENDING": pending,
            "CASE_SUPPORT_ONLY_EXCLUDED": sum(
                1
                for row in self.projection_rows
                if str(row.get("palace_id", "")).strip() == palace_id
                and _truthy(row.get("case_support_only"))
            ),
        }
        engine = _engine_version(snapshot)
        package = graph_to_evidence_package(
            graph,
            self._executable_rules,
            facts=frozen_facts,
            question=str(question or f"{self.domain_id} natal structure").strip(),
            coverage=coverage,
            chart_facts={
                "palace_id": palace_id,
                "time_layer": "NATAL",
                "observed_fact_count": len(frozen_facts),
            },
            engine_version=engine,
            knowledge_version=self.knowledge_version,
        )
        return NatalDomainEvidence.from_evidence_package(self.domain_id, package)


def load_registry_driven_natal_provider(
    repository_root: str | Path,
    registry_relative_path: str | Path,
) -> RegistryDrivenNatalDomainProvider:
    """Load one Product-owned provider registry plus its read-only source rows."""

    root = Path(repository_root)
    registry_path = Path(registry_relative_path)
    if not registry_path.is_absolute():
        registry_path = root / registry_path
    with registry_path.open("r", encoding="utf-8") as handle:
        registry = json.load(handle)

    source_paths = registry.get("projection_sources")
    if not isinstance(source_paths, list) or not source_paths:
        raise ValueError("domain provider registry requires projection_sources")
    rows: list[dict[str, str]] = []
    seen: set[str] = set()
    for relative_path in source_paths:
        path = Path(str(relative_path))
        if not path.is_absolute():
            path = root / path
        for row in load_projection_rows(path):
            rule_id = str(row.get("projection_rule_id", "")).strip()
            if not rule_id:
                raise ValueError(f"{path}: projection row missing projection_rule_id")
            if rule_id in seen:
                raise ValueError(f"duplicate projection_rule_id across source files: {rule_id}")
            seen.add(rule_id)
            rows.append(row)

    ontology_path = Path(str(registry.get("palace_ontology", "")).strip())
    if not str(ontology_path):
        raise ValueError("domain provider registry requires palace_ontology")
    if not ontology_path.is_absolute():
        ontology_path = root / ontology_path
    ontology = load_palace_ontology(ontology_path)
    return RegistryDrivenNatalDomainProvider(
        projection_rows=rows,
        registry=registry,
        palace_ontology=ontology,
    )
