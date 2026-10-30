# PI 级研究路线调整提案 v1.1：原局详批先行，时间层递进

- 提案 Issue：[#947](https://github.com/15937-ass/ziwei-state-space/issues/947)
- 提案 PR：[#948](https://github.com/15937-ass/ziwei-state-space/pull/948)
- 状态：**PI_APPROVED_SCOPE / FORMAL_GOVERNANCE_IMPLEMENTATION_PENDING**
- PI 决策日期：2026-10-30
- 性质：Knowledge / Core / Product 的长期研究顺序与协作路线调整；不构成新的紫微斗数理论、语义授权、KIB 晋升或运行时授权。

---

## 1. 已批准的项目主路线

PI 已批准以正常学习与推演顺序组织产品建设：

**原局（NATAL）详批闭环 → 大限（DECADE）分析 → 流年（YEAR）分析。**

Knowledge、Core、Product 不再采用“知识全部完成后产品再开始”的串行模式，而是分工并行：

1. Product 先使用当前 main 上已经接受、实际可用的原局能力，打通十二宫原局详批。
2. Knowledge 宫位线继续按现行宫位顺序和槽位规则做来源研究，并逐步补充大限、流年的来源材料与时间层标注。
3. Core 在当前 C9 完成后，优先研究原局、大限、流年之间的共享时间层语义与作用关系。
4. Product 在原局详批稳定后，消费已经接受且达到相应消费条件的时间层成果，先升级大限，再升级流年。
5. 案例重建贯穿原局和时间层开发，作为推理方法与来源忠实度的验证材料；不再把 WP03/WP06A 独立案例试点排在原局产品闭环之前。

这条路线的目标不是先做出“什么都能断”的长报告，而是逐层形成**能检查、能解释、能追溯、知道何时应当停止**的紫微斗数推演系统。

## 2. 当前已有基础与真实缺口

### 2.1 原局产品基础已经存在

以下工作已经在 main 上形成基础，后续必须复用，不重复造轮子：

- Product #798：QuickRead capability-aware evidence contract 与 current-main knowledge reader，区分 RUNTIME、SOURCE、MODEL_SUPPLEMENT。
- Product #882：DetailedRead v0.1 规划器，规定十二宫 NATAL 检查面、主题式章节、渐进式读取、跨领域一致性检查和分阶段输出。
- Governance #894 / PR #895：自然语言 DetailedRead Skill 已接入，负责把“详批/完整看盘”路由到既有 Product 契约。
- 确定性排盘和现有 NATAL 规则运行能力继续复用。

**当前缺口不是再设计一份详批目录，而是让已有 DetailedRead 规划器真正消费整盘证据，形成完整的原局分析流程和可验收输出。**

### 2.2 原局覆盖并不均衡

- Career NATAL 已有 190 条接受的规则。
- Wealth NATAL 仍为部分覆盖（Product state 记录 W01 59/100 executable）。
- Natal Essence Graph 仍为部分实现。
- 其他宫位的 runtime、source-backed 和未知状态各不相同。

因此，十二宫都进入检查流程，不等于十二宫都已经拥有同等强度的知识，更不等于每一宫都必须给出强结论。

### 2.3 KIB 为空不应阻塞原局详批建设

当前 P4 候选影响评估没有产生可晋升的 K_manifest 条目，active KIB / lock 保持原状；15 个 KMN / 15 个 KMM 也不能被误认为已经获得 Product 消费或执行授权。

但这不妨碍 Product 使用现有、已接受且允许使用的 RUNTIME 与 SOURCE 证据建设原局详批。必须继续分开报告：

- 实际执行过的 RUNTIME；
- 可检索、可解释但未获执行授权的 SOURCE；
- 明确标为非 canonical 的 MODEL_SUPPLEMENT；
- BLOCKED / UNKNOWN / NOT_AVAILABLE 等缺口。

不得为了让详批显得完整而绕过 KIB、allowed-use 或知识晋升制度。

### 2.4 大限、流年能力仍未形成完整闭环

当前已有时间环境基础设施和部分条件编译/评估能力，但生产时间反应内容仍然稀疏或为空，M0 的生产映射也未准备好。

因此，不能把“已经有 temporal data structure”说成“已经能完整推演大限流年”。后续必须由 Knowledge 和 Core 提供有来源的时间层知识，再由 Product 按正式消费条件逐步接入。

---

## 3. 阶段一：先打通原局 NATAL DetailedRead

**优先级：Product 第一优先级；可与 Knowledge 宫位线及当前 Core C9 并行。**

### 3.1 实施原则

复用 #798、#882、#894 和现有 chart/runtime/readers。不得重建第二套排盘引擎、规则引擎、Knowledge registry 或 DetailedRead Skill。

目标链路：

```
同一张命盘
  -> 确定性排盘与结构化 chart facts
  -> DetailedRead 十二个 NATAL atomic slots
  -> current-main progressive evidence retrieval
  -> RUNTIME / SOURCE / MODEL_SUPPLEMENT 分层
  -> coverage / gap report
  -> 跨宫、跨主题一致性检查
  -> 主题式、分阶段原局详批
```

### 3.2 必须具备的能力

1. **十二宫完整检查**：十二个 NATAL domain 都必须进入计划和覆盖报告，不能因当前规则较少而直接跳过。
2. **主题式组织**：最终按全盘总论、性格精神、事业、财富、感情、家庭、人际、迁移、健康等主题组织，不机械逐宫念规则。
3. **渐进式读取**：首轮保持轻量；对证据复杂、冲突或用户追问的主题再继续读取，保留 continuation、去重和 main snapshot pinning。
4. **证据分层**：RUNTIME、SOURCE、MODEL_SUPPLEMENT 分开计数和表达；模型补充不能冒充 canonical 规则或提高知识覆盖率。
5. **跨领域校验**：至少检查事业—财富—迁移、感情—命/福德、家庭成员边界、人际角色边界、健康措辞等既有 DetailedRead checklist。
6. **缺口可见**：没有充分证据的主题可以简短说明、保留 UNKNOWN 或标记不可用，不为凑成“完整报告”而补写。
7. **分阶段交付**：优先总论/性格，再事业/财富、关系/家庭/人际、迁移/健康，最后收束 3–5 条最强主线；用户明确要求单篇完整报告时可以合并呈现。
8. **同盘连续性**：QuickRead 升级 DetailedRead 时，只复用确实存在且 main 版本一致的已读证据；没有可验证 continuation 时不得声称已经复用。

### 3.3 原局详批 v1 的验收

- 一张输入命盘能够生成完整的十二宫 NATAL inspection plan。
- 每个 domain 都有独立、可追溯的 runtime/source/model/gap 状态。
- 已读证据和新读取证据能够去重，且绑定同一 main snapshot。
- 主题章节能消费多宫位证据，并执行跨主题一致性检查。
- 重要结论能追溯到实际证据；证据不足时保留不确定性。
- 不将原局倾向写成已经发生的具体事件。
- 复用 #882 / #894，不重复实现规划器或自然语言路由。
- 不要求十二宫达到同一覆盖率，也不以报告长度作为验收指标。

### 3.4 明确不包含

第一版只交付 NATAL 原局详批闭环。除非用户明确提出且有相应 accepted temporal evidence，否则不输出具体大限、流年结论；不修改 canonical Knowledge、active KIB/lock、生产 registry、runtime 权限、概率或预测有效性。

---

## 4. 阶段二：Knowledge 与 Core 同步建设大限、流年知识

本阶段与阶段一的 Product 原局建设并行，不要求 Product 等待全部时间层知识完成。

### 4.1 Knowledge 宫位线

宫位线继续遵守现行宫位顺序、每宫 WIP 和来源审查合同。每次处理相关材料时，逐步明确记录：

- 来源描述的是 NATAL、DECADE 还是 YEAR；
- 时间层作用对象及其宫位/星曜范围；
- 与原局结构的关系；
- 大限与流年条件是否同时出现、是否存在前后依赖；
- 四化、星曜、宫位、辅煞等条件的限定、前提和例外；
- 来源明说的结果、候选应象与不能推出的结论；
- 来源冲突、缺失条件和 UNKNOWN。

不得把仅有原局性质的文本改写成大限或流年规则，也不得把不同时间层的相似词句自动视为同一语义。

### 4.2 Core：C9 之后的共享研究重点

当前 Core C9 #945 / PR #946 必须先按原定范围完成，不扩大其写集、不改变其验收目标。

**C9 完成后的 Core 首要方向调整为：原局—大限—流年时间层关系与反应语义研究。**

核心研究问题包括：

1. NATAL 原局结构在时间推演中承担什么基础角色；
2. DECADE 环境如何作用于原局，哪些关系有来源依据；
3. YEAR 条件如何与所处 DECADE 及 NATAL 结构发生关系；
4. 大限、流年四化及相关星曜条件如何区分环境、引动、反应和应象；
5. 多层条件、跨宫依赖、继承条件、修饰条件和来源前提如何保留；
6. 哪些关系可以明确描述，哪些仍需保留 UNKNOWN / HOLD。

必须继续区分已批准 v0.4 架构中的：

- `N`：Natal Essence / 原局本质；
- `E_decade`：大限时间环境；
- `E_year`：流年时间环境；
- `τ_t`：原局对特定时间环境的反应；
- `M0`：有来源支持的应象候选。

不能预先假设大限和流年简单相加、线性叠加或共享一个无条件算子；具体关系必须由来源和案例支持。Core 只负责共享语义和契约，不代替宫位线抽取宫位专属规则，也不直接授权 Product/runtime 执行。

### 4.3 案例与六十星系的定位

WP03 六十星系验证、WP06A 案例重建不取消，但调整为**服务于原局详批和时间层关系的验证材料**：

- 用代表性星系检查单星性质如何进入星系本质；
- 用教材案例重建作者从命盘事实到原局判断的推理链；
- 选取具有大限/流年材料的案例，检验时间层解释是否忠实于作者原文；
- 记录无法重建的步骤、反例、缺失前提和跨案例差异。

案例数量按来源完整度和可重建性确定，不为凑数降低标准。案例只能支持方法重建或其明确范围内的判断，不自动成为经验概率 ground truth。

---

## 5. 阶段三：Product 接入大限 DECADE

触发条件：Knowledge/Core 已在 main 形成与大限有关、来源可追溯、allowed-use 明确且达到对应 Product 消费条件的检查点。

Product 在 NATAL 基础上增加：

- 大限所处的时间环境 `E_decade`；
- 与原局 N 的关系；
- 有来源支持时才生成的反应描述 `τ_decade`；
- 仍然未知、受阻或缺少条件的部分。

输出必须明确区分“原局本质”“大限环境”“原局在该环境下的反应”。不能把大限宫位或四化直接写成必然现实事件，也不能用模型补充填补没有获准消费的语义。

Product 只消费已接受并 pin 住的 main checkpoint；Knowledge 合并不自动更新 Product active lock。若材料尚未达到消费条件，Product 可以展示时间层事实和缺口，但不得声称完成大限推演。

---

## 6. 阶段四：Product 接入流年 YEAR

触发条件：阶段三的大限结构稳定，并且 Knowledge/Core 已提供可消费的流年条件和层间关系。

Product 在原局和大限基础上增加：

- 流年环境 `E_year`；
- 流年与所处大限、原局之间有来源支持的条件关系；
- 有来源支持时才生成的流年反应 `τ_year`；
- 不同时间层之间的前提、修饰、冲突和未知项。

必须保留“某年出现一个条件”与“某年必然发生某个事件”的区别。大限与流年的层间依赖不得被压平成单一吉凶标签。无足够 accepted evidence 的宫位/领域继续 fail-closed。

---

## 7. 案例验证、Forecast Ledger 与经验有效性

案例重建不是等到所有产品功能完成后才开始，而是贯穿原局、大限和流年的开发：

- 原局阶段：检验单星、星系、宫位和跨宫综合是否忠实于教材案例；
- 大限阶段：检验阶段环境和原局反应的重建；
- 流年阶段：检验年层条件、所处大限与原局之间的关系；
- 专家方法评估与现实预测有效性分别记录，不得混为一谈。

Forecast Ledger 仍遵守 v0.4 原门槛：只有第一条 `N -> E -> τ -> M0` source-only vertical slice 真正可执行后，才按其既有规则启动前瞻记录。来源忠实度、专家方法忠实度和现实预测有效性是不同指标；前两者通过不代表第三者通过。

---

## 8. 三线并行与槽位规则

本次路线调整不改变现有 WIP 上限和集成制度：

- 宫位线：继续现行一次一个宫位的准入安排；
- Knowledge Core：最多一个 ACTIVE work unit；
- Product：最多一个 ACTIVE work unit；
- Core 与 Product 可并行推进，Product 可消费已接受的旧 checkpoint，Core 同时建设下一批时间层语义；
- 宫位线按现有依赖继续来源工作，不等待 Product；
- 最终合入 main 仍由 #888 Integration Lease 串行控制。

**原提案中的“两宫位并行槽位试点”没有包含在本次 PI 批准范围内。** #676 记录的一次一个宫位安排继续有效；不得把 P06 #773 自动作为第二个并行槽位启动。若未来要改变宫位并行度，必须另行提出并取得 PI 明确批准。

---

## 9. 证据、治理和禁止越界事项

以下边界全部保留：

- accepted main 是正式输入；未合并 PR、Issue 描述、旧分支和模型记忆不能当作 accepted Knowledge。
- 原文、页码、来源哈希、条件、前提、例外、否定、时间层和反例必须可追溯。
- Zhongzhou canonical 与其他流派材料严格隔离；跨流派方法比较不能反写中州 canonical。
- RUNTIME / SOURCE / MODEL_SUPPLEMENT 分开；`RETRIEVAL_ONLY`、`SEMANTIC_ONLY`、`CASE_SUPPORT_ONLY`、`BLOCKED` 不得被 Product 偷换成 `EXECUTABLE`。
- S1–S6（来源明文、保真归一化、研究假说、PI 接受的理论结构、可执行契约、经验校准）可作为研究成熟度描述；它们不自动构成新的晋升权限或替代现有 Human Gate。
- 不新增未经批准的 universal primitive、执行算子、概率、权重、因果关系或预测有效性。
- 不把健康材料转成医学诊断、治疗或预后；不从弱证据/案例材料强推婚育、伤亡等具体事件。
- Knowledge merge 不自动改变 Product KIB/lock；Product 变更仍需独立影响评估、验证和明确晋升授权。
- 所有正式集成遵守 #888、路径所有权和 exact-head 全量质量门。

---

## 10. PI 汇报与阶段验收

每轮汇报优先回答：

1. 本轮真正弄明白了什么；
2. 直接来源和案例证据在哪里；
3. 哪些反例、条件或边界不支持该解释；
4. 这项发现对原局、大限、流年哪一层有何影响；
5. 是否存在真正需要 PI 决定的理论问题；
6. 下一步最值得推进什么。

路线阶段验收：

| 阶段 | 完成标志 |
|---|---|
| 原局详批 | 十二宫 NATAL 全检查、证据分层、跨主题综合、缺口透明、输出可追溯 |
| 大限 | accepted 时间层证据可被 Product 安全消费，N 与 E_decade / τ_decade 清晰分离 |
| 流年 | accepted 流年证据与大限/原局层间关系可被 Product 安全消费 |
| 案例验证 | 能重建与不能重建的推理步骤均有来源和边界记录 |
| 预测有效性 | 仅在独立、适当的前瞻或经验设计下单独评估，不由传统案例代替 |

任何阶段都不以“十二宫必须全部有强结论”或“报告必须给出具体事件”作为完成条件。

---

## 11. 获批后的治理实施

PI 已在 2026-10-30 明确批准本提案第 1 节所述的 NATAL → DECADE → YEAR 主路线。

后续通过独立、有界 Governance work unit 完成正式控制文件和恢复入口更新：

- 建立版本化的 Core + Product continuation plan v2，保留 v1 作为历史基线；
- 更新 Core plan pointer #901：当前 C9 仍先完成，C9 之后转向共享时间层语义研究；WP03/WP06A 案例重建作为验证输入；
- 更新 Product plan pointer #900：Product 第一优先级改为 NATAL DetailedRead 闭环；大限、流年按 accepted Knowledge/Core checkpoint 递进；
- 更新 Product recovery state 和三线启动入口；
- Core state 的最终恢复指针应与 C9 合并时的真实状态一起更新，避免与 C9 当前写集冲突；
- 不修改 #676 的一次一个宫位决定，不改变 G12 硬上限，不在本次实施中启动第二宫位槽位。

本次路线批准不代表该 Governance 实施 PR 已经合入 main；在正式计划、入口和状态缓存通过治理验证并合入前，实时 Issue/PR 仍优先。

---

## 12. PI 决策记录与边界

### 已批准

- 原局 NATAL 详批作为 Product 第一优先级；
- Knowledge 与 Core 并行建设大限、流年所需知识；
- Product 先完成原局，再在 accepted checkpoint 基础上升级大限，最后升级流年；
- 案例重建服务于原局和时间层推理验证，不再作为原局产品闭环之前的独立首要阻塞。

### 未批准 / 不在本次范围

- 两个宫位同时 ACTIVE 的并行试点；
- 任何新的 KIB / runtime / registry 晋升或执行授权；
- 新的概率、因果、权重或现实预测有效性主张；
- 任何将其他流派内容并入 Zhongzhou canonical 的修改。

**项目目标：先让系统真正读懂并综合一张原局命盘，再让它逐步理解大限如何改变环境、流年如何在大限与原局条件下发生作用。每一层都必须有来源、有条件、有边界，并且能够被 Product 实际检验。**
