# Relation Semantics v0.1 — 宫位关系语义压缩

Status: **SOURCE-GROUNDED CANONICAL LAYER**  
Issue: #430

## 1. 核心原则

关系词不再“一词一个 primitive”。

采用双层表示：

```text
source surface
    ↓ 保留
canonical operator / geometry
```

也就是：

> **压缩语义，不压缩证据。**

同一句原文仍保存“同度 / 见 / 会 / 同会 / 会照 / 朝拱 / 相对 / 夹”等原始词，但程序推演只面对少量 canonical geometry 与 scope operator。

## 2. 来源直接支持的几何骨架

SRC-ZZ-001《中州派紫微斗数初级讲义》的术语定义段直接区分：

- **同度**：星曜同躔一宫；
- **拱照**：星曜见于对宫，并说明“有时又称朝拱”；
- **会照**：星曜见于三合宫；
- **相夹**：两星曜位于本宫的两个邻宫；
- **见**：星曜会合于三方四正的统称；
- **三方**：本宫 + 两个合宫；
- **四正**：三方 + 对宫。

因此程序层真正需要的基础几何只需：

```text
SAME_PALACE
OPPOSITION
TRINE_ASPECT
FLANKING
```

再加两个非几何的 scope/operator：

```text
FOUR_DIRECTIONS_VISIBILITY
THREE_DIRECTIONS_SCOPE
```

以及一个对“会 / 同会 / 会合”的压缩 family：

```text
MEETING_GENERIC
```

## 3. 关键映射

| Surface | Canonical |
|---|---|
| 同度 | SAME_PALACE |
| 拱照 / 朝拱 | OPPOSITION |
| 相对 | OPPOSITION |
| 会照 | TRINE_ASPECT |
| 相夹 / 夹 | FLANKING |
| 见 | FOUR_DIRECTIONS_VISIBILITY |
| 三方 | THREE_DIRECTIONS_SCOPE |
| 会 / 同会 / 会合 | MEETING_GENERIC |

其中“见”不是第五种几何关系。它表示：

```text
SAME_PALACE
OR TRINE_ASPECT
OR OPPOSITION
```

也就是三方四正范围内的 umbrella operator。

“会 / 同会 / 会合”则先压成同一 lexical family；如果目标句没有进一步说明到底是三合、对宫还是其他具体位置，就不制造 geometry。

## 4. 为什么这比“一词一个关系”更合理

如果把“会”“同会”“会合”“会照”“朝拱”等全部建成平级 primitive，程序会把古籍语言习惯误当成不同物理关系。

新的结构是：

```text
词法差异
≠
几何差异
```

真正影响命盘结构的是星曜位于：

- 本宫；
- 对宫；
- 三合宫；
- 邻宫夹持；

以及原文是否只是用一个更宽的“见 / 会”来描述这些关系。

## 5. Named pattern guard

“朝拱”作为普通关系词可以映射到 OPPOSITION，但：

```text
百官朝拱
君臣庆会
府相朝垣
```

这类命名结构仍是 structured pattern。

不能因为里面出现“朝拱 / 会”两个字，就把整个格局降维成一条普通 relation edge。

## 6. 当前没有做的事情

本版本没有：
- 修改 Product runtime；
- 改变任何 source rule 的可执行状态；
- 解决 group activation；
- 解决吉曜/煞曜等开放类别；
- 给“会 / 同会 / 会合”强行指定精确宫位；
- 用概率或数值权重描述关系强弱。

这是 Relation ontology 的 canonicalization layer，不是最终 compiler。
