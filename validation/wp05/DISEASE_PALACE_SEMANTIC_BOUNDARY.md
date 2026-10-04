# WP05 Disease Palace Semantic Boundary

Status: **ACTIVE — SOURCE-GROUNDED SAFETY BOUNDARY**

## Source basis
Canonical source: `SRC-ZZ-003`, Disease Palace chapter, printed pp93 onward.

The source itself sets a materially different reasoning boundary for 疾厄宫:

1. Do not infer health from the natal Disease Palace alone. The chapter explicitly requires whole-chart observation and, at minimum, joint reading of 疾厄宫、命宫、福德宫.
2. Natal structure primarily supplies **constitution / susceptibility**. Major illness, surgery and severe events require temporal activation through 大限 / 流年 and relevant malefic or transformation combinations.
3. The source explicitly states that a chart configuration does **not** make a disease inevitable. It discusses a brewing period, an onset period and the possibility that preventive care changes whether disease manifests.
4. The source explicitly acknowledges incomplete validation: some rare diseases are not reliably distinguishable, and its AIDS-related proposal is described as an unverified hypothesis.
5. The chapter is organized by disease name for teaching convenience, but the project normalizes it back into star/system → susceptibility/mechanism → temporal activation → event-candidate evidence.

## Projection boundary
For P06, records are separated into five layers:

- **susceptibility_domain** — body-system or constitutional tendency supported by the source;
- **mechanism** — source-described five-element / star-system mechanism;
- **symptom_cluster** — traditional symptom-level expression;
- **clinical_event_candidate** — named disease, surgery, disability, cancer, poisoning, etc.;
- **timing** — decade/year activation window.

### Reusable
Reusable records may express:
- whole-chart observation requirements;
- palace interaction requirements;
- body-system susceptibility;
- qualitative severity modifiers;
- temporal activation structure;
- source-explicit mechanism without converting it into modern clinical fact.

### CASE_SUPPORT_ONLY
Named diagnoses, specific diseases, operations, disability, cancer, death/survival claims, infectious disease, poisoning, sexual/reproductive pathology and other concrete medical outcomes are **EVENT_CANDIDATE + case_support_only=true by default**.

These records preserve source content for research and later case validation. They are not executable medical diagnoses and must not be surfaced to users as clinical conclusions.

## Temporal semantics
The chapter supplies a two-stage logic:

**natal susceptibility / disease-star structure → decade/year activation → possible manifestation**

This is handled by the existing temporal resolver and does not create a new history-memory class by itself. A source-explicit disease progression may be stored for research, but no probability, incubation duration, hazard rate, recovery rate or continuous decay is inferred.

## Product safety
The product must not:
- diagnose disease from a chart;
- recommend treatment from astrological evidence;
- estimate survival, cancer probability or medical prognosis;
- replace clinical evaluation.

It may describe source-defined traditional susceptibility language with provenance and uncertainty, and it may explain which temporal/palace structures the source asks the practitioner to inspect.

## Closure criterion for P06
P06 can close only when:
- all source spans are reviewed;
- concrete medical claims are quarantined as CASE_SUPPORT_ONLY;
- reusable rules remain at constitution / mechanism / timing / cross-palace level;
- OCR-ambiguous medical terms are not silently repaired;
- no new clinical certainty, probability or causal parameter is invented.
