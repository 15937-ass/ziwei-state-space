# WP07B source-reaction disposition — Issue #671

Status: **SOURCE RE-AUDIT COMPLETE; NO RUNTIME-ELIGIBLE REACTION IN THIS BOUNDED SET**

- Lane/shard: `KNOWLEDGE_ONLY / CORE`
- Work unit: `KB-WP07B-SOURCE-REACTION-CONTRACT-01`
- Base `main`: `45d308c95437062110c013f086f48e368f42eaaf`
- Machine-readable record: `knowledge/core/WP07B_TEMPORAL_REACTION_SOURCE_DISPOSITION_v0.1.json`
- Product contract reviewed read-only: `product/PL3T_NATAL_TEMPORAL_REACTION_COMPILER_ACCEPTANCE.md`
- Current adapter reviewed read-only: `src/product/temporal_asset_adapter.py`

## Source-span review coverage

All 9 Career candidates and all 35 Property candidates were re-audited against the source ID `SRC-ZZ-003`, the printed-page locator in the canonical eligibility row, and the supplied scan of *中州派紫微斗数深造讲义（下）*. Exact source condition text remains in the referenced canonical eligibility row rather than being duplicated here.

| Printed page(s) | Scan PDF page(s), 1-based | Candidate family |
|---|---:|---|
| Career 140 | 70 | CA04-346 |
| Career 141 | 71 | CA04-350 |
| Career 145–146 | 73 | CA05-496/497; CA06-545 |
| Career 147–148 | 74 | CA06-580/600 |
| Career 154 | 77 | CA09-851 |
| Career 155 | 78 | CA09-867 |
| Property 156 | 78 | TP01-037 |
| Property 157–158 | 79 | TP01-044/045/048/049/050/051/061/084 |
| Property 159–160 | 80 | TP02-103/135/137/165/166/167/168 |
| Property 161–162 | 81 | TP02-175/176/191; TP03-213/228/232/233/234 |
| Property 163–164 | 82 | TP03-245/246/247/248/273; TP04-307/308/338 |
| Property 165 | 83 | TP04-355/356/357 |

The JSON ledger links each disposition to its source eligibility row and, for Career, its canonical projection-review row. Scan-page numbers are convenience locators; `SRC-ZZ-003` and the printed-page/source-row reference remain the durable source identity.

## Disposition

| Scope | Candidates | Eligible under current PL3-T contract | Blocked reusable rows | Excluded CASE_SUPPORT_ONLY rows |
|---|---:|---:|---:|---:|
| Career / P09 | 9 | 0 | 8 | 1 |
| Property / P10 | 35 | 0 | 19 | 16 |
| **Total** | **44** | **0** | **27** | **17** |

These are candidate disposition counts. Individual blocker-code counts overlap. **Zero eligible means zero rows satisfy this compiler contract; it does not mean the tradition contains no temporal rules.**

## Re-audit findings that change or sharpen the previous blocker picture

### 1. CA04-350 — stale implementation blocker removed, semantic/context blocker remains

The earlier audit lists `STAR_MUTAGEN_BINDING_GAP`. The current PL3-T adapter now emits a star-bound `TRANSFORMATION_PRESENT` fact when and only when the PL1 temporal star object itself carries `mutagen`. That old gap is therefore no longer a sufficient current blocker.

The candidate still cannot enter runtime:

- The source's capital-shortage claim is conditioned on commerce. The WP07A Career natal audit explicitly classifies CA04-348's commerce phrase as `CONTEXT_DEPENDENT_COMMERCE_GATE`, not a natal fact.
- CA04-349 describes a technical-skill scene; substituting it as the antecedent for a capital-shortage reaction would change the source meaning.
- The source names major and annual periods. A one-layer rule must not silently narrow this to DECADE; any layer-specific decomposition must be explicitly source-preserving.
- No executable real-world commerce/context atom is available in this reaction contract.

Result: keep CA04-350 blocked, but update the reason from a stale adapter limitation to the remaining source-context and layer-normalization gaps.

### 2. TP03-245 / TP03-246 — temporal shape is representable; natal antecedent is absent

The annual Property-palace Tanlang Hua Lu/Hua Ji fact shape is representable when PL1 explicitly binds the mutagen to Tanlang in the annual Property palace. The source clauses are nevertheless pure annual triggers and do not supply an independent natal antecedent. Adding `PALACE_PRESENT(P10)` would be a vacuous software-only gate, not source semantics.

### 3. TP04-307 / TP04-308 — natal context is supported; temporal star binding remains under-specified

The natal Tianliang–Tianji Property context is source-supported. The annual Tianji transformation phrase does not license a specific temporal `palace_name`, while the adapter's star-bound transformation fact requires that field. Joining separate `STAR_PRESENT(天机)` and scope-level `TRANSFORMATION_PRESENT(忌/禄)` facts would invent a relation, so both rows remain blocked.

### 4. Remaining blocker families

- CASE_SUPPORT_ONLY rows remain excluded even when their condition looks specific.
- `前格`/parent-dependent clauses remain dependent; a case-only parent is not promoted.
- Generic `吉曜`, `煞曜`, `煞忌`, broad `吉化`, and their negative forms are not closed executable groups.
- Temporal brightness (`庙/陷`) is not currently emitted as a temporal condition fact.
- DECADE+YEAR and YEAR+SMALL_LIMIT source scope is preserved; no layer is silently discarded.
- “Favorable/unfavorable period”, “supportive period”, activation/convergence geometry, and multi-year persistence are not inferred from the predicted outcome or turned into invented scores/timers.
- The three-to-four-year wording in CA09-851 remains source evidence, not a universal threshold, timer, hazard rate, or probability.

## Boundary and handoff

- No production reaction specification was emitted.
- No shared atom, ontology node, time scale, precedence, persistence rule, numeric weight, probability, or event mapping was added.
- No Product file was changed. The production temporal reaction registry must remain empty until a separate source-owned candidate passes every compiler gate and the Product-owned validation/promotion workflow.
- The accepted negative/partial result should be handed to the Product KIB consumer as a source-backed **BLOCKED/UNKNOWN disposition**, not misreported as an executable reaction.
- Core WP06B remains queued behind the single Core WIP slot. Separate palace-local WP06C source candidate indexing and independent palace source audits can proceed in their own shard slots; they must preserve unresolved ontology references and fail closed rather than define shared semantics.
