# TC10

Working checkpoint.
## TC10 structured review
schema: id | source_id | page | section | subject | condition | claim | operator | target | change | layer | disposition
reviewer: gpt-5.6-sol/wp04-tc10
reviewed_at: 2026-10-03
source_epistemic: EXPLICIT
review_status: SOURCE_SPAN_VERIFIED
normalization: SOURCE_PRESERVING

TC10-001 | SRC-ZZ-002 | 223 | 廉贞化忌 | 廉贞化忌 | 一般 | 廉贞化忌可表现为六亲或感情挫折 | transform | relationship_distress | increase | DERIVED_RESPONSE | ADD_CANDIDATE
TC10-002 | SRC-ZZ-002 | 223 | 廉贞化忌 | 廉贞化忌 | 挫折持续 | 源文明示此类挫折具有持续、非事过境迁即消失的性质 | history_marker | acquired_emotional_disposition | persist | ACQUIRED_DISPOSITION | ADD_CANDIDATE
TC10-003 | SRC-ZZ-002 | 223 | 廉贞化忌 | 廉贞化忌 | 科文诸曜 | 忧愁可转化为文艺性情绪并增加艺术深度 | transform | emotional_distress_to_artistic_depth | increase | DERIVED_RESPONSE | ADD_CANDIDATE
TC10-004 | SRC-ZZ-002 | 223 | 廉贞化忌 | 廉贞化忌 | 煞曜同躔 | 煞曜会使文艺性忧愁更易转为艺术不得意 | gate | artistic_realization | decrease_with_malefics | STRUCTURAL_GATE | ADD_CANDIDATE
TC10-005 | SRC-ZZ-002 | 223 | 廉贞化忌 | 廉贞化忌 | 六亲互动 | 源文把受骗尤其受六亲欺骗列为感情挫折的一种来源 | transform | trust_betrayal | increase | DERIVED_RESPONSE | ADD_CANDIDATE
TC10-006 | SRC-ZZ-002 | 223 | 廉贞化忌 | 廉相对破 | 煞刑并集 | 感情挫折强度可被廉相对破及煞刑进一步放大 | gate | relationship_distress | amplify | STRUCTURAL_GATE | ADD_CANDIDATE
TC10-007 | SRC-ZZ-002 | 223 | 廉贞化忌 | 廉贞化忌 | 替人谋事 | 替人谋事可能反招怨，形成 prosocial action → negative feedback 的反转 | transform | social_help_feedback | negative_reversal | DERIVED_RESPONSE | ADD_CANDIDATE
TC10-008 | SRC-ZZ-002 | 223 | 廉贞化忌 | 廉贞化忌 | 不量力而为 | 超出能力边界会增加自尊受损 | gate | self_esteem_risk | increase_by_overreach | STRUCTURAL_GATE | ADD_CANDIDATE
TC10-009 | SRC-ZZ-002 | 223 | 廉贞化忌 | 廉贞化忌 | 身体投影 | 源文将脓血、意外、手术等列为身体投影 | projection | health_case | injury_or_surgery | L3_PROJECTION | CASE_SUPPORT_ONLY
TC10-010 | SRC-ZZ-002 | 223 | 廉贞化忌 | 廉贞化忌 | 疾厄宫 | 血病、性病等属于疾厄宫传统具体投影 | projection | health_case | blood_or_reproductive_disorder | L3_PROJECTION | CASE_SUPPORT_ONLY
TC10-011 | SRC-ZZ-002 | 223 | 廉贞化忌 | 子午廉相 | 强出头 | 强自出头会提高损失或破败风险 | gate | overexposure_risk | increase | STRUCTURAL_GATE | ADD_CANDIDATE
TC10-012 | SRC-ZZ-002 | 223 | 廉贞化忌 | 子午廉相 | 合作 | 该结构不利合作，合作会成为额外风险通道 | gate | collaboration_stability | decrease | STRUCTURAL_GATE | ADD_CANDIDATE
TC10-013 | SRC-ZZ-002 | 223 | 廉贞化忌 | 子午廉相 | 财源 | 感情和合作风险存在时，资源生成与积存仍可维持较好 | structural_relation | relationship_risk_vs_resource | decouple | L0_STRUCTURE | ADD_CANDIDATE
TC10-014 | SRC-ZZ-002 | 223 | 廉贞化忌 | 子午廉相 | 保守策略 | 不急求成与保守可降低破败概率 | gate | loss_risk | decrease_by_conservatism | STRUCTURAL_GATE | ADD_CANDIDATE
TC10-015 | SRC-ZZ-002 | 223-224 | 廉贞化忌 | 丑未廉杀 | 宫位差异 | 丑宫较未宫顺遂，宫位改变结构实现质量 | gate | system_quality | enhance_in_chou | COMPATIBILITY_RELATION | ADD_CANDIDATE
TC10-016 | SRC-ZZ-002 | 224 | 廉贞化忌 | 丑未廉杀 | 武职 | 化忌使武职风险提高，职业适配受到限制 | projection | occupation_example | martial_role_risk | L3_PROJECTION | CASE_SUPPORT_ONLY
TC10-017 | SRC-ZZ-002 | 224 | 廉贞化忌 | 丑未廉杀 | 煞刑 | 煞刑会增加人生艰辛与意外风险 | enhance | adversity_intensity | increase | LOCAL_STATE | ADD_CANDIDATE
TC10-018 | SRC-ZZ-002 | 224 | 廉贞化忌 | 丑未廉杀 | 应酬支出 | 交际支出可能增加却得不到预期效果，形成低效资源消耗 | transform | social_spending_efficiency | decrease | DERIVED_RESPONSE | ADD_CANDIDATE
TC10-019 | SRC-ZZ-002 | 224 | 廉贞化忌 | 寅申廉贞独坐 | 忧郁色彩 | 该结构增加忧郁与感情敏感性 | enhance | depressive_affect | increase | LOCAL_STATE | ADD_CANDIDATE
TC10-020 | SRC-ZZ-002 | 224 | 廉贞化忌 | 寅申廉贞独坐 | 资助友人 | 对外资助倾向增强而家庭储蓄重视度下降 | transform | external_giving_vs_household_saving | giving_up_saving_down | DERIVED_RESPONSE | ADD_CANDIDATE
TC10-021 | SRC-ZZ-002 | 224 | 廉贞化忌 | 卯酉廉破 | 暴败 | 结构具有暴败风险，卯宫较酉宫严重 | gate | collapse_risk | higher_in_mao | STRUCTURAL_GATE | ADD_CANDIDATE
TC10-022 | SRC-ZZ-002 | 224 | 廉贞化忌 | 卯酉廉破 | 大额资金经手 | 可出现阶段性大量资金经手后再转为困乏的资源波动 | time_scale_effect | resource_scale | boom_then_contraction | TEMPORAL_GATE | ADD_CANDIDATE
TC10-023 | SRC-ZZ-002 | 224 | 廉贞化忌 | 辰戌廉府 | 罗网 | 罗网中化忌反可增加斗志，显示 constraint → activation 反转 | transform | constraint_to_drive | increase | DERIVED_RESPONSE | ADD_CANDIDATE
TC10-024 | SRC-ZZ-002 | 224 | 廉贞化忌 | 辰戌廉府 | 成败不一 | 外部成败波动与内部心境开朗可以并存 | structural_relation | outcome_vs_affect | decouple | L0_STRUCTURE | ADD_CANDIDATE
TC10-025 | SRC-ZZ-002 | 224 | 廉贞化忌 | 巳亥廉贪 | 文曜 | 文曜可把深度忧郁部分转化为文艺情绪 | transform | distress_to_artistic_expression | increase | DERIVED_RESPONSE | ADD_CANDIDATE
