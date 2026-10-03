# Product Evaluation Protocol v0.1

## 1. 目的

把“用户觉得准”拆成可测指标，防止事后解释、测试集泄漏与输出长度造成的主观准确幻觉。

## 2. 四个相互独立的评估层

### E1 Chart Correctness / Agreement
衡量确定性排盘实现。

指标：
- exact chart-field agreement；
- disagreement count per 1,000 charts；
- unresolved disagreement rate；
- crash/invalid-input rate。

注意：多引擎一致只代表 agreement，不自动代表 truth。

### E2 Internal Formalization Fidelity
衡量是否忠实执行冻结知识。

指标：
- source trace completeness；
- active-rule precision/recall on manually reviewed cases；
- deterministic reproducibility；
- conflict preservation；
- rule-to-output trace completeness。

### E3 External Outcome Benchmark
衡量对未见真实事件的区分能力。

规则：
- benchmark answer 在最终预测落盘前不可读；
- 任何基于测试答案的 schema/rule/prompt 修改必须进入下一版本，不能回算当前分数；
- development/test 分离；
- 公开说明 sample size 与 answer provenance。

### E4 Calibration / Selective Prediction
对每个预测同时记录 confidence band。

至少报告：
- overall accuracy；
- accuracy by confidence；
- coverage；
- selective accuracy at each coverage；
- Brier/log loss（只有得到合法概率模型后）；
- abstention rate。

## 3. Baselines

每个外部 benchmark 至少比较：

1. random/chance（若任务允许）；
2. generic LLM，无领域资料；
3. LLM + source RAG；
4. flat rule retrieval；
5. current symbolic inference；
6. symbolic inference + LLM verbalizer。

如存在公开 human baseline，则独立展示，不将最高人类分数错误称为平均水平。

## 4. Ablation

产品达到 inference MVP 后依次做：
- remove star-system interaction delta；
- remove system mode；
- replace subject-dependent transformations with uniform +/- gains；
- remove typed history；
- remove cross-palace graph；
- remove provenance/conflict constraints；
- LLM-only replacement。

目的不是追求论文花样，而是找到真正提高产品结果的部件。

## 5. Category Metrics

不得只报告总准确率。至少分：
- career；
- resource/finance；
- relationship；
- family；
- health；
- mobility；
- timing。

只在样本量足够时给稳定结论。

## 6. Leakage Control

Fate-Bench 等外部测试集接入后：
- 单独目录；
- answer file 与 development pipeline 解耦；
- prompt/规则开发默认不可读取 answer；
- benchmark run 记录 commit SHA、knowledge version、model version、prompt hash；
- 如人工查看答案，必须标记该版本已 contaminated，不再作为 blind score。

## 7. 产品置信度不是“玄学概率”

在真实概率校准完成前，confidence 只表示：
- evidence coverage；
- source/review quality；
- conflict load；
- rule specificity；
- unresolved gates。

不得把 HIGH 直接解释成“80%会发生”。

## 8. 发布声明

对外任何“最高准确率”声明必须同时给出：
- benchmark 名；
-版本；
- 样本量；
- 评价任务；
- baseline；
- 是否盲测；
- confidence interval/不确定性（可计算时）；
- 代码或复现实验入口（条件允许时）。
