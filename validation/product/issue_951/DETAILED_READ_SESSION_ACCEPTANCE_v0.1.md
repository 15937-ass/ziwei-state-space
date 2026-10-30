# Product #951 — DetailedRead session acceptance fixture v0.1

**Status:** SYNTHETIC_SESSION_CONTRACT_FIXTURE  
**Purpose:** Reproducible orchestration-contract validation only.

This fixture exercises the 12-domain NATAL session, one-main-SHA pin, QuickRead-to-DetailedRead same-chart continuation, per-slot continuation, UNKNOWN preservation, model-supplement separation, case-only exclusion accounting, staged delivery metadata and negative controls.

## Fixture identity

- Synthetic target: `DETAILEDREAD-TEST-CHART-001`
- Current accepted main at checkpoint: `33e738e834a198217e26d3d645826283315b4b73`
- Product branch initial base: `09b6c3521d6772012847088d3209d0cabe0548c6`
- Synthetic reader test SHA: `aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa` (test constant only; not a repository commit)

## Expected contract

- All twelve NATAL domains appear in the coverage denominator.
- After all planned NATAL stages, the fixture reports 12/12 inspected and `NATAL_INSPECTION_COMPLETE`.
- Runtime, accepted source and model supplementation remain separate.
- The synthetic model supplement does not increase runtime or source coverage.
- Case-only exclusions are reported separately and never enter accepted runtime/source evidence.
- UNKNOWN runtime/source statuses remain UNKNOWN.
- Cross-domain checks, thematic sections and staged delivery metadata are preserved.
- A main change, chart-target mismatch, invalid continuation, or model supplement for an uninspected slot fails closed.

## Scope limitation

This fixture uses a synthetic loader. It is **not** an actual user chart reading and does not claim that live accepted source/runtime evidence was loaded. It makes no chart calculation, runtime execution, LLM call, KIB promotion, registry mutation or predictive-validity claim. Real reading reports must record the exact accepted main SHA and per-domain evidence provenance returned by the production QuickRead reader.
