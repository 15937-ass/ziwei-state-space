"""Generic PL3-N domain-provider registry.

The registry composes already-approved natal domain providers. It does not
compile new traditional rules or use temporal/personal feedback.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Mapping, Protocol, runtime_checkable

from .natal_prior import NatalDomainEvidence, NatalStateProfile, build_natal_state_profile
from .palace_structure import PalaceOntology
from .natal_domain_providers import (
    WealthNatalDomainProvider,
    load_default_wealth_natal_provider,
)


@runtime_checkable
class NatalDomainProvider(Protocol):
    @property
    def domain_id(self) -> str: ...

    @property
    def knowledge_version(self) -> str: ...

    @property
    def palace_ontology(self) -> PalaceOntology: ...

    def build_domain_evidence(
        self,
        snapshot: Mapping[str, Any],
        *,
        question: str = "",
    ) -> NatalDomainEvidence: ...


@dataclass(frozen=True)
class NatalDomainProviderRegistry:
    providers: tuple[NatalDomainProvider, ...]

    def __post_init__(self) -> None:
        if not self.providers:
            raise ValueError("NatalDomainProviderRegistry requires at least one provider")

        ids = [provider.domain_id for provider in self.providers]
        if any(not domain_id.strip() for domain_id in ids):
            raise ValueError("domain provider id must be non-empty")
        if len(set(ids)) != len(ids):
            raise ValueError("duplicate natal domain provider id")

        reference = self.providers[0].palace_ontology.entries
        for provider in self.providers[1:]:
            if provider.palace_ontology.entries != reference:
                raise ValueError("all natal domain providers must share one palace ontology")

    @property
    def domain_ids(self) -> tuple[str, ...]:
        return tuple(sorted(provider.domain_id for provider in self.providers))

    @property
    def knowledge_version(self) -> str:
        parts = [
            f"{provider.domain_id}={provider.knowledge_version}"
            for provider in sorted(self.providers, key=lambda item: item.domain_id)
        ]
        return "PL3N[" + ";".join(parts) + "]"

    @property
    def palace_ontology(self) -> PalaceOntology:
        return self.providers[0].palace_ontology

    def _provider_index(self) -> dict[str, NatalDomainProvider]:
        return {provider.domain_id: provider for provider in self.providers}

    def build_domain_evidence(
        self,
        snapshot: Mapping[str, Any],
        *,
        selected_domains: Iterable[str] | None = None,
        questions: Mapping[str, str] | None = None,
    ) -> tuple[NatalDomainEvidence, ...]:
        provider_by_id = self._provider_index()
        if selected_domains is None:
            domain_ids = self.domain_ids
        else:
            domain_ids = tuple(sorted({str(item).strip() for item in selected_domains}))
            if not all(domain_ids):
                raise ValueError("selected domain ids must be non-empty")

        unknown = sorted(set(domain_ids) - set(provider_by_id))
        if unknown:
            raise ValueError(
                "unknown natal domain provider(s): " + ", ".join(unknown)
            )

        question_map = dict(questions or {})
        evidence = []
        for domain_id in domain_ids:
            provider = provider_by_id[domain_id]
            question = str(question_map.get(domain_id, "")).strip()
            if question:
                item = provider.build_domain_evidence(snapshot, question=question)
            else:
                item = provider.build_domain_evidence(snapshot)
            if item.domain_id != domain_id:
                raise ValueError(
                    f"provider {domain_id} returned mismatched domain {item.domain_id}"
                )
            evidence.append(item)
        return tuple(evidence)

    def build_profile(
        self,
        snapshot: Mapping[str, Any],
        *,
        selected_domains: Iterable[str] | None = None,
        questions: Mapping[str, str] | None = None,
    ) -> NatalStateProfile:
        domains = self.build_domain_evidence(
            snapshot,
            selected_domains=selected_domains,
            questions=questions,
        )
        selected_versions = [
            f"{item.domain_id}={item.knowledge_version}"
            for item in sorted(domains, key=lambda value: value.domain_id)
        ]
        knowledge_version = "PL3N[" + ";".join(selected_versions) + "]"
        return build_natal_state_profile(
            snapshot,
            self.palace_ontology,
            knowledge_version=knowledge_version,
            domain_evidence=domains,
        )


class _WealthProviderAdapter:
    """Expose the existing wealth provider through the generic protocol."""

    def __init__(self, provider: WealthNatalDomainProvider):
        self._provider = provider

    @property
    def domain_id(self) -> str:
        return "wealth"

    @property
    def knowledge_version(self) -> str:
        return self._provider.knowledge_version

    @property
    def palace_ontology(self) -> PalaceOntology:
        return self._provider.palace_ontology

    def build_domain_evidence(
        self,
        snapshot: Mapping[str, Any],
        *,
        question: str = "财帛原局结构",
    ) -> NatalDomainEvidence:
        return self._provider.build_domain_evidence(snapshot, question=question)


def load_default_natal_domain_registry(
    repository_root: str | Path,
) -> NatalDomainProviderRegistry:
    wealth = load_default_wealth_natal_provider(repository_root)
    return NatalDomainProviderRegistry(providers=(_WealthProviderAdapter(wealth),))
