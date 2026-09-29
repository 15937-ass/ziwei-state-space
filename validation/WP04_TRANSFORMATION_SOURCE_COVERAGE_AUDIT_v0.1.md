# WP04 Transformation Source-Coverage Audit v0.1

Status: **ACTIVE — SOURCE COVERAGE GAP CONFIRMED**

## Why this audit was opened

The existing WP04 transformation catalog contains 56 reviewed rows, but its provenance does not yet establish 100% coverage of the dedicated 四化 chapter.

A repository-level check of `knowledge/operators/transformation_rules_v0.1.csv` found:

- existing transformation rules: **56**
- rows whose `source_location` points to the dedicated 四化 chapter (printed pages 176–232 / Project-text transformation section): **0**
- the existing 56 rows are useful semantic rules extracted from earlier star/system sections, but they cannot by themselves prove chapter-level completeness.

Therefore the previous metric “56 reviewed transformation rules” is retained, but it must not be interpreted as “四化原章节 100% closed”.

## Source structure verified so far

The Project source explicitly contains the four transformation groups:

- 化禄 begins at source line 6397
- 化权 begins at source line 6951
- 化科 begins at source line 7555
- 化忌 begins at source line 8031

Most individual star headings were directly verified in the source text. A small number were not returned by exact-string search because of OCR/typographic variation; those units are marked `SOURCE_SPAN_PENDING` rather than silently treated as verified.

The machine-readable inventory is:

`knowledge/coverage/wp04_transformation_source_units_v0.1.csv`

## Immediate findings

Several exact modifier subjects currently have **zero** dedicated rows in the transformation catalog, including examples such as:

- 巨门化禄
- 巨门化权
- 武曲化科
- 文昌化科
- 文曲化科
- 左辅化科
- 右弼化科
- 文昌化忌 / 文曲化忌

This does not mean the repository has no related semantics anywhere; it means the current canonical transformation catalog has not yet closed the dedicated source subsection.

## Execution rule

For every one of the 40 star-transformation source units:

1. verify the exact source span;
2. compare source claims against existing transformation rules;
3. reuse an existing rule only when the semantic claim and provenance both match;
4. extract missing atomic operators into a source-coverage sidecar first;
5. distinguish latent state, structural gate, pair interaction, temporal trigger and L3 projection;
6. do not overwrite raw reviewed rows solely to improve provenance;
7. quarantine any source/normalization mismatch;
8. update section-level coverage only after the source span is exhausted.

## Architecture status

No new primitive qi or core operator change is required by this audit opening.

**Human Gate: NO**

## Next mechanical unit

Start with **WP04-HL-01 ... WP04-HL-10 (化禄)**, exhaust the dedicated source spans, then continue 化权 → 化科 → 化忌.
