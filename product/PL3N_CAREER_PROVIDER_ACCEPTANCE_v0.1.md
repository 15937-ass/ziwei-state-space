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
