"""Capability-aware QuickRead evidence contract v0.1.

This module is a deterministic adapter, not a chart engine or LLM client. It
keeps executed runtime evidence, accepted source material, and model
supplementation in separate lanes so the latter cannot inflate project
capability coverage.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from enum import Enum
from typing import Any, Mapping, Sequence

from .canonical_chart_contract import validate_canonical_production_chart_snapshot


SCHEMA_VERSION = "0.1"
AVAILABLE = frozenset({"AVAILABLE", "PARTIAL"})
AVAILABILITY_VALUES = frozenset(
    {"AVAILABLE", "PARTIAL", "BLOCKED", "UNKNOWN", "NOT_AVAILABLE"}
)
SOURCE_ALLOWED_USES = frozenset(
    {"RETRIEVAL_ONLY", "SEMANTIC_ONLY", "CASE_SUPPORT_ONLY"}
)
ALL_ALLOWED_USES = SOURCE_ALLOWED_USES | frozenset(
    {"EXECUTABLE", "BLOCKED", "UNKNOWN"}
)
ACCEPTED_REVIEW_STATUSES = frozenset(
    {
        "ACCEPTED",
        "ACCEPTED_ON_MAIN",
        "APPROVED",
        "HUMAN_VERIFIED",
        "REVIEWED",
        "SOURCE_REVIEWED",
        "SOURCE_SPAN_VERIFIED",
    }
)
NAMESPACES = frozenset({"CANONICAL", "TEMPORAL", "CASE"})


def _text(value: Any, field: str) -> str:
    result = str(value or "").strip()
    if not result:
        raise ValueError(f"{field} is required")
    return result


def _enum_value(value: Any) -> str:
    if isinstance(value, Enum):
        return str(value.value)
    return str(value or "").strip().upper()


def _ratio(numerator: int, denominator: int) -> float:
    return round(numerator / denominator, 4) if denominator else 0.0


def _json_mapping(value: Mapping[str, Any] | None, field: str) -> dict[str, Any]:
    if value is None:
        return {}
    if not isinstance(value, Mapping):
        raise ValueError(f"{field} must be a mapping")
    try:
        copied = json.loads(
            json.dumps(dict(value), ensure_ascii=False, sort_keys=True)
        )
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{field} must contain JSON-compatible values") from exc
    if not isinstance(copied, dict):
        raise ValueError(f"{field} must serialize to an object")
    return copied


@dataclass(frozen=True)
class QuickReadScopeSlot:
    """One explicitly requested capability unit; the coverage denominator."""

    slot_id: str
    domain: str
    temporal_layer: str
    capability_kind: str
    required_namespaces: tuple[str, ...] = ("CANONICAL",)
    case_scope: str | None = None

    def __post_init__(self) -> None:
        for field_name in ("slot_id", "domain", "temporal_layer", "capability_kind"):
            object.__setattr__(self, field_name, _text(getattr(self, field_name), field_name))
        layer = self.temporal_layer.upper()
        object.__setattr__(self, "temporal_layer", layer)
        namespaces = tuple(_enum_value(item) for item in self.required_namespaces)
        if not namespaces or len(set(namespaces)) != len(namespaces):
            raise ValueError("required_namespaces must be non-empty and unique")
        if not set(namespaces).issubset(NAMESPACES):
            raise ValueError("required_namespaces contains an unsupported namespace")
        if layer != "NATAL" and "TEMPORAL" not in namespaces:
            raise ValueError("non-NATAL scope slots must require TEMPORAL evidence")
        case_scope = str(self.case_scope or "").strip() or None
        if "CASE" in namespaces and not case_scope:
            raise ValueError("CASE namespace requires an explicit case_scope")
        if case_scope and "CASE" not in namespaces:
            raise ValueError("case_scope requires CASE in required_namespaces")
        object.__setattr__(self, "case_scope", case_scope)
        kind = self.capability_kind.upper()
        if layer != "NATAL" and any(
            marker in kind for marker in ("RESPONSE", "MANIFESTATION")
        ) and "CANONICAL" not in namespaces:
            raise ValueError(
                "temporal response/manifestation slots must require CANONICAL and TEMPORAL evidence"
            )
        object.__setattr__(self, "required_namespaces", namespaces)

    def to_dict(self) -> dict[str, Any]:
        return {
            "slot_id": self.slot_id,
            "domain": self.domain,
            "temporal_layer": self.temporal_layer,
            "capability_kind": self.capability_kind,
            "required_namespaces": list(self.required_namespaces),
            "case_scope": self.case_scope,
        }


@dataclass(frozen=True)
class EvidenceSourceRef:
    """Auditable source pointer plus the namespace and allowed-use boundary."""

    source_id: str
    source_location: str
    review_status: str
    allowed_use: str
    namespace: str = "CANONICAL"
    time_layer: str = "NATAL"

    def __post_init__(self) -> None:
        for field_name in ("source_id", "source_location"):
            object.__setattr__(self, field_name, _text(getattr(self, field_name), field_name))
        for field_name in ("review_status", "allowed_use", "namespace"):
            value = _text(getattr(self, field_name), field_name)
            object.__setattr__(self, field_name, value.upper())
        object.__setattr__(self, "time_layer", str(self.time_layer or "").strip().upper())
        if self.allowed_use not in ALL_ALLOWED_USES:
            raise ValueError(f"unsupported allowed_use: {self.allowed_use}")
        if self.namespace not in NAMESPACES:
            raise ValueError(f"unsupported evidence namespace: {self.namespace}")
        if self.namespace == "TEMPORAL" and not self.time_layer:
            raise ValueError("TEMPORAL source references require time_layer")
        if self.namespace == "CASE" and self.allowed_use != "CASE_SUPPORT_ONLY":
            raise ValueError("CASE namespace requires CASE_SUPPORT_ONLY allowed_use")
        if self.allowed_use == "CASE_SUPPORT_ONLY" and self.namespace != "CASE":
            raise ValueError("CASE_SUPPORT_ONLY allowed_use requires CASE namespace")
        if self.review_status not in ACCEPTED_REVIEW_STATUSES:
            raise ValueError(
                f"source reference is not accepted/reviewed: {self.review_status}"
            )

    def identity(self) -> tuple[str, str, str, str, str, str]:
        return (
            self.source_id,
            self.source_location,
            self.review_status,
            self.allowed_use,
            self.namespace,
            self.time_layer,
        )

    def to_dict(self) -> dict[str, str]:
        return {
            "source_id": self.source_id,
            "source_location": self.source_location,
            "review_status": self.review_status,
            "allowed_use": self.allowed_use,
            "namespace": self.namespace,
            "time_layer": self.time_layer,
        }


@dataclass(frozen=True)
class CapabilityRecord:
    """Current per-slot capability snapshot supplied by accepted artifacts."""

    slot: QuickReadScopeSlot
    runtime_status: str = "NOT_AVAILABLE"
    source_status: str = "NOT_AVAILABLE"
    runtime_rule_ids: tuple[str, ...] = ()
    runtime_source_refs: tuple[EvidenceSourceRef, ...] = ()
    source_refs: tuple[EvidenceSourceRef, ...] = ()
    reason: str = ""

    def __post_init__(self) -> None:
        runtime_status = _enum_value(self.runtime_status)
        source_status = _enum_value(self.source_status)
        object.__setattr__(self, "runtime_status", runtime_status)
        object.__setattr__(self, "source_status", source_status)
        if runtime_status not in AVAILABILITY_VALUES:
            raise ValueError(f"unsupported runtime_status: {runtime_status}")
        if source_status not in AVAILABILITY_VALUES:
            raise ValueError(f"unsupported source_status: {source_status}")
        rule_ids = tuple(_text(item, "runtime_rule_id") for item in self.runtime_rule_ids)
        if len(set(rule_ids)) != len(rule_ids):
            raise ValueError("runtime_rule_ids must be unique")
        object.__setattr__(self, "runtime_rule_ids", rule_ids)
        runtime_refs = tuple(self.runtime_source_refs)
        if not all(isinstance(item, EvidenceSourceRef) for item in runtime_refs):
            raise ValueError("runtime_source_refs must contain EvidenceSourceRef values")
        object.__setattr__(self, "runtime_source_refs", runtime_refs)
        refs = tuple(self.source_refs)
        if not all(isinstance(item, EvidenceSourceRef) for item in refs):
            raise ValueError("source_refs must contain EvidenceSourceRef values")
        object.__setattr__(self, "source_refs", refs)
        object.__setattr__(self, "reason", str(self.reason or "").strip())
        if runtime_status in AVAILABLE:
            if not rule_ids:
                raise ValueError("available runtime capability requires runtime_rule_ids")
            if not runtime_refs:
                raise ValueError("available runtime capability requires runtime_source_refs")
            for ref in runtime_refs:
                if ref.allowed_use != "EXECUTABLE" or ref.namespace == "CASE":
                    raise ValueError(
                        "runtime_source_refs must be executable and non-case-scoped"
                    )
        if source_status in AVAILABLE:
            if not refs:
                raise ValueError("available source capability requires source_refs")
            for ref in refs:
                if ref.allowed_use not in SOURCE_ALLOWED_USES:
                    raise ValueError(
                        "available source capability may not expose non-retrieval source refs"
                    )

    def to_dict(self) -> dict[str, Any]:
        return {
            "slot": self.slot.to_dict(),
            "runtime_status": self.runtime_status,
            "source_status": self.source_status,
            "runtime_rule_ids": list(self.runtime_rule_ids),
            "runtime_source_refs": [item.to_dict() for item in self.runtime_source_refs],
            "source_refs": [item.to_dict() for item in self.source_refs],
            "reason": self.reason,
        }


@dataclass(frozen=True)
class CapabilityManifest:
    """Version-pinned snapshot; callers rebuild it from accepted current inputs."""

    main_sha: str
    knowledge_version: str
    runtime_version: str
    records: tuple[CapabilityRecord, ...]
    schema_version: str = SCHEMA_VERSION

    def __post_init__(self) -> None:
        if self.schema_version != SCHEMA_VERSION:
            raise ValueError(f"unsupported CapabilityManifest schema: {self.schema_version}")
        for field_name in ("main_sha", "knowledge_version", "runtime_version"):
            object.__setattr__(self, field_name, _text(getattr(self, field_name), field_name))
        records = tuple(self.records)
        if not all(isinstance(item, CapabilityRecord) for item in records):
            raise ValueError("records must contain CapabilityRecord values")
        ids = [item.slot.slot_id for item in records]
        if len(ids) != len(set(ids)):
            raise ValueError("CapabilityManifest contains duplicate slot IDs")
        object.__setattr__(self, "records", records)

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "main_sha": self.main_sha,
            "knowledge_version": self.knowledge_version,
            "runtime_version": self.runtime_version,
            "records": [item.to_dict() for item in self.records],
        }


@dataclass(frozen=True)
class QuickReadRequest:
    question: str
    target_id: str
    requested_slots: tuple[QuickReadScopeSlot, ...]
    mode: str = "HYBRID"
    min_chars: int = 120
    max_chars: int = 220

    def __post_init__(self) -> None:
        object.__setattr__(self, "question", _text(self.question, "question"))
        object.__setattr__(self, "target_id", _text(self.target_id, "target_id"))
        mode = _enum_value(self.mode)
        if mode not in {"HYBRID", "AUDIT", "SOURCE_FIRST"}:
            raise ValueError(f"unsupported QuickRead mode: {mode}")
        object.__setattr__(self, "mode", mode)
        slots = tuple(self.requested_slots)
        if not slots:
            raise ValueError("requested_slots must be non-empty")
        if not all(isinstance(item, QuickReadScopeSlot) for item in slots):
            raise ValueError("requested_slots must contain QuickReadScopeSlot values")
        ids = [item.slot_id for item in slots]
        if len(ids) != len(set(ids)):
            raise ValueError("requested_slots contains duplicate slot IDs")
        object.__setattr__(self, "requested_slots", slots)
        if self.min_chars < 1 or self.max_chars < self.min_chars or self.max_chars > 2000:
            raise ValueError("invalid output character range")

    def to_dict(self) -> dict[str, Any]:
        return {
            "question": self.question,
            "target_id": self.target_id,
            "mode": self.mode,
            "requested_slots": [item.to_dict() for item in self.requested_slots],
            "output_chars": {"min": self.min_chars, "max": self.max_chars},
        }


@dataclass(frozen=True)
class QuickReadEvidenceItem:
    """A single claim assigned to exactly one epistemic/evidence lane."""

    evidence_id: str
    slot_id: str
    lane: str
    claim: str
    rule_id: str | None = None
    source_refs: tuple[EvidenceSourceRef, ...] = ()
    epistemic_label: str = ""
    uncertainty: str = ""
    case_scope: str | None = None
    target_id: str | None = None
    execution_id: str | None = None
    runtime_version: str | None = None
    main_sha: str | None = None
    knowledge_version: str | None = None

    def __post_init__(self) -> None:
        for field_name in ("evidence_id", "slot_id", "claim"):
            object.__setattr__(self, field_name, _text(getattr(self, field_name), field_name))
        lane = _enum_value(self.lane)
        if lane not in {"RUNTIME", "SOURCE", "MODEL_SUPPLEMENT"}:
            raise ValueError(f"unsupported evidence lane: {lane}")
        object.__setattr__(self, "lane", lane)
        object.__setattr__(self, "epistemic_label", _enum_value(self.epistemic_label))
        object.__setattr__(self, "uncertainty", str(self.uncertainty or "").strip())
        object.__setattr__(self, "rule_id", str(self.rule_id or "").strip() or None)
        object.__setattr__(self, "case_scope", str(self.case_scope or "").strip() or None)
        refs = tuple(self.source_refs)
        if not all(isinstance(item, EvidenceSourceRef) for item in refs):
            raise ValueError("source_refs must contain EvidenceSourceRef values")
        object.__setattr__(self, "source_refs", refs)

        if lane == "RUNTIME":
            for name in ("target_id", "execution_id", "runtime_version", "main_sha", "knowledge_version"):
                _text(getattr(self, name), f"runtime evidence {name}")
            if not self.rule_id or not refs:
                raise ValueError("runtime evidence requires rule_id and source_refs")
            if self.epistemic_label not in {"CANONICAL_RUNTIME", "TEMPORAL_RUNTIME"}:
                raise ValueError("runtime evidence requires an explicit runtime epistemic label")
            if any(ref.allowed_use != "EXECUTABLE" for ref in refs):
                raise ValueError("runtime evidence refs must have EXECUTABLE allowed_use")
            if any(ref.namespace == "CASE" for ref in refs):
                raise ValueError("runtime evidence may not use case-only source refs")
            if self.case_scope:
                raise ValueError("runtime evidence may not carry case_scope")
        elif lane == "SOURCE":
            if any(getattr(self, name) is not None for name in ("target_id", "execution_id", "runtime_version", "main_sha", "knowledge_version")):
                raise ValueError("source-only evidence cannot claim runtime execution provenance")
            if not refs:
                raise ValueError("source evidence requires source_refs")
            if any(ref.allowed_use not in SOURCE_ALLOWED_USES for ref in refs):
                raise ValueError("source evidence contains a non-retrievable source ref")
            has_case_only = any(ref.allowed_use == "CASE_SUPPORT_ONLY" for ref in refs)
            if has_case_only:
                if self.epistemic_label != "CASE_SUPPORT_ONLY" or not self.case_scope:
                    raise ValueError("case-only evidence requires CASE_SUPPORT_ONLY label and case_scope")
                if any(ref.allowed_use != "CASE_SUPPORT_ONLY" for ref in refs):
                    raise ValueError("case-only evidence may not be mixed with general source refs")
            elif self.epistemic_label != "SOURCE_GROUNDED":
                raise ValueError("reviewed source evidence requires SOURCE_GROUNDED label")
            if self.case_scope and not has_case_only:
                raise ValueError("case_scope is only valid for CASE_SUPPORT_ONLY evidence")
        else:
            if any(getattr(self, name) is not None for name in ("target_id", "execution_id", "runtime_version", "main_sha", "knowledge_version")):
                raise ValueError("model supplements cannot claim runtime execution provenance")
            if self.rule_id or refs:
                raise ValueError("model supplements may not invent rule_id or source_refs")
            if self.epistemic_label != "MODEL_SUPPLEMENT":
                raise ValueError("model evidence must be labeled MODEL_SUPPLEMENT")
            if not self.uncertainty:
                raise ValueError("model supplements require an uncertainty note")
            if self.case_scope:
                raise ValueError("model supplements may not claim a source case scope")

    def to_dict(self) -> dict[str, Any]:
        return {
            "evidence_id": self.evidence_id,
            "slot_id": self.slot_id,
            "lane": self.lane,
            "claim": self.claim,
            "rule_id": self.rule_id,
            "source_refs": [item.to_dict() for item in self.source_refs],
            "epistemic_label": self.epistemic_label,
            "uncertainty": self.uncertainty,
            "case_scope": self.case_scope,
            "target_id": self.target_id,
            "execution_id": self.execution_id,
            "runtime_version": self.runtime_version,
            "main_sha": self.main_sha,
            "knowledge_version": self.knowledge_version,
        }


@dataclass(frozen=True)
class SlotCoverage:
    slot: QuickReadScopeSlot
    runtime_capability_status: str
    source_capability_status: str
    runtime_evidence_count: int
    source_evidence_count: int
    model_supplement_count: int

    @property
    def runtime_capable(self) -> bool:
        return self.runtime_capability_status in AVAILABLE

    @property
    def source_available(self) -> bool:
        return self.source_capability_status in AVAILABLE

    @property
    def has_runtime_evidence(self) -> bool:
        return self.runtime_evidence_count > 0

    @property
    def has_source_evidence(self) -> bool:
        return self.source_evidence_count > 0

    @property
    def has_model_supplement(self) -> bool:
        return self.model_supplement_count > 0

    @property
    def uncovered_by_runtime_and_source(self) -> bool:
        return not self.has_runtime_evidence and not self.has_source_evidence

    def to_dict(self) -> dict[str, Any]:
        return {
            "slot": self.slot.to_dict(),
            "runtime_capability_status": self.runtime_capability_status,
            "source_capability_status": self.source_capability_status,
            "runtime_capable": self.runtime_capable,
            "source_available": self.source_available,
            "runtime_evidence_count": self.runtime_evidence_count,
            "source_evidence_count": self.source_evidence_count,
            "model_supplement_count": self.model_supplement_count,
            "uncovered_by_runtime_and_source": self.uncovered_by_runtime_and_source,
        }


@dataclass(frozen=True)
class QuickReadCoverageReport:
    requested_slot_count: int
    runtime_capable_slot_count: int
    source_available_slot_count: int
    runtime_evidenced_slot_count: int
    source_evidenced_slot_count: int
    model_supplemented_slot_count: int
    uncovered_by_runtime_and_source_slot_count: int
    runtime_capability_ratio: float
    source_availability_ratio: float
    runtime_evidence_coverage_ratio: float
    source_evidence_coverage_ratio: float
    slot_reports: tuple[SlotCoverage, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "requested_slot_count": self.requested_slot_count,
            "runtime_capable_slot_count": self.runtime_capable_slot_count,
            "source_available_slot_count": self.source_available_slot_count,
            "runtime_evidenced_slot_count": self.runtime_evidenced_slot_count,
            "source_evidenced_slot_count": self.source_evidenced_slot_count,
            "model_supplemented_slot_count": self.model_supplemented_slot_count,
            "uncovered_by_runtime_and_source_slot_count": (
                self.uncovered_by_runtime_and_source_slot_count
            ),
            "runtime_capability_ratio": self.runtime_capability_ratio,
            "source_availability_ratio": self.source_availability_ratio,
            "runtime_evidence_coverage_ratio": self.runtime_evidence_coverage_ratio,
            "source_evidence_coverage_ratio": self.source_evidence_coverage_ratio,
            "slot_reports": [item.to_dict() for item in self.slot_reports],
            "interpretation": (
                "Ratios use only the explicitly requested slots as denominator. "
                "Model supplements do not increase runtime or source-backed coverage."
            ),
        }


def _slot_index(slots: Sequence[QuickReadScopeSlot]) -> dict[str, QuickReadScopeSlot]:
    return {slot.slot_id: slot for slot in slots}


def _record_index(manifest: CapabilityManifest) -> dict[str, CapabilityRecord]:
    return {record.slot.slot_id: record for record in manifest.records}


def _validate_required_namespaces(
    slot: QuickReadScopeSlot, refs: Sequence[EvidenceSourceRef]
) -> None:
    present = {ref.namespace for ref in refs}
    missing = set(slot.required_namespaces) - present
    if missing:
        raise ValueError(
            f"{slot.slot_id}: evidence missing required namespaces {sorted(missing)}"
        )
    temporal_refs = [ref for ref in refs if ref.namespace == "TEMPORAL"]
    mismatched_layers = [ref.time_layer for ref in temporal_refs if ref.time_layer != slot.temporal_layer]
    if mismatched_layers:
        raise ValueError(
            f"{slot.slot_id}: temporal source layer(s) {sorted(set(mismatched_layers))} "
            f"do not match requested layer {slot.temporal_layer}"
        )
    if "TEMPORAL" in slot.required_namespaces:
        if not temporal_refs:
            raise ValueError(
                f"{slot.slot_id}: evidence requires TEMPORAL source for "
                f"{slot.temporal_layer}"
            )


def _validate_item_against_manifest(
    item: QuickReadEvidenceItem,
    slot: QuickReadScopeSlot,
    record: CapabilityRecord | None,
    request: QuickReadRequest,
    manifest: CapabilityManifest,
) -> None:
    if item.lane == "MODEL_SUPPLEMENT":
        return
    if record is None:
        raise ValueError(f"{slot.slot_id}: non-model evidence has no capability record")
    if item.lane == "RUNTIME":
        if record.runtime_status not in AVAILABLE:
            raise ValueError(f"{slot.slot_id}: runtime evidence supplied while runtime is unavailable")
        if item.rule_id not in record.runtime_rule_ids:
            raise ValueError(f"{slot.slot_id}: rule_id is not listed in the capability manifest")
        if item.target_id != request.target_id:
            raise ValueError(f"{slot.slot_id}: runtime target_id does not match request")
        if item.execution_id is None or not item.execution_id.strip():
            raise ValueError(f"{slot.slot_id}: runtime execution_id is required")
        if item.main_sha != manifest.main_sha:
            raise ValueError(f"{slot.slot_id}: runtime main_sha does not match manifest")
        if item.knowledge_version != manifest.knowledge_version:
            raise ValueError(f"{slot.slot_id}: runtime knowledge_version does not match manifest")
        if item.runtime_version != manifest.runtime_version:
            raise ValueError(f"{slot.slot_id}: runtime_version does not match manifest")
        expected_label = "CANONICAL_RUNTIME" if slot.temporal_layer == "NATAL" else "TEMPORAL_RUNTIME"
        if item.epistemic_label != expected_label:
            raise ValueError(f"{slot.slot_id}: runtime epistemic label does not match requested layer")
        allowed_refs = {ref.identity() for ref in record.runtime_source_refs}
        if any(ref.identity() not in allowed_refs for ref in item.source_refs):
            raise ValueError(f"{slot.slot_id}: runtime source ref is absent from the capability manifest")
    else:
        if record.source_status not in AVAILABLE:
            raise ValueError(f"{slot.slot_id}: source evidence supplied while source is unavailable")
        allowed_refs = {ref.identity() for ref in record.source_refs}
        if any(ref.identity() not in allowed_refs for ref in item.source_refs):
            raise ValueError(f"{slot.slot_id}: source evidence ref is absent from the capability manifest")
        if any(ref.allowed_use == "CASE_SUPPORT_ONLY" for ref in item.source_refs):
            if item.case_scope != slot.case_scope:
                raise ValueError(f"{slot.slot_id}: case_scope does not match requested scope")
    _validate_required_namespaces(slot, item.source_refs)


def _included_lanes(mode: str) -> frozenset[str]:
    if mode == "AUDIT":
        return frozenset({"RUNTIME"})
    if mode == "SOURCE_FIRST":
        return frozenset({"RUNTIME", "SOURCE"})
    return frozenset({"RUNTIME", "SOURCE", "MODEL_SUPPLEMENT"})


def build_coverage_report(
    request: QuickReadRequest,
    manifest: CapabilityManifest,
    evidence_items: Sequence[QuickReadEvidenceItem],
    *,
    included_lanes: frozenset[str] | None = None,
) -> QuickReadCoverageReport:
    """Report capability availability and actual evidence separately."""

    lanes = _included_lanes(request.mode) if included_lanes is None else included_lanes
    requested = _slot_index(request.requested_slots)
    records = _record_index(manifest)
    runtime_counts = {slot_id: 0 for slot_id in requested}
    source_counts = {slot_id: 0 for slot_id in requested}
    model_counts = {slot_id: 0 for slot_id in requested}
    seen_ids: set[str] = set()

    for item in evidence_items:
        if not isinstance(item, QuickReadEvidenceItem):
            raise ValueError("evidence_items must contain QuickReadEvidenceItem values")
        if item.evidence_id in seen_ids:
            raise ValueError(f"duplicate evidence_id: {item.evidence_id}")
        seen_ids.add(item.evidence_id)
        slot = requested.get(item.slot_id)
        if slot is None:
            raise ValueError(f"evidence item is outside requested scope: {item.slot_id}")
        _validate_item_against_manifest(item, slot, records.get(item.slot_id), request, manifest)
        if item.lane not in lanes:
            continue
        if item.lane == "RUNTIME":
            runtime_counts[item.slot_id] += 1
        elif item.lane == "SOURCE":
            source_counts[item.slot_id] += 1
        else:
            model_counts[item.slot_id] += 1

    slot_reports: list[SlotCoverage] = []
    for slot in request.requested_slots:
        record = records.get(slot.slot_id)
        if record is not None and record.slot != slot:
            raise ValueError(f"{slot.slot_id}: request/manifest scope mismatch")
        slot_reports.append(
            SlotCoverage(
                slot=slot,
                runtime_capability_status=record.runtime_status if record else "UNKNOWN",
                source_capability_status=record.source_status if record else "UNKNOWN",
                runtime_evidence_count=runtime_counts[slot.slot_id],
                source_evidence_count=source_counts[slot.slot_id],
                model_supplement_count=model_counts[slot.slot_id],
            )
        )

    total = len(slot_reports)
    runtime_capable = sum(item.runtime_capable for item in slot_reports)
    source_available = sum(item.source_available for item in slot_reports)
    runtime_evidenced = sum(item.has_runtime_evidence for item in slot_reports)
    source_evidenced = sum(item.has_source_evidence for item in slot_reports)
    model_supplemented = sum(item.has_model_supplement for item in slot_reports)
    uncovered = sum(item.uncovered_by_runtime_and_source for item in slot_reports)
    return QuickReadCoverageReport(
        requested_slot_count=total,
        runtime_capable_slot_count=runtime_capable,
        source_available_slot_count=source_available,
        runtime_evidenced_slot_count=runtime_evidenced,
        source_evidenced_slot_count=source_evidenced,
        model_supplemented_slot_count=model_supplemented,
        uncovered_by_runtime_and_source_slot_count=uncovered,
        runtime_capability_ratio=_ratio(runtime_capable, total),
        source_availability_ratio=_ratio(source_available, total),
        runtime_evidence_coverage_ratio=_ratio(runtime_evidenced, total),
        source_evidence_coverage_ratio=_ratio(source_evidenced, total),
        slot_reports=tuple(slot_reports),
    )


def validate_model_supplements(
    request: QuickReadRequest,
    items: Sequence[QuickReadEvidenceItem],
) -> tuple[QuickReadEvidenceItem, ...]:
    """Validate LLM-returned supplements without promoting them to source truth."""

    requested_ids = {slot.slot_id for slot in request.requested_slots}
    seen: set[str] = set()
    validated: list[QuickReadEvidenceItem] = []
    for item in items:
        if item.lane != "MODEL_SUPPLEMENT":
            raise ValueError("model supplement validator accepts MODEL_SUPPLEMENT items only")
        if item.slot_id not in requested_ids:
            raise ValueError(f"model supplement is outside requested scope: {item.slot_id}")
        if item.evidence_id in seen:
            raise ValueError(f"duplicate model supplement evidence_id: {item.evidence_id}")
        seen.add(item.evidence_id)
        if not item.uncertainty or item.rule_id or item.source_refs:
            raise ValueError("model supplement violates non-canonical evidence contract")
        validated.append(item)
    return tuple(validated)




def _validate_chart_context(chart: Mapping[str, Any]) -> str:
    """Accept only a canonical production chart or a narrowly scoped case anchor."""
    if not chart:
        return "MISSING"
    if chart.get("chart_contract_id"):
        validation = validate_canonical_production_chart_snapshot(chart)
        if not validation.ok:
            raise ValueError(
                "QuickRead chart_context is not a canonical production chart: "
                + "; ".join(validation.errors)
            )
        return "CANONICAL_PRODUCTION"

    case_anchor_fields = (
        "fixture_id",
        "source_chart_span_ref",
        "target_domain",
        "target_palace",
        "target_branch",
        "target_main_stars",
        "target_anchor_status",
    )
    is_case_anchor = (
        chart.get("case_allowed_use") == "CASE_SUPPORT_ONLY"
        and chart.get("full_source_chart_equivalence_verified") is False
        and chart.get("target_anchor_status") == "UNIQUE_ANCHOR_MATCH_RECONFIRMED"
        and all(
            chart.get(field) not in (None, "", [])
            for field in case_anchor_fields
        )
    )
    if is_case_anchor:
        return "CASE_ANCHOR_ONLY"
    raise ValueError(
        "QuickRead chart_context must be a canonical production snapshot or an "
        "explicit CASE_SUPPORT_ONLY unique target anchor"
    )

def build_quickread_payload(
    request: QuickReadRequest,
    manifest: CapabilityManifest,
    evidence_items: Sequence[QuickReadEvidenceItem],
    *,
    chart_context: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Build one deterministic, scope-limited payload for a downstream verbalizer.

    This function never calls an LLM, reads repository state, or writes data.
    The caller must supply a manifest derived from accepted current inputs and
    normalized chart facts rather than raw birth records or personal identity.
    """

    if manifest.schema_version != SCHEMA_VERSION:
        raise ValueError("QuickRead requires a v0.1 capability manifest")
    chart = _json_mapping(chart_context, "chart_context")
    chart_context_status = _validate_chart_context(chart)
    requested = _slot_index(request.requested_slots)
    records = _record_index(manifest)
    seen_ids: set[str] = set()
    items = tuple(evidence_items)

    for slot_id, record in records.items():
        if slot_id in requested and record.slot != requested[slot_id]:
            raise ValueError(f"{slot_id}: request/manifest scope mismatch")

    for item in items:
        if not isinstance(item, QuickReadEvidenceItem):
            raise ValueError("evidence_items must contain QuickReadEvidenceItem values")
        if item.evidence_id in seen_ids:
            raise ValueError(f"duplicate evidence_id: {item.evidence_id}")
        seen_ids.add(item.evidence_id)
        slot = requested.get(item.slot_id)
        if slot is None:
            raise ValueError(f"evidence item is outside requested scope: {item.slot_id}")
        _validate_item_against_manifest(item, slot, records.get(item.slot_id), request, manifest)

    lanes = _included_lanes(request.mode)
    selected = tuple(item for item in items if item.lane in lanes)
    selected = tuple(
        sorted(
            selected,
            key=lambda item: (
                next(i for i, slot in enumerate(request.requested_slots) if slot.slot_id == item.slot_id),
                item.lane,
                item.evidence_id,
            ),
        )
    )
    report = build_coverage_report(
        request, manifest, selected, included_lanes=lanes
    )
    slot_reports = {item.slot.slot_id: item for item in report.slot_reports}

    model_supplement_slots: list[str] = []
    if request.mode == "HYBRID" and chart_context_status == "CANONICAL_PRODUCTION":
        for slot in request.requested_slots:
            coverage = slot_reports[slot.slot_id]
            if (
                coverage.uncovered_by_runtime_and_source
                and not coverage.has_model_supplement
            ):
                model_supplement_slots.append(slot.slot_id)

    gaps: list[dict[str, Any]] = []
    for slot in request.requested_slots:
        coverage = slot_reports[slot.slot_id]
        if coverage.uncovered_by_runtime_and_source:
            gaps.append(
                {
                    "slot": slot.to_dict(),
                    "runtime_status": coverage.runtime_capability_status,
                    "source_status": coverage.source_capability_status,
                    "model_supplement_requested": slot.slot_id in model_supplement_slots,
                    "model_supplement_present": coverage.has_model_supplement,
                }
            )

    payload = {
        "schema_version": SCHEMA_VERSION,
        "request": request.to_dict(),
        "versions": {
            "main_sha": manifest.main_sha,
            "knowledge_version": manifest.knowledge_version,
            "runtime_version": manifest.runtime_version,
        },
        "coverage": report.to_dict(),
        "evidence": {
            "runtime": [item.to_dict() for item in selected if item.lane == "RUNTIME"],
            "source": [item.to_dict() for item in selected if item.lane == "SOURCE"],
            "model_supplement": [
                item.to_dict() for item in selected if item.lane == "MODEL_SUPPLEMENT"
            ],
        },
        "gaps": gaps,
        "model_supplement_request": {
            "enabled": (
                request.mode == "HYBRID"
                and chart_context_status == "CANONICAL_PRODUCTION"
            ),
            "slot_ids": model_supplement_slots,
            "disabled_reason": (
                "NORMALIZED_CHART_CONTEXT_MISSING"
                if request.mode == "HYBRID" and chart_context_status == "MISSING"
                else (
                    "CASE_ANCHOR_ONLY_NOT_CANONICAL_CHART"
                    if request.mode == "HYBRID" and chart_context_status == "CASE_ANCHOR_ONLY"
                    else None
                )
            ),
        },
        "chart_context": chart if request.mode != "AUDIT" else {},
        "chart_context_status": chart_context_status,
        "verbalizer_instructions": [
            "Use only supplied RUNTIME evidence as claims produced by the accepted runtime.",
            "Use SOURCE evidence only within each source ref's allowed-use boundary.",
            "Never count MODEL_SUPPLEMENT as runtime or source-backed coverage.",
            "Never invent rule IDs, source IDs, source locations, or runtime execution.",
            "A non-NATAL slot requires matching TEMPORAL evidence for its target layer before a claim can be described as source/runtime-supported.",
            "Model-only additions must be returned as MODEL_SUPPLEMENT with an uncertainty note and without rule_id or source_refs.",
            "CASE_SUPPORT_ONLY evidence must remain limited to its named case and must not be generalized into a canonical rule.",
            "Do not turn natal tendencies or model-only interpretations into certain real-world event claims.",
            "Preserve unknowns, conflicts, and unsupported slots instead of silently filling them with canonical-sounding claims.",
            "Only CANONICAL_PRODUCTION chart context may support general chart interpretation or model supplementation.",
            "CASE_ANCHOR_ONLY context is restricted to its named case and target anchor; never generalize it into a full natal chart.",
            f"Write natural Chinese in approximately {request.min_chars}-{request.max_chars} characters unless the user requests otherwise.",
        ],
    }
    return json.loads(json.dumps(payload, ensure_ascii=False, sort_keys=True))
