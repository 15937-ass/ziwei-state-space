# Execution evidence — P03 Issue #794

## Identity

- Issue: #794 — SP02-101…200 source-first spouse-palace audit.
- Lane / shard: KNOWLEDGE_ONLY / P03 夫妻宫.
- Base main SHA at activation: `0b372a188f2edf1bef3544c30c94388b6a88a131`.
- Branch: `knowledge/p03-794-spouse-sp02-101-200`.
- Source ID: `SRC-ZZ-003`, 《中州派紫微斗数深造讲义（下册）》, 下篇·宫垣论·夫妻宫.
- Approved source SHA-256: `6bddb3cac2e4b4efcf265229cbda22904ab3394aeef832e338ee5939088e5c5c`.
- Historical candidate index blob SHA: `0bc7a6f9c03790cf8b7c610a19ca55d78b3cf007`.

The original PDF's SHA-256 was recomputed locally and matched the approved pin. Original scan images for PDF physical pp18–19 were inspected directly; the audited printed-page span is pp35–37. Text extraction was used only to locate spans.

## Work performed

- Re-adjudicated exactly 100 candidate rows, SP02-101…SP02-200.
- 77 source-grounded candidate rows promoted into 77 source-audit records.
- 60 reusable projection/method records; 17 CASE_SUPPORT_ONLY records.
- 23 rows held because their historical YEAR/TIMING_TRIGGER mapping was not supported at that time-layer specificity.
- 0 deduplications; 0 history-feedback items; 0 new primitives, shared semantics, weights, probabilities or decay.
- Reconciled prior source gaps P03-SP01-GAP-002/003/004 using SP02-101, SP02-102/103, and corrected SP02-104 respectively. P03-SP01-GAP-001 remains open.
- Retained three printed-p37 gaps and recovered two printed-p35/p36 gaps from duplicate PR #795; six total open gaps including the prior p33 gap.
- Carried forward the two prior temporal-scope residuals and added ten grouped residuals for this batch.

## Required final exact-head gate

This evidence is source-review evidence, not a claim that repository CI has passed. The final PR head SHA and the workflow run tied to that exact head must be taken from the live PR/Actions records after all audit files, including this evidence file, are committed. Any later file change invalidates prior exact-head validation. Do not merge unless all of the following pass on the same final head and current main:

1. `python -m pytest -q`
2. Product JS adapter syntax check
3. `python src/audit_repository.py --fail-on-p0`
4. Repository Governance v1 validation with exact base/head
5. P03 write-set validation
6. Recheck main/base/head immediately before merge; if main advances, sync and rerun the exact-head gate.

The audit artifact does not authorize conditions_compiled, execution_unlocked, Product/runtime use, or any shared Core semantic change.

## Repair/recovery checkpoint — 2026-10-26, Asia/Shanghai

Ownership: this user-requested recovery takes over Issue #794 via PR #796 only;
PR #795 is retained as superseded comparison evidence, not an additional batch.
Observed parent head: `69064bf157182b3be4e23ef7a084a9239b487b79`.
Observed main/base: `0b372a188f2edf1bef3544c30c94388b6a88a131`.
The final exact head/run is recorded in the live PR after this file is committed.

Root technical failure: the SP01 test froze the shared current state at 100
reviewed candidates and 90 source records. SP02 correctly advances these to
200 and 167. Replaced obsolete snapshot assertions with exact reconciliation
against every batch ledger, retaining the SP01 source checks and adding a
duplicate-candidate check. Corrected 11/nine to 12/ten temporal-group labels.

Reconciliation: source hash recomputed against the supplied original PDF;
physical pp18–19 visually reinspected. Retain #796's full compound P03S-190
record; adopt #795's conservative event-only classifications for five records,
recover its two independent p35/p36 residuals, and preserve the anomalous
printed `机录像` without interpreting it as `机梁紫破`. Final result is 77
records (60 reusable / 17 case-only), 23 held; nine gap entries / six open;
12 temporal residual groups including two carried from SP01.

Timeout diagnosis: failed runs #40292978623 and #40294257789 terminated with
assertion failures (390.06s and 291.24s pytest), not Actions timeout. Duplicate
PRs were created 27 seconds apart. These demonstrate duplicated work and long
validation latency; they do not establish the cause of a ChatGPT request
expiry. No platform trace, HAR or tool-timeout log is available. Recover one
existing PR and its run identity; do not recreate the same 100-item audit or
start redundant identical CI on an unchanged validation identity.

Historical status note: when this recovery checkpoint was drafted, final validation had not yet completed. This records that historical point only. For current acceptance, use the live PR head and its matching GitHub Actions run; this file is not a live status cache and does not claim that any later head passed. All
source residuals remain explicit; no execution or empirical-validity upgrade.
