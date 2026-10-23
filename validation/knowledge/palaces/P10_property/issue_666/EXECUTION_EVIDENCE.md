# P10 recovery-state synchronization — Issue #666

- Date: 2026-10-23
- Lane/shard: `KNOWLEDGE_ONLY / P10 / 田宅宫`
- Work unit: `KB-P10-STATE-SYNC-AFTER-COMPOUND-MAP-01`

## Source checkpoints

- Product snapshot-contract fix: PR #660, merge commit `6523a0a07051ebe8416dd6d074bf4c6e157aa217`.
- P10 same-palace compound-star mapping: PR #661, merge commit `ec61c8872ec1e407bf8372e2f2ef67bd225c3661`.
- State-sync branch base/snapshot checkpoint: `6523a0a07051ebe8416dd6d074bf4c6e157aa217`.
- Mapping artifact: `knowledge/palaces/P10_property/wp07a/PROPERTY_SAME_PALACE_COMPOUND_STAR_MAP_01_v0.1.json`.
- Mapping audit ID: `KB-WP07A-PROPERTY-SAME-PALACE-COMPOUND-STAR-MAP-01`.
- Mapping status: `MAPPING_COMPLETE_13_OF_13_NOT_PRODUCTION`.

## Exact mapped source IDs

`TP01-071`, `TP01-072`, `TP01-097`, `TP02-121`, `TP02-126`, `TP02-160`, `TP02-186`, `TP03-226`, `TP03-227`, `TP04-306`, `TP04-310`, `TP04-311`, `TP04-340`.

## Preserved boundaries

- Every mapping remains a static, non-executable candidate; every `executable_registry_entry` is `false`.
- Conditions use only existing `PALACE_HAS_STAR` facts bound to P10.
- TP02-121 retains explicit 火贪 / 铃贪 alternatives; TP04-340 retains explicit 廉贞七杀 / 武曲七杀 alternatives.
- TP02-126 retains the unresolved 天府得禄 / 府库空露 dependency. No treasury state is inferred from palace geometry or missing transformation facts.
- No canonical source row, shared Core semantic, Product runtime, production registry, atom, probability, numeric weight, threshold, or time primitive is changed.
- `knowledge/states/P10_PROPERTY_STATE.yaml` is a mutable recovery cache and is excluded from the Product handoff's immutable `source_artifacts`; immutable source artifacts remain pinned by exact Git blob SHA.
- The completed recovery cache preserves `ACTIVE_NO_ACTIVE_WORK` and null active issue/branch/PR pointers.

## Exact-head validation history

- Repository quality gate run #2273 on head `5387084aad0f310fc90d38147598395c8a40e664`: **FAIL**. Full pytest reported 2,526 passed and 1 failed in 353.93 seconds. The failure was an overstrict test expectation requiring every mapping to use `MAPPED_EXISTING_ATOMS`.
- The canonical mapping correctly assigns TP02-126 `MAPPED_GEOMETRY_WITH_EXPLICIT_UNRESOLVED_STATE_DEPENDENCY`; the regression was corrected to require that status for TP02-126 and `MAPPED_EXISTING_ATOMS` for the other twelve rows. No source mapping or Product runtime was changed.
- Repository quality gate run #2275 on head `ee2053045ff336452d8b66ccddd79954ab81bd91`: **PASS** — https://github.com/15937-ass/ziwei-state-space/actions/runs/39879627186. Full pytest: **2,527 passed** in 340.15 seconds; Product JS adapter check, deterministic P0 audit, and Repository Governance v1 / Knowledge write-boundary validation all passed.
- Repository quality gate run #2276 on head `cdc019c44d3c40e4190eb3548c496fb5253bf6ce`: **PASS** — https://github.com/15937-ass/ziwei-state-space/actions/runs/39880417539. Full pytest: **2,527 passed** in 286.37 seconds; Product JS adapter check, deterministic P0 audit, and Repository Governance v1 / Knowledge write-boundary validation all passed.
- This evidence consolidation is documentation-only. The final PR-head gate must also pass before merge; its authoritative outcome is recorded in the PR's GitHub Actions checks and final description.
