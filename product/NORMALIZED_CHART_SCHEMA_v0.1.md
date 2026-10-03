# Normalized Chart Snapshot Schema v0.1

状态：PRODUCT ENGINEERING CONTRACT  
用途：把不同排盘引擎的输出映射到同一个最小可比较结构，供 differential test 使用。

## 1. 认识论边界

Normalized snapshot 不是新的斗数理论，只是工程层中间格式。

它解决：
- 不同引擎字段名不同；
- 星曜数组顺序不同；
- 语言/序列化格式不同；
- 配置元数据遗漏导致的“假差异”。

它不解决：
- 哪个流派正确；
- 哪个引擎在争议规则上是真值；
- 现实预测是否准确。

## 2. 顶层结构

必需字段：schema_version、engine、input、chart。

engine 必须记录 name、version、source_revision（可空）、adapter_version。

input 至少记录 solar_date、time_index、gender、fix_leap 和 config。

chart 至少记录日期、命身信息、五行局与十二宫 palaces。

## 3. Palace object

每个 palace 以宫名为 key，至少包含：
- stem
- branch
- is_body_palace
- major_stars
- minor_stars
- adjective_stars
- decadal（如引擎提供）

星曜记录建议包含 name、brightness、mutagen、type、scope。

### 对比规则

集合语义：major_stars、minor_stars、adjective_stars、transformations、modifiers。
这些字段数组顺序不参与差异判定。

序列语义：大限列表、时间层列表、其他明确具有顺序含义的字段。

## 4. 必须记录配置

任何 cross-engine compare 都必须保存：
- engine name；
- engine version / commit；
- algorithm/school；
- day divide / early-late Zi policy；
- leap-month policy；
- year/horoscope divide；
- location/true-solar-time policy（若启用）。

没有配置快照的差异不得直接判为 bug。

## 5. 差异分类

后续每个 mismatch 最终必须归入：
- OUR_BUG
- EXTERNAL_BUG
- SCHOOL_DIFFERENCE
- CONFIG_DIFFERENCE
- INPUT_AMBIGUITY
- SERIALIZATION_ONLY
- UNRESOLVED

只有人工/文献解决后，才能进入 golden expected output。
