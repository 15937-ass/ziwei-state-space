# Source Literal Normalization Semantics v0.1

Issue: #467  
Status: **representation-only; no execution unlock**

本层解决的是“source literal 还没有被正规化”，而不是“原书没有给答案”。

## 原则
- 显式星名不能因为旧 tokenizer 未识别就继续作为 generic literal。
- 原文明写 `或`、同度、相对、会合时，只保存 source-local clause structure。
- `煞 / 吉 / 凶` 可正规化到 scoped open category / valence，但不因此闭合成员。
- `昌曲 / 火铃 / 空劫` 等已知 group 可以被识别，但不因此获得 ANY / ALL / N_OF。
- 显式列出多个星名，只证明“这些名称在 source surface 中被列出”；若前一轮 source quantifier review 仍未解决数量/合取语义，则保留 `SOURCE_LIST_QUANTIFIER_UNSPECIFIED`，不能偷偷解释为 ALL。
- `刑曜 / 禄 / 吉辅 / 财星化禄 / 火曜` 等 source shorthand 若证据不足，使用 `SOURCE_SHORTHAND_MEMBERSHIP_UNSPECIFIED`。
- `昌曲化忌` 或未指定载体的 `化禄`，保留 `TRANSFORMATION_CARRIER_UNSPECIFIED`。
- “多辅曜 / 多见火曜”保留 cardinal wording，但不发明“多=几颗”。

所以 generic blocker 可以被消除，但 genuine source uncertainty 只会被**精确化**，不会被吞掉。
