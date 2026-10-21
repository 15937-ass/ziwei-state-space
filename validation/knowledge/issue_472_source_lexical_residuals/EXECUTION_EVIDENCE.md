# Validation Evidence — Issue #472 Career Source Lexical Residuals

Execution runtime: **OpenAI / ChatGPT Work code-mode + container attempt**  
Base commit: `f9831cbe510ce80ca1ee6436104d583a23f341d3`  
Validated content head before state/evidence sync: `9e61d33b91c393311376eb29d6c5c3f5e8382357`  
State sync commit: `872b1b9c6282ee7c0e655ebff31ae421d1ea6f04`

## Validation actually executed

### 1. Source/canonical consistency review
The 10 target Career rows were re-read against the approved Zhongzhou deep-lecture corpus. The resulting artifact records source excerpts, page/printed-page provenance, disposition, normalized structure, residual blockers, and guardrails for all 10/10 rows.

Result: **PASS — 10/10 source-dispositioned.**

### 2. Deterministic branch-content assertions
The actual branch copies of:
- `knowledge/wp08/CAREER_SOURCE_LEXICAL_RESIDUALS_10_v0.1.json`
- `knowledge/wp07c/CAREER_CONTEXTUAL_ACTIVATION_CLOSURE_251_v0.5.json`
- `tests/test_knowledge_career_source_lexical_residuals_10.py`

were fetched back from GitHub and parsed in the OpenAI code-mode runtime. A 27-assertion deterministic check verified:
- exact 10-rule coverage;
- no global ANY / ALL defaults;
- no invented numeric threshold;
- no execution unlock;
- CA01-059 source-surface repair and fail-closed list quantifier;
- CA03-289 paired-pattern local structure;
- CA04-345 open fire-property category + nonnumeric cardinality blocker;
- CA04-391 `NO_UNIVERSAL_RULE`;
- CA05-433 `INSUFFICIENT_SOURCE`;
- CA05-484 corrected alternative structure, with no false `+` conjunction;
- CA06-502 remains nonexhaustive/contextual;
- CA08-723 retains pattern-binding uncertainty;
- CA09-864 no longer uses generic source-shorthand membership;
- closure v0.5 retains 251 rows;
- blocker/count deltas exactly match the declared summary.

Result: **PASS — 27 checks, 0 errors.**

Observed closure:
- `SOURCE_SHORTHAND_MEMBERSHIP_UNSPECIFIED`: 6 -> 0
- `SOURCE_LIST_QUANTIFIER_UNSPECIFIED`: 4 -> 3
- `OPEN_CATEGORY_MEMBER_OR_QUANTIFIER_UNSPECIFIED`: 129 -> 132
- `SOURCE_PATTERN_BINDING_UNSPECIFIED`: 0 -> 1
- no-current-blocker rows: 17 -> 19
- source-underdetermined rows: 207 -> 205
- execution unlocked: 0

### 3. Lane-boundary inspection
PR #474 changed-file list was fetched from GitHub. Current changed paths are:
- `knowledge/KNOWLEDGE_STATE.yaml`
- `knowledge/wp07c/CAREER_CONTEXTUAL_ACTIVATION_CLOSURE_251_v0.5.json`
- `knowledge/wp07c/CAREER_CONTEXTUAL_ACTIVATION_CLOSURE_251_v0.5.md`
- `knowledge/wp08/CAREER_SOURCE_LEXICAL_RESIDUALS_10_v0.1.json`
- `knowledge/wp08/CAREER_SOURCE_LEXICAL_RESIDUALS_10_v0.1.md`
- `tests/test_knowledge_career_source_lexical_residuals_10.py`

These all match the `KNOWLEDGE_ONLY` ownership patterns in `governance/PATH_OWNERSHIP.json`.

Result: **PASS — static changed-path ownership inspection.**

## Mandatory repository shell gate — NOT RUN

Per `governance/WORK_CODEX_EXECUTION_PROTOCOL_v0.1.md`, Knowledge work normally requires before merge:

```bash
PYTHONPATH="$PWD" python -m pytest -q tests/test_knowledge_career_source_lexical_residuals_10.py
PYTHONPATH="$PWD" python -m pytest -q
PYTHONPATH="$PWD" python src/audit_repository.py --fail-on-p0
python tools/validate_governance.py --base-ref "origin/main" --head-branch "knowledge/472-source-lexical-residuals-10"
```

The current OpenAI container could not obtain a repository checkout:
- `git clone` failed because outbound DNS/network access is unavailable in the container;
- GitHub archive/raw download bridging was unavailable in this runtime;
- GitHub Actions was **not** used, in accordance with the G7 policy and PI instruction.

Therefore:
- targeted pytest: **NOT RUN**
- full pytest: **NOT RUN**
- P0 repository audit: **NOT RUN**
- executable governance validator: **NOT RUN**
- product regression: **NOT REQUIRED**

This is an **infrastructure/runtime validation blocker, not a test failure**. PR #474 must remain unmerged until the mandatory full OpenAI/Codex repository gate is actually executed or the Issue receives an explicitly approved narrower validation scope.

## Known limitations

No claim is made that full repository tests pass. No GitHub Actions minutes were consumed. No Product runtime files, probability truth, empirical labels, numeric weights, or canonical source text were modified.
