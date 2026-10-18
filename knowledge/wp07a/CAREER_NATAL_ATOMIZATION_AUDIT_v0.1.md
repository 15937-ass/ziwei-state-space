# 事业宫原局规则原子化试点审查 v0.1

状态：**映射完成；仅供产品实现，不是可执行注册表**

## 一、范围与来源

- 工作单元：`KB-WP07A-CAREER-NATAL-ATOMIZATION-PILOT`
- 来源：`SRC-ZZ-003`，《中州派紫微斗数深造讲义（下）》
- 正式语料：事业宫 P09，CA01–CA09；CA09 已在主分支闭合。
- 本次只处理 CA04-347、CA04-349、CA09-852 三条原局规则。
- 对照材料：主分支 `src/product/condition_atoms.py` 的 `ALLOWED_ATOM_TYPES`，以及 `src/product/palace_structure.py` 的 `ResolvedPalaceStructure.runtime_facts`。

## 二、审查结论

| 来源规则 | 原局条件 | 现有原子映射 | 保留的投影目标 | 投影模式 |
|---|---|---|---|---|
| CA04-347，事业宫印刷页 140 | 武曲化科 | `TRANSFORMATION_PRESENT(palace=P09, star=武曲, mutagen=科)` | `career_requires_reputation_building` | `FUNCTIONAL_PROJECTION` |
| CA04-349，事业宫印刷页 141 | 武曲化忌 | `TRANSFORMATION_PRESENT(palace=P09, star=武曲, mutagen=忌)` | `technical_skill_work_scene_preferred` | `SCENE_TRANSLATION` |
| CA09-852，事业宫印刷页 154 | 破军化禄 | `TRANSFORMATION_PRESENT(palace=P09, star=破军, mutagen=禄)` | `multiple_jobs_side_roles_or_business_lines_are_common` | `FUNCTIONAL_PROJECTION` |

**结果：3 条全部完成映射，0 条因现有原子不足而阻塞。** 三条记录在正式语料中均为 `SOURCE_SPAN_VERIFIED`、`NATAL`、`CASE_SUPPORT_ONLY=false`。

### 为什么映射可以成立

当前原局事实生成器会对带有四化的星曜发出同时绑定宫位、星曜与四化的事实，例如：

```json
{
  "atom_type": "TRANSFORMATION_PRESENT",
  "args": {
    "palace": "P09",
    "star": "武曲",
    "mutagen": "科"
  }
}
```

因此，这里使用的是现有 `TRANSFORMATION_PRESENT` 原子，并保留 `palace + star + mutagen` 三者的绑定。不能用“武曲存在”与“某处有化忌”两个互不绑定的事实代替“武曲化忌”。

### 原典语义边界

- **CA04-347**：印刷页 140 将武曲化科与声誉联系。本映射保留已审核的目标“事业需要建立声誉”，不增加声誉分值或成功概率。
- **CA04-349**：印刷页 141 将技艺类工作作为武曲化忌的适宜场景。本映射保留原有 `SCENE_TRANSLATION`，不把邻近段落的经商资金限制另写成事件预测。
- **CA09-852**：印刷页 154 将破军化禄与兼行、兼职兼差等多线工作形态联系。本映射只保留多角色/多业务线投影；“非重点行业或职务后来成为事业基础”的路径关系属于 CA09-853，不并入本条。

## 三、邻近记录的排除清单

| 来源规则 | 排除原因 | 本次处理 |
|---|---|---|
| CA04-345 | `CASE_SUPPORT_ONLY=true` 且为 `EVENT_CANDIDATE` | 不推广为可复用原局规则 |
| CA04-346 | `DECADE` 时序触发，不是 `NATAL` | 归属已完成的 WP07B 时序资格审计 |
| CA04-348 | 条件包含“经商”，需要现实职业/行为背景 | 不以原局原子伪装成现实情境事实 |
| CA04-350 | `DECADE` 时序触发，原文涉及大运与流年 | 归属 WP07B；不混入 NATAL 映射 |
| CA09-851 | 连续多年良好流年，且标记 `PATH_DEPENDENT_GATE` | 保留原典的字面时序证据，不创建计时器或阈值 |
| CA09-853 | 非重点行业/职务先行、后成为事业基础，属于路径关系 | 不压缩成静态原局条件 |
| CA09-854 | 困苦在先、突然发展在后，属于路径关系 | 不压缩成静态原局条件 |
| CA09-855 | 需要突发之后的现实行为与后续结果 | 不将现实行为写成原局事实 |
| CA09-863 | “破军与火铃同度”的归一化条件尚需澄清 | 不猜测火铃组合的操作边界 |

排除记录只用于界定本次映射范围，不修改其来源行、审查状态或历史计数。

## 四、验证与交接

- 三条指定来源行均逐项核对了 `source_id`、印刷页码、`review_status`、`source_span_verified`、`time_layer` 与 `case_support_only`。
- 映射只使用现有允许原子 `TRANSFORMATION_PRESENT`，未新增原子、规则语义、阈值、权重或概率。
- 来源的 `projection_domain`、`projection_target`、`projection_mode` 原样保留。
- 没有修改任何 canonical source row，没有新增可执行规则，没有修改产品运行时或生产注册表。

**交给产品侧的内容**：可按 JSON 映射文件实现三条候选 NATAL 规则，并在产品侧独立验证运行事实、规则激活与证据追踪。知识侧映射完成不代表产品实现或预测有效性已经通过验证。
