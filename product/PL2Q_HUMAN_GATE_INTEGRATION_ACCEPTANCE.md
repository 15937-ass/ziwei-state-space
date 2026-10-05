# PL2-Q Human Gate Integration Acceptance v0.1

状态：**IMPLEMENTED — CONTRACTS READY, W01 PROMOTION DEFERRED**

## 1. 本批实现

本批把已批准的两个 Human Gate 从决议文档落成产品 contract：

- HG_PL2N_PALACE_VALENCE_MODEL
- HG_PL2L_BAIGUAN_STRUCTURE

新增：
- src/product/human_gate_contracts.py
- product/PL2Q_HUMAN_GATE_CONTRACT_REGISTRY_v0.1.json
- product/PL2Q_WEALTH_HUMAN_GATE_REFRESH_v0.1.csv
- tests/test_product_human_gate_contracts.py

## 2. Palace valence / pattern contract

已实现非数值 dataclass contract：

- PatternAssessment
  - status = FORMED / BROKEN / UNFORMED / UNKNOWN
  - scale = LARGE / NOT_LARGE / UNKNOWN
  - integrity_direction = PRESERVED / DEGRADED / TRANSFORMED / UNRESOLVED
  - magnitude_status 固定为 UNIDENTIFIED

- ContextualValence
  - 必须指定 palace / domain / target
  - 只允许 FAVORABLE / UNFAVORABLE / MIXED / UNRESOLVED
  - resolved 状态必须携带 rule evidence

本批没有建立任何：
- universal palace score；
- 吉星加分/煞星扣分；
- 庙旺数值化；
- 人工 effect magnitude。

## 3. BAIGUAN_SUPPORT_PROFILE

v0.1 仅允许紫微 anchor。

profile 可收集：
- 天府、天相；
- 左辅、右弼、天魁、天钺；
- 文昌、文曲、禄存、天马；
- 三台八座、恩光天贵、台辅封诰、龙池凤阁、天福天寿。

三化明确不属于百官 component。

运行时 v0.1 **不会**产生 EXPLICIT_TEMPLATE_MATCH，也不会生成 BAIGUAN STRUCTURE_PRESENT fact。

当前 profile 只返回：
- PARTIAL_SUPPORT
- CONFLICTED
- ABSENT
- UNKNOWN

直到 KNOWLEDGE_BAIGUAN_ACTIVATION_REVIEW 冻结 source-backed activation criterion。

## 4. Quality guard

本批只实现两类源文边界清楚且不需要新阈值的 guard：

- 天府与地空/天空同宫 -> empty-treasury degradation/inactivation evidence；
- 天相受羊陀夹 -> degraded evidence。

没有在本批擅自实现：
- 财荫夹印完整判定；
- 刑忌夹印完整判定；
- 百官总强度；
- 百官成员数量阈值。

## 5. W01 blocker refresh

Human Gate 8 条现在不再是“等待用户批准”，而是进入更精确的后续 blocker：

- W01-016/017/022/023/035：
  Human Gate 已批准表示法，但仍缺 source-backed state/scale/valence producer，因此不自动 executable。

- W01-095/096/098：
  profile 可以实现，但完整百官 activation criterion 仍 deferred，因此不自动 executable。

当前 W01 executable count 保持原状态，不为了覆盖率硬提升。

## 6. Fail-closed 保证

PL2-Q 明确保证：

1. PARTIAL_SUPPORT != 百官朝拱成立；
2. BROKEN != integrity=0；
3. LARGE != GOOD；
4. contextual valence != universal palace score；
5. UNKNOWN 是合法结果；
6. Human Gate approval != W01 auto promotion；
7. empirical probability / LLM judgment 不参与本批 canonical contract。

## 7. 下一步

产品侧下一 work unit：

**PRODUCT_PL3N_NATAL_PRIOR_ENGINE**

但进入 PL3-N 时只消费已经 executable / source-backed 的状态生产器。

并行知识侧应执行：

**KNOWLEDGE_BAIGUAN_ACTIVATION_REVIEW**

以判断是否存在可冻结的 source-backed 百官最小成立模板；若不存在，应正式冻结 NO_UNIVERSAL_THRESHOLD，而不是发明数量门槛。
