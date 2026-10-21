# Career Residual Classification 100 v0.1

Issue: #475  
Status: **100/100 classified — no blocker clear, no execution unlock**

## 本轮范围
从 Career closure v0.5 中取出全部 **93 条 `MEMBER_QUANTIFIER_UNSPECIFIED`**，再按原顺序补入 **7 条仅含 `OPEN_CATEGORY_MEMBER_OR_QUANTIFIER_UNSPECIFIED` 的规则**，组成新的 100 条研究批次。

这一步不是为了把 100 条强行解释成 ANY / ALL / N_OF，而是把“下一步究竟该查什么”正规化。

## 分类结果
- CLOSED_WORLD_NEGATION_GATED: **11**
- SOURCE_LOCAL_QUANTIFIER_CANDIDATE: **14**
- NAMED_GROUP_RELATION_REVIEW: **57**
- COMPOUND_OR_DEPENDENCY_GATED: **7**
- OPEN_CATEGORY_NO_UNIVERSAL_RULE_CANDIDATE: **7**
- SOURCE_RECHECK_REQUIRED: **4**

可直接进入后续 source-local / named-group corpus 研究的规则：**75**。
主要受 negation / antecedent 结构门控的规则：**18**。
初步属于开放类别、倾向 NO_UNIVERSAL_RULE 的规则：**7**。

## 高频语义面
- 空劫: 29
- 昌曲: 21
- 火铃: 18
- 辅弼: 11
- 吉曜: 9
- 魁钺: 9
- 辅佐: 8
- 得禄: 7
- 桃花: 5
- 科文诸曜: 5
- 刑耗: 4
- 辅佐吉曜: 4
- 三台八座: 3
- 四煞: 3
- 煞曜: 3

最明显的集中簇是空劫、昌曲、火铃、辅弼、魁钺等 pair/group shorthand。它们并不能用一个统一量词解决。来源中已经明确存在“对星/单星”的区别：同一部讲义会明确写“见齐对星始吉，见单星者……”；也会直接写“必须见辅佐对星”，以及“见辅佐单星”“见昌曲对星”。因此下一步应做 **source-local contextual quantifier**，而不是创造一个全局 pair=ALL 或 pair=ANY 规则。

## 下一研究顺序
1. `PAIR_SHORTHAND_CONTEXT`：空劫、昌曲、火铃、辅弼、魁钺等，系统收集对星/单星/同度/会照语句。
2. `LU_SHORTHAND_CONTEXT`：得禄、禄马及早期压缩出的禄类简称，恢复 source-local carrier/alternative。
3. `AUXILIARY_SUPPORT_CONTEXT`：辅佐、辅佐诸曜、辅佐吉曜，区分成员集合、成对要求与吉性限定。
4. `OPEN_CATEGORY_CONTEXT`：吉曜、桃花、科文诸曜、刑耗等，只找局部明示，不追求全局封闭。
5. negation / antecedent 继续保持结构门控，待 closed-world 与 dependency compiler 层单独处理。

## 不变边界
- blockers cleared = **0**
- source resolution changes = **0**
- conditions compiled = **0**
- execution unlocked = **0**
- Product runtime changes = **0**
- GitHub Actions used = **0**
