# P10 recovery-state synchronization — Issue #666

- Date: 2026-10-23
- Lane/shard: `KNOWLEDGE_ONLY / P10 / 田宅宫`
- Work unit: `KB-P10-STATE-SYNC-AFTER-COMPOUND-MAP-01`

## Source checkpoints

- Product snapshot-contract fix: PR #660, merge commit `6523a0a07051ebe8416dd6d074bf4c6e157aa217`.
- P10 same-palace compound-star mapping: PR #661, merge commit `ec61c8872ec1e407bf8372e2f2ef67bd225c3661`.
- State-sync branch base / snapshot checkpoint: `6523a0a07051ebe8416dd6d074bf4c6e157aa217`.
- Mapping artifact: `knowledge/palaces/P10_property/wp07a/PROPERTY_SAME_PALACE_COMPOUND_STAR_MAP_01_v0.1.json`.
- Mapping audit ID: `KB-WP07A-PROPERTY-SAME-PALACE-COMPOUND-STAR-MAP-01`.
- Mapping status: `MAPPING_COMPLETE_13_OF_13_NOT_PRODUCTION`.

## Exact mapped source IDs

`TP01-071`, `TP01-072`, `TP01-097`, `TP02-121`, `TP02-126`, `TP02-160`, `TP02-186`, `TP03-226`, `TP03-227`, `TP04-306`, `TP04-310`, `TP04-311`, `TP04-340`.

## Preserved boundaries

- Every mapping remains a static, non-executable candidate; every `executable_registry_entry` is `false`.
- Conditions use only existing `PALACE_HAS_STAR` facts bound to P10.
- TP02-121 retains its explicit 火贪 / 铃贪 alternatives; TP04-340 retains its explicit 廉贞七杀 / 武曲七杀 alternatives.
- TP02-126 retains the unresolved 天府得禄 / 府库空露 dependency. No treasury state is inferred from palace geometry or missing transformation facts.
- No canonical source row, shared Core semantic, Product runtime, production registry, atom, probability, numeric weight, threshold, or time primitive is changed.
- `knowledge/states/P10_PROPERTY_STATE.yaml` is a mutable recovery cache and is not included among the Product handoff's immutable `source_artifacts`. Immutable source-artifact blob-SHA checks remain strict.
- The recovery cache preserves `ACTIVE_NO_ACTIVE_WORK` and null active issue/branch/PR pointers after the bounded issue is complete.

## Validation plan

The exact-head PR gate must verify:
1. `PYTHONPATH="$PWD" python -m pytest -q tests/test_knowledge_p10_state_recovery.py`
2. `PYTHONPATH="$PWD" python -m pytest -q`
3. `PYTHONPATH="$PWD" python src/audit_repository.py --fail-on-p0 --output /tmp/issue-666-audit.json`
4. `python tools/validate_governance.py --base-ref origin/main --head-branch knowledge/p10-666-state-sync-after-compound-map`
5. `git diff --check origin/main` and the repository's scope/diff guard.
6. Confirm Product handoff tests continue to exclude all mutable recovery caches from immutable `source_artifacts`.

Record the resulting GitHub Actions run IDs and outcomes here after the first exact-head run. Any subsequent evidence update must be followed by another exact-head gate; the final PR head must pass.


## First exact-head validation result

- Repository quality-gate run: [#39878761619](https://github.com/15937-ass/ziwei-state-space/actions/runs/39878761619) on head `5387084aad0f310fc90d38147598395c8a40e664` — **FAIL**, so it is not accepted as merge evidence.
- Full pytest: **2,526 passed, 1 failed** in 353.93 seconds.
- The only failure was an overly strict test expectation for TP02-126. The source mapping correctly uses `MAPPED_GEOMETRY_WITH_EXPLICIT_UNRESOLVED_STATE_DEPENDENCY`, preserving the unresolved Tianfu treasury-state dependency; the test had incorrectly required `MAPPED_EXISTING_ATOMS` for every row.
- The regression now requires that explicit unresolved status for TP02-126 and `MAPPED_EXISTING_ATOMS` for the other twelve rows. No canonical mapping/source data or Product runtime was changed.
- The updated head must pass a fresh full repository quality gate, including pytest, Product JS adapter checks, deterministic P0 audit, and Repository Governance v1, before merge.

## Exact-head validation results

- Repository quality gate run #2275: **PASS** — https://github.com/15937-ass/ziwei-state-space/actions/runs/39879627186
- Validated PR head: `ee2053045ff336452d8b66ccddd79954ab81bd91`; base main checkpoint: `6523a0a07051ebe8416dd6d074bf4c6e157aa217`.
- Full pytest: **2,527 passed** in 340.15 seconds.
- Product JS adapter syntax check: **PASS**.
- Deterministic P0 repository audit: **PASS**.
- Repository Governance v1 / Knowledge shard write-isolation validation: **PASS**.
- The prior run #2273 failure was limited to an overstrict test expectation for TP02-126; the test now asserts its explicit unresolved-state mapping status while preserving the non-executable boundary.
- This record update requires a fresh exact-head gate before merge; the final PR head must pass with this evidence included.
