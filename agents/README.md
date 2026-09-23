# Ziwei Research Agent Runtime v0.1

目标：将 AGENT_WORKFLOW.md 中定义的研究角色转化为可执行任务框架。

当前阶段：离线可运行原型。

## Agent角色

- A0 Orchestrator：任务编排
- A1 Extractor：文本到原子规则
- A2 Ontology：规则到气机候选维度
- A4 Auditor：来源、冲突、过度推断检查
- A6 Writer：阶段报告

## 执行原则

1. 所有输出必须经过 schema 校验。
2. 未经人工Gate，不冻结核心理论变量。
3. 所有规则必须保留source provenance。
4. Agent只能修改draft层，不直接修改frozen层。
