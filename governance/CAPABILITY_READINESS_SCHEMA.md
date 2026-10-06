# Capability Readiness Schema v1.0

Product capabilities use six independent maturity dimensions.

| Dimension | Allowed states |
|---|---|
| Specification | MISSING / DRAFT / SPECIFIED / FROZEN |
| Implementation | NONE / PARTIAL / IMPLEMENTED |
| Canonical Content | NOT_APPLICABLE / EMPTY / PARTIAL / READY / BLOCKED |
| Internal Validation | NONE / CONTRACT / PARTIAL_FIDELITY / FIDELITY_PASS |
| Empirical Calibration | NOT_APPLICABLE / NONE / PILOT / CALIBRATED |
| Production Readiness | NOT_READY / LIMITED / READY |

Rules:
1. IMPLEMENTED does not imply READY.
2. Empty registry/schema-only coverage cannot produce FIDELITY_PASS.
3. CALIBRATED requires dataset/model/version/metric provenance.
4. Production READY requires an explicit phase graduation decision.
5. "Complete" without a named dimension is forbidden in product state reporting.
