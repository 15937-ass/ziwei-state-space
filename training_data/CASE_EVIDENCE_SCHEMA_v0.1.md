# CaseEvidenceRecord Schema v0.1

```yaml
case_id: string
source:
  book_id: string
  page_start: int
  page_end: int
person_group_id: string
birth:
  raw_text: string
  normalized:
    solar_date: string|null
    lunar_date: string|null
    time_index: int|null
    gender: string|null
    location: string|null
question:
  raw_text: string
  domains: [string]
context:
  stated_past_facts: [string]
chart:
  snapshot_ref: string|null
  engine_version: string|null
reasoning:
  author_claims:
    - claim_id: string
      text_span_ref: string
      normalized_claim: string
      linked_rule_ids: [string]
      inferred_operators: [string]
      temporal_layer: string|null
      palace_targets: [string]
      epistemic_status: string
prediction_claims:
  - prediction_id: string
    event_type: string
    time_window: string|null
    polarity: string|null
feedback:
  immediate: [string]
  later_outcomes: [string]
grades:
  provenance: string
  outcome: string
review:
  status: string
  notes: string|null
```

## Outcome grade

- O0_NONE：无后验结果；
- O1_SUBJECTIVE：只有主观反馈；
- O2_STATED_EVENT：书中明确描述后来事件，但无独立核验；
- O3_EXTERNALLY_VERIFIED：可由独立公开/可靠来源核验。

## Provenance grade

- P1_PAGE_BOUND：案例与页码已绑定；
- P2_CHART_REBUILT：出生资料已重新排盘；
- P3_RULE_LINKED：推理句已链接 canonical rule；
- P4_HUMAN_REVIEWED：完成案例级人工/PI抽检。
