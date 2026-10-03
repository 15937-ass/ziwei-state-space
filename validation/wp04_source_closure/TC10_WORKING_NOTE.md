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

TC10-026 | SRC-ZZ-002 | 224 | 廉贞化忌 | 巳亥廉贪 | 地空地劫 | 空劫会进一步放大忧郁与自寻困扰 | enhance | emotional_distress | increase | LOCAL_STATE | ADD_CANDIDATE
TC10-027 | SRC-ZZ-002 | 224 | 廉贞化忌 | 巳亥廉贪 | 理财 | 该结构资源流入与保存能力分离，呈现左手来右手去 | structural_relation | resource_inflow_vs_retention | decouple | L0_STRUCTURE | ADD_CANDIDATE
TC10-028 | SRC-ZZ-002 | 224 | 廉贞化忌 | 巳亥廉贪 | 奔波流浪 | 该结构显著提高生活与环境变动性 | enhance | mobility_instability | increase | LOCAL_STATE | ADD_CANDIDATE
TC10-029 | SRC-ZZ-002 | 224-225 | 巨门化忌 | 巨门化忌 | 一般 | 巨门原有是非口舌被化忌明显放大 | enhance | verbal_conflict | increase | LOCAL_STATE | ADD_CANDIDATE
TC10-030 | SRC-ZZ-002 | 224-225 | 巨门化忌 | 巨门化忌 | 非自招 | 是非可在并非主动招惹的情况下进入系统 | transform | exogenous_social_conflict | increase | DERIVED_RESPONSE | ADD_CANDIDATE
TC10-031 | SRC-ZZ-002 | 224-225 | 巨门化忌 | 巨门化忌 | 感情 | 感情发展容易出现不可预期的反覆与困扰 | transform | relationship_volatility | increase | DERIVED_RESPONSE | ADD_CANDIDATE
TC10-032 | SRC-ZZ-002 | 224-225 | 巨门化忌 | 巨门化忌 | 首次关系 | 源文把首次婚恋痛苦描述为长期难忘，属于传统关系案例且含持续性 | projection | relationship_case | persistent_distress | L3_PROJECTION | CASE_SUPPORT_ONLY
TC10-033 | SRC-ZZ-002 | 224-225 | 巨门化忌 | 巨门化忌 | 求全求美 | 完美主义提高事业不如理想时的失望与劳累 | transform | perfectionism_cost | increase | DERIVED_RESPONSE | ADD_CANDIDATE
TC10-034 | SRC-ZZ-002 | 224-225 | 巨门化忌 | 巨门化忌 | 陀罗同度 | 陀罗进一步放大执着、忧煎与劳累 | enhance | rumination_effort | increase | LOCAL_STATE | ADD_CANDIDATE
TC10-035 | SRC-ZZ-002 | 224-225 | 巨门化忌 | 子午巨门独坐 | 凶事 | 挫折可反成激发力并改善最终结果，形成“视凶实吉” | transform | adversity_to_outcome | improve_after_setback | DERIVED_RESPONSE | ADD_CANDIDATE
TC10-036 | SRC-ZZ-002 | 224-225 | 巨门化忌 | 子午巨门独坐 | 多次挫折 | 每次挫折可累积为结局改善，但过程压力仍存在 | time_scale_effect | repeated_setback_feedback | cumulative_improvement | TEMPORAL_GATE | ADD_CANDIDATE
TC10-037 | SRC-ZZ-002 | 224-225 | 巨门化忌 | 子午巨门独坐 | 午 vs 子 | 午宫是非更强，但激发效应也更明显 | gate | conflict_activation | higher_in_wu | COMPATIBILITY_RELATION | ADD_CANDIDATE
TC10-038 | SRC-ZZ-002 | 225 | 巨门化忌 | 丑未同巨 | 天同同时化权 | 该系统需直接联动天同化权规则 | structural_relation | cross_reference_rule | reuse_tiantong_quan | L0_STRUCTURE | ADD_CANDIDATE
TC10-039 | SRC-ZZ-002 | 225 | 巨门化忌 | 寅申巨阳 | 四化同会 | 四化同会仍不能消除人际关系损害 | structural_relation | multi_transform_vs_social_conflict | conflict_persists | L0_STRUCTURE | ADD_CANDIDATE
TC10-040 | SRC-ZZ-002 | 225 | 巨门化忌 | 寅申巨阳 | 上司关系 | 是非口舌可投影为上司冲突与权威关系摩擦 | projection | authority_conflict | increase | L3_PROJECTION | ADD_CANDIDATE
TC10-041 | SRC-ZZ-002 | 225 | 巨门化忌 | 寅申巨阳 | 口舌求财 | 口舌型工作可把冲突通道部分转为名誉与财禄 | transform | verbal_conflict_to_resource | convert | DERIVED_RESPONSE | ADD_CANDIDATE
TC10-042 | SRC-ZZ-002 | 225 | 巨门化忌 | 寅申巨阳 | 职业例示 | 律师等口舌求财职业属于传统应用场景 | projection | occupation_example | communication_role | L3_PROJECTION | CASE_SUPPORT_ONLY
TC10-043 | SRC-ZZ-002 | 225 | 巨门化忌 | 卯酉机巨 | 天机化科 | 该系统直接联动天机化科规则 | structural_relation | cross_reference_rule | reuse_tianji_ke | L0_STRUCTURE | ADD_CANDIDATE
TC10-044 | SRC-ZZ-002 | 225 | 巨门化忌 | 辰戌巨门独坐 | 罗网 | 罗网中化忌反而最明显呈现“视凶实吉” | transform | constraint_to_favorable_outcome | increase | DERIVED_RESPONSE | ADD_CANDIDATE
TC10-045 | SRC-ZZ-002 | 225 | 巨门化忌 | 辰戌巨门独坐 | 过程成本 | 最终结果改善并不消除排解辛苦、忧虑与是非 | structural_relation | outcome_vs_process_cost | decouple | L0_STRUCTURE | ADD_CANDIDATE
TC10-046 | SRC-ZZ-002 | 225 | 巨门化忌 | 辰戌巨门独坐 | 火铃或空劫 | 火铃空劫可进一步加强口舌求财适配 | gate | communication_income_channel | increase | STRUCTURAL_GATE | ADD_CANDIDATE
TC10-047 | SRC-ZZ-002 | 225 | 巨门化忌 | 辰戌巨门独坐 | 排难解纷 | 事业可因替人排难解纷而佳，但生活宁静度下降 | transform | problem_solving_vs_calmness | career_up_calmness_down | DERIVED_RESPONSE | ADD_CANDIDATE
TC10-048 | SRC-ZZ-002 | 225 | 巨门化忌 | 巳亥巨门独坐 | 六亲 vs 是非 | 六亲损害较轻时，是非口舌与感情波折仍可很重 | structural_relation | kinship_damage_vs_conflict | decouple | L0_STRUCTURE | ADD_CANDIDATE
TC10-049 | SRC-ZZ-002 | 225 | 巨门化忌 | 巳亥巨门独坐 | 外部观感 vs 当事体验 | 外界可视关系良好，而当事人主观不满仍可能存在 | structural_relation | external_relationship_quality_vs_subjective_satisfaction | decouple | L0_STRUCTURE | ADD_CANDIDATE
TC10-050 | SRC-ZZ-002 | 225 | 巨门化忌 | 巳亥巨门独坐 | 中年关系变化 | 源文给出中年感情变化的传统案例投影 | projection | relationship_case | midlife_change | L3_PROJECTION | CASE_SUPPORT_ONLY

TC10-051 | SRC-ZZ-002 | 225-226 | 天机化忌 | 天机化忌 | 灵动 | 化忌削弱灵动与机动性，增加受阻和失机 | transform | adaptive_mobility | decrease | DERIVED_RESPONSE | ADD_CANDIDATE
TC10-052 | SRC-ZZ-002 | 225-226 | 天机化忌 | 天机化忌 | 计划 | 计划能力可转为计划失误或延误 | transform | planning_quality | decrease | DERIVED_RESPONSE | ADD_CANDIDATE
TC10-053 | SRC-ZZ-002 | 225-226 | 天机化忌 | 天机化忌 | 思考 | 思考可转为过度思虑甚至焦虑 | transform | cognition_to_anxiety | increase | DERIVED_RESPONSE | ADD_CANDIDATE
TC10-054 | SRC-ZZ-002 | 225-226 | 天机化忌 | 天机化忌 | 疾厄宫 | 失眠、神经衰弱等为传统健康投影 | projection | health_case | neuropsychological_symptoms | L3_PROJECTION | CASE_SUPPORT_ONLY
TC10-055 | SRC-ZZ-002 | 225-226 | 天机化忌 | 天机化忌加煞曜 | 同躔 | 煞曜会放大神经性疾病类传统投影 | projection | health_case | neurological_risk_up | L3_PROJECTION | CASE_SUPPORT_ONLY
TC10-056 | SRC-ZZ-002 | 225-226 | 天机化忌 | 天机化忌 | 诽谤攻击竞争 | 面对外部攻击若持续对抗，风波易连锁升级 | transform | conflict_feedback | positive_escalation | DERIVED_RESPONSE | ADD_CANDIDATE
TC10-057 | SRC-ZZ-002 | 225-226 | 天机化忌 | 天机化忌 | 以不变应万变 | 降低反应强度可使风波更容易平息 | gate | conflict_damping | increase_by_nonreaction | STRUCTURAL_GATE | ADD_CANDIDATE
TC10-058 | SRC-ZZ-002 | 226 | 天机化忌 | 子午天机独坐 | 思维 | 简单问题容易被复杂化并导致计划错误 | transform | cognitive_complexification | increase | DERIVED_RESPONSE | ADD_CANDIDATE
TC10-059 | SRC-ZZ-002 | 226 | 天机化忌 | 子午天机独坐 | 工作组织 | 无事奔忙与工作忙乱欠条理可同时增加 | transform | work_disorganization | increase | DERIVED_RESPONSE | ADD_CANDIDATE
TC10-060 | SRC-ZZ-002 | 226 | 天机化忌 | 子午天机独坐 | 压力 | 惊恐、恐吓、恶性竞争等具体形式可统一视作压力输入 | structural_relation | pressure_input | generalized | L0_STRUCTURE | ADD_CANDIDATE
TC10-061 | SRC-ZZ-002 | 226 | 天机化忌 | 子午天机独坐 | 煞刑并照 | 煞刑会放大健康后遗症类传统投影，午宫较子宫重 | projection | health_case | higher_in_wu | L3_PROJECTION | CASE_SUPPORT_ONLY
TC10-062 | SRC-ZZ-002 | 226 | 天机化忌 | 丑未天机独坐 | 天梁相对 | 麻烦最终可化解，但精神成本很高 | transform | problem_resolution_vs_mental_cost | resolution_preserved_cost_up | DERIVED_RESPONSE | ADD_CANDIDATE
TC10-063 | SRC-ZZ-002 | 226 | 天机化忌 | 丑未天机独坐 | 计划估计错误 | 突发麻烦常与计划失误或估计错误形成因果链 | transform | planning_error_to_problem | increase | DERIVED_RESPONSE | ADD_CANDIDATE

TC10-064 | SRC-ZZ-002 | 226 | 天机化忌 | 丑未天机独坐 | 婚姻例示 | 源文给出配偶出锋头或夫妻不和的传统关系投影 | projection | relationship_case | conflict | L3_PROJECTION | CASE_SUPPORT_ONLY
TC10-065 | SRC-ZZ-002 | 226 | 天机化忌 | 寅申机阴 | 太阴同时化权 | 该系统直接联动太阴化权规则 | structural_relation | cross_reference_rule | reuse_taiyin_quan | L0_STRUCTURE | ADD_CANDIDATE
TC10-066 | SRC-ZZ-002 | 226 | 天机化忌 | 卯酉机巨 | 破荡本质 | 化忌进一步放大不守一业与见异思迁 | enhance | occupational_instability | increase | LOCAL_STATE | ADD_CANDIDATE
TC10-067 | SRC-ZZ-002 | 226 | 天机化忌 | 卯酉机巨 | 主观体验 | 高频变动可被当事人解释为怀才不遇，客观路径与主观评价需分离 | structural_relation | mobility_vs_self_appraisal | decouple | L0_STRUCTURE | ADD_CANDIDATE
TC10-068 | SRC-ZZ-002 | 226 | 天机化忌 | 卯酉机巨 | 语言 | 语言失误易集中在重要节点，增加关键决策风险 | transform | communication_error_at_critical_points | increase | DERIVED_RESPONSE | ADD_CANDIDATE
TC10-069 | SRC-ZZ-002 | 226 | 天机化忌 | 卯酉机巨 | 口舌求财 | 即使化忌，口舌型工作仍可作为适配通道 | gate | communication_income_channel | remain_available | STRUCTURAL_GATE | ADD_CANDIDATE
TC10-070 | SRC-ZZ-002 | 226 | 天机化忌 | 辰戌机梁 | 阴阳化吉会照 | 吉化会照能保留整体力量，使主要问题集中为天梁反复排解 | transform | system_support_vs_problem_load | support_preserved_resolution_cost_up | DERIVED_RESPONSE | ADD_CANDIDATE
TC10-071 | SRC-ZZ-002 | 226 | 天机化忌 | 辰戌机梁 | 流离与举棋不定 | 思想浮动、犹疑与处事反覆共同增加 | enhance | indecision_and_instability | increase | LOCAL_STATE | ADD_CANDIDATE
TC10-072 | SRC-ZZ-002 | 226 | 天机化忌 | 辰戌机梁 | 预感 | 预感能力可因化忌转成过虑并导致决断错误 | transform | intuition_to_overthinking | increase | DERIVED_RESPONSE | ADD_CANDIDATE
TC10-073 | SRC-ZZ-002 | 226 | 天机化忌 | 辰戌机梁 | 戌 vs 辰 | 戌宫过虑与误判倾向更明显 | gate | overthinking_risk | higher_in_xu | COMPATIBILITY_RELATION | ADD_CANDIDATE
TC10-074 | SRC-ZZ-002 | 226 | 天机化忌 | 巳亥天机独坐 | 机关错用 | 过度机巧或错误运用策略会同时损害事业与感情 | transform | strategic_misuse | increase | DERIVED_RESPONSE | ADD_CANDIDATE
TC10-075 | SRC-ZZ-002 | 226 | 天机化忌 | 巳亥天机独坐 | 平常心 | 降低过度操控可显著减少波折困扰 | gate | volatility | decrease_by_nonmanipulation | STRUCTURAL_GATE | ADD_CANDIDATE

TC10-076 | SRC-ZZ-002 | 226-227 | 文曲化忌 | 文曲化忌 | 一般 | 文曲化忌首先削弱原有文曲性质，并可由是非引出挫折 | transform | wenqu_function_quality | decrease | DERIVED_RESPONSE | ADD_CANDIDATE
TC10-077 | SRC-ZZ-002 | 226-227 | 文曲化忌 | 文曲化忌 | 口才 | 口才优势可转为语言失误 | transform | verbal_accuracy | decrease | DERIVED_RESPONSE | ADD_CANDIDATE
TC10-078 | SRC-ZZ-002 | 226-227 | 文曲化忌 | 文曲化忌 | 文书契约 | 文书和契约错误会增加麻烦与损失 | transform | document_contract_error | increase | DERIVED_RESPONSE | ADD_CANDIDATE
TC10-079 | SRC-ZZ-002 | 226-227 | 文曲化忌 | 文曲化忌 | 异性欣赏 | 原本的吸引力可转为误会与感情风波 | transform | attraction_to_relationship_conflict | increase | DERIVED_RESPONSE | ADD_CANDIDATE
TC10-080 | SRC-ZZ-002 | 226-227 | 文曲化忌 | 文曲化忌 | 杂学才艺 | 化忌不等于杂学才艺增强，二者需解耦 | structural_relation | miscellaneous_talent_vs_ji | decouple | L0_STRUCTURE | ADD_CANDIDATE
TC10-081 | SRC-ZZ-002 | 226-227 | 文曲化忌 | 文曲化忌 | 语文能力 | 化忌可抵消语言天赋并提高被批评风险 | transform | language_skill_and_criticism | skill_down_criticism_up | DERIVED_RESPONSE | ADD_CANDIDATE
TC10-082 | SRC-ZZ-002 | 226-227 | 文曲化忌 | 文曲化忌 | 金钱 | 文曲化忌可直接形成受骗、空头支票等物质损失通道 | transform | financial_loss | increase | DERIVED_RESPONSE | ADD_CANDIDATE
TC10-083 | SRC-ZZ-002 | 226-227 | 文曲化忌 | 文曲 vs 文昌化忌 | 金钱责任 | 文曲的物质损失属性强于文昌化忌，二者责任来源不同 | mechanism_comparison | document_finance_failure_mode | differentiate | MECHANISM_COMPARISON | ADD_CANDIDATE
TC10-084 | SRC-ZZ-002 | 226-227 | 文曲化忌 | 文曲化忌 | 感情与钱财 | 感情和财务风险可耦合为复杂困扰 | transform | relationship_finance_coupling | increase | DERIVED_RESPONSE | ADD_CANDIDATE
TC10-085 | SRC-ZZ-002 | 226-227 | 文曲化忌 | 文曲化忌 | 幻想 | 幻想与执着会提高怀才不遇的主观感受 | transform | fantasy_to_frustrated_self_appraisal | increase | DERIVED_RESPONSE | ADD_CANDIDATE
TC10-086 | SRC-ZZ-002 | 227 | 天同化忌 | 天同化忌 | 一般 | 天同以情绪为核心，化忌主要增加情绪不稳定 | enhance | emotional_instability | increase | LOCAL_STATE | ADD_CANDIDATE
TC10-087 | SRC-ZZ-002 | 227 | 天同化忌 | 天同化忌 | 入庙 | 入庙时情绪不稳定虽增加但整体危害相对较轻 | gate | adverse_intensity | attenuate_in_dignity | COMPATIBILITY_RELATION | ADD_CANDIDATE
TC10-088 | SRC-ZZ-002 | 227 | 天同化忌 | 天同化忌 | 白手兴家 | 化忌会加强中年经历艰辛并被迫独立的路径 | time_scale_effect | independence_after_adversity | increase | TEMPORAL_GATE | ADD_CANDIDATE

TC10-089 | SRC-ZZ-002 | 227 | 天同化忌 | 天同化忌 | 感情 | 感情困扰可干扰事业专注 | transform | relationship_distress_to_career | increase | DERIVED_RESPONSE | ADD_CANDIDATE
