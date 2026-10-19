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

The Product exports `run_career_inference(repository_root, normalized_snapshot, target_id=..., question=...)`. It loads the source-pinned Career provider, adds it explicitly to the domain registry, and always uses the production temporal reaction registry. The default selected temporal layers are `DECADE + YEAR`; callers may supply a different valid selection.

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
