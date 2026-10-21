# Career Canonical Manifestation Candidates M0 v0.1

Status: IMPLEMENTED CANDIDATE — Product #539

## Position in Product v0.4

```text
NATAL N
  -> Temporal Environment E_t
  -> ResponseProfile τ_t
  -> Canonical Manifestation Candidates M0
```

M0 is deliberately **not** a prediction distribution. It is the set of manifestation possibilities for which the current symbolic response state has an explicit, source-reviewed ontology/mapping path.

## Input discipline

The M0 adapter consumes only rule IDs carried by actual `CareerResponseProfile.entries`:

- `natal_rule_id`;
- `temporal_rule_id`.

It does not read projection prose to guess an event. It does not expose every active natal rule. It does not turn `ACTIVATE`, `STRENGTHEN`, etc. into invented activation ontology IDs.

Therefore:

```text
not present in tau
=> cannot independently trigger M0
```

## Existing router reused

The existing manifestation router remains the semantic authority for routing:

- ontology readiness;
- mapping readiness;
- exact antecedent set match;
- evidence tiers;
- source refs;
- probability_status=UNKNOWN.

Only `EXPLICIT` and `TRANSPARENT_INFERENCE` mappings may become `SOURCE_SUPPORTED_POSSIBILITY`. `CASE_SUPPORT_ONLY` and `HYPOTHESIS` remain held.

## Provenance chain

Each M0 candidate now carries:

```text
tau response support
  -> natal rule + natal source span
  -> temporal reaction rule + temporal source
  -> manifestation mapping source
  -> manifestation ontology source
```

This is the first complete runtime contract path from N/E/τ into M0 without introducing a probability.

## Production status

The contract path is implemented, but canonical dynamic content is still intentionally unavailable:

- production temporal reaction registry: empty;
- production manifestation ontology: pending KB-WP06B;
- production manifestation mapping: pending KB-WP06C.

So current production execution must return zero M0 candidates with explicit blockers. That is an **unknown/readiness state**, not evidence that no event will happen.

## Next boundary

The first N -> E -> τ -> M0 source-only vertical slice now has runtime contracts. The next Product priority can move to fidelity/replay and Forecast Ledger activation prerequisites, while Knowledge continues supplying canonical temporal/manifestation content independently.
