# Execution evidence — issue #603 / PR #620

## Source review performed

- Source artifact: `SRC-ZZ-003`, 《中州派紫微斗数深造讲义（下册）》.
- Local source PDF: `中州派-紫微斗数深造讲义(下册).pdf`.
- Rendered and visually inspected PDF physical pages 6, 7, and 8 at 90 dpi.
- PDF physical page 6 contains printed pages 11–12; page 7 contains printed pages 13–14; page 8 begins printed page 15.
- The scan, not the historical candidate CSV, establishes that P04-376…400 are on printed p14.

## Source-first accounting

- P04 candidate census: 100 unique IDs, P04-301…400.
- Candidate promotions: 100; 88 reusable; 12 CASE_SUPPORT_ONLY.
- Omitted source atoms: P01-SG-125…152 (28 total; 21 reusable; 7 CASE_SUPPORT_ONLY).
- P01-SRC-GAP-023 closed by 47 rules: P04-301…335 plus P01-SG-125…136.
- P01-SRC-GAP-024 closed by 81 rules: P04-336…400 plus P01-SG-137…152.
- P01-SRC-GAP-025 remains open for printed p15 onward (remaining 太阴 and 贪狼).
- Expected cumulative after merge: 550 canonical records (451 reusable, 99 CASE_SUPPORT_ONLY).

## Verification still pending

- Focused test: `tests/test_knowledge_p01_source_readjudication_301_400.py`.
- Replacement PR targets current main; exact-final-head quality gate is pending.
- No automatic push workflow is to be invoked.
