# Issue #352：火铃量词批准来源证据

Execution runtime: Codex / OpenAI cloud environment
Environment: Python 3.12.14; pytest 9.1.1; Node v24.19.0
Base commit: 9116579ce35de7ad4556a77430005641946c633d
Head commit: recorded in PR #355 Validation Evidence after publication (avoids self-reference).

## Result / producer-critic review

审查8段、3项已批准中州派来源，未超过10段Issue范围。各附件SHA-256与source_index逐一一致；实际渲染检查初级PDF21/65、深造上PDF72/87/88、深造下PDF67页。星名身份、局部或、同时、分居两邻宫及分星讨论分别记录。同页不同分支不互相覆盖；没有把局部解释冻结为通用AND/OR。FB05的局部判断单独标为INFERRED_FROM_LOCAL_EXPOSITION；FB07保留原字“需用同时”，不静默校订。

CA01-035的量词仍无直接适用的充分证据，条件null、执行阻塞不变。原canonical行、#349历史上下文审查、Product运行时／生产注册表及工作流未改。源文中的其他宫位、星系、财富或事件结果没有迁入事业宫规则。有限8段审查不等于穷尽文献。

## Exact commands

Run from repository root:

```bash
python -m pip install --upgrade pytest
PYTHONPATH="$PWD" python -m pytest -q tests/test_knowledge_career_fire_bell_source_evidence.py
PYTHONPATH="$PWD" python -m pytest -q
node --check tools/iztro_export.mjs
PYTHONPATH="$PWD" python src/audit_repository.py --fail-on-p0 > /workspace/scratch/180b896fb3e5/audit352.json
python tools/validate_governance.py --base-ref origin/main --head-branch knowledge/352-fire-bell-source-evidence
git diff --check origin/main
git diff --exit-code origin/main -- product src .github sources validation/wp05 knowledge/wp07a/CAREER_CONTEXT_MAP_CA01_035_043_045_v0.1.json
```

Results:
- Targeted: 14 passed / 0 failed / 0 skipped.
- Full pytest: 639 passed / 0 failed / 0 skipped.
- JS syntax / P0 audit / Knowledge governance / diff checks: PASS.
- P0=0; 907 existing P1 review candidates retained.
- Product/engine/Go/B02 regression: NOT_REQUIRED; no corresponding code or algorithm change, not run and not claimed.
- GitHub Actions: NOT_USED.
- Durable generated report: this file. Full P0 output is reproducible temporary evidence; existing907候选不重复提交。

## Snapshot / limitations

固定提交快照通过connector读取，并逐文件核对Git blob SHA；origin/main为对应本地验证基线。合入前逐个核对远端PR更改文件与本地内容哈希，基线外其他blob保持不变。

确定性测试保障来源ID、附件哈希、PDF/印刷页锚点、局部量词分离、原目标字段及非生产状态；原文意义经直接视觉核对，测试不替代语言解释审查。没有批准新的默认量词、schema、原子、概率或理论本体，也没有新增可执行规则。本工作既不证明现实预测有效性，也不证明所有文献都无法定解。进一步解释冻结须有明确适用证据或另行中文PI报告。

执行更正：建立隔离验证副本后，一次命令误从父级scratch目录启动pytest，递归收集临时副本而产生160个导入／重复模块收集错误（exit2）；这是错误工作目录，不是本批断言失败。已改为从repo352final仓库根运行同一完整命令，639 passed／0 failed／0 skipped；未改测试断言或产品代码。期间主线合入#353，最终基线更新到9116579并重新验证。
