# DECISION_LOG.md

All important conceptual decisions are recorded here.

## Frozen decisions

### D-001 — Paper-1 scope
**Decision:** Use Zhongzhou-school theory as the formal core.  
**Status:** FROZEN  
**Rationale:** Limits model complexity and school mixing; permits later ablation/extension.

### D-002 — Qi operational definition
**Decision:** Treat qi as a latent state representation, not as a proven physical energy.  
**Status:** FROZEN

### D-003 — No arbitrary empirical weights
**Decision:** Before system identification, use symbolic parameters, signs, order constraints, and qualitative classes rather than invented continuous weights.  
**Status:** FROZEN

### D-004 — Internal/external validity separation
**Decision:** Paper 1 evaluates formalization fidelity and reproducibility, not real-world predictive accuracy.  
**Status:** FROZEN

### D-005 — Nonlinear response assumption
**Decision:** Do not assume that star-system or temporal effects are simple additive linear combinations. Preserve state-dependent and interaction effects when texts require them.  
**Status:** FROZEN

### D-006 — Multi-agent method
**Decision:** Use artifact-centered role separation with producer/reviewer gates rather than training separate agents or allowing uncontrolled agent debate.  
**Status:** FROZEN

## Pending decisions

### P-001 — Candidate qi ontology dimensionality
Need initial 100-rule pilot before freezing.

### P-002 — Representation of five-element structure
Candidates: 5D simplex/vector + directed generation/control relations; graph-algebra representation.

### P-003 — Palace state organization
Candidates: 12 local latent states vs global latent state with palace projection operators.

### P-004 — First formal state equation
Candidate:
`x_(t+1) = F_theta(x_t, u_t^astro, G_t)`
Need rule extraction before choosing decomposition.

### P-005 — Structural observability criterion
To define after observation/projection schema exists.
