# PL3-S AcquiredState Schema v0.1 Acceptance

状态：**IMPLEMENTED — REALITY STATE CONTRACT READY**

## 1. 本批完成

建立独立于 Natal Prior 与 Temporal Environment 的现实状态容器 AcquiredStateProfile。

它覆盖六个产品现实域：RELATIONSHIP / CAREER / RESOURCE / RELOCATION / COMMITMENT / EXPOSURE。

## 2. 关键边界

- KNOWN state 必须有 observation provenance；
- UNKNOWN 不能被当成否定事实；
- action / intention / exposure 与当前 state 分开；
- previous state 只通过 previous_state_id 引用，不自动继承；
- contradiction 与 missingness 有显式容器；
- confidence 暂时只有非数值 ordinal labels；
- 不允许修改 Natal Prior；
- 不允许修改 Temporal Environment；
- 不计算 empirical probability；
- 不输出 outcome prediction。

## 3. Provenance

允许 USER_CONFIRMED / STRUCTURED_RECORD / ACTION_LOG / EXPOSURE_LOG / PREVIOUS_STATE。

所有 state/context 中引用的 observation_ref 必须存在于 profile provenance，引用缺失时 fail closed。

## 4. Privacy

person_key 只允许作为 opaque product key 使用。本 schema 不设置姓名、证件、联系方式字段；长篇 raw narrative 也拒绝进入 normalized state value。

## 5. Determinism

builder 对 entries、context、missingness、contradictions、provenance 做稳定排序。相同规范化输入必须生成相同 state_id。

## 6. 本批不做

不做 deterministic transition update、不自动合并 previous state、不解决 contradiction、不做 missing-value imputation、不做 Bayesian posterior。

## 7. 下一步

**PRODUCT_PL3S_DETERMINISTIC_STATE_UPDATER_V0_1**

用 verified observation / actual action / exposure 对 previous state 做可追踪、确定性的更新；所有 overwrite / preserve / conflict 决策必须可审计。
