# Product #906 — Expanded Manifestation Crosswalk P2 Acceptance

## 1. Scope and frozen input

P2 consumes only accepted main commit `4e41074d351a720a639cb702d2ce100c44aa5ca1` from Core #898 / PR #904.

Frozen checkpoint:
- 9 canonical manifestation nodes: `KMN-000001..000009`
- 9 canonical mappings: `KMM-000001..000009`
- next IDs remain `KMN-000010` / `KMM-000010`
- all mappings remain `executable=false`, `product_consumable=false`, and `probability_status=UNKNOWN`

P2 does not consume a later unmerged Core branch and does not change active Product KIB/Knowledge Lock.

## 2. P1 stability result

The P1 field-disposition matrix still covers every field path observed in the expanded 9+9 checkpoint. No new canonical field path is silently ignored.

That does **not** mean the Product interface is ready. The expanded checkpoint adds materially different semantic values and condition structures, so P2 separately audits semantic-value compatibility.

All five Product gaps from P1 remain valid:

- **PG-001 CONFIRMED** — canonical `output_kind` and event-specificity axes are still not represented losslessly.
- **PG-002 CONFIRMED** — provenance, review, identity and supersession metadata are still incompletely retained.
- **PG-003 CONFIRMED_UNCHANGED** — KMM-000002 still needs governed binding from a source-explicit real-world prerequisite into existing `A_t/actions`.
- **PG-004 CONFIRMED_STRONGLY** — all nine mappings carry execution/forbidden-inference boundaries that Product cannot retain as first-class mapping fields.
- **PG-005 CONFIRMED** — source and normalization epistemics still cannot be safely collapsed into one Product `evidence_tier`.

## 3. Expanded semantic structures

The six new pairs test semantic structures that were not present in P1:

- KMM-000004: unresolved 煞曜空劫 trigger quantifier -> **HOLD**
- KMM-000005: abstract state/tendency -> **GAP_PRODUCT**
- KMM-000006: qualitative modifier context -> **GAP_PRODUCT**
- KMM-000007: explicit opposite-palace dependency -> **GAP_PRODUCT**
- KMM-000008: source-explicit OR alternatives -> **GAP_PRODUCT**
- KMM-000009: `DECADE_YEAR` temporal hinge -> **GAP_PRODUCT**

No unresolved source meaning is forced into an executable Product interpretation.

## 4. New Product-owned gaps

### PG-006 — structured condition contract

The current `ManifestationMapping` carries `required_activation_ids` and `required_rule_ids`, while routing checks them by set inclusion. That model is conjunctive and has no first-class representation for:

- source-explicit OR alternatives such as KMM-000008;
- cross-palace dependency structure such as KMM-000007.

This is a Product interface/compiler gap. P2 does not parse free text into hidden executable semantics.

### PG-007 — temporal layer binding

KMM-000009 explicitly carries `conditions.time_layer = DECADE_YEAR`.

Product context correctly keeps natal and temporal rule IDs separate, but `ManifestationMapping` has no time-layer requirement/binding. Product therefore cannot consume this mapping without risking decade/year collapse.

## 5. Safe Core hold

P2 adds **HOLD-CORE-002** for KMM-000004.

The source phrase 煞曜空劫 does not yet provide an accepted Boolean quantifier. Product preserves the unresolved relation and abstains. No Human Gate is required because safe fail-closed behavior is available.

## 6. Entity dispositions

Across 18 entities:

- HOLD: 2 mappings
- LOSSY: 1 node + 1 mapping
- GAP_PRODUCT: 14 entities
- GAP_CORE: 0 forced escalations
- runtime consumption allowed: 0

The absence of a forced GAP_CORE is intentional: unresolved semantics are preserved as HOLD where Product can safely abstain.

## 7. Production boundary

P2 does not authorize production promotion.

The following remain unchanged:

- production manifestation ontology registry stays empty;
- production manifestation mapping registry stays empty;
- active KIB / Product Knowledge Lock stays unchanged;
- runtime execution stays unauthorized;
- probability remains UNKNOWN;
- no predictive-validity claim is made.

P2 verdict:

`EXPANDED_CHECKPOINT_AUDITABLE_PRODUCTION_PROMOTION_BLOCKED`

## 8. P3 readiness / next Product work

Two accepted checkpoints have now been audited, but semantic diversity exposed two additional Product-owned gaps. Therefore formal P3 crosswalk freeze is **not yet justified**.

The next Product-owned work should harden the adapter contract against the confirmed P1/P2 gaps before freezing a production-facing crosswalk. Existing fallback Issue #908 is the appropriate next bounded Product nominee after #906 is accepted.

## 9. Validation

`tests/test_product_manifestation_crosswalk_p2.py` verifies:

- the P2 checkpoint is pinned to accepted Core main;
- all 9 KMN / 9 KMM are covered;
- the P1 field matrix still covers every observed field path;
- KMM-000001 and KMM-000004 remain HOLD;
- KMM-000008 OR semantics are not silently compiled into the conjunctive Product mapping model;
- KMM-000009 `DECADE_YEAR` semantics are not collapsed into an untyped mapping;
- PG-001..PG-005 remain confirmed;
- PG-006 / PG-007 are explicit;
- production registries remain empty;
- all probability/predictive claims remain prohibited.
