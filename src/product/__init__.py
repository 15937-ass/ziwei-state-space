"""Product-layer utilities.

These modules consume approved research artifacts but must not silently create
new domain theory.
"""

from .chart_diff import ChartDifference, compare_chart_snapshots, summarize_differences
from .evidence_package import ConfidenceBand, EvidenceItem, EvidencePackage
from .rule_runtime import (
    ActiveRuleGraph,
    ActiveRuleNode,
    CompilationReport,
    CompileDisposition,
    CompileIssue,
    RuleIR,
    RuleRuntime,
    RuntimeState,
    compile_rule_row,
    compile_rule_rows,
)

__all__ = [
    "ChartDifference",
    "compare_chart_snapshots",
    "summarize_differences",
    "ConfidenceBand",
    "EvidenceItem",
    "EvidencePackage",
    "ActiveRuleGraph",
    "ActiveRuleNode",
    "CompilationReport",
    "CompileDisposition",
    "CompileIssue",
    "RuleIR",
    "RuleRuntime",
    "RuntimeState",
    "compile_rule_row",
    "compile_rule_rows",
]
