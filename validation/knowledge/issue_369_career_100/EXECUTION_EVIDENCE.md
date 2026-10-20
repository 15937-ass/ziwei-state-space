# Issue #369 execution evidence

Execution context: OpenAI chat environment with GitHub connector.  
Canonical base commit: `ec3131f77571c8134cfa452bd4df4c199d79d717`.  
Draft PR: #371.

## Scope

- Selected canonical range after prior structured IDs: CA03-236 through CA04-342.
- Source rows rechecked: 100.
- Complete condition mappings: 30.
- Methodology/context records: 8.
- Blocked outcome mappings: 62.
- Production additions: 0.
- Unique structured records: 252 -> 352.
- Canonical source-reviewed Career count remains 888.

## Source review

Approved source: SRC-ZZ-003, printed pages 137-140 / PDF pages 69-70.  
Attachment SHA-256: `6bddb3cac2e4b4efcf265229cbda22904ab3394aeef832e338ee5939088e5c5c`.

The page images and parsed text were inspected in the OpenAI file environment. OCR wording was not silently corrected.

## Deterministic validation completed

A connector-side independent validation re-read the branch JSON and the canonical CA03/CA04 CSVs and checked:

- exactly 100 records;
- first/last IDs CA03-236 / CA04-342;
- every embedded `source_record` byte-for-byte matches the parsed canonical CSV record;
- disposition counts are 30 complete / 8 context / 62 blocked;
- every complete mapping uses only already-approved condition atom types;
- every non-complete mapping has `condition=null` and a blocker;
- every record remains `executable_registry_entry=false`;
- branch diff contains only the review JSON, Chinese audit, targeted test, and this evidence file.

Result: PASS.

## Validation still required before merge

The PR intentionally remains Draft. Full repository pytest, targeted pytest execution, governance validation, diff check, Node/P0 checks and any required regression suite have not yet been executed in a materialized Codex/OpenAI repository environment. They must pass before this PR is marked ready or merged.

GitHub Actions were not used.


## Critic / red-team pass

The initial producer pass was deliberately re-audited for over-compilation.

Corrections:
- CA03-277 was downgraded from complete to GROUP-blocked because the source uses the collective term “昌曲” without fixing a one-star/two-star quantifier.
- CA03-278 was downgraded from complete to RELATION-blocked because “左辅、右弼同会事业宫” cannot be rewritten as both stars physically co-located in P09.
- CA03-286 was downgraded from complete to methodology/context because teaching and singing are examples clarifying the “口舌” semantic, not direct profession predictions.
- “前格” records now preserve explicit inherited source-rule IDs.
- Source span records now preserve the parsed text of printed pages 137-140 after direct page review rather than summary-only placeholders.

A fresh independent connector-side check after these revisions re-read the canonical CA03/CA04 CSV rows and branch artifact and returned PASS for:
- 100/100 exact source-record equality;
- 30/8/62 disposition closure;
- approved atom types only;
- null condition for every non-complete mapping;
- no production registry entry;
- reviewed source spans present;
- branch scope limited to Knowledge artifact/audit/test/evidence/state.

Mandatory shell validation remains pending; this evidence does not substitute for pytest/governance commands.
