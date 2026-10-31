# Canonical Zhongzhou Chart Contract v1.1

Status: **CANONICAL PRODUCTION CONTRACT — PI APPROVED / PENDING ACCEPTANCE**

PI decision: 2026-10-31  
Implementation: Product Issue [#981](https://github.com/15937-ass/ziwei-state-space/issues/981)  
Supersedes: `product/CANONICAL_CHART_CONTRACT_v1.0.md` for all newly generated production snapshots  
Machine-readable authority: `product/CANONICAL_CHART_CONTRACT_v1.1.json`

## 1. 唯一生产排盘方法

本项目所有正式命盘事实必须使用**中州派排盘口径**，并由固定版本的 **iztro JS 2.6.1** 生成。

适用范围：

- NATAL 本命盘；
- DECADE 大限；
- AGE / SMALL_LIMIT 小限；
- YEAR 流年；
- MONTH 流月；
- DAY 流日；
- HOUR 流时。

上述所有时间层必须由同一固定排盘契约生成。大限、流年等时间事实由同一 iztro chart instance 的 horoscope 接口计算，不得由 LLM 根据出生日期、年龄或年份自行推算。

## 2. v1.1 固定配置

| 字段 | 唯一允许值 |
|---|---|
| School / algorithm | `zhongzhou` |
| Production engine | `iztro-js` |
| Engine version | `2.6.1` |
| iztro source revision | `2c7ef9be669df7b19d1799f4dce335fed3794f78` |
| Adapter version | `0.3` |
| Astro type | `heaven` |
| `fix_leap` | `true` |
| `day_divide` | `current` |
| `year_divide` | `normal` |
| `horoscope_divide` | `normal` |
| Language | `zh-CN` |

除明确修正的子时日界外，其余 v1.0 配置保持不变。

## 3. 子时分界：中州派生产规则

本条以王亭之《中州派紫微斗数初级讲义》“出生时换算法”一节为来源依据。该节指出，关于 23:00–01:00 是否统归当日子时存在争论；王亭之明确选择按表列分割，并说明**交入 00:00 才是新一天的开始**。

因此，本项目选定中州派作为唯一生产流派后，子时规则必须固定为：

| 输入真太阳时 | time_index | 日期归属 |
|---|---:|---|
| 23:00–23:59（晚子时） | 12 | 仍属于输入日期 |
| 00:00–00:59（早子时） | 0 | 属于已经进入的新日期 |

对应 iztro 配置：

- `day_divide=current`：晚子时归当日；
- 禁止使用 `day_divide=forward` 生成 v1.1 生产盘。

这里的“当日”指输入中已经确定的日期，不得因 23:00 进入晚子时而自动把日期加一。00:00 后，输入日期本身应当是新日期。

## 4. 时间输入契约：当前已是真太阳时

v1.1 规定，当前进入排盘引擎的出生时间**已经是真太阳时**。

- 每个生产输入必须记录 `time_basis=true_solar_time`。
- 排盘引擎不得再次根据出生地经度、时区或地点对时间进行修正。
- 当前排盘不要求出生地点字段。
- 地点换算暂不属于排盘引擎；未来如增加，必须作为独立的上游预处理步骤，在进入排盘引擎前完成，并记录转换来源与结果。
- 同一输入不得被重复校正。未来地点预处理完成后，仍须向排盘引擎提供符合本契约的时间输入，并保留预处理 provenance。

这是当前项目的输入接口约定，不把未来地点换算逻辑提前混入本次排盘实现。

## 5. 输入与快照 provenance

出生日期输入可以是公历或农历，但必须明确记录输入历法和对应入口：

- solar：`astro.withOptions`；
- lunar：`astro.byLunar`。

每份正式快照必须记录：

- `chart_contract_id=ZHONGZHOU_IZTRO_JS_2_6_1_V1_1`；
- 引擎名称、版本、source revision、adapter version；
- school 与完整 chart config；
- `time_basis=true_solar_time`；
- `location_correction_applied=false`；
- 输入历法与实际调用入口；
- 出生输入和时间目标；
- 本命及全部已生成时间层的来源链。

缺失或不一致时，生产推理必须 fail closed，不得猜测、补默认值或静默修复。

## 6. 引擎职责边界

### 唯一生产计算引擎

`iztro-js@2.6.1` 是唯一生产排盘计算引擎。生产 NATAL 与所有 temporal facts 均由它生成。

### 仅供差分审计的实现

- `x-iztro 0.6.1` Rust/Python；
- 独立 Go core。

它们只用于发现实现漂移、序列化错误、边界差异和共享字段问题。它们不是生产 fallback，不是中州派语义权威，也不得通过多数投票覆盖 canonical iztro 输出。跨流派/独立引擎在晚子时的差异只作诊断，不得覆盖本项目已选定的中州派 same-day 规则。

### 明确禁止

- LLM 自行安星、排宫、计算大限或流年；
- 人工手排命盘进入正式生产链路；
- 为了命中知识规则而修改星曜、宫位、四化或时间层；
- 使用其他流派或其他引擎替代正式中州派命盘；
- 对错误或缺失快照进行静默补值、修盘或猜测；
- 对已经是真太阳时的输入再次进行地点/经度校正；
- 把差分测试盘、合成盘或 test-only 产物送入正式推理。

## 7. v1.0 → v1.1 迁移

v1.0 固定使用 `day_divide=forward`，而 v1.1 固定使用 `day_divide=current`。因此：

- v1.0 的 contract、快照、测试输出和执行报告均保留为历史证据，不得覆盖或伪装成 v1.1；
- v1.0 快照不满足 v1.1 生产准入，必须由 v1.1 exporter 重新生成后才能进入新的生产推理；
- 不自动批量改写历史出生日期、历史案例或 source signatures；
- 若历史案例要用于 v1.1 生产链路，必须重新核对来源输入、重新排盘、重新验证锚点，并生成新的 provenance；
- v1.0 与 v1.1 的结果差异必须归档，不得通过手工改星盘消除。

详细迁移边界见 `product/CANONICAL_CHART_MIGRATION_v1.0_to_v1.1.md`。

## 8. 生产准入

生产推理入口必须在加载任何宫位 Provider、规则 Runtime 或推理模块之前完成两道检查：

1. Full-chart structural contract：检查快照结构、字段、宫位和时间层完整性；
2. Canonical chart contract：检查 v1.1 contract ID、iztro 引擎与版本、adapter、school、完整配置、时间输入基准、输入历法和入口。

任一失败即拒绝进入推理。不能因为某张盘“看起来合理”或某条规则无法命中而放宽检查。

## 9. 变更控制

任何人或 Agent 都不得自行更改生产排盘流派、引擎、版本或固定配置。

未来如确需调整，必须同时具备：

1. PI 明确批准；
2. 新的、递增版本的 canonical chart contract；
3. 兼容性与历史快照迁移方案；
4. 本命、时间层、历法边界和大限切换的完整 P1 回归；
5. 新旧版本差异账本与明确的切换日期。

本 v1.1 变更已经获得 PI 明确批准；正式生产切换仍以 PR 合并及验收通过为准。

## 10. 证据边界

Chart Trust 的双实现/独立核心一致性用于证明确定性、可复现性和工程差异受控；它不等于证明所有传统命理命题为真，也不等于证明现实预测有效。

本契约只锁定排盘方法和计算链路，不创造、修改或晋升任何中州派知识规则。知识语义仍须由 Knowledge 来源审计和既有 Human Gate 决定。
