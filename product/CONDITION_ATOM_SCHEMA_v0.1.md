# Condition Atom Schema v0.1

状态：ACTIVE — PRODUCT IMPLEMENTATION SCHEMA

## 1. 目的

PL2 的条件层必须把“传统文本条件”和“运行时布尔判断”分开。

本 schema 只定义**工程表示**，不定义新的紫微理论，也不允许程序从自由文本自动猜条件。

```text
source condition text
  -> reviewed normalization
  -> typed condition atoms
  -> boolean condition spec
  -> RuleIR
```

## 2. Atom

每个 atom：

```json
{
  "atom_type": "PALACE_HAS_STAR",
  "args": {
    "palace": "P05",
    "star": "武曲"
  }
}
```

v0.1 允许：

- `SUBJECT_PRESENT`
- `STAR_PRESENT`
- `TRANSFORMATION_PRESENT`
- `PALACE_PRESENT`
- `PALACE_HAS_STAR`
- `PALACE_RELATION`
- `STRUCTURE_PRESENT`
- `BRANCH_PRESENT`
- `TIME_LAYER`
- `MODE_PRESENT`
- `TAG_PRESENT`

这些类型只是运行时事实词汇；具体某条传统规则应当映射成哪些 atoms，必须来自可审计 normalization，而不是 LLM 即时生成。

## 3. Boolean spec

```json
{
  "all_of": [
    {"atom_type": "PALACE_PRESENT", "args": {"palace": "P05"}}
  ],
  "any_of": [
    [
      {"atom_type": "STAR_PRESENT", "args": {"star": "武曲"}},
      {"atom_type": "STAR_PRESENT", "args": {"star": "天府"}}
    ]
  ],
  "none_of": [
    {"atom_type": "TAG_PRESENT", "args": {"tag": "QUARANTINED"}}
  ]
}
```

语义：

- `all_of`：全部满足；
- `any_of`：每个子组至少满足一个；
- `none_of`：全部不得出现。

v0.1 暂不支持隐式优先级、概率条件、连续权重或模糊匹配。

## 4. Canonical serialization

Atom 使用稳定 JSON canonical key：

```text
atom:{"args":{"palace":"P05","star":"武曲"},"type":"PALACE_HAS_STAR"}
```

键排序固定，因此参数输入顺序不同不会制造不同事实。

## 5. 安全边界

禁止：

- 从 condition 原文用关键词切分后直接上线；
- 用正则把“或”“除外”“见煞”“三方四正”等复杂语义拍扁；
- LLM 在请求时临时创造 atom；
- 未经 normalization verification 的 atom 进入 executable set；
- 将 CASE_SUPPORT_ONLY 记录直接转成一般规则。

## 6. PL2-B 验收

本阶段只验收 condition language 本身：

1. canonicalization deterministic；
2. unknown atom type fail closed；
3. all/any/none 可执行；
4. forbidden fact 可以阻断；
5. RuleRuntime 可消费 structured condition；
6. 原有简单 all-of registry 兼容。

实际事业/财帛规则的首批 atomization 在下一 checkpoint 单独进行并产生 coverage ledger。
