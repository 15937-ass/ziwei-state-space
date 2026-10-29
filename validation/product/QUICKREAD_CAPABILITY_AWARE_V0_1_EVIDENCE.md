# QuickRead v0.1 validation ledger

Issue: [#798](https://github.com/15937-ass/ziwei-state-space/issues/798)  
PR: [#804](https://github.com/15937-ass/ziwei-state-space/pull/804)  
Status: earlier code snapshot `0be470daddb6d388474972462bb1985d689f2843` passed all required checks. The current PR additionally implements PI-approved progressive source retrieval: the 20-item default is a first-pass batch budget, later batches use a main-pinned continuation with seen-evidence identities, and stale-main continuation fails closed. Exact-head validation for the amended PR is recorded in the PR conversation after the final code/doc head is fixed.

## Base and code snapshot

- Base `main` SHA: `d45e2cfd6c0dc59fb80ec2210f7e729c53391c4f`.
- Code snapshot validated: `0be470daddb6d388474972462bb1985d689f2843`.
- Source-of-truth policy: current public `main` only, pinned to one commit per invocation.
- The older stale-base [PR #800](https://github.com/15937-ass/ziwei-state-space/pull/800) is superseded and closed without merge.

## Results on the validated code snapshot

- Repository quality gate: [run 40447635164](https://github.com/15937-ass/ziwei-state-space/actions/runs/40447635164) — **success**.
  - `python -m pytest -q`: 2,821 passed; 132 subtests passed; 355.68 seconds.
  - Product JS adapter syntax: passed.
  - Deterministic P0 repository gate: passed.
  - Repository Governance v1: passed.
- Product P1 regression workflows on the same code snapshot: all passed.
  - [dual engine, run 40447635330](https://github.com/15937-ass/ziwei-state-space/actions/runs/40447635330)
  - [B02B Zi day, run 40447635324](https://github.com/15937-ass/ziwei-state-space/actions/runs/40447635324)
  - [B02C temporal, run 40447635222](https://github.com/15937-ass/ziwei-state-space/actions/runs/40447635222)
  - [B02 calendar, run 40447635181](https://github.com/15937-ass/ziwei-state-space/actions/runs/40447635181)

## What was validated

- The reader resolves current `main`, pins selected files to that SHA, and verifies each fetched Git blob hash.
- Source-first palace ledgers are selected by requested scope; only supported, complete, directly reviewed ledgers and records with explicit safety dispositions are eligible.
- Chinese source-note variants `直接目视核对` / `直接目视检查` and the existing English `Direct visual review` wording are recognized; explicit negation is rejected.
- Held, case-only, uncertain, unreviewed, missing-provenance, and mismatched-time records are excluded.
- The earlier bounded source selection was tested across a ledger. The amended reader now tests first-pass batch accounting, continuation without duplicate evidence, remaining-evidence counts, scope mismatch rejection, and stale-main fail-closed behavior.
- Product provider discovery selects the highest declared version and never silently activates an opt-in provider.
- Runtime capability is distinguished from chart-specific runtime execution and is not asserted for a stale/dirty checkout or mismatched local input files.
- No LLM call, UI, persistence, Knowledge/KIB/registry mutation, or canonical semantic change is introduced.

## Final-head rule

Do not merge unless the GitHub Actions checks attached to the exact resulting head pass after the progressive-retrieval amendment and any final sync with `main`. Record that final head and its matching workflow run IDs in the PR conversation rather than repeatedly changing this ledger after validation.

## Known limitations

- Only the supported `SOURCE_READJUDICATION` palace ledger format is ingested as source evidence in v0.1.
- The executable manifest adapter currently supports the default Wealth provider; other domains require an explicit reviewed adapter.
- No accepted production temporal response/manifestation registry is inferred from source-only or NATAL material.
- The reader returns a compact payload for a caller; invocation from the existing QuickRead Skill/UI and any LLM verbalizer integration remain separate governed work.
- Continuation applies to the same requested scope on the same pinned `main`. Newly introduced scope slots begin a fresh first pass rather than inheriting an unrelated continuation.
- No production-readiness or predictive-validity claim is made.
