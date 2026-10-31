# PL3-N Career Natal Provider Acceptance v0.1

Status: **PRODUCT REGISTRY IMPLEMENTED; TEMPORAL CONCLUSION REMAINS PARTIAL**

## Scope

This Product-owned registry turns explicitly selected reviewed WP07A mapping entries into an explicit, executable NATAL provider. It does not change the Knowledge mapping, canonical Career CSV rows, source prose, or Knowledge state.

## Activated NATAL rules

| Source rule | Exact condition | Preserved projection |
|---|---|---|
| CA04-347 | `TRANSFORMATION_PRESENT(palace=P09, star=武曲, mutagen=科)` | `reputation → career_requires_reputation_building` (`FUNCTIONAL_PROJECTION`) |
| CA04-349 | `TRANSFORMATION_PRESENT(palace=P09, star=武曲, mutagen=忌)` | `career → technical_skill_work_scene_preferred` (`SCENE_TRANSLATION`) |
| CA09-852 | `TRANSFORMATION_PRESENT(palace=P09, star=破军, mutagen=禄)` | `role → multiple_jobs_side_roles_or_business_lines_are_common` (`FUNCTIONAL_PROJECTION`) |

The Product registry preserves each canonical source row's source ID, location, review status, condition text, projection domain, target, and mode. The generic provider fails closed on drift in any of those fields, rejects CASE_SUPPORT_ONLY rows, and accepts NATAL rules only.

## Mapping handoff integrity

`load_default_career_natal_provider` validates the Product registry against the source-grounded mapping artifact before compiling:
- the mapping audit ID, schema version, and non-executable mapping status;
- exact selected rule ID coverage across disjoint source mapping handoffs;
- each source row's NATAL / verified / non-case provenance;
- condition atoms and projection values against the reviewed mapping;
- the Knowledge artifact's `executable_registry_entry=false` marker.

The Knowledge mapping remains `SOURCE_GROUNDED_MAPPING_COMPLETE_NOT_EXECUTABLE`. The executable form exists only in this Product-owned registry; the mapping file is not edited or promoted.

## Runtime contract

- The provider is opt-in. `load_default_natal_domain_registry(ROOT)` remains Wealth-only.
- To use Career, load the Career provider explicitly and pass it through `additional_providers`.
- Only the explicitly nominated rules are compiled. The remaining rows in the source CSVs remain pending and are not implicitly normalized.
- A rule activates only if the exact star-bound transformation fact exists in the normalized natal chart. A missing mutagen, wrong star, or wrong palace does not match.
- Rule evidence includes the canonical rule ID and source provenance.

## End-to-end acceptance

The integration test runs the real Product registry through the full inference pipeline with `selected_domains=("career",)` and `selected_temporal_layers=("DECADE", "YEAR")`.

Expected behavior:
- canonical natal rule evidence can be emitted and source-traced;
- the selected decade and year are present in the temporal namespace;
- the empty production temporal reaction registry remains a blocker;
- the structured conclusion is `PARTIAL`, with no temporal reaction rule IDs;
- no real-world event claim, probability, universal valence, or magnitude is invented.

## Explicitly out of scope

The following are not executable through this provider:
- decade/year Career reaction semantics;
- activation/convergence rules;
- favorable/unfavorable period predicates;
- multi-year persistence or path-dependent Career gates;
- manifestation or event certainty;
- numeric probabilities, weights, and thresholds.

Those require separate source-faithful Product contracts and reviewed temporal mappings. This acceptance file records implementation behavior, not empirical predictive validity.


## High-level Product API

The Product exports `run_career_inference(repository_root, normalized_snapshot, target_id=..., question=...)`. Before loading any provider, it validates both the structural full-chart snapshot contract and `product/CANONICAL_CHART_CONTRACT_v1.1.md`. The lower-level `run_symbolic_inference` repeats the canonical chart gate as defense in depth. Only Zhongzhou `iztro-js@2.6.1` snapshots with the exact frozen configuration are accepted for production inference. It then loads the source-pinned Career provider, adds it explicitly to the domain registry, and always uses the production temporal reaction registry. The default selected temporal layers are `DECADE + YEAR`; callers may supply a different valid selection.

The wrapper never substitutes a temporal test fixture. With the current empty production reaction registry, it returns `PARTIAL_TEMPORAL_REGISTRY_EMPTY`, preserves the matched canonical NATAL evidence, and reports the temporal blocker. Invalid or absent targets still fail closed.


## Chinese-facing report contract

`build_career_inference_report(repository_root, run)` produces a deterministic report view for the Career-only run. It exposes:
- Chinese status text that explicitly says when temporal inference is partial;
- each activated NATAL rule's source condition, mapping summary, preserved projection, and source provenance;
- selected time layers and temporal fact counts;
- matched temporal rule IDs, registry status, blockers, unknowns, conflicts, and limitations.

The report builder checks that active rule evidence and projection fields still match the Product registry. It always emits `real_world_event_prediction_supported=false`; it does not turn a rule projection into a real-world event forecast.


## Command-line invocation

From the repository root:

```bash
python -m src.product.career_inference_cli \
  --snapshot path/to/normalized-full-chart.json \
  --target-id T-2030 \
  --question "事业本命结构及大限、流年环境" \
  --temporal-layers DECADE YEAR \
  --output path/to/career-report.json
```

The module CLI calls the same Product APIs as Python callers, writes deterministic UTF-8 JSON, and refuses to overwrite the input snapshot and optional migration-window file. If `--output` is omitted, the report is written to stdout. The CLI intentionally has no option for substituting a temporal test registry.

A successful invocation can still return `PARTIAL_TEMPORAL_REGISTRY_EMPTY`; process success means the report was generated correctly, not that temporal rules were available or that a real-world event was predicted.


## Approved event-relative migration window

The Product API optionally accepts a typed `MigrationFirstThreeYearsInput`, and the CLI exposes it through `--migration-window path/to/window.json`. The JSON object must contain `confirmed_distant_settlement`, `years_since_distant_relocation`, and `travel_only`; confirmed settlement also requires non-empty `trigger_provenance`.

This uses only the already approved `MIGRATION_FIRST_THREE_YEARS` resolver:
- confirmed distant settlement, not travel-only, year 1–3: `ACTIVE`;
- travel-only or year 4+: `INACTIVE`;
- confirmed settlement with no elapsed-year value: `INSUFFICIENT`.

The context is reported with its source provenance and routing facts. It is not a temporal reaction rule, does not add a seventh calendar time layer, and does not change `PARTIAL_TEMPORAL_REGISTRY_EMPTY` while the production reaction registry remains empty.


CLI example with an explicit external trigger:

```json
{
  "confirmed_distant_settlement": true,
  "years_since_distant_relocation": 2,
  "travel_only": false,
  "trigger_provenance": "OBS-RELOCATION-001"
}
```

Save the object as `migration-window.json` and pass `--migration-window migration-window.json`. The provenance token identifies the externally supplied observation; it is not inferred from the Zi Wei chart. If the user has only travelled without confirmed distant settlement, the window must remain inactive.


## Normalized full-chart input gate

Before loading a provider, `run_career_inference` now validates the PL1 full-exporter schema v0.2 through `validate_normalized_full_chart_snapshot`. The Product contract is documented in `product/PL3_FULL_CHART_SNAPSHOT_CONTRACT_v0.2.md` and represented as `product/PL3_FULL_CHART_SNAPSHOT_SCHEMA_v0.2.json`.

The validator checks engine provenance, the twelve-branch natal palace map, target uniqueness and selection, target/date consistency, all six temporal scopes and adapter-required fields, and optional `yearly_dec_stars`. Invalid snapshots fail closed with deterministic diagnostics; the validator never mutates or repairs input. Both Python API and module CLI use the same gate.


## CA01–CA03 static expansion (Issue #344)

The provider now executes 17 NATAL rules: the original three above and these 14
source-preserving entries from the merged CA01–CA03 mapping:

| Rule IDs | Condition and required boundary |
|---|---|
| CA01-052 / 053 | 紫微化权；独立性投影与“不由权直接推出富贵”的限制同时保留 |
| CA01-054 / 055 | 紫微化科；声誉与专业工作场景投影 |
| CA01-070 / 071 | 紫微化权，且事业宫必须在子或午；事业优势与婚姻张力并存的来源限制 |
| CA01-078 | 紫微化科，且事业宫必须在子或午 |
| CA02-155 | 天机化禄；不消除天机不稳定性的结构限制 |
| CA02-160 / CA03-254 | 天机化科；规划管理设计场景与变化性质保留 |
| CA03-252 | 天机化忌，且事业宫必须在巳或亥；保险工作场景 |
| CA03-279 | 太阳化禄；声誉或品牌价值投影 |
| CA03-283 | 太阳化科；依赖声誉的专业场景 |
| CA03-285 | 太阳化忌；排难解纷或言语工作场景，不推断纠纷事件 |

All transformations are bound to the named star in P09. Exact canonical targets,
projection modes, conditions and provenance remain in the registry and report.
The mapping is selected explicitly; future Knowledge mapping additions cannot
activate automatically. The Knowledge files remain non-executable and unchanged.

CA02-158 and CA02-164 remain blocked because their outputs require prior change
or repeated settlement history. CA02-194 remains blocked for manifestation review.
A static condition match cannot supply that missing history or event semantics.
The handoff rejects blocked readiness even if an entry is manually selected.

This is internal condition/source-trace validation. It is not empirical validation,
career advice, event prediction, a time forecast, or an accuracy estimate.


## CA04–CA09 static expansion (Issue #346)

The provider now executes 23 NATAL rules. The previous 17 remain unchanged.
Six additional entries come exclusively from the reviewed direct-transformation
mapping merged in PR #315:

| Rule | P09 condition | Preserved scene or function |
|---|---|---|
| CA04-327 | 太阳化忌 | 排难解纷性质的工作，不推成现实是非事件 |
| CA05-469 | 廉贞化忌 | 带血光象义的行业场景，保留饮食/化验语境，不作疾病或伤害预测 |
| CA07-671 | 巨门化禄 | 口舌/表达类事业投影，不推断收入金额 |
| CA07-672 | 巨门化权 | 表达类事业支持，不推出必然职业成功 |
| CA07-673 | 巨门化忌 | 偏门或带政治色彩的行业场景；保留“不应直接推为官非诉讼”的来源限定 |
| CA08-765 | 天梁化权 | 权威性质工作，法律/监察/秘书为来源举例，不作唯一职业判断 |

Exact source summaries, projections, modes, conditions and provenance are shown
in the actual Chinese report. Missing transformation, a different transformation,
a wrong named star, or the same transformation outside P09 cannot activate its
rule. There is no additional branch restriction for these six source conditions.

CA05-403 remains blocked as a timing trigger. CA08-766 remains blocked for its
social-status-before-wealth ordering and PATH_DEPENDENT_GATE metadata. Selecting
such IDs manually cannot bypass the readiness validator. Knowledge mapping files
remain unchanged and non-executable; only this explicit Product subset runs.

The production temporal reaction registry is still empty. This expansion is
internally verified source-faithful rule execution, not empirical validation.


## Star-presence expansion and modality (Issue #350)

The Career provider now executes 31 explicit NATAL rules. The prior 23 entries
remain unchanged. Eight entries from merged Knowledge PR #335 are compiled
separately in Product:

| Rules | Exact P09 condition | Source boundary |
|---|---|---|
| CA01-026 / 027 | 地空 AND 地劫 | Distinct industry/method projections; alternative interpretations, not two guaranteed outcomes |
| CA01-031 / 032 / 033 | 陀罗 | Three distinct targets; “往往”“有时亦主” remain qualitative, with no predicted delay length |
| CA01-034 | 擎羊 | Modern engineering/technical scene preserves ancient-to-modern translation, not a unique occupation |
| CA01-042 | 禄存 | Existing-business/salaried scene; cannot alone establish wealth |
| CA01-044 | 禄存 AND 地空 AND 地劫 | All three in P09; indecision tendency only, no forced-change outcome |

The handoff recognizes exactly the reviewed transformation-mapping status and
reviewed star-presence-mapping status. It still requires non-executable Knowledge
entries, source verification, NATAL, non-case status, precise selected IDs and
exact conditions/projections. Star-presence source modality is pinned in Product
and must be nonempty and unchanged. Unknown statuses fail closed.

The actual Chinese report adds `source_modality_note` for these eight entries,
verbatim from the reviewed mapping. Existing transformation report entries retain
their previous fields. Empty charts are not negative outcomes; they simply do
not match these rules. Missing any required star or placing it in any other
palace cannot complete a same-palace condition.

CA01-035, CA01-043 and CA01-045 are not activated here. Active Knowledge context
recovery is independent of this Product unit and does not authorize automatic
execution. No temporal reaction, probability, severity or empirical claim is added.


## Cross-palace expansion (Issue #353)

The provider now executes34 explicitly selected NATAL rules. The prior31 entries
remain unchanged. Three entries come from the reviewed mapping in merged PR #322:

| Rule | Complete condition | Preserved projection |
|---|---|---|
| CA01-066 | P09紫微 at子 or午 AND P05廉贞化禄 | 合作创业场景，非保证创业成功 |
| CA02-188 | P09午宫天机化禄 AND P05太阴化忌 | 事业投机倾向的跨宫联系，非必然投资行为 |
| CA03-255 | P09天机化科 AND P01天同与巨门同在，且P01巨门化忌 | 劳心与额外工作倾向，非必然工作负荷事件 |

Each condition retains the exact reviewed all_of/alternatives structure. A
matching star or transformation in another palace cannot substitute for the
required palace. Generic transformation facts without the named star are not
sufficient. The report preserves source summaries, locations and exact
CROSS_PALACE_CONSTRAINT projection targets.

The handoff separately recognizes the reviewed cross-palace mapping status and
requires its MAPPED_EXISTING_ATOMS entry marker; existing single-atom handoffs
retain their original marker. No arbitrary status is accepted. Knowledge files
remain non-executable; Product activates only these three nominated entries.

The tested synthetic chart fixtures establish conditional logic and source
traces, not that every injected star pattern is reachable from a birth input or
that the described outcomes occur. The raw pinned engine audit exercises actual
exported charts separately. No causal inference, time forecast, empirical
probability or event certainty is established.

CA01-023 spouse空劫 and CA01-020/064/065 remain unselected in this unit. No
PALACE_RELATION semantics or ontology change is needed by these three rules.
The production temporal reaction registry remains empty.


## Career–Spouse 空劫 (Issue #356)

The Career provider now executes35 explicit NATAL rules. The previous34 entries
remain unchanged. CA01-023 comes solely from the reviewed mapping merged in #331.

The condition preserves a global P09 -> P03 OPPOSITE prerequisite plus four full
alternatives: P09寅/P03申 or P09申/P03寅, each with either P09地空/P03地劫 or
P09地劫/P03地空. Both branch facts and both stars are required. Same-palace pairs,
other branches, missing stars and a missing relation fact cannot substitute.

This source mapping stores source_context rather than source_span_summary.
Product pins the entire reviewed context and requires its four nonempty fields:
source_scope_note, branch_gate_reading, normalized_reading and relation_basis.
The actual report uses the reviewed normalized_reading as source_summary, and
also exposes the exact source_context, including source-scope/OCR uncertainty.
No new source paraphrase, relationship advice or empirical causal conclusion is
introduced. Existing summary/modality fields for prior rules retain their values.

The target spouse_influence_can_impair_career is preserved as a conditional
source projection, not a finding that a real spouse harms an individual's career.
The report still declares real_world_event_prediction_supported=false, and the
production temporal reaction registry remains empty. Deterministic testing proves
logical prerequisites and source traces, not real-world causation or accuracy.


## Ziwei / 丑未紫破 candidate batch (Issue #363; BLOCKED by #364)

Candidate Career NATAL execution expands35 ->43 by adding all eight explicitly reviewed
candidates from merged #360: CA01-047,050,083,087,088,089,093,095. Previous35 entries
are unchanged.

| Rules | Complete P09 condition | Preserved meaning |
|---|---|---|
| 047 / 050 | 紫微 | 独当一面的责任性质；独立工作或部门负责，不推为自行经营或领袖身份 |
| 083 / 093 | 丑或未，紫微与破军同宫 | 开创适宜性／资源规模与收成差异；保留本段范围 |
| 087 / 088 | 上述范围，加破军化禄 | 事业多变／额外工作两个独立投影；088完整继承同句四化 |
| 089 | 上述范围，加破军化权 | 保留波折性质，不混用化禄分支 |
| 095 | 上述范围，加左辅和右弼同度 | 四曜全在P09；不以任一辅曜或他宫会照代替 |

The handoff explicitly declares PARAGRAPH_SCOPE_V0_1 for this mapping. All context
is pinned exactly; palace, paragraph scope, inherited source IDs, branch gate,
modality and source-scope notes are validated. The prior spouse mapping retains
its BRANCH_GATE_V0_1 default and four mandatory context fields. Unknown context
schemas, empty mandatory text, invalid scope and context drift fail closed.
The actual report shows the original source summary and complete source context.

093 uses the reviewed general paragraph scope. No extra化禄 or不能开创 condition
is introduced. Source projections are not real income, career-event or leadership
forecasts. Production temporal registry remains empty and empirical validation
is still absent.

A content-facing review in
`validation/product/issue_363_ziwei_zipo/CONTENT_CAPABILITY_REVIEW.md` distinguishes
the responsibility, creation, workload, turbulence, resource and assistance
meanings, including how they combine in one report and which real-world claims
remain unsupported. It also records a read-only preview of the twenty complete
Knowledge #366 mappings without selecting or activating them.


Issue #363 is not accepted on main while Knowledge dependency #364 is open.
After synchronization with Knowledge #366, the candidate full suite is826
passed/1 failed: a Knowledge-owned historical
assertion forbids these IDs in the Product registry. No test is skipped and
no failing-gate merge is permitted. Main accepted count remains35.


## Knowledge #366 review-batch expansion (Issue #378)

The Career provider expands from 43 to 63 explicitly selected NATAL rules by
integrating exactly twenty complete mappings from
`knowledge/wp07a/CAREER_100_REVIEW_01_v0.1.json`:

- CA01-067, 068, 072, 076, 077, 084;
- CA02-102, 103, 104, 105, 109, 110, 111, 112, 114, 119, 120, 122, 124, 128.

The Product handoff accepts the batch artifact only under the exact
`HUNDRED_RULE_REVIEW_COMPLETE_NOT_PRODUCTION` status and pins a dedicated
`REVIEW_BATCH_PARAGRAPH_SCOPE_V0_1` context contract. For every selected row,
Product preserves the reviewed paragraph scope, supported chart-context subset,
inherited source IDs, incomplete-antecedent marker, and the explicit prohibition
against inventing additional semantics. Unknown status/schema values, context
drift, blocked readiness, condition drift, and unselected rows fail closed.

The new rules cover five bounded content groups: 子午紫微 responsibility and
spouse/collaboration constraints; 丑未紫破 labor-intensive creation; 寅申紫微天府
platform/resource/operational-realism differences; 卯酉紫微贪狼 market,
cooperation, 空劫 and organization/team properties; and 辰戌紫微天相 rise/fall
tendency. Exact source wording, conditions and projection targets remain in the
registry/report.

CA02-121 is intentionally not selected: its adjacent year-period condition is
temporal and must not leak into CA02-119/120. Likewise, relationship, political,
competition and industry projections remain source-scene properties, not real-world
event certainty or unique occupation labels.

The production temporal reaction registry remains empty. Passing deterministic
Product tests and engine regressions establishes source/condition execution
integrity only; it does not establish empirical predictive accuracy.


## Knowledge Review-02 expansion (Issue #389)

The Career provider candidate expands from 63 to 104 explicitly selected NATAL
rules by integrating exactly 41 complete mappings from
`knowledge/wp07a/CAREER_100_REVIEW_02_v0.1.json`.

The Review-02 handoff reuses the strict review-batch contract introduced for
Issue #378. Product accepts the exact non-production batch status, explicit
selected IDs, complete source/projection provenance and verbatim source_context.
All selected rows remain `executable_registry_entry=false` in Knowledge; the
executable form exists only in Product. Blocked or context-only Review-02 rows
remain unselected and cannot be made executable by registry insertion without
failing readiness validation.

This batch substantially expands Career content around 辰戌紫微天相, 巳亥紫微七杀,
天机总论, 子午天机, 丑未天机天梁, 寅申天机太阴, 卯酉天机巨门 and 辰戌天机天梁.
Named transformations remain bound to named stars, branch gates remain exact,
and P09/P03 OPPOSITE relations remain explicit condition atoms.

Important source boundaries are preserved:
- CA02-174 includes 天机化禄/化权/化忌, not 化科;
- CA03-207 requires both 天机化禄 and 太阴化忌;
- CA03-220 represents a structural requirement that development needs 化禄 or
  禄存; matching the mother star-system condition does not mean the requirement
  has already been satisfied;
- CA02-165 may inherit reviewed condition context from CA02-164 without activating
  the blocked path-dependent target CA02-164 itself;
- scene translations such as personnel management, retail, advertising, finance,
  service industries and speech-based income remain examples/fit properties,
  not unique occupation or real-income predictions.

The production temporal reaction registry remains empty. Deterministic tests prove
condition/provenance/report integrity and engine consistency, not empirical
predictive validity, causal truth or event certainty.


## Knowledge Review-03 expansion (Issue #400)

The Career provider candidate expands from 104 to 134 explicitly selected NATAL
rules by integrating exactly thirty complete mappings from
`knowledge/wp07a/CAREER_100_REVIEW_03_v0.1.json`.

This batch uses the exact Knowledge status `REVIEW_COMPLETE_NON_PRODUCTION`.
Product accepts that status explicitly rather than widening the handoff to arbitrary
review documents. Review-03 uses a dedicated `REVIEW_COMPLETE_CONTEXT_V0_1`
source-context contract because its reviewed rows mark the chart antecedent complete,
unlike Review-01/02. Paragraph scope, optional supported-chart context, inherited
source IDs, the complete-antecedent marker and the prohibition on invented semantics
are pinned verbatim. Review-01/02 keep their stricter incomplete-antecedent contract.

The thirty rules expand content around 天机天梁／巳亥天机, 太阳总论, 太阳天梁,
太阳太阴, 太阳巨门 and 武曲. They add bounded projections for instability and
mobility, reputation versus material return, public trust, internal operations,
administration/finance/planning scenes, external-affairs and language-based work,
cross-region resources, and finance/engineering/technical-craft orientations.

Important boundaries remain explicit:
- CA03-250 inherits only CA03-249;
- CA03-284 inherits the already reviewed solar-化科 condition from CA03-283;
- CA03-293 inherits CA03-292;
- CA04-308 inherits CA04-307;
- CA04-330 inherits CA04-329;
- CA04-315 keeps 太阴化忌 bound to 太阴;
- CA04-329 permits only 太阳化禄 or 太阳化权 in the reviewed alternatives;
- P09/P03 OPPOSITE relations remain explicit where reviewed;
- Review-03 rows with null conditions or blocked/context-only dispositions remain
  non-executable and are not approximated into simpler conditions.

Scene translations such as electronics/computing, medical/insurance/service,
administration, finance, advertising/external affairs, speech/language/singing,
metal/engineering and technical craft are source-bounded scene properties rather
than unique occupation predictions.

The production temporal reaction registry remains empty. Deterministic validation
establishes source/condition/projection execution integrity only, not empirical
predictive validity, event certainty, causal truth or numeric probability.


## Review-04 expansion (Issue #407)

Product selects exactly 31 complete Review-04 mappings and expands the Career NATAL
provider from 134 to 165 rules. The handoff reuses the explicit
`REVIEW_COMPLETE_NON_PRODUCTION` / `REVIEW_COMPLETE_CONTEXT_V0_1` contract already
approved for reviewed hundred-rule batches.

The selected rules preserve source provenance, reviewed conditions, projection targets,
paragraph context and inherited source IDs verbatim. Named transformation atoms remain
bound to their named star carrier. Review-04 blocked/context-only rows remain outside
the Product registry.

Issue #407 also preserves the layered inference rule established in Issue #400:
general star-system rules and more-specific transformation/combination rules may coexist
when the same chart satisfies both. In particular, 武曲化忌 may simultaneously satisfy
general 武曲 properties, CA04-349, and the Review-04 risk-industry rule CA04-352.
Product must not invent negative/exclusion conditions merely to force single-rule output.

All rules remain static NATAL evidence. No temporal reaction, empirical probability,
real-world event certainty or unique occupation claim is authorized.


## Review-05 expansion (Issue #416)

Product selects exactly 25 Review-05 mappings that satisfy the existing provenance gate and
expands the Career NATAL provider from 165 to 190 rules. The batch reuses the explicit
`REVIEW_COMPLETE_NON_PRODUCTION` / `REVIEW_COMPLETE_CONTEXT_V0_1` handoff contract.

The selected rules preserve source provenance, reviewed condition atoms, projection targets,
paragraph context and inherited source IDs verbatim. Named transformations remain star-bound,
and CA05-453 / CA05-454 / CA05-498 retain explicit P09->P03 OPPOSITE relations.

This batch expands 天同天梁, 天同对太阴 and 廉贞-related Career structure, including
planning/management, mobility, transportation/service, artistic and design scenes,
career-partnership orientation, financial/metal scenes, material-return/reputation links,
multiple-business-lines and social-network expansion.

CA05-495 and CA06-527 are deliberately **not** selected. Although their mapping rows are marked
COMPLETE_CONDITION_MAPPING, their source provenance has `case_support_only=true` and their
projection mode is `EVENT_CANDIDATE`. The Product handoff already rejects case-support-only
provenance. Issue #416 preserves that boundary rather than weakening it. These two rows remain
non-executable candidates and are not converted into dated event predictions, probabilities or
guaranteed setbacks/change events.

Historical batch/scenario tests remain additive: they validate their own handoff and required/
forbidden evidence rather than freezing future global rule counts or complete active-rule sets.
