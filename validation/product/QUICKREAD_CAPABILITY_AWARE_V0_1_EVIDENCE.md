# QuickRead v0.1 validation ledger

Issue: [#798](https://github.com/15937-ass/ziwei-state-space/issues/798)  
PR: [#800](https://github.com/15937-ass/ziwei-state-space/pull/800)  
Base / main SHA observed: `bacc582403efa5ac573d4a63009b032c61e64e65)

## Implementation-head validation

- Exact implementation head tested: `2f6ca1fc0aa49834d67f99f00003cefb8fd49653`.
- Runtime: GitHub Actions standard public Ubuntu runner; Python 3.12.15; pytest 9.1.1.
- Repository quality gate: **PASS** — [run #40439451016](https://github.com/15937-ass/ziwei-state-space/actions/runs/40439451016).
  - `python -m pytest -q`: **2,799 passed**, **132 subtests passed**, 353.90 seconds.
  - Product JS adapter syntax check: **PASS** (`node --check tools/iztro_export.mjs`, when the adapter file is present).
  - Deterministic P0 repository audit: **PASS** (`python src/audit_repository.py --fail-on-p0`). Reported P1 review candidates are informational and are not P0 failures.
  - Repository Governance v1: **PASS** (`python tools/validate_governance.py --base-ref origin/main --head-branch product/798-quickread-capability-aware-hybrid-v0-1`).
- Applicable Product P1 regression workflows: **4/4 PASS** on the same implementation head:
  - Dual engine: [run #40439450917](https://github.com/15937-ass/ziwei-state-space/actions/runs/40439450917).
  - B02 calendar: [run #40439450989](https://github.com/15937-ass/ziwei-state-space/actions/runs/40439450989).
  - B02B Zi-day: [run #40439450876](https://github.com/15937-ass/ziwei-state-space/actions/runs/40439450876).
  - B02C temporal: [run #40439451000](https://github.com/15937-ass/ziwei-state-space/actions/runs/40439451000).

## Scope and limitations

- The fixture is synthetic and does not represent actual production capability coverage.
- The module is a deterministic adapter contract: it does not calculate charts, call an LLM/API, scan GitHub, persist data, or promote model text into canonical knowledge.
- The manifest is an explicit, version-pinned caller input. Live accepted-main manifest construction is a separate future integration.
- No canonical semantics, Knowledge artifacts, Product KIB/locks, registries, production runtime behavior, probabilities, or predictive-validity claims are changed.

## Final-head freshness

This ledger update is a documentation-only commit after the implementation-head validation above. Per repository policy, those earlier runs are not represented as validation of the new ledger commit. Re-run the required exact-head checks on the resulting PR head, then record that final head and its run IDs in the PR #800 conversation. Do not merge automatically.
