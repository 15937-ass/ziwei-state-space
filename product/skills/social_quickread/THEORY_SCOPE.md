# Social QuickRead Theory Scope v0.1

## Canonical truth

理论真值沿用仓库既有优先级：

1. 已审核、可执行的中州派 canonical rule；
2. 已审核但尚未进入 executable runtime 的中州派资产，只能作为上游 knowledge work 的输入，不能由本 Skill 自行升级；
3. 王亭之中州派资料中的直接 source span；
4. 古籍材料只在已有中州派解释/归属下使用，不由 Product 层自行做新释义。

本 Skill 不负责把 source span 变成 canonical rule。

## Expression-only sources

以下材料只能控制“怎么说”，不能控制“说什么”：

- 《紫微斗数命理师在助人历程上之语言技巧的研究》；
- PI 提供的社交平台简批样本；
- 后续经 PI 接受的 gold style examples。

从《话术研究》吸收的仅包括：平实性叙述、直接而口语化的表达、必要的确认/联结、点到为止、避免长篇术语解释等。不得使用“察言观色后修改事实”“为了取信而圆错”等做法污染命理结论。

## School boundary

v0.1 只允许：

```text
school = ZHONGZHOU
```

钦天、河洛、飞星等资料即使存在于 Project sources，也不得自动进入本 Skill。未来需要 multi-school 时必须走显式 school adapter。

## Natal / temporal boundary

- 人格、外形、身材、长期爱好、人际基本模式、父母基本关系、择偶偏好：原则上消费 NATAL/canonical evidence。
- 某一年状态、近年变化、当前恋爱环境、大限趋势：必须消费 TEMPORAL evidence。
- “已经恋爱/已经分手/已经升学/已经入职”属于现实事件状态，symbolic evidence 只能支持倾向或条件式表达，不能冒充 observation。
