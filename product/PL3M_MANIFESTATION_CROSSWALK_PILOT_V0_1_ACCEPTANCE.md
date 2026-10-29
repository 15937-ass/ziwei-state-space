# Product #897 — Manifestation Knowledge→Product Crosswalk Pilot v0.1

Status: **P1 RESULT READY FOR INTEGRATION — production promotion remains blocked**

## 1. Scope

This bounded pilot consumes only the first accepted canonical Knowledge checkpoint on main commit:

`df66959b126e44eb309507fc5400b82e3af58187`

Inputs are pinned in `PL3M_MANIFESTATION_CROSSWALK_PILOT_V0_1.json`, including exact Git blob SHAs for:

- KMN-000001..000003;
- KMM-000001..000003;
- the canonical node/mapping indexes;
- the current PL3-M ontology/mapping adapters and routing-context interface.

This work does **not** populate production manifestation registries, promote KIB/K_manifest, authorize runtime execution, add probability, or claim predictive validity.

## 2. Main finding

The first canonical checkpoint is **auditable but not losslessly promotable through the current Product v0.1 contracts**.

The blocker is no longer simply “Knowledge is missing.” The accepted Knowledge artifacts now contain distinctions that the older Product adapter does not represent as first-class fields, especially:

- `output_kind`;
- full `event_specificity {state,value}`;
- separate `source_epistemic` and `normalization_epistemic`;
- review / identity / supersession provenance;
- unresolved semantics;
- execution readiness and blockers;
- forbidden inferences / negative boundaries;
- real-world action prerequisites.

Therefore the correct P1 result is:

**PILOT_FEASIBLE_PRODUCTION_PROMOTION_BLOCKED**

The Product layer should refine its crosswalk/interface contract rather than asking Core to flatten or rewrite canonical semantics.

## 3. Mandatory case verdicts

### KMM-000001 — 火铃 shorthand

Verdict: **HOLD**

Knowledge explicitly preserves BOTH_STARS vs EITHER_STAR as unresolved. Product must not select either interpretation. This is a safe semantic hold, not a reason to coerce the mapping into the current router.

### KMM-000002 — 勉强求变

Verdict: **GAP_PRODUCT**

Important detail: Product already has a legitimate real-world action layer.

`ManifestationRoutingContext.actions` carries A_t, backed by acquired-state/observation provenance.

The actual missing link is narrower:

> current `ManifestationMapping` / possibility router has no governed action-prerequisite predicate binding.

Therefore `勉强求变` must not be inferred from chart facts, but this does **not** require rewriting Core. Product owns the interface gap.

### KMM-000003 — career/industry scene

Verdict: **LOSSY, research-only**

A coarse Product `SCENE_LEVEL` representation is possible. However the canonical meaning also preserves:

- `SCENE_NOT_OBSERVED_EVENT`;
- `normalization_epistemic = INFERRED`;
- explicit negative boundary against person-level injury, illness, accident, diagnosis, treatment, or medical event.

The current production mapping contract cannot retain all of those boundaries as first-class fields. Therefore the pilot may document a lossy scene crosswalk, but runtime/promotion remains blocked.

## 4. Field-level result

Every field actually present in KMN-000001..000003 and KMM-000001..000003 receives exactly one disposition in the versioned matrix:

- `DIRECT`
- `LOSSY`
- `GAP_PRODUCT`
- `GAP_CORE`
- `HOLD`

No UNKNOWN/conflict is converted into a Product value.

The deterministic pilot validator checks that no observed canonical field is left unclassified.

## 5. Product-owned gaps

The P1 gap register identifies five concrete Product gaps:

1. **PG-001** — canonical `output_kind` and full event-specificity axes are missing from Product ontology.
2. **PG-002** — canonical review/normalization/identity/supersession provenance is not fully retained.
3. **PG-003** — A_t exists, but manifestation mapping cannot bind real-world action prerequisites.
4. **PG-004** — execution readiness, blockers, forbidden inferences and negative boundaries are not first-class mapping fields.
5. **PG-005** — no governed translation exists from separate source + normalization epistemics into the current single `evidence_tier`.

These are Product interface problems. They must not be “fixed” by weakening canonical Knowledge.

## 6. Safe Core hold

KMM-000001 contains a genuine unresolved shared semantic point, but Product can safely abstain.

The pilot records this as:

`HOLD-CORE-001`

It is **not** automatically escalated into a demand that Core choose a meaning. A later Core decision may resolve it, but P1 remains correct while preserving HOLD.

## 7. Production state remains unchanged

The following must remain true after P1:

- `PL3M_MANIFESTATION_ONTOLOGY_REGISTRY_v0.1.json` stays empty;
- `PL3M_MANIFESTATION_MAPPING_REGISTRY_v0.1.json` stays empty;
- active Product Knowledge Lock/KIB is unchanged;
- `runtime_execution_allowed = false`;
- `probability_status = UNKNOWN`;
- no predictive-validity claim.

## 8. P2 handoff

P2 starts only after Core accepts a materially larger canonical checkpoint.

P2 must pin that accepted checkpoint and re-run:

- field coverage;
- node/mapping verdict stability;
- PG-001..PG-005;
- HOLD behavior;
- newly introduced semantic structures.

Knowledge advancement never auto-refreshes Product.

## 9. Validation

Added deterministic coverage in:

`tests/test_product_manifestation_crosswalk_pilot.py`

It verifies:

- all observed canonical fields are classified;
- mandatory KMM/KMN verdicts are deterministic;
- KMM-000001 stays HOLD;
- KMM-000002 is a Product action-binding gap while A_t already exists;
- KMM-000003 retains the person-injury/illness negative boundary as explicit loss;
- production registries remain empty;
- probability/predictive claims remain prohibited.

Build validation run #40851314906 passed repository pytest, Product JS adapter checks, deterministic P0, and Governance validation. Final merge authorization still requires the #888 Integration Lease and a fresh exact-head final gate.
