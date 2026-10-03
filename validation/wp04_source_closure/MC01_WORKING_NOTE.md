# MC01

Working misc source-review checkpoint.
status: ACTIVE

## MC01 structured review
schema: id | source_id | page | section | subject | condition | claim | operator | target | change | layer | disposition
reviewer: gpt-5.6-sol/wp04-mc01
reviewed_at: 2026-10-03
source_epistemic: EXPLICIT
review_status: SOURCE_SPAN_VERIFIED
normalization: SOURCE_PRESERVING

MC01-001 | SRC-ZZ-002 | 232 | 杂曜总论 | 杂曜 | 一般 | 杂曜用于使六十星系的既有本质发生进一步变化 | structural_relation | system_modification | enable | L0_STRUCTURE | ADD_CANDIDATE
MC01-002 | SRC-ZZ-002 | 232 | 杂曜总论 | 杂曜 | 与正曜星系组合 | 杂曜不能脱离十四正曜与六十星系独立定象 | structural_relation | context_dependence | require_base_system | L0_STRUCTURE | ADD_CANDIDATE
MC01-003 | SRC-ZZ-002 | 232 | 杂曜总论 | 杂曜 | 推断 | 杂曜作用应作为对原有星系本质的补充与变用 | structural_relation | modifier_role | modify_existing_state | L0_STRUCTURE | ADD_CANDIDATE
MC01-004 | SRC-ZZ-002 | 232 | 天伤天使 | 天伤 | 一般 | 天伤的基本性质为虚耗 | enhance | depletion | increase | LOCAL_STATE | ADD_CANDIDATE
MC01-005 | SRC-ZZ-002 | 232 | 天伤天使 | 天使 | 一般 | 天使的基本性质为灾病 | projection | adversity_health_case | increase | L3_PROJECTION | CASE_SUPPORT_ONLY
MC01-006 | SRC-ZZ-002 | 232 | 天伤天使 | 伤使 | 安星结构 | 天伤天使必夹迁移宫 | structural_relation | palace_geometry | flank_migration | L0_STRUCTURE | ADD_CANDIDATE
MC01-007 | SRC-ZZ-002 | 232 | 天伤天使 | 阳男阴女 | 顺行 | 天伤在交友宫、天使在疾厄宫 | structural_relation | placement_rule | friend_health_axis | L0_STRUCTURE | ADD_CANDIDATE
MC01-008 | SRC-ZZ-002 | 232 | 天伤天使 | 阴男阳女 | 逆行 | 天伤在疾厄宫、天使在交友宫 | structural_relation | placement_rule | health_friend_axis | L0_STRUCTURE | ADD_CANDIDATE
MC01-009 | SRC-ZZ-002 | 232 | 天伤天使 | 伤使所夹宫位 | 正曜化忌 | 被夹宫位正曜化忌会提高灾厄风险 | gate | adversity_risk | increase | STRUCTURAL_GATE | ADD_CANDIDATE
MC01-010 | SRC-ZZ-002 | 232 | 天伤天使 | 伤使所夹宫位 | 四煞并照 | 四煞并照会提高灾厄风险 | gate | adversity_risk | increase | STRUCTURAL_GATE | ADD_CANDIDATE
MC01-011 | SRC-ZZ-002 | 232 | 天伤天使 | 伤使所夹宫位 | 流年大运煞忌冲起 | 时间层冲起可激活原有伤使风险 | layer_interaction | latent_adversity_activation | increase | TEMPORAL_LAYER | ADD_CANDIDATE
MC01-012 | SRC-ZZ-002 | 232 | 天伤天使 | 天机或巨门 | 伤使夹 | 天机或巨门被伤使夹时更易出现多病类传统投影 | projection | health_case | increase | L3_PROJECTION | CASE_SUPPORT_ONLY
MC01-013 | SRC-ZZ-002 | 232 | 天伤天使 | 天机或巨门 | 再见煞忌 | 煞忌会进一步放大伤使夹的负面作用 | enhance | adversity_intensity | increase | LOCAL_STATE | ADD_CANDIDATE
MC01-014 | SRC-ZZ-002 | 232 | 天伤天使 | 伤使夹迁移 | 宫位联动 | 伤使夹迁移同时会照兄弟宫与父母宫 | structural_relation | cross_palace_link | activate_family_palaces | L0_STRUCTURE | ADD_CANDIDATE
MC01-015 | SRC-ZZ-002 | 232 | 天伤天使 | 小限 | 落伤使夹池 | 判断时需回查兄弟宫、父母宫的机巨与煞忌情况 | structural_relation | diagnostic_dependency | require_cross_palace_check | L0_STRUCTURE | ADD_CANDIDATE
MC01-016 | SRC-ZZ-002 | 232 | 天伤天使 | 小限 | 推断应期 | 小限伤使推断可存在一至两年时差 | time_scale_effect | event_timing | uncertain_offset_1_2_years | TEMPORAL_GATE | ADD_CANDIDATE
MC01-017 | SRC-ZZ-002 | 232 | 天伤天使 | 天伤 | 巳酉丑 | 天伤在金局宫位作用较轻 | gate | adversity_intensity | attenuate | COMPATIBILITY_RELATION | ADD_CANDIDATE
MC01-018 | SRC-ZZ-002 | 232 | 天伤天使 | 天伤 | 午未 | 天伤在火方作用较重 | gate | adversity_intensity | increase | COMPATIBILITY_RELATION | ADD_CANDIDATE
MC01-019 | SRC-ZZ-002 | 232 | 天伤天使 | 天使 | 子午未 | 天使在子午未较有利 | gate | adversity_intensity | attenuate | COMPATIBILITY_RELATION | ADD_CANDIDATE
MC01-020 | SRC-ZZ-002 | 232 | 天伤天使 | 天使 | 辰酉戌 | 天使在辰酉戌较不利 | gate | adversity_intensity | increase | COMPATIBILITY_RELATION | ADD_CANDIDATE
MC01-021 | SRC-ZZ-002 | 231-232 | 天伤天使 | 流禄 | 阳年生人且与伤使同宫 | 流禄与伤使同宫被源文列为疾病传统投影 | projection | health_case | increase | L3_PROJECTION | CASE_SUPPORT_ONLY
MC01-022 | SRC-ZZ-002 | 233 | 天刑天姚 | 天刑 | 一般 | 天刑主自律 | enhance | self_discipline | increase | LOCAL_STATE | ADD_CANDIDATE
MC01-023 | SRC-ZZ-002 | 233 | 天刑天姚 | 天姚 | 一般 | 天姚主放纵 | enhance | indulgence | increase | LOCAL_STATE | ADD_CANDIDATE
MC01-024 | SRC-ZZ-002 | 233 | 天刑天姚 | 天刑天姚 | 对星 | 天刑与天姚构成本质相反的对星 | structural_relation | polarity_pair | opposite | L0_STRUCTURE | ADD_CANDIDATE
MC01-025 | SRC-ZZ-002 | 233 | 天刑天姚 | 天刑 | 昌曲成对会照或同度 | 昌曲可使天刑的自律减少肃杀色彩 | transform | self_discipline_style | soften | DERIVED_RESPONSE | ADD_CANDIDATE
