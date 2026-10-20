# Social QuickRead Skill v0.1

状态：PRODUCT VERBALIZER CONTRACT

## 1. 目标

把已经由中州派 canonical/runtime 或 temporal runtime 计算出的证据，压缩成适合社交平台评论区的 120–220 字简批。

目标风格不是命书、报告或教学，而是：

> 一个熟悉紫微斗数的人扫完盘后，用普通中文直接说判断。

本 Skill 只负责 **claim 选择后的约束表达**，不拥有命理真值。

## 2. 硬边界

1. 不从模型记忆创造紫微规则。
2. 不把钦天、河洛或网络口诀静默混入中州派。
3. 每个进入 verbalizer 的命理 claim 必须绑定至少一个已审核 evidence ref。
4. verbalizer 不接触原始命盘作为自由推理入口；只接触经过验证的 claim envelope。
5. 《紫微斗数话术研究》只用于研究说话方式、互动节奏和表达技巧，不能作为命理事实来源。
6. PI 提供的 gold examples 只定义语言风格，不能反向生成理论规则。
7. 无证据的 topic 允许不写；禁止为了凑齐“性格、父母、恋爱”等栏目而补话。
8. 原局为主；大限/流年只在有 TEMPORAL evidence 时进入输出。
9. 当前恋爱状态、具体事件发生与否不能仅凭原局写成已发生事实。

## 3. 执行顺序

```text
Normalized chart / question
  -> Canonical / Temporal runtime
  -> reviewed evidence refs
  -> QuickReadClaim envelope
  -> topic / temporal gate
  -> confidence + conflict filtering
  -> semantic-group 去重
  -> verbalizer_payload()
  -> LLM 生成内部 draft + sentence->claim mapping
  -> blocking pre-send audit
  -> deterministic style lint
  -> final 120–220 字评论
```

## 4. Claim 生成原则

候选 claim 必须先写成不带修辞的语义句，例如：

```text
主体性强，做事果决。
对艺术/审美存在明确兴趣倾向。
与同辈能正常相处，但深层亲近关系数量有限。
2025 年学习/工作环境存在明显变动倾向。
```

然后绑定 rule/source evidence。只有通过 `QuickReadClaim.validate()` 才能进入 verbalizer。

严禁直接把：

```text
命宫廉贞七杀 + 夫妻宫武曲...
```

交给语言模型并让它“自己看着发挥”。

## 5. 输出选择

默认优先级：

1. 最鲜明的人格/行为特征；
2. 1 个能快速验证的外形、爱好或人际特征；
3. 1 个感情/择偶特征；
4. 2–4 个最明显的近年 temporal 特征（若有）；
5. 必要时一句总体趋势。

不要求每次覆盖所有 topic。

## 6. 真人化规则

- 直接说结论，不解释宫位、星曜和规则编号。
- 强证据用直接句；只有落地不唯一时使用“感觉、可能、如果……的话”。
- 不连续三句都加“可能/应该/大概率”。
- 不使用“不是……而是……”这类先否定再转折的对照句式，直接说正面判断。
- 用日常场景表达抽象特征，例如“有主见”可以落到“不喜欢别人替你做决定”。
- 一次最多挑 3–6 个高信息量判断，不做百科全书式罗列。
- 不加“仅供娱乐”“无法确定”等模板化免责声明，除非产品层另有明确要求。

## 7. Fail-closed

出现以下情况直接删除该 claim，而不是补全：

- evidence ref 为空；
- school 不是 ZHONGZHOU；
- temporal topic 没有 TEMPORAL evidence；
- source/review status 不完整；
- claim 与现有 evidence 之间只能靠模型常识或网络记忆连接；
- 两条高优先级证据冲突且 runtime 未给出可用 resolution。

## 8. 双输出：用户版与 PI 审计版

用户最终评论不得暴露技术字段；`verbalizer_payload()` 仍故意不发送 source refs，防止 LLM 顺着原文继续扩写新的命理判断。

但 **Manual Pilot 面向 PI 的每一次运行都必须同时返回两段结果**，包括首次简批和所有 Follow-up：

1. **用户可读版**：可直接复制到社交平台的自然语言；
2. **PI 审计版**：说明每个输出点的语义来源、证据状态与模型参与方式。

PI 审计至少保留：

```text
claim_id
-> semantic_origin
-> runtime_run_id（若宣称 RUNTIME_*）
-> rule_id / source_id / source_location
-> language_origin
-> llm_added_semantics
-> coverage_gap / observation（如有）
```

允许的 `semantic_origin`：

- `RUNTIME_CANONICAL`：本次或可追溯 session 中实际执行 canonical runtime 得到；
- `RUNTIME_TEMPORAL`：本次或可追溯 session 中实际执行 temporal runtime 得到；
- `SOURCE_BACKED_FALLBACK`：当前 runtime 未覆盖，但由批准的中州派 source 直接检索并人工组成 claim。

**不得仅因 evidence namespace 是 CANONICAL/TEMPORAL，就默认声称 runtime 已经实际执行。** 若没有可追溯的 `runtime_run_id`，不得标成 `RUNTIME_CANONICAL` 或 `RUNTIME_TEMPORAL`。

`LLM_VERBALIZATION` 只表示把已有 claim 改写成自然中文，不是独立事实来源。若出现新的事实/解释语义，必须进入 `llm_added_semantics`，并阻断用户版发送。

因此，在 PI 当前试用阶段，**只给用户版而省略 PI 审计版属于 contract violation**。

## 9. 用户可限定的简批窗口

QuickRead 不强制“整盘都说”。用户可以限定一个 focus window，只把相关 claim 送进 verbalizer。

预设窗口：

```text
full
relationship
personality
appearance
social
family
study_work
custom
```

例如“只要感情简批”：

```text
scope = relationship
```

允许进入的内容包括：

- 长期感情模式；
- 喜欢/容易被什么类型吸引；
- 当前感情环境（必须有 TEMPORAL evidence）；
- 标记为 relationship domain 的具体年份判断。

不会混入无关的事业、外貌、父母内容。

`custom` 还可以进一步限制 topic 和年份，例如：

```text
domain = relationship
topic = specific_year
period = 2025
```

这时只写 2025 年感情相关简批。

## 10. 简批后继续在同一 GPT 对话深入批盘

对外发布的 120–220 字只是一个窄 render，不等于丢弃其余推理结果。

每次简批后生成一个 `QuickReadConversationContext`，在同一 GPT 对话中保留：

- subject key；
- knowledge version；
- normalized chart / birth context 的结构化上下文或引用；
- natal profile reference；
- temporal profile references；
- 本次已使用的 claims；
- 本次没写出来、但已经验证过的其他 claims；
- 每个 claim 的 rule/source trace；
- 上一段已经发出的简批；
- 当前 focus window。

因此如果最开始只发了“感情简批”，之后盘主继续追问：

> 那事业呢？
> 
> 为什么说我喜欢这种类型？
> 
> 具体看看 23–25 年。
> 
> 我和父母怎么样？

系统可以在**同一个盘主 session**中切换 scope，优先复用已经验证过的 claims；如果问题需要新的判断，则重新走 canonical/temporal runtime 后再加入 session，而不是让 GPT 根据原始命盘自由发挥。

这里有两个不同 payload：

```text
verbalizer_payload
  -> 很窄，只包含这次允许说的 claims
  -> 用于生成 120–220 字评论

continuation_payload
  -> 很全，留在 GPT 对话上下文
  -> 包含所有已验证 claims + evidence refs + chart/profile context
  -> 用于后续追问和换窗口
```

`continuation_payload` 可以被 UI 做成“盘主上下文卡”供用户查看；即使 UI 暂时不展示，产品也不能只依赖聊天模型自己记忆上一轮内容，必须把 session capsule 持续传回后续对话。


## 11. 当前试用策略

当前由 PI 自己在 GPT 中试用，因此先启用 **Manual Pilot**，不继续堆产品基础设施。

最简交互：

```text
上传/给出一个盘
+ 一句话限定窗口
=> 直接出短简批
=> 同一对话继续追问
```

中文窗口别名已支持最常用说法：全盘/简批/整体、感情/恋爱/婚恋、性格、长相/外貌、人际/朋友、父母/家庭、事业/工作/学业。

复杂的持久化、UI 上下文卡、多用户 session 等保留为未来能力；当前测试不以此为前置条件。


## 12. 每次发送前必须审计

Manual Pilot 也不能“先发再审计”。最终文字发送给 PI 之前必须经过 blocking audit：

1. 每句话至少映射到一个已验证 claim；
2. 每个 claim 必须有 evidence；
3. 同一个 `semantic_group + target_period` 默认只允许表达一次；
4. 同义改写不能算新增信息；
5. 如果后一条只是把前一条换一种说法，直接删除后一条，不以“丰富表达”为理由保留；
6. 任何无法映射回 claim 的修饰、外貌印象、心理补充、生活化发挥，均视为 unsupported hallucination；
7. 审计不通过则不发送，先删改再重新审计。

典型反例：

```text
内心很有主见。
更在意自己有没有位置、能不能做主。
```

若两句都来自同一“主体性 / 控制感”证据轴，则第二句没有新增信息，属于 semantic repetition。即使每句话单独看都“说得通”，也不能同时进入简批。

因此 claim 除 topic 外还必须标记 `semantic_group`；QuickReadPackage 在进入 verbalizer 前先做一次去重，render draft 再做一次句级审计。
