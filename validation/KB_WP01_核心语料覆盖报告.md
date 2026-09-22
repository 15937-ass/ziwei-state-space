# KB-WP01 中州派核心语料覆盖矩阵报告

状态：COMPLETE（目录/章节级 Source Inventory）

## 1. 核心来源

已固定三本核心中州派材料及文件指纹：

- 王亭之《中州派紫微斗数初级讲义》：SHA-256 `7ebafc8e...`，PDF 113页；
- 《中州派紫微斗数深造讲义（上）》：SHA-256 `1cd57c20...`，PDF 124页；
- 《中州派紫微斗数深造讲义（下）》：SHA-256 `6bddb3ca...`，PDF 93页。

coverage matrix 中的 page_start/page_end 优先采用书内目录/印刷页码，不等同于 PDF 物理页号。

## 2. Source Inventory Coverage

三本核心材料的主要目录/章节均已进入 `knowledge/coverage_matrix.csv`：

- 初级讲义：序论、起例、安星、闰月、星盘推断、形性、星曜基本性质、十二宫、辅煞宫位影响、年限/流月/流日时；
- 深造上册：序论、前言、十四正曜、六十星系、辅佐八曜、煞曜、化曜、杂曜、流曜、庙陷；
- 深造下册：前言及十二宫垣全部章节。

当前核心 Source Inventory Coverage：**100%（目录/章节级）**。

## 3. 重要边界

Source Inventory COMPLETE 不等于知识抽取 COMPLETE。

它只表示：

> 不再存在整章完全未被项目追踪的盲区。

后续 KB-WP02～KB-WP06 会把粗粒度 coverage unit 继续拆到：
- 星曜级；
- 星系级；
- 宫位级；
- 小节/页段级；
- 案例级。

## 4. 下一步

KB-WP02：十四正曜全文穷尽式规则抽取。

《深造讲义（上）》十四正曜书内页5–32将拆为十四个独立 coverage units，并要求：
- 双遍抽取；
- provenance 完整；
- source/normalization 分离；
- 冲突登记；
- ontology mapping；
- completeness 审核。
