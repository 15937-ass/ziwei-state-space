# PL3-N Wealth Domain Provider Acceptance v0.1

状态：**IMPLEMENTED — W01 EXECUTABLE-59 CONNECTED TO NATAL PRIOR**

## 1. 目标

把 PL2 已经安全 executable 的 W01 财帛宫规则接入 PL3-N NatalStateProfile。

本工作单元不新增传统规则，只做：

~~~text
PL2 executable W01
 -> EvidencePackage
 -> NatalDomainEvidence(domain=wealth)
 -> NatalStateProfile
~~~

## 2. Frozen baseline

provider 明确加载 8 个历史 batch：

1. PL2C
2. PL2F
3. PL2H
4. PL2J
5. PL2J2
6. PL2M
7. PL2L
8. PL2O2

合计 executable = **59**。

运行时初始化会重新 compile 并校验 59；任何 baseline drift 直接 fail closed。

## 3. Human Gate rows 继续不进入 provider

以下 8 条被硬排除：

- W01-016
- W01-017
- W01-022
- W01-023
- W01-035
- W01-095
- W01-096
- W01-098

原因不是 Human Gate 未批准，而是 post-gate remaining blockers 仍未关闭。

因此：

> Human Gate approval != executable truth predicate.

## 4. Feedback-free 保证

provider 没有：
- user history 参数；
- acquired-state 参数；
- outcome 参数；
- empirical probability；
- personalization。

输出为 NATAL EvidencePackage，再由 NatalDomainEvidence 冻结。

## 5. 产品意义

PL3-N 现在不只是“空容器”。

它已经可以对任一 Normalized Chart Snapshot：

1. 构建全盘 canonical facts；
2. 构建 approved named structures；
3. 保存 Baiguan evidence profile；
4. 激活当前 59 条 W01 executable rules；
5. 把 active rules / projection / conflict / confidence 放进 wealth domain；
6. 生成稳定 NatalStateProfile。

这构成第一条完整：

~~~text
chart -> canonical rule runtime -> natal domain evidence -> NatalStateProfile
~~~

链路。

## 6. 下一步

PL3-N 后续优先级：

1. 建立 generic domain-provider registry/interface；
2. 等事业宫 canonical executable registry 成熟后接入 career domain；
3. 扩展 EvidencePackage 的 canonical namespace；
4. 建立 Natal Prior snapshot/fixture benchmark；
5. 不提前进入 temporal outcome prediction。

当前产品下一 work unit 建议：

**PRODUCT_PL3N_DOMAIN_PROVIDER_REGISTRY**
