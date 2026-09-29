# A2-R1 History Heuristic Closure

Status: **HEURISTIC QUEUE CLOSED — SEMANTIC BACKSCAN REQUIRED**

## Scope closed

The deterministic history-marker scan produced 45 candidates. All 45 have now received source-span review.

Final candidate outcomes:

- 18 source-supported typed history transitions
  - ACQUIRED_DISPOSITION
  - PATH_DEPENDENT_GATE
- 2 normalization mismatches quarantined
  - ZZ-SYS-38-034
  - ZZ-SYS-50-028
- 25 reviewed non-history records
  - sequence-only
  - current-period-only
  - lookahead/future-check
  - case evidence
  - historical-context non-executable

No HEURISTIC_CANDIDATE remains.

## Important limitation

This closes the **heuristic candidate queue**, not the full semantic history audit.

The regex scanner is intentionally conservative and cannot prove exhaustiveness. During source review, additional cross-period statements were observed outside the 45 candidates. Therefore the project must run a second source-semantic backscan before declaring HISTORY_BACKWARD_AUDIT complete.

The semantic backscan must search and map phrases/concepts such as:

- 影响后运 / 决定后运 / 扭转后运
- 以后数年 / 他日
- 养成…性格 / 形成…性格 / 根深蒂固
- 长期 / 终身 / 一生受影响
- explicit statements that an action in one period changes later response eligibility

Each hit must be mapped to an existing canonical rule ID or logged as an extraction gap.

## A2-R1 boundary remains unchanged

No new architecture is introduced here. The same hard rules remain:

- natal essence E is not overwritten;
- acquired disposition and path-dependent gate remain distinct;
- no default duration/decay/weight is invented;
- a cross-period transition is executable only after source-span verification;
- source-normalization mismatches remain quarantined until repaired through auditable sidecars.

## Next

1. Run semantic source backscan beyond the 45 heuristic candidates.
2. Resolve every additional true cross-period hit.
3. Run regression + deterministic P0 gate.
4. If no new architecture is required, close PR #48 history work and proceed to LB-07.
