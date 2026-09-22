# KB-WP01 中州派核心语料覆盖矩阵报告

状态：COMPLETE（目录/章节级 Source Inventory）

## 1. 核心来源

已固定三本核心中州派材料：

1. 王亭之《中州派紫微斗数初级讲义》
   - SHA-256: `7ebafc8e3477430e2f8e69c6925ecc373d3c28966955f7035078c4949b7475a2`
   - PDF pages: 113

2. 《中州派紫微斗数深造讲义（上）》
   - SHA-256: `1cd57c205297f78004c0d59db7cb77b05ecad53313757e55d8f1c78600609e9a`
   - PDF pages: 124

3. 《中州派紫微斗数深造讲义（下）》
   - SHA-256: `6bddb3cac2e4b4efcf265229cbda22904ab3394aeef832e338ee5939088e5c5c`
   - PDF pages: 93

注意：coverage matrix 优先使用书内目录/印刷页码，不等同于 PDF 物理页号。

## 2. 已索引的知识域

### 初级讲义
已覆盖目录层级：
- 序论
- 入门及起例
- 安星法
- 闰月推算法
- 星盘推断法
- 形性赋/诸星形性
- 诸星曜基本性质
- 诸星曜入十二宫
- 辅佐煞曜对兄弟/子女/财帛/迁移/交友宫的影响
- 年限推断
- 大限/流年
- 流月
- 流日/流时
- 后记

### 深造讲义（上）
已覆盖：
- 序论
- 星曜论前言
- 十四正曜
- 六十星系
- 辅佐煞曜总论
- 辅佐八曜
- 煞曜
- 化曜
- 杂曜总论
- 流曜总论
- 星曜庙陷

### 深造讲义（下）
已覆盖：
- 宫垣论前言
- 命宫
- 兄弟宫
- 夫妻宫
- 子女宫
- 财帛宫
- 疾厄宫
- 迁移宫
- 交友宫/奴仆宫
- 事业宫/官禄宫
- 田宅宫
- 福德宫
- 父母宫

## 3. “Source Inventory COMPLETE” 的含义

本工作包的 COMPLETE 仅表示：

> 核心三本材料的目录、章节和主要页段均已经纳入 coverage matrix，不再存在“整章未被项目追踪”的盲区。

不表示：
- 规则已经全部抽取；
- 案例已经全部结构化；
- 每页都已人工复核；
- 每个章节已经达到 knowledge-module COMPLETE。

后续 KB-WP02～06 会把粗粒度 coverage unit 继续拆成：
- 星曜级；
- 星系级；
- 宫位级；
- 小节/页段级；
- case级。

## 4. 覆盖率计算原则

以后区分两种 coverage：

### Source Inventory Coverage
章节/页段是否已经被矩阵追踪。

当前核心三本：
**100%（目录/章节级）**

### Knowledge Extraction Coverage
已追踪页段中，可执行规则是否完成双遍抽取和审核。

当前显著低于100%，由 KB-WP02～05 逐步推进。

## 5. 下一步

进入 KB-WP02：

> 十四正曜全文穷尽式规则抽取。

第一阶段将把《深造讲义（上）》书内页 5–32 拆为十四个 coverage units，每颗正曜独立维护：
- raw source span
- atomic rules
- conflicts
- examples
- ontology mapping
- extraction completeness
- review status
