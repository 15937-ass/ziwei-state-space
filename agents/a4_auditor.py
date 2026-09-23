"""
A4 Red Team Auditor skeleton.

Checks:
- provenance
- schema completeness
- unsupported inference
- school mixing
- hidden contradictions
"""


def audit_rule(rule: dict) -> dict:
    issues = []

    if not rule.get("source"):
        issues.append("missing_source")

    if rule.get("epistemic_type") not in [
        "EXPLICIT",
        "INFERRED",
        "HYPOTHESIS",
        "IMPLEMENTATION"
    ]:
        issues.append("invalid_epistemic_type")

    return {
        "rule_id": rule.get("rule_id"),
        "issues": issues,
        "pass": len(issues) == 0
    }
