# Issue #357：紫微／丑未紫破八条映射验证

Execution runtime: Codex / OpenAI cloud environment
Environment: Python3.12.14; pytest9.1.1; Nodev24.19.0
Base commit: 9a6729699ff83d29e52b1ab36f7295001b840c15
Head commit: see PR #360 Validation Evidence after publication (avoids self-reference).

## 规则计数

- 本轮复核既有源规则：8条。
- 首次完成条件映射：8条（CA01-047、050、083、087、088、089、093、095）。
- 本批新增未决／阻塞：0条。
- 新增生产可执行规则：0条；全部为非生产知识候选。
- 事业宫源文已审查：888→888，不重复增加既有源行。
- 结构化映射／审查去重ID：44→52，包含此前阻塞和方法审查项；不冒称52条全可执行。

机器统计已由针对性测试核对：八个ID此前均未出现在其他WP07A映射记录中；资料片段、证据文件、测试用例不当作规则累计。

## Producer / critic / source

Producer完成原条件、来源、审核状态、NATAL、case_support_only、history_feedback及投影字段逐项保真；六条紫破映射均保留丑未、紫微和破军同宫。087／088指定破军化禄；089指定破军化权；095要求左辅右弼同时位于P09。只有现有PALACE_HAS_STAR、BRANCH_PRESENT、TRANSFORMATION_PRESENT。

Critic复核133–134页原文：紫微独当一面不等于自行经营或领袖；088同句继承087化禄；093“无论如何”回到丑未紫破总范围，不误加前句化禄／不能开创条件，也不跨到寅申紫府；095同度不改成任一或会照。详细中文审查在对应AUDIT文件。没有改源行、Product运行时、生产注册表或既有映射。

来源SRC-ZZ-003，本轮附件PDF67页／印刷133–134页，直接视觉核对。SHA-256为6bddb3cac2e4b4efcf265229cbda22904ab3394aeef832e338ee5939088e5c5c，与批准source_index一致。

## Exact commands and results

从仓库根目录执行：

```bash
python -m pip install --upgrade pytest
PYTHONPATH="$PWD" python -m pytest -q tests/test_knowledge_career_ziwei_zipo_static_8.py
PYTHONPATH="$PWD" python -m pytest -q
node --check tools/iztro_export.mjs
PYTHONPATH="$PWD" python src/audit_repository.py --fail-on-p0 > /workspace/scratch/180b896fb3e5/audit357.json
python tools/validate_governance.py --base-ref origin/main --head-branch knowledge/357-career-ziwei-zipo-static-8
git diff --check origin/main
git diff --exit-code origin/main -- product src .github sources validation/wp05
```

- Targeted:21 passed /0 failed /0 skipped。
- Full pytest:673 passed /0 failed /0 skipped。
- JS syntax / P0 audit / Knowledge governance / scope+diff:PASS。
- P0=0；907既有P1 review candidates保留。
- Product dual-engine／Go／B02 regression:NOT_REQUIRED，本批无排盘／引擎／适配器／Product修改，未执行也不声称执行。
- GitHub Actions:NOT_USED。
- Generated durable report:本文件。完整P0输出为上述临时文件，可重建。

恢复后首次测试启动发现环境未安装pytest（No module named pytest）；按协议安装pytest9.1.1后，同一针对性命令及整仓命令均通过。该依赖缺失不是规则断言失败，未改测试断言或产品逻辑。

## Snapshot / limits

固定主线快照通过connector读取并逐文件核对Git blob SHA，共855个基线文件。origin/main是匹配固定提交内容的本地基线引用。合入前远端PR每个改动文件与本地验证内容核对哈希，其他主线blob保持不变。

合成结构验证条件布尔语义，不证明真实排盘可达性；来源投影不升级为现实职业、收入、开创成功或波折事件的确定预测。没有经验概率、数值权重或经验预测有效性结论。本批八条尚未交付生产执行。
