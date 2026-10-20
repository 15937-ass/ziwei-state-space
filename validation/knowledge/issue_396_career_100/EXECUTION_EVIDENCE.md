# Issue #396 validation evidence

Execution model: current ChatGPT conversation as repository operator under G9; deterministic repository validation by G8 standard public GitHub-hosted PR runner.

## Knowledge scope

- source rules rechecked: 100
- range: CA08-750 through CA09-851, excluding already structured CA08-765/766
- complete condition mappings: 16
- methodology/context: 17
- blocked outcome mappings: 67
- production additions: 0
- unique structured IDs: 752 -> 852
- canonical Career source-review count: 888 unchanged

## Source review

Approved source: SRC-ZZ-003 《中州派紫微斗数深造讲义（下册）》, printed pp.151-154 / PDF pp.76-77.
Attachment SHA-256: `6bddb3cac2e4b4efcf265229cbda22904ab3394aeef832e338ee5939088e5c5c`.

Pages were directly reviewed in the OpenAI file environment. Parsed source text is stored without silent correction of OCR/scan anomalies.

## Producer / critic checks

Critic pass explicitly checked:
- 天梁“同拱/借会” is not rewritten as an explicit opposite relation;
- only CA08-787 binds 天机化忌 to P03 because the source explicitly states 相对;
- commercial/public-service/education choices remain external context states;
- 七杀 postnatal cultivation is preserved as control/method evidence and does not rewrite natal truth;
- 子午七杀 vague 会 transformations remain relation blockers;
- 寅申七杀 opposite 紫微天府 remains exact geometry;
- CA09-851 remains YEAR temporal logic rather than a static natal trigger;
- all complete mappings remain non-production and use only approved atoms.

## Deterministic repository gate

Final PR head must pass:
- targeted eighth-review deterministic tests;
- full `python -m pytest -q`;
- Node syntax check when applicable;
- `python src/audit_repository.py --fail-on-p0`;
- Knowledge lane governance validation against `origin/main`.

Exact workflow run/result will be recorded in the PR after completion.

## Known limitations

- source-grounded normalization is not empirical calibration;
- traditional scene candidates are possibilities in the cited system, not population probabilities;
- all complete mappings remain non-production candidates.
