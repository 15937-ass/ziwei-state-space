# LB-07 ... LB-10 EXECUTION

Status: **ACTIVE — LB-07 COMPLETE; LB-08 NEXT**

Scope: 200 layer-boundary candidates in `P1_layer_boundary_review_batches_v0.1.csv`.

## Required cycle

For each batch:

1. source-span review against approved Zhongzhou source;
2. classify L1 intrinsic state / L2 relational state / L3 projection / mixed branch;
3. preserve raw canonical extraction;
4. create auditable split or correction sidecars when normalization needs repair;
5. quarantine source/normalization mismatches;
6. feed verified special cases back into ontology, system-mode, operator, history, or projection layers where justified;
7. run regression tests and deterministic P0 gate.

## Batch order

- LB-07: 50 candidates
- LB-08: 50 candidates
- LB-09: 50 candidates
- LB-10: 50 candidates

No human Gate is required for ordinary source normalization. Escalate only if evidence requires:
- a new primitive qi;
- a core operator-definition change;
- an unresolved major Zhongzhou conflict;
- a state architecture beyond A2-R1 typed history memory.
