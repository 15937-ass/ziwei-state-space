# 事业宫星曜存在条件映射审查：CA01-026 至 CA01-044（限定批次）

状态：**8 条源文映射完成；全部不可执行**
工作单元：`KB-WP07A-CAREER-STAR-PRESENCE-CA01-026_027_031_034_042_044`
来源：`SRC-ZZ-003`，《中州派紫微斗数深造讲义（下）》印刷页 132–133。

## 一、映射清单

| 来源规则 | 原始位置 | 原始条件 | 原始投影目标 | 模式 |
|---|---|---|---|---|
| CA01-026 | 事业宫printed_p132-133 | 事业宫见地空地劫 | `niche_or_nonmainstream_industry_suited` | `SCENE_TRANSLATION` |
| CA01-027 | 事业宫printed_p132-133 | 事业宫见地空地劫 | `unconventional_operating_method_suited` | `FUNCTIONAL_PROJECTION` |
| CA01-031 | 事业宫printed_p133 | 事业宫见陀罗 | `career_development_slow` | `FUNCTIONAL_PROJECTION` |
| CA01-032 | 事业宫printed_p133 | 事业宫见陀罗 | `nominal_status_exceeds_real_authority` | `FUNCTIONAL_PROJECTION` |
| CA01-033 | 事业宫printed_p133 | 事业宫见陀罗 | `career_reversals_or_instability` | `FUNCTIONAL_PROJECTION` |
| CA01-034 | 事业宫printed_p133 | 事业宫见擎羊古今转换 | `engineering_or_technical_scene` | `SCENE_TRANSLATION` |
| CA01-042 | 事业宫printed_p133 | 事业宫与禄存同度 | `existing_business_or_salaried_role_preferred` | `SCENE_TRANSLATION` |
| CA01-044 | 事业宫printed_p133 | 禄存再与空劫同度 | `advance_retreat_indecision` | `FUNCTIONAL_PROJECTION` |

## 二、源文锚点与条件解释

### CA01-026 / CA01-027：事业宫地空、地劫

印刷页 132（PDF 第66页右栏，续至印刷133页／PDF第67页左栏）将事业宫见地空、地劫与较冷僻行业及出人意料的营运方式联系。两条规则共用条件 `PALACE_HAS_STAR(P09,地空) AND PALACE_HAS_STAR(P09,地劫)`，但分别保留行业场景与营运方式两个原始目标。缺少任一星曜均不匹配。

### CA01-031 / CA01-032 / CA01-033：事业宫陀罗

印刷页 133 说“事业宫最不宜见陀罗”，并分别提及事业发展缓慢、名义与实际权力不相称、事业反覆。三条映射都使用 `PALACE_HAS_STAR(P09,陀罗)`，但不合并成一个含混的负面结论，也不新增严重程度或概率。

### CA01-034：擎羊的古今职业解释转换

印刷页 133 明确写到古代武职与现代工程科技人员的解释转换。映射只保留现代职业场景目标 `engineering_or_technical_scene`，并在审查元数据中保留古今转换语境；不把古代职业分类原样套用于现代。

### CA01-042：事业宫禄存同度

印刷页 133 将禄存同度联系到经营现成事业或受薪的场景，同时提醒不可据此单独论富。因此只映射 `PALACE_HAS_STAR(P09,禄存)` 与原始目标，不添加财富结论。

### CA01-044：禄存与空劫同度

同段在禄存同度的基础上进一步描述“若更见空劫同度，则主进退失据”。映射要求禄存、地空、地劫三曜全部位于 P09；不将前一条的禄存单星条件与本条复合条件混为一谈。

## 三、排除项

- **CA01-035**：“火铃”简写是否要求火星、铃星同时出现，尚需来源语义审查。
- **CA01-043**：条件为“前格”，保留为上下文依赖项。
- **CA01-045**：“前格勉强求变”依赖前文，未压缩成单星条件。

## 四、验证与边界

确定性测试从真实 `ResolvedPalaceStructure.runtime_facts` 发出的事实进行匹配，并核对 canonical 行的来源位置、条件、审核状态、时间层级、投影域/目标/模式和原始 history_feedback。测试覆盖缺少任一必需星曜、星曜放错宫位、三曜条件缺项等负例。

本批只使用现有 `PALACE_HAS_STAR`。所有映射 `executable_registry_entry=false`；没有修改源行、产品运行时或生产注册表，也没有创建数值权重或概率。


## 五、本轮复核及限定语

直接核对本轮附件 PDF 第66–67页（印刷131–134页）；第67页左栏为本批陀罗、擎羊及禄存段。地空地劫段的起始页是印刷132页，故两条映射的单页锚点修正为132；canonical来源范围132–133保持原样。CA01-032原页字形为“权力被挂空”，引文保留原字，不按通行措辞改写。

“往往”“有时亦主”“一般只宜”是源文解释边界，逐条保存在 `source_modality_note`；它们不构成概率、事件必然性或唯一职业判断。CA01-027与行业场景是并列解释，不要求两个现实结果同时发生。地空地劫段的后天人事提醒亦保留，不据星曜存在推断现实成败。

红队复核发现测试原先遗漏映射文件名的 `MAP_`，已修正。补齐八条映射逐一缺少每颗必需星曜的负例，并将该星移到其他11宫逐一验证；这些是条件语义测试，不是真实排盘可达性或经验预测测试。三条排除项仍未升级。

本轮核对附件 SHA-256：`6bddb3cac2e4b4efcf265229cbda22904ab3394aeef832e338ee5939088e5c5c`。原始附件不上传仓库。
