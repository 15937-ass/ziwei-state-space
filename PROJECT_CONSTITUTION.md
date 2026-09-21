# PROJECT_CONSTITUTION.md

Version: 0.1  
Status: ACTIVE

This document defines the non-negotiable research rules for Paper 1.

## 1. Research scope

Paper 1 formalizes the **Zhongzhou-school Zi Wei Dou Shu** knowledge system into a machine-readable latent-state dynamical framework.

In-scope core:
- fourteen major stars,
- sixty basic star systems,
- auxiliary/supportive/malefic/transformation modifiers,
- twelve palaces,
- three-harmony/four-directions structural relations when explicitly required by Zhongzhou interpretation,
- natal essence versus decade/year temporal response.

Out of scope for the core Paper-1 model:
- Heluo qi-number positions,
- Qintian recursive flying transformations,
- self-transformation / centripetal transformation,
- Laiyin palace,
- seven-star positioning,
- full Northern-school flying transformation chains,
- empirical prediction-accuracy claims.

These may appear only as future extensions or comparative discussion.

## 2. Epistemic rule

Every domain claim must be assigned one epistemic class:

- **EXPLICIT** — directly stated in the approved source text.
- **INFERRED** — a transparent interpretation derived from one or more explicit passages.
- **HYPOTHESIS** — a modeling proposal introduced by this research.
- **IMPLEMENTATION** — a software or mathematical representation choice.

No INFERRED or HYPOTHESIS item may be presented as if it were an original Zhongzhou statement.

## 3. Provenance rule

Every EXPLICIT or INFERRED rule must contain:
- source work,
- source location/page when available,
- quotation/paraphrase note,
- rule author/reviewer,
- extraction version.

No provenance -> no promotion to the approved rule base.

## 4. Numerical rule

Before system identification:
- do not invent empirical continuous weights;
- use signs, order constraints, symbolic parameters, categories, or intervals where supported;
- illustrative numbers must be explicitly marked `ILLUSTRATIVE_ONLY` and excluded from findings.

Examples:
- allowed: `alpha > 0`
- allowed: `alpha_A > alpha_B`
- not allowed as research fact: `alpha = 0.73` without empirical estimation.

## 5. Qi definition

For Paper 1, “qi” is operationally defined as:

> a latent state representation introduced to unify repeated directional and relational properties in the textual Zi Wei system.

This project does not claim that qi is an empirically established physical substance or energy.

## 6. Model-separation rule

Keep separate:
1. latent qi state,
2. textual symbol/structure,
3. palace/context projection,
4. temporal stimulus,
5. observable event or interpretation.

Do not encode downstream event labels (wealth, divorce, surgery, etc.) as primitive qi dimensions without explicit justification.

## 7. Valence rule

“Good/bad” is not a primitive qi dimension.

Valence must be treated as context-dependent suitability, balance, stability, or downstream outcome evaluation.

## 8. Internal vs external validation

Paper 1 may test:
- rule coverage,
- annotation agreement,
- logical consistency,
- traceability,
- semantic fidelity,
- executable reproducibility,
- internal case reconstruction.

Paper 1 must not describe those tests as proof of real-world predictive validity.

## 9. Human approval gates

The following require PI approval before being frozen:
- rule schema,
- candidate qi ontology,
- fourteen-star cores,
- sixty-star-system model,
- state-space definitions,
- paper conclusions.

GPT-generated artifacts remain provisional until the relevant gate is approved.

## 10. Agent behavior

Agents must:
- prefer source-grounded extraction over elegant completion,
- preserve unresolved contradictions,
- report uncertainty,
- never silently reconcile conflicting passages,
- separate production from review,
- write machine-readable artifacts whenever possible.

## 11. Versioning

Frozen artifacts use semantic project versions:
- `v0.x` exploratory,
- `v1.0` first frozen Paper-1 model.

All major conceptual changes must be recorded in `DECISION_LOG.md`.
