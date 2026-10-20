# Ordinal / Constraint Schema v0.1

Status: **SOURCE-EXPLICIT / NON-NUMERIC**

KB-WP08 保存来源已经明确表达的相对关系，而不是给传统术语补权重。

## 可保存
- A 强于 / 弱于 B；
- A 优于 / 不如 B；
- “最喜 / 最宜 / 最不喜 / 尤忌”等 source-local 极值偏好；
- “上格 / 次之 / 第一”等排序；
- “煞轻 / 煞重 / 重重 / 均弱”等非数值程度；
- “尤其 / 尤然 / 更甚”等局部强调。

## 禁止
- 把“重”写成 0.8；
- 把“最喜”写成高概率事件；
- 自动做 A>B 且 B>C 所以 A>C 的 canonical transitive closure；
- 对 OCR 不安全句静默校正后入库；
- 把“宜/不宜”普通建议一律当 ordinal。
