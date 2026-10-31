# DetailedRead private-chat full reading v0.1

Status: Product planning/orchestration contract. It reuses the accepted QuickRead evidence stack and makes no deployment or predictive-validity claim.

## 1. Purpose

DetailedRead is the private-chat **advanced reading** mode. QuickRead remains the concise entry mode. DetailedRead performs a systematic full-chart inspection, retrieves evidence progressively, reconciles cross-domain conclusions, and presents the result by life theme rather than by mechanically reciting twelve palaces.

DetailedRead is **not** a second rule engine, a second Knowledge registry, a new chart calculator, or an LLM client.

## 2. Canonical chart prerequisite

DetailedRead is not a chart calculator. Before any chart facts enter a DetailedRead session, the caller/Skill must require a snapshot accepted by `product/CANONICAL_CHART_CONTRACT_v1.1.md`: Zhongzhou + pinned `iztro-js@2.6.1` and the exact fixed configuration. The LLM must never manually calculate or repair palace placement, stars, transformations, DECADE, YEAR or other temporal scopes. A third-party or manually supplied chart without verifiable canonical metadata is unverified and cannot be represented as the system's calculated chart.

If the canonical snapshot or generator is unavailable, stop before making canonical chart claims. The session remains a read-only evidence retrieval/orchestration component and does not create chart facts.

## 3. Product shape

The intended interaction is:

```text
QuickRead
  -> user asks “完整详批 / 详细看一下”
  -> DetailedRead plan
       -> atomic domain evidence reads
       -> progressive continuation for complex domains
       -> cross-domain consistency pass
       -> multi-turn private-chat delivery
       -> 3–5 strongest integrated themes
```

A user can also enter DetailedRead directly without first using QuickRead.

## 4. Backend inspection surface

A full NATAL plan always represents all twelve palace domains:

```text
life / siblings / relationship / children
wealth / health / migration / friends
career / property / fortune / parents
```

“Full” means **full inspection**, not “force a strong conclusion in every domain.” A domain with no accepted runtime/source support remains uncovered or brief; the verbalizer must not invent filler merely to make the report look complete.

Retrieval is atomic by domain/time-layer slot. Sections may reuse a domain, but that does not duplicate retrieval identity.

The planner also emits staged retrieval batches aligned to the private-chat delivery order. Stage 1 only needs the domains required for overview/disposition; later stages add previously unseen domains. Optional temporal slots are deferred until the environment/health/time stage. Therefore “full chart” does not mean “fetch all twelve domains before the first reply.”

## 5. User-facing sections

DetailedRead organizes the private-chat reading as:

1. 全盘总论
2. 性格、精神与行为方式
3. 学业、事业与工作方式
4. 财富与资源模式
5. 感情与亲密关系
6. 家庭与代际关系
7. 人际、合作与社会关系
8. 迁移、外部环境与发展
9. 健康与身心倾向
10. 时间层与阶段（only when explicitly requested and supported）
11. 综合收束：最值得注意的 3–5 条主线

These are synthesis sections, not one-to-one palace dumps.

## 6. Progressive evidence retrieval

Each atomic slot uses the existing QuickRead request/evidence contract. The current reader's default first pass remains 20 source items per slot and continuation may fetch later unseen batches.

When upgrading from QuickRead, `continuation_for_detailed_slot(...)` may reuse a previous main-pinned continuation **only for a slot that was already in the previous request**. It retains the same `main_sha` and seen evidence identities, so the first DetailedRead continuation does not repeat already-seen evidence. Newly introduced domains start a fresh first pass.

The underlying reader still rejects a stale continuation if `main` changed. DetailedRead must not silently combine accepted evidence from two repository snapshots.

## 7. Dynamic evidence budget

DetailedRead does not define a giant fixed total evidence count. The caller should:

- run a first pass for every needed atomic slot;
- deepen only domains whose evidence is complex, conflicting, or directly requested by the user;
- stop when additional evidence is repetitive or irrelevant;
- preserve unresolved/unsupported domains instead of filling them with model memory.

This keeps a full reading broad without making every domain equally expensive.

## 8. Cross-domain consistency pass

Before final synthesis, the caller/verbalizer must reconcile at least:

- career vs wealth vs life/migration;
- relationship vs life/fortune/migration;
- parents/siblings/children/property family boundaries;
- friends/siblings/career/children social-role boundaries;
- migration signal vs actual career/wealth outcome;
- health vs life/fortune with non-diagnostic wording.

A contradiction is not automatically an error. Preserve the different conditions or scopes when accepted evidence genuinely points in different directions.

## 9. Temporal analysis

NATAL is always the base layer. DECADE and YEAR slots are opt-in only.

A non-NATAL slot requires both `CANONICAL` and `TEMPORAL` namespaces under the existing QuickRead contract. If matching accepted temporal evidence is absent, DetailedRead must say that the period cannot yet be grounded rather than relabeling natal evidence as a specific-year result.

## 9. Private-chat delivery

Prefer staged delivery instead of a single giant report:

1. 全盘总论 + 性格；
2. 事业 + 财富；
3. 感情 + 家庭 + 人际；
4. 迁移 + 健康 + explicitly requested time layer；
5. 3–5 条综合主线和 user-selected deep dives.

The user may interrupt at any point and request a deeper topic. That topic may consume additional continuation batches while other domains remain at first-pass depth.

## 10. Safety / epistemic boundaries

- Current accepted `main` remains the source of truth.
- RUNTIME / SOURCE / MODEL_SUPPLEMENT stay separate.
- Model supplementation never increases runtime/source coverage and cannot invent rule/source IDs.
- Natal pattern is a tendency, not proof a concrete event occurred.
- Health output is not medical diagnosis, treatment, prognosis, or disease certainty.
- Traditional child counts, death/injury, marriage timing and similar concrete family events are not generalized from case-only material.
- No Knowledge/KIB/runtime semantics, probability, or predictive-validity status changes in this feature.

## 11. Governance boundary

The Product layer owns this planning contract and implementation. A natural-language Agent Skill for “详批 / 完整看盘” is Governance-owned under `.agents/skills/**` and must be a separate bounded Governance integration after this Product contract is accepted on `main`.

## 12. Session-level runner and immutable main pin

Product #951 adds \`DetailedReadSession\` in \`src/product/detailed_read.py\`. It orchestrates the existing planner and the accepted QuickRead reader; it does not create a second evidence parser or rule engine.

- The first atomic-slot read resolves the accepted \`main\` SHA and pins the session to it.
- Every later independent slot read passes \`expected_main_sha\` to \`load_latest_main_knowledge(...)\`. If \`main\` has moved, the reader fails closed and the whole session must restart on a fresh snapshot; it may not mix commits.
- A QuickRead upgrade must pass the same \`target_id\`. Its continuation cursor is reused only for the slot already present in that cursor. Newly introduced domains start a fresh first pass but retain the same session-level main pin.
- \`run_stage(...)\` is idempotent and retrieves the not-yet-read atomic slots in the requested delivery stage. \`run_all_stages(...)\` completes the planned first pass. \`continue_slot(...)\` deepens one domain using its own seen-evidence cursor and the same main pin.
- The session report always includes all twelve NATAL domains, including \`NOT_INSPECTED\`, \`UNKNOWN\`, \`BLOCKED\` or \`NOT_AVAILABLE\` states. Unequal coverage remains explicit.
- \`RUNTIME\`, accepted \`SOURCE\`, and \`MODEL_SUPPLEMENT\` are serialized separately. Model supplementation can be attached only to an already-inspected slot and cannot increase runtime/source coverage.
- Case-only, unpromoted, uncertain/unverified, temporal-mismatch and missing-provenance exclusions remain separate counts; excluded material is not inserted into runtime/source evidence.
- The report carries the plan's cross-domain checks, thematic sections and staged delivery order. The session itself does not reconcile or erase conflicting claims; the downstream verbalizer must preserve their conditions, scopes and provenance.
- The runner performs no chart calculation, runtime execution, LLM call, KIB promotion, registry mutation or runtime authorization.

