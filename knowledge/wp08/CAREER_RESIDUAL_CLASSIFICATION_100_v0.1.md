# Career Residual Classification 100 v0.1

Issue: #475  
Status: **100/100 classified — no blocker clear, no execution unlock**

## 本轮范围
从 Career closure v0.5 中取出全部 **93 条 `MEMBER_QUANTIFIER_UNSPECIFIED`**，再按原顺序补入 **7 条仅含 `OPEN_CATEGORY_MEMBER_OR_QUANTIFIER_UNSPECIFIED` 的规则**，组成新的 100 条研究批次。分类时同时读取现有 Category Open Lexicon，避免把已经闭合的 `煞曜/煞/吉化/辅佐诸曜/辅佐吉曜/羊陀` 再误判为开放类别。

## 分类结果
- CLOSED_WORLD_NEGATION_GATED: **11**
- SOURCE_LOCAL_QUANTIFIER_CANDIDATE: **14**
- NAMED_GROUP_RELATION_REVIEW: **60**
- COMPOUND_OR_DEPENDENCY_GATED: **7**
- OPEN_CATEGORY_NO_UNIVERSAL_RULE_CANDIDATE: **4**
- SOURCE_RECHECK_REQUIRED: **4**

可进入 source-local / named-group / direct source recheck 的规则：**78**。
主要受 negation / antecedent 结构门控的规则：**18**。
当前真正倾向 open / NO_UNIVERSAL_RULE 的规则：**4**。

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

最明显的集中簇仍是空劫、昌曲、火铃、辅弼、魁钺等 pair/group shorthand。来源中明确存在“对星/单星”的区别：同一部讲义会写“见齐对星始吉，见单星者……”，也会直接写“必须见辅佐对星”，以及“见辅佐单星”“见昌曲对星”。因此这些 100 条不能靠一个全局 pair=ALL 或 pair=ANY 解决。

同时，本轮发现一个很重要的知识工程现象：closure 中的 `OPEN_CATEGORY...` blocker 并不总意味着成员真的开放。例如 `煞曜`、`煞`、`吉化` 已在现有 canonical lexicon 中闭合；这些规则应进入 named-group/contextual activation 研究，而不是重新打开成员表。

## 下一研究顺序
1. `PAIR_OR_CLOSED_GROUP_CONTEXT`：空劫、昌曲、火铃、辅弼、魁钺，以及已闭合的煞曜/吉化等，研究 source-local member realization。
2. `LU_SHORTHAND_CONTEXT`：得禄、禄马及禄类简称，恢复 source-local carrier/alternative。
3. `AUXILIARY_SUPPORT_CONTEXT`：辅佐、辅佐诸曜、辅佐吉曜，区分成员集合、成对要求与吉性限定。
4. `OPEN_CATEGORY_CONTEXT`：科文诸曜、刑曜、煞刑耗等真正开放/复合表述，只找局部明示，不追求全局封闭。
5. negation / antecedent 继续保持结构门控，待 closed-world 与 dependency compiler 层单独处理。

## 不变边界
- blockers cleared = **0**
- source resolution changes = **0**
- conditions compiled = **0**
- execution unlocked = **0**
- Product runtime changes = **0**
- GitHub Actions used = **0**
