# Issue #381 validation evidence

Execution model: current ChatGPT conversation as repository operator under G9; deterministic repository validation by G8 standard public GitHub-hosted PR runner.

## Knowledge scope

- source rules rechecked: 100
- range: CA04-343 through CA05-445 after excluding previously structured IDs
- complete condition mappings: 31
- methodology/context: 11
- blocked outcome mappings: 58
- production additions: 0
- unique structured IDs: 352 -> 452
- canonical Career source-review count: 888 unchanged

## Source review

Approved source: SRC-ZZ-003 《中州派紫微斗数深造讲义（下册）》, printed pp.140-143 / PDF pp.70-72.
Attachment SHA-256: `6bddb3cac2e4b4efcf265229cbda22904ab3394aeef832e338ee5939088e5c5c`.

Pages were directly reviewed in the OpenAI file environment. OCR wording was not silently corrected.

## Producer / critic checks

The review intentionally preserves blockers for:
- 昌曲、火铃、煞曜、辅佐/桃花等群组的成员或量词不确定性；
- “见/会/同拱”等未固定空间关系；
- 财荫夹、刑忌夹、火贪/铃贪等复合结构；
- “墓”等当前未建模状态体系；
- 经商、自行经营、稳守、后天努力等现实行为条件；
- 大运流年、中年、晚成等时序语义。

Career examples such as 潜水/水管 and “后天努力可以扭转命运” are preserved as context rather than promoted into direct occupational predictions.

## Deterministic repository gate

The final PR head must pass:
- changed-unit deterministic tests;
- full `python -m pytest -q`;
- Node syntax check when applicable;
- `python src/audit_repository.py --fail-on-p0`;
- Knowledge lane governance validation against `origin/main`.

The exact final workflow reference/result will be recorded in the PR body after completion.

## Known limitations

- Source-grounded normalization is not empirical calibration.
- All complete mappings remain non-production candidates.
