# P10 Recovery State Sync — Execution Evidence

- Issue: #666
- Work unit: `KB-P10-STATE-SYNC-AFTER-COMPOUND-MAP-01`
- Lane / shard: `KNOWLEDGE_ONLY / P10`
- Snapshot contract prerequisite: Product PR #660, merge commit `6523a0a07051ebe8416dd6d074bf4c6e157aa217`
- Accepted same-palace mapping: PR #661, merge commit `ec61c8872ec1e407bf8372e2f2ef67bd225c3661`
- Accepted relation/cross-palace mapping: PR #616, merge commit `83db2c351e09cff686527530823e44fda6ec1808`
- Canonical source baseline: `PROPERTY_P10_CANONICAL_358_OF_358`
- Same-palace map: `knowledge/palaces/P10_property/wp07a/PROPERTY_SAME_PALACE_COMPOUND_STAR_MAP_01_v0.1.json`
- Recovery cache: `knowledge/states/P10_PROPERTY_STATE.yaml`
- Regression: `tests/test_knowledge_p10_state_recovery.py`

## Accepted same-palace rule IDs

`TP01-071`, `TP01-072`, `TP01-097`, `TP02-121`, `TP02-126`, `TP02-160`, `TP02-186`, `TP03-226`, `TP03-227`, `TP04-306`, `TP04-310`, `TP04-311`, `TP04-340`.

## Validation contract

The recovery regression reconciles the state checkpoint against the exact 13-row mapping artifact and preserves source-span verification, `NATAL` scope, non-`CASE_SUPPORT_ONLY` provenance, P10-local `PALACE_HAS_STAR` facts, explicit 火贪/铃贪 and 廉贞七杀/武曲七杀 alternatives, and the unresolved Tianfu treasury-state dependency.

Every row must retain `executable_registry_entry: false` and a static/non-executable readiness value. No new runtime atom, production registry entry, numeric weight, probability, threshold, canonical source edit, shared Core semantic, other-palace write, or Product runtime authorization is permitted.

## Exact-head validation record

Do not reuse the prior green run for PR #661 as evidence for this recovery-cache update. The authoritative full repository quality-gate, full pytest, deterministic P0 audit, and Knowledge/G12 governance result must be taken from the exact final head of the PR closing Issue #666. The issue closeout records that final commit and its workflow results.
