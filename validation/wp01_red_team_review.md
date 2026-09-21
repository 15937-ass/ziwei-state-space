# WP-01 Red-Team Review — Pilot 100

Reviewer role: A4 (red-team auditor)  
Scope: `knowledge/pilot_rules_100.csv`  
Status: PRE-HUMAN-GATE

## 1. What the pilot established

The first 100 rules can be represented in the current atomic-rule framework without assigning empirical continuous weights.

Corpus slice:
- 紫微：25 rules
- 天机：25 rules
- 太阳：25 rules
- 武曲：25 rules

Source scope:
- 《中州派紫微斗数深造讲义（上）》十四正曜，书页约 5–12.

The sample already contains four modeling patterns needed by the later state-space model:

1. **direct latent-property descriptions** — e.g. 发射、刚烈、聪敏;
2. **modifier operations** — strengthen/weaken/transform-like relations;
3. **context-dependent valence** — e.g. 武曲刚烈在财帛/事业与六亲宫位的评价不同;
4. **state-dependent / nonlinear response** — e.g. 太阳强则需收敛、弱则需发射；运限太阳化禄增益受原局约束.

## 2. Major schema issues discovered

### R1 — `direction = positive/negative` is ambiguous

Current rows sometimes use:
- positive/negative as the direction of change,
- while other rows implicitly use it as favorable/unfavorable valence.

These are not the same concept.

**Recommendation:** replace with two fields:
- `state_change`: increase / decrease / transform / none / nonlinear
- `valence`: favorable / unfavorable / mixed / context_dependent / not_applicable

This is important because Paper 1 explicitly rejects “good/bad” as a primitive state coordinate.

### R2 — Source claim and normalized target are currently fused

Example:
- source says “紫微最喜百官朝拱”;
- pilot normalizes this to target “整体适配性”.

The first part is EXPLICIT; the normalized latent interpretation is a research formalization.

**Recommendation:** separate:
- `epistemic_type_source`
- `formalization_status`

or add:
- `target_mapping_type = literal / normalized / inferred`.

### R3 — Identity statements need a dedicated operator

Rows such as:
- 紫微属阴土,
- 天机属阴木,
- 太阳属阳火,
- 武曲属阴金

are currently represented with `operator=condition`, which is semantically awkward.

**Recommendation:** add `operator=define` or `assert`.

### R4 — Comparison rules need explicit relational operands

A rule such as “武曲化禄 > 廉贞化禄 > 禄存” should not hide its ordering in notes.

**Recommendation:** add optional:
- `lhs`
- `relation`
- `rhs`

or a dedicated comparison-rule table.

### R5 — Context should eventually be controlled, not free text

Current context strings such as:
- `财帛宫或事业宫`
- `命宫父母宫兄弟宫夫妻宫子女宫交友宫`

are human-readable but difficult for deterministic execution.

**Recommendation:** later normalize to structured lists:
```yaml
palace_scope: [财帛宫, 事业宫]
time_scope: [natal]
```

### R6 — Confidence should mean extraction confidence, not truth confidence

The pilot uses `confidence=high` to mean that the source-to-rule extraction is clear.

**Recommendation:** rename to `extraction_confidence`.

It must never be interpreted as confidence that the astrological claim is empirically true.

## 3. Atomicity issues

Two rules should be split or normalized before approval:

- **ZZ-ZW-007**: contains a three-level ordering in one row.
- **ZZ-TY-015**: classifies multiple possible outcomes (清贵/富贵/富而不贵) in one relation.

Several set-valued context rules are acceptable for the pilot but should later use structured scopes rather than duplicated rows.

## 4. Ontology signals found in the pilot

The following **candidate** dimensions recur and deserve evaluation in WP-02:

- 发射 ↔ 收敛
- 刚烈 ↔ 柔和
- 稳定 ↔ 变动
- 聪敏 / 机变
- 领导 / 统御
- 独断 ↔ 可协调
- 孤克 / 关系疏离
- 进取
- 沉实 ↔ 空虚
- 竞争
- 计划延缓
- 空想化
- 名誉 / 贵显 (likely downstream, not primitive)
- 财富性 (likely downstream/contextual, not primitive)

Important: the last two should **not** automatically become primitive qi dimensions.

## 5. Strong evidence for nonlinear representation

The pilot supports retaining a nonlinear/state-dependent model rather than forcing an LTI model:

- 太阳：过强需收敛，过弱需发射，明确存在“中和”要求；
- 武曲：同一“刚烈”性质在财帛/事业宫与六亲宫位呈不同评价；
- 运限太阳化禄：增益受原局命宫强弱约束；
- 武曲见破军：由刚烈进一步转为躁决，体现组合交互项。

These are sufficient to justify a Paper-1 working form such as:

```text
x_(t+1) = F_theta(x_t, u_t, context)
```

rather than assuming a fixed additive operator.

## 6. Audit result

- Source traceability: PASS for all 100 pilot rows at chapter/book-page level.
- School contamination: PASS; only Zhongzhou core text used.
- Arbitrary continuous weights: PASS; none assigned.
- Epistemic separation: PARTIAL; source claim vs normalized target needs schema refinement.
- Atomicity: PARTIAL; 2 clear revisions identified.
- Ready for G1/G2 use: YES, after schema v0.2 proposal.

## 7. Recommended next action

Do **not** expand to 1,000 rules yet.

First:
1. revise Rule Schema to v0.2;
2. normalize these 100 pilot rows under v0.2;
3. derive candidate qi ontology v0.1 from this reviewed sample;
4. submit G2 ontology for human approval.

This avoids propagating schema errors into a large corpus.
