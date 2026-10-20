# Career Ordinal Candidate Audit v0.1

Broad scan found **131** candidate sentences across 24 source spans.

- accepted: **118**
- excluded: **13**
- normalized constraints: **130**

Excluded reasons:
- BACKGROUND_HISTORICAL_COMPARISON_NOT_ZIWEI_CONSTRAINT: 1
- OCR_UNSAFE_COMPOUND_SENTENCE: 1
- VALUATION_WITHOUT_RELATIVE_ORDER: 5
- OUTCOME_TARGET_MAGNITUDE_NOT_RULE_STRENGTH: 1
- OCR_UNSAFE_DEGREE_WORDING: 1
- OCR_UNSAFE_TARGET_ENTITY: 1
- OCR_UNSAFE_CONDITION_SCOPE: 1
- VALUATION_WITHOUT_STABLE_COMPARATOR: 1
- LEXICAL_FALSE_POSITIVE_FIRST_SEAT: 1

排除项包括背景历史比较、OCR 不安全复合句/关键实体/条件、没有明确相对次序的“为贵”、把“第一把交椅”误识别成 rank，以及不能安全正规化的程度词。
