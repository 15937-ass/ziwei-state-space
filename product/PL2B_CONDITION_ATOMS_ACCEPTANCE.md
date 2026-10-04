# PL2-B Condition Atom Compiler

状态：IMPLEMENTED

## 本 checkpoint 完成

- typed ConditionAtom；
- stable canonical serialization；
- all_of / any_of / none_of；
- registry compiler；
- RuntimeState fact builder；
- RuleIR 扩展 any/forbidden 条件；
- RuleRuntime deterministic boolean matcher；
- fail-closed unknown atom types；
- 与 PL2-A 简单 condition atom list 向后兼容。

## 为什么不直接批量解析现有 932 条财帛规则

财帛 corpus 已 SOURCE_SPAN_VERIFIED，但原 condition 字段仍包含大量：

- 前述结构；
- 跨宫关系；
- 例外条件；
- 先后次序；
- 路径依赖；
- 多星组合。

若产品层直接做字符串解析，会把 source verification 与 executable normalization 混为一谈。因此 PL2-B 只把“语言”做好，下一 checkpoint 再做小批、可回滚的 wealth pilot atomization，并单独统计：

- executable；
- normalization pending；
- path-dependent hold；
- case/support exclusions；
- conflict candidates。

这保持产品速度，同时不降低现有 provenance 标准。
