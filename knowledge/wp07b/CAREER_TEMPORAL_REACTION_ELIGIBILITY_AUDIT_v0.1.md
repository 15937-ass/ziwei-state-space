# Career Temporal-Reaction Eligibility Audit v0.1

Status: **COMPLETE FOR THE CURRENT PL3-T CONTRACT**

## Scope and source basis

- Canonical source ID: SRC-ZZ-003, 《中州派紫微斗数深造讲义（下）》.
- Corpus: canonical Career/P09 rows CA01–CA09 on main.
- Scope: all nine rows whose normalized time layer is not NATAL.
- Method: compare the source-span meaning and its antecedent context with the current temporal asset adapter and reaction-compiler contract. This is an eligibility audit, not a rewrite of source rules.

## Result

- Candidates audited: **9**
- Eligible for executable normalization under the current contract: **0**
- Excluded directly because CASE_SUPPORT_ONLY: **1**
- Blocked pending antecedent, layer-scope, temporal-fact, or multi-year semantics: **8**
- Executable pilot emitted: **none**
- Production temporal reaction registry: remains intentionally empty.

Zero eligible candidates is a valid result. The audit must not force a rule into the registry just to make it non-empty.

## Findings

1. **Antecedent references are not automatically executable.** CA04-346 references CA04-345, which is CASE_SUPPORT_ONLY; CA06-545 references CA06-544, also CASE_SUPPORT_ONLY. CA05-496 points to a compound antecedent that includes case-support evidence and an underspecified “financial star” condition.
2. **The declared layer is narrower than the source scope.** Several source spans refer to “大运或流年” or “大运及流年”, while the current projection row declares only DECADE. A row must not silently discard the YEAR branch.
3. **The temporal fact adapter lacks star-bound transformation evidence.** It can expose STAR_PRESENT and TRANSFORMATION_PRESENT, but the condition-fact contract does not currently prove that the named star is the one carrying the named mutagen. CA04-350 is therefore not safe to normalize as a Wuqu-specific Hua Ji trigger.
4. **Terms such as “煞忌冲起”, “财星化忌…凑会”, “流年大运良好”, “大运或流年配合”, and “年限不佳” are not executable atoms merely because they are source-supported phrases.** They require source-faithful conditions that the current contract can actually observe.
5. **CA09-851 is path-dependent and multi-year.** The source's three-or-four-year wording remains literal evidence. It must not become a universal duration threshold, a hazard rate, or a new temporal clock.
6. **CA05-497 remains excluded.** Its source row is explicitly CASE_SUPPORT_ONLY and EVENT_CANDIDATE; it cannot be promoted to a reusable temporal reaction.

## Decision

No candidate is added to an executable registry. The existing empty production registry is the correct state under the current evidence and adapter contract.

## Handoff

- Knowledge: preserve the nine-row eligibility ledger and source provenance.
- Product: treat star-bound temporal transformation and explicit activation/convergence facts as interface gaps. Any schema/atom expansion requires a separate, versioned design and tests; it must not be smuggled into this Knowledge PR.
- Human Gate: no new theory decision is made here. If implementing “favorable/unfavorable period” or multi-year persistence requires new semantics, stop and submit a separate Chinese-language Human Gate request.
