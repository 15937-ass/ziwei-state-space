# Casebook Training Policy v0.1

状态：ACTIVE

## 1. 定位

了然山人案例书进入产品侧 **Case Reasoning Corpus**，用于训练/验证推理链、规则激活与时序解读。
它们不是 Zhongzhou canonical source，也不自动等于现实 ground truth。

案例书与理论书分开：
- 理论书：回答“规则是什么”；
- 案例书：回答“一个老师在具体盘上如何组合规则”；
- 真实后验事件：回答“这个判断后来是否发生”。

三类证据不得互相偷换。

## 2. 单案例结构

每个案例最终转换成 CaseEvidenceRecord：

- case_id
- source_book_id
- source_page_span
- person_group_id（用于防止同人泄漏到 train/test）
- birth_input_raw
- birth_input_normalized
- question_raw
- question_domain
- chart_snapshot
- temporal_context
- author_conclusion_spans
- author_reasoning_spans
- extracted_rule_candidates
- linked_canonical_rule_ids
- inferred_operator_sequence
- prediction_claims
- stated_historical_facts
- asker_feedback
- later_verified_outcomes
- provenance_grade
- outcome_grade
- review_status

## 3. 训练用途

允许用于：
1. rule activation / rule ranking；
2. 组合推理顺序学习；
3. palace + temporal projection 学习；
4. EvidencePackage 生成与覆盖率测试；
5. LLM verbalizer 的结构化表达训练；
6. symbolic engine 与专家案例推演的一致性比较。

不允许直接用于：
- 把作者结论当作现实真值；
- 从案例反向改写 canonical theory 而不回查原典；
- 训练后再用同一案例测“预测准确率”；
- 只因案例中出现一次就生成通用连续权重。

## 4. 数据分层

### CR-A：Author Reasoning
作者对命盘的判断与推演过程。可作为 expert demonstration。

### CR-B：Questioner Facts
提问者在提问时明确给出的既往事实。可作为已知上下文，不算预测命中。

### CR-C：Immediate Feedback
书中提问者的即时反馈。仅作为弱验证，因为可能有选择性反馈与主观性。

### CR-D：Later Outcome
若书中明确记录预测后实际发生的事件，单独标记为 outcome evidence。

只有 CR-D 才能进入“现实预测验证”候选集，并仍需做来源与时间核验。

## 5. 防泄漏拆分

数据拆分必须按 person_group_id，而不是按段落/问题随机切分。
同一个人若在本命、十年大限、多个流年被重复讨论，全部进入同一个 split。

推荐：
- train 70%
- development 15%
- held-out casebook test 15%

外部真实 benchmark（如 Fate-Bench）继续完全独立。

## 6. 与知识库的关系

案例抽取产生的新 rule candidate 必须标记 CASE_DERIVED。
只有回查 Zhongzhou source 并通过 source-span review 后，才允许升级为 canonical rule。

## 7. 产品目标

案例书的核心价值不是让模型“学会像老师一样说话”，而是把：

chart facts -> active rules -> interaction -> temporal projection -> conclusion

做成可学习、可审计、可回放的结构化训练样本。
