# Validation Evidence — Issue #472 Career Source Lexical Recheck

Execution runtime: **OpenAI / ChatGPT code-mode GitHub-content assertions + local container checkout attempt**
Base commit: `7865dfa8e02506cbff92454a4e00dbda2efede9f`
Initial artifact/test content head: `cbccf56e806b7817854e7a8ac1e1638185baa24c`
Post-state validation head checked with 44 assertions: `60818a48eb46cfe9a7274aefcfd2f656768aa7e5`
State sync commits (Knowledge lane checkpoint and superseded-PR status): `749a192ecd41bb4c70ff37cc13dbb79f4af14fde`, `edf6c887092629061ac974cc3304817fa663d168`
Final network-diagnostic evidence update: `e71ff341fd54d7bff30601a138b0620865c06696`

## Validation actually executed

### 1. Source re-adjudication
- Reviewed all 10 target rows against the prior Issue #469 source-lexicon artifact and current main closure v0.10.
- Disclosed exact target overlap: **10/10 IDs overlap with Issue #469**; this is a re-adjudication, not new row coverage.
- Rechecked the lower-volume Career clause and upper-volume pair commentary for CA03-289.

Result: **PASS — 10/10 source dispositions.**

### 2. Deterministic OpenAI code-mode assertions
Fetched the current main baseline, prior Issue #469 artifact, new recheck artifact, and closure v0.10/v0.11 directly from GitHub and validated the actual content.

Result: **PASS — 44 assertions / 0 errors** on the post-state validation head listed above.

Assertions cover:
- exact 10-rule target set and duplicate overlap disclosure;
- CA01-059 restoration of the inner source-list quantifier blocker;
- CA03-289 pair-internal evidence while preserving outer list quantifier and `等杂曜` blockers, with no `ANY_OF` inference;
- CA06-502 refinement to existing `LU_SHORTHAND_CONTEXTUAL_UNRESOLVED`;
- all recheck rows remain uncompiled and execution-locked;
- closure v0.11 retains 251 rows, 22 no-current-blocker rows, 202 source-underdetermined rows, 41 cumulative source-resolution changes, 9 source-condition repairs;
- blocker counts: source-list quantifier 8, generic source-shorthand 0, contextual LU 5;
- guardrails against global quantifier defaults, numeric thresholds, and Product/runtime changes.

### 3. Repository shell attempt
Attempted the required checkout in the available OpenAI container:

```bash
git clone --depth 1 https://github.com/15937-ass/ziwei-state-space.git /tmp/ziwei-state-space
```

Result: **INFRASTRUCTURE BLOCKER** — `fatal: unable to access 'https://github.com/15937-ass/ziwei-state-space.git/': Could not resolve host: github.com`. A follow-up `curl --resolve` attempt against four GitHub HTTPS IPs also failed immediately with `Could not connect to server`; outbound repository access is unavailable, not merely a missing local DNS cache.

Because no repository checkout is available in this runtime, the following were **NOT RUN**:
- targeted pytest;
- full `PYTHONPATH="$PWD" python -m pytest -q`;
- `python src/audit_repository.py --fail-on-p0`;
- `python tools/validate_governance.py --base-ref origin/main --head-branch knowledge/472-lexical-recheck-v02`.

GitHub Actions: **NOT USED**.
Product regression: **NOT REQUIRED** (Knowledge-only paths).

## Merge gate
The 31 content assertions are not represented as pytest or as a substitute for the mandatory full repository gate. **Keep the PR unmerged** until the full approved OpenAI/Codex shell gate is run, or a narrower validation scope is explicitly approved by the PI. The failure is infrastructure/network DNS, not a test failure.

PR #474 was closed unmerged as superseded because its base is stale/dirty and its target IDs duplicate Issue #469; clean-main draft PR #493 now carries this re-adjudication.

Known limitations: no shell checkout, no pytest/P0/governance execution evidence yet.