# Canonical Zhongzhou Chart Contract v1.0

Status: **CANONICAL PRODUCTION CONTRACT — FROZEN**

PI decision: 2026-10-31  
Tracking implementation: Product Issue [#977](https://github.com/15937-ass/ziwei-state-space/issues/977)  
Machine-readable authority: `product/CANONICAL_CHART_CONTRACT_v1.0.json`

## 1. 唯一生产排盘方法

本项目所有正式命盘事实必须使用**中州派排盘口径**，并由固定版本的 **iztro JS 2.6.1** 生成。

这是一项产品基础架构硬约束，不是单次任务的默认建议。适用于：

- NATAL 本命盘；
- DECADE 大限；
- AGE / SMALL_LIMIT 小限；
- YEAR 流年；
- MONTH 流月；
- DAY 流日；
- HOUR 流时。

上述所有时间层必须由同一固定排盘契约生成。大限、流年等时间事实由 iztro 的 horoscope 接口计算，不得由 LLM 根据出生日期、年龄或年份自行推算。

## 2. 冻结配置

| 字段 | 唯一允许值 |
|---|---|
| School / algorithm | `zhongzhou` |
| Production engine | `iztro-js` |
| Engine version | `2.6.1` |
| iztro source revision | `2c7ef9be669df7b19d1799f4dce335fed3794f78` |
| Adapter version | `0.2` |
| Astro type | `heaven` |
| `fix_leap` | `true` |
| `day_divide` | `forward` |
| `year_divide` | `normal` |
| `horoscope_divide` | `normal` |
| Language | `zh-CN` |

出生日期输入可以是公历或农历，但必须明确记录输入历法和对应入口；这不授权改变上表中的中州派算法及固定配置。机器契约列出当前允许的 solar / lunar 入口。

所有正式快照必须记录：

- `chart_contract_id`；
- 引擎名称、版本、source revision、adapter version；
- school 与完整 chart config；
- 输入历法与实际调用入口；
- 出生输入和时间目标；
- 本命及全部已生成时间层的来源链。

缺失或不一致时，生产推理必须 fail closed，不得猜测、补默认值或静默修复。

## 3. 引擎职责边界

### 唯一生产计算引擎

`iztro-js@2.6.1` 是唯一生产排盘计算引擎。生产 NATAL 与所有 temporal facts 均由它生成。

### 仅供差分审计的实现

- `x-iztro 0.6.1` Rust/Python；
- 独立 Go core。

它们只用于发现实现漂移、序列化错误、边界差异和共享字段问题。它们不是生产 fallback，不是中州派语义权威，也不得通过多数投票覆盖 canonical iztro 输出。

### 明确禁止

- LLM 自行安星、排宫、计算大限或流年；
- 人工手排命盘进入正式生产链路；
- 为了命中知识规则而修改星曜、宫位、四化或时间层；
- 使用其他流派或其他引擎替代正式中州派命盘；
- 对错误或缺失快照进行静默补值、修盘或猜测；
- 把差分测试盘、合成盘或 test-only 产物送入正式推理。

测试环境可以构造负例或差分输入，但必须与生产路径隔离，并由生产快照校验器拒绝。

## 4. 生产准入

生产推理入口必须在加载任何宫位 Provider、规则 Runtime 或推理模块之前完成两道检查：

1. Full-chart structural contract：检查快照结构、字段、宫位和时间层完整性；
2. Canonical chart contract：检查 contract ID、iztro 引擎与版本、adapter、school、完整配置、输入历法和入口。

任一失败即拒绝进入推理。不能因为某张盘“看起来合理”或某条规则无法命中而放宽检查。

## 5. 变更控制

任何人或 Agent 都不得自行更改生产排盘流派、引擎、版本或固定配置。

未来如确需调整，必须同时具备：

1. PI 明确批准；
2. 新的、递增版本的 canonical chart contract；
3. 兼容性与历史快照迁移方案；
4. 本命、时间层、历法边界和大限切换的完整 P1 回归；
5. 新旧版本差异账本与明确的切换日期。

未完成上述步骤前，当前 v1.0 契约持续有效。

## 6. 证据边界

Chart Trust 的双实现/独立核心一致性用于证明确定性、可复现性和工程差异受控；它不等于证明所有传统命理命题为真，也不等于证明现实预测有效。

本契约只锁定排盘方法和计算链路，不创造、修改或晋升任何中州派知识规则。知识语义仍须由 Knowledge 来源审计和既有 Human Gate 决定。
