# WP04 transformation canonical split

Status: **SOURCE-CANONICAL SPLIT CREATED**

The 181 source-reviewed transformation closure rules are now represented losslessly in two source-canonical catalogs:

- `transformation_general_v0.1.csv`: 7 rules from the transformation general section;
- `transformation_star_specific_v0.1.csv`: 174 rules from the 40 star-specific source units.

The legacy `transformation_rules_v0.1.csv` (56 rules) is retained unchanged during reconciliation because it preserves earlier provenance from star/system chapters.

This split does **not** declare semantic equivalence between the legacy 56 and the dedicated-chapter 181. The reconciliation ledger remains authoritative for overlap/add/variant decisions.
