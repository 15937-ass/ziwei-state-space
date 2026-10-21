# Validation Evidence — Issue #472 Career Source Lexical Recheck

Execution runtime: **OpenAI / ChatGPT code-mode GitHub-content assertions + local container checkout attempt**
Base commit: `7865dfa8e02506cbff92454a4e00dbda2efede9f`
Initial artifact/test content head: `cbccf56e806b7817854e7a8ac1e1638185baa24c`
Earlier post-state validation head checked with 44 assertions: `60818a48eb46cfe9a7274aefcfd2f656768aa7e5`
Revised semantic content head after same-source CA05-433 critic pass: `680ea3354b7f4228f0f260498e6945a80263c5fa`
State sync commits (Knowledge lane checkpoint and superseded-PR status): `749a192ecd41bb4c70ff37cc13dbb79f4af14fde`, `edf6c887092629061ac974cc3304817fa663d168`
Final network-diagnostic evidence update: `e71ff341fd54d7bff30601a138b0620865c06696`

## Validation actually executed

### 1. Source re-adjudication
- Reviewed all 10 target rows against the prior Issue #469 source-lexicon artifact and current main closure v0.10.
- Disclosed exact target overlap: **10/10 IDs overlap with Issue #469**; this is a re-adjudication, not new row coverage.
- Rechecked the lower-volume Career clause and upper-volume pair commentary for CA03-289.
- Performed a deeper same-source cross-passage check for CA05-433. The Career clause `见天厨、火星同度者尤然` is reinforced later in the same volume by `天厨、火星同度` tied to food-industry manifestation plus the discriminating contrast `不见天厨` -> sharp-tool occupations, and by a further `天厨、火星同躔` food-appreciation passage. This supports source-local pair co-presence for CA05-433 without creating a global pair rule.

Result: **PASS — 10/10 source dispositions, with one revised source-local resolution (CA05-433).**

### 2. Deterministic OpenAI code-mode assertions
Fetched the current main baseline, prior Issue #469 artifact, new recheck artifact, and closure v0.10/v0.11 directly from GitHub and validated the actual content.

Earlier result: **PASS — 44 assertions / 0 errors**.

After the CA05-433 correction, the current branch artifacts were re-fetched from GitHub and checked again.

Revised result: **PASS — 69 assertions / 0 errors**.

Assertions cover:
- exact 10-rule target set and duplicate overlap disclosure;
- CA01-059 restoration of the inner source-list quantifier blocker;
- CA03-289 pair-internal evidence while preserving outer list quantifier and `等杂曜` blockers, with no `ANY_OF` inference;
- CA05-433 source-local pair co-presence resolution from repeated same-source syntax, with no global pair generalization;
- CA06-502 refinement to existing `LU_SHORTHAND_CONTEXTUAL_UNRESOLVED`;
- all recheck rows remain uncompiled and execution-locked;
- closure v0.11 retains 251 rows, **23** no-current-blocker rows, **201** source-underdetermined rows, **42** cumulative source-resolution changes, 9 source-condition repairs;
- blocker counts: source-list quantifier **7**, generic source-shorthand 0, contextual LU 5;
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

Post-revision shell retry from the available OpenAI container against branch head `e392a184138895d0d949323f1475cc52b731b49b`:

```bash
git clone --depth 1 --branch knowledge/472-lexical-recheck-v02 https://github.com/15937-ass/ziwei-state-space.git /tmp/ziwei-state-space
```

Result: **INFRASTRUCTURE BLOCKER again** — `Could not resolve host: github.com`. No test command was falsely counted as executed.

Historical G8 repository quality gate on superseded PR #493 head `563c16625910d43c646445a872bf84f5db613b63`: **PASS — run #1849 / 39555667234**. This proves the former exact head passed full pytest, P0 audit and governance validation. PR #493 later became stale after Governance main advanced and is superseded by a clean current-main reconstitution.

Current reconstitution: PR created from current main under `knowledge/472-lexical-recheck-v03`; its exact final head must pass the current G8 repository quality gate before merge. Product regressions are not semantically required for this Knowledge-only change, though repository path filters may run them automatically.

## Merge gate
The earlier local container network failure is historical infrastructure evidence only. Under current G8, standard public GitHub Actions are the approved routine deterministic validation runtime. The superseded PR #493 exact head passed repository-quality-gate #1849; the clean current-main reconstitution must also pass the repository-quality-gate on its own final exact head before merge.

PR #474 and PR #493 are preserved as superseded audit history. The current implementation is the clean current-main reconstitution branch `knowledge/472-lexical-recheck-v03`.

Known limitation: blocker-free Knowledge structure still does not imply Product compilation or runtime execution; conditions_compiled=0 and execution_unlocked=0 remain unchanged.