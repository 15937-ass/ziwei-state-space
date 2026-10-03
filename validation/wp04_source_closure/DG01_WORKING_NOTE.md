# DG01 — DIGNITY / ENVIRONMENT SOURCE REVIEW

status: CHECKPOINT_CLOSED_SOURCE_SPAN_VERIFIED

## Scope

- source: SRC-ZZ-002《中州派紫微斗数深造讲义（上册）》
- printed pages: 241–246
- section: 星曜庙陷
- boundary: end of upper volume
- table rows are preserved in `DG01_dignity_tables_v0.1.csv`

## General rules

DG01-001 | SRC-ZZ-002 | 241 | 星曜庙陷 | 宫垣 | 一般 | 宫垣在此处等同星曜所处环境，环境适合度影响星曜力量发挥 | structural_relation | environment_compatibility | define | L0_STRUCTURE | ADD_CANDIDATE
DG01-002 | SRC-ZZ-002 | 241 | 星曜庙陷 | 庙旺平闲陷 | 分类 | 源文以庙、旺、平、闲、陷表示星曜所处环境等级 | structural_relation | dignity_category | five_level_ordinal | L0_STRUCTURE | ADD_CANDIDATE
DG01-003 | SRC-ZZ-002 | 241 | 星曜庙陷 | 入庙 | 吉曜 | 入庙时吉曜最能发挥其本来力量 | gate | favorable_star_expression | maximize_relative_expression | STRUCTURAL_GATE | ADD_CANDIDATE
DG01-004 | SRC-ZZ-002 | 241 | 星曜庙陷 | 入庙 | 凶煞 | 入庙时凶煞的凶暴性质反而减轻 | gate | malefic_adversity_intensity | attenuate | STRUCTURAL_GATE | ADD_CANDIDATE
DG01-005 | SRC-ZZ-002 | 241 | 星曜庙陷 | 落陷 | 吉曜 | 落陷时吉曜较难发挥原有力量 | gate | favorable_star_expression | decrease | STRUCTURAL_GATE | ADD_CANDIDATE
DG01-006 | SRC-ZZ-002 | 241 | 星曜庙陷 | 落陷 | 凶曜 | 落陷时凶曜较易发挥凶暴性质 | gate | malefic_adversity_intensity | increase | STRUCTURAL_GATE | ADD_CANDIDATE
DG01-007 | SRC-ZZ-002 | 241 | 星曜庙陷 | 旺平闲 | 相对等级 | 旺仅次于庙；平与闲影响较小且平略优于闲；部分书籍另以得地/不得地/失地称之 | structural_relation | dignity_order | preserve_source_ordering | L0_STRUCTURE | ADD_CANDIDATE

## Source-preserved tables

DG01-008–019 | printed p242 | 天干星曜庙陷表 | 12 branch rows
DG01-020–031 | printed p243 | 地支星曜庙陷表 | 12 branch rows
DG01-032–043 | printed p244 | 生月星曜庙陷表 | 12 branch rows
DG01-044–055 | printed p245 | 生时星曜庙陷表 | 12 branch/star-association rows
DG01-056–067 | printed p246 | 吉凶杂曜庙陷表 | 12 branch rows

The table artifact is intentionally source-preserving:
- `-` means the source cell is blank.
- the glyph `地` is preserved literally where printed; it is not silently rewritten to `平`, `旺`, or any other category.
- no numeric gain is assigned to 庙/旺/平/闲/陷.
- no interpolation is performed for blank cells.

## Model feedback

1. 庙旺平闲陷 is an **environment-compatibility / expression gate**, not evidence for a fixed linear multiplier.
2. The source explicitly distinguishes favorable-star expression from malefic-star adversity: the same environmental category does not imply a universal signed scalar.
3. Table values belong in a discrete lookup/compatibility layer before any empirical parameter fitting.
4. The source does not provide distances between categories, so treating 庙=+2、旺=+1 etc. would be an implementation hypothesis, not source extraction.
5. No natal-essence rewrite, new primitive qi, history-memory type, second time scale, or default decay is required.

## Checkpoint summary

- reviewed: 67
- ADD_CANDIDATE: 67
- CASE_SUPPORT_ONLY: 0
- source_span_verified: 67/67
- normalization_verified: 67/67
- new Human Gate: 0
- new primitive qi: 0
- new history-memory type: 0
- chapter boundary reached: YES
- source boundary: END_OF_UPPER_VOLUME
