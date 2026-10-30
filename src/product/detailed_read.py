"""DetailedRead private-chat planning contract v0.1.

This module plans a full-chart, multi-turn reading on top of the accepted
QuickRead evidence contract. It does not calculate a chart, read GitHub,
call an LLM, or create a second rule/knowledge engine.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any, Callable, Mapping, Sequence

from .quickread_capability import (
    QuickReadEvidenceItem,
    QuickReadRequest,
    QuickReadScopeSlot,
)
from .quickread_main_reader import (
    DEFAULT_FIRST_PASS_SOURCE_ITEMS_PER_SLOT,
    DEFAULT_TIMEOUT_SECONDS,
    MainKnowledgeBundle,
    MainKnowledgeUnavailable,
    load_latest_main_knowledge,
)


SCHEMA_VERSION = "0.1"
SUPPORTED_MODES = frozenset({"HYBRID", "AUDIT", "SOURCE_FIRST"})
SUPPORTED_TEMPORAL_LAYERS = frozenset({"DECADE", "YEAR"})

# The twelve palace domains are the backend inspection surface. User-facing
# sections below deliberately synthesize them by life theme instead of
# mechanically reciting palace-by-palace output.
NATAL_DOMAIN_ORDER: tuple[str, ...] = (
    "life",
    "siblings",
    "relationship",
    "children",
    "wealth",
    "health",
    "migration",
    "friends",
    "career",
    "property",
    "fortune",
    "parents",
)

DOMAIN_TITLES: dict[str, str] = {
    "life": "命与总体格局",
    "siblings": "同辈与手足",
    "relationship": "感情与亲密关系",
    "children": "子女、晚辈与门生",
    "wealth": "财富与资源",
    "health": "健康与身心倾向",
    "migration": "迁移与外部环境",
    "friends": "人际与合作网络",
    "career": "事业与工作方式",
    "property": "田宅、居住与家庭资产",
    "fortune": "精神、福德与内在状态",
    "parents": "父母、长辈与代际关系",
}


@dataclass(frozen=True)
class DetailedReadSection:
    section_id: str
    title: str
    domains: tuple[str, ...]
    guidance: str
    required: bool = True

    def __post_init__(self) -> None:
        if not self.section_id.strip() or not self.title.strip():
            raise ValueError("section_id and title are required")
        domains = tuple(str(item).strip().lower() for item in self.domains)
        if not domains or len(domains) != len(set(domains)):
            raise ValueError("section domains must be non-empty and unique")
        unknown = set(domains) - set(NATAL_DOMAIN_ORDER)
        if unknown:
            raise ValueError(f"unknown DetailedRead domains: {sorted(unknown)}")
        object.__setattr__(self, "domains", domains)
        object.__setattr__(self, "guidance", str(self.guidance or "").strip())

    def to_dict(self) -> dict[str, Any]:
        return {
            "section_id": self.section_id,
            "title": self.title,
            "domains": list(self.domains),
            "guidance": self.guidance,
            "required": self.required,
        }


DEFAULT_SECTIONS: tuple[DetailedReadSection, ...] = (
    DetailedReadSection(
        "overview",
        "全盘总论",
        ("life", "fortune", "career", "migration"),
        "先给整盘主线、优势、主要矛盾与人生驱动力，不按宫位逐条复述。",
    ),
    DetailedReadSection(
        "disposition",
        "性格、精神与行为方式",
        ("life", "fortune"),
        "综合外在行为、内在需求、决策方式、压力反应与边界感。",
    ),
    DetailedReadSection(
        "career",
        "学业、事业与工作方式",
        ("career", "life", "migration", "fortune"),
        "解释适合的工作方式、发展动力、环境要求与主要阻力；不把事业宫单点等同职业成败。",
    ),
    DetailedReadSection(
        "wealth",
        "财富与资源模式",
        ("wealth", "career", "property"),
        "区分得财、资源流动、管理与积累，不把财富结构直接等同事业地位。",
    ),
    DetailedReadSection(
        "relationship",
        "感情与亲密关系",
        ("relationship", "life", "fortune", "migration"),
        "讲关系模式、择偶倾向、互动矛盾与适配方式；原局倾向不等于具体婚恋事件已经发生。",
    ),
    DetailedReadSection(
        "family",
        "家庭与代际关系",
        ("parents", "siblings", "children", "property"),
        "覆盖父母、手足、子女/晚辈与家庭环境；具体人数、伤亡、婚育事件不得由传统案例直接确定化。",
    ),
    DetailedReadSection(
        "social",
        "人际、合作与社会关系",
        ("friends", "siblings", "career"),
        "区分同辈朋友、合作网络、职场协作和亲近晚辈，不把不同宫位关系对象混成一类。",
    ),
    DetailedReadSection(
        "migration",
        "迁移、外部环境与发展",
        ("migration", "life", "career"),
        "区分移动/外部机会与移动后的吉凶，不把动象直接写成必然外地发财或定居。",
    ),
    DetailedReadSection(
        "health",
        "健康与身心倾向",
        ("health", "life", "fortune"),
        "只谈来源支持的体质/压力/生活倾向；不得给医学诊断、疾病确定性、治疗或预后结论。",
    ),
)


CROSS_DOMAIN_CHECKS: tuple[dict[str, Any], ...] = (
    {
        "check_id": "career_wealth",
        "domains": ("career", "wealth", "life", "migration"),
        "instruction": "事业发展、赚钱方式、资源积累与外部机会要互相校验；不得把其中一项自动推出另外三项。",
    },
    {
        "check_id": "relationship_inner_state",
        "domains": ("relationship", "life", "fortune", "migration"),
        "instruction": "关系倾向需与个体行为和内在需求一致；冲突时保留条件，不强行压成单一结论。",
    },
    {
        "check_id": "family_boundaries",
        "domains": ("parents", "siblings", "children", "property"),
        "instruction": "家庭成员、同辈、晚辈与居住资产语义分开；传统人数/具体事件案例不得泛化。",
    },
    {
        "check_id": "social_boundaries",
        "domains": ("friends", "siblings", "career", "children"),
        "instruction": "朋友、同辈、合作伙伴、普通下属与亲自提拔晚辈应按 accepted palace/domain 边界区分。",
    },
    {
        "check_id": "mobility_outcome",
        "domains": ("migration", "life", "career", "wealth"),
        "instruction": "移动、外部环境、事业与财富结果分开判断；移动信号本身不是结果。",
    },
    {
        "check_id": "health_caution",
        "domains": ("health", "life", "fortune"),
        "instruction": "健康章节必须保持倾向性和不确定性，不得把命理材料改写为医学诊断或具体疾病必然发生。",
    },
)


DELIVERY_STAGES: tuple[dict[str, Any], ...] = (
    {
        "stage_id": "stage_1_overview",
        "section_ids": ("overview", "disposition"),
        "purpose": "先建立整盘主线与人格/精神底色。",
    },
    {
        "stage_id": "stage_2_work_resources",
        "section_ids": ("career", "wealth"),
        "purpose": "展开学业/事业、工作方式与财富资源。",
    },
    {
        "stage_id": "stage_3_relationships",
        "section_ids": ("relationship", "family", "social"),
        "purpose": "展开亲密关系、家庭代际和社会合作。",
    },
    {
        "stage_id": "stage_4_environment_health_time",
        "section_ids": ("migration", "health"),
        "purpose": "展开外部环境、迁移与身心倾向；显式时间问题在此追加 temporal synthesis。",
    },
    {
        "stage_id": "stage_5_synthesis",
        "section_ids": (),
        "purpose": "收束为 3–5 条最强整合主线，并接受用户选择继续深挖。",
    },
)


VERBALIZER_INSTRUCTIONS: tuple[str, ...] = (
    "DetailedRead is a full inspection, not a promise of strong conclusions in every topic.",
    "Organize the user-facing reading by life themes, not as a mechanical twelve-palace recital.",
    "Use only supplied RUNTIME/SOURCE evidence as project-grounded support; MODEL_SUPPLEMENT remains explicitly non-canonical.",
    "If a section has weak or no accepted support, say so briefly or keep it short instead of inventing filler.",
    "Preserve conflicts, prerequisites, exceptions and uncertainty across domains before synthesizing.",
    "Do not convert natal tendencies into proof that a concrete event happened.",
    "Specific decade/year claims require matching accepted TEMPORAL evidence for that layer.",
    "Health content is non-diagnostic; child counts, death/injury, marriage timing and other concrete family events require explicit supported evidence and must not be forced from case-only material.",
    "Hide rule IDs, source paths and internal debug details in ordinary private-chat output unless the user asks for evidence.",
    "Prefer multi-turn delivery: overview/disposition, career/wealth, relationship/family/social, migration/health/time, then 3–5 strongest integrated themes.",
)


@dataclass(frozen=True)
class DetailedReadPlan:
    question: str
    target_id: str
    mode: str
    natal_slots: tuple[QuickReadScopeSlot, ...]
    temporal_slots: tuple[QuickReadScopeSlot, ...]
    sections: tuple[DetailedReadSection, ...] = DEFAULT_SECTIONS

    def __post_init__(self) -> None:
        question = str(self.question or "").strip()
        target_id = str(self.target_id or "").strip()
        if not question or not target_id:
            raise ValueError("question and target_id are required")
        mode = str(self.mode or "").strip().upper()
        if mode not in SUPPORTED_MODES:
            raise ValueError(f"unsupported DetailedRead mode: {mode}")
        natal = tuple(self.natal_slots)
        temporal = tuple(self.temporal_slots)
        if len(natal) != 12:
            raise ValueError("DetailedRead full plan must contain exactly 12 NATAL slots")
        if {slot.domain for slot in natal} != set(NATAL_DOMAIN_ORDER):
            raise ValueError("DetailedRead NATAL slots must cover all twelve palace domains")
        if any(slot.temporal_layer != "NATAL" for slot in natal):
            raise ValueError("natal_slots may contain only NATAL slots")
        all_ids = [slot.slot_id for slot in (*natal, *temporal)]
        if len(all_ids) != len(set(all_ids)):
            raise ValueError("DetailedRead slot IDs must be unique")
        if any(slot.temporal_layer == "NATAL" for slot in temporal):
            raise ValueError("temporal_slots may not contain NATAL slots")
        if any(slot.domain not in NATAL_DOMAIN_ORDER for slot in temporal):
            raise ValueError("temporal_slots must use a DetailedRead palace domain")
        if any(slot.temporal_layer not in SUPPORTED_TEMPORAL_LAYERS for slot in temporal):
            raise ValueError("temporal_slots contain an unsupported time layer")
        sections = tuple(self.sections)
        if not sections or not all(isinstance(item, DetailedReadSection) for item in sections):
            raise ValueError("sections must contain DetailedReadSection values")
        section_ids = [item.section_id for item in sections]
        if len(section_ids) != len(set(section_ids)):
            raise ValueError("DetailedRead section IDs must be unique")
        covered_domains = {domain for section in sections for domain in section.domains}
        if covered_domains != set(NATAL_DOMAIN_ORDER):
            raise ValueError("DetailedRead sections must cover all twelve palace domains")
        object.__setattr__(self, "question", question)
        object.__setattr__(self, "target_id", target_id)
        object.__setattr__(self, "mode", mode)
        object.__setattr__(self, "natal_slots", natal)
        object.__setattr__(self, "temporal_slots", temporal)
        object.__setattr__(self, "sections", sections)

    @property
    def retrieval_slots(self) -> tuple[QuickReadScopeSlot, ...]:
        return (*self.natal_slots, *self.temporal_slots)

    def retrieval_batches(self) -> tuple[dict[str, Any], ...]:
        """Return staged, deduplicated retrieval work for private-chat delivery."""

        section_by_id = {item.section_id: item for item in self.sections}
        natal_by_domain = {item.domain: item for item in self.natal_slots}
        seen_slot_ids: set[str] = set()
        batches: list[dict[str, Any]] = []
        for stage in DELIVERY_STAGES:
            slot_ids: list[str] = []
            for section_id in stage["section_ids"]:
                section = section_by_id.get(section_id)
                if section is None:
                    raise ValueError(
                        f"delivery stage references an unknown section: {section_id}"
                    )
                for domain in section.domains:
                    slot_id = natal_by_domain[domain].slot_id
                    if slot_id not in seen_slot_ids:
                        seen_slot_ids.add(slot_id)
                        slot_ids.append(slot_id)
            if stage["stage_id"] == "stage_4_environment_health_time":
                for slot in self.temporal_slots:
                    if slot.slot_id not in seen_slot_ids:
                        seen_slot_ids.add(slot.slot_id)
                        slot_ids.append(slot.slot_id)
            if slot_ids:
                batches.append(
                    {
                        "stage_id": stage["stage_id"],
                        "slot_ids": tuple(slot_ids),
                    }
                )

        expected = {slot.slot_id for slot in self.retrieval_slots}
        if seen_slot_ids != expected:
            missing = sorted(expected - seen_slot_ids)
            raise ValueError(f"DetailedRead retrieval schedule missed slots: {missing}")
        return tuple(batches)

    def request_for_slot(
        self,
        slot_id: str,
        *,
        min_chars: int = 240,
        max_chars: int = 900,
    ) -> QuickReadRequest:
        slot = next((item for item in self.retrieval_slots if item.slot_id == slot_id), None)
        if slot is None:
            raise ValueError(f"slot is not in this DetailedRead plan: {slot_id}")
        return QuickReadRequest(
            question=f"{self.question}｜详批取证：{DOMAIN_TITLES[slot.domain]}",
            target_id=self.target_id,
            requested_slots=(slot,),
            mode=self.mode,
            min_chars=min_chars,
            max_chars=max_chars,
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": SCHEMA_VERSION,
            "reading_mode": "DETAILED_READ",
            "question": self.question,
            "target_id": self.target_id,
            "mode": self.mode,
            "natal_slots": [item.to_dict() for item in self.natal_slots],
            "temporal_slots": [item.to_dict() for item in self.temporal_slots],
            "sections": [item.to_dict() for item in self.sections],
            "cross_domain_checks": [
                {
                    "check_id": item["check_id"],
                    "domains": list(item["domains"]),
                    "instruction": item["instruction"],
                }
                for item in CROSS_DOMAIN_CHECKS
            ],
            "verbalizer_instructions": list(VERBALIZER_INSTRUCTIONS),
            "retrieval_batches": [
                {
                    "stage_id": item["stage_id"],
                    "slot_ids": list(item["slot_ids"]),
                }
                for item in self.retrieval_batches()
            ],
            "delivery": {
                "multi_turn_preferred": True,
                "stages": [
                    {
                        "stage_id": item["stage_id"],
                        "section_ids": list(item["section_ids"]),
                        "purpose": item["purpose"],
                    }
                    for item in DELIVERY_STAGES
                ],
                "final_summary_theme_count": {"min": 3, "max": 5},
                "mechanical_twelve_palace_output": False,
            },
        }


def _slot(domain: str, layer: str) -> QuickReadScopeSlot:
    layer = layer.upper()
    namespaces = ("CANONICAL",) if layer == "NATAL" else ("CANONICAL", "TEMPORAL")
    kind = "NATAL_INTERPRETATION" if layer == "NATAL" else "TEMPORAL_RESPONSE"
    return QuickReadScopeSlot(
        slot_id=f"{domain}_{layer.lower()}",
        domain=domain,
        temporal_layer=layer,
        capability_kind=kind,
        required_namespaces=namespaces,
    )


def build_detailed_read_plan(
    question: str,
    target_id: str,
    *,
    mode: str = "HYBRID",
    temporal_layers: Sequence[str] = (),
    temporal_domains: Sequence[str] | None = None,
) -> DetailedReadPlan:
    """Build a full-chart plan while keeping retrieval atomic and bounded."""

    normalized_layers = tuple(str(item).strip().upper() for item in temporal_layers)
    if len(normalized_layers) != len(set(normalized_layers)):
        raise ValueError("temporal_layers must be unique")
    unsupported_layers = set(normalized_layers) - SUPPORTED_TEMPORAL_LAYERS
    if unsupported_layers:
        raise ValueError(f"unsupported DetailedRead temporal layers: {sorted(unsupported_layers)}")

    if temporal_domains is None:
        domains = NATAL_DOMAIN_ORDER if normalized_layers else ()
    else:
        domains = tuple(str(item).strip().lower() for item in temporal_domains)
        if len(domains) != len(set(domains)):
            raise ValueError("temporal_domains must be unique")
        unknown = set(domains) - set(NATAL_DOMAIN_ORDER)
        if unknown:
            raise ValueError(f"unknown temporal domains: {sorted(unknown)}")
        if domains and not normalized_layers:
            raise ValueError("temporal_domains requires at least one temporal layer")

    natal_slots = tuple(_slot(domain, "NATAL") for domain in NATAL_DOMAIN_ORDER)
    temporal_slots = tuple(
        _slot(domain, layer)
        for layer in normalized_layers
        for domain in domains
    )
    return DetailedReadPlan(
        question=question,
        target_id=target_id,
        mode=mode,
        natal_slots=natal_slots,
        temporal_slots=temporal_slots,
    )


def continuation_for_detailed_slot(
    previous_continuation: Mapping[str, Any] | None,
    slot_id: str,
) -> dict[str, Any] | None:
    """Reuse already-seen evidence for a slot when upgrading from QuickRead.

    The helper never fabricates continuation for a new slot. New DetailedRead
    slots begin with a fresh first pass. If the previous QuickRead scope
    included this slot, the main pin and accumulated seen evidence are retained
    while the request scope is narrowed to the atomic slot.
    """

    if previous_continuation is None:
        return None
    if not isinstance(previous_continuation, Mapping):
        raise ValueError("previous_continuation must be a mapping")
    main_sha = str(previous_continuation.get("main_sha", "")).strip()
    if not re.fullmatch(r"[0-9a-f]{40}", main_sha):
        raise ValueError("previous_continuation.main_sha must be a 40-character Git SHA")
    requested = previous_continuation.get("requested_slot_ids")
    seen = previous_continuation.get("seen_evidence_ids")
    if (
        not isinstance(requested, list)
        or not all(isinstance(item, str) and item.strip() for item in requested)
        or len(requested) != len(set(requested))
    ):
        raise ValueError("previous_continuation.requested_slot_ids must be a unique string list")
    if (
        not isinstance(seen, list)
        or not all(isinstance(item, str) and item.strip() for item in seen)
        or len(seen) != len(set(seen))
    ):
        raise ValueError("previous_continuation.seen_evidence_ids must be a unique string list")
    if slot_id not in requested:
        return None
    return {
        "main_sha": main_sha,
        "requested_slot_ids": [slot_id],
        "seen_evidence_ids": list(seen),
    }

@dataclass
class DetailedReadSession:
    """Session-wide orchestration over the accepted QuickRead reader.

    A session pins every independent atomic-slot read to one accepted main SHA.
    It does not calculate a chart, execute runtime rules, call an LLM, or turn
    source-only material into executable evidence.
    """

    plan: DetailedReadPlan
    loader: Callable[..., MainKnowledgeBundle] = load_latest_main_knowledge
    previous_quickread_continuation: Mapping[str, Any] | None = None
    previous_quickread_target_id: str | None = None
    main_sha: str | None = None
    completed_stage_ids: list[str] = field(default_factory=list)
    slot_batches: dict[str, list[MainKnowledgeBundle]] = field(default_factory=dict)
    model_supplement_items: dict[str, QuickReadEvidenceItem] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not isinstance(self.plan, DetailedReadPlan):
            raise ValueError("plan must be a DetailedReadPlan")
        if self.main_sha is not None:
            self.main_sha = str(self.main_sha).strip()
            if not re.fullmatch(r"[0-9a-f]{40}", self.main_sha):
                raise ValueError("main_sha must be a 40-character Git SHA")
        if self.previous_quickread_continuation is not None:
            if not isinstance(self.previous_quickread_continuation, Mapping):
                raise ValueError("previous_quickread_continuation must be a mapping")
            if self.previous_quickread_target_id != self.plan.target_id:
                raise ValueError(
                    "QuickRead-to-DetailedRead continuation must keep the same chart target_id"
                )
            cursor_sha = str(
                self.previous_quickread_continuation.get("main_sha", "")
            ).strip()
            if not re.fullmatch(r"[0-9a-f]{40}", cursor_sha):
                raise ValueError(
                    "previous_quickread_continuation.main_sha must be a 40-character Git SHA"
                )
            if self.main_sha is not None and self.main_sha != cursor_sha:
                raise ValueError(
                    "main_sha does not match the previous QuickRead snapshot"
                )
            self.main_sha = cursor_sha
        elif self.previous_quickread_target_id is not None:
            raise ValueError(
                "previous_quickread_target_id requires a previous QuickRead continuation"
            )

    def _slot(self, slot_id: str) -> QuickReadScopeSlot:
        slot = next(
            (item for item in self.plan.retrieval_slots if item.slot_id == slot_id),
            None,
        )
        if slot is None:
            raise ValueError(f"slot is not in this DetailedRead plan: {slot_id}")
        return slot

    def _load_slot_bundle(
        self,
        slot_id: str,
        *,
        continuation: Mapping[str, Any] | None,
        source_items_per_slot: int,
        fetch_bytes: Callable[[str, float, int], bytes] | None,
        timeout_seconds: float,
        repository_root: str | None,
    ) -> MainKnowledgeBundle:
        request = self.plan.request_for_slot(slot_id)
        kwargs: dict[str, Any] = {
            "source_items_per_slot": source_items_per_slot,
            "continuation": continuation,
            "expected_main_sha": self.main_sha,
            "timeout_seconds": timeout_seconds,
        }
        if fetch_bytes is not None:
            kwargs["fetch_bytes"] = fetch_bytes
        if repository_root is not None:
            kwargs["repository_root"] = repository_root

        bundle = self.loader(request, **kwargs)
        if not isinstance(bundle, MainKnowledgeBundle):
            raise MainKnowledgeUnavailable(
                "DetailedRead loader did not return a verified MainKnowledgeBundle"
            )
        if bundle.request.target_id != self.plan.target_id:
            raise MainKnowledgeUnavailable(
                "DetailedRead loader returned evidence for a different chart target"
            )
        if (
            len(bundle.request.requested_slots) != 1
            or bundle.request.requested_slots[0].slot_id != slot_id
        ):
            raise MainKnowledgeUnavailable(
                "DetailedRead loader returned evidence outside the requested atomic slot"
            )
        if (
            len(bundle.manifest.records) != 1
            or bundle.manifest.records[0].slot.slot_id != slot_id
        ):
            raise MainKnowledgeUnavailable(
                "DetailedRead capability manifest does not match the requested atomic slot"
            )
        try:
            bundle.build_payload()
        except (TypeError, ValueError) as exc:
            raise MainKnowledgeUnavailable(
                "DetailedRead bundle failed the accepted QuickRead evidence contract"
            ) from exc

        resolved_sha = bundle.manifest.main_sha
        if not re.fullmatch(r"[0-9a-f]{40}", resolved_sha):
            raise MainKnowledgeUnavailable(
                "DetailedRead loader returned an invalid main snapshot SHA"
            )
        if self.main_sha is None:
            self.main_sha = resolved_sha
        elif resolved_sha != self.main_sha:
            raise MainKnowledgeUnavailable(
                "DetailedRead session rejected mixed main snapshots; restart the full session"
            )
        if bundle.reader_report.get("main_sha") != self.main_sha:
            raise MainKnowledgeUnavailable(
                "DetailedRead reader report does not match the pinned main snapshot"
            )

        cursor = bundle.reader_report.get("continuation")
        if not isinstance(cursor, Mapping):
            raise MainKnowledgeUnavailable(
                "DetailedRead reader report is missing its continuation cursor"
            )
        if cursor.get("main_sha") != self.main_sha:
            raise MainKnowledgeUnavailable(
                "DetailedRead continuation cursor changed the session main snapshot"
            )
        requested_ids = cursor.get("requested_slot_ids")
        if requested_ids != [slot_id]:
            raise MainKnowledgeUnavailable(
                "DetailedRead continuation cursor does not match the atomic slot"
            )
        if any(item.slot_id != slot_id for item in bundle.evidence_items):
            raise MainKnowledgeUnavailable(
                "DetailedRead evidence escaped its requested atomic slot"
            )
        return bundle

    def run_stage(
        self,
        stage_id: str,
        *,
        source_items_per_slot: int = DEFAULT_FIRST_PASS_SOURCE_ITEMS_PER_SLOT,
        fetch_bytes: Callable[[str, float, int], bytes] | None = None,
        timeout_seconds: float = DEFAULT_TIMEOUT_SECONDS,
        repository_root: str | None = None,
    ) -> dict[str, Any]:
        """Read the first pass for every not-yet-read slot in one delivery stage."""

        batch = next(
            (
                item
                for item in self.plan.retrieval_batches()
                if item["stage_id"] == stage_id
            ),
            None,
        )
        if batch is None:
            raise ValueError(f"unknown DetailedRead stage: {stage_id}")
        if stage_id in self.completed_stage_ids:
            return self.stage_report(stage_id)

        for slot_id in batch["slot_ids"]:
            if self.slot_batches.get(slot_id):
                continue
            cursor = (
                continuation_for_detailed_slot(
                    self.previous_quickread_continuation, slot_id
                )
                if self.previous_quickread_continuation is not None
                else None
            )
            bundle = self._load_slot_bundle(
                slot_id,
                continuation=cursor,
                source_items_per_slot=source_items_per_slot,
                fetch_bytes=fetch_bytes,
                timeout_seconds=timeout_seconds,
                repository_root=repository_root,
            )
            self.slot_batches.setdefault(slot_id, []).append(bundle)

        self.completed_stage_ids.append(stage_id)
        return self.stage_report(stage_id)

    def run_all_stages(
        self,
        *,
        source_items_per_slot: int = DEFAULT_FIRST_PASS_SOURCE_ITEMS_PER_SLOT,
        fetch_bytes: Callable[[str, float, int], bytes] | None = None,
        timeout_seconds: float = DEFAULT_TIMEOUT_SECONDS,
        repository_root: str | None = None,
    ) -> dict[str, Any]:
        """Complete the scheduled first-pass inspection for every planned domain."""

        for batch in self.plan.retrieval_batches():
            self.run_stage(
                batch["stage_id"],
                source_items_per_slot=source_items_per_slot,
                fetch_bytes=fetch_bytes,
                timeout_seconds=timeout_seconds,
                repository_root=repository_root,
            )
        return self.to_dict()

    def continue_slot(
        self,
        slot_id: str,
        *,
        source_items_per_slot: int = DEFAULT_FIRST_PASS_SOURCE_ITEMS_PER_SLOT,
        fetch_bytes: Callable[[str, float, int], bytes] | None = None,
        timeout_seconds: float = DEFAULT_TIMEOUT_SECONDS,
        repository_root: str | None = None,
    ) -> dict[str, Any]:
        """Fetch the next unseen source batch for one already-inspected slot."""

        self._slot(slot_id)
        batches = self.slot_batches.get(slot_id)
        if not batches:
            raise ValueError("DetailedRead slot must receive a first pass before continuation")
        cursor = batches[-1].reader_report.get("continuation")
        if not isinstance(cursor, Mapping):
            raise MainKnowledgeUnavailable("DetailedRead slot has no valid continuation cursor")
        if cursor.get("has_more") is not True:
            return self.slot_report(slot_id)

        bundle = self._load_slot_bundle(
            slot_id,
            continuation=cursor,
            source_items_per_slot=source_items_per_slot,
            fetch_bytes=fetch_bytes,
            timeout_seconds=timeout_seconds,
            repository_root=repository_root,
        )
        batches.append(bundle)
        return self.slot_report(slot_id)

    def add_model_supplement(self, item: QuickReadEvidenceItem) -> None:
        """Attach a clearly labeled model-only note without changing source/runtime coverage."""

        if not isinstance(item, QuickReadEvidenceItem):
            raise ValueError("model supplement must be a QuickReadEvidenceItem")
        if item.lane != "MODEL_SUPPLEMENT":
            raise ValueError("only MODEL_SUPPLEMENT evidence may use this method")
        self._slot(item.slot_id)
        if not self.slot_batches.get(item.slot_id):
            raise ValueError("model supplement cannot stand in for an uninspected domain")
        if item.evidence_id in self.model_supplement_items:
            raise ValueError(f"duplicate model supplement evidence_id: {item.evidence_id}")
        if any(
            item.evidence_id == existing.evidence_id
            for existing in self._accepted_evidence_items()
        ):
            raise ValueError(f"duplicate evidence_id: {item.evidence_id}")
        self.model_supplement_items[item.evidence_id] = item

    def _accepted_evidence_items(self) -> tuple[QuickReadEvidenceItem, ...]:
        indexed: dict[str, QuickReadEvidenceItem] = {}
        slot_order = {
            slot.slot_id: index
            for index, slot in enumerate(self.plan.retrieval_slots)
        }
        for slot in self.plan.retrieval_slots:
            for bundle in self.slot_batches.get(slot.slot_id, []):
                for item in bundle.evidence_items:
                    previous = indexed.get(item.evidence_id)
                    if previous is not None and previous != item:
                        raise MainKnowledgeUnavailable(
                            f"conflicting duplicate DetailedRead evidence_id: {item.evidence_id}"
                        )
                    indexed[item.evidence_id] = item
        indexed.update(self.model_supplement_items)
        return tuple(
            sorted(
                indexed.values(),
                key=lambda item: (
                    slot_order[item.slot_id],
                    item.lane,
                    item.evidence_id,
                ),
            )
        )

    def slot_report(self, slot_id: str) -> dict[str, Any]:
        slot = self._slot(slot_id)
        batches = self.slot_batches.get(slot_id, [])
        model_count = sum(
            1 for item in self.model_supplement_items.values()
            if item.slot_id == slot_id
        )
        if not batches:
            return {
                "slot_id": slot.slot_id,
                "domain": slot.domain,
                "temporal_layer": slot.temporal_layer,
                "inspection_status": "NOT_INSPECTED",
                "runtime_status": "NOT_CHECKED",
                "source_status": "NOT_CHECKED",
                "runtime_evidence_count": 0,
                "source_evidence_count": 0,
                "model_supplement_count": model_count,
                "source_evidence_total_eligible": None,
                "source_evidence_remaining_after_batch": None,
                "excluded_case_support_only_count": 0,
                "excluded_not_promoted_count": 0,
                "excluded_uncertain_or_unverified_count": 0,
                "reason": "Domain has not yet been inspected.",
            }

        latest = batches[-1]
        record = latest.manifest.records[0]
        raw_slot = next(
            (
                item
                for item in latest.reader_report.get("slots", [])
                if item.get("slot_id") == slot_id
            ),
            {},
        )
        # Ledger exclusion counts describe the whole slot ledger, not each continuation batch.
        aggregate = batches[0].reader_report.get("aggregate_source_ledger_counts", {})
        evidence = [
            item
            for item in self._accepted_evidence_items()
            if item.slot_id == slot_id
        ]
        return {
            "slot_id": slot.slot_id,
            "domain": slot.domain,
            "temporal_layer": slot.temporal_layer,
            "inspection_status": "INSPECTED",
            "runtime_status": record.runtime_status,
            "source_status": record.source_status,
            "runtime_evidence_count": sum(1 for item in evidence if item.lane == "RUNTIME"),
            "source_evidence_count": sum(1 for item in evidence if item.lane == "SOURCE"),
            "model_supplement_count": model_count,
            "source_evidence_total_eligible": raw_slot.get(
                "source_evidence_total_eligible"
            ),
            "source_evidence_selected_this_batch": raw_slot.get(
                "source_evidence_selected_this_batch"
            ),
            "source_evidence_already_seen": raw_slot.get(
                "source_evidence_already_seen"
            ),
            "source_evidence_remaining_after_batch": raw_slot.get(
                "source_evidence_remaining_after_batch"
            ),
            "excluded_case_support_only_count": aggregate.get(
                "excluded_case_only", 0
            ),
            "excluded_not_promoted_count": aggregate.get(
                "excluded_not_promoted", 0
            ),
            "excluded_uncertain_or_unverified_count": aggregate.get(
                "excluded_uncertain_or_unverified", 0
            ),
            "excluded_layer_mismatch_count": aggregate.get(
                "excluded_layer_mismatch", 0
            ),
            "excluded_missing_provenance_count": aggregate.get(
                "excluded_missing_provenance", 0
            ),
            "reader_reason": raw_slot.get("reason", ""),
            "batch_count": len(batches),
            "main_sha": self.main_sha,
        }

    def stage_report(self, stage_id: str) -> dict[str, Any]:
        batch = next(
            (
                item
                for item in self.plan.retrieval_batches()
                if item["stage_id"] == stage_id
            ),
            None,
        )
        if batch is None:
            raise ValueError(f"unknown DetailedRead stage: {stage_id}")
        return {
            "stage_id": stage_id,
            "completed": all(
                self.slot_batches.get(slot_id)
                for slot_id in batch["slot_ids"]
            ),
            "main_sha": self.main_sha,
            "target_id": self.plan.target_id,
            "coverage": [
                self.slot_report(slot_id) for slot_id in batch["slot_ids"]
            ],
        }

    def to_dict(self) -> dict[str, Any]:
        evidence = self._accepted_evidence_items()
        coverage = [
            self.slot_report(slot.slot_id)
            for slot in self.plan.retrieval_slots
        ]
        natal_coverage = [
            item for item in coverage if item["temporal_layer"] == "NATAL"
        ]
        excluded_keys = (
            "excluded_case_support_only_count",
            "excluded_not_promoted_count",
            "excluded_uncertain_or_unverified_count",
            "excluded_layer_mismatch_count",
            "excluded_missing_provenance_count",
        )
        excluded = {
            key.removesuffix("_count"): sum(
                int(item.get(key, 0) or 0) for item in coverage
            )
            for key in excluded_keys
        }
        natal_complete = all(
            item["inspection_status"] == "INSPECTED"
            for item in natal_coverage
        )
        return {
            "schema_version": SCHEMA_VERSION,
            "reading_mode": "DETAILED_READ",
            "target_id": self.plan.target_id,
            "main_sha": self.main_sha,
            "session_status": (
                "NATAL_INSPECTION_COMPLETE"
                if natal_complete
                else "IN_PROGRESS"
            ),
            "natal_domain_count_required": len(NATAL_DOMAIN_ORDER),
            "natal_domain_count_inspected": sum(
                1
                for item in natal_coverage
                if item["inspection_status"] == "INSPECTED"
            ),
            "completed_stage_ids": list(self.completed_stage_ids),
            "coverage": coverage,
            "evidence": {
                "runtime": [
                    item.to_dict() for item in evidence if item.lane == "RUNTIME"
                ],
                "source": [
                    item.to_dict() for item in evidence if item.lane == "SOURCE"
                ],
                "model_supplement": [
                    item.to_dict()
                    for item in evidence
                    if item.lane == "MODEL_SUPPLEMENT"
                ],
            },
            "excluded_evidence_counts": excluded,
            "cross_domain_checks": self.plan.to_dict()["cross_domain_checks"],
            "sections": [item.to_dict() for item in self.plan.sections],
            "delivery": self.plan.to_dict()["delivery"],
            "guardrails": {
                "one_main_snapshot_for_all_slots": True,
                "same_chart_target_required": True,
                "runtime_source_model_supplement_separated": True,
                "case_support_only_and_unpromoted_records_excluded": True,
                "runtime_execution_performed": False,
                "unmerged_branches_consumed": False,
                "unsupported_domains_filled_from_model_memory": False,
            },
        }

