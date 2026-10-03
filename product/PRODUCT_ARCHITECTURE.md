# Product Architecture v0.1

状态：IMPLEMENTATION DESIGN  
不改变 G1-G6 / A0-A2-R1 已冻结领域理论。

## 1. 设计原则

产品层把现有研究资产串接起来，但不让产品便利性反向污染 canonical knowledge。

核心分层：

```text
Input
 -> Deterministic Chart Layer
 -> Normalized Chart Snapshot
 -> Domain State Layer
 -> Evidence-First Inference
 -> Confidence / Conflict Layer
 -> EvidencePackage
 -> Language Model Verbalizer
 -> UI
```

LLM 不负责排盘，不直接访问未筛选的全文后自由选择断语。

## 2. Deterministic Chart Layer

接口目标：

```python
ChartAdapter.render(birth_input, config) -> NormalizedChartSnapshot
```

至少实现：
- internal adapter；
- iztro adapter/reference export；
- 第二外部引擎 adapter/reference export。

所有 adapter 必须显式携带：
- engine name/version/commit；
- school/config；
- timezone/solar-time policy；
- early/late Zi-hour policy；
- calendar-conversion policy。

## 3. Cross-engine Differential Layer

外部引擎只作为**差异发现器**，不是 ground truth。

```text
snapshot A
snapshot B
  -> deterministic diff
  -> mismatch taxonomy
  -> human/source resolution
  -> golden regression case
```

禁止规则：
- 不能多数投票决定流派事实；
- 不能把配置差异标成 bug；
- 未解决差异不得进入“100%准确”宣传。

## 4. Domain State Layer

继续复用当前研究架构：
- L0 structural substrate；
- L1 QI state；
- L2 relational state；
- star core；
- star-system mode；
- modifier operator；
- palace projection；
- typed history memory；
- temporal input。

不在 product layer 新增 primitive qi。

## 5. Evidence-First Inference

每个结论必须通过结构化 trace 形成：

```text
chart fact
 -> matched rule(s)
 -> state/mode/operator transition
 -> palace/context projection
 -> candidate semantic conclusion
```

每一步保留 rule id / source pointer / review status。

## 6. EvidencePackage

LLM 输入只允许来自 EvidencePackage 的已解析内容，包括：

- question/context；
- normalized chart facts；
- active rule IDs；
- latent-state deltas；
- active star-system modes；
- temporal/history conditions；
- palace projections；
- conflicts；
- alternative interpretations；
- evidence status；
- confidence band。

LLM 可以：
- 重组；
- 解释；
- 压缩；
- 根据用户水平切换表达。

LLM 不可以：
- 生成不存在的 rule id；
- 将 LOW/CONFLICTED 说成确定结论；
- 把 case-support-only 升格为 general rule；
- 隐藏关键冲突。

## 7. 三层解释 UI

### Level 1 — 普通用户
结论 + 核心原因 + 不确定性。

### Level 2 — 高级用户
原局本质、星系、四化/辅煞、宫位、时序、反事实条件。

### Level 3 — Expert/Debug
rule ID、source location、operator、target、conflicts、review status、engine version。

## 8. Contrastive Explanation

系统应支持：

> 为什么是 A，而不是 B？

实现上要求至少返回：
- 支持 A 的证据；
- 反对/削弱 A 的证据；
- 支持 B 的证据；
- B 尚未满足的 gate；
- 哪个新增条件会使 A/B 翻转。

## 9. 最小 MVP 范围

第一版不要同时覆盖所有人生主题。

MVP：
- 本命；
- 一个大限；
- 一个流年；
- 事业 + 财帛；
- 只消费 SOURCE_SPAN_VERIFIED 或明确允许等级的规则；
- 输出完整 EvidencePackage；
- LLM verbalizer 可替换。

MVP 通过后，再扩到关系、健康、迁移等主题。
