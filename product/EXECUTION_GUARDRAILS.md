# Product Execution Guardrails v0.1

状态：ACTIVE  
适用范围：产品侧批量排盘、双引擎 diff、案例抽取、benchmark、规则匹配与后续推理批处理。

## 1. 总原则

任何产品任务都必须满足：

1. **有界输入**：不得一次处理无上限记录；
2. **有界错误**：错误达到阈值立即中止；
3. **有界时间**：每一步必须有 timeout；
4. **有界输出**：日志与 diff 详情不得无限增长；
5. **可恢复 checkpoint**：每个批次独立可重跑；
6. **禁止无限自动重试**：同一失败最多自动重试 1 次，第二次仍失败则停止并记录 BLOCKED。

## 2. 默认硬限制

### 单批记录数
- 普通结构回归：最多 100 natal inputs / batch；
- 单个 temporal manifest：最多 8 targets；
- 因此单 job 最多 800 horoscope snapshots；
- 案例结构化抽取：最多 20 cases / batch；
- source review：沿用知识库规则，最多 100 items / recoverable checkpoint。

### 错误数
- engine execution errors：最多 10；
- malformed input errors：最多 5；
- unresolved mismatch：任意 1 条都不允许自动关闭 gate；
- comparator 捕获的 total differences：达到 500 后停止继续收集详情并立即失败；
- 单 case 最多保存 100 条 diff detail，其余只计数。

### 时间
- GitHub job：15 分钟；
- install step：5 分钟；
- 单个 exporter：5 分钟；
- comparator：3 分钟；
- independent engine export：6 分钟；
- independent comparator：3 分钟。

超时后不得原地循环等待；保留 artifact 和当前 checkpoint 后退出。

## 3. Retry policy

同一 commit / 同一输入：

- 第一次失败：允许自动或人工重跑 1 次；
- 第二次同类失败：标记 `REPEATED_FAILURE`；
- 不再连续重试；
- 先检查日志、输入规模、依赖版本、网络、算法异常；
- 修复后必须产生新 commit 才重新执行。

## 4. Diff fail-fast

若大量字段同时不一致，通常代表：
- adapter schema 漂移；
- 配置未对齐；
- engine API 变化；
- 上游版本变化。

因此 comparator 达到 hard cap 后必须停止，不允许为了“把所有报错打印完”继续占用 runner。

## 5. 日志限制

- 正常 stdout 控制在 200 行以内；
- 详细 diff 写入 JSON artifact；
- 控制台只显示 summary + 前 20 条差异路径；
- 禁止在 CI 中 cat 整个超大 JSONL。

## 6. P1 B02 专用规则

B02 分三块独立执行：

- B02-A：历法边界；
- B02-B：早子/晚子与日界；
- B02-C：大限/小限/流年/流月/流日动态边界。

每个子块必须：
- 独立 target manifest；
- 独立 CI；
- 独立 acceptance note；
- `UNRESOLVED=0` 后才进入下一块。

不得把 A/B/C 合成一个超大单 job。

## 7. Gate close

任何“COMPLETE / CLOSED”必须同时满足：
- 当前批次无 timeout；
- 无 repeated failure 未解释；
- unresolved mismatch = 0；
- artifact 可复现；
- 状态文件已同步。
