# Source Literal Normalization Semantics v0.1

Issue: #467  
Status: **representation-only; no execution unlock**

本层解决的是“source literal 还没有被正规化”，而不是“原书没有给答案”。

## 原则

- 显式星名 / 显式列名集合，不因旧 tokenizer 未识别而继续作为 generic literal。
- 原文明写 `或`、同度、相对、会合时，只保存 source-local clause structure。
- `煞 / 吉 / 凶` 可正规化到 scoped open category / valence，但不因此闭合成员。
- `昌曲 / 火铃 / 空劫` 等已知 group 可以被识别，但不因此获得 ANY / ALL / N_OF。
- `刑曜 / 禄 / 吉辅 / 财星化禄 / 火曜` 等来源 shorthand 若当前证据不足，使用精确的 `SOURCE_SHORTHAND_MEMBERSHIP_UNSPECIFIED`。
- `昌曲化忌` 这类 transformation carrier 未明确时，保留 `TRANSFORMATION_CARRIER_UNSPECIFIED`。
- “多辅曜 / 多见火曜”保留 cardinal wording，但不发明“多=几颗”。

因此，本层允许 generic blocker 消失，但 genuine source uncertainty 必须转成更精确的 blocker，而不是被吞掉。
