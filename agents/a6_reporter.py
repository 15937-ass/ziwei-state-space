"""
A6 Research Report Agent skeleton.

Generates Chinese human-facing review reports from validated artifacts.
"""

from datetime import datetime


class A6Reporter:
    name = "A6-Report-Writer"

    def generate_gate_report(self, title: str, findings: list) -> str:
        lines = [
            f"# {title}",
            "",
            f"生成时间: {datetime.now().isoformat()}",
            "",
            "## 人工审核事项"
        ]
        lines.extend([f"- {item}" for item in findings])
        return "\n".join(lines)
