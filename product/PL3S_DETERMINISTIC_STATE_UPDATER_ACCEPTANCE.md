# PL3-S Deterministic State Updater v0.1

状态：**IMPLEMENTED — EXPLICIT-DIRECTIVE UPDATE ONLY**

## 1. 目的

把经过验证的 longitudinal observation 确定性更新为 `AcquiredStateProfile`。

但 v0.1 不允许：

~~~text
event label -> hidden inferred state
LLM prose -> automatic state mutation
~~~

现实事件本身不会自动改写状态；只有显式、结构化、`user_confirmed=true` 的 state directive 才能更新 assertion。

## 2. 两类 directive

~~~text
UPSERT_ASSERTION
MARK_MISSING
~~~

`UPSERT_ASSERTION` 写入明确现实状态；`MARK_MISSING` 明确表示当前状态未知/未观察/过期等。

## 3. Observation 自动带入的内容

不需要额外语义解释的部分可以确定性复制：

- observation.actions -> AcquiredAction；
- exposures -> EXPOSED context；
- external_factors -> EXTERNAL context；
- counterparty_factors -> COUNTERPARTY context。

这只是 provenance-preserving copy，不把 event_type 映射成状态。

## 4. 状态变化规则

同一 domain/key：

- 没有旧值：直接加入；
- 新旧值相同：合并 observation provenance；
- 值不同且 `supersedes_existing=true`：显式替换；
- 值不同且没有 supersede：保留两条事实并生成 UNRESOLVED conflict。

系统不猜哪个报告更可信。

## 5. Missingness

`MARK_MISSING` 会移除该 domain/key 的当前 assertion，并写入显式 missingness。

另外，只有 assertion 自己给出了 `valid_through` 且已经过期时，系统才自动转为 OUTDATED。

没有通用衰减时间，没有“30 天没更新就失效”之类拍脑袋规则。

## 6. Action / Context persistence

既有 action/context 若本次 observation 没提及，不自动当成结束。

这遵守：

~~~text
absence of report != negative evidence
~~~

同 ID/同 context label 再次观察时只合并 provenance。

## 7. 顺序与回放

v0.1 只允许按时间向前更新。

如果收到 backdated observation，必须从更早的 state snapshot 重新 replay；本层不偷偷重排历史。

## 8. 永久边界

- 不读取 Natal Prior 来决定现实状态；
- 不读取 Temporal Environment 来决定现实状态；
- 不根据命盘预测结果补写 state；
- 不产生 probability；
- 不把 observation outcome 自动解释为特定 state；
- LLM 未来只能生成 directive candidate，必须用户确认后进入 updater。

## 9. 下一步

**PRODUCT_PL3S_MISSINGNESS_CONTRADICTION_MODEL_V0_1**

下一步把 missingness、conflict、observation confidence 的审计状态再向前推进，为后续 Bayesian belief update 准备明确的 observation-quality interface。
