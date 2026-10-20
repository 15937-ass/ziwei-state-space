# Issue #386 validation evidence

Execution model: current ChatGPT conversation as repository operator under G9; deterministic repository validation by G8 standard public GitHub-hosted PR runner.

## Knowledge scope

- source rules rechecked: 100
- range: CA05-446 through CA06-546 after excluding previously structured CA05-469
- complete condition mappings: 27
- methodology/context: 17
- blocked outcome mappings: 56
- production additions: 0
- unique structured IDs: 452 -> 552
- canonical Career source-review count: 888 unchanged

## Source review

Approved source: SRC-ZZ-003 《中州派紫微斗数深造讲义（下册）》, printed pp.143-146 / PDF pp.72-73.
Attachment SHA-256: `6bddb3cac2e4b4efcf265229cbda22904ab3394aeef832e338ee5939088e5c5c`.

Pages were directly reviewed in the OpenAI file environment. OCR wording was not silently corrected.

## Producer / critic checks

Critic pass explicitly checked:
- 天同六宫过渡：寅申天同天梁、卯酉天同对太阴、辰戌天同、巳亥天同不互相误继承；
- CA06-501 仍属于寅申廉贞对贪狼上下文，不提前进入卯酉廉贞破军；
- 古今转换、血腥导演例、工商文武转换、跨宫校验与现实从政/从商选择不伪装成 chart-only rules；
- 夹宫、禄马交驰、府相朝垣、群组量词、庙陷、缺席和 temporal semantics 保持阻塞；
- all complete mappings use only existing approved atoms and remain non-production.

## Deterministic repository gate

Final PR head must pass:
- targeted fifth-review deterministic tests;
- full `python -m pytest -q`;
- Node syntax check when applicable;
- `python src/audit_repository.py --fail-on-p0`;
- Knowledge lane governance validation against `origin/main`.

Exact workflow run/result will be recorded in PR #390 after completion.

## Known limitations

- source-grounded normalization is not empirical calibration;
- scene candidates remain traditional/source possibilities, not population probabilities;
- all complete mappings remain non-production candidates.
