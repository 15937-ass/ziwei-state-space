# 中州派知识库完整度判据 v0.1

任何模块标记为 COMPLETE 前，必须同时满足：

## 1. Source coverage
- 对应章节页段 100% 已划分 coverage unit；
- 不存在未知遗漏页段。

## 2. Rule coverage
- 每个 coverage unit 至少完成两遍抽取；
- 所有可执行陈述均被标为：
  - rule；
  - example-only；
  - commentary；
  - unresolved。

## 3. Provenance
- 100% approved rules 有 source_id + location；
- 关键规则尽量有 page；
- OCR 不确定项有标记。

## 4. Schema quality
- required fields 完整率 = 100%；
- 原子化审计通过率目标 >= 95%；
- source claim / normalized interpretation 分离。

## 5. Conflict handling
- 发现的冲突 100% 进入 conflict registry；
- 禁止静默合并；
- 条件可解释冲突需标明 scope resolution。

## 6. Case coverage
- 所有教材显式案例都有 case_id；
- 每个案例映射到其测试的规则或反应原则。

## 7. Generative coverage
模块规则可以被 inference engine 调用；
不得只存在自然语言摘要而不能进入推演。

## 8. Regression tests
- 新规则加入后不能破坏已冻结 G1–G6 原则；
- 关键教材案例要作为 regression test。

## 9. Complete status

只有全部满足，模块才允许：

~~~text
status = COMPLETE
~~~

否则只能：
- inventory
- partial
- extracting
- reviewed
- near_complete
