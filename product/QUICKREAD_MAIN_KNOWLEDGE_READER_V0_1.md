# QuickRead main knowledge reader v0.1

Status: implementation contract for a read-only, main-pinned reader; no deployment or predictive-validity claim.

## Purpose

Fetch the latest accepted repository snapshot from `main` on each call, then retrieve only the source-backed material relevant to the requested chart domain and time layer. This lets QuickRead notice newly merged source-review batches and Product provider declarations without maintaining a manually copied knowledge list.

## Data flow

1. Resolve `main` to one commit SHA through the public GitHub API.
2. Fetch the recursive Git tree for that exact SHA. If GitHub reports a truncated tree, stop rather than use an incomplete inventory.
3. Fetch only the selected files by immutable commit SHA and verify each content body against the Git blob SHA in the tree.
4. Discover Product provider declarations under `product/PL3N_*_DOMAIN_PROVIDER_v*.json`. Read the accepted default runtime registry from `src/product/natal_domain_registry.py`; provider files not enabled by that registry remain visible as opt-in and are never silently activated.
5. Discover the currently supported source-first ledgers under `knowledge/palaces/Pxx_*/wp05/*SOURCE_READJUDICATION*.json` for the requested palace.
6. Convert eligible, directly source-reviewed, non-case-only records into the QuickRead `SOURCE` evidence lane. Build a version-pinned capability manifest and an audit report for the caller.

## What qualifies as source evidence

A source ledger is consumed only when its status is exactly `SOURCE_REVIEW_COMPLETE` and its source basis uses `DIRECT_PDF_VISUAL_REVIEW`. A record must also have an explicit promotion disposition, normalized source condition, no unresolved source-condition uncertainty, no changed source span, a direct-visual-review note, source location, and an exact match to the requested time layer.

The reader excludes `CASE_SUPPORT_ONLY`, held/unpromoted, uncertain, unverified, and time-layer-mismatched records. Eligible source records are marked `SOURCE_GROUNDED` with `SEMANTIC_ONLY` allowed use. This is source support, not executable rule authorization.

## Runtime capability boundary

The manifest reports a runtime capability only when (1) the current main runtime registry declares that domain by default, (2) its explicit input registry/source rows reconcile, (3) the caller supplies a clean local Git checkout whose HEAD is exactly the current-main SHA, and (4) the local provider/source input files match the blob SHAs from that pinned main tree. If the checkout is stale, dirty, or omitted, the reader still retrieves source-only material but does not assert executable runtime capability. It does not claim a chart-specific rule executed. The caller must run the actual accepted runtime and provide its result as `RUNTIME` evidence with target, execution ID, and exact version provenance.

A provider file on main is not enough to activate a provider. For example, a Product provider marked `CANONICAL_READY` but absent from the default registry is reported as opt-in and left disabled. The reader never changes Product KIB locks, runtime registries, or Knowledge acceptance flags.

## Scope, progressive retrieval, and token-cost controls

- Only requested domains and their supported palace source ledgers are retrieved.
- The default **first-pass** source budget is 20 items per requested slot. This is a per-call batch size for a brief reading, **not** a session/global cap and not a claim that only 20 relevant records exist.
- The report distinguishes total eligible evidence, evidence already seen in earlier batches, evidence selected in the current batch, and evidence remaining after the batch.
- When more evidence remains, the reader returns a continuation object containing the pinned `main_sha`, requested slot IDs, accumulated `seen_evidence_ids`, and `has_more=true`. A later call may pass that continuation to retrieve the next ranked unseen batch without repeating earlier evidence.
- Continuation is fail-closed: if GitHub `main` changed, the old continuation is rejected and the caller must begin a fresh first-pass read against the new accepted snapshot. This prevents a detailed follow-up from silently mixing two repository versions.
- A caller can therefore support **简批 → 追问 → 详细批/理由展开** progressively. It should keep the first response small, continue the same scope only when the conversation needs more depth, and start a fresh first pass for newly introduced scope slots.
- Each individual batch remains bounded (currently 1–50 source items per slot), while repeated continuation batches have no fixed 20-item session total. The practical ceiling is the caller's answer/token budget plus the reader's per-call byte and integrity limits.
- The module returns a compact, traceable payload. It does not send the entire repository corpus to an LLM.
- It uses Python standard-library HTTP/JSON/CSV/AST utilities only; no new package dependency and no GitHub token are required for this public repository.
- Each invocation resolves current `main`; there is no stale-cache fallback. A network, schema, size, truncation, or blob-integrity error fails closed.
- Runtime capability is not exposed unless the caller passes `repository_root`, the checkout is clean at the exact current-main SHA, and the selected local runtime inputs match the pinned main tree. The CLI supplies its repository root automatically.
- HTTP timeout is 8 seconds; a selected artifact is limited to 2 MB and the aggregate fetched-byte budget is 10 MB.

## Current supported formats and known gaps

- Product provider discovery: `PL3N_*_DOMAIN_PROVIDER_v*.json`.
- Executable NATAL manifest adapter: default Wealth provider input paths and explicit source rows; other domains are executable only if they are enabled by the default registry and have a supported provider adapter.
- Source-only retrieval: directly visually reviewed source-first palace ledgers matching `SOURCE_READJUDICATION`.
- Other Knowledge formats, mapping candidates, state caches, Issue text, unmerged branches, archived material, and free-form historical reports are not auto-promoted or treated as source evidence. They require a separately reviewed adapter.
- The currently accepted production temporal response/manifestation registry remains empty. NATAL-only evidence is not relabeled as a DECADE/YEAR/MONTH/DAY/HOUR conclusion.

## Use

From a repository checkout with network access:

```bash
python -m src.product.quickread_main_reader \
  --domain relationship \
  --layer NATAL \
  --question "简单看看夫妻宫感情倾向"
```

The CLI emits the main SHA, discovered providers, the current source-evidence batch, capability manifest, exclusions, continuation state, and a compact QuickRead payload. It does not calculate a chart or call an LLM. An application caller can pass the normalized chart context and payload to its chosen verbalizer, then validate any returned model supplements with the existing QuickRead contract. Programmatic callers can pass the returned `reader_report.continuation` into a later `load_latest_main_knowledge(..., continuation=...)` call to expand the same scope progressively.

## Acceptance criteria

- Every loaded artifact is pinned to one current-main commit and passes Git blob SHA verification.
- The reader does not call the API for a branch/PR ref, and never reads unmerged PR files.
- Newly merged source-review ledgers and provider files following the supported naming/schema conventions are discovered automatically on the next call.
- Held, uncertain, case-only, unreviewed, and mismatched-time records are excluded.
- Provider discovery does not equal runtime execution; opt-in providers remain opt-in.
- A missing/unavailable current-main snapshot fails closed instead of silently falling back to stale local knowledge or model memory.
- Focused tests use a deterministic fake transport; routine CI does not depend on live network availability.
- The default 20-item first pass is tested as a batch budget, continuation returns only unseen evidence, and a stale-main continuation fails closed.
