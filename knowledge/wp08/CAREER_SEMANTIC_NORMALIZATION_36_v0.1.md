# Career Semantic Normalization 36 v0.1

Issue: #467  
Status: **36/36 dispositioned — no execution unlock**

## Coverage
- target residuals: **36**
- reviewed: **36**
- remaining generic semantic-normalization residuals: **0**

## Dispositions
- NORMALIZED_COMPOSITE_EXPRESSION: **10**
- SOURCE_SHORTHAND_REMAINS_UNRESOLVED: **4**
- NORMALIZED_TO_OPEN_CATEGORY_OR_VALENCE: **8**
- NORMALIZED_KNOWN_GROUP_PLUS_LITERAL: **4**
- NORMALIZED_EXPLICIT_ATOM_OR_SET: **6**
- NORMALIZED_EXPLICIT_LOGICAL_EXPRESSION: **4**

## New precise blockers
- SOURCE_SHORTHAND_MEMBERSHIP_UNSPECIFIED: **6**
- OPEN_CATEGORY_MEMBER_OR_QUANTIFIER_UNSPECIFIED: **13**
- CARDINALITY_THRESHOLD_UNSPECIFIED: **2**
- TRANSFORMATION_CARRIER_UNSPECIFIED: **1**

## 代表性修复
- CA05-423 `禄存或化禄` → source-local explicit OR；
- CA04-391 `铃星陀罗阴煞华盖天刑` → explicit listed local set；
- CA05-433 `天厨火星` → explicit listed local set；
- CA09-818 `武曲天府` → explicit star pair；
- CA02-147 / CA03-238 等 `见煞` → scoped open malefic category；
- CA09-860 `昌曲化忌` → known group + transformation with carrier unspecified；
- CA06-502 `必须见禄` → necessity 保留，但“禄”的 membership 不擅自补齐。

## 边界
本轮 source resolution changes=0，conditions compiled=0，execution unlocked=0。
