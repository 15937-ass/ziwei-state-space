# P01 / WP05 — Source-first readjudication P01-401…500

## Status

- Issue: #646
- Lane: `KNOWLEDGE_ONLY`
- Source: `SRC-ZZ-003`, 《中州派紫微斗数深造讲义（下册）》, 下篇·宫垣论·命宫
- Candidate IDs: exactly P01-401 through P01-500 (100 unique rows)
- Direct scan mapping: PDF physical p7 = printed pp13–14; physical p8 = printed pp15–16; physical p9 = printed pp17–18.

## Disposition

- Historical candidates re-adjudicated: **100**
- Corrected p14 duplicate rows, retained for audit but not promoted twice: **18** (P01-401…418 → existing P01-SG-144…152)
- Candidate rows promoted: **82** (P01-419…500)
- Omitted source atoms added: **15** (P01-SG-153…167)
- New canonical records in this checkpoint: **97**
- Reusable projection rules: **79**
- `CASE_SUPPORT_ONLY`: **18**
- Cumulative P01 checkpoint after merge: **647** records (530 reusable; 117 CASE_SUPPORT_ONLY)

## Source corrections and coverage

1. **Printed-page correction.** The image for physical PDF page 7 shows that P01-401…418 belong to printed p14, not p15. Their claim identities duplicate P01-SG-144…152. The audit records all 18 dispositions, corrects the source location, and avoids duplicate canonical promotion.
2. **Taiyin (printed p15).** P01-419…430 are source-rechecked. P01-SG-153 separately records the marital-adversity clause from the Chen-Xu Taiyin sentence; P01-SG-154…157 add its four explicitly listed but previously omitted “枢纽” atoms. The source only says “枢纽” for this branch, so its temporal layer remains unspecified.
3. **Printed “己亥太阴”.** The scan shows the printed glyph “己亥太阴”; the following clauses separately discuss 巳宫 and 亥宫. The artifact preserves the printed glyph in uncertainty metadata rather than silently rewriting it to “巳亥”. P01-SG-158…161 capture the omitted branch outcomes/conditions; P01-SG-162…165 preserve the explicitly stated 大运流年 hubs.
4. **Tanlang (printed pp15–16).** P01-431…494 were reviewed against the image. Conditions were tightened where historical rows were too vague, including the 寅午戌 birth-year mapping, the combined 空曜/天刑 condition for “端正”, and the exact conditions around 天刑, 羊陀, and 火贪/铃贪 pattern breaks. P01-SG-166 adds the omitted 寅宫贪狼 penal-event alternative; P01-SG-167 adds the “否则” branch when the flowing sha does not additionally rise.
5. **Jumen opening only.** P01-495…500 are promoted as the six source-backed opening claims. They do not close the whole Jumen section. Gap P01-SRC-GAP-026 remains open for the Jumen remainder and the following Tianxiang/Tianliang sections.

## Temporal scope

- P01-424…427 and P01-487…492 retain the source’s explicit **大运流年** as `DECADE + YEAR`.
- P01-448/449 preserve “流曜” without guessing which time layer it denotes.
- P01-494 preserves generic “年运” as unresolved rather than forcing `DECADE`.
- P01-SG-154…157 preserve the unqualified “枢纽”; P01-SG-162…165 preserve explicit `DECADE + YEAR`.
- Life-stage phrases such as “先贫困、后突发” and “中年后发迹” are metadata about source-described sequence, not a new continuous clock.

## Evidence and boundaries

- The source-span audit used the actual scan images for physical PDF pages 7–9, not the old candidate page labels or OCR line numbers.
- Concrete traditional claims about marriage, wealth, penal events, health, or litigation remain `CASE_SUPPORT_ONLY` where marked. They are source claims, not empirically validated predictions or modern diagnoses.
- No shared semantic primitive, new memory type, independent time scale, numeric weight, probability, or decay was added.
- No Product/runtime authorization is implied.

## Next source anchor

`P01-501…P01-600 source-first checkpoint: continue 巨门余段 from printed p17, then cover 天相 and 天梁; verify every printed page from scan images and preserve source-native time wording.`
