# Wang Tingzhi Expert Case Corpus v0.1 — Acceptance

Tracking Issue: #441  
Lane: PRODUCT_ONLY  
Status: **IMPLEMENTED / VALIDATION PENDING**

## 1. Scope

本工作单元把王亭之《安星法与推断实例》中的“推断实例二十四则”结构化为 Product v0.4 Expert Case Bank v0.1，并建立 LOCO-24 split manifest。

本版本只做：
- source-backed case inventory；
- minimal source-demonstrated ExpertReasoningGraph；
- source-explicit procedural MethodPattern；
- blind-safe LOCO split；
- deterministic validation。

本版本不做：
- 机器盲推；
- Case-Based Retrieval ranking；
- Method Policy π；
- method-fidelity score；
- Response Compiler；
- empirical probability；
- predictive-validity claim。

---

## 2. Source-backed inventory

来源目录明确列出 12 个宫位主题、每主题 2 例，共 24 例。

| Seq | Topic | Source label | Source pages |
|---:|---|---|---:|
| 1 | 父母宫 | 谭仪 | 7 |
| 2 | 父母宫 | 某女士 | 7–8 |
| 3 | 命宫 | 诸葛亮 | 8–9 |
| 4 | 命宫 | 某女士 | 9–10 |
| 5 | 兄弟宫 | 曾国藩 | 10–11 |
| 6 | 兄弟宫 | 陈公博 | 11 |
| 7 | 夫妻宫 | 杨森 | 11–12 |
| 8 | 夫妻宫 | 某女士 | 12–13 |
| 9 | 子女宫 | 蒋介石 | 13–14 |
| 10 | 子女宫 | 某男士 | 14 |
| 11 | 财帛宫 | 宋子文 | 14–15 |
| 12 | 财帛宫 | 某男士 | 15–16 |
| 13 | 疾厄宫 | 李纯 | 16–17 |
| 14 | 疾厄宫 | 某女童 | 17–18 |
| 15 | 迁移宫 | 秦桧 | 18 |
| 16 | 迁移宫 | 某女士 | 18–19 |
| 17 | 奴仆宫 | 慈禧 | 19–20 |
| 18 | 奴仆宫 | 某男士 | 20–21 |
| 19 | 官禄宫 | 于右任 | 21 |
| 20 | 官禄宫 | 某男士 | 22 |
| 21 | 田宅宫 | 黄金荣 | 22–23 |
| 22 | 田宅宫 | 某男士 | 23–24 |
| 23 | 福德宫 | 汪精卫 | 24 |
| 24 | 福德宫 | 某男士 | 25 |

重要修正：

> 早期项目讨论曾把“王亭之案例约 10 个”作为非正式估计；本书来源本身明确有“推断实例二十四则”。因此当前 Wang v0.1 corpus 使用 24 例。这里不声称王亭之全部著作合计只有这 24 例。

---

## 3. Why case IDs are deliberately anonymous

命名人物只保存在 Source Inventory 中。

CaseBundle 使用：

~~~text
WANG-CASE-001
WANG-PERSON-001
WANG-BLIND-001
~~~

而不是：

~~~text
诸葛亮
曾国藩
慈禧
……
~~~

原因不是隐私，而是 benchmark leakage。

如果未来让通用 LLM 看到“诸葛亮”“慈禧”“汪精卫”等名字，即使没有打开专家答案，模型也可能从预训练知识中调出历史经历，使所谓 blind replay 失真。

因此 v0.1 明确要求 blind evaluation 不可访问：
- source subject mapping；
- source inventory；
- expert prose；
- ExpertReasoningGraph；
- expert conclusion；
- source outcome；
- external biographical knowledge。

这使未来 LOCO 评测更接近：

> 只给结构资料，看看系统会不会按所学方法推。

---

## 4. CaseBundle maturity

24 个 CaseBundle 全部为：

~~~text
epistemic_status = SOURCE_DEMONSTRATED
allowed_use      = CASE_SUPPORT_ONLY
~~~

任何案例都不是：
- EXECUTABLE canonical rule；
- empirical probability datum；
- Zhongzhou source truth replacement。

### Minimal graph policy

本次没有为了“看起来像专家推理”而补大量隐形步骤。

每例 v0.1 只保存最低限度、来源可支持的三步图：

~~~text
INSPECT
  ↓
CLASSIFY
  ↓
STOP
~~~

含义：
1. source case 明确展示一张盘/目标宫位；
2. source prose 对该目标结构作解释、分类或判断；
3. source case 给出结论/收束。

所有节点均为 SOURCE_DEMONSTRATED。

当前：

~~~text
24 cases × 3 nodes = 72 source-demonstrated nodes
RECONSTRUCTED nodes = 0
~~~

这是刻意保守的。

后续若要细化为：

~~~text
INSPECT
→ CROSS_CHECK
→ COMPARE
→ REFINE decade
→ REFINE year
→ CONFIRM
→ STOP
~~~

必须逐例返回原文做第二轮 source span review，不能因为这种路径“很像王亭之”就自动补全。

---

## 5. Source-explicit method patterns

案例章节之前的“推断要领”本身给出了明确方法，因此本 work unit 另建 SOURCE_EXPLICIT method corpus。

v0.1 收录 6 条：

### WT-METHOD-001
先看父母宫，再看田宅宫，以了解出身与父母荫庇背景。

### WT-METHOD-002
命宫与福德宫同时观察，以同时考虑较实质的人生表现与精神/思想活动。

### WT-METHOD-003
完成前述综合观察后，再按出现的疑点定位相关宫位作交叉检查。

### WT-METHOD-004
由原盘宫位观察继续追查大限、流年，以补充原盘的综合判断。

### WT-METHOD-005
借星安宫时，借入的是所借宫的整组星系，而非只借正曜；三方四正遇到无正曜宫，应先借对宫再合看。

### WT-METHOD-006
“对星”出现不能只按有没有判断，还要比较相对位置；相对位置会影响力量层级。

这 6 条当前统一为：

~~~text
maturity    = SOURCE_EXPLICIT
allowed_use = SEMANTIC_ONLY
~~~

原因：它们已是明确方法知识，但 Method Policy π 尚未实现，因此现在不把 method record 本身直接当 runtime action policy。

---

## 6. LOCO-24

由于本来源确认有 24 个 case，当前 split 从早期设想的“10-fold”调整为：

~~~text
LOCO-24
~~~

每个 fold：

~~~text
1 held-out case / person_group
23 train cases
23 retrieval cases
~~~

并满足：
- 每个 case 恰好 hold out 一次；
- held-out person_group 不得出现在 training/retrieval；
- source subject label 不进入 blind view；
- conclusion/outcome 不进入 available_information；
- fold order deterministic。

当前 24 个 source cases 在本书中各自只有一个 person_group record，因此 v0.1 的 leave-one-person-group-out 数量上等价于 leave-one-case-out。

保留 person_group 约束是为了以后把同一人物在其他王亭之著作中的案例并入时，不发生人物级数据泄漏。

---

## 7. Current corpus layout

~~~text
product/expert_cases/wang_tingzhi/
├─ CASE_SOURCE_INVENTORY_v0.1.json
├─ METHOD_PATTERNS_v0.1.json
├─ LOCO_FOLDS_v0.1.json
└─ cases/
   ├─ wang_case_001.json
   ├─ ...
   └─ wang_case_024.json
~~~

Runtime validation:

~~~text
src/product/expert_case_corpus.py
~~~

Tests:

~~~text
tests/test_product_wang_expert_case_corpus.py
~~~

---

## 8. Acceptance matrix

| Requirement | Status |
|---|---|
| source inventory = 24 cases | PASS |
| 12 palace topics × 2 cases | PASS |
| 24 CaseBundles created | PASS |
| all CaseBundles compile under #431 contract | PENDING CI |
| source labels separated from blind case IDs | PASS |
| historical external biography excluded in blind policy | PASS |
| no CaseBundle executable canonical truth | PASS |
| no probability / learned weight | PASS |
| no hidden/free-form chain-of-thought field | PASS |
| SOURCE_DEMONSTRATED / RECONSTRUCTED distinguishable | PASS; reconstructed=0 |
| source-explicit method corpus created | PASS; 6 patterns |
| LOCO folds = 24 | PASS |
| every case held out once | PENDING CI |
| 23 train/retrieval cases per fold | PENDING CI |
| held-out person-group leakage prevented | PENDING CI |
| Product full regressions | PENDING CI |

---

## 9. Critic / red-team findings

### Finding A — historical-name leakage
**Risk:** named cases can be answered from an LLM's world knowledge rather than learned Ziwei method.

**Resolution:** names live only in source inventory; blind CaseBundle IDs and fold aliases are pseudonymous. External biography and inventory mapping are explicitly excluded resources.

### Finding B — over-reconstructing Wang's reasoning
**Risk:** converting prose into a detailed DAG can tempt the extractor to insert plausible but unstated intermediate steps.

**Resolution:** v0.1 uses a minimal 3-node source-demonstrated graph and zero RECONSTRUCTED nodes. Detailed graph enrichment is deferred to a later source-span review.

### Finding C — treating case outcomes as probabilities
**Risk:** historical/editorially selected cases have severe selection bias.

**Resolution:** outcomes are held out from blind inputs and never used as population probability or empirical calibration.

### Finding D — confusing method teaching with runtime policy
**Risk:** source-explicit method patterns could be treated as already implemented π.

**Resolution:** all six patterns are SEMANTIC_ONLY. Method Policy remains NOT_IMPLEMENTED.

---

## 10. Maturity claim

After this work unit passes CI and merges, the strongest allowed claims are:

~~~text
Wang source inventory       = STRUCTURED
Wang Expert Case Bank       = V0_1 STRUCTURED
source-explicit method KB   = V0_1 STRUCTURED
LOCO split manifest         = READY
case graph detail           = MINIMAL_SOURCE_DEMONSTRATED
machine expert replay       = NOT_RUN
Case-Based Retrieval        = NOT_IMPLEMENTED
Method Policy π             = NOT_IMPLEMENTED
method fidelity             = NOT_VALIDATED
predictive validity         = NOT_VALIDATED
~~~

---

## 11. Next Product work

After merge, the next Product work unit should be:

~~~text
METHOD_POLICY_V0_1_CBR_HEURISTIC_SYMBOLIC
~~~

It should first use:
- six SOURCE_EXPLICIT patterns；
- 23-case retrieval side of each LOCO fold；
- Product canonical verifier；

to generate a blind InferenceTrace for the held-out case.

Only then can Benchmark B begin measuring whether the machine actually learned how Wang Tingzhi organized evidence.
