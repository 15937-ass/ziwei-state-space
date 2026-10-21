# Social QuickRead Pilot Case Loop v0.1

状态：EXTRA / SMALL-SCALE EVAL / HUMAN-IN-THE-LOOP

## 1. 目标

把小红书评论区的真实试用变成可复盘的小规模案例集，同时保持与 Knowledge canonical
和 Product runtime 完全隔离。

这个 Case Loop 只做四件事：

1. 记录真实用户问题的类型；
2. 记录本次简批实际用了哪些 claim / origin；
3. 记录盘主后续反馈，区分命中、部分命中、反例、新事实；
4. 由 PI 挑选少量“事实干净 + 语言好”的回复，作为 **style-only few-shot** 范例。

它不是自动训练 canonical rules 的入口。

## 2. 最短工作流

```text
PI 选一条真实帖子
 -> 新建独立 subject_key
 -> QuickRead 双输出
 -> PI 人工发评论
 -> 盘主追问 / 验证
 -> FeedbackRecord
 -> PIReview
 -> CaseRecord
 -> 可选：PreferredExample
 -> 每 20~50 例做一次 aggregate eval
```

### 什么时候记录 CaseRecord

优先记录满足以下任一条件的案例：

- 盘主明确回复“对 / 不对 / 实际情况是……”；
- 有至少一个可验证的前后事；
- PI 认为这条回复的语言特别自然，值得保留；
- 暴露出一个高频 coverage gap；
- 出现模型幻觉、串盘、重复或错误读宫等反例。

没有真实反馈的普通路过评论可以不入库，避免样本膨胀。

## 3. Feedback 标签

- `HIT`：盘主明确确认某个判断；
- `PARTIAL`：方向对，但落地细节只对一部分；
- `CONTRADICT`：盘主明确否定；
- `NEW_FACT`：盘主给出此前未知的现实事实；
- `STYLE_ONLY`：只评价“说话像真人 / 太啰嗦”等表达；
- `UNCLEAR`：反馈无法对应到具体 claim。

反馈永远是：

```text
OBSERVATION / EVAL DATA
```

不能自动升级为：

```text
CANONICAL RULE
```

## 4. PIReview

每个值得保留的案例只打很轻的标签：

- `factual_score`: 1~5
- `style_score`: 1~5
- `redundancy_count`
- `hallucination_count`
- `useful_followup`
- `preferred_example`

推荐进入 style few-shot bank 的最低门槛：

```text
factual_score >= 4
style_score >= 4
hallucination_count == 0
PI explicit approval == true
```

## 5. PreferredExample 只学语言

PreferredExample 的作用只有：

- 句子长度；
- 信息密度；
- 开头方式；
- 口语节奏；
- 如何直接回答追问；
- 如何避免 AI 腔、同义反复、过度防御。

它 **不能** 提供当前命盘的事实。

运行时仍然必须：

```text
当前盘 validated claims
        ↓
决定能说什么

PreferredExample
        ↓
只决定怎么说
```

禁止从 few-shot 样例复制“对象年长”“26年换工作”“财运留不住”等事实到另一个盘。

## 6. 去标识化

Git 中 CaseRecord 不保存：

- 小红书用户名；
- 主页 / 帖子 URL；
- 头像；
- 原始命盘截图；
- 精确出生时间；
- 与评估无关的私聊内容。

允许保存：

- 随机/顺序 `case_id`；
- `subject_key`；
- 问题的去标识化摘要；
- 最终公开回复文本；
- claim ids / provenance 统计；
- coverage gaps；
- 去标识化后的盘主反馈；
- PIReview。

若某条反馈文本本身含姓名、学校、单位、地址等可识别信息，写入 Git 前先改成语义等价的匿名描述。

## 7. 小规模范例阶段

当前建议阶段：

### 0~20 例
主要找工作流 bug：

- 串盘；
- 错读宫；
- unsupported semantics；
- PI 审计漏出；
- 语言太长 / 太 AI。

### 20~50 例
开始看：

- 用户问题分布；
- HIT / PARTIAL / CONTRADICT 比例；
- 哪些 scope 最依赖 SOURCE_BACKED_FALLBACK；
- 哪些 coverage gap 最常出现；
- 哪类话术最容易得到继续追问。

### 50~100 例
才考虑：

- 基于 scope / prompt pattern 检索 3~5 条 PreferredExample；
- 建立固定 QuickRead eval set；
- 比较不同 verbalizer prompt。

在此之前不做模型权重微调。

## 8. 与主项目隔离

Case Loop 不允许：

- 写入 `knowledge/**`；
- 自动改 canonical rule；
- 用单个 HIT 证明一个新理论；
- 用单个 CONTRADICT 删除一条原书规则；
- 修改 Product inference semantics；
- 把真实反馈偷偷拼进下一张独立命盘。

若多案例反复出现理论缺口，只生成：

```text
knowledge research candidate
```

之后必须重新查原书、实例和治理流程，才能进入 Knowledge 工作流。
