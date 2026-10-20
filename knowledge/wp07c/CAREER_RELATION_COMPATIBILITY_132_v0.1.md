# Career Relation Compatibility — 132 条

Status: **132/132 CANONICALIZED — NO EXECUTION UNLOCK**  
Issue: #430

## 1. 全量结果

此前 Response-era blocker map 中共有 **132 条** RELATION_SCOPE_SEMANTICS residual。

本轮全部完成 relation canonicalization：

| 分类 | 数量 | 含义 |
|---|---:|---|
| R1 — canonical relation/scope 已可表示 | **105** | 关系可以直接落入来源已定义的精确 geometry 或 scope operator |
| R2 — generic meeting 已压缩但 geometry 未定 | **26** | “会 / 同会 / 会合”统一为 MEETING_GENERIC，不再拆成多个平级 primitive |
| R3 — source recheck | **1** | CA06-549“天府见火铃照射”中“照射”尚不足以冻结 geometry |

因此当前关系层的主要问题已经从“每个词到底是不是一种新关系”，转成“少量 canonical geometry / scope 已知后，具体 object/group 怎样绑定”。

## 2. 压缩效果

原 132 条中共抓取到 **157 个 relation marker**。旧抽取里，同会 / 会合有时又重复抓出内部单字“会”。本轮去掉 **12 个嵌套重复 marker**，得到 **145 个 relation atom**。

当前实际出现的 surface relation 只有 9 种：同度 58、见 54、同会 14、会 10（去除嵌套重复后）、相对 3、会合 2、朝拱 2、三方 1、照射 1。

它们被压缩成 5 个主要 operator family：EXACT_GEOMETRY、FOUR_DIRECTIONS_VISIBILITY、THREE_DIRECTIONS_SCOPE、MEETING_GENERIC、ASPECT_GENERIC。

底层几何只使用 bounded vocabulary：SAME_PALACE、OPPOSITION、TRINE_ASPECT、FLANKING、UNSPECIFIED、UNSPECIFIED_WITHIN_SCOPE。

## 3. 程序表示已经进一步压成 Z_12 位移

十二宫关系可写成相对宫位偏移：

```text
delta = (p_object - p_subject) mod 12
```

因此本批 132 条的 canonical atom 可以直接携带 offset constraint：

- 同度 → {0}
- 相对 / 朝拱 → {6}
- 三方 → {0,4,8}
- 见 → {0,4,6,8}
- 会 / 同会 / 会合 → UNKNOWN（来源未指定时不猜）

这样 relation 层不必继续膨胀成大量中文枚举，后面真正复杂的部分只剩 group/member binding 和上下文 activation。

## 4. 最关键的压缩

### 见

根据中州派术语定义，“见”是三方四正范围的统称。因此见(X)不再成为一种独立空间几何，而是限定在 SAME_PALACE / TRINE_ASPECT / OPPOSITION 三类 canonical geometry 中。这一个变化就覆盖了 54 个 surface marker。

### 会 / 同会 / 会合

这三个词不再各建一个 runtime geometry，统一为 MEETING_GENERIC，geometry 保持 UNSPECIFIED。其中同会的“同”若表达多对象共同出现，可由 clause composition 层保留 jointness，而不是创造新的宫位几何。

### 朝拱

普通 relation surface：朝拱 → OPPOSITION，因为初级讲义明确说明拱照有时又称朝拱。但命名结构如“百官朝拱”不会因此被扁平化为一个普通 opposition edge。

## 5. R1 的 105 条意味着什么

这 105 条不是“规则已可执行”。它们只是说明：这条规则不再需要为关系词本身发明新 ontology primitive。

例如 A 与 B 同度，现在可以稳定表示为 geometry(A,B)=SAME_PALACE；但如果 B 是火铃、昌曲、煞曜，仍可能继续有 contextual activation、open category、group-member binding 等其他 blocker。

所以本轮仍然 source_resolution_change=0、condition_compiled=0、execution_unlocked=0。

## 6. 下一步关系层真正要处理什么

经过这次压缩，Relation workstream 后续不再需要围绕十几个中文关系词扩 ontology。真正剩下的是 binding：relation(subject, object/member/group, canonical_geometry_or_scope)。

例如“七杀得辅弼魁钺三台八座朝拱同会”，真正困难的已经不是“朝拱是什么词”，而是哪些成员分别处于对宫 / 三合 / 其他会合范围，三台八座的 pair requirement 如何绑定，以及辅弼 / 魁钺的 contextual activation 如何与 relation 结合。

这比继续细分中文词汇更接近未来 compiler 所需的数据结构。

## 7. 边界

- source surface 全部保留；
- source truth 不重写；
- named pattern 不扁平化；
- meeting generic 不虚构 geometry；
- Product runtime 不改；
- 0 条自动解锁；
- 不引入数值权重或概率。
