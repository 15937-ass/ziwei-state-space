# Social QuickRead Sidecar v0.1

状态：EXTRA / READ-ONLY CONSUMER / MANUAL PILOT

## 目的

这是主项目之外的轻量小应用。它不修改 Knowledge canonical、Product runtime
或整体架构，只消费上游已经验证的 `QuickReadClaim`，把它们压缩成社交平台
简批，并同时输出一份给 PI 的溯源审计。

```text
existing chart/runtime/evidence
        ↓
validated QuickReadClaim[]
        ↓
apps/social_quickread_pilot
        ↓
┌──────────────────┬──────────────────────────┐
│ 用户可读版        │ PI 审计版                 │
│ 120-220字自然语言 │ 每句 claim/evidence/origin │
└──────────────────┴──────────────────────────┘
```

## 双输出原则

**这是强制协议，不是可选 debug。** Manual Pilot 的每一次首次简批、窗口简批、盘主追问、年份追问，都必须在给 PI 的回复中同时展示 A+B。只输出 A 属于 contract violation。

### A. 用户可读版

只出现自然语言结论，不展示 rule/source 技术信息。

### B. PI 审计版

每句话显示：

- `claim_ids`
- `semantic_origins`
- `language_origin = LLM_VERBALIZATION`
- evidence namespace / rule / source / location
- 是否存在 `llm_added_semantics`
- coverage gaps
- 盘主现实反馈 observations

### 不是简单的“大模型 vs 真实推演”二选一

一条正常句子通常同时有两层来源：

```text
事实含义：RUNTIME_CANONICAL / RUNTIME_TEMPORAL
表达措辞：LLM_VERBALIZATION
```

例如：

> 25年自己状态偏累，情绪压力比表面大。

PI 版可以显示：

```yaml
semantic_origin: RUNTIME_TEMPORAL
claim_id: y2025_pressure
language_origin: LLM_VERBALIZATION
evidence:
  - rule_id: ...
    source: ...
llm_added_semantics: []
```

这表示“25年压力上升”来自真实规则推演，而“自己状态偏累”是模型对同一语义的
口语化表达，没有新增事实。

## Origin 分类

- `RUNTIME_CANONICAL`：现有 canonical/runtime **实际执行**所得，必须附可追溯 `runtime_run_id`；
- `RUNTIME_TEMPORAL`：现有 temporal runtime **实际执行**所得，必须附可追溯 `runtime_run_id`;
- `SOURCE_BACKED_FALLBACK`：中州派原书有明确依据，但当前尚未进入 executable runtime；
- `LLM_VERBALIZATION`：只负责说人话，不是独立事实来源；
- `llm_added_semantics != []`：模型新增了 claim 没有支持的事实/解释，用户版直接阻断。

`SOURCE_BACKED_FALLBACK` 特意单列。它不是“大模型瞎补”，但也不能伪装成 Git runtime
已经自动算出来的结果。

每个实际进入用户版的 claim 都必须显式提供 `ClaimTrace`。禁止根据 evidence namespace 自动猜测 origin；没有 `runtime_run_id` 就不能标成 `RUNTIME_*`。

## 盘主反馈

盘主回复：

> 我确实是事业编，走专业技术岗。

进入 `ObservationRecord`，PI 版标记：

```text
OBSERVATION_ONLY_NOT_CANONICAL_TRUTH
```

它可以辅助后续个体化对话，但不能反向改写原局规则。

## Coverage Gap

如果用户问“未来老婆怎么样”，而当前 executable runtime 没有足够 relationship
claim，则记录：

```yaml
request: 未来老婆怎么样
topic: relationship
reason: executable runtime coverage insufficient
```

可以在 Manual Pilot 中继续人工查中州派原书形成
`SOURCE_BACKED_FALLBACK`，但必须在 PI 版明确标出。

## 最小使用

```python
request = PilotRequest(
    subject_key="QR-017",
    request_text="事业简批",
    knowledge_version="...",
    claims=validated_claims,
)

prepared = prepare_pilot(request)

# GPT 根据 prepared.verbalizer_payload 生成自然语言，并返回逐句 claim mapping。
result = finalize_pilot(
    prepared,
    sentences=rendered_sentence_traces,
    claim_traces=claim_traces,
)
```

最终 `result["public"]` 给社交平台使用，`result["pi"]` 给 PI 查看。

## 边界

这个 sidecar 不允许：

- 修改 `knowledge/**`；
- 修改 canonical rule；
- 修改 Product inference semantics；
- 把盘主反馈写回 canonical truth；
- 把 LLM 新增语义静默混入用户版；
- 为了凑 120 字补无证据内容。

它的生命周期可以独立于主产品：验证失败可直接删除，不影响主项目。


## Pilot Case Loop

真实小红书试用现在允许进入一个独立的去标识化案例闭环：

```text
QuickRead 双输出
 -> PI 人工发布
 -> 盘主真实反馈
 -> FeedbackRecord
 -> PIReview
 -> CaseRecord
 -> 可选 PreferredExample（style-only）
 -> summarize_cases()
```

实现位于：

- `apps/social_quickread_pilot/case_loop.py`
- `apps/social_quickread_pilot/CASE_LOOP.md`
- `apps/social_quickread_pilot/examples/preferred_style_seeds_v0.1.json`

### 核心约束

- CaseRecord 只存去标识化内容；
- 盘主反馈只做 observation / eval，不自动改 Knowledge；
- PreferredExample 只教语言，不提供另一个命盘的事实；
- 只有 PI 明确批准、factual/style 均 >= 4 且 hallucination=0 的案例，才可晋升为 PreferredExample；
- 被 `LLM_ADDED_UNSUPPORTED_SEMANTICS` 阻断的输出不能进入案例库；
- 当前阶段先积累 20~50 个小样本，再看 question routing、coverage gap 和 verbalizer 的实际效果。

### PI 使用时的默认记录习惯

盘主出现明确反馈后，PI 审计末尾额外给出一行：

```text
CASE_CAPTURE: candidate / skip / preferred_candidate
```

并说明命中、反例、新事实或语言反馈。这样不要求每个路过盘都入库，只保留有训练价值的案例。
