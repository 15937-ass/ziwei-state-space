# Career Decade/Year Response Compiler v0.1

Status: IMPLEMENTED CANDIDATE — Product #534

## What this adds

This work introduces the first explicit Product `ResponseProfile τ_t` object for the v0.4 dynamic path:

```text
NATAL condition evaluation
+ TemporalEnvironmentProfile E_t
+ source-normalized DECADE/YEAR reactions
-> sparse symbolic CareerResponseProfile τ_t
```

The compiler does **not** infer a reaction from raw decade/year chart facts. A temporal reaction can affect a natal Career basis only when `TemporalReactionEvidence.matched_natal_rule_ids` explicitly links it to a NATAL condition that was actually matched by the bounded Career evaluator.

## Production boundary

The current production temporal reaction registry is still intentionally empty. Therefore the production path is expected to return:

```text
status = PARTIAL_UNKNOWN
entries = 0
unknowns include:
  PRODUCTION_TEMPORAL_RESPONSE_NOT_AVAILABLE
  NO_SOURCE_BACKED_DECADE_YEAR_RESPONSE
```

This is not negative evidence and does not mean "nothing happens". It means the Product does not yet possess source-normalized canonical decade/year response content that it is allowed to execute.

## Allowed symbolic effects

The compiler only preserves the already governed PL3-T vocabulary:

- ACTIVATE
- STRENGTHEN
- WEAKEN
- TRANSFORM
- ROUTE
- PRESERVE

No numeric strength is created. `SOURCE_ORDINAL_ONLY` is transported as source-level ordinal metadata only.

## Lineage and source trace

Each response entry keeps both sides of the evidence chain:

- matched NATAL Career rule ID and condition ID;
- source-reviewed NATAL projection descriptor and source spans;
- temporal reaction ID/rule ID;
- DECADE or YEAR layer;
- temporal source ID/location/review status;
- matched natal/temporal fact references.

The response profile also binds to:

- `NatalStateProfile.profile_id`;
- `TemporalEnvironmentProfile.profile_id`;
- one identical `knowledge_version`.

Any mismatch fails closed.

## What is still not complete

This milestone means the **ResponseProfile runtime contract and deterministic compiler exist**. It does not mean canonical dynamic Career response content is ready.

Still false:

- production decade/year reaction content ready;
- M0 manifestation ready;
- empirical probability ready;
- predictive validity validated.

The next Product work should therefore build M0 only from real source-backed τ entries and preserve an empty/unknown result when τ has no canonical dynamic entries.
