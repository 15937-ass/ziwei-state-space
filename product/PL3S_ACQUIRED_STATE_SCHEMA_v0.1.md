# PL3-S AcquiredState Schema v0.1

状态：**IMPLEMENTATION CONTRACT — REALITY STATE ONLY**

## 1. 目的

PL3-S 开始建立现实世界状态 S_t。

Natal Prior N != Temporal Environment E_t != Acquired State S_t。

AcquiredStateProfile 只表示“现实已经发展到哪里”，不属于原局真值，也不属于大限/流年排盘事实。

## 2. v0.1 状态域

固定六类现实状态容器：RELATIONSHIP、CAREER、RESOURCE、RELOCATION、COMMITMENT、EXPOSURE。

这只是产品状态域，不是新增紫微斗数宫位或传统 primitive。

## 3. 输入来源

允许的 provenance 类型：USER_CONFIRMED、STRUCTURED_RECORD、ACTION_LOG、EXPOSURE_LOG、PREVIOUS_STATE。

每个 KNOWN state entry 必须能回指 observation provenance。用户没说、未收集或资料缺失不能自动解释成“没有发生”。

## 4. state / action / intention / exposure 分离

entries 保存当前现实状态。reality_context 单独保存 ACTION、INTENTION、EXPOSURE。

planned action 不等于 actual action；intent 不等于 outcome；exposure 不等于 event。

## 5. 非数值 confidence

v0.1 只允许 CONFIRMED、SUPPORTED、LOW_CONFIDENCE、UNKNOWN，不在本层生成经验概率或个人 posterior。

## 6. Missingness 与 contradiction

schema 预留 missingness 与 contradictions，但 PL3S-01 不自动解决矛盾、不插值缺失状态。正式更新逻辑由 PL3S-02 Deterministic State Updater 负责；缺失/冲突策略在 PL3S-03 进一步冻结。

## 7. Privacy / raw narrative boundary

person_key 必须是产品侧 opaque key，不保存姓名、身份证等直接身份信息。state value 只接受紧凑 JSON-compatible normalized value。长篇 raw narrative 不进入 AcquiredState；原始文本应在独立受控存储中，并通过 provenance ref 关联。

## 8. 永久边界

AcquiredStateProfile 明确禁止修改 NatalStateProfile、修改 TemporalEnvironmentProfile、计算 manifestation probability、输出 outcome prediction、用现实反馈反写 canonical knowledge。

## 9. 确定性

相同 person_key、as_of、normalized entries、reality context、missingness、contradictions、provenance、previous_state_id 必须得到相同 state_id，与输入顺序无关。

## 10. 下一步

**PRODUCT_PL3S_DETERMINISTIC_STATE_UPDATER_V0_1**

把 confirmed observations / actions / exposures 与 previous state 以可审计规则更新成新的 AcquiredStateProfile；不使用黑盒 LLM 状态推断。
