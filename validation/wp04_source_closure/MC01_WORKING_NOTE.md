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

MC01-026 | SRC-ZZ-002 | 233 | 天刑天姚 | 天刑 | 寅卯酉戌入庙见昌曲 | 入庙并见昌曲时可形成偏纪律、制度或行政执行型角色 | projection | occupation_example | disciplined_administration | L3_PROJECTION | CASE_SUPPORT_ONLY
MC01-027 | SRC-ZZ-002 | 233 | 天刑天姚 | 太阳巨门天刑 | 同会 | 太阳巨门与天刑同会可强化刑法、规则执行的职业适配 | transform | legal_regulatory_orientation | increase | DERIVED_RESPONSE | ADD_CANDIDATE
MC01-028 | SRC-ZZ-002 | 233 | 天刑天姚 | 太阳天梁天刑 | 再见煞忌 | 太阳天梁与天刑见煞忌时更偏争讼而非执掌刑法 | mechanism_comparison | legal_role_vs_litigation | shift_to_litigation | MECHANISM_COMPARISON | ADD_CANDIDATE
MC01-029 | SRC-ZZ-002 | 233 | 天刑天姚 | 紫微贪狼 | 天刑同度或会合 | 天刑可抑制紫贪的桃花犯主并增强自律 | transform | desire_self_regulation | increase | DERIVED_RESPONSE | ADD_CANDIDATE
MC01-030 | SRC-ZZ-002 | 233 | 天刑天姚 | 武曲七杀 | 擎羊加天刑 | 结构可导向使用器械或利器的职业场景 | projection | occupation_example | tool_or_surgical_role | L3_PROJECTION | CASE_SUPPORT_ONLY
MC01-031 | SRC-ZZ-002 | 233 | 天刑天姚 | 天刑 | 丑未 | 丑未天刑带较强孤克色彩 | enhance | social_isolation | increase | LOCAL_STATE | ADD_CANDIDATE
MC01-032 | SRC-ZZ-002 | 233 | 天刑天姚 | 天刑 | 丑未六亲宫 | 六亲关系风险需依具体六亲宫进一步判定 | structural_relation | kinship_context_dependence | require_palace_context | L0_STRUCTURE | ADD_CANDIDATE
MC01-033 | SRC-ZZ-002 | 233 | 天刑天姚 | 天刑 | 疾厄宫且煞忌冲会 | 源文给出先天残疾或身体异常等传统投影 | projection | health_case | traditional_disability_case | L3_PROJECTION | CASE_SUPPORT_ONLY
MC01-034 | SRC-ZZ-002 | 233 | 天刑天姚 | 运限疾厄宫天刑 | 流羊冲会 | 源文将手术作为可能的运限健康投影 | projection | health_case | surgical_event | L3_PROJECTION | CASE_SUPPORT_ONLY
MC01-035 | SRC-ZZ-002 | 233 | 天刑天姚 | 天姚 | 一般 | 天姚的桃花带偶遇或迅速吸引的性质 | enhance | spontaneous_attraction | increase | LOCAL_STATE | ADD_CANDIDATE
MC01-036 | SRC-ZZ-002 | 233 | 天刑天姚 | 天姚 | 咸池大耗沐浴 | 咸池、大耗、沐浴会放大天姚的桃花与放纵性质 | enhance | indulgence_attraction | increase | LOCAL_STATE | ADD_CANDIDATE
MC01-037 | SRC-ZZ-002 | 233 | 天刑天姚 | 天姚 | 红鸾天喜 | 红鸾天喜可缓和天姚的放纵性，使结果偏受欢迎 | transform | attraction_style | soften | DERIVED_RESPONSE | ADD_CANDIDATE
MC01-038 | SRC-ZZ-002 | 233 | 天刑天姚 | 天姚 | 丑未守命 | 丑未守命时天姚的享乐与风月倾向较易增强 | gate | indulgence | increase_in_chou_wei | COMPATIBILITY_RELATION | ADD_CANDIDATE
MC01-039 | SRC-ZZ-002 | 233 | 天刑天姚 | 昌曲天姚 | 同度 | 昌曲与天姚同度可增强风流自赏性质 | transform | aesthetic_self_display | increase | DERIVED_RESPONSE | ADD_CANDIDATE
MC01-040 | SRC-ZZ-002 | 233 | 天刑天姚 | 昌曲天刑 | 同度 | 昌曲与天刑同度更偏脚踏实地，与昌曲天姚形成对照 | mechanism_comparison | literary_modifier_style | disciplined_vs_indulgent | MECHANISM_COMPARISON | ADD_CANDIDATE
MC01-041 | SRC-ZZ-002 | 233 | 天刑天姚 | 天姚 | 会煞忌 | 煞忌会放大因桃花引发麻烦的风险 | gate | attraction_adversity | increase | STRUCTURAL_GATE | ADD_CANDIDATE
MC01-042 | SRC-ZZ-002 | 233 | 天刑天姚 | 天姚 | 财帛宫 | 源文将酒色财气导致资源损失作为传统投影 | projection | financial_case | attraction_related_loss | L3_PROJECTION | CASE_SUPPORT_ONLY
MC01-043 | SRC-ZZ-002 | 233 | 天刑天姚 | 天姚 | 田宅宫 | 源文将祖业破散作为传统宫位投影 | projection | property_case | ancestral_property_loss | L3_PROJECTION | CASE_SUPPORT_ONLY
MC01-044 | SRC-ZZ-002 | 233 | 天刑天姚 | 天姚 | 夫妻宫 | 源文将重婚再娶作为传统关系投影 | projection | relationship_case | repeated_union | L3_PROJECTION | CASE_SUPPORT_ONLY
MC01-045 | SRC-ZZ-002 | 233 | 天刑天姚 | 天姚 | 福德宫 | 天姚在福德宫可增加思想混乱 | transform | mental_order | decrease | DERIVED_RESPONSE | ADD_CANDIDATE
MC01-046 | SRC-ZZ-002 | 233 | 天刑天姚 | 天姚 | 迁移宫且吉曜正曜佳 | 外出环境可提高机遇并获得外乡助力 | transform | mobility_opportunity | increase | DERIVED_RESPONSE | ADD_CANDIDATE
MC01-047 | SRC-ZZ-002 | 233 | 天刑天姚 | 天姚 | 流年同沐浴咸池大耗 | 流年可触发带苦衷性质的感情事件 | layer_interaction | relationship_event | activate | TEMPORAL_LAYER | CASE_SUPPORT_ONLY
MC01-048 | SRC-ZZ-002 | 233 | 天哭天虚 | 天哭 | 一般 | 天哭主刑克忧伤 | enhance | sorrow | increase | LOCAL_STATE | ADD_CANDIDATE
MC01-049 | SRC-ZZ-002 | 233 | 天哭天虚 | 天虚 | 一般 | 天虚主空虚忧虑 | enhance | emptiness_anxiety | increase | LOCAL_STATE | ADD_CANDIDATE
MC01-050 | SRC-ZZ-002 | 233 | 天哭天虚 | 天哭 | 福德宫 | 天哭的情感痛苦性质在福德宫更不利 | gate | inner_distress | increase_in_fude | STRUCTURAL_GATE | ADD_CANDIDATE

MC01-051 | SRC-ZZ-002 | 233 | 天哭天虚 | 天虚 | 财帛宫 | 天虚在财帛宫强化物质缺乏与资源不足 | gate | material_sufficiency | decrease_in_wealth_palace | STRUCTURAL_GATE | ADD_CANDIDATE
MC01-052 | SRC-ZZ-002 | 233 | 天哭天虚 | 天虚 | 疾厄宫 | 传统资料将其作为身体虚耗类投影 | projection | health_case | depletion_related_weakness | L3_PROJECTION | CASE_SUPPORT_ONLY
MC01-053 | SRC-ZZ-002 | 233 | 天哭天虚 | 哭虚 | 禄存或化禄同度且正曜财气旺 | 得财可同步提高外部知名度 | transform | resource_gain_to_visibility | increase | DERIVED_RESPONSE | ADD_CANDIDATE
MC01-054 | SRC-ZZ-002 | 233 | 天哭天虚 | 哭虚 | 卯申财气旺 | 卯申是源文给出的因财增名条件 | gate | resource_to_reputation_conversion | increase_in_mao_shen | COMPATIBILITY_RELATION | ADD_CANDIDATE
MC01-055 | SRC-ZZ-002 | 233 | 天哭天虚 | 哭虚 | 天同星系守兄弟宫 | 传统资料给出特定姻亲关系不和投影 | projection | kinship_case | inlaw_conflict | L3_PROJECTION | CASE_SUPPORT_ONLY

MC01-056 | SRC-ZZ-002 | 234 | 红鸾天喜 | 红鸾 | 一般 | 红鸾主婚姻 | structural_relation | marriage_signal | associate | L0_STRUCTURE | ADD_CANDIDATE
MC01-057 | SRC-ZZ-002 | 234 | 红鸾天喜 | 天喜 | 一般 | 天喜主生育 | structural_relation | fertility_signal | associate | L0_STRUCTURE | ADD_CANDIDATE
MC01-058 | SRC-ZZ-002 | 234 | 红鸾天喜 | 红鸾天喜 | 永远相对 | 两星性质会互相影响，不能完全拆开使用 | structural_relation | paired_modifier | coupled | L0_STRUCTURE | ADD_CANDIDATE
MC01-059 | SRC-ZZ-002 | 234 | 红鸾天喜 | 红鸾天喜 | 命宫例示 | 源文以俏艳、冷艳区分两星外在气质，保留为传统案例 | projection | appearance_case | differentiated_style | L3_PROJECTION | CASE_SUPPORT_ONLY
MC01-060 | SRC-ZZ-002 | 234 | 红鸾天喜 | 鸾喜 | 子女宫 | 源文给出传统子女结构投影 | projection | offspring_case | traditional_projection | L3_PROJECTION | CASE_SUPPORT_ONLY
MC01-061 | SRC-ZZ-002 | 234 | 红鸾天喜 | 紫微加鸾喜 | 再见吉曜 | 年龄阶段改变其投影：少年偏婚姻，老年偏荣衔 | time_scale_effect | age_dependent_projection | branch_by_age | TEMPORAL_GATE | ADD_CANDIDATE
MC01-062 | SRC-ZZ-002 | 234 | 红鸾天喜 | 鸾喜 | 财帛宫正曜吉 | 可形成小额喜庆型资源收益 | transform | celebratory_income | increase | DERIVED_RESPONSE | ADD_CANDIDATE
MC01-063 | SRC-ZZ-002 | 234 | 红鸾天喜 | 鸾喜 | 喜庆行业 | 与喜庆场景结合可提高职业适配 | projection | occupation_example | celebration_related_business | L3_PROJECTION | CASE_SUPPORT_ONLY
MC01-064 | SRC-ZZ-002 | 234 | 红鸾天喜 | 流年鸾喜 | 命宫或夫妻宫 | 流年鸾喜可作为婚育应期候选信号 | layer_interaction | relationship_family_timing | activate | TEMPORAL_LAYER | ADD_CANDIDATE
MC01-065 | SRC-ZZ-002 | 234 | 红鸾天喜 | 流年鸾喜 | 正曜星系不稳定 | 若正曜不稳则应期可延后，鸾喜不能单独决定事件发生 | gate | event_timing | delay_if_base_unstable | STRUCTURAL_GATE | ADD_CANDIDATE
