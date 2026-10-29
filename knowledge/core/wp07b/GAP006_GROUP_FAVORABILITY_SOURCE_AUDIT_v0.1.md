# WP07B GAP-006 generic-group / favorability semantics source audit v0.1

Status: `PROPOSAL_AUDIT_ONLY_NOT_EXECUTABLE`

Issue: #922  
Activation main: `25f69fcac2af901f7898ea2fb2899f26ca5b815c`

## Verdict

`SHARED_DESCRIPTIVE_TAXONOMY_ONLY`

WP07B-GAP-006 currently combines several different source phenomena. The reviewed source does **not** support one universal executable "good/bad/support" predicate or one universal group-expansion rule.

The safe shared result is a descriptive taxonomy that reuses the already-approved Response Semantics principle from Proposal #419:

> lexical membership, activation, interaction, relation, qualitative severity, and period evaluation are separate semantic dimensions.

No new executable primitive is created here.

## 1. Group/category reference family

### 吉曜

`吉曜` is a favorable-star category reference, but this audit does not establish a universal closed member list.

The accepted Career category lexicon already treats `吉曜` as open-world. That artifact is Career-scoped. No accepted Property/P10 scoped category lexicon was found, so Career closure must not be copied across palaces.

Disposition: `OPEN_VALENCE_CATEGORY_REFERENCE`.

### 吉化

Existing accepted Career evidence supports a favorable-transformation class with 化禄 / 化权 / 化科, but #922 does not promote that Career-scoped representation into a new cross-palace universal executable group.

Disposition: `SOURCE_SUPPORTED_CATEGORY_REFERENCE_SCOPE_PRESERVED`.

### 煞 / 煞曜

The source tradition explicitly defines 四煞 / 六煞 membership, and Career artifacts use a scoped lexical alias for plain `煞`. However the reviewed Property rows do not themselves define a new P10 category contract or activation cardinality.

Disposition: `CATEGORY_REFERENCE_WITH_MEMBERSHIP_EVIDENCE_BUT_SCOPE_AND_ACTIVATION_SEPARATE`.

### 煞忌 / 吉化吉曜

These are source compounds. Their components may be recognizable, but the internal composition operator and activation cardinality must not be invented.

Disposition: `SOURCE_COMPOUND_CATEGORY_PRESERVE_COMPOSITION`.

## 2. Qualitative severity family

`煞重` is not a group-membership problem. It modifies severity/cardinality qualitatively.

No numeric threshold, count, score, weight, probability, or universal cut-off is supplied by the source.

Disposition: `QUALITATIVE_SEVERITY_MODIFIER_UNSPECIFIED_THRESHOLD`.

## 3. Period-valence / support family

The reviewed phrases include:
- `流年大运良好`;
- `必须大运或流年配合`;
- `年限不佳`;
- `流年及小限吉`.

These phrases evaluate an entire period/context. They do not provide an independent source-defined formula for what makes a period "good", "bad", or "supportive".

Therefore a runtime fact such as `GOOD_PERIOD=true` would be circular unless another source-backed contract independently establishes the criterion.

Disposition:
- `SOURCE_EVALUATED_PERIOD_VALENCE`;
- `SOURCE_EVALUATED_PERIOD_SUPPORT`;
- executable predicate: **HOLD**.

## 4. Why one universal predicate is unsafe

The source itself distinguishes:
- category membership;
- category presence in a clause;
- source compounds;
- qualitative severity;
- configuration-level 吉/凶;
- period-level 良好/不佳;
- contextual support such as 大运或流年配合.

Collapsing all of these into one `FAVORABLE(...)` operator would destroy source structure and could make predicted outcomes feed back into the condition that supposedly predicts them.

## 5. Per-rule dispositions

| Rule | Source surface | Descriptive class | Remaining executable blocker |
|---|---|---|---|
| CA06-580 | 前格流年大运良好 | PERIOD_VALENCE | criterion undefined + multi-layer scope |
| CA06-600 | 必须大运或流年配合 | PERIOD_SUPPORT | support criterion undefined + inherited antecedent + multi-layer scope |
| CA09-867 | 年限不佳 | PERIOD_VALENCE | criterion undefined / circular if inferred from outcome |
| TP01-045 | 前格煞重 | QUALITATIVE_SEVERITY | no numeric/cardinality threshold + parent + DECADE/YEAR scope |
| TP01-049 | 吉曜、吉化 + named stars | CATEGORY_REFERENCES_IN_EXPLICIT_MULTI_COMPONENT_CONDITION | 吉曜 open; activation/cardinality/clause realization unresolved |
| TP02-165 | 流年天同见煞忌 | SOURCE_COMPOUND_CATEGORY | composition + activation unresolved |
| TP02-166 | 流年天同见吉化吉曜 | SOURCE_COMPOUND_CATEGORY | 吉曜 open; activation/cardinality unresolved |
| TP02-175 | 流年及小限吉 + 红鸾天喜 | PERIOD_VALENCE | combined YEAR+SMALL_LIMIT criterion undefined |
| TP03-233 | 落陷化忌见煞 | CATEGORY_REFERENCE | brightness fact + group activation unresolved |
| TP03-248 | 前格见吉 | OPEN_VALENCE_SHORTHAND | case/path antecedent + meaning of 吉 not a member list |
| TP04-355 | 入庙又见吉曜 | OPEN_VALENCE_CATEGORY_REFERENCE | brightness fact + 吉曜 membership/activation unresolved |
| TP04-356 | 落陷见煞 | CATEGORY_REFERENCE | brightness fact + group activation unresolved |

All 12 remain non-executable in this work unit.

## 6. Reconciliation with Proposal #419

Proposal #419 already rejected global ANY and global ALL defaults and established:

- group = membership only;
- activation = independent;
- interaction = independent;
- relation = independent;
- `UNSPECIFIED` is valid and required when source evidence is absent;
- learned magnitude/probability is outside canonical KB.

#922 does not replace that architecture. It classifies GAP-006 into that architecture.

The old `HG-KB-GROUP-QUANTIFIER-01` decision path was superseded by Proposal #419 and is not reopened.

## 7. WP07B gap disposition

`WP07B-GAP-006-GROUP-OR-FAVORABILITY`

New disposition:

`DESCRIPTIVE_TAXONOMY_CLARIFIED_EXECUTABLE_HOLD`

The gap should be understood as four separable blocker families:

1. `CATEGORY_REFERENCE_SCOPE_OR_ACTIVATION`
2. `SOURCE_COMPOUND_CATEGORY`
3. `QUALITATIVE_SEVERITY`
4. `PERIOD_VALENCE_OR_SUPPORT`

This refinement improves blocker ownership and future compiler design, but it does not authorize runtime facts.

## 8. Human Gate

No PI decision is required now.

`HG-WP07B-FAVORABILITY-AND-GROUPS-01` remains `FUTURE_NOT_PENDING`.

A Human Gate becomes mandatory only if a later unit proposes:
- a universal closed `吉曜` / `煞曜` member set beyond already scoped/source-explicit evidence;
- a universal ANY/ALL/N_OF activation default;
- a universal `GOOD_PERIOD` / `BAD_PERIOD` / `SUPPORTIVE_PERIOD` predicate;
- numeric severity, score, probability, weight, or causal semantics;
- Product/runtime authorization.

## 9. Product/runtime boundary

This audit does not:
- modify Product files or temporal registries;
- populate KIB/K_manifest;
- alter canonical KMN/KMM;
- add runtime condition facts;
- infer probability, score, magnitude, frequency, or predictive validity;
- solve closed-world negation (WP07B-GAP-011);
- solve temporal persistence/path semantics (WP07B-GAP-007);
- globalize Career-scoped category membership into Property/P10.

## Conclusion

The useful shared minimum is structural, not predictive:

> **A source may reference a category, compound category, qualitative severity, or evaluated period valence. Those are distinct descriptive objects. Membership never supplies activation; evaluated period valence never becomes a runtime condition unless its criterion is independently source-defined.**
