# Career Semantic Normalization 36 v0.1

Issue: #467  
Status: **36/36 dispositioned — no execution unlock**

## Coverage
- target residuals: **36**
- reviewed: **36**
- remaining `SEMANTIC_NORMALIZATION_OR_QUANTIFIER_UNSPECIFIED`: **0**

## Dispositions
- NORMALIZED_COMPOSITE_EXPRESSION: **10**
- SOURCE_SHORTHAND_REMAINS_UNRESOLVED: **4**
- NORMALIZED_TO_OPEN_CATEGORY_OR_VALENCE: **8**
- NORMALIZED_KNOWN_GROUP_PLUS_LITERAL: **4**
- NORMALIZED_EXPLICIT_ATOM_OR_SET: **6**
- NORMALIZED_EXPLICIT_LOGICAL_EXPRESSION: **4**

## Generic → precise blockers
- SOURCE_SHORTHAND_MEMBERSHIP_UNSPECIFIED: **6**
- OPEN_CATEGORY_MEMBER_OR_QUANTIFIER_UNSPECIFIED: **13**
- SOURCE_LIST_QUANTIFIER_UNSPECIFIED: **4**
- CARDINALITY_THRESHOLD_UNSPECIFIED: **2**
- TRANSFORMATION_CARRIER_UNSPECIFIED: **2**

## 代表性变化
- CA05-423 `禄存或化禄`：OR 结构明确；但 `化禄` 的 carrier 仍按既有审查保留 unspecified。
- CA04-391 `铃星陀罗阴煞华盖天刑`：星名全部正规化，但不因“列名”自动发明 ALL，保留 list quantifier blocker。
- CA05-433 `天厨火星`：两颗星从 generic literal 中拆出，但原 source quantifier 仍不强制闭合。
- CA02-147 / CA03-238 等 `见煞`：正规化为 scoped open malefic category，ANY/ALL 继续未知。
- CA09-860 `昌曲化忌`：正规化为 known group + transformation，carrier 继续未知。
- CA06-502 `必须见禄`：necessity 是明确的；“禄”的 membership 仍不擅自补齐。

## 结果解释
本轮没有提高“看起来的执行率”：v0.2 与 v0.3 的 no-current-blocker rows 都是 **17**。真正的进步是把 36 个“笼统未正规化”全部改写成结构化表达或更准确的 source-underdetermination。

source resolution changes=0，conditions compiled=0，execution unlocked=0。
