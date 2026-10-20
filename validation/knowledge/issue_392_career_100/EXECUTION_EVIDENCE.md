# Issue #392 validation evidence

Execution model: current ChatGPT conversation as repository operator under G9; deterministic repository validation by G8 standard public GitHub-hosted PR runner.

## Knowledge scope

- source rules rechecked: 100
- range: CA06-547 through CA07-646
- complete condition mappings: 20
- methodology/context: 10
- blocked outcome mappings: 70
- production additions: 0
- unique structured IDs: 552 -> 652
- canonical Career source-review count: 888 unchanged

## Source review

Approved source: SRC-ZZ-003 《中州派紫微斗数深造讲义（下册）》, printed pp.146-149 / PDF pp.73-75.
Attachment SHA-256: `6bddb3cac2e4b4efcf265229cbda22904ab3394aeef832e338ee5939088e5c5c`.

Pages were directly reviewed in the OpenAI file environment. OCR wording was not silently corrected.

## Producer / critic checks

Critic pass explicitly checked:
- 天府夹宫、叠禄、火铃/空劫/羊陀群组与“来会/照射”关系不被缩写成普通同宫；
- 巳亥天府对宫紫微七杀及紫微化权载体保持在 P03 opposite geometry；
- 太阴—天机化禄/太阴化忌同时保留同度和对宫两种空间实现；
- 卯酉太阴规则保留天同对拱母结构；
- 辰戌太阴规则把太阳化禄/化忌绑定到对宫载体；
- 贪狼“化禄、化权”按二择分支，不误写为同一星同时化禄化权；
- “贪狼为饮食之星”仅保留象义/语境，未直接升级成餐饮职业规则；
- 庙陷、缺席、学历/日夜生、temporal semantics 和现实选择不被静态近似；
- all complete mappings use only existing approved atoms and remain non-production.

## Deterministic repository gate

Final PR head must pass:
- targeted sixth-review deterministic tests;
- full `python -m pytest -q`;
- Node syntax check when applicable;
- `python src/audit_repository.py --fail-on-p0`;
- Knowledge lane governance validation against `origin/main`.

Exact workflow run/result will be recorded in the PR after completion.

## Known limitations

- source-grounded normalization is not empirical calibration;
- traditional scene candidates are possibilities in the cited system, not population probabilities;
- all complete mappings remain non-production candidates.
