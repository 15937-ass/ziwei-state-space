# Career Residual 28 Final Source Pass — Issue #501

Status: **28 / 28 COMPLETE — ALL 228 BLOCKED CAREER ROWS NOW DEEP-SOURCE-REVIEWED**

本批把 closure v0.12 中尚未进入 #489 / #498 的最后 **28 条** blocked Career contextual-activation rows 全部回到中州派原文重审。

## 覆盖闭合

当前 251 条 contextual-activation rows 中有 23 条无 blocker、228 条仍有 blocker。现在这 228 条形成无重叠分区：#489 100 条 + #498 100 条 + #501 28 条 = **228 / 228**。因此以后 SOURCE_UNDERDETERMINED 不再等同于“尚未查原书”，而是深审后仍需保留的知识边界。

## 两个新修订

### CA04-337
原抽取“武曲得禄权科且见辅佐吉曜”把三个四化写成了不清晰列表。原文实际是武曲以得化禄、化权、化科者为宜，且宜见辅佐吉曜。对同一颗武曲而言，化禄 / 化权 / 化科是互斥 transformation state，因此本句可安全收敛为 source-local alternatives；移除 SOURCE_LIST_QUANTIFIER_UNSPECIFIED，但保留 AUXILIARY_SUPPORT_ACTIVATION_CONTEXTUAL_UNRESOLVED。

### CA05-471
原抽取“廉贞会紫微吉曜百官朝拱”把百官朝拱压成额外必需条件。原文是“廉贞所会的紫微有吉曜，若百官朝拱之类，则宜文职”。其中“百官朝拱之类”是紫微有吉曜的例示/优质 realization，不是要求先定义百官数量阈值才能触发本条。因此移除本条 BAIGUAN_ACTIVATION_NO_UNIVERSAL_THRESHOLD，保留 OPEN_VALENCE_CATEGORY_ACTIVATION_CONTEXTUAL_UNRESOLVED。

## 其余 26 条
其余 26 条经直接回源后继续 fail-closed。主要原因是：吉化/吉曜/吉辅内部激活仍未闭合；“重重”“煞重”“力量微薄”没有数值阈值；“等杂曜”仍是开放尾项；“无煞/无吉曜”仍需要闭世界缺席证据；科文、桃花、辅佐等即使有 scoped membership，也不能自动生成 ANY/ALL/N_OF。

## v0.13
- blocked rows deep-source-reviewed: **228 / 228**
- source-condition repairs: **11 -> 13**
- cumulative source-resolution-changed rows: **43 -> 45**
- new blocker-free rows: **0**
- no-current-blocker rows: **23**
- source-underdetermined rows: **201**
- conditions compiled: **0**
- execution unlocked: **0**

下一阶段不应继续机械重复回源，而应把已确认的 source-local dependency / branch / relation 表达整理成严格 dependency compiler contract，同时让真正 source-underdetermined 的激活规则继续 fail-closed。