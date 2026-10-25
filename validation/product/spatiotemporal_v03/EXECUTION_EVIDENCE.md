# Spatiotemporal guarded-temporal probe v0.3 — execution evidence

Status: **PENDING exact-head repository validation** until the linked Draft PR checks complete.

## Source and fixture pins

- Producer workflow run: `40161980768`.
- Producer artifact: `12586873751`, digest `sha256:730158ea500b26b458ca836091a23bf209363e8121437bf0296f374dc5936a8f`.
- Reduced fixture SHA-256: `f2cea083717685fbacf2911ed5fe2e15ba3692122519708ac606943c45684450`.
- Main activation base at issue creation: `20c5716a6bf609fc86e1b6668595a10f84ccc934`; recheck current main before PR validation.

## Validation policy

GitHub Actions checks on the final PR head are authoritative. Exact base/head and workflow run IDs will be recorded in Issue #772 after the final run completes. Any code or evidence-file edit changes the head and invalidates earlier-head evidence. Do not represent older runs as validation of a later commit.

## Scope boundary

Only files listed in Issue #772 may change. No production runtime, canonical temporal registry, Knowledge/Core/Governance, KIB lock, PL1 exporter/schema, or workflow changes are authorized. No canonical semantics, production migration, or predictive-validity claim is authorized.
