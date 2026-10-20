# Social QuickRead Session Handoff v0.1

## 1. 目的

简批文本是给社交平台看的，盘主后续追问则需要完整上下文。

因此同一次看盘生成两个不同对象：

```text
Public QuickRead
  = 120–220 字、仅当前 focus window

Conversation Session Capsule
  = 该盘在当前知识版本下的完整可追溯上下文
```

两者不能混为一谈。

## 2. Session capsule 至少保存

- subject_key：区分不同盘主；
- knowledge_version；
- chart_context：出生资料/normalized chart 的结构化上下文或稳定引用；
- natal_profile_ref；
- temporal_profile_refs；
- all validated QuickReadClaim；
- 每条 claim 的 evidence refs；
- active_scope；
- last rendered quickread。

这里的“all claims”是**已经通过当前知识库验证的候选判断**，不是模型随手想到的所有话。

## 3. 为什么要保存未输出的 claim

假设第一次只要求：

> 只看感情，给我 150 字。

公开输出只消费 relationship scope。

但后台仍然保留本次已经算出的 personality / family / study_work 等 validated claims。盘主如果回复：

> 那你再看看我学习和工作呢？

可以直接切到 `study_work` scope，无需重新依赖聊天模型记忆，也不会因为第一次没说事业就丢掉证据。

## 4. 如果后续问题超出已有 claim

例如第一次只预计算了原局，后来盘主问：

> 2027 年感情呢？

若 session 里没有 2027 temporal evidence：

1. 读取同一个 chart/profile reference；
2. 调用 canonical/temporal runtime；
3. 生成新的 evidence-backed claim；
4. 将 claim 追加到 session；
5. 再交给 verbalizer。

禁止：

```text
GPT 看着原始盘 -> 凭训练记忆直接回答 2027
```

## 5. GPT 对话可见性

产品层应把 `continuation_payload()` 每轮作为同一会话的结构化上下文提供给 GPT。

这不是隐藏 chain-of-thought，也不保存模型推理草稿；它保存的是：

- 盘面结构数据；
- 已验证的结论；
- 证据来源；
- 时间层信息；
- 用户选择的窗口；
- 已经发送过的文字。

如产品 UI 需要，可提供“盘主上下文卡/Expert Debug”让用户显式展开查看同一份 payload。

## 6. 多盘主隔离

不同人的 `subject_key` 必须隔离。

社交软件使用场景中，用户可能连续看很多人的盘；不能让 A 的感情结论、B 的出生信息或 C 的年份判断进入另一个 session。

建议一人一 session capsule，并允许用户在 GPT 中明确：

> 回到刚才第一个女生的盘。

此时系统按 subject_key 恢复对应 capsule，而不是依赖模糊聊天记忆。

## 7. 当前边界

v0.1 先冻结数据契约和切换机制。

尚未在本 work unit 中实现：

- ChatGPT UI 的实际上下文卡；
- 持久化数据库；
- 自动 subject disambiguation；
- topic -> executable runtime 的完整 adapter。

这些属于后续产品接线，不改变本 contract。
