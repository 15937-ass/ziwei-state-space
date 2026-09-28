# src

当前状态：**ACTIVE EXECUTABLE PROTOTYPE**

当前模块：

- `audit_repository.py` — deterministic P0 schema/provenance gate
- `audit_layer_boundary.py` — L1/L2 与 L3 projection 边界候选审计
- `audit_history_markers.py` — history/path-dependence candidate scan
- `rule_engine.py` — immutable canonical + sidecar 的 effective-rule loader/query/trace
- `model_spec.py` — Paper-1 symbolic model objects，包括 A2-R1 typed history memory
- `validate_corpus.py` — corpus validation utilities

当前 `rule_engine.py` 仍是**有效规则视图/查询与溯源层**，尚不是完整端到端推演引擎。WP07 将补齐：

```text
chart structure
-> natal essence
-> star/system modes
-> modifier operators
-> typed history memory
-> temporal reaction
-> cross-palace projection
-> semantic output
-> provenance/conflict/uncertainty trace
```

硬约束：实现不得静默添加 approved artifacts 中不存在的领域知识；不得把 heuristic candidate 自动升级为 executable rule。
