# PL7-Q3 Raw-Text Observation Candidate Gate v0.1

Status: implementation proposal on the Product branch; acceptance depends on exact-head validation and review.
Tracking Issue: #714
Lane: PRODUCT_ONLY
Base main: bdcbf24ef85959d7a7b35014e82708bbedb329bf

## Purpose

Provide a bounded intake gate for candidate fields proposed by an upstream language model from user-reported narrative. This module does not call a model. It verifies an exact evidence span transiently, validates candidate fields against a locked prospective check-in plan, and requires a separate user-confirmation action before calling the existing deterministic check-in bridge.

The gate is a data-intake capability only. It does not make the canonical source-only N -> E -> tau -> M0 slice executable and does not activate Forecast Ledger.

## Data flow

1. An upstream caller supplies raw text and a structured candidate payload.
2. The gate validates the payload and checks that its evidence quote exactly matches the supplied source text at the supplied offsets.
3. The returned candidate includes only offsets, normalized event-time bounds, and validated fields. It omits the narrative and quote.
4. The caller obtains explicit user confirmation separately.
5. After confirmation, the gate delegates to bridge_checkin_response_v02; that bridge remains authoritative for locked target/window semantics and observation creation.

## Safety and epistemic boundaries

- Candidate/model output is not ground truth.
- A model-supplied user_confirmed field is ignored.
- The raw text is used only in-memory for exact span verification; this module does not persist, log, or return it.
- Observation confidence is supplied separately at confirmation time and must use the existing confidence vocabulary. Model self-confidence is ignored.
- NO, UNSURE, NO_RESPONSE, missing event-time detail, and temporal ambiguity retain the existing bridge semantics. A mid-window NO is not a closed-window negative; missing or absent candidate evidence is not a negative event.
- No raw narrative is committed in fixtures or validation artifacts.
- No database, network, UI, telemetry, external model invocation, or long-term retention is implemented. The PL7-Q5 privacy/consent/deletion boundary remains a prerequisite for real productization.
- No canonical Zi Wei rule, Knowledge artifact, KIB lock, temporal-reaction registry, manifestation registry, probability, or Forecast Ledger state is changed.

## Acceptance checklist

- [ ] Candidate schema, plan identity, target, checkpoint, answer, response date, event-time shape, and exact evidence span are validated deterministically.
- [ ] Candidate remains pending even if upstream output claims it is already user-confirmed.
- [ ] Only a separate confirmation argument can proceed to the existing v0.2 bridge.
- [ ] Bridge outputs preserve event-time precision and reject partial-window ambiguity and premature window-close negatives.
- [ ] Returned candidate artifacts contain no raw narrative or quoted evidence text.
- [ ] Synthetic tests cover malformed candidates, missing evidence, missing event time, uncertainty/no response, and temporal edge cases.
- [ ] Full repository quality gate and applicable Product regressions pass on the exact PR head.
- [ ] Product state and handoff preserve the separate blocker on the source-only N -> E -> tau -> M0 slice.

## Limitations

This contract does not assess whether a language model correctly understood a narrative. It only validates candidate structure, exact span grounding, user-confirmation sequencing, and deterministic conversion. Human confirmation and the existing bridge are required; this is not an automated fact extractor or predictive-validity result.
