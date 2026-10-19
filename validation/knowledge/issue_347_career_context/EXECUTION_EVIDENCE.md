# Issue #347：事业宫火铃／前格语境审查验证证据

Execution runtime: Codex / OpenAI cloud environment
Environment: Python 3.12.14; pytest 9.1.1; Node v24.19.0
Base commit: 9fc487192c1e46ffe58144610559e5c73bfb14a2
Head commit: recorded in PR #349 Validation Evidence after publication (avoids self-reference).

## 结果与边界

只审查 CA01-035、CA01-043、CA01-045：两条前文星曜语境恢复，一条火铃组合量词未决；完整可执行结果条件为零。全部顶层 condition=null、executable_registry_entry=false、执行就绪状态为 BLOCKED_。CA01-043 方法限制不等于“不富”；CA01-045 的勉强求变行为前提不能由星曜事实补出。没有新增行为标签、原子类型或生产规则。

来源为本轮《深造讲义（下）》附件 PDF 第67页左栏／印刷133页，视觉核对完成。附件 SHA-256：6bddb3cac2e4b4efcf265229cbda22904ab3394aeef832e338ee5939088e5c5c。canonical 行、#335 历史审查、Product 文件和所有注册表保持不变。

Producer pass 恢复前格指代；critic pass 检查财富否定误读、行为前提遗漏、火铃强行定解、通用标签偷渡语义和 null 转空条件风险；revision 明确两个审查语境均不是完整结果条件。审查条目本身不执行。合成结构只验证条件逻辑，不证明排盘结构的物理可达性或经验预测有效性。

## Exact commands

从仓库根目录执行：

```bash
python -m pip install --upgrade pytest
PYTHONPATH="$PWD" python -m pytest -q tests/test_knowledge_career_context_ca01_035_043_045.py
PYTHONPATH="$PWD" python -m pytest -q
node --check tools/iztro_export.mjs
PYTHONPATH="$PWD" python src/audit_repository.py --fail-on-p0 > /workspace/scratch/180b896fb3e5/audit347_final.json
python tools/validate_governance.py --base-ref origin/main --head-branch knowledge/347-career-context-035-043-045
git diff --check origin/main
git diff --exit-code origin/main -- product src .github
```

Results:
- Targeted pytest: 7 passed / 0 failed / 0 skipped。
- Full pytest after latest-main integration: 588 passed / 0 failed / 0 skipped。
- JS syntax: PASS。
- P0 audit: PASS，P0=0；907 既有 P1 review candidates 保留，不宣称全部语义问题消除。
- Knowledge lane governance / diff / Product-source-workflow unchanged checks: PASS。
- Product dual-engine / Go / B02 regression: NOT_REQUIRED，本批无 Product、排盘、引擎、历法或适配器修改；未执行也未冒称执行。
- GitHub Actions: NOT_USED。
- Generated durable report: 本文件；完整 P0 输出为上述临时文件，可重建，不重复提交907条既有候选。

基线通过 connector 获取固定提交，每个 Git blob SHA 与远端清单核对。`origin/main` 是经过字节验证的本地基线引用，不是联网 clone。首次传输中的额外末尾换行经 blob hash 确认后去除；最终测试后 Product 文件与基线保持字节一致。期间产品侧合入 #346，故从原始79ed544基线重新整合到9fc487并重跑全套；以上588为最终结果。最终远端树与本地验证内容的 blob SHA 在合入前核对。

Known limitations:
- 火铃量词尚无本轮审查段落内的充分证据；不是断言所有中州派文献都无法定解。
- CA01-045 行为条件没有批准的命盘事实表示；星曜语境匹配不能触发困境结果。
- 本批没有新增可执行规则、经验概率或真实世界预测有效性证据。
