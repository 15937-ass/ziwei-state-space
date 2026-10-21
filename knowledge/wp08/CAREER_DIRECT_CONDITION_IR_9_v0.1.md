# Career Direct Condition IR 9 v0.1

Status: **9 / 9 direct conditions serialized at Knowledge layer — Product compiler still OFF**

This artifact serializes nine blocker-free direct Career conditions using only existing canonical Knowledge semantics.

It is deliberately narrower than Product RuleIR:
- no Product facts are generated;
- no runtime matcher is authorized;
- no free-form Chinese parser is used;
- no global ANY/ALL rule is created;
- generic `会/同会` is never assigned a geometry when the source has not fixed one.

## Direct IR set

1. CA02-181 — 天机 + 龙池凤阁 pair, SAME_PALACE.
2. CA03-228 — 天机巨门 + source-local ANY(火星,铃星), SAME_PALACE.
3. CA05-411 — 天同化忌 + source-local ANY(四煞 members), SAME_PALACE.
4. CA05-417 — 天同 + 龙池凤阁 pair, SAME_PALACE.
5. CA05-419 — 天同化忌 + FOUR_DIRECTIONS_VISIBILITY of explicit BOTH(左辅,右弼).
6. CA05-433 — 天同巨门 + source-local BOTH(天厨,火星), SAME_PALACE.
7. CA07-638 — 贪狼 + explicit BOTH(左辅,右弼), SAME_PALACE.
8. CA07-681 — 子午巨门 + local OR(巨门化禄, 禄存).
9. CA09-820 — 子午七杀 + local OR(武曲化禄, 贪狼化禄, 破军化禄, 禄存).

CA05-484 / CA06-582 / CA07-699 remain explicit negative controls for unresolved generic meeting/composition semantics.

`conditions_compiled=0`; `execution_unlocked=0`.
