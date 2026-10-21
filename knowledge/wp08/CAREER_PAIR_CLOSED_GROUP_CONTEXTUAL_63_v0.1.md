# Career Pair / Closed-Group Contextual Activation 63 v0.1

Issue: #477  
Status: **63/63 reviewed; generic ambiguity narrowed; 0 execution unlocks**

## 结论
这一轮把 #475 中 `PAIR_OR_CLOSED_GROUP_CONTEXT` 的 63 条全部复核。核心结论不是“某一组星曜到底统一按 ANY 还是 ALL”，而是相反：中州派原文反复证明 **单星、对星、同时、相夹、同度、或** 都是 source-local 结构，不能把一个简称的成员表直接升级成全局触发量词。

因此：
- 60 条 `MEMBER_QUANTIFIER_UNSPECIFIED` 被细化为 `PAIR_OR_CLOSED_GROUP_ACTIVATION_CONTEXTUAL_UNRESOLVED`；
- 3 条原先误落入 OPEN_CATEGORY 的 `煞曜 / 吉化 / 见煞` 被细化为 `CLOSED_CATEGORY_ACTIVATION_CONTEXTUAL_UNRESOLVED`；
- blocker cleared = 0；execution unlocked = 0。

## 高频 family contract
- 空劫: 21 条；成员=地空、地劫；activation=CONTEXTUAL_UNRESOLVED
- 昌曲: 18 条；成员=文昌、文曲；activation=CONTEXTUAL_UNRESOLVED
- 火铃: 17 条；成员=火星、铃星；activation=CONTEXTUAL_UNRESOLVED
- 魁钺: 9 条；成员=天魁、天钺；activation=CONTEXTUAL_UNRESOLVED
- 辅弼: 7 条；成员=左辅、右弼；activation=CONTEXTUAL_UNRESOLVED
- 煞曜/煞: 4 条；成员=擎羊、陀罗、火星、铃星、地空、地劫；activation=CONTEXTUAL_UNRESOLVED
- 三台八座: 2 条；成员=三台、八座；activation=CONTEXTUAL_UNRESOLVED_OUTSIDE_STATED_STATUS_EFFECT
- 四煞: 2 条；成员=擎羊、陀罗、火星、铃星；activation=CONTEXTUAL_UNRESOLVED
- 吉化: 2 条；成员=化禄、化权、化科；activation=CONTEXTUAL_UNRESOLVED
- 羊陀: 1 条；成员=擎羊、陀罗；activation=CONTEXTUAL_UNRESOLVED

## 来源支持的关键区别
- 昌曲：来源能明确写“文昌文曲同时聚于垣内”，也能另写“昌曲对星”；因此 BOTH 只能在这些明确局部表达中成立。
- 辅弼：来源明确区分“对星”与“单星”，而且单星另有自己的论断。
- 魁钺：来源一方面说成对会合始发生主要作用，另一方面紧接着讨论单星状态，说明不能把所有简称机械改写为 ALL。
- 火铃：既有专门审查已同时发现 explicit OR 与 BOTH/夹结构；事业宫“火铃同度”自身仍没有内部量词明示。
- 空劫：地空、地劫身份可闭合；来源也会特地写“空劫二星同度”，所以未写“二星”的普通空劫句不能自动套用 BOTH。
- 三台八座：对“增高地位”有明确“必须成对会照”证据；但七杀事业宫复合句还同时含辅弼、魁钺，不能把这一局部 pair rule 扩散成整个列表的共享量词。

## Closure v0.6
- MEMBER_QUANTIFIER_UNSPECIFIED: 93 -> 33
- OPEN_CATEGORY_MEMBER_OR_QUANTIFIER_UNSPECIFIED: 132 -> 129
- PAIR_OR_CLOSED_GROUP_ACTIVATION_CONTEXTUAL_UNRESOLVED: 60
- CLOSED_CATEGORY_ACTIVATION_CONTEXTUAL_UNRESOLVED: 3
- rows with no current activation blocker: 18
- Product runtime changes: 0

这次减少的是**模糊 blocker**，不是减少事实上的不确定性：我们现在知道“不确定的究竟是成员还是局部触发语法”，后续可以按 family/context 精确推进。
