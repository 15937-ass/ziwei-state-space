"""PL2-C wealth-palace executable pilot.

Consumes the source-span-verified W01 projection checkpoint plus an explicit
product normalization registry. It never parses traditional free-text
conditions heuristically.
"""

from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Mapping

from .condition_atoms import compile_condition_spec, fact_from_atom
from .rule_runtime import CompilationReport, RuleRuntime, RuntimeState, compile_rule_row


@dataclass(frozen=True)
class WealthPilotLedgerRow:
    projection_rule_id: str
    disposition: str
    reason: str


def _truthy(value: Any) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def load_projection_rows(path: str | Path) -> list[dict[str, str]]:
    with Path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def load_pilot_registry(path: str | Path) -> dict[str, Any]:
    with Path(path).open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if data.get("schema_version") != "0.1":
        raise ValueError("wealth pilot registry schema_version must be 0.1")
    if data.get("palace_id") != "P05":
        raise ValueError("wealth pilot registry must target P05")
    rules = data.get("rules")
    if not isinstance(rules, Mapping) or not rules:
        raise ValueError("wealth pilot registry requires a non-empty rules mapping")
    return data


def _row_index(rows: Iterable[Mapping[str, str]]) -> dict[str, Mapping[str, str]]:
    out: dict[str, Mapping[str, str]] = {}
    for row in rows:
        rule_id = str(row.get("projection_rule_id", "")).strip()
        if not rule_id:
            raise ValueError("projection row missing projection_rule_id")
        if rule_id in out:
            raise ValueError(f"duplicate projection_rule_id: {rule_id}")
        out[rule_id] = row
    return out


def _validate_selected_source_row(
    rule_id: str,
    source_row: Mapping[str, str],
    registry_row: Mapping[str, Any],
) -> None:
    if source_row.get("review_status") != "SOURCE_SPAN_VERIFIED":
        raise ValueError(f"{rule_id}: source row is not SOURCE_SPAN_VERIFIED")
    if not _truthy(source_row.get("source_span_verified")):
        raise ValueError(f"{rule_id}: source span is not verified")
    if _truthy(source_row.get("case_support_only")):
        raise ValueError(f"{rule_id}: CASE_SUPPORT_ONLY cannot enter executable pilot")
    if source_row.get("palace_id") != "P05":
        raise ValueError(f"{rule_id}: expected palace P05")
    if source_row.get("time_layer") != "NATAL":
        raise ValueError(f"{rule_id}: PL2-C v0.1 accepts NATAL rules only")

    checks = {
        "condition": registry_row.get("expected_condition"),
        "projection_target": registry_row.get("expected_projection_target"),
        "projection_mode": registry_row.get("expected_projection_mode"),
    }
    for field, expected in checks.items():
        if source_row.get(field) != expected:
            raise ValueError(
                f"{rule_id}: canonical source drift in {field}: "
                f"{source_row.get(field)!r} != {expected!r}"
            )


def compile_wealth_pilot(
    projection_rows: Iterable[Mapping[str, str]],
    registry: Mapping[str, Any],
) -> CompilationReport:
    """Compile only explicitly selected, source-verified W01 rules."""

    index = _row_index(projection_rows)
    executable = []
    issues = []

    for rule_id in sorted(registry["rules"]):
        registry_row = registry["rules"][rule_id]
        source_row = index.get(rule_id)
        if source_row is None:
            raise ValueError(f"{rule_id}: selected rule missing from canonical W01 source")
        _validate_selected_source_row(rule_id, source_row, registry_row)

        normalized_row = {
            "rule_id": rule_id,
            "school": "中州派",
            "source_work": source_row["source_id"],
            "source_location": source_row["source_location"],
            "subject": "财帛宫",
            "context": "wealth",
            "condition": source_row["condition"],
            "time_scope": json.dumps(["NATAL"], ensure_ascii=False),
            "palace_scope": json.dumps(["P05"], ensure_ascii=False),
            "topic_scope": json.dumps(["财帛"], ensure_ascii=False),
            "operator": "projection",
            "target_type": source_row["projection_domain"],
            "target_normalized": source_row["projection_target"],
            "state_change": source_row["projection_mode"],
            "valence": "",
            # W01 checkpoints do not export source_epistemic as a column.
            # Do not invent EXPLICIT/INFERRED; preserve the checkpoint fact instead.
            "source_epistemic": "WP05_SOURCE_SPAN_VERIFIED",
            "normalization_epistemic": "IMPLEMENTATION",
            "review_status": source_row["review_status"],
            "source_span_verified": source_row["source_span_verified"],
            "normalization_verified": "true",
            "evidence_text": source_row["condition"],
        }

        condition = compile_condition_spec(registry_row["condition"])
        ir, issue = compile_rule_row(normalized_row, condition_spec=condition)
        if ir is not None:
            executable.append(ir)
        if issue is not None:
            issues.append(issue)

    return CompilationReport(
        executable=tuple(sorted(executable, key=lambda item: item.rule_id)),
        issues=tuple(sorted(issues, key=lambda item: item.rule_id)),
    )


def build_w01_coverage_ledger(
    projection_rows: Iterable[Mapping[str, str]],
    registry: Mapping[str, Any],
) -> tuple[WealthPilotLedgerRow, ...]:
    """Classify the whole W01 checkpoint without auto-normalizing unselected rows."""

    selected = set(registry["rules"])
    ledger: list[WealthPilotLedgerRow] = []
    for row in projection_rows:
        rule_id = row["projection_rule_id"]
        if _truthy(row.get("case_support_only")):
            disposition = "EXCLUDED"
            reason = "CASE_SUPPORT_ONLY"
        elif str(row.get("history_feedback", "")).strip():
            disposition = "PATH_DEPENDENT_HOLD"
            reason = "history feedback requires typed temporal/history integration"
        elif rule_id in selected:
            disposition = "EXECUTABLE"
            reason = "explicit PL2-C normalization registry"
        else:
            disposition = "NORMALIZATION_PENDING"
            reason = "not atomized in bounded PL2-C pilot"
        ledger.append(WealthPilotLedgerRow(rule_id, disposition, reason))
    return tuple(ledger)


def summarize_ledger(
    ledger: Iterable[WealthPilotLedgerRow],
) -> dict[str, int]:
    counts = {
        "EXECUTABLE": 0,
        "NORMALIZATION_PENDING": 0,
        "PATH_DEPENDENT_HOLD": 0,
        "EXCLUDED": 0,
    }
    for row in ledger:
        counts[row.disposition] = counts.get(row.disposition, 0) + 1
    return counts


def _find_wealth_palace(snapshot: Mapping[str, Any]) -> Mapping[str, Any]:
    chart = snapshot.get("chart")
    if isinstance(chart, Mapping) and isinstance(chart.get("palaces"), Mapping):
        palaces = chart["palaces"]
    else:
        natal = snapshot.get("natal")
        if not isinstance(natal, Mapping) or not isinstance(natal.get("palaces"), Mapping):
            raise ValueError("snapshot has no chart/natal palaces mapping")
        palaces = natal["palaces"]

    for key, palace in palaces.items():
        if not isinstance(palace, Mapping):
            continue
        name = str(palace.get("name", "")).strip()
        if str(key).strip() in {"财帛", "财帛宫"} or name in {"财帛", "财帛宫"}:
            return palace
    raise ValueError("wealth palace not found in normalized snapshot")


def extract_wealth_facts(snapshot: Mapping[str, Any]) -> frozenset[str]:
    """Extract only chart facts needed by the current PL2-C pilot."""

    palace = _find_wealth_palace(snapshot)
    facts: set[str] = {
        "subject:财帛宫",
        fact_from_atom("PALACE_PRESENT", palace="P05"),
    }

    branch = str(palace.get("branch", "")).strip()
    if branch:
        facts.add(fact_from_atom("BRANCH_PRESENT", palace="P05", branch=branch))

    for field in ("major_stars", "minor_stars", "adjective_stars"):
        stars = palace.get(field, [])
        if not isinstance(stars, list):
            raise ValueError(f"wealth palace {field} must be a list")
        for star in stars:
            if not isinstance(star, Mapping):
                continue
            name = str(star.get("name", "")).strip()
            if not name:
                continue
            facts.add(fact_from_atom("STAR_PRESENT", star=name))
            facts.add(fact_from_atom("PALACE_HAS_STAR", palace="P05", star=name))

            mutagen = str(star.get("mutagen") or "").strip()
            if mutagen:
                facts.add(
                    fact_from_atom(
                        "TRANSFORMATION_PRESENT",
                        palace="P05",
                        mutagen=mutagen,
                    )
                )
                facts.add(
                    fact_from_atom(
                        "TRANSFORMATION_PRESENT",
                        palace="P05",
                        star=name,
                        mutagen=mutagen,
                    )
                )

    return frozenset(facts)


def build_wealth_runtime_state(snapshot: Mapping[str, Any]) -> RuntimeState:
    return RuntimeState(
        facts=extract_wealth_facts(snapshot),
        latent_states={},
        time_scope="NATAL",
        palace_scope="P05",
    )


def run_wealth_pilot(
    snapshot: Mapping[str, Any],
    projection_rows: Iterable[Mapping[str, str]],
    registry: Mapping[str, Any],
):
    report = compile_wealth_pilot(projection_rows, registry)
    if report.issues:
        raise ValueError(f"wealth pilot contains compile issues: {report.issues!r}")
    runtime = RuleRuntime(report.executable)
    return runtime.match(
        build_wealth_runtime_state(snapshot),
        question_scope="财帛",
    )


def build_wealth_evidence_package(
    snapshot: Mapping[str, Any],
    projection_rows: Iterable[Mapping[str, str]],
    registry: Mapping[str, Any],
    *,
    question: str = "财帛结构",
):
    """Build a deterministic no-LLM EvidencePackage for the PL2-C pilot."""

    from .evidence_bridge import graph_to_evidence_package

    report = compile_wealth_pilot(projection_rows, registry)
    if report.issues:
        raise ValueError(f"wealth pilot contains compile issues: {report.issues!r}")

    runtime_state = build_wealth_runtime_state(snapshot)
    runtime = RuleRuntime(report.executable)
    graph = runtime.match(runtime_state, question_scope="财帛")

    ledger = build_w01_coverage_ledger(projection_rows, registry)
    coverage = summarize_ledger(ledger)

    engine = snapshot.get("engine", {})
    if isinstance(engine, Mapping):
        engine_name = str(engine.get("name", "")).strip()
        engine_version_value = str(engine.get("version", "")).strip()
    else:
        engine_name = ""
        engine_version_value = ""

    engine_version = ":".join(
        part for part in (engine_name, engine_version_value) if part
    )

    return graph_to_evidence_package(
        graph,
        report.executable,
        facts=runtime_state.facts,
        question=question,
        coverage=coverage,
        chart_facts={
            "palace_id": "P05",
            "time_layer": "NATAL",
            "observed_fact_count": len(runtime_state.facts),
        },
        engine_version=engine_version,
        knowledge_version="W01+PL2C-v0.1",
    )
