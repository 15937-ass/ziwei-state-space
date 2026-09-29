# A2-R1 POST-APPROVAL EXECUTION

Status: **ACTIVE**

Checkpoint:
- Gate A0: APPROVED
- Gate A1: APPROVED
- Gate A2-R1: APPROVED
- A0/A1/A2-R1 checkpoint merged to main at `b3558d7a7e1ff138d1279408b07ddfc7ac6d6463`

## Frozen A2-R1 rules

1. Natal essence `E` remains fixed.
2. History memory is typed:
   - `ACQUIRED_DISPOSITION`
   - `PATH_DEPENDENT_GATE`
3. Only source-explicit cross-period evidence may update history memory.
4. No default persistence duration, decay, weight, learning rate, or continuous recurrence.
5. `ZZ-SYS-38-034` is quarantined; System-38 history uses source-supported `ZZ-SYS-38-021`.

## Automatic work sequence

1. Re-audit all 45 deterministic history-marker candidates.
2. Separate:
   - true acquired-disposition updates;
   - path-dependent gates;
   - sequence-only references;
   - ordinary current-period rules;
   - source/normalization mismatches.
3. Expand `knowledge/history/history_transitions_v0.1.csv` only after source-span verification.
4. Re-run ontology/system-mode regression after each resolved batch.
5. Resume LB-07 ... LB-16 under A2-R1.
6. Escalate only if evidence requires a new architecture beyond A2-R1.

## Human-review boundary

No new PI Gate is required for routine source verification, sidecar repair, typed history migration, or LB batch continuation within D-016. A new Gate is required only if the evidence demands:
- rewriting fixed natal essence;
- multi-palace long-memory propagation as a new structural primitive;
- a second independent time scale;
- default decay/forgetting dynamics;
- continuous learned recurrence in Paper 1.
