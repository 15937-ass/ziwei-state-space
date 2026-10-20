# Issue #362：事业宫百条批次01验证证据

Execution runtime: Codex / OpenAI cloud environment
Environment: Python3.12.14; pytest9.1.1; Nodev24.19.0
Base commit: 64158b2f253e2ac5a709cdee5f44c33cd8954e56
Head commit: PR #366 Validation Evidence records final publication SHA (avoids self-reference).

## 计数与来源

按canonical顺序排除52个既有结构化ID后，预先固定下一100条；不是按测试通过情况筛选。内部来源推理50+50，每个子批50个ID，整合和PI报告一次100。

- 本轮复核源规则100条；20条首次完整条件映射；30条方法／语境；50条结果条件阻塞。20+30+50=100。
- 新增生产可执行0条；所有100项的executable_registry_entry=false。
- canonical源文已审查888→888，复核不重复新增源规则。
- 结构化映射／审查ID52→152，包含方法与阻塞，不冒称152条完整映射或可执行。
- 20条完整条件ID及其余80条逐条理由见JSON和中文AUDIT表；证据段落及测试用例不计作规则。

来源SRC-ZZ-003下册PDF66–68页、印刷132–135页对应列已视觉核对；SHA-256为6bddb3cac2e4b4efcf265229cbda22904ab3394aeef832e338ee5939088e5c5c，与批准source_index一致。每条保留完整canonical行、provenance、review、原time_layer、case、history及投影字段。JSON保留分列原文用于追溯，OCR错误不静默校订。

## Producer / critic / revision

Producer逐条恢复母段、前格、星系／地支／四化及对宫分配；只有全部必要条件能用现有事实表达的20条才编译。Critic检查群体吉煞、百官、桃花、夹／会／拱照关系、示例范围、现实行为、时序路径与方法非蕴含，分别保留30条方法语境和50条结果阻塞，condition均null。不会把null转为空条件。

CA01-067复用已审066条件；068含8个完整分支，CA02-124含4个完整分支，均有OPPOSITE。其余完整条目保留子午／丑未／寅申／卯酉／辰戌母段范围及命名四化。没有改Product代码、生产注册表、canonical源行、旧映射、原子类型、本体或权重。

前批357计数测试动态扫描未来文件会污染当时44→52基线。本批将其固定到当时8份前序映射文件；保留全部历史断言不放宽。本批以9份前序映射文件独立验证52→152，未来新增文件不改历史计数。

首次针对性测试123 passed /21 failed：20处是新测试错误调用fact_from_atom接口，1处是CA01-014理由不足长度阈值。一次修复正确传参并补充014真实缺口说明，未删／放松断言、未改产品逻辑；重跑144项全通过。

## Exact commands

Run from repository root:

```bash
PYTHONPATH="$PWD" python -m pytest -q tests/test_knowledge_career_100_review_01.py tests/test_knowledge_career_ziwei_zipo_static_8.py
PYTHONPATH="$PWD" python -m pytest -q
node --check tools/iztro_export.mjs
PYTHONPATH="$PWD" python src/audit_repository.py --fail-on-p0 > /workspace/scratch/180b896fb3e5/audit362.json
python tools/validate_governance.py --base-ref origin/main --head-branch knowledge/362-career-100-review-01
git diff --check origin/main
git diff --exit-code origin/main -- product src .github sources validation/wp05
```

Results:
- Targeted144 passed /0 failed /0 skipped（本批123＋前批历史计数21）。
- Full pytest804 passed /0 failed /0 skipped；整仓验证集中在本百条批次收尾执行。
- JS syntax / P0 audit / Knowledge governance / scope+diff:PASS。
- P0=0，907既有P1 review candidates保留。
- Product dual-engine／Go／B02 regression:NOT_REQUIRED，未修改对应代码／算法，未执行且不冒称执行。
- GitHub Actions:NOT_USED。
- Generated durable report:本文件；完整P0输出为上述可重建临时文件。

## Snapshot / limits

固定基线864个blob逐文件核对SHA；origin/main为字节验证的本地基线引用。大JSON按base64传输创建Git blob，回读SHA046b880fb797e698683a9a5b56e77a82fc524a4c与本地git hash-object一致。合入前所有PR变更blob与本地内容逐一核对，其余主线内容不变。

条件匹配与来源追溯是内部保真验证，不是现实预测有效性、行为发生证明或经验因果证据。群体／复合关系／时序／行为缺口需要后续专门工作，不在本批冻结新语义。30条方法语境不当作结果，50条阻塞不冒称完成映射。下一批仍按100条PI报告，不自动串行开启下一个Issue。
