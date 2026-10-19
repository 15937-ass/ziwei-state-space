# Registry-Driven Natal Domain Provider Acceptance v0.1

Status: **IMPLEMENTED AS A GENERIC PRODUCT COMPONENT; CAREER NOT YET ACTIVE**

## Purpose

Provide one tested execution path for future NATAL domains without duplicating the Wealth-specific provider implementation. The component is domain-agnostic; this work does not normalize or activate any new Zi Wei rule.

## Runtime contract

The provider consumes:
- a Product-owned registry with `schema_version=0.1`, an explicit domain/palace/topic, a knowledge version, and a non-empty selected rule mapping;
- read-only projection rows from canonical source-review CSVs;
- the shared active palace ontology;
- an explicit structured condition for each selected rule.

Before a rule can execute, the provider checks:
1. its source row exists uniquely;
2. `review_status` is `SOURCE_SPAN_VERIFIED` or `HUMAN_VERIFIED`, and `source_span_verified=true`;
3. `case_support_only` is not true;
4. the source row is NATAL and belongs to the provider's palace;
5. condition text, projection target, and projection mode match the Product registry's expected source values;
6. the condition is explicit and uses only approved condition atoms, including at least one positive atom;
7. Rule IR compiles without issues and antecedent links are valid.

No free-text parsing or condition generation is performed. A mismatch blocks provider construction.

## Output contract

The provider builds facts from the normalized chart and shared palace ontology, runs only its selected rules, and returns a `NatalDomainEvidence` with active rules, source pointers, projections, conflicts, and conservative confidence. Unselected source rows remain pending; they are not implicitly normalized.

## Registry loading and activation

- The production loader accepts only a registry with `status=CANONICAL_READY`.
- The default natal domain registry remains Wealth-only.
- Additional providers must be explicitly constructed and passed to `load_default_natal_domain_registry(..., additional_providers=...)`.
- No Career provider or Career rule mapping is activated by this PR.
- The tests use clearly synthetic `SRC-TEST-ONLY` source rows solely to verify provider plumbing.

## Scope boundary

This is Product-owned runtime code and test coverage only. It does not change Knowledge CSVs, Knowledge state, canonical source text, or any Human Gate decision.

## Acceptance tests

- valid explicit condition activates and traces its source row;
- missing condition does not activate;
- case-support-only, unverified, wrong-layer, wrong-palace, source-drift, unknown-atom, and unconditional-rule cases fail closed;
- registry loader refuses non-canonical-ready status;
- the default registry remains Wealth-only unless an additional provider is explicitly supplied.
