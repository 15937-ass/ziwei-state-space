# Issue #369 validation evidence

Execution model: current ChatGPT conversation as repository operator under G9; deterministic repository validation by G8 standard public GitHub-hosted PR runner.

## Knowledge scope

- source rules rechecked: 100
- range: CA03-236 through CA04-342 after excluding previously structured IDs
- complete condition mappings: 30
- methodology/context: 8
- blocked outcome mappings: 62
- production additions: 0
- unique structured IDs: 252 -> 352
- canonical Career source-review count: 888 unchanged

## Source review

Approved source: SRC-ZZ-003 《中州派紫微斗数深造讲义（下册）》, printed pp.137-140 / PDF pp.69-70.
Attachment SHA-256: `6bddb3cac2e4b4efcf265229cbda22904ab3394aeef832e338ee5939088e5c5c`.

The source pages were directly reviewed in the OpenAI file environment. OCR wording was not silently corrected.

## Producer / critic checks

Independent post-review checks verified:
- all 100 embedded source records match the canonical CA03/CA04 CSV rows;
- disposition closure is exactly 30/8/62;
- every complete mapping uses only existing approved atom types;
- every non-complete mapping has `condition=null` and an explicit blocker;
- no mapping enters the production registry;
- source-span context is preserved;
- critic corrections for 昌曲 quantifier, 左辅/右弼会照 relation, 教学/演唱 example semantics, and 前格 inheritance are preserved.

## Deterministic repository gate

The final PR head is validated by the repository quality gate required by G8:
- full `python -m pytest -q`;
- Node syntax check when applicable;
- `python src/audit_repository.py --fail-on-p0`;
- lane governance validation against `origin/main`.

Exact final workflow run/result is recorded in PR #379 after the run completes. The workflow result is execution evidence only and does not upgrade Zhongzhou source claims into empirical truth.

## Known limitations

- This work is source-grounded normalization, not empirical calibration.
- All complete mappings remain non-production candidates.
