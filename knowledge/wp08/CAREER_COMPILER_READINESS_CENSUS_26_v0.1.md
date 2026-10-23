# Career Compiler Readiness Census 26 v0.1

Status: **26 / 26 audited — 12 Knowledge condition-IR-ready, 14 still fail-closed**

Issue #510 audits every Career row currently marked `LOCAL_STRUCTURE_READY` after closure v0.15.

The key result is that **row-local readiness is not compiler readiness**.

## Census

- LOCAL_STRUCTURE_READY rows: **26**
- DEPENDENCY_EFFECTIVE_UNDERDETERMINED: **11**
- DEPENDENCY_CONDITION_IR_READY: **3**
- DIRECT_CONDITION_IR_READY: **9**
- DIRECT_RELATION_OR_COMPOSITION_DEFERRED: **3**
- total Knowledge condition-IR-ready: **12**
- not condition-IR-ready despite row-local readiness: **14**
- Product conditions compiled: **0**
- execution unlocked: **0**

## The 11 dependency-effective underdetermined rows

These rows have no target-row blocker, but their required parent or ancestor condition still carries source uncertainty. They remain fail-closed. CA02-171 is the canonical regression case: CA02-171 -> CA02-170 -> CA02-169 propagates the open-valence uncertainty even though CA02-170 is row-locally clear.

## The 3 dependency IR-ready rows

CA05-420, CA07-639 and CA07-682 reuse exact parent condition scope through the explicit IR created by #508.

## The 9 direct IR-ready rows

CA02-181, CA03-228, CA05-411, CA05-417, CA05-419, CA05-433, CA07-638, CA07-681 and CA09-820 can now be serialized as Knowledge condition IR from already-approved canonical relation/member/source-local semantics. No new source meaning is added.

## The 3 direct rows still deferred

- **CA05-484**: internal alternatives are source-resolved, but generic `会` geometry is not.
- **CA06-582**: 文昌文曲 BOTH is source-local, but `见 + 同会` relation composition is not deterministic.
- **CA07-699**: 文昌文曲 BOTH is source-local, but generic `同会` geometry remains unspecified.

These rows are intentionally not forced into an executable geometry.

This census leaves canonical blocker counts unchanged and creates no Product execution permission.
