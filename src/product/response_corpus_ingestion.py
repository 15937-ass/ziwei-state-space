"""Source-backed Response Corpus ingestion/readiness audit v0.1.

This module inventories Knowledge-owned source material that can eventually feed
the Product Response Compiler.  It is intentionally fail-closed:

- source-explicit != compiler-ready Kr;
- reviewed != executable;
- normalized source row != canonical response record;
- time-scope labels are not split or upgraded by Product;
- case evidence is not promoted into reusable response rules.

The Product lane only selects rows through exact Knowledge-owned metadata and
reports readiness.  It does not infer missing Ziwei response semantics.
"""

from __future__ import annotations

from collections import Counter
import csv
from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any, Callable, Iterable, Mapping, Sequence

from .knowledge_bundle import require_artifact_locked


ROOT = Path(__file__).resolve().parents[2]

FROZEN_BASELINE = "16bb9b30f491afa27368e88767e5662dbdc54983"
ISSUE = 482

MAJOR_STARS_PATH = (
    ROOT / "knowledge" / "rules" / "stars" / "major_stars_canonical_v0.1.csv"
)
SIXTY_SYSTEMS_PATH = (
    ROOT / "knowledge" / "rules" / "systems" / "sixty_systems_canonical_v0.1.csv"
)
SIXTY_SYSTEMS_REVIEW_PATH = (
    ROOT / "knowledge" / "review" / "sixty_systems_review_v0.3.csv"
)
SIXTY_SYSTEMS_OVERRIDES_PATH = (
    ROOT
    / "knowledge"
    / "migrations"
    / "a0_sixty_systems_schema_overrides_v0.1.csv"
)
CAREER_TEMPORAL_ELIGIBILITY_PATH = (
    ROOT
    / "knowledge"
    / "wp07b"
    / "CAREER_TEMPORAL_REACTION_ELIGIBILITY_v0.1.csv"
)
CAREER_TEMPORAL_SUMMARY_PATH = (
    ROOT
    / "knowledge"
    / "wp07b"
    / "CAREER_TEMPORAL_REACTION_ELIGIBILITY_SUMMARY_v0.1.json"
)
RESPONSE_PILOT_PATH = (
    ROOT / "knowledge" / "response" / "RESPONSE_SEMANTICS_PILOT_v0.1.json"
)

READINESS_CLASSES = frozenset(
    {
        "SEMANTIC_VOCABULARY_ONLY",
        "SOURCE_TEMPORAL_CANDIDATE_AWAITING_KR_NORMALIZATION",
        "KNOWLEDGE_EXPLICITLY_BLOCKED",
        "COMPILER_READY_KR",
    }
)

MAJOR_REQUIRED_SOURCE_FIELDS = (
    "rule_id",
    "subject",
    "condition",
    "target_type",
    "target_literal",
    "operator",
    "evidence_text",
    "source_location",
)
SYSTEM_REQUIRED_SOURCE_FIELDS = (
    "rule_id",
    "system_name",
    "condition",
    "target_type",
    "target_literal",
    "operator",
    "evidence_text",
    "source_location",
)
CAREER_REQUIRED_SOURCE_FIELDS = (
    "candidate_id",
    "source_id",
    "source_location",
    "declared_time_layer",
    "source_time_scope",
    "eligibility_status",
    "blocking_reasons",
    "source_claim_summary",
    "decision",
)

MISSING_CANONICAL_KR_CONTRACT = (
    "CANONICAL_KR_RECORD_ID",
    "NATAL_ESSENCE_BINDING",
    "ENCOUNTERED_TEMPORAL_STRUCTURE_BINDING",
    "RESPONSE_OPERATOR_CONTRACT",
    "RESPONSE_EFFECT_TARGET_CONTRACT",
    "TEMPORAL_SCOPE_EXECUTION_CONTRACT",
    "KR_EXECUTION_STATUS_CONTRACT",
)


def _read_csv(path: Path) -> tuple[dict[str, str], ...]:
    require_artifact_locked(ROOT, path, "K_response")
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return tuple(dict(row) for row in csv.DictReader(handle))


def _read_json(path: Path) -> Any:
    require_artifact_locked(ROOT, path, "K_response")
    return json.loads(path.read_text(encoding="utf-8"))


def _required_text(value: Any, path: str) -> str:
    text = str(value or "").strip()
    if not text:
        raise ValueError(f"{path} is required")
    return text


def _counts(values: Iterable[str]) -> dict[str, int]:
    counter = Counter(value if value else "(empty)" for value in values)
    return dict(sorted(counter.items()))


def _missing_field_counts(
    rows: Sequence[Mapping[str, Any]],
    fields: Sequence[str],
) -> dict[str, int]:
    return {
        field: sum(1 for row in rows if not str(row.get(field, "") or "").strip())
        for field in fields
    }


def _require_unique(
    rows: Sequence[Mapping[str, Any]],
    key: str,
    family: str,
) -> None:
    values = [_required_text(row.get(key), f"{family}.{key}") for row in rows]
    if len(values) != len(set(values)):
        raise ValueError(f"{family}: duplicate {key} values")


def select_major_star_temporal_candidates(
    rows: Sequence[Mapping[str, str]],
) -> tuple[Mapping[str, str], ...]:
    """Use only the Knowledge-owned rule_family marker.

    Free-text time words are intentionally ignored.
    """

    return tuple(row for row in rows if row.get("rule_family") == "temporal_response")


def select_sixty_system_temporal_candidates(
    rows: Sequence[Mapping[str, str]],
) -> tuple[Mapping[str, str], ...]:
    """Use only the Knowledge-owned interaction_role marker."""

    return tuple(
        row for row in rows if row.get("interaction_role") == "temporal_reaction"
    )


@dataclass(frozen=True)
class SourceFamilyInventory:
    family_id: str
    artifact_paths: tuple[str, ...]
    selection_criterion: str
    total_rows: int
    selected_rows: int
    readiness_class: str
    scope_counts: Mapping[str, int]
    operator_counts: Mapping[str, int]
    review_status_counts: Mapping[str, int]
    source_epistemic_counts: Mapping[str, int]
    source_span_verified_counts: Mapping[str, int]
    normalization_epistemic_counts: Mapping[str, int]
    normalization_verified_counts: Mapping[str, int]
    missing_required_source_fields: Mapping[str, int]
    blockers: tuple[str, ...]
    details: Mapping[str, Any]

    def __post_init__(self) -> None:
        if self.readiness_class not in READINESS_CLASSES:
            raise ValueError(
                f"{self.family_id}: unsupported readiness class {self.readiness_class}"
            )
        if self.total_rows < 0 or self.selected_rows < 0:
            raise ValueError(f"{self.family_id}: row counts cannot be negative")
        if self.selected_rows > self.total_rows:
            raise ValueError(f"{self.family_id}: selected rows exceed total rows")

    def to_dict(self) -> dict[str, Any]:
        return {
            "family_id": self.family_id,
            "artifact_paths": list(self.artifact_paths),
            "selection_criterion": self.selection_criterion,
            "total_rows": self.total_rows,
            "selected_rows": self.selected_rows,
            "readiness_class": self.readiness_class,
            "scope_counts": dict(self.scope_counts),
            "operator_counts": dict(self.operator_counts),
            "review_status_counts": dict(self.review_status_counts),
            "source_epistemic_counts": dict(self.source_epistemic_counts),
            "source_span_verified_counts": dict(
                self.source_span_verified_counts
            ),
            "normalization_epistemic_counts": dict(
                self.normalization_epistemic_counts
            ),
            "normalization_verified_counts": dict(
                self.normalization_verified_counts
            ),
            "missing_required_source_fields": dict(
                self.missing_required_source_fields
            ),
            "blockers": list(self.blockers),
            "details": dict(self.details),
        }


def inventory_major_star_temporal_response() -> SourceFamilyInventory:
    rows = _read_csv(MAJOR_STARS_PATH)
    _require_unique(rows, "rule_id", "major_stars")
    selected = select_major_star_temporal_candidates(rows)

    blockers = ["NO_CANONICAL_KR_RECORD_CONTRACT"]
    if any(row.get("source_span_verified") != "true" for row in selected):
        blockers.append("SOURCE_SPAN_NOT_VERIFIED_FOR_SELECTED_ROWS")
    if any(row.get("normalization_verified") != "true" for row in selected):
        blockers.append("NORMALIZATION_NOT_VERIFIED_FOR_SELECTED_ROWS")

    return SourceFamilyInventory(
        family_id="MAJOR_STAR_TEMPORAL_RESPONSE",
        artifact_paths=(str(MAJOR_STARS_PATH.relative_to(ROOT)),),
        selection_criterion="rule_family == temporal_response",
        total_rows=len(rows),
        selected_rows=len(selected),
        readiness_class="SOURCE_TEMPORAL_CANDIDATE_AWAITING_KR_NORMALIZATION",
        scope_counts=_counts(row.get("applicability_scope", "") for row in selected),
        operator_counts=_counts(row.get("operator", "") for row in selected),
        review_status_counts=_counts(row.get("review_status", "") for row in selected),
        source_epistemic_counts=_counts(
            row.get("source_epistemic", "") for row in selected
        ),
        source_span_verified_counts=_counts(
            row.get("source_span_verified", "") for row in selected
        ),
        normalization_epistemic_counts=_counts(
            row.get("normalization_epistemic", "") for row in selected
        ),
        normalization_verified_counts=_counts(
            row.get("normalization_verified", "") for row in selected
        ),
        missing_required_source_fields=_missing_field_counts(
            selected, MAJOR_REQUIRED_SOURCE_FIELDS
        ),
        blockers=tuple(blockers),
        details={
            "candidate_ids_sample": [row["rule_id"] for row in selected[:10]],
            "candidate_ids_total": len(selected),
            "product_semantic_promotion": False,
        },
    )


def inventory_sixty_system_temporal_reaction() -> SourceFamilyInventory:
    rows = _read_csv(SIXTY_SYSTEMS_PATH)
    reviews = _read_csv(SIXTY_SYSTEMS_REVIEW_PATH)
    overrides = _read_csv(SIXTY_SYSTEMS_OVERRIDES_PATH)

    _require_unique(rows, "rule_id", "sixty_systems")
    _require_unique(reviews, "rule_id", "sixty_system_reviews")

    row_ids = {row["rule_id"] for row in rows}
    review_ids = {row["rule_id"] for row in reviews}
    if row_ids != review_ids:
        raise ValueError("sixty-system canonical/review sidecar IDs do not match")

    review_by_id = {row["rule_id"]: row for row in reviews}
    override_ids = {row.get("rule_id", "") for row in overrides}
    if not override_ids.issubset(row_ids):
        raise ValueError("sixty-system override references unknown rule IDs")

    selected = select_sixty_system_temporal_candidates(rows)
    selected_review = [review_by_id[row["rule_id"]] for row in selected]

    blockers = ["NO_CANONICAL_KR_RECORD_CONTRACT"]
    if any(row.get("source_span_verified") != "true" for row in selected_review):
        blockers.append("SOURCE_SPAN_NOT_VERIFIED_FOR_SELECTED_ROWS")
    if any(row.get("normalization_verified") != "true" for row in selected_review):
        blockers.append("NORMALIZATION_NOT_VERIFIED_FOR_SELECTED_ROWS")
    if any(
        row.get("normalization_epistemic") == "UNRESOLVED"
        for row in selected_review
    ):
        blockers.append("NORMALIZATION_EPISTEMIC_UNRESOLVED_PRESENT")

    selected_ids = {row["rule_id"] for row in selected}
    return SourceFamilyInventory(
        family_id="SIXTY_SYSTEM_TEMPORAL_REACTION",
        artifact_paths=(
            str(SIXTY_SYSTEMS_PATH.relative_to(ROOT)),
            str(SIXTY_SYSTEMS_REVIEW_PATH.relative_to(ROOT)),
            str(SIXTY_SYSTEMS_OVERRIDES_PATH.relative_to(ROOT)),
        ),
        selection_criterion="interaction_role == temporal_reaction",
        total_rows=len(rows),
        selected_rows=len(selected),
        readiness_class="SOURCE_TEMPORAL_CANDIDATE_AWAITING_KR_NORMALIZATION",
        scope_counts=_counts(row.get("applicability_scope", "") for row in selected),
        operator_counts=_counts(row.get("operator", "") for row in selected),
        review_status_counts=_counts(
            row.get("review_status", "") for row in selected_review
        ),
        source_epistemic_counts=_counts(
            row.get("source_epistemic", "") for row in selected_review
        ),
        source_span_verified_counts=_counts(
            row.get("source_span_verified", "") for row in selected_review
        ),
        normalization_epistemic_counts=_counts(
            row.get("normalization_epistemic", "") for row in selected_review
        ),
        normalization_verified_counts=_counts(
            row.get("normalization_verified", "") for row in selected_review
        ),
        missing_required_source_fields=_missing_field_counts(
            selected, SYSTEM_REQUIRED_SOURCE_FIELDS
        ),
        blockers=tuple(blockers),
        details={
            "candidate_ids_sample": [row["rule_id"] for row in selected[:10]],
            "candidate_ids_total": len(selected),
            "selected_rows_with_schema_override": sum(
                1 for rule_id in selected_ids if rule_id in override_ids
            ),
            "product_semantic_promotion": False,
        },
    )


def inventory_career_temporal_eligibility() -> SourceFamilyInventory:
    rows = _read_csv(CAREER_TEMPORAL_ELIGIBILITY_PATH)
    summary = _read_json(CAREER_TEMPORAL_SUMMARY_PATH)
    _require_unique(rows, "candidate_id", "career_temporal_eligibility")

    if int(summary.get("candidates_audited", -1)) != len(rows):
        raise ValueError("Career temporal summary/candidate count mismatch")

    eligible = int(summary.get("eligible_for_current_compiler", -1))
    blocked = int(summary.get("blocked", -1))
    excluded = int(summary.get("case_support_only_excluded", -1))
    if eligible < 0 or blocked < 0 or excluded < 0:
        raise ValueError("Career temporal summary contains invalid counts")
    if eligible + blocked + excluded != len(rows):
        raise ValueError("Career temporal disposition counts do not cover candidates")

    if eligible > 0:
        # "Eligible for current compiler" is a Knowledge-owned eligibility
        # finding, not proof that a canonical Kr contract exists.  Product may
        # surface it as candidate material but may not promote it to Kr.
        readiness = "SOURCE_TEMPORAL_CANDIDATE_AWAITING_KR_NORMALIZATION"
        blockers: tuple[str, ...] = (
            "CANONICAL_KR_CONTRACT_REQUIRED_AFTER_ELIGIBILITY",
            "NO_PRODUCT_PROMOTION_OF_ELIGIBILITY_TO_KR",
        )
    else:
        readiness = "KNOWLEDGE_EXPLICITLY_BLOCKED"
        blockers = (
            "KNOWLEDGE_ELIGIBLE_FOR_CURRENT_COMPILER_ZERO",
            "NO_PRODUCT_PROMOTION_OF_BLOCKED_OR_CASE_SUPPORT_ROWS",
        )

    return SourceFamilyInventory(
        family_id="CAREER_TEMPORAL_ELIGIBILITY",
        artifact_paths=(
            str(CAREER_TEMPORAL_ELIGIBILITY_PATH.relative_to(ROOT)),
            str(CAREER_TEMPORAL_SUMMARY_PATH.relative_to(ROOT)),
        ),
        selection_criterion="all rows in explicit Knowledge temporal eligibility audit",
        total_rows=len(rows),
        selected_rows=len(rows),
        readiness_class=readiness,
        scope_counts=_counts(row.get("declared_time_layer", "") for row in rows),
        operator_counts={},
        review_status_counts={},
        source_epistemic_counts={},
        source_span_verified_counts={},
        normalization_epistemic_counts={},
        normalization_verified_counts={},
        missing_required_source_fields=_missing_field_counts(
            rows, CAREER_REQUIRED_SOURCE_FIELDS
        ),
        blockers=blockers,
        details={
            "eligibility_status_counts": _counts(
                row.get("eligibility_status", "") for row in rows
            ),
            "eligible_for_current_compiler": eligible,
            "blocked": blocked,
            "case_support_only_excluded": excluded,
            "executable_pilot_emitted": bool(
                summary.get("executable_pilot_emitted", False)
            ),
            "production_registry_should_remain_empty": bool(
                summary.get("production_registry_should_remain_empty", False)
            ),
            "product_semantic_promotion": False,
        },
    )


def inventory_response_semantics_pilot() -> SourceFamilyInventory:
    payload = _read_json(RESPONSE_PILOT_PATH)
    records = payload.get("records")
    if not isinstance(records, list):
        raise ValueError("Response Semantics pilot records must be an array")
    ids = [_required_text(row.get("record_id"), "response_pilot.record_id") for row in records]
    if len(ids) != len(set(ids)):
        raise ValueError("Response Semantics pilot record IDs must be unique")

    time_layers = []
    for row in records:
        scope = row.get("scope")
        if not isinstance(scope, dict):
            raise ValueError(f"{row.get('record_id')}: scope must be an object")
        time_layers.append(str(scope.get("time_layer") or "(unset)"))

    executable = sum(
        1 for row in records if row.get("execution_status") == "SAFE_SYMBOLIC"
    )
    # ResponseSemanticsRecord is vocabulary/structure for the Product adapter;
    # SAFE_SYMBOLIC, if it appears in a future pilot revision, still does not
    # turn this artifact into a temporal Kr corpus.
    readiness = "SEMANTIC_VOCABULARY_ONLY"
    blockers_list = ["NO_CANONICAL_KR_RECORD_CONTRACT"]
    if all(value == "(unset)" for value in time_layers):
        blockers_list.append("NO_TEMPORAL_SCOPE_BINDING")
    blockers_list.append("RESPONSE_SEMANTICS_EXECUTION_STATUS_IS_NOT_KR_AUTHORIZATION")
    blockers = tuple(blockers_list)

    return SourceFamilyInventory(
        family_id="RESPONSE_SEMANTICS_PILOT",
        artifact_paths=(str(RESPONSE_PILOT_PATH.relative_to(ROOT)),),
        selection_criterion="all explicit ResponseSemanticsRecord pilot rows",
        total_rows=len(records),
        selected_rows=len(records),
        readiness_class=readiness,
        scope_counts=_counts(time_layers),
        operator_counts={},
        review_status_counts={},
        source_epistemic_counts={},
        source_span_verified_counts={},
        normalization_epistemic_counts={},
        normalization_verified_counts={},
        missing_required_source_fields={},
        blockers=blockers,
        details={
            "semantic_role_counts": _counts(
                str(row.get("semantic_role") or "") for row in records
            ),
            "execution_status_counts": _counts(
                str(row.get("execution_status") or "") for row in records
            ),
            "temporal_scope_bound_records": sum(
                1 for value in time_layers if value != "(unset)"
            ),
            "safe_symbolic_records": executable,
            "product_semantic_promotion": False,
        },
    )


def build_source_family_inventories() -> tuple[SourceFamilyInventory, ...]:
    return (
        inventory_major_star_temporal_response(),
        inventory_sixty_system_temporal_reaction(),
        inventory_career_temporal_eligibility(),
        inventory_response_semantics_pilot(),
    )


def _merge_count_maps(*maps: Mapping[str, int]) -> dict[str, int]:
    merged: Counter[str] = Counter()
    for mapping in maps:
        merged.update(mapping)
    return dict(sorted(merged.items()))


def build_response_corpus_readiness() -> dict[str, Any]:
    families = build_source_family_inventories()
    by_id = {family.family_id: family for family in families}

    major = by_id["MAJOR_STAR_TEMPORAL_RESPONSE"]
    systems = by_id["SIXTY_SYSTEM_TEMPORAL_REACTION"]
    career = by_id["CAREER_TEMPORAL_ELIGIBILITY"]
    pilot = by_id["RESPONSE_SEMANTICS_PILOT"]

    source_candidate_rows = major.selected_rows + systems.selected_rows
    compiler_ready_kr = sum(
        family.selected_rows
        for family in families
        if family.readiness_class == "COMPILER_READY_KR"
    )

    source_span_verified_candidate_rows = (
        major.source_span_verified_counts.get("true", 0)
        + systems.source_span_verified_counts.get("true", 0)
    )
    normalization_verified_candidate_rows = (
        major.normalization_verified_counts.get("true", 0)
        + systems.normalization_verified_counts.get("true", 0)
    )

    missing_source_fields = sum(
        sum(family.missing_required_source_fields.values())
        for family in (major, systems, career)
    )

    report = {
        "schema_version": "0.1",
        "artifact_id": "PRODUCT_RESPONSE_CORPUS_READINESS_V0_1",
        "issue": ISSUE,
        "frozen_baseline": FROZEN_BASELINE,
        "mode": "FAIL_CLOSED_SOURCE_INVENTORY_NO_SEMANTIC_INFERENCE",
        "source_families": [family.to_dict() for family in families],
        "summary": {
            "source_temporal_candidate_rows": source_candidate_rows,
            "major_star_temporal_response_rows": major.selected_rows,
            "sixty_system_temporal_reaction_rows": systems.selected_rows,
            "career_temporal_audit_rows": career.selected_rows,
            "response_semantics_pilot_rows": pilot.selected_rows,
            "source_span_verified_temporal_candidate_rows": (
                source_span_verified_candidate_rows
            ),
            "normalization_verified_temporal_candidate_rows": (
                normalization_verified_candidate_rows
            ),
            "missing_required_source_field_occurrences": missing_source_fields,
            "knowledge_explicit_compiler_eligible_rows": int(
                career.details["eligible_for_current_compiler"]
            ),
            "compiler_ready_kr_records": compiler_ready_kr,
            "candidate_scope_counts": _merge_count_maps(
                major.scope_counts, systems.scope_counts
            ),
            "candidate_operator_counts": _merge_count_maps(
                major.operator_counts, systems.operator_counts
            ),
        },
        "kr_contract_gap": {
            "missing_canonical_contract_dimensions": list(
                MISSING_CANONICAL_KR_CONTRACT
            ),
            "knowledge_owned_normalization_required": True,
            "product_may_infer_missing_semantics": False,
            "product_may_split_decade_or_year": False,
            "product_may_promote_case_support": False,
            "product_may_numericize_valence": False,
        },
        "now6_gate": {
            "NOW6_RESPONSE_COMPILER_INPUT_READY": compiler_ready_kr > 0,
            "reason": (
                "No Knowledge-owned compiler-ready Kr records are present in the "
                "audited source families; source temporal candidates remain "
                "candidate material awaiting canonical Kr normalization."
                if compiler_ready_kr == 0
                else "Knowledge-owned compiler-ready Kr records are present."
            ),
            "response_compiler_implemented": False,
            "response_profile_tau_implemented": False,
            "predictive_validity": "NOT_VALIDATED",
        },
        "boundaries": {
            "source_explicit_implies_compiler_ready": False,
            "reviewed_implies_executable": False,
            "normalized_source_row_implies_kr_record": False,
            "favorable_unfavorable_implies_numeric_gain": False,
            "temporal_scope_implies_layer_split": False,
            "case_support_implies_reusable_rule": False,
        },
    }

    if report["summary"]["compiler_ready_kr_records"] != 0:
        # v0.1 may report a future source-controlled unlock, but cannot silently
        # call NOW-6 ready without an explicit Knowledge-owned Kr contract.
        if report["kr_contract_gap"]["missing_canonical_contract_dimensions"]:
            report["now6_gate"]["NOW6_RESPONSE_COMPILER_INPUT_READY"] = False
            report["now6_gate"]["reason"] = (
                "Candidate Knowledge rows report eligibility, but the canonical "
                "Kr contract is still absent; Product remains fail-closed."
            )

    return report


def validate_current_fail_closed_state() -> None:
    report = build_response_corpus_readiness()
    summary = report["summary"]
    if summary["compiler_ready_kr_records"] != 0:
        raise ValueError("v0.1 unexpectedly detected compiler-ready Kr records")
    if report["now6_gate"]["NOW6_RESPONSE_COMPILER_INPUT_READY"]:
        raise ValueError("NOW-6 must remain blocked without canonical Kr records")


def write_readiness_report(path: Path) -> None:
    path.write_text(
        json.dumps(
            build_response_corpus_readiness(),
            ensure_ascii=False,
            indent=2,
            sort_keys=False,
        )
        + "\n",
        encoding="utf-8",
    )
