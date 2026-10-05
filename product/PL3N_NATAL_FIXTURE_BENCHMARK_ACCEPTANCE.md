# PL3-N Natal Fixture Benchmark Acceptance v0.1

状态：**IMPLEMENTED — CONTRACT FIXTURE REGRESSION READY**

## 1. 目的

PL3-N 在进入更多 domain 或 temporal layer 前，先建立一组小而明确的 deterministic contract fixtures。

它测试的是：

- executable rule composition；
- named structure preservation；
- Human Gate fail-closed boundary；
- Baiguan evidence profile；
- deterministic profile identity。

它**不测试现实预测准确率**。

## 2. v0.1 fixtures

### NF01
火星 + 地空 + 武曲化忌于财帛宫。

要求：
- W01-067 激活。

### NF02
财帛禄存、对宫福德天马。

要求：
- LU_MA_JIAO_CHI structure；
- W01-024 激活。

### NF03
紫微 anchor + 左辅/天魁支持证据。

要求：
- Baiguan = PARTIAL_SUPPORT；
- W01-095/096/098 不得激活；
- 不得生成 BAIGUAN STRUCTURE_PRESENT。

### NF04
紫微 anchor + 天府，同时天府与地空同宫。

要求：
- Baiguan profile = CONFLICTED；
- 不得升级完整百官 predicate。

## 3. 为什么 v0.1 不硬编码 golden profile_id

profile_id 会被 benchmark report 输出，并已有同输入同版本稳定性测试。

当前 v0.1 优先冻结：
- active-rule semantic expectation；
- structure expectation；
- Human Gate boundary。

等 NatalStateProfile schema 与 domain composition 再稳定一个版本后，再冻结 golden profile IDs，避免把早期 serialization 细节误当语义真值。

## 4. 下一步

当前 PL3-N 下一工作单元：

**PRODUCT_PL3N_CAREER_READINESS_AUDIT**

目的：
- 消费当前事业宫 WP05 corpus 状态；
- 区分 source-ready / normalization-needed / temporal / history / Human-Gate blocker；
- 在知识侧事业宫 closure 后，形成第一批 career executable candidates。

仍不进入 PL3-T。
