# PL3-T Temporal EvidencePackage Integration v0.1

状态：**IMPLEMENTED — LAYERED EVIDENCE CONTRACT READY**

## 1. 目的

把 `NatalStateProfile` 与 `TemporalEnvironmentProfile` 接入一个明确分层的 EvidencePackage vNext，同时不破坏现有 legacy `EvidencePackage`。

新包使用四个永久 namespace：

~~~text
CANONICAL
TEMPORAL
PERSONAL
EMPIRICAL
~~~

PL3-T 阶段只允许填充 CANONICAL + TEMPORAL。

## 2. Canonical namespace

保存：

- natal_profile_id；
- knowledge_version；
- canonical facts；
- named structures；
- active natal domain rule ids。

它仍然是 feedback-independent。

## 3. Temporal namespace

保存：

- temporal_profile_id；
- natal_profile_id；
- target_label；
- active temporal layers；
- raw TemporalFact provenance；
- matched TemporalReactionEvidence；
- approved event-relative context；
- temporal conflicts；
- external_event_trigger_used。

这里的内容仍是 environment / activation evidence，不是 outcome truth。

## 4. PERSONAL / EMPIRICAL 硬边界

v0.1 明确要求：

~~~text
personal == {}
empirical == {}
~~~

如果 PL3-T 调用试图提前写入个人现实状态或经验概率，constructor 直接拒绝。

PERSONAL 由 PL3-S owner；EMPIRICAL 由 PL5 owner。

## 5. Legacy compatibility

现有 `EvidencePackage` 不修改，避免打断 PL2/PL3-N 已有 runtime。

如果调用方已经有 legacy symbolic package，可通过 `legacy_symbolic` 原样携带；但 knowledge_version 必须与 NatalStateProfile 一致。

## 6. Version lock

必须满足：

~~~text
canonical.natal_profile_id == temporal.natal_profile_id
canonical.knowledge_version == temporal.knowledge_version
~~~

跨版本混装直接 fail closed。

## 7. LLM 边界

LLM 只允许 verbalize 已经存在于 namespace 中的证据。

它不能：

- 把 temporal environment 改写为确定事件；
- 从空 EMPIRICAL namespace 自己生成概率；
- 从空 PERSONAL namespace假设用户现实状态；
- 修改 CANONICAL rule truth。

## 8. PL3-T 阶段收口

完成本 work unit 后，PL3-T 的产品骨架已经具备：

~~~text
validated temporal assets
-> TemporalEnvironmentProfile
-> source-gated reaction compiler
-> approved event-relative overlay
-> deterministic temporal fixtures
-> layered EvidencePackage
~~~

生产 reaction registry 仍等待知识侧 KB-WP07B structured normalization；这不应阻塞下一阶段 PL3-S。

## 9. 下一步

**PRODUCT_PL3S_ACQUIRED_STATE_SCHEMA_V0_1**

开始建立现实获得性状态 S_t，并继续保持 Natal / Temporal / Personal 三层分离。
