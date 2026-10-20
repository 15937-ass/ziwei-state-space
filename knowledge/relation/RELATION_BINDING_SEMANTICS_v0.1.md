# Relation Binding Semantics v0.1

Status: **PROGRAM REPRESENTATION SCHEMA — NO EXECUTION UNLOCK**  
Issue: #436

## 1. 为什么 Relation 之后还需要 Binding

Relation Semantics v0.1 已经把同度、相对、会照、见、夹等 surface 词压缩成 Z_12 宫位几何或 scope。下一步不再是继续扩关系词，而是回答：

> **这一个 relation clause 到底作用于哪一个 source semantic object？**

例如：

```text
天机与火铃同度
```

关系层已经知道 `同度 -> delta={0}`。但 `火铃` 是一个 shorthand group。Binding 层只建立：

```text
RELATION_CLAIM(
  subject = 天机,
  target = GROUP_SYMBOL(火铃),
  geometry = SAME_PALACE
)
```

它 **不等于**：

```text
火星与天机同宫 AND 铃星与天机同宫
```

后者属于 member realization / contextual activation，必须由来源或后续 response semantics 决定。

所以本层的核心原则是：

```text
relation binding != group activation
```

这一步能避免把 GROUP、Relation、Activation 三个问题再次揉回一个布尔条件。

## 2. Source 与 Program Representation 的边界

来源负责提供：原始短语、星曜/群组/复合结构、宫位关系、局部显式并列与成对要求。

程序层新增的 `NODE / binding_mode / expansion_policy / clause graph` 只是为了忠实保存这些区别。它不是新的斗数断语，不增加吉凶，不决定权重，也不决定概率。

## 3. Target Node

| Node | 用途 | 默认展开 |
|---|---|---|
| ATOMIC / SOURCE_LITERAL | 单星、化曜或旧 token registry 未覆盖的字面对象 | semantic normalization deferred |
| GROUP_SYMBOL | 火铃、昌曲、辅弼、魁钺、空劫、四煞等 shorthand | no member expansion |
| SCOPED_GROUP_SYMBOL | 仅在特定领域有成员定义的 group | no member expansion |
| EXPLICIT_MEMBER_SET | 原文直接写出左辅右弼、文昌文曲 | explicit members local only |
| OPEN_CATEGORY | 吉曜、煞曜、桃花诸曜等未闭合类别 | category expansion deferred |
| NAMED_COMPOSITE | 三台八座、龙池凤阁等具内部结构的复合 | preserve composite integrity |
| STRUCTURED_PATTERN | 百官朝拱等结构格 | never flatten |
| GENERIC_SHORTHAND | 例如“禄马”，不得自动继承“禄马交驰” | no named-composite inheritance |

## 4. Source Expression 优先于旧 token 完整度

当前 GROUP token registry 不是通用紫微语言 tokenizer。某些 condition 中会出现明确的原子对象，例如 `华盖`、`天机`、`武曲天府`、`文曲化忌`，但旧 GROUP 专项没有把它们做成 group token。

这不应该让 Relation Binding 失败。

因此本层允许 `SOURCE_LITERAL_EXPRESSION_NODE`：

```text
source phrase 已知
semantic ontology 尚未正规化
relation binding 先保存
```

它的含义只是“句法/来源目标已经定位”，不是“这个对象的全部语义已经解决”。

## 5. Compound Clause Graph

同一句中多个 relation surface 不再被扁平成无序列表。

典型结构：

```text
武曲天府三方见煞
```

表示为：

```text
THREE_DIRECTIONS_SCOPE
  restricts
FOUR_DIRECTIONS_VISIBILITY(煞)

=> effective delta ∈ {0,4,8}
```

又如：

```text
太阴与天机同度或相对且见吉化吉曜
```

保存为两个 clause：

```text
relation(太阴, 天机) in {delta=0, delta=6}
AND
visibility(吉化吉曜)
```

而不是把 `同度 / 相对 / 见` 三个词当成三个互相独立的条件。

## 6. Positive / Negative Relation

`廉贞入庙不与煞忌同度` 中，NEGATED 修饰的是 `煞忌同度`；
`辰戌七杀无煞见辅佐吉曜` 中，`无煞` 是另一个 absence condition，`见辅佐吉曜` 本身仍是 AFFIRMATIVE。

因此 polarity 必须按 clause 边界绑定，不能简单向左扫描整个句子。

## 7. Structured Pattern Guard

`百官朝拱` 中包含 surface `朝拱`，但它首先是一个 structured pattern。内部“朝拱”不能因为字面命中而自动变成一个 standalone opposition edge。

同理，命名 composite 的内部 pair requirement 也不会被普通 relation binding 拆掉。

## 8. Compiler 方向

未来 condition compiler 可以按以下顺序工作：

```text
source condition
  -> clause graph
  -> target node binding
  -> Z_12 relation constraint
  -> category / membership resolution
  -> activation / interaction
  -> qualitative response
  -> future learned magnitude
```

这样 relation 只负责“在哪儿/以什么 scope 相遇”，group activation 只负责“哪些成员算触发”，二者互不越权。

## 9. 边界

- 不推断 global ANY / ALL；
- 不把 shorthand relation 默认分发给全部成员；
- 不闭合开放类别；
- 不拆平 named composite / structured pattern；
- 不改变 source truth；
- 不编译 Product condition；
- 不增加数值权重与概率。
