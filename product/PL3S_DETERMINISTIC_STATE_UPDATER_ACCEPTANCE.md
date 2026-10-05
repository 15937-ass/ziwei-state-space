# PL3-S Deterministic State Updater v0.1

状态：**IMPLEMENTED — EXPLICIT COMMAND UPDATER**

## 1. 目的

把 previous AcquiredStateProfile 通过明确、可审计的现实更新命令生成下一个 S_t。

Updater 不读取命盘来猜现实状态，也不从自由文本自动抽取状态，不做 Bayesian posterior。

## 2. v0.1 operations

只允许：ADD_ASSERTION、CLOSE_ASSERTION、ADD_ACTION、ADD_CONTEXT、SET_MISSINGNESS、CLEAR_MISSINGNESS、ADD_CONFLICT、CLEAR_CONFLICT。

没有通用 UPDATE/OVERWRITE 指令，避免静默覆盖现实历史。

## 3. Provenance gate

每个 StateUpdateCommand 必须携带 observation_refs。所有 ref 必须已经存在于 previous profile 或本次显式 new_source_observation_ids 中，否则 fail closed。

## 4. 状态变化规则

已有 assertion 默认保留。状态改变需要显式 CLOSE_ASSERTION + ADD_ASSERTION。

若同一 domain/key 出现两个仍 active 且 value 不同的 assertion，必须通过 ADD_CONFLICT 显式声明；Updater 不自动选择谁真谁假。

Action 与 Context v0.1 只追加，不静默改写历史记录。

Missingness 只通过 SET/CLEAR 指令变化。

## 5. 时间边界

next as_of_date 不得早于 previous as_of_date。previous_state_id 自动指向上一快照 state_id。

Updater 不自行计算状态衰减，不因为时间经过就删除 assertion。

## 6. 与传统模型的边界

本层只更新现实 S_t。它不能改 Natal Prior N、Temporal Environment E_t、canonical rule truth，也不产生 manifestation probability。

## 7. 下一步

**PRODUCT_PL3S_MISSINGNESS_CONTRADICTION_MODEL_V0_1**

冻结 missingness / stale evidence / contradiction 的处理策略；依旧保持 UNKNOWN != false，并把 conflict resolution 与概率学习分开。
