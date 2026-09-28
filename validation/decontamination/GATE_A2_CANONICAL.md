# Gate A2（Canonical）：A2-R1 时序记忆与获得性状态架构

状态：**APPROVED AS A2-R1**  
前置 Gate：A0 APPROVED；A1 APPROVED  
批准人：PI  
批准结论：原 A2 方向通过，但按回源审核加入 typed memory 与 source-correction 两项硬约束。

## 1. 为什么必须修订 G5

原 G5 的 Paper-1 主模型近似为：

```text
fixed natal essence E + current temporal input -> current reaction
```

全文回源已确认存在跨期规则：某一运限中的反应、选择或经历可以改变后续运限的反应条件。于是同一 `E` 与同一当前输入，在不同历史下可以产生不同后续反应。

同时，中州派文本又区分原局本质与年限反应，因此 A2-R1 不允许用运限直接 overwrite `E`。

## 2. A2-R1 核心冻结

保留：

```text
E = fixed natal essence
```

新增 typed history memory：

```text
M_t = {D_t, H_t}
D_t = acquired disposition memory
H_t = path-dependent gate memory
```

当前反应：

```text
R_t = React(E, D_t, H_t, U_t, Z_t, G_t, C_t)
```

只有 source-explicit persistence / path-dependence rule 才允许：

```text
(D_(t+1), H_(t+1)) = T_k(D_t, H_t, R_t, U_t)
```

否则：

```text
D_(t+1) = D_t
H_(t+1) = H_t
```

## 3. 两类 history memory 不得混层

### ACQUIRED_DISPOSITION
表示源文明示某种后天倾向被形成、强化、固化、冷退或改变，并会影响后续反应。

### PATH_DEPENDENT_GATE
表示过去关键阶段、机会利用或事件是否发生，会改变后续规则的资格、分支或发展路径，但源文并未要求把它解释为人格/气机本身的永久改变。

## 4. Persistence 硬约束

没有 persistence 证据，不得自动假设状态永久保存。

允许的范围标记：
- `specific_next_period`
- `later_periods`
- `unspecified`

`decay` 默认必须为 `UNRESOLVED`。Paper 1 不得自动产生任何数值衰减率、记忆权重、学习率或持续年限。

## 5. Source correction：ZZ-SYS-38-034

A2-R1 回源发现：`ZZ-SYS-38-034` 当前归一化写成“七杀运检验天同先前形成的意志结构”，但对应源文未支持这一具体条件链。

因此：
- raw canonical 行保留，仅用于审计历史；
- `ZZ-SYS-38-034` 加入 quarantine，退出有效推理；
- 不把它迁移为 HistoryUpdate；
- 系统 38 的 source-supported path dependence 由已存在的 `ZZ-SYS-38-021` 承接，其对应“武曲破军考验性大限中的反应影响后运”。

## 6. 第一批 source-gated history transitions

- `ZZ-SYS-30-033` -> ACQUIRED_DISPOSITION
- `ZZ-SYS-31-020` -> PATH_DEPENDENT_GATE
- `ZZ-SYS-31-033` -> ACQUIRED_DISPOSITION
- `ZZ-SYS-38-021` -> ACQUIRED_DISPOSITION
- `ZZ-SYS-41-023` -> ACQUIRED_DISPOSITION

## 7. Paper 1 / Paper 2 边界

Paper 1 允许的是：`source-constrained symbolic hybrid state-transition system`。

一般连续递归 `x_(t+1)=F_theta(...)` 继续属于 Paper 2+ hypothesis。

## 8. A2-1 至 A2-5 决议

- A2-1：APPROVED WITH TYPED MEMORY
- A2-2：APPROVED；source-explicit 为硬门控
- A2-3：APPROVED；仅 symbolic / ordinal
- A2-4：APPROVED；一般递归留 Paper 2+
- A2-5：APPROVED WITH SOURCE CORRECTION；不得原样迁移 `ZZ-SYS-38-034`

## 9. Approval record

**PI approved A2-R1.**

如后续全文回源要求重写 natal essence、引入多宫长期历史传播、新增第二独立时间尺度或默认记忆衰减/遗忘机制，必须再次升级人工 Gate。
