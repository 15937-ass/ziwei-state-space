"""Deterministic semantic aggregation for the PL2-E wealth report.

This layer groups already-active evidence into the multi-state dimensions
confirmed by the Wealth Palace closure audit. It does not score wealth, infer
net auspiciousness, or select additional rules.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable, Mapping

from .evidence_package import EvidencePackage


@dataclass(frozen=True)
class WealthSemanticFinding:
    rule_id: str
    section_id: str
    display_claim: str
    projection_domain: str
    projection_mode: str
    source_pointer: str
    matched_conditions: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class WealthSemanticSection:
    section_id: str
    label: str
    findings: tuple[WealthSemanticFinding, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "section_id": self.section_id,
            "label": self.label,
            "findings": [item.to_dict() for item in self.findings],
        }


@dataclass(frozen=True)
class SharedTriggerGroup:
    rule_ids: tuple[str, ...]
    matched_conditions: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class WealthStructureReport:
    report_type: str
    palace_id: str
    time_layer: str
    question: str
    confidence_band: str
    confidence_rationale: str
    coverage: Mapping[str, Any]
    sections: tuple[WealthSemanticSection, ...]
    shared_trigger_groups: tuple[SharedTriggerGroup, ...]
    conflicts: tuple[Mapping[str, Any], ...]
    limitations: tuple[str, ...]
    engine_version: str
    knowledge_version: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "report_type": self.report_type,
            "palace_id": self.palace_id,
            "time_layer": self.time_layer,
            "question": self.question,
            "confidence_band": self.confidence_band,
            "confidence_rationale": self.confidence_rationale,
            "coverage": dict(self.coverage),
            "sections": [section.to_dict() for section in self.sections],
            "shared_trigger_groups": [
                group.to_dict() for group in self.shared_trigger_groups
            ],
            "conflicts": [dict(item) for item in self.conflicts],
            "limitations": list(self.limitations),
            "engine_version": self.engine_version,
            "knowledge_version": self.knowledge_version,
        }


def load_wealth_semantic_registry(path: str | Path) -> dict[str, Any]:
    with Path(path).open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if data.get("schema_version") != "0.1":
        raise ValueError("wealth semantic registry schema_version must be 0.1")
    if data.get("palace_id") != "P05":
        raise ValueError("wealth semantic registry must target P05")
    sections = data.get("sections")
    rules = data.get("rules")
    if not isinstance(sections, list) or not sections:
        raise ValueError("wealth semantic registry requires sections")
    if not isinstance(rules, Mapping) or not rules:
        raise ValueError("wealth semantic registry requires rule mappings")

    seen_sections: set[str] = set()
    for section in sections:
        section_id = str(section.get("id", "")).strip()
        if not section_id or section_id in seen_sections:
            raise ValueError("section ids must be non-empty and unique")
        seen_sections.add(section_id)

    for rule_id, rule in rules.items():
        if str(rule.get("section", "")).strip() not in seen_sections:
            raise ValueError(f"{rule_id}: semantic section is not registered")
        if not str(rule.get("display_claim", "")).strip():
            raise ValueError(f"{rule_id}: display_claim is required")
    return data


def load_wealth_semantic_overlay(path: str | Path) -> dict[str, Any]:
    with Path(path).open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if data.get("schema_version") != "0.1":
        raise ValueError("wealth semantic overlay schema_version must be 0.1")
    if data.get("palace_id") != "P05":
        raise ValueError("wealth semantic overlay must target P05")
    rules = data.get("rules")
    if not isinstance(rules, Mapping) or not rules:
        raise ValueError("wealth semantic overlay requires rule mappings")

    sections = data.get("sections", [])
    if not isinstance(sections, list):
        raise ValueError("wealth semantic overlay sections must be a list")
    seen: set[str] = set()
    for section in sections:
        if not isinstance(section, Mapping):
            raise ValueError("wealth semantic overlay section must be a mapping")
        section_id = str(section.get("id", "")).strip()
        label = str(section.get("label", "")).strip()
        domains = section.get("domains")
        if not section_id or section_id in seen:
            raise ValueError("wealth semantic overlay section ids must be unique")
        if not label:
            raise ValueError(f"{section_id}: section label is required")
        if not isinstance(domains, list) or not all(str(x).strip() for x in domains):
            raise ValueError(f"{section_id}: section domains must be a non-empty list")
        seen.add(section_id)
    return data


def compose_wealth_semantic_registries(
    base: Mapping[str, Any],
    *overlays: Mapping[str, Any],
) -> dict[str, Any]:
    """Compose presentation mappings while preserving the PL2-E section ontology."""

    sections = base.get("sections")
    if not isinstance(sections, list) or not sections:
        raise ValueError("base wealth semantic registry requires sections")
    section_ids = {str(section.get("id", "")).strip() for section in sections}
    if "" in section_ids:
        raise ValueError("base wealth semantic registry has empty section id")

    combined = dict(base)
    combined_rules = dict(base.get("rules", {}))
    combined_sections = [dict(section) for section in sections]

    for overlay in overlays:
        if overlay.get("schema_version") != "0.1":
            raise ValueError("wealth semantic overlay schema_version must be 0.1")
        if overlay.get("palace_id") != base.get("palace_id"):
            raise ValueError("wealth semantic overlay palace_id mismatch")
        rules = overlay.get("rules")
        if not isinstance(rules, Mapping) or not rules:
            raise ValueError("wealth semantic overlay requires rule mappings")

        for section in overlay.get("sections", []):
            section_id = str(section.get("id", "")).strip()
            if not section_id or section_id in section_ids:
                raise ValueError(
                    f"duplicate or empty wealth semantic section: {section_id!r}"
                )
            label = str(section.get("label", "")).strip()
            domains = section.get("domains")
            if not label:
                raise ValueError(f"{section_id}: section label is required")
            if not isinstance(domains, list) or not domains:
                raise ValueError(f"{section_id}: section domains are required")
            combined_sections.append(dict(section))
            section_ids.add(section_id)

        overlap = set(combined_rules).intersection(rules)
        if overlap:
            raise ValueError(
                "duplicate wealth semantic rule across registries: "
                + ", ".join(sorted(overlap))
            )

        for rule_id, spec in rules.items():
            section_id = str(spec.get("section", "")).strip()
            if section_id not in section_ids:
                raise ValueError(f"{rule_id}: semantic section is not registered")
            if not str(spec.get("display_claim", "")).strip():
                raise ValueError(f"{rule_id}: display_claim is required")
            combined_rules[str(rule_id)] = dict(spec)

    combined["sections"] = combined_sections
    combined["rules"] = dict(sorted(combined_rules.items()))
    combined["knowledge_version"] = f"WEALTH_SEMANTIC_{len(combined_rules)}"
    return combined


def _projection_index(package: EvidencePackage) -> dict[str, Mapping[str, Any]]:
    out: dict[str, Mapping[str, Any]] = {}
    for projection in package.projections:
        rule_id = str(projection.get("rule_id", "")).strip()
        if not rule_id:
            raise ValueError("projection missing rule_id")
        if rule_id in out:
            raise ValueError(f"duplicate projection rule_id: {rule_id}")
        out[rule_id] = projection
    return out


def _shared_trigger_groups(
    findings: Iterable[WealthSemanticFinding],
) -> tuple[SharedTriggerGroup, ...]:
    by_trigger: dict[tuple[str, ...], list[str]] = {}
    for finding in findings:
        if not finding.matched_conditions:
            continue
        by_trigger.setdefault(finding.matched_conditions, []).append(finding.rule_id)

    groups = [
        SharedTriggerGroup(
            rule_ids=tuple(sorted(rule_ids)),
            matched_conditions=trigger,
        )
        for trigger, rule_ids in by_trigger.items()
        if len(rule_ids) > 1
    ]
    return tuple(
        sorted(groups, key=lambda item: (item.matched_conditions, item.rule_ids))
    )


def _limitations(package: EvidencePackage) -> tuple[str, ...]:
    items: list[str] = []
    pending = int(package.coverage.get("NORMALIZATION_PENDING", 0) or 0)
    holds = int(package.coverage.get("PATH_DEPENDENT_HOLD", 0) or 0)
    excluded = int(package.coverage.get("EXCLUDED", 0) or 0)

    if pending:
        items.append(f"仍有 {pending} 条规则尚未完成 executable normalization。")
    if holds:
        items.append(f"仍有 {holds} 条路径/时序规则等待 typed history integration。")
    if excluded:
        items.append(f"有 {excluded} 条记录不进入当前 executable set。")
    items.append("本报告不计算单一财富分数，也不合成为净吉凶。")
    items.append("当前结论仅覆盖已执行化规则，未覆盖的 canonical 规则不得按缺失处理。")
    return tuple(items)


def aggregate_wealth_evidence(
    package: EvidencePackage,
    registry: Mapping[str, Any],
) -> WealthStructureReport:
    """Aggregate active evidence without adding new rule semantics."""

    projection_by_id = _projection_index(package)
    registry_rules = registry["rules"]
    active_ids = {item.rule_id for item in package.active_rules}

    unknown = sorted(active_ids - set(registry_rules))
    if unknown:
        raise ValueError(
            "active rule missing from wealth semantic registry: " + ", ".join(unknown)
        )

    sections_meta = registry["sections"]
    section_findings: dict[str, list[WealthSemanticFinding]] = {
        str(section["id"]): [] for section in sections_meta
    }
    all_findings: list[WealthSemanticFinding] = []

    for evidence in sorted(package.active_rules, key=lambda item: item.rule_id):
        projection = projection_by_id.get(evidence.rule_id)
        if projection is None:
            raise ValueError(f"{evidence.rule_id}: active evidence missing projection")

        semantic = registry_rules[evidence.rule_id]
        section_id = str(semantic["section"])
        allowed_domains = set()
        for section in sections_meta:
            if section["id"] == section_id:
                allowed_domains = {str(x) for x in section.get("domains", [])}
                break

        domain = str(projection.get("projection_domain", "")).strip()
        if allowed_domains and domain not in allowed_domains:
            raise ValueError(
                f"{evidence.rule_id}: projection domain {domain!r} "
                f"does not fit semantic section {section_id!r}"
            )

        finding = WealthSemanticFinding(
            rule_id=evidence.rule_id,
            section_id=section_id,
            display_claim=str(semantic["display_claim"]),
            projection_domain=domain,
            projection_mode=str(projection.get("projection_mode", "")),
            source_pointer=str(projection.get("source_pointer", "")),
            matched_conditions=tuple(
                sorted(str(x) for x in projection.get("matched_conditions", []))
            ),
        )
        section_findings[section_id].append(finding)
        all_findings.append(finding)

    sections = tuple(
        WealthSemanticSection(
            section_id=str(section["id"]),
            label=str(section["label"]),
            findings=tuple(
                sorted(
                    section_findings[str(section["id"])],
                    key=lambda item: item.rule_id,
                )
            ),
        )
        for section in sections_meta
        if section_findings[str(section["id"])]
    )

    conflicts = tuple(
        {
            "conflict_id": item.conflict_id,
            "description": item.description,
            "rule_ids": list(item.rule_ids),
        }
        for item in package.conflicts
    )

    return WealthStructureReport(
        report_type=str(registry["report_type"]),
        palace_id=str(registry["palace_id"]),
        time_layer=str(registry["time_layer"]),
        question=package.question,
        confidence_band=package.confidence_band.value,
        confidence_rationale=package.confidence_rationale,
        coverage=dict(package.coverage),
        sections=sections,
        shared_trigger_groups=_shared_trigger_groups(all_findings),
        conflicts=conflicts,
        limitations=_limitations(package),
        engine_version=package.engine_version,
        knowledge_version=package.knowledge_version,
    )


def render_wealth_structure_report(report: WealthStructureReport) -> str:
    """Render a stable Chinese report without LLM generation."""

    lines = [
        "财帛结构报告（本命）",
        f"置信档位：{report.confidence_band}",
        f"置信原因：{report.confidence_rationale}",
        "",
    ]

    if not report.sections:
        lines.append("当前已执行化规则中，没有规则在本命盘上激活。")
    else:
        for section in report.sections:
            lines.append(f"【{section.label}】")
            for finding in section.findings:
                lines.append(
                    f"- {finding.display_claim} "
                    f"（{finding.rule_id}；{finding.source_pointer}）"
                )
            lines.append("")

    if report.shared_trigger_groups:
        lines.append("【共同触发】")
        for group in report.shared_trigger_groups:
            lines.append(
                "- 同一组已观测条件同时激活："
                + "、".join(group.rule_ids)
            )
        lines.append("")

    if report.conflicts:
        lines.append("【显式冲突】")
        for conflict in report.conflicts:
            lines.append(
                "- "
                + str(conflict["conflict_id"])
                + "："
                + "、".join(str(x) for x in conflict["rule_ids"])
            )
        lines.append("")

    lines.append("【覆盖与限制】")
    for item in report.limitations:
        lines.append(f"- {item}")

    return "\n".join(lines).rstrip() + "\n"
