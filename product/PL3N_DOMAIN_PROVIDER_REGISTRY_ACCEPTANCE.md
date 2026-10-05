# PL3-N Domain Provider Registry Acceptance v0.1

状态：**IMPLEMENTED — GENERIC NATAL DOMAIN COMPOSITION READY**

## 1. 目标

把 PL3-N 从“财帛专用入口”升级为通用 domain-provider composition。

统一接口：

~~~text
NatalDomainProvider
  -> NatalDomainEvidence
  -> NatalDomainProviderRegistry
  -> NatalStateProfile
~~~

## 2. v0.1 active provider

当前只有：

- wealth / W01 executable-59

career 只登记为 planned provider，不进入 runtime。

原因：
- WP05 事业宫 source corpus 正在收口；
- 尚无与 W01 同级别的 product executable registry；
- 产品侧不得因为 source corpus 已抽取就跳过 normalization/runtime gate。

## 3. Registry invariants

- provider domain_id 必须唯一；
- 所有 provider 共用同一 palace ontology；
- unknown domain fail closed；
- 可以只选择部分 active domains；
- knowledge_version 根据实际 selected domains 生成；
- registry 无 feedback / temporal / empirical probability 接口。

## 4. 价值

从此以后接新宫位不需要复制整套 Natal Prior engine。

每个 domain 只需实现：

1. domain_id；
2. knowledge_version；
3. palace_ontology；
4. build_domain_evidence(snapshot)。

其余：
- domain selection；
- deterministic composition；
- profile identity；
- feedback-free boundary；

由通用 registry 统一处理。

## 5. 下一步

在事业宫 executable registry 尚未准备好之前，产品侧先做：

**PRODUCT_PL3N_NATAL_FIXTURE_BENCHMARK**

目标是为当前 wealth-enabled NatalStateProfile 建立固定 snapshot fixtures、golden profile IDs、active-rule expectations 与 order-invariance regression。

事业宫 corpus closure 后，再单独启动：

**PRODUCT_PL3N_CAREER_READINESS_AUDIT**
