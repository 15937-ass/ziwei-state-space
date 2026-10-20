# Social QuickRead Skill v0.1 — Acceptance

状态：IMPLEMENTED CONTRACT / NOT A NEW THEORY LAYER

## 1. 这一步解决什么

建立一个位于 EvidencePackage / structured claims 之后、LLM verbalizer 之前的社交平台简批约束层，并加入用户可控 focus window 与同一 GPT 对话可复用的 session capsule。

它解决两个问题：

1. LLM 看见原始命盘后自由调用预训练记忆，导致流派混杂和幻觉；
2. 即使底层推理正确，输出仍容易变成长报告、论文腔或 AI 套话。

## 2. 主要机制

```text
reviewed Zhongzhou evidence
 -> QuickReadClaim
 -> fail-closed validation
 -> narrow verbalizer payload
 -> social style lint
 -> 120–220 字简批
```

同时：

```text
all validated claims + chart/profile refs
 -> QuickReadConversationContext
 -> same GPT thread follow-up
```

关键点：**LLM 不再拥有从命盘重新选规则的权限。**

## 3. 理论与话术分离

- 中州派书籍 / canonical assets：决定 claim 是否允许存在；
- 《紫微斗数话术研究》：只贡献平实叙述、直接表达、点到为止等语言研究；
- PI gold examples：决定评论区中文的长度、节奏和口吻。

话术材料不能生成命理事实。

## 4. 已冻结 topic

v0.1 支持：

- personality
- appearance
- body_type
- hobbies
- peers
- teachers_elders
- parents
- relationship_pattern
- current_relationship
- partner_preference
- study_work
- specific_year
- decade_trend

TOPIC_MAP 中的宫位只是 retrieval hints；真正输出仍由 evidence ref 决定。

## 5. 幻觉控制

代码层已实现：

- 无 evidence ref -> reject；
- 非 ZHONGZHOU school -> reject；
- current relationship / specific year / decade trend 无 TEMPORAL evidence -> reject；
- current relationship 禁止以 symbolic evidence 直接写成确定事实；
- source refs 保留在 audit 侧，但从 verbalizer payload 中剥离；
- 用户输出 lint 禁止 RULE/source/EvidencePackage 等 debug 词；
- 对过度 hedge、Markdown 报告格式进行 deterministic warning。

## 6. Focus window 与持续对话

用户可以选择 full / relationship / personality / appearance / social / family / study_work / custom。

例如 relationship scope 只消费感情模式、择偶偏好、当前感情环境，以及明确标记为 relationship domain 的年份判断。用户还可以用 custom 进一步限定 topic 和 period。

简批生成后，不丢弃其他已验证信息。系统建立 `QuickReadConversationContext`，把 all validated claims、evidence refs、chart/profile context、上一段简批和当前 scope 保留给同一 GPT 对话。后续可以从“只看感情”切到“再看事业/父母/某几年”，新 claim 仍必须重新经过 runtime。

## 7. 当前成熟度

- Specification：READY
- Implementation：READY (contract + validator)
- Canonical content：取决于各 topic 已有 reviewed/executable 中州派规则覆盖率
- Internal validation：TARGETED PASS
- Empirical calibration：NONE
- Production readiness：LIMITED

这不是“简批已经能覆盖所有十二宫”的声明。某 topic 没有可执行证据时应少说，而不是补说。

## 8. Targeted validation

执行：

```bash
PYTHONPATH="$PWD" pytest -q tests/test_product_social_quickread.py
```

结果：

```text
11 passed
```

覆盖：缺证据拒绝、流派拒绝、temporal gate、current relationship 事实门槛、relationship/custom scope 过滤、年份 domain/period 过滤、verbalizer payload 隔离、session capsule 全量 claim/evidence 保留、同一 session 切换窗口、audit trace、style linter。

## 9. Manual Pilot

当前功能定位为 PI 自用的小测试辅助，不以完整产品化为目标。新增中文简易窗口解析：例如“只看感情”“事业简批”“看父母关系”，直接映射到已有 scope；未识别时默认 full。

现阶段不做独立 UI、数据库或复杂会话服务，优先在同一 GPT 对话里用真实命盘试用。

## 10. 下一步

1. 直接用真实命盘开始 manual pilot；
2. 每次记录“命理判断是否合理 / 有没有说过头 / 像不像真人”；
3. 只有反复出现的缺口才回到 topic adapter 或知识侧补规则，不提前把这个小功能做重。
