"""Canonical PL3-N domain providers.

A domain provider adapts already-executable PL2 knowledge into a feedback-free
NatalDomainEvidence. It must not normalize new traditional rules, use user
history, or add empirical outcome probabilities.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

from .natal_prior import NatalDomainEvidence, NatalStateProfile, build_natal_state_profile
from .palace_structure import PalaceOntology, load_palace_ontology
from .wealth_pilot import (
    build_wealth_evidence_package,
    compose_wealth_registries,
    compile_wealth_pilot,
    load_pilot_registry,
    load_projection_rows,
)


WEALTH_HUMAN_GATE_RULE_IDS = frozenset(
    {
        "W01-016",
        "W01-017",
        "W01-022",
        "W01-023",
        "W01-035",
        "W01-095",
        "W01-096",
        "W01-098",
    }
)

DEFAULT_WEALTH_BATCH_PATHS = (
    "product/PL2C_WEALTH_PILOT_v0.1.json",
    "product/PL2F_WEALTH_NORMALIZATION_BATCH2_v0.1.json",
    "product/PL2H_WEALTH_CROSS_PALACE_BATCH_v0.1.json",
    "product/PL2J_WEALTH_READY_BATCH1_v0.1.json",
    "product/PL2J2_WEALTH_READY_BATCH2_v0.1.json",
    "product/PL2M_WEALTH_ANTECEDENT_EXECUTABLE_BATCH_v0.1.json",
    "product/PL2L_WEALTH_SOURCE_BACKED_BATCH_v0.1.json",
    "product/PL2O2_WEALTH_NORMALIZATION_SAFE_BATCH_v0.1.json",
)
DEFAULT_WEALTH_PROJECTION_PATH = (
    "validation/wp05/W01_wealth_projection_review_001_100.csv"
)
DEFAULT_PALACE_ONTOLOGY_PATH = "knowledge/wp05/palace_ontology_v0.1.csv"


@dataclass
class WealthNatalDomainProvider:
    projection_rows: list[dict[str, str]]
    registry: dict[str, Any]
    palace_ontology: PalaceOntology

    def __post_init__(self) -> None:
        rules = self.registry.get("rules")
        if not isinstance(rules, Mapping):
            raise ValueError("wealth provider registry requires rules")
        if len(rules) != 59:
            raise ValueError(
                f"PL3-N wealth provider expects frozen 59-rule baseline, got {len(rules)}"
            )
        overlap = set(rules).intersection(WEALTH_HUMAN_GATE_RULE_IDS)
        if overlap:
            raise ValueError(
                "Human Gate rows cannot enter wealth natal provider before their "
                "remaining source/runtime blockers close: "
                + ", ".join(sorted(overlap))
            )

        report = compile_wealth_pilot(self.projection_rows, self.registry)
        if report.issues:
            raise ValueError(f"wealth provider contains compile issues: {report.issues!r}")
        if len(report.executable) != 59:
            raise ValueError(
                f"wealth provider compile baseline drift: {len(report.executable)} != 59"
            )

    @property
    def knowledge_version(self) -> str:
        return str(self.registry.get("knowledge_version", "")).strip()

    @property
    def executable_rule_count(self) -> int:
        return len(self.registry["rules"])

    def build_domain_evidence(
        self,
        snapshot: Mapping[str, Any],
        *,
        question: str = "财帛原局结构",
    ) -> NatalDomainEvidence:
        package = build_wealth_evidence_package(
            snapshot,
            self.projection_rows,
            self.registry,
            question=question,
            palace_ontology=self.palace_ontology,
        )
        return NatalDomainEvidence.from_evidence_package("wealth", package)

    def build_profile(
        self,
        snapshot: Mapping[str, Any],
        *,
        question: str = "财帛原局结构",
    ) -> NatalStateProfile:
        domain = self.build_domain_evidence(snapshot, question=question)
        return build_natal_state_profile(
            snapshot,
            self.palace_ontology,
            knowledge_version=self.knowledge_version,
            domain_evidence=(domain,),
        )


def load_default_wealth_natal_provider(
    repository_root: str | Path,
) -> WealthNatalDomainProvider:
    root = Path(repository_root)
    rows = load_projection_rows(root / DEFAULT_WEALTH_PROJECTION_PATH)
    registries = [
        load_pilot_registry(root / relative_path)
        for relative_path in DEFAULT_WEALTH_BATCH_PATHS
    ]
    registry = compose_wealth_registries(*registries)
    ontology = load_palace_ontology(root / DEFAULT_PALACE_ONTOLOGY_PATH)
    return WealthNatalDomainProvider(
        projection_rows=rows,
        registry=registry,
        palace_ontology=ontology,
    )
