# Social QuickRead Manual Pilot v0.1

状态：SMALL TEST / HUMAN-IN-THE-LOOP

## 1. 为什么先做这个

这个功能当前只是给 PI 自己试用的辅助算命工具，不追求完整产品化。

因此 v0.1 采用最短路径：

```text
PI 提供命盘/出生资料
 -> 指定“全盘 / 感情 / 性格 / 事业 / 父母 / 人际 / 长相”
 -> 读取现有中州派知识与已验证规则
 -> 形成少量 evidence-backed claims
 -> 生成约 120–220 字真人口吻简批
 -> 继续在同一 GPT 对话追问
```

不先做数据库、前端、复杂 session manager 或完整十二宫自动化。

## 2. PI 使用方式

在同一 GPT 对话里直接发送命盘截图或出生资料，然后用很短的指令即可：

- “全盘简批，150字”
- “只看感情”
- “只看性格和长相”
- “事业简批”
- “看父母关系”
- “感情重点看22-25年”

如果没有指定窗口，默认 full。

## 3. 输出标准

Manual Pilot 对 PI **固定双输出**，不得只返回一段公开文案。

### A. 用户可读版

- 约 120–220 字；
- 1 段；
- 不列技术标题；
- 不解释 rule/source；
- 先说最明显的 3–6 个判断；
- 强判断直接说；
- 落地不唯一时才用“感觉/可能/看起来”；
- 具体年份只在有 temporal evidence 时写。

如果窗口很窄而证据不足，可以少于 120 字，不为了凑字数跨领域补内容。

### B. PI 审计版

紧跟用户版输出，至少逐点列出：

- 输出判断；
- `semantic_origin`；
- 是实际 runtime 推演、source-backed fallback，还是仅 LLM verbalization；
- rule/source trace；
- `llm_added_semantics` 是否为 0；
- coverage gap；
- 已知盘主 observation（如有）。

首次简批、指定窗口简批、盘主追问、年份追问都遵守同一双输出要求。

## 4. 同一盘继续批

第一次例如只发“感情简批”，之后可以继续：

- “再看她事业”
- “详细说说喜欢的类型”
- “为什么说24年感情不顺”
- “再看父母”
- “把22-25年展开一点”

试用阶段优先依靠同一 GPT thread 的盘主上下文 + QuickReadConversationContext，不额外建设持久化服务。

如果切换到另一个人，建议 PI 给一个简单标签，例如：

- A盘
- B盘
- 女1
- 男2

避免连续测试时串盘。

## 5. 幻觉控制的最低要求

即使是小测试，也保留三条硬规则：

1. 不用模型自己记得的紫微知识补规则；
2. 不把钦天/河洛混进中州派；
3. 具体 claim 必须能回到现有 source/reviewed rule；找不到就少说。

试用阶段每次都必须把 **PI 审计版** 展示给 PI。可以先给简要 trace，但不得只在后台保存；PI 必须能看到每个判断是 runtime、source fallback 还是模型措辞。

## 6. 当前不做

- 不做独立网页；
- 不做账号/数据库；
- 不做长期盘主档案；
- 不做自动私信/社交平台发布；
- 不做复杂自然语言意图解析；
- 不为了覆盖率补全尚未成熟的知识 topic。

先用真实命盘测试“好不好用、准不准、像不像真人”，再决定是否继续产品化。


## 7. 新命盘默认独立

Manual Pilot 中每一张新上传的命盘默认建立新的 `subject_key`，不得继承上一张盘的出生资料、claims、年份判断、反馈或风格性事实。

只有 PI 明确说明“还是上一张盘 / 同一个人 / 继续这个盘”时，才允许复用上一 session。

因此默认行为是：

```text
new chart image => new independent subject session
```

而不是：

```text
new chart image => continue previous chart context
```

所有命理判断仍以 Git 中当前 Social QuickRead contract、canonical/runtime 与中州派 source priority 为准。


## 8. 盘主追问：进入 Follow-up Mode

公开评论用 QuickRead；盘主一旦回复追问，立即切换到 `social_quickread_followup_v0.1`。

Follow-up 不是再生成一遍“整体简批”，而是：

```text
同一 subject capsule
 -> 识别盘主当前问题
 -> 保持原窗口，或显式切换到新窗口
 -> 只取与该问题有关的 validated claims
 -> 必要时补跑新的 canonical / temporal evidence
 -> 直接回答问题
```

### 典型交互

第一次评论：

> 整体看人挺果断……26年感情和合作容易折腾。

盘主追问：

> 为什么说我感情磨合多？

此时保持 relationship scope，不重复“你性格果断、事业上心”等总评，直接回答感情依据和现实表现。

盘主再问：

> 那事业呢？

此时在同一个 subject session 中切换到 study_work scope，不重新排盘，不带其他盘主信息。

### Follow-up 输出风格

- 默认 80–280 字，问题简单可以更短；
- 第一口就回答问题，不再用“整体看”开头；
- 不复述第一次评论，除非必须引用其中一句解释；
- 每次只展开当前问题，允许比公开简批多一层原因或现实表现；
- 用户问“为什么”时可以适量解释星系/宫位；没问原因就继续说人话；
- 用户提供现实反馈时记录为 observation：可用于确认、否定或选择歧义分支，但不能反向制造盘面规则；
- 若当前 capsule 没有足够 claim，先补检索/推演，再回答；不要拿第一次那几句话硬扩写。


## 9. 小规模案例积累

当前 Manual Pilot 同时承担小规模真实样本积累，但案例数据只能进入
`apps/social_quickread_pilot` 的 EXTRA sidecar，不能直接回写 Knowledge/Product。

当盘主出现明确现实反馈时：

```text
当前 subject session
 -> Observation / FeedbackRecord
 -> PIReview
 -> de-identified CaseRecord
```

反馈标签固定为：

- `HIT`
- `PARTIAL`
- `CONTRADICT`
- `NEW_FACT`
- `STYLE_ONLY`
- `UNCLEAR`

### 每次 Follow-up 的 PI 侧附加状态

若盘主已给出验证信息，在 PI 审计末尾补：

```text
CASE_CAPTURE: candidate | skip | preferred_candidate
```

- `candidate`：有明确可验证反馈，值得入案例集；
- `preferred_candidate`：同时语言质量高，可待 PI 批准为 style-only few-shot；
- `skip`：没有新增验证信息、只是礼貌回复或信息太弱。

### PreferredExample

只有满足以下全部条件才进入语言范例集：

```text
PI explicit approval
factual_score >= 4
style_score >= 4
hallucination_count == 0
```

范例仅允许影响“怎么说”，严禁提供“说什么”。当前命盘的事实仍必须来自本盘
validated claims / approved source fallback。

Git 中禁止保存小红书用户名、帖子 URL、头像、原始盘图和精确出生时间。


## 10. Temporal-4H Mini Mode

当 PI 问“近两年 / 某一年 / 哪年出去 / 哪年感情动 / 哪年工作变”时，
Manual Pilot 可以额外启用 `Temporal-4H Mini Kernel v0.1`。

输入优先级：

1. 已验证 P1 temporal snapshot；
2. 命盘截图中人工读取的当前大限宫干 + 目标流年天干；
3. 信息不足则不运行，不让 LLM 猜宫干。

流程：

```text
原局基础判断
 -> 当前大限宫星
 -> 大限四化
 -> 流年落宫
 -> 流年四化
 -> 同星/同宫跨层交互
 -> 必要时检查生年四化同星再激活
 -> 回原书/现有 reviewed rule 做语义解释
 -> QuickRead
```

### Provenance

- P1 runtime 直接提供四化且有 run id：
  `RUNTIME_TEMPORAL`
- PI/GPT 从截图读取天干，再由 sidecar 固定表计算：
  `DETERMINISTIC_TEMPORAL_SIDECAR`
- 对“这意味着事业推进 / 感情消耗 / 财务压力”等语义解释：
  必须另有 reviewed/source-backed evidence；否则不得输出。

`DETERMINISTIC_TEMPORAL_SIDECAR` 只证明：
“某层某星化某曜并落某宫”这个结构事实，
不自动证明事件层结论。

### 当前限制

v0.1 的 `NATAL_STAR_REACTIVATED` 只检测**同一颗生年化曜星**
在大限/流年再次发生四化；尚不把三方四正冲会自动称为“冲起”。
关系图版本留给后续增量。
