# PL3-T Temporal Fixture Benchmark Acceptance v0.1

状态：**IMPLEMENTED — CONTRACT REGRESSION READY**

## 1. 目的

PL3-T 在继续进入 EvidencePackage 前，先冻结一组 deterministic contract fixtures。

本 benchmark 验证：

- PL1 normalized temporal asset 能稳定进入 PL3-T；
- 六层 active temporal layers 不丢失；
- approved event-relative overlay 能稳定进入 profile；
- ACTIVE / INACTIVE 边界不漂移；
- repeated run profile_id 稳定；
- production temporal reaction registry 仍为空时，基础 Temporal Environment 不被阻塞。

它**不测试现实预测准确率**。

## 2. v0.1 fixtures

### TF01 — Base Temporal Environment

不带现实 event-relative trigger。

要求六层：DECADE / SMALL_LIMIT / YEAR / MONTH / DAY / HOUR 全部存在，且 `external_event_trigger_used=false`。

### TF02 — Migration Year 2

confirmed distant settlement + year=2 + non-travel。

要求：

- event-relative status = ACTIVE；
- migration palace priority = PRIMARY；
- annual life-palace rotation preserved；
- other-palace rotation preserved；
- `external_event_trigger_used=true`。

### TF03 — Migration Year 4

要求 window 已失活；不得保留 migration PRIMARY routing。

### TF04 — Travel Only

要求 settlement window 不激活。

## 3. Profile identity

v0.1 与 PL3-N fixture policy 一致：暂不硬编码 golden profile_id。

但同 fixture 连续运行必须产生完全相同的 profile_id。

等 TemporalEnvironmentProfile serialization 稳定后再考虑冻结 golden IDs。

## 4. Reaction registry 边界

当前 production `PL3T_TEMPORAL_REACTION_REGISTRY_v0.1.json` 按设计为空，等待 KB-WP07B structured normalization。

因此 benchmark 不伪造 temporal reaction，只测试当前已经可执行的 temporal facts + Human-Gate-approved event-relative overlay。

## 5. 下一步

**PRODUCT_PL3T_TEMPORAL_EVIDENCE_PACKAGE_INTEGRATION_V0_1**

把 PL3-T 输出接入 EvidencePackage 的 TEMPORAL namespace，同时保持 CANONICAL / TEMPORAL / PERSONAL / EMPIRICAL 四类证据的边界。
