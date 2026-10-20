# Issue #367 execution evidence

Execution runtime: Codex / OpenAI cloud environment
Canonical base commit: `dc62f6d694aa178a9ebf4f7094e1abb7d5afcd23`
Canonical base tree: `104843a3763f4f17ae0fbb972951b7a92f1f5fab`
Initial published PR head: `febdeb44d533fee9c630bd80fe3960f894681c21`
PR: #368

The local repository was reconstructed from a byte-verified main snapshot because the private remote was accessed through the GitHub connector. All four initial changed files were uploaded as Git blobs and their returned SHA values matched local `git hash-object` values. The final evidence/state-only follow-up commit uses the initial published head as its parent.

## Scope and substantive result

- Fixed canonical selection: the next 100 Career rows after excluding 152 pinned prior structured IDs, from CA02-130 through CA03-235.
- Source rules rechecked: 100.
- First-time complete condition mappings: 41.
- Methodology/context only: 1.
- Blocked outcome mappings: 58.
- Production-executable additions: 0.
- Unique structured mapping/audit IDs: 152 → 252.
- Canonical source-reviewed Career count: 888 → 888; rechecks were not counted as new source rows.
- Approved source: SRC-ZZ-003, PDF pages 68–69 / printed pages 135–137, visually reviewed.
- Attachment SHA-256: `6bddb3cac2e4b4efcf265229cbda22904ab3394aeef832e338ee5939088e5c5c`.

The Chinese audit includes an eight-part content synopsis covering 紫微天相、紫微七杀、天机总论 and the 子午／丑未／寅申／卯酉／辰戌 Tianji systems. It separately explains the 41 complete mappings and the group, relation, composite, absence, real-context and temporal reasons for the 58 blockers.

## Commands and results

1. `python -m pip install --upgrade pytest`
   - pytest 9.1.1 already satisfied.
2. `PYTHONPATH="$PWD" python -m pytest -q tests/test_knowledge_career_100_review_02.py`
   - final: 186 passed, 0 failed, 0 skipped in 0.99s.
3. `PYTHONPATH="$PWD" python -m pytest -q`
   - 990 passed, 0 failed, 0 skipped in 16.07s.
4. `node --check tools/iztro_export.mjs`
   - PASS.
5. `PYTHONPATH="$PWD" python src/audit_repository.py --fail-on-p0 > /workspace/scratch/180b896fb3e5/audit367.json`
   - PASS; P0=0. The existing 907 P1 review candidates remain.
6. `python tools/validate_governance.py --base-ref origin/main --head-branch knowledge/367-career-100-review-02`
   - PASS.
7. `git diff --check origin/main`
   - PASS.
8. `git diff --exit-code origin/main -- product src .github sources validation/wp05`
   - PASS; no Product, runtime, workflow, source or canonical Career CSV changes.
9. Local deterministic invariant script:
   - exactly 100 unique selected rows;
   - every non-complete record has `condition=null`;
   - every entry has `executable_registry_entry=false`;
   - approved source SHA-256 matches;
   - PASS.

Product dual-engine and independent Go regressions were not required because no Product/runtime/engine file changed. GitHub Actions was not used.

## Repair history

The first targeted run produced 185 passes and one failure. The failing assertion incorrectly required CA02-174 to stop matching when 天机化禄 was changed to 天机化权, although 禄、权、忌 are three explicit OR branches in the source rule. One test-only repair changed the assertion to require all three authorized branches to match and 化科 not to match. No source mapping, canonical row, Product code or runtime semantics changed. The final targeted and full suites passed.

## Known limitations

These records are source-preserving, non-production condition candidates and explicit blockers. Runtime condition matching does not establish real-chart reachability, empirical prediction validity, probability, or causal effect.
