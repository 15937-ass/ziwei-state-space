"""DetailedRead private-chat planning contract v0.1.

This module plans a full-chart, multi-turn reading on top of the accepted
QuickRead evidence contract. It does not calculate a chart, read GitHub,
call an LLM, or create a second rule/knowledge engine.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any, Mapping, Sequence

from .quickread_capability import QuickReadRequest, QuickReadScopeSlot


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
