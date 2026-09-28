# HISTORY_MEMORY_SCHEMA v0.1

Status: **ACTIVE — APPROVED AT GATE A2-R1**

## 1. Purpose

Paper 1 represents only source-explicit cross-period dependence. It does not introduce free learned recurrence.

```text
M_t = {D_t, H_t}
D_t = acquired disposition memory
H_t = path-dependent gate memory
```

## 2. Controlled memory kinds

### ACQUIRED_DISPOSITION
Use only when the source explicitly says an experience/period forms, strengthens, entrenches, weakens, preserves, or changes a later-relevant disposition.

### PATH_DEPENDENT_GATE
Use when a previous period/event/choice changes later eligibility, branching, or development, without enough source support to claim an internal disposition was rewritten.

These types are distinct. A record must not silently move between them.

## 3. Required transition fields

- `transition_id`
- `memory_kind`
- `source_rule_id`
- `verified_source_location`
- `trigger_literal`
- `operation`
- `target_key`
- `persistence_scope`
- `source_epistemic`
- `normalization_epistemic`
- `execution_status`
- `notes`

## 4. Persistence scopes

Allowed values:
- `specific_next_period`
- `later_periods`
- `unspecified`

No default duration is inferred. Numeric decay, retention weights, learning rates, and time constants are forbidden in Paper 1 unless later approved under a separate Gate.

## 5. Source gate

A transition is executable only when source support is explicit, the source span has been reviewed, the effective source rule is not quarantined, and the transition does not overstate duration or magnitude. Otherwise history memory remains unchanged.

## 6. State semantics

Natal essence is immutable under temporal transitions:

```text
E_(t+1) = E_t = E
```

History update:

```text
M_(t+1) = T_k(M_t, R_t, U_t)   if source gate k is active
M_(t+1) = M_t                  otherwise
```

This is a symbolic hybrid transition interface, not an identified continuous dynamical law.

## 7. Epistemic boundary

The source supports the cross-period relation. The split into `D_t` and `H_t`, record IDs, enums, and software containers are project formalization/implementation choices and must be labeled as such.
