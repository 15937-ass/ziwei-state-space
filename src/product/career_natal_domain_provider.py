"""Canonical Career natal provider entry point.

The provider is opt-in so the existing default registry remains backward
compatible and Wealth-only.
"""

from __future__ import annotations

from pathlib import Path

from .registry_driven_natal_provider import (
    RegistryDrivenNatalDomainProvider,
    load_registry_driven_natal_provider,
)


DEFAULT_CAREER_PROVIDER_REGISTRY_PATH = (
    "product/PL3N_CAREER_DOMAIN_PROVIDER_v0.1.json"
)


def load_default_career_natal_provider(
    repository_root: str | Path,
) -> RegistryDrivenNatalDomainProvider:
    """Load the source-pinned three-rule Career NATAL provider."""

    return load_registry_driven_natal_provider(
        repository_root,
        DEFAULT_CAREER_PROVIDER_REGISTRY_PATH,
    )
