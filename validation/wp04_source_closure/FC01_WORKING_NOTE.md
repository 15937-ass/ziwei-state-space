# FC01

Working flow-star source-review checkpoint.
status: ACTIVE

## FC01 structured review
schema: id | source_id | page | section | subject | condition | claim | operator | target | change | layer | disposition
reviewer: gpt-5.6-sol/wp04-fc01
reviewed_at: 2026-10-03
source_epistemic: EXPLICIT
review_status: SOURCE_SPAN_VERIFIED
normalization: SOURCE_PRESERVING

FC01-001 | SRC-ZZ-002 | 239 | 流曜总论 | 流曜体系 | 一般 | 流曜分为辅佐煞化流曜与小限专用流曜两套 | structural_relation | flow_star_system | split_into_two | L0_STRUCTURE | ADD_CANDIDATE
FC01-002 | SRC-ZZ-002 | 239 | 流曜总论 | 辅佐煞化流曜 | 一般 | 该套流曜主要用于推断大运或流年十二宫 | structural_relation | temporal_scope | decade_and_year | L0_STRUCTURE | ADD_CANDIDATE
FC01-003 | SRC-ZZ-002 | 239 | 流曜总论 | 小限流曜 | 一般 | 另一套流曜专用于小限推断 | structural_relation | temporal_scope | small_limit | L0_STRUCTURE | ADD_CANDIDATE
FC01-004 | SRC-ZZ-002 | 239 | 流曜总论 | 辅佐煞化流曜 | 组成 | 包含流魁流钺、流昌流曲、流禄流马、流四化、流羊流陀及流年年解 | structural_relation | flow_star_inventory | defined | L0_STRUCTURE | ADD_CANDIDATE
FC01-005 | SRC-ZZ-002 | 239 | 流曜总论 | 辅佐煞化流曜 | 语义继承 | 流曜意义与对应辅佐煞化本身的意义相同 | structural_relation | semantic_inheritance | inherit_base_meaning | L0_STRUCTURE | ADD_CANDIDATE
FC01-006 | SRC-ZZ-002 | 239 | 流曜总论 | 流曜 | 冲起原局辅佐煞化 | 流曜冲起原局对应曜时双方力量加强 | layer_interaction | natal_flow_activation | strengthen | TEMPORAL_LAYER | ADD_CANDIDATE
FC01-007 | SRC-ZZ-002 | 239 | 流曜总论 | 冲起机制 | 大运流年 | 流曜冲起原局可作为推断变动的枢纽 | layer_interaction | change_trigger | activate | TEMPORAL_LAYER | ADD_CANDIDATE
FC01-008 | SRC-ZZ-002 | 239 | 流曜总论 | 小限流曜 | 三组 | 小限流曜分博士十二神、将前十二神、岁前十二神，并须配合流年十二宫检视 | structural_relation | small_limit_review_dependency | require_annual_palaces | L0_STRUCTURE | ADD_CANDIDATE
FC01-009 | SRC-ZZ-002 | 239 | 博士十二神 | 博士 | 一般 | 博士主聪明 | enhance | intelligence | increase | LOCAL_STATE | ADD_CANDIDATE
FC01-010 | SRC-ZZ-002 | 239 | 博士十二神 | 博士 | 流年小限与辅佐诸曜同会 | 博士与辅佐诸曜同会可增加名誉表现 | transform | reputation | increase | TEMPORAL_LAYER | ADD_CANDIDATE
FC01-011 | SRC-ZZ-002 | 239 | 博士十二神 | 博士 | 一般 | 博士主心境佳 | enhance | positive_mood | increase | LOCAL_STATE | ADD_CANDIDATE
FC01-012 | SRC-ZZ-002 | 239 | 博士十二神 | 力士 | 一般 | 力士主权势 | enhance | authority | increase | LOCAL_STATE | ADD_CANDIDATE
FC01-013 | SRC-ZZ-002 | 239 | 博士十二神 | 力士 | 与化权同度 | 力士与化权同度时权力表现加强 | gate | authority_realization | increase_with_huaquan | STRUCTURAL_GATE | ADD_CANDIDATE
FC01-014 | SRC-ZZ-002 | 239 | 博士十二神 | 青龙 | 一般 | 青龙主进财 | enhance | resource_inflow | increase | LOCAL_STATE | ADD_CANDIDATE
FC01-015 | SRC-ZZ-002 | 239 | 博士十二神 | 青龙 | 喜事情境 | 青龙尤其主因喜事进财 | transform | celebration_to_resource | increase | DERIVED_RESPONSE | ADD_CANDIDATE
FC01-016 | SRC-ZZ-002 | 239 | 博士十二神 | 小耗 | 一般 | 小耗主耗财 | enhance | resource_depletion | increase | LOCAL_STATE | ADD_CANDIDATE
FC01-017 | SRC-ZZ-002 | 239 | 博士十二神 | 小耗 | 一般 | 小耗尤其主遗失 | projection | loss_case | lost_property | L3_PROJECTION | CASE_SUPPORT_ONLY
FC01-018 | SRC-ZZ-002 | 239 | 博士十二神 | 将军 | 一般 | 将军主威福 | enhance | prestige_authority | increase | LOCAL_STATE | ADD_CANDIDATE
FC01-019 | SRC-ZZ-002 | 239 | 博士十二神 | 将军 | 一般 | 将军主得意 | enhance | subjective_success | increase | LOCAL_STATE | ADD_CANDIDATE
FC01-020 | SRC-ZZ-002 | 239 | 博士十二神 | 奏书 | 一般 | 奏书带喜庆性质 | enhance | celebration | increase | LOCAL_STATE | ADD_CANDIDATE
FC01-021 | SRC-ZZ-002 | 239 | 博士十二神 | 奏书 | 文字活动 | 奏书主因文字而进取 | transform | writing_to_advancement | increase | DERIVED_RESPONSE | ADD_CANDIDATE
FC01-022 | SRC-ZZ-002 | 239 | 博士十二神 | 奏书 | 词讼 | 奏书主词讼胜利 | projection | litigation_case | favorable | L3_PROJECTION | CASE_SUPPORT_ONLY
FC01-023 | SRC-ZZ-002 | 239 | 博士十二神 | 蜚廉 | 一般 | 蜚廉主小人 | enhance | hidden_social_interference | increase | LOCAL_STATE | ADD_CANDIDATE
FC01-024 | SRC-ZZ-002 | 239 | 博士十二神 | 蜚廉 | 一般 | 蜚廉带桃花性质 | enhance | attraction | increase | LOCAL_STATE | ADD_CANDIDATE
FC01-025 | SRC-ZZ-002 | 239 | 博士十二神 | 蜚廉 | 一般 | 蜚廉主受谗 | enhance | slander | increase | LOCAL_STATE | ADD_CANDIDATE

FC01-026 | SRC-ZZ-002 | 239 | 博士十二神 | 蜚廉 | 一般 | 蜚廉主购物 | transform | consumption_drive | increase | DERIVED_RESPONSE | ADD_CANDIDATE
FC01-027 | SRC-ZZ-002 | 239 | 博士十二神 | 喜神 | 一般 | 喜神主喜庆 | enhance | celebration | increase | LOCAL_STATE | ADD_CANDIDATE
FC01-028 | SRC-ZZ-002 | 239 | 博士十二神 | 喜神 | 一般 | 喜神亦主拖延 | enhance | delay | increase | LOCAL_STATE | ADD_CANDIDATE
FC01-029 | SRC-ZZ-002 | 239 | 博士十二神 | 喜神 | 喜事情境 | 喜神可使喜事延续 | time_scale_effect | positive_event_duration | extend | TEMPORAL_GATE | ADD_CANDIDATE
FC01-030 | SRC-ZZ-002 | 239 | 博士十二神 | 病符 | 一般 | 病符主小灾病 | projection | health_case | minor_illness | L3_PROJECTION | CASE_SUPPORT_ONLY
FC01-031 | SRC-ZZ-002 | 239 | 博士十二神 | 病符 | 一般 | 病符兼带是非性质 | enhance | social_friction | increase | LOCAL_STATE | ADD_CANDIDATE
FC01-032 | SRC-ZZ-002 | 239 | 博士十二神 | 大耗 | 一般 | 大耗主破耗 | enhance | resource_depletion | increase | LOCAL_STATE | ADD_CANDIDATE
FC01-033 | SRC-ZZ-002 | 239 | 博士十二神 | 大耗 | 一般 | 大耗主失物 | projection | loss_case | lost_property | L3_PROJECTION | CASE_SUPPORT_ONLY
FC01-034 | SRC-ZZ-002 | 239 | 博士十二神 | 大耗 | 一般 | 大耗主祖业不守 | projection | inheritance_case | discontinuity | L3_PROJECTION | CASE_SUPPORT_ONLY
FC01-035 | SRC-ZZ-002 | 239 | 博士十二神 | 大耗 | 与桃花诸曜同会 | 桃花同会可把大耗导向因色生灾 | transform | attraction_to_adversity | increase | DERIVED_RESPONSE | ADD_CANDIDATE
FC01-036 | SRC-ZZ-002 | 239 | 博士十二神 | 伏兵 | 一般 | 伏兵主暗算 | enhance | covert_harm | increase | LOCAL_STATE | ADD_CANDIDATE
FC01-037 | SRC-ZZ-002 | 239 | 博士十二神 | 伏兵 | 一般 | 伏兵主拖延受阻 | enhance | delay_obstruction | increase | LOCAL_STATE | ADD_CANDIDATE
FC01-038 | SRC-ZZ-002 | 239 | 博士十二神 | 官府 | 一般 | 官府主官非词讼 | projection | litigation_case | increase | L3_PROJECTION | CASE_SUPPORT_ONLY
FC01-039 | SRC-ZZ-002 | 239 | 博士十二神 | 官府 | 与化忌财星同度 | 官府与化忌财星同度可形成钱财纠纷 | transform | financial_dispute | increase | DERIVED_RESPONSE | ADD_CANDIDATE
FC01-040 | SRC-ZZ-002 | 239 | 博士十二神 | 官府 | 七杀擎羊同度又见白虎 | 该组合被源文列为刑杖类传统司法投影 | projection | legal_punishment_case | increase | L3_PROJECTION | CASE_SUPPORT_ONLY
FC01-041 | SRC-ZZ-002 | 239 | 将前十二神 | 将星 | 一般 | 将星主武贵 | enhance | martial_status | increase | LOCAL_STATE | ADD_CANDIDATE
FC01-042 | SRC-ZZ-002 | 239 | 将前十二神 | 将星 | 一般 | 将星主得意 | enhance | subjective_success | increase | LOCAL_STATE | ADD_CANDIDATE
FC01-043 | SRC-ZZ-002 | 239 | 将前十二神 | 将星 | 流日 | 流日逢将星可增加神采与表现状态 | layer_interaction | daily_presentation | increase | TEMPORAL_LAYER | ADD_CANDIDATE
FC01-044 | SRC-ZZ-002 | 239 | 将前十二神 | 将星 | 竞争 | 将星主竞争时得助力 | transform | competition_support | increase | DERIVED_RESPONSE | ADD_CANDIDATE
FC01-045 | SRC-ZZ-002 | 239 | 将前十二神 | 攀鞍 | 一般 | 攀鞍利功名 | enhance | achievement_reputation | increase | LOCAL_STATE | ADD_CANDIDATE
FC01-046 | SRC-ZZ-002 | 239 | 将前十二神 | 攀鞍 | 一般 | 攀鞍主近贵得势 | transform | access_to_status_support | increase | DERIVED_RESPONSE | ADD_CANDIDATE
FC01-047 | SRC-ZZ-002 | 239 | 将前十二神 | 岁驿 | 一般 | 岁驿利迁动 | enhance | mobility | increase | LOCAL_STATE | ADD_CANDIDATE
FC01-048 | SRC-ZZ-002 | 239 | 将前十二神 | 岁驿 | 与流禄或流化禄同度 | 岁驿与流禄类同度形成禄马交驰 | structural_relation | lu_ma_configuration | activate | L0_STRUCTURE | ADD_CANDIDATE
FC01-049 | SRC-ZZ-002 | 239 | 将前十二神 | 息神 | 一般 | 息神主消沉 | enhance | discouragement | increase | LOCAL_STATE | ADD_CANDIDATE
FC01-050 | SRC-ZZ-002 | 239 | 将前十二神 | 息神 | 一般 | 息神主丧志 | enhance | motivation_loss | increase | LOCAL_STATE | ADD_CANDIDATE
