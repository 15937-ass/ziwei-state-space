# Core shared-schema path ownership — execution evidence

- Issue: #753
- Work unit: `GOV_CORE_SHARED_SCHEMA_PATH_OWNERSHIP_ALIGNMENT_01`
- Branch: `governance/753-core-schema-path-ownership`
- Activation base/main SHA: `3611e5e73654ca3015910314edf92fc0ca612a8b`
- Status: authorization-only governance correction; schema contents are untouched.

## Exact paths proposed for Core

Add these two exact paths to `governance/KNOWLEDGE_SHARDS.json` under `core.allowed_paths`:
- `knowledge/KB_SCHEMA.md`
- `knowledge/REVIEW_SCHEMA_v0.3.md`

No wildcard or broad root permission is added. Palace shards continue to reject both paths. Core continues to reject unrelated root-level Knowledge files.

## Changed-path boundary
- `governance/KNOWLEDGE_SHARDS.json`
- `governance/GOVERNANCE_STATE.yaml` (execution recovery cache)
- `tests/test_governance_knowledge_shards.py`
- `governance/evidence/core-shared-schema-path-ownership/EVIDENCE.md`

No schema content, ontology, canonical mapping, source row, Product/runtime, registry/lock, or consumer permission is changed.

## Exact-head validation
The full repository-quality-gate result and exact tested head will be recorded in the PR validation comment after the exact-head checks complete. This evidence file records the intended scope and must not be edited after the final gate, because that would create a new unvalidated head.
