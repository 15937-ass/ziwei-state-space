# Career Response Semantics Compatibility 02 — 第二个 100 条

Status: **COMPATIBILITY CLASSIFICATION COMPLETE — NO EXECUTION UNLOCK**  
Issue: #423  
范围：CA04-383 → CA07-691，共 **100/100** 条；累计 **200/251**。

## 1. 本批结论

| 档位 | 数量 |
|---|---:|
| RS1 — response layer covers known semantics | 22 |
| RS2 — partial response gain | 10 |
| RS0 — no direct response gain | 68 |

这批与第一批相比，最明显的变化不是 group membership，而是 **relation 结构显著增多**。这说明进入 CA04 后半到 CA07 后，很多 blocker 实际已经是“群组 × 空间关系”的联合问题。

## 2. 主要剩余 blocker

| 类型 | 条数 |
|---|---:|
| RELATION_SCOPE_SEMANTICS | 69 |
| CATEGORY_OR_COMPOSITE_LEXICON | 46 |
| INHERITED_ANTECEDENT_GRAPH | 28 |
| CONTEXTUAL_ACTIVATION_SEMANTICS | 27 |
| ABSENCE_SCOPE_OPEN_WORLD | 10 |
| DIGNITY_CARRIER_SEMANTICS | 3 |
| SEVERITY_ORDINAL_SEMANTICS | 2 |
| COMPOSITE_RELATION_BINDING | 1 |
| STRUCTURED_PATTERN_INTEGRATION | 1 |

这些计数允许重叠：一条规则可能同时存在 relation、category 与 inherited blocker。

## 3. 本批新增的可复用认识

### 3.1 局部 operator 与 group 默认必须分离

本批已有 6 条 explicit OR、1 条 explicit simultaneity、2 条 explicit necessity、10 条 explicit negation、9 条 conjunction。它们都可以作为 source-clause operator 保存，但不能反推“某群组默认 OR/ALL”。

尤其 CA05-429“前格同时见火铃”：本句的“同时”足以保存局部 simultaneity / ALL-members hint，但 generic 火铃仍保持 activation = UNSPECIFIED。

### 3.2 原文直接列出成员时，可以保存局部 BOTH

CA05-419 的“左辅右弼”、CA06-582 的“文昌文曲”、CA07-638 的“左辅右弼”都不是模糊简称，而是原文直接列出两个成员。新层可以保存 `EXPLICIT_MEMBER_LIST_BOTH_LOCAL`，但不能据此把 generic “辅弼”“昌曲”永久改成 ALL。

### 3.3 relation 已经成为比 GROUP 更大的实际瓶颈

本批有 **69** 条需要 relation scope。
这意味着下一阶段很可能必须处理“见 / 同度 / 同会 / 会照 / 相对”等关系到底如何绑定 group member、named composite 与宫位，而不能只继续扩充词典。

### 3.4 强弱词仍保持非数值

“煞轻”等 source literal 被保留，但不会转换成 +1 / -1 / 0.3 等数字。它只能进入未来 severity / ordinal ontology。

## 4. 累计 200/251 后的趋势

前两批合计：

- RS1 = 40
- RS2 = 27
- RS0 = 133

说明约三分之一记录从 Response Semantics 获得了某种结构表达收益，但**没有任何一条因为本兼容性工作自动获得 Product execution**。

从两批叠加标签看，最持续的四类问题已经非常稳定：

- category/open lexicon；
- relation scope；
- inherited antecedent；
- contextual activation。

剩余 51 条完成后，就可以用全量 251 的数据决定下一 ontology workstream，而不再凭经验排序。

## 5. 边界

source resolution change = 0；condition compiled = 0；execution unlocked = 0；Product change = 0；numeric weight / probability = 0。
