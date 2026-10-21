# Property Temporal-Reaction Eligibility Audit v0.1

Status: **COMPLETE — 0/35 eligible under the current PL3-T contract**

## Scope
This is the P10 equivalent of the Career WP07B audit. It covers every canonical non-NATAL Property row after the 358/358 source closure.

- candidates: **35**
- YEAR: **32**
- DECADE: **3**
- reusable: **19**
- CASE_SUPPORT_ONLY: **16**
- eligible for current compiler: **0**

Zero eligible is a source/contract result, not a requirement. The current Product contract is stronger than during the original Career audit, so every Property candidate was reconsidered against the current implementation rather than inheriting Career's old blocker list.

## What changed since the Career audit
The current temporal adapter can preserve a star-bound transformation when the PL1 star object itself explicitly supplies the mutagen, and it now transports SMALL_LIMIT. Those improvements matter, but they do not by themselves make a source row executable.

The current compiler still requires:
1. a source-supported NATAL antecedent or canonical required natal rule;
2. a positive temporal condition;
3. exact typed fact matching at one selected temporal layer;
4. no CASE_SUPPORT_ONLY promotion.

## Four near-ready rows
**TP03-245 / TP03-246** are unusually clean annual Property-palace transformation clauses: annual Property Palace Tanlang Hua Lu/Hua Ji can be represented by the current temporal fact shape when PL1 explicitly binds the mutagen to Tanlang in the annual Property palace. They still fail the compiler because the source clauses are pure annual triggers and do not supply an independent natal antecedent. A vacuous `PALACE_PRESENT(P10)` gate would exist only to satisfy software and would therefore be invented semantics.

**TP04-307 / TP04-308** do have a source-supported natal Tianliang–Tianji Property context. Their temporal phrase is annual Tianji Hua Ji/Hua Lu. The remaining gap is exact fact shape: the adapter's star-bound temporal transformation contains `palace_name`, while the source phrase does not license a specific temporal palace location for Tianji. Using separate YEAR `STAR_PRESENT(天机)` plus scope-level `TRANSFORMATION_PRESENT(忌/禄)` would silently join two independent facts, which the Product contract explicitly forbids.

## Main blocker families
- **16 CASE_SUPPORT_ONLY rows** remain excluded outright.
- Generic source classes such as 吉曜、煞曜、煞忌、吉化 and their negations are not closed executable groups.
- 庙/陷 brightness is not emitted as a current temporal condition fact.
- 流煞冲会/冲破 and related activation geometry is not an approved executable relation.
- TP01-044/045 and TP03-273 preserve source multi-layer 大限/流年 scope; one-layer reaction normalization must not silently discard a branch.
- TP02-175 preserves 流年+小限 context, but the source also requires an undefined 吉 judgement and a cross-layer conjunction.
- 前格 and PATH_DEPENDENT rows stay dependent; they are not flattened into standalone triggers.

## Decision
No Property temporal rule is normalized into an executable registry in this unit. No Product file, shared ontology, atom type, probability, numeric weight, duration threshold or new time scale is introduced.

The durable outcome is the 35-row eligibility ledger. The next Career-equivalent step is a **Property NATAL atomization pilot (WP07A)**, followed by bounded structural review batches.
