# Issue #394 validation evidence

Execution model: current ChatGPT conversation as repository operator under G9; deterministic repository validation by G8 standard public GitHub-hosted PR runner.

## Knowledge scope

- source rules rechecked: 100
- range: CA07-647 through CA08-749, with CA07-671/672/673 excluded because already structured
- complete condition mappings: 24
- methodology/context: 11
- blocked outcome mappings: 65
- production additions: 0
- unique structured IDs: 652 -> 752
- canonical Career source-review count: 888 unchanged

## Source review

Approved source: SRC-ZZ-003 《中州派紫微斗数深造讲义（下册）》, printed pp.149-151 / PDF pp.75-76.
Attachment SHA-256: `6bddb3cac2e4b4efcf265229cbda22904ab3394aeef832e338ee5939088e5c5c`.

Pages were directly reviewed in the OpenAI file environment. Parsed source text is stored without silent correction of OCR/scan anomalies.

## Producer / critic checks

Critic pass explicitly checked:
- “前格” records keep explicit inherited source IDs;
- 子午贪狼—紫微、寅申贪狼—廉贞、辰戌巨门—天同、巳亥巨门—太阳 and Tianxiang explicit opposite structures are not flattened;
- 巨门化禄 vs 禄存同度 is represented as OR, not AND;
- “从商/从军刑/从医/名义最高位置/任职” remain external real-world state;
- vague 会/借会/相会 relations are not rewritten as same-palace facts;
- 廉贞化忌 and 武曲化忌 are bound to explicit opposite-palace carriers only when source geometry is explicit;
- profession examples remain context unless the source explicitly states a scene translation from a complete chart antecedent;
- all complete mappings use only existing approved atoms and remain non-production.

## Deterministic repository gate

Final PR head must pass:
- targeted seventh-review deterministic tests;
- full `python -m pytest -q`;
- Node syntax check when applicable;
- `python src/audit_repository.py --fail-on-p0`;
- Knowledge lane governance validation against `origin/main`.

Exact workflow run/result will be recorded in the PR after completion.

## Known limitations

- source-grounded normalization is not empirical calibration;
- traditional scene candidates are possibilities in the cited system, not population probabilities;
- all complete mappings remain non-production candidates.
