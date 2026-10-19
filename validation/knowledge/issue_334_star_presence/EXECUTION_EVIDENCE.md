# 事业宫八条星曜条件映射：本地验证证据

Execution runtime: Codex / OpenAI cloud environment
Python: 3.12.14; pytest: 9.1.1; Node: v24.19.0
Base commit: b0e055022484447a94c60b74afedee63b88a74c4
Head commit: 见 PR #335 的 Validation Evidence（避免自引用提交哈希）。

## 验证方法

通过 GitHub connector 获取固定主线快照，逐文件核对 Git blob SHA，最新基线所有文件均通过。执行目录为本地验证副本；`origin/main` 是相同文件快照的本地基线引用，不是联网 clone。空目录树不参与本地 Git 工作树表示。远端提交树在写入后再与已验证文件核对。

## Commands and results

从仓库根目录执行：

```bash
python -m pip install --upgrade pytest
PYTHONPATH="$PWD" python -m pytest -q tests/test_knowledge_career_star_presence_ca01_026_044.py
PYTHONPATH="$PWD" python -m pytest -q
node --check tools/iztro_export.mjs
PYTHONPATH="$PWD" python src/audit_repository.py --fail-on-p0
python tools/validate_governance.py --base-ref origin/main --head-branch knowledge/334-career-star-presence-ca01-026-044
git diff --check origin/main
```

- pip：成功，pytest 9.1.1 已满足。
- 本批针对性测试：15 passed / 0 failed / 0 skipped。
- 最新主线整合后整仓测试：544 passed / 0 failed / 0 skipped。
- JS syntax：PASS。
- P0 audit：PASS；P0=0，既有 P1 review candidates=907，未将其宣称为全部语义审查通过。
- Knowledge lane governance：PASS。
- Product dual-engine/Go regression：NOT_REQUIRED，本批无 Product 代码或排盘算法修改；完整 pytest 覆盖当前已合入的 Product 版本。
- Generated reports：本证据文件；完整 P0 输出为可由上述命令重建的临时报告，不重复提交907条既有候选。

## 来源与红队复核

- 直接核对本轮《深造讲义（下）》附件 PDF 第66–67页，印刷131–134页；本批锚点132–133页。
- 附件 SHA-256：6bddb3cac2e4b4efcf265229cbda22904ab3394aeef832e338ee5939088e5c5c。
- 修复原待审测试路径遗漏 MAP_；补齐八条每个必需星曜缺失以及移到其他11宫的负例。
- 源条件、来源、审核状态、NATAL、CASE_SUPPORT_ONLY=false、history_feedback、投影域/目标/模式与 canonical CSV 逐项一致。
- 原始空劫段开始于132页，修正两条单页锚点；原始来源范围不变。
- 原页“挂空”字形照录；保留“往往”“有时亦主”“一般只宜”的解释边界。

## Known limitations

全部八条均为不可执行知识候选；条件匹配不证明真实排盘结构可达性，不构成经验预测验证。CA01-035 的火铃简写及 CA01-043/045 的前文依赖仍未定解。本批没有改动源行、Product 运行时、生产注册表或概率权重。
