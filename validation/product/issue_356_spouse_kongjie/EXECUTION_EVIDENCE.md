# Issue #356：事业—夫妻空劫条件与完整来源上下文

Execution runtime: Codex / OpenAI cloud environment
Environment: Python3.12.14; Node v24.19.0; Linux x86_64
Original base: 9116579ce35de7ad4556a77430005641946c633d
Final base: 63b36749806949e166eb81f14f2e7fa19454b466
Final head/tree: recorded in GitHub Issue/PR after publication.

## Result and review

Career NATAL provider expands34 ->35 by adding only CA01-023 from merged #331.
All previous34 rule entries and source handoffs are unchanged as JSON values.
Knowledge mapping, canonical CSV and ontology files are not edited.

Producer: exact global P09->P03 OPPOSITE prerequisite plus four complete reviewed
alternatives: two 寅申 orientations × two 地空/地劫 allocations. Pin the full
source_context. Because this artifact has no source_span_summary, report uses
its reviewed normalized_reading verbatim and exposes the complete source_context.
Four context fields must be nonempty and match the pinned Product object exactly.
No invented source paraphrase is introduced; previous summary/modality fields
are retained for existing rules.

Critic: test both allocations over all12 branches, each missing star, each star
moved to any of the other11 palaces, and wrong spouse branch. Relation absence is
independently tested using an in-memory ontology-negative provider fixture only;
no ontology file/production relation semantics changes. Context omission,
empty reading, dropped Product pin, context wording drift, relation omission
and branch omission all fail closed. Actual reports retain the reviewed OCR
uncertainty, exact scope and provenance, with no real-world-event claim.

The source projection spouse_influence_can_impair_career is a conditional research
statement, not empirical proof or relationship advice. No rule triggers a
statement that an observed spouse harmed career. No temporal, probability or
causal-certainty upgrade. Empty production temporal registry still yields PARTIAL.

## Commands

Run from repository root:

```bash
PYTHONPATH="$PWD" python -m pytest -q tests/test_product_career_spouse_kongjie.py tests/test_product_career_cross_palace.py tests/test_product_career_natal_domain_provider.py
PYTHONPATH="$PWD" python -m pytest -q
node --check tools/iztro_export.mjs
node --check tools/iztro_full_export.mjs
PYTHONPATH="$PWD" python src/audit_repository.py --fail-on-p0 --output /tmp/issue356-audit.json > /tmp/issue356-audit.stdout
PYTHONPATH="$PWD" python validation/product/issue_356_spouse_kongjie/audit_native_inference.py /tmp/ziwei-336/p1_iztro_js.jsonl /tmp/ziwei-336/p1_xiztro_rust.jsonl --report validation/product/issue_356_spouse_kongjie/native_inference_report.json
PYTHONPATH="$PWD" python tools/p1_compare_full.py /tmp/ziwei-336/p1_iztro_js.jsonl /tmp/ziwei-336/p1_xiztro_rust.jsonl --report validation/product/issue_356_spouse_kongjie/dual_engine_report.json --fail-on-diff
python tools/validate_governance.py --base-ref origin/main --head-branch product/356-career-spouse-kongjie
git diff --check
git diff --exit-code origin/main -- knowledge .github validation/knowledge
```

Results:
- Targeted42 passed /0 failed /0 skipped.
- Original-base full pytest638 passed /0 failed /0 skipped.
- Final latest-main full pytest652 passed /0 failed /0 skipped.
- Node/P0 audit/Product governance/scope checks PASS. P0=0; existing907 P1 candidates remain.
- Raw Product API/report JS400/400 + Rust400/400 target runs PASS; all raw input
  preserved, existing source traces/modality preserved; no temporal reactions.
- Dual-engine comparison100 natal/400 temporal, zero differences.
- Reports in this directory: native_inference_report.json, dual_engine_report.json.

## Concurrent-main integration

Knowledge PR #355 merged as63b36749806949e166eb81f14f2e7fa19454b466 while this unit
was running. Restored its five exact blobs, verified each Git SHA, reconstructed
the exact base tree and imported its signed commit locally. Full pytest and
Product governance were repeated on the integrated tree; Node and P0 were also
repeated. Fire/bell source dossier still leaves CA01-035 blocked and adds no
Product executable rule. No consumed mapping or Product code changed during
integration, so completed raw engine regression remains applicable.

## Limits and skipped scopes

Cached pinned iztro-js2.6.1/x-iztro-rust0.6.1 adapter0.2 exports from #336/#342 are
unchanged; exact hashes/revisions in raw audit report. No engine reinstall or
export regeneration; original reproduction commands are preserved in #336.
Raw regression charts do NOT activate CA01-023. Its four positive alternatives
and negative gates are tested in synthetic API fixtures; this proves conditional
logic/source trace only, not birth-chart reachability, case validity or real-world
causation. Repeated targets are not independent natal cases. No personal inputs.

No PL1/calendar/Zi-day/exporter/algorithm changes; Go/B02 NOT_REQUIRED and not
claimed (Go unavailable). No GitHub Actions. Empirical predictive validity and
production temporal reaction readiness remain unestablished.
