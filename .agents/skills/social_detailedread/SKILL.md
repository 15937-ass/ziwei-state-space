# Zi Wei Dou Shu DetailedRead

A thin, manually invoked, read-only helper for **private-chat detailed Zi Wei Dou Shu readings**. Use it when the user asks for **紫微斗数详批、完整看盘、全面详解、详细批一下、完整命盘分析** or explicitly upgrades a current QuickRead with wording such as “继续详批”“完整展开”“把各方面详细说说”.

It is a task instruction over the accepted Product/Knowledge stack, not a separate inference engine.

## How to use it

1. Identify the chart/person from the current conversation. A same-conversation upgrade from QuickRead keeps the same chart unless the user explicitly changes person/chart. If essential chart information is missing, ask one short clarification instead of guessing.
2. Follow the accepted current-main DetailedRead contract in `product/DETAILED_READ_V0_1.md` and `src/product/detailed_read.py`. Use only accepted current-main runtime/source material. Do not re-create a second rule engine in this Skill.
3. Treat DetailedRead as **full inspection with progressive retrieval**, not one giant repository read. Consider the full supported NATAL domain surface, but retrieve evidence in the staged plan and deepen only domains that need more support or that the user asks to expand.
4. Prefer private-chat staged delivery:
   - 全盘总论 + 性格/精神；
   - 学业事业 + 财富资源；
   - 感情 + 家庭 + 人际合作；
   - 迁移/外部环境 + 健康 + explicitly requested time layer；
   - 3–5 条最强综合主线，并接受用户继续深挖。
   If the user explicitly asks for one complete report, the same evidence-bounded material may be assembled into one coherent response after the required inspection.
5. Organize the answer by life themes rather than mechanically reciting twelve palaces. Reconcile cross-domain signals before writing a conclusion. If two supported signals apply under different conditions, preserve the distinction instead of forcing one verdict.
6. On a QuickRead -> DetailedRead upgrade, reuse the same-chart supported context and already-read evidence when actually available. Retrieve newly needed domains progressively; do not pretend evidence was reused when no verified continuation/context is available.

## Evidence and interpretation boundaries

- Accepted `main` is the source of truth. Never treat an Issue, unmerged PR, archived branch, online口诀, another school, or model memory as accepted Zhongzhou evidence.
- Full inspection does **not** mean every topic must receive a strong conclusion. If accepted support is weak or absent, keep that part brief, mark it insufficient/unknown, or omit unsupported detail instead of inventing filler.
- RUNTIME, SOURCE and any MODEL_SUPPLEMENT remain distinct. Model wording/synthesis may help explain evidence but cannot inflate runtime/source coverage or invent source/rule identities.
- A NATAL pattern supports a tendency, not proof that a concrete event happened. Specific DECADE/YEAR claims require matching accepted temporal evidence for that layer.
- Health content is non-diagnostic. Do not turn astrological material into medical diagnosis, treatment, prognosis, or disease certainty.
- Traditional child counts, death/injury, marriage timing and similar concrete family events must not be generalized from case-only material or weak support.
- Hide rule IDs, source paths, coverage/debug metadata and internal reasoning in ordinary private-chat output unless the user asks why or requests evidence.

## Boundaries

Read-only. A user asking for a DetailedRead does not itself start repository implementation, consume a governance/Product/Knowledge WIP slot, create an Issue/PR, or authorize writes. The Skill consumes the best accepted content currently available on `main`; later accepted Knowledge/Product improvements can improve future readings automatically.
