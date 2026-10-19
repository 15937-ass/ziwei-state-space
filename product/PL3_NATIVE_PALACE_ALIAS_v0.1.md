# Pinned engine palace-label compatibility v0.1

Product input compatibility — Issue #342; not a Knowledge ontology change.

| Engine | Version | Adapter | Observed label | Existing canonical identity |
|---|---|---|---|---|
| iztro-js | 2.6.1 | 0.2 | 仆役 | P08 / 交友宫 |
| x-iztro-rust | 0.6.1 | 0.2 | 仆役 | P08 / 交友宫 |

The mapping is an explicit Product transport alias in `palace_structure.py`.
It is activated only by the exact engine/version/adapter tuple above. Engine
metadata declares compatibility; it does not authenticate the source. The
existing deterministic suffix handling also accepts 仆役宫. Unknown engines,
versions or labels are not guessed. The caller's explicit `extra_aliases` hook
remains available but may not conflict with the ontology or transport mapping.

All three current resolver consumers (domain provider, natal profile and Wealth
pilot) see the same binding. `ResolvedPalace.observed_name` and `raw` preserve
the original label/input. Stars, branches, transformations and relation facts
are unchanged. The separate temporal adapter keeps raw scope labels unchanged;
this is not new temporal rule content or temporal alias normalization.

## 中文研究边界

这里处理的是排盘软件标签与既有宫位编号的衔接。P08 的中州派语义仍来自原有
`knowledge/wp05/palace_ontology_v0.1.csv`，没有扩大为“所有朋友”，没有修改
兄弟宫、子女宫与交友宫之间的边界。输入原文仍可追溯，不用改名后的盘冒充原盘。

内部批量验收使用仓库既有合成回归输入，不使用历史私人命例。接口跑通只说明
输入、宫位绑定、已执行本命规则与证据报告能衔接；当前生产时间反应规则库仍空，
始终返回 `PARTIAL_TEMPORAL_REGISTRY_EMPTY`。不声称能预测具体事件或已有实证准确率。

验证命令及完整结果见 `validation/product/issue_342_native_alias/EXECUTION_EVIDENCE.md`。
