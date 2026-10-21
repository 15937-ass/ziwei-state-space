# Response Semantics Product Adapter v0.1

Status: **IMPLEMENTED IN PRODUCT #462 — VALIDATION PENDING**

## 1. Purpose

本层是 Product v0.4 的 Knowledge -> Product 安全边界。

它负责把 Knowledge 已经审核完成的 Response Semantics 带入 Product，同时把两件事彻底拆开：

~~~text
语义可以表达
!=
允许产生 runtime effect
~~~

本版本不生成 ResponseProfile τ，不编译 N + E，不新增中州派规则。

## 2. Input baseline

当前消费的 Knowledge 输入包括：

- Response Semantics schema / pilot；
- Career Response Compatibility 251/251；
- Relation Binding 132/132；
- Open Category review 59 occurrences；
- Contextual Activation closure v0.3 251/251；
- Career Ordinal/Constraint registry v0.1（130 normalized constraints）；
- #458 source recheck 后的 antecedent closure：
  - unresolved antecedent refs = 0；
  - explicit antecedent dependency rows = 64。

所有 Knowledge 文件为只读输入。

## 3. ResponseSemanticEnvelope

每个 Knowledge ResponseSemanticsRecord 原样保留：

~~~text
record_id / term / semantic_role
members
scope
activation
relation_constraints
interaction
ordinal_constraints
effect_targets
provenance
epistemic_status
Knowledge execution_status
~~~

Product 只增加：

~~~text
allowed_use
runtime_effect_allowed
authorization_ref
blockers
~~~

## 4. Fail-closed execution mapping

默认：

~~~text
LEXICAL_ONLY    -> SEMANTIC_ONLY
STRUCTURAL_ONLY -> SEMANTIC_ONLY
BLOCKED         -> BLOCKED
SAFE_SYMBOLIC   -> SEMANTIC_ONLY
~~~

即使是 SAFE_SYMBOLIC，也必须再有独立、显式的 execution authorization 才能产生 runtime effect。

当前真实 Response pilot 没有这种授权，所以：

~~~text
8 / 8 semantic records preserved
0 / 8 runtime effects authorized
~~~

Synthetic fixture 仅用于验证 positive path，不进入真实语料。

## 5. Authorization cannot override semantics

即使存在 execution authorization，仍不能绕过：

- Knowledge execution status；
- activation UNSPECIFIED；
- local scope binding；
- scope mismatch；
- named composite identity。

例如：

~~~text
禄马交驰
!=
generic 禄马
~~~

命名复合结构不能借 authorization 被扩成 generic shorthand。

## 6. Career readiness gate

251 条 Career Response Compatibility 与最新 251 条 Contextual Activation closure 以 source_rule_id 精确 join。

Product derived decision：

~~~text
LOCAL_STRUCTURE_READY
-> SEMANTIC_ONLY_PENDING_COMPILATION

SOURCE_UNDERDETERMINED
-> BLOCKED_SOURCE_UNDERDETERMINED

DEPENDENCY_COMPILER_GATED
-> BLOCKED_DEPENDENCY_COMPILER

NORMALIZATION_DEFERRED
-> BLOCKED_NORMALIZATION

MULTI_CLASS_BLOCKED
-> BLOCKED_MULTIPLE
~~~

当前实际统计：

~~~text
SEMANTIC_ONLY_PENDING_COMPILATION      17
BLOCKED_SOURCE_UNDERDETERMINED        160
BLOCKED_DEPENDENCY_COMPILER            27
BLOCKED_STRUCTURED_PATTERN_COMPILER      1
BLOCKED_MULTIPLE                       46
-----------------------------------------
TOTAL                                 251
~~~

## 7. Why 17 ready rows still do not execute

Knowledge 的 `LOCAL_STRUCTURE_READY` 只表示当前局部结构语义已经足够明确。

它不表示：

- condition 已编译；
- runtime evidence 已满足；
- execution 已授权。

当前 Knowledge 明确记录：

~~~text
condition_compiled = 0
execution_unlocked = 0
~~~

所以这 17 条在 Product 只进入：

~~~text
SEMANTIC_ONLY_PENDING_COMPILATION
~~~

而不是 executable。

## 8. Relation / category separation

Relation Binding 现在覆盖 132 条 source rules，但：

~~~text
relation binding
!=
member realization
!=
activation
!=
execution
~~~

Open Category review 覆盖 59 个 occurrence，但：

~~~text
membership known
!=
activation quantifier known
~~~

尤其 OPEN_WORLD category 永远不能因为“数据库里没列”就被当成 absent。

## 9. Closed-world absence

涉及“无 / 不见”等 source negation 时：

~~~text
database missing
!=
source-supported absence
~~~

未来 compiler 至少需要显式 closed-world evidence token 才能满足 absence precondition。

v0.1 的 `absence_evidence_ready()` 只检查该前提；即使 evidence ready，也不会自动解除其他 blocker，更不会直接授权 runtime。

## 10. Ordinal / emphasis / severity

在本 work unit 验证期间，Knowledge #461 / PR #463 新增了 Career ordinal/constraint registry。Product 同步最新 main 后把它作为只读输入消费。

当前 registry：

~~~text
normalized constraints = 130
runtime execution unlocked = 0
numericized constraints = 0
transitive closure authorized = 0
~~~

随后 Knowledge #465 / PR #466 又完成了这 130 条 constraint 到 atomic Career rules 的来源约束回链。Product 在最终合并前同步最新 main，并将这两个新 artifact 作为只读审计输入：

~~~text
ordinal constraints dispositioned = 130 / 130
linked atomic rule IDs             = 130
DIRECT_ATOMIC_RULE                 = 114
MULTI_RULE_SHARED_SOURCE_SENTENCE  = 15
METHODOLOGY_OR_CONTEXT_ONLY        = 1

activation rules touched           = 33
NO_BLOCKER_REDUCTION               = 94
QUALITATIVE_REFINEMENT_ONLY        = 36
blockers resolved                  = 0
execution unlocked                 = 0
~~~

这说明 ordinal 信息已经能回到具体 atomic rule 上，但它仍然只补充定性顺序/强调，不能自动补出 activation quantifier、closed-world absence、numeric threshold 或 compiler dependency。

Knowledge 已保存的：

- 尤其；
- 煞轻 / 煞重；
- 吉煞均弱；
- stronger / weaker 等局部关系；

在本 adapter 中保持非数值语义。

禁止自动生成：

- 0–1 weight；
- gain；
- threshold；
- probability；
- confidence score。

## 11. Current readiness

版本化结果：

~~~text
product/RESPONSE_SEMANTICS_ADAPTER_READINESS_v0.1.json
~~~

核心统计：

~~~text
Response pilot total                 8
Career rows                        251
Response gain rows                  89
Semantic-only pending compilation   17
Source-underdetermined             204
Closed-world evidence gated         23
Explicit antecedent dependencies    64
Unresolved antecedent refs           0
Relation-bound rows                132
Category-reviewed rows              59
Career ordinal constraints             130
Ordinal atomic links                    130
Ordinal-linked activation rules          33
Ordinal blocker resolutions               0
Semantic-normalization residuals reviewed 36
Generic normalization blocker after       0
Ordinal runtime unlock                    0
Ordinal numericized constraints           0
Real runtime effects authorized           0
Unauthorized unlock                  0
~~~

## 12. Source-literal normalization refinement

Knowledge #467 / PR #468 在本 Product work unit 最终合并前完成了 36 条 source-literal residual 的正规化，并生成 Contextual Activation closure v0.3。Product 再次同步 latest main，只读消费这一变化。

结果不是“又多了 36 条可执行规则”，而是把一个过于笼统的 blocker：

~~~text
SEMANTIC_NORMALIZATION_OR_QUANTIFIER_UNSPECIFIED
36 -> 0
~~~

拆成更精确、可审计的来源约束：

~~~text
SOURCE_SHORTHAND_MEMBERSHIP_UNSPECIFIED          +6
OPEN_CATEGORY_MEMBER_OR_QUANTIFIER_UNSPECIFIED +13
SOURCE_LIST_QUANTIFIER_UNSPECIFIED               +4
CARDINALITY_THRESHOLD_UNSPECIFIED                +2
TRANSFORMATION_CARRIER_UNSPECIFIED               +2
~~~

36 条的 disposition：

~~~text
NORMALIZED_COMPOSITE_EXPRESSION             10
NORMALIZED_TO_OPEN_CATEGORY_OR_VALENCE       8
NORMALIZED_EXPLICIT_ATOM_OR_SET              6
NORMALIZED_KNOWN_GROUP_PLUS_LITERAL          4
NORMALIZED_EXPLICIT_LOGICAL_EXPRESSION       4
SOURCE_SHORTHAND_REMAINS_UNRESOLVED          4
~~~

关键负结果继续成立：

~~~text
LOCAL_STRUCTURE_READY              17 -> 17
condition compiled                  0
execution unlocked                  0
Product runtime authorized          0
~~~

所以 Product 将 v0.3 视为“语义精度提高”，不是“执行成熟度提高”。

## 13. Architectural meaning

Product 现在第一次可以安全地回答：

> 这条 Knowledge 语义我能不能理解？  
> 如果理解了，我现在有没有权执行？

而不是以前的：

~~~text
能结构化
-> 就尝试执行
~~~

这一步是 PL3-R Response Compiler 的直接前置层。

## 14. Next step

本 adapter 完成后，主线进入：

~~~text
SOURCE_BACKED_RESPONSE_CORPUS_DEPENDENCY
↓
PL3R_DECADE_YEAR_RESPONSE_COMPILER
~~~

Response Compiler 必须只消费 adapter 明确允许的结构，并继续保留 BLOCKED / UNKNOWN / conflict。

本版本完成不代表 ResponseProfile τ 已经可生成。
