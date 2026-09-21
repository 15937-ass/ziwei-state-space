# Structural Observability and Identifiability — Draft 0.1

## 1. Purpose

Paper 1 has no fitted numerical state matrices, so classical LTI observability rank tests are not yet available.

Instead, this project defines a **structural observability audit** for the proposed Zi Wei latent-state ontology:

> A candidate latent variable is structurally observable only if the formalized theory provides at least one path from that variable, through modifiers/system modes/palace projections, to a distinguishable observable or semantic output.

This is a research formalization inspired by observability, not a claim that the traditional theory itself contains control-theory observability concepts.

---

## 2. Graph representation

Construct a directed heterogeneous graph:

### Node classes
- primitive qi dimensions QI;
- relational states QR;
- star cores S;
- star-system states H;
- system modes z;
- modifier operators T;
- palace essences E_p;
- temporal inputs U_t;
- projection domains P_p;
- observable descriptors Y.

### Edge classes
- `supports`: source rule supports latent property;
- `modifies`: modifier changes a dimension/mode;
- `composes`: star -> star-system;
- `interacts`: interaction_delta relation;
- `projects`: latent/system state -> palace output;
- `conditions`: context gates relation;
- `observes`: output descriptor -> measurable/annotatable event.

---

## 3. Structural observability criteria

A latent candidate q passes the Paper-1 structural audit when:

### O1 — Output reachability
At least one directed path exists:

~~~text
q -> ... -> Y
~~~

If no path exists, the state cannot be tested from any defined output and should be removed, merged, or supplied with an observation channel.

### O2 — Distinguishability
For two candidates q_i and q_j, their support/projection/operator signatures must not be identical.

Define a symbolic signature:

~~~text
sig(q) = {
  supporting stars,
  supporting systems,
  modifiers that selectively affect q,
  palace projections,
  output descriptor classes
}
~~~

If:

~~~text
sig(q_i) == sig(q_j)
~~~

under the available corpus, they are structurally indistinguishable and should not both be frozen without further evidence.

### O3 — Differential excitation
There should ideally be at least one context/modifier that affects one candidate differently from a competing candidate.

Example:
- QI-03 稳定—变动 can be activated by temporal 天机/破军 structures;
- QI-04 守成—开创 distinguishes 天府 from 七杀/破军.

This differential response supports keeping the two dimensions separate.

### O4 — Cross-context semantic stability
The meaning of q should remain recognizable across more than one star/system/context.

A variable that only exists in one textual phrase is weakly identifiable.

### O5 — No direct outcome contamination
If q is defined only by a downstream event (“发财”“离婚”“手术”), it fails the latent-state criterion even if observable.

---

## 4. Audit of current G2 ontology

### Strong structural support

The following have multiple independent support paths and distinct operators/projections:

- QI-01 发射—收敛
- QI-02 刚—柔
- QI-03 稳定—变动
- QI-04 守成—开创/冲刺
- QI-05 现实化—空泛
- QI-06 决策激活度
- QI-07 认知机变
- QI-08 行动驱动
- QI-09 欲望驱动
- QI-10 原则/规范约束
- QI-12 资源保存/管理能力
- QI-13 表达/传播能力
- QI-15 缓冲/调和能力
- QR-01 关系整合—孤离
- QR-02 主导—协同
- QR-03 竞争激活
- QR-04 支持资源

These remain provisionally retained.

### Moderate / redundancy-risk support

#### QI-11 感性—理性张力
Status: KEEP PROVISIONAL.

Reason:
- appears strongly in 廉贞 and several star systems;
- may be representable as coupling between desire/affect and normative/cognitive states rather than one primitive coordinate.

Test:
~~~text
QI-11 ?= coupling(QI-09, QI-10, QI-07)
~~~

Do not delete yet.

#### QI-14 遮蔽—显明
Status: KEEP PROVISIONAL, high redundancy risk.

Possible overlap:
- QI-01 发射—收敛;
- QI-13 表达/传播.

Counterexample supporting separation:
- 巨门 can have strong expression capacity while retaining hidden/obscure quality;
- therefore “visible/hidden” is not identical to “expressive capacity”.

Need larger rule corpus before merging.

---

## 5. G4 candidate dimensions

### QI-16-CAND 目标导向性
Structural status: DERIVED / NOT PROMOTED.

Current signature can largely be reconstructed from:
- QI-04 开创/冲刺;
- QI-08 行动驱动;
- star-system mode z.

No clear differential modifier uniquely targets “goal directedness” yet.

Decision:
~~~text
QI-16 remains derived variable
goal_directedness = f(QI-04, QI-08, z_s)
~~~

### QI-17-CAND 持续意志/韧性
Structural status: HIGH-PRIORITY CANDIDATE / NOT YET PROMOTED.

Evidence:
- multiple star systems independently distinguish 坚强/薄弱、坚忍/躁进、刚毅/脆弱;
- not reducible in wording to decision speed or immediate action strength.

But current operator/projection paths are not yet sufficiently explicit.

Decision:
- retain as derived candidate;
- expand rules specifically targeting persistence under adversity before promotion.

---

## 6. Palace-node observability

Because Paper 1 uses 12 local palace essences, observability must be considered at node level.

A local latent state e_p is observable only through:
- its own palace projection P_p;
- graph-linked palace outputs;
- temporal reactions that selectively excite that node.

Important implication:

> Two palace states with identical latent signatures can still be distinguishable if their projection domains differ.

For example the same “变动” latent state projected through:
- 事业宫,
- 田宅宫,
- 夫妻宫

has different observation spaces.

This supports the choice of 12 local palace nodes rather than one global latent vector.

---

## 7. Structural identifiability risks

Even if a state is observable, its parameter may not be identifiable.

Major risks:

### I1 — Product ambiguity
If only a product of two gains is seen:

~~~text
y = alpha * beta * q
~~~

alpha and beta cannot be separately identified without additional conditions.

### I2 — Redundant operators
If two modifiers always co-occur in the dataset, their individual gains cannot be separated.

### I3 — Sparse star-system coverage
Rare systems may have too few cases to estimate system-specific Delta_s.

### I4 — Context confounding
Age, occupation, marriage status and social environment can mimic palace-output differences.

### I5 — Person leakage
Multiple years from one person must not be split across train/test in a way that leaks stable natal structure.

These are Paper-2 system-identification concerns, but Paper 1 should define them in advance.

---

## 8. Proposed future numerical tests

After parameters/data exist:

### Local linearization

~~~text
delta x_(t+1) = A_t delta x_t + B_t delta u_t
delta y_t     = C_t delta x_t
~~~

Then classical/local observability can use:

~~~text
O_t = [C_t; C_t A_t; C_t A_t^2; ...]
~~~

or nonlinear observability tools/Jacobians.

### Parameter identifiability
Use:
- profile likelihood;
- Fisher information / sensitivity rank;
- Bayesian posterior concentration;
- constrained system identification.

No such numerical result is claimed in Paper 1.

---

## 9. G5 recommendation

Freeze the following principles:

1. observability is a property of the proposed latent representation relative to defined outputs, not of “qi” in the abstract;
2. candidate dimensions with no output path must be removed/merged/redefined;
3. structurally indistinguishable dimensions should remain provisional;
4. QI-16 is not promoted;
5. QI-17 remains high-priority candidate but is not promoted;
6. local palace nodes improve structural distinguishability because projections differ by domain;
7. numerical observability/identifiability tests wait for fitted models and data.
