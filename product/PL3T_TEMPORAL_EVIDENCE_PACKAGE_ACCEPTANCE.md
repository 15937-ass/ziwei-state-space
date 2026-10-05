# PL3-T Temporal EvidencePackage Integration v0.1

状态：**IMPLEMENTED — TEMPORAL NAMESPACE READY**

## 1. 目的

把已经计算完成的 `TemporalEnvironmentProfile` 接入产品 `EvidencePackage`，形成独立的：

`TEMPORAL`

evidence namespace。

这一层只序列化 PL3-T 已有结果，不重新选规则、不推断事件、不计算概率。

## 2. EvidencePackage vNext 边界

产品架构要求最终区分四类证据：

- CANONICAL
- TEMPORAL
- PERSONAL
- EMPIRICAL

本工作单元只实现 TEMPORAL。

现有 canonical/top-level payload 保持兼容，不在本批重构成新的 canonical namespace，以避免破坏 PL2/PL3-N 已运行接口。PERSONAL 与 EMPIRICAL 留给后续阶段。

## 3. TEMPORAL namespace

新增 `TemporalEvidenceNamespace`，保存：

- `profile_id`
- `natal_profile_id`
- `target_label`
- `active_layers`
- `temporal_facts`
- `temporal_reactions`
- `environment_states`
- `event_relative_context`
- `conflicts`
- `external_event_trigger_used`

所有 reaction/source/event-relative provenance 原样保留。

## 4. 禁止越界

TEMPORAL namespace 结构上拒绝：

- probability
- posterior
- outcome
- acquired_state
- personal_state
- empirical_calibration

因此 PL3-T 不会因为接入 EvidencePackage 就偷偷承担 PL3-S、PL3-M 或 PL5 的职责。

## 5. Adapter

新增：

`src/product/temporal_evidence.py`

接口：

- `temporal_profile_to_evidence_namespace(profile)`
- `attach_temporal_profile_to_evidence_package(package, profile)`

后者返回新的 EvidencePackage，不修改原 package。

如果 package 已经声明 `knowledge_version`，必须与 TemporalEnvironmentProfile 完全一致；否则 fail closed。若 package version 为空，则继承 PL3-T profile 的 knowledge version。

## 6. Canonical compatibility

接入 TEMPORAL 后：

- 原 `active_rules` 不变；
- 原 `projections` 不变；
- 原 `chart_facts` 不变；
- temporal evidence 不混入 canonical rule list；
- temporal conflict 不伪装成 canonical conflict；
- source possibility 仍不等于 empirical probability。

## 7. Event-relative evidence

已批准的 `MIGRATION_FIRST_THREE_YEARS` 会作为 TEMPORAL event-relative context 出现。

`external_event_trigger_used=true` 只说明某个 source-explicit temporal window 使用了已确认外部事件触发；它不等于 acquired state、personal posterior 或 outcome truth。

## 8. 测试

新增 `tests/test_product_temporal_evidence.py`，验证：

- profile -> TEMPORAL namespace；
- temporal source trace 保留；
- event-relative routing 保留；
- canonical payload 不被改写；
- package serialization；
- knowledge-version lock；
- forbidden personal/empirical/outcome payload fail closed；
- inactive context 不误标 external trigger。

## 9. PL3-T 阶段结论

至此 PL3-T v0.1 产品主干已具备：

1. TemporalEnvironmentProfile core；
2. validated temporal asset adapter；
3. source-gated Natal × Temporal reaction compiler；
4. approved event-relative window；
5. deterministic temporal fixture benchmark；
6. TEMPORAL EvidencePackage namespace。

Production temporal reaction registry 仍按设计等待 KB-WP07B structured normalization，不阻塞进入下一主阶段。

## 10. 下一步

**PRODUCT_PL3S_ACQUIRED_STATE_SCHEMA_V0_1**

开始 PL3-S Personal State Observer：建立 acquired reality-state 容器，并继续保持 Natal Prior、Temporal Environment、现实状态三者永久分层。
