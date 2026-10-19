# PL3-N Career Natal Provider Acceptance v0.1

Status: **PRODUCT REGISTRY IMPLEMENTED; TEMPORAL CONCLUSION REMAINS PARTIAL**

## Scope

This Product-owned registry turns the three reviewed WP07A mapping entries into an explicit, executable NATAL provider. It does not change the Knowledge mapping, canonical Career CSV rows, source prose, or Knowledge state.

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
- exact nominated rule ID coverage;
- each source row's NATAL / verified / non-case provenance;
- condition atoms and projection values against the reviewed mapping;
- the Knowledge artifact's `executable_registry_entry=false` marker.

The Knowledge mapping remains `SOURCE_GROUNDED_MAPPING_COMPLETE_NOT_EXECUTABLE`. The executable form exists only in this Product-owned registry; the mapping file is not edited or promoted.

## Runtime contract

- The provider is opt-in. `load_default_natal_domain_registry(ROOT)` remains Wealth-only.
- To use Career, load the Career provider explicitly and pass it through `additional_providers`.
- Only the three nominated rules are compiled. The remaining rows in the source CSVs remain pending and are not implicitly normalized.
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
