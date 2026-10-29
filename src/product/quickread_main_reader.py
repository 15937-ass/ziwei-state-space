"""Read the latest accepted QuickRead knowledge snapshot from public GitHub main.

This module is a read-only discovery/retrieval adapter. It pins every artifact to
one main commit, verifies Git blob SHAs, discovers only explicitly supported
Product provider registries and source-first review ledgers, and never promotes
source records into executable rules or invokes an LLM.
"""
from __future__ import annotations

import argparse
import ast
import csv
import hashlib
import io
import json
import re
import subprocess
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Callable, Mapping, Sequence
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

from .quickread_capability import (
    CapabilityManifest,
    CapabilityRecord,
    EvidenceSourceRef,
    QuickReadEvidenceItem,
    QuickReadRequest,
    QuickReadScopeSlot,
    build_quickread_payload,
)


REPOSITORY = "15937-ass/ziwei-state-space"
API_ROOT = f"https://api.github.com/repos/{REPOSITORY}"
RAW_ROOT = f"https://raw.githubusercontent.com/{REPOSITORY}"
DEFAULT_TIMEOUT_SECONDS = 8.0
MAX_API_BYTES = 24_000_000
MAX_ARTIFACT_BYTES = 2_000_000
MAX_TOTAL_FETCH_BYTES = 10_000_000
DEFAULT_FIRST_PASS_SOURCE_ITEMS_PER_SLOT = 12
MAX_SOURCE_ITEMS_PER_BATCH_PER_SLOT = 50
SUPPORTED_SOURCE_LEDGER_STATUS = "SOURCE_REVIEW_COMPLETE"
SUPPORTED_SOURCE_REVIEW_METHOD = "DIRECT_PDF_VISUAL_REVIEW"
SOURCE_REVIEW_STATUS = "SOURCE_SPAN_VERIFIED"

# Keep aliases explicit and conservative. Unknown domains can still discover a
# matching Product provider, but they do not scan an unrelated palace's ledger.
DOMAIN_PALACE: dict[str, tuple[str, str]] = {
    "life": ("P01", "life"),
    "命": ("P01", "life"),
    "命宫": ("P01", "life"),
    "siblings": ("P02", "siblings"),
    "兄弟": ("P02", "siblings"),
    "兄弟宫": ("P02", "siblings"),
    "relationship": ("P03", "spouse"),
    "spouse": ("P03", "spouse"),
    "marriage": ("P03", "spouse"),
    "感情": ("P03", "spouse"),
    "夫妻": ("P03", "spouse"),
    "夫妻宫": ("P03", "spouse"),
    "wealth": ("P05", "wealth"),
    "finance": ("P05", "wealth"),
    "财帛": ("P05", "wealth"),
    "财帛宫": ("P05", "wealth"),
    "health": ("P06", "health"),
    "健康": ("P06", "health"),
    "疾厄": ("P06", "health"),
    "疾厄宫": ("P06", "health"),
    "migration": ("P07", "migration"),
    "travel": ("P07", "migration"),
    "迁移": ("P07", "migration"),
    "迁移宫": ("P07", "migration"),
    "friends": ("P08", "friends"),
    "network": ("P08", "friends"),
    "交友": ("P08", "friends"),
    "交友宫": ("P08", "friends"),
    "career": ("P09", "career"),
    "work": ("P09", "career"),
    "事业": ("P09", "career"),
    "事业宫": ("P09", "career"),
    "property": ("P10", "property"),
    "田宅": ("P10", "property"),
    "田宅宫": ("P10", "property"),
    "fortune": ("P11", "fortune"),
    "福德": ("P11", "fortune"),
    "福德宫": ("P11", "fortune"),
    "parents": ("P12", "parents"),
    "父母": ("P12", "parents"),
    "父母宫": ("P12", "parents"),
}

DOMAIN_QUERY_TERMS: dict[str, tuple[str, ...]] = {
    "life": ("命宫", "性格", "个性", "格局"),
    "siblings": ("兄弟", "手足", "同辈"),
    "relationship": ("夫妻", "婚姻", "配偶", "感情", "伴侣"),
    "wealth": ("财帛", "财富", "金钱", "收入", "理财"),
    "health": ("疾厄", "健康", "身体"),
    "migration": ("迁移", "出行", "外地", "搬迁"),
    "friends": ("交友", "朋友", "人际", "合作"),
    "career": ("事业", "工作", "职业", "职位", "创业"),
    "property": ("田宅", "房产", "居住", "家庭资产"),
    "fortune": ("福德", "精神", "享受", "内在"),
    "parents": ("父母", "长辈", "家庭关系"),
}


class MainKnowledgeUnavailable(RuntimeError):
    """Raised when current-main data cannot be verified safely."""


FetchBytes = Callable[[str, float, int], bytes]


def _default_fetch_bytes(url: str, timeout: float, max_bytes: int) -> bytes:
    request = Request(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "ziwei-state-space-quickread/0.1",
        },
    )
    try:
        with urlopen(request, timeout=timeout) as response:
            data = response.read(max_bytes + 1)
    except (HTTPError, URLError, TimeoutError, OSError) as exc:
        raise MainKnowledgeUnavailable(f"GitHub main read failed: {type(exc).__name__}") from exc
    if len(data) > max_bytes:
        raise MainKnowledgeUnavailable(f"response exceeds configured limit: {url}")
    return data


def _git_blob_sha(content: bytes) -> str:
    header = f"blob {len(content)}\0".encode("ascii")
    return hashlib.sha1(header + content).hexdigest()


def _default_checkout_matches_main(root: Path, main_sha: str) -> bool:
    """Return true only for a clean checkout at the exact remote-main commit."""
    try:
        head = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=root,
            capture_output=True,
            text=True,
            timeout=3,
            check=False,
        )
        if head.returncode != 0 or head.stdout.strip() != main_sha:
            return False
        status = subprocess.run(
            ["git", "status", "--porcelain", "--untracked-files=all"],
            cwd=root,
            capture_output=True,
            text=True,
            timeout=3,
            check=False,
        )
        return status.returncode == 0 and not status.stdout.strip()
    except (OSError, subprocess.SubprocessError):
        return False


def _sha256_digest(parts: Sequence[str]) -> str:
    material = "\n".join(sorted(parts)).encode("utf-8")
    return hashlib.sha256(material).hexdigest()


def _normalize_domain(value: str) -> str:
    raw = str(value or "").strip()
    if raw in DOMAIN_PALACE:
        code, slug = DOMAIN_PALACE[raw]
        return {
            "P01": "life",
            "P02": "siblings",
            "P03": "relationship",
            "P05": "wealth",
            "P06": "health",
            "P07": "migration",
            "P08": "friends",
            "P09": "career",
            "P10": "property",
            "P11": "fortune",
            "P12": "parents",
        }[code]
    normalized = raw.lower().replace("-", "_").replace(" ", "_")
    aliases = {
        "spouse": "relationship",
        "marriage": "relationship",
        "finance": "wealth",
        "work": "career",
        "travel": "migration",
        "network": "friends",
    }
    return aliases.get(normalized, normalized)


def _palace_code(domain: str) -> str | None:
    normalized = _normalize_domain(domain)
    for alias, (code, _) in DOMAIN_PALACE.items():
        if _normalize_domain(alias) == normalized:
            return code
    return None


def _call_name(node: ast.AST) -> str:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        return node.attr
    return ""


def _default_runtime_domains(source: str) -> tuple[str, ...]:
    """Read the default provider set from the accepted runtime registry AST.

    If the registry shape changes, fail closed instead of guessing from filenames.
    """
    try:
        module = ast.parse(source)
    except SyntaxError:
        return ()
    function = next(
        (
            node
            for node in module.body
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
            and node.name == "load_default_natal_domain_registry"
        ),
        None,
    )
    if function is None:
        return ()

    assigned: dict[str, str] = {}
    provider_pattern = re.compile(r"^load_default_([a-z0-9]+)_natal_provider$")
    for node in function.body:
        if not isinstance(node, (ast.Assign, ast.AnnAssign)):
            continue
        value = node.value
        if not isinstance(value, ast.Call):
            continue
        match = provider_pattern.match(_call_name(value.func))
        if not match:
            continue
        targets = node.targets if isinstance(node, ast.Assign) else [node.target]
        for target in targets:
            if isinstance(target, ast.Name):
                assigned[target.id] = match.group(1)

    returned_domains: set[str] = set()
    for node in ast.walk(function):
        if not isinstance(node, ast.Return) or not isinstance(node.value, ast.Call):
            continue
        if _call_name(node.value.func) != "NatalDomainProviderRegistry":
            continue
        providers_node = next(
            (keyword.value for keyword in node.value.keywords if keyword.arg == "providers"),
            None,
        )
        if providers_node is None:
            continue
        for child in ast.walk(providers_node):
            if isinstance(child, ast.Name) and child.id in assigned:
                returned_domains.add(assigned[child.id])
            elif isinstance(child, ast.Call):
                match = provider_pattern.match(_call_name(child.func))
                if match:
                    returned_domains.add(match.group(1))
    return tuple(sorted(returned_domains))


def _literal_assignments(source: str) -> dict[str, Any]:
    """Read only simple literal module constants; never execute repository code."""
    try:
        module = ast.parse(source)
    except SyntaxError:
        return {}
    result: dict[str, Any] = {}
    for node in module.body:
        if not isinstance(node, ast.Assign):
            continue
        try:
            value = ast.literal_eval(node.value)
        except (ValueError, TypeError, SyntaxError):
            continue
        for target in node.targets:
            if isinstance(target, ast.Name):
                result[target.id] = value
    return result


@dataclass(frozen=True)
class ProviderDiscovery:
    domain_id: str
    provider_id: str
    source_path: str
    source_blob_sha: str
    declared_status: str
    time_layer: str
    knowledge_version: str
    rule_count: int
    activation_mode: str
    note: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class MainKnowledgeBundle:
    request: QuickReadRequest
    manifest: CapabilityManifest
    evidence_items: tuple[QuickReadEvidenceItem, ...]
    providers: tuple[ProviderDiscovery, ...]
    reader_report: Mapping[str, Any]

    def build_payload(self, *, chart_context: Mapping[str, Any] | None = None) -> dict[str, Any]:
        return build_quickread_payload(
            self.request,
            self.manifest,
            self.evidence_items,
            chart_context=chart_context,
        )

    def to_dict(self, *, include_payload: bool = True) -> dict[str, Any]:
        result = {
            "request": self.request.to_dict(),
            "manifest": self.manifest.to_dict(),
            "evidence_items": [item.to_dict() for item in self.evidence_items],
            "providers": [item.to_dict() for item in self.providers],
            "reader_report": dict(self.reader_report),
        }
        if include_payload:
            result["payload"] = self.build_payload()
        return result


def _truthy(value: Any) -> bool:
    return str(value or "").strip().lower() in {"1", "true", "yes", "y"}


def _is_direct_visual_review_note(note: str) -> bool:
    """Accept repository review-note variants while rejecting explicit negation.

    The structured ledger source_basis is the primary gate. Record notes in
    accepted main ledgers use both “直接目视核对” and “直接目视检查”, and
    older batches use English “Direct visual review”. A negated phrase must
    never pass just because it contains one of the positive markers.
    """
    normalized = str(note or "").strip()
    folded = normalized.casefold()
    positive_markers = (
        "直接目视核对",
        "直接目视检查",
        "直接目视复核",
        "direct visual review",
        "direct visual inspection",
    )
    if not any(marker in folded for marker in positive_markers):
        return False
    negative_markers = (
        "不是直接目视核对",
        "并非直接目视核对",
        "未直接目视核对",
        "没有直接目视核对",
        "非直接目视核对",
        "不属于直接目视核对",
        "未进行直接目视核对",
        "不是直接目视检查",
        "并非直接目视检查",
        "未直接目视检查",
        "没有直接目视检查",
        "非直接目视检查",
        "未进行直接目视检查",
        "not direct visual review",
        "not a direct visual review",
        "no direct visual review",
        "direct visual review was not performed",
        "direct visual review not performed",
        "not direct visual inspection",
        "no direct visual inspection",
        "not directly visually reviewed",
    )
    return not any(marker in folded for marker in negative_markers)


def _provider_paths(
    tree: Mapping[str, Mapping[str, Any]], domains: set[str]
) -> tuple[list[str], list[str]]:
    """Select the highest declared provider version per requested domain.

    Older versioned files remain in Git history/main for auditability. If two
    different files claim the same highest version, fail closed rather than
    choosing one based on lexical path order.
    """
    selected: list[str] = []
    superseded: list[str] = []
    version_pattern = re.compile(r"_DOMAIN_PROVIDER_v([0-9]+(?:\.[0-9]+)*)\.json$", re.IGNORECASE)
    for domain in sorted(domains):
        candidates: list[tuple[tuple[int, ...], str]] = []
        for path in tree:
            if not path.startswith("product/PL3N_") or not path.lower().endswith(".json"):
                continue
            if f"_{domain.upper()}_DOMAIN_PROVIDER_V" not in path.upper():
                continue
            match = version_pattern.search(path)
            if match is None:
                continue
            candidates.append((tuple(int(part) for part in match.group(1).split(".")), path))
        if not candidates:
            continue
        highest = max(version for version, _ in candidates)
        latest = sorted(path for version, path in candidates if version == highest)
        if len(latest) != 1:
            raise MainKnowledgeUnavailable(
                f"multiple Product provider files claim the latest {domain} version: {latest}"
            )
        selected.append(latest[0])
        superseded.extend(path for version, path in candidates if version < highest)
    return sorted(selected), sorted(superseded)


def _source_ledger_paths(
    tree: Mapping[str, Mapping[str, Any]], domains: set[str]
) -> list[str]:
    codes = {_palace_code(domain) for domain in domains}
    codes.discard(None)
    candidates = []
    for path in tree:
        if not path.startswith("knowledge/palaces/") or "/wp05/" not in path:
            continue
        if "SOURCE_READJUDICATION" not in path.upper() or not path.lower().endswith(".json"):
            continue
        if any(re.search(rf"/{code}_[^/]+/", path) for code in codes):
            candidates.append(path)
    return sorted(candidates)


def _supported_source_ledger(artifact: Mapping[str, Any]) -> bool:
    source_basis = artifact.get("source_basis")
    records = artifact.get("records")
    return (
        artifact.get("status") == SUPPORTED_SOURCE_LEDGER_STATUS
        and isinstance(source_basis, Mapping)
        and source_basis.get("verification_method") == SUPPORTED_SOURCE_REVIEW_METHOD
        and bool(str(source_basis.get("source_id", "")).strip())
        and isinstance(records, list)
    )


def _parse_source_ledger(
    artifact: Mapping[str, Any],
    *,
    path: str,
    main_sha: str,
    requested_slots: Sequence[QuickReadScopeSlot],
    question: str,
) -> tuple[dict[str, list[tuple[QuickReadEvidenceItem, int]]], dict[str, int]]:
    counters = {
        "records_seen": 0,
        "records_eligible_pre_batch": 0,
        "excluded_not_promoted": 0,
        "excluded_case_only": 0,
        "excluded_uncertain_or_unverified": 0,
        "excluded_layer_mismatch": 0,
        "excluded_missing_provenance": 0,
    }
    output: dict[str, list[tuple[QuickReadEvidenceItem, int]]] = {
        slot.slot_id: [] for slot in requested_slots
    }
    if not _supported_source_ledger(artifact):
        return output, counters
    source_basis = artifact["source_basis"]
    source_id = str(source_basis["source_id"]).strip()
    records = artifact["records"]

    artifact_id = str(artifact.get("artifact_id", path.rsplit("/", 1)[-1])).strip()
    for record in records:
        if not isinstance(record, Mapping):
            counters["excluded_uncertain_or_unverified"] += 1
            continue
        counters["records_seen"] += 1
        if record.get("canonical_promotion") is not True:
            counters["excluded_not_promoted"] += 1
            continue
        if record.get("case_support_only") is not False:
            counters["excluded_case_only"] += 1
            continue
        disposition = str(record.get("disposition", "")).strip().upper()
        if disposition.startswith("HOLD") or "UNRESOLVED" in disposition:
            counters["excluded_not_promoted"] += 1
            continue
        if (
            record.get("source_condition_normalized") is not True
            or record.get("source_span_changed") is not False
            or "source_condition_uncertainty" not in record
            or record.get("source_condition_uncertainty") not in (None, "")
        ):
            counters["excluded_uncertain_or_unverified"] += 1
            continue
        source_note = str(record.get("source_note", "")).strip()
        source_location = str(record.get("source_location", "")).strip()
        condition = str(record.get("canonical_condition", "")).strip()
        target = str(record.get("canonical_projection_target", "")).strip()
        projection_domain = str(record.get("canonical_projection_domain", "")).strip()
        rule_key = str(record.get("projection_rule_id", "")).strip()
        if (
            not _is_direct_visual_review_note(source_note)
            or not source_location
            or not condition
            or not target
            or not rule_key
        ):
            counters["excluded_missing_provenance"] += 1
            continue

        layer = str(record.get("primary_time_layer", "")).strip().upper()
        matching_slots = [
            slot for slot in requested_slots
            if _normalize_domain(slot.domain) in {
                _normalize_domain(str(artifact.get("palace", ""))),
                _normalize_domain(str(artifact.get("shard", ""))),
            }
            and slot.temporal_layer.upper() == layer
        ]
        # The source-review adapter currently supports one namespace per row.
        # A temporal response/manifestation slot needs both canonical and temporal
        # evidence, so a single ledger row must not satisfy it by itself.
        matching_slots = [
            slot for slot in matching_slots
            if not (
                slot.temporal_layer.upper() != "NATAL"
                and any(token in slot.capability_kind.upper() for token in ("RESPONSE", "MANIFESTATION"))
            )
        ]
        if not matching_slots:
            counters["excluded_layer_mismatch"] += 1
            continue

        namespace = "CANONICAL" if layer == "NATAL" else "TEMPORAL"
        claim = (
            f"来源复核条件：{condition}；"
            f"解释性投影：{projection_domain or '未标注领域'} → {target}。"
            "此记录仅为来源支持材料，不代表规则已编译或解锁。"
        )
        reference = EvidenceSourceRef(
            source_id=source_id,
            source_location=source_location,
            review_status=SOURCE_REVIEW_STATUS,
            allowed_use="SEMANTIC_ONLY",
            namespace=namespace,
            time_layer=layer,
        )
        for slot in matching_slots:
            evidence = QuickReadEvidenceItem(
                evidence_id=f"{main_sha[:12]}:{artifact_id}:{rule_key}:{slot.slot_id}",
                slot_id=slot.slot_id,
                lane="SOURCE",
                claim=claim,
                source_refs=(reference,),
                epistemic_label="SOURCE_GROUNDED",
            )
            score = _relevance_score(
                slot.domain,
                question,
                claim,
                slot_domain=_normalize_domain(slot.domain),
            )
            output[slot.slot_id].append((evidence, score))
            counters["records_eligible_pre_batch"] += 1

    for slot_id, candidates in output.items():
        unique: dict[str, tuple[QuickReadEvidenceItem, int]] = {}
        for item, score in candidates:
            unique[item.evidence_id] = (item, score)
        output[slot_id] = sorted(
            unique.values(), key=lambda pair: (-pair[1], pair[0].evidence_id)
        )
    return output, counters


def _relevance_score(domain: str, question: str, claim: str, *, slot_domain: str) -> int:
    text = f"{question} {claim}".lower()
    terms = set(DOMAIN_QUERY_TERMS.get(slot_domain, ()))
    terms.update(DOMAIN_QUERY_TERMS.get(_normalize_domain(domain), ()))
    return sum(1 for term in terms if term and term.lower() in text)


def _provider_summary(
    path: str,
    artifact: Mapping[str, Any],
    blob_sha: str,
    default_domains: set[str],
) -> ProviderDiscovery:
    domain_id = _normalize_domain(str(artifact.get("domain_id", "")))
    status = str(artifact.get("status", "")).strip() or "PRODUCT_PROVIDER_PRESENT"
    layer = str(artifact.get("time_layer", "")).strip().upper() or "UNKNOWN"
    knowledge_version = str(artifact.get("knowledge_version", "")).strip() or "UNKNOWN"
    rules = artifact.get("rules")
    if isinstance(rules, Mapping):
        rule_count = len(rules)
    else:
        try:
            rule_count = int(artifact.get("expected_executable_rules", 0))
        except (TypeError, ValueError):
            rule_count = 0
    active = domain_id in default_domains
    if active:
        activation = "DEFAULT_RUNTIME"
        note = "The accepted main runtime registry includes this domain by default; no chart-specific rule has been executed by the reader."
    else:
        activation = "OPT_IN_OR_NOT_DEFAULT"
        note = "A provider file exists on main, but the default runtime registry does not activate this domain. The reader will not silently enable it."
    return ProviderDiscovery(
        domain_id=domain_id,
        provider_id=str(artifact.get("provider_id", path.rsplit("/", 1)[-1])).strip(),
        source_path=path,
        source_blob_sha=blob_sha,
        declared_status=status,
        time_layer=layer,
        knowledge_version=knowledge_version,
        rule_count=rule_count,
        activation_mode=activation,
        note=note,
    )


def _wealth_runtime_rules(
    *,
    provider: Mapping[str, Any],
    tree: Mapping[str, Mapping[str, Any]],
    main_sha: str,
    fetch_artifact: Callable[[str], bytes],
    runtime_source: str,
) -> tuple[tuple[str, ...], tuple[EvidenceSourceRef, ...], tuple[str, ...]]:
    declared_status = str(provider.get("status", "")).strip()
    if declared_status and declared_status != "CANONICAL_READY":
        raise MainKnowledgeUnavailable(
            f"Wealth provider is not declared CANONICAL_READY: {declared_status}"
        )
    constants = _literal_assignments(runtime_source)
    code_projection = constants.get("DEFAULT_WEALTH_PROJECTION_PATH")
    code_batches = constants.get("DEFAULT_WEALTH_BATCH_PATHS")
    code_ontology = constants.get("DEFAULT_PALACE_ONTOLOGY_PATH")
    if not isinstance(code_projection, str) or not isinstance(code_batches, (list, tuple)):
        raise MainKnowledgeUnavailable("cannot verify Wealth runtime input paths from main code")
    metadata_batches = provider.get("batch_paths")
    if (
        code_projection != provider.get("projection_source")
        or list(code_batches) != metadata_batches
        or not isinstance(code_ontology, str)
    ):
        raise MainKnowledgeUnavailable("Wealth Product metadata and runtime input paths drifted")
    if code_ontology not in tree:
        raise MainKnowledgeUnavailable("Wealth runtime palace ontology is absent from main tree")

    rule_specs: dict[str, Mapping[str, Any]] = {}
    for path in code_batches:
        if path not in tree:
            raise MainKnowledgeUnavailable(f"Wealth runtime batch is missing from main: {path}")
        batch = json.loads(fetch_artifact(path).decode("utf-8"))
        rules = batch.get("rules")
        policy = batch.get("policy")
        if (
            batch.get("schema_version") != "0.1"
            or batch.get("palace_id") != "P05"
            or not isinstance(rules, Mapping)
            or not isinstance(policy, Mapping)
            or policy.get("source_review_required", SOURCE_REVIEW_STATUS) != SOURCE_REVIEW_STATUS
            or policy.get("case_support_only_allowed", False) is not False
            or policy.get("normalization_verified") is not True
            or str(policy.get("time_layer", "NATAL")).strip().upper() != "NATAL"
        ):
            raise MainKnowledgeUnavailable(f"Wealth batch fails the accepted runtime contract: {path}")
        for rule_id, spec in rules.items():
            if not isinstance(spec, Mapping):
                raise MainKnowledgeUnavailable(f"Wealth rule is not an object: {rule_id}")
            if rule_id in rule_specs and rule_specs[rule_id] != spec:
                raise MainKnowledgeUnavailable(f"Conflicting Wealth rule definitions: {rule_id}")
            rule_specs[str(rule_id)] = spec

    expected = int(provider.get("expected_executable_rules", 0))
    if not expected or len(rule_specs) != expected:
        raise MainKnowledgeUnavailable(
            f"Wealth runtime rule count mismatch: found {len(rule_specs)}, expected {expected}"
        )
    if code_projection not in tree:
        raise MainKnowledgeUnavailable("Wealth projection source is absent from main tree")
    csv_text = fetch_artifact(code_projection).decode("utf-8-sig")
    rows = list(csv.DictReader(io.StringIO(csv_text)))
    row_by_id: dict[str, Mapping[str, str]] = {}
    for row in rows:
        rule_id = str(row.get("projection_rule_id", "")).strip()
        if rule_id:
            if rule_id in row_by_id:
                raise MainKnowledgeUnavailable(f"duplicate Wealth projection rule ID: {rule_id}")
            row_by_id[rule_id] = row

    refs: dict[tuple[str, str, str, str, str, str], EvidenceSourceRef] = {}
    for rule_id in sorted(rule_specs):
        row = row_by_id.get(rule_id)
        if row is None:
            raise MainKnowledgeUnavailable(f"Wealth runtime rule has no source row: {rule_id}")
        review = str(row.get("review_status", "")).strip().upper()
        if (
            review not in {"SOURCE_SPAN_VERIFIED", "HUMAN_VERIFIED"}
            or not _truthy(row.get("source_span_verified"))
            or _truthy(row.get("case_support_only"))
            or str(row.get("time_layer", "")).strip().upper() != "NATAL"
        ):
            raise MainKnowledgeUnavailable(f"Wealth runtime source row is not executable: {rule_id}")
        reference = EvidenceSourceRef(
            source_id=str(row.get("source_id", "")).strip(),
            source_location=str(row.get("source_location", "")).strip(),
            review_status=review,
            allowed_use="EXECUTABLE",
            namespace="CANONICAL",
            time_layer="NATAL",
        )
        refs[reference.identity()] = reference
    input_paths = tuple(sorted({code_projection, code_ontology, *code_batches}))
    return tuple(sorted(rule_specs)), tuple(refs[key] for key in sorted(refs)), input_paths


def load_latest_main_knowledge(
    request: QuickReadRequest,
    *,
    fetch_bytes: FetchBytes | None = None,
    timeout_seconds: float = DEFAULT_TIMEOUT_SECONDS,
    source_items_per_slot: int = DEFAULT_FIRST_PASS_SOURCE_ITEMS_PER_SLOT,
    continuation: Mapping[str, Any] | None = None,
    repository_root: str | Path | None = None,
) -> MainKnowledgeBundle:
    """Load a scoped, version-pinned view of accepted artifacts from GitHub main.

    Each call resolves main to one commit SHA and reads all selected files by
    that immutable SHA. Network errors, truncated trees, oversized files, blob
    mismatches, or unsupported schemas fail closed; the reader never silently
    falls back to model memory or a stale local checkout.
    """
    if not isinstance(request, QuickReadRequest):
        raise ValueError("request must be a QuickReadRequest")
    if (
        source_items_per_slot < 1
        or source_items_per_slot > MAX_SOURCE_ITEMS_PER_BATCH_PER_SLOT
    ):
        raise ValueError(
            "source_items_per_slot must be between 1 and "
            f"{MAX_SOURCE_ITEMS_PER_BATCH_PER_SLOT}"
        )

    continuation_main_sha: str | None = None
    seen_evidence_ids: set[str] = set()
    if continuation is not None:
        if not isinstance(continuation, Mapping):
            raise ValueError("continuation must be a mapping")
        continuation_main_sha = str(continuation.get("main_sha", "")).strip()
        if not re.fullmatch(r"[0-9a-f]{40}", continuation_main_sha):
            raise ValueError("continuation.main_sha must be a 40-character Git SHA")
        raw_slot_ids = continuation.get("requested_slot_ids")
        if (
            not isinstance(raw_slot_ids, list)
            or not all(isinstance(item, str) and item.strip() for item in raw_slot_ids)
            or len(raw_slot_ids) != len(set(raw_slot_ids))
        ):
            raise ValueError("continuation.requested_slot_ids must be a unique string list")
        current_slot_ids = sorted(slot.slot_id for slot in request.requested_slots)
        if sorted(raw_slot_ids) != current_slot_ids:
            raise ValueError("continuation requested scope does not match the current request")
        raw_seen_ids = continuation.get("seen_evidence_ids")
        if (
            not isinstance(raw_seen_ids, list)
            or not all(isinstance(item, str) and item.strip() for item in raw_seen_ids)
            or len(raw_seen_ids) != len(set(raw_seen_ids))
        ):
            raise ValueError("continuation.seen_evidence_ids must be a unique string list")
        if len(raw_seen_ids) > 10_000:
            raise ValueError("continuation.seen_evidence_ids exceeds the safety limit")
        seen_evidence_ids = {item.strip() for item in raw_seen_ids}

    transport = fetch_bytes or _default_fetch_bytes
    total_bytes = 0

    def read(url: str, limit: int) -> bytes:
        nonlocal total_bytes
        try:
            data = transport(url, timeout_seconds, limit)
        except MainKnowledgeUnavailable:
            raise
        except Exception as exc:
            raise MainKnowledgeUnavailable(f"GitHub main read failed: {type(exc).__name__}") from exc
        if not isinstance(data, bytes):
            raise MainKnowledgeUnavailable("transport must return bytes")
        if len(data) > limit:
            raise MainKnowledgeUnavailable(f"response exceeds configured limit: {url}")
        total_bytes += len(data)
        if total_bytes > MAX_TOTAL_FETCH_BYTES:
            raise MainKnowledgeUnavailable("QuickRead main read exceeded total byte budget")
        return data

    def json_from_url(url: str, limit: int) -> dict[str, Any]:
        try:
            value = json.loads(read(url, limit).decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise MainKnowledgeUnavailable(f"invalid JSON response: {url}") from exc
        if not isinstance(value, dict):
            raise MainKnowledgeUnavailable(f"expected JSON object: {url}")
        return value

    commit = json_from_url(f"{API_ROOT}/commits/main", 512_000)
    main_sha = str(commit.get("sha", "")).strip()
    if not re.fullmatch(r"[0-9a-f]{40}", main_sha):
        raise MainKnowledgeUnavailable("GitHub did not return a valid main commit SHA")
    if continuation_main_sha is not None and continuation_main_sha != main_sha:
        raise MainKnowledgeUnavailable(
            "QuickRead continuation is stale because GitHub main changed; "
            "start a fresh first-pass read on the new main snapshot"
        )
    tree_payload = json_from_url(f"{API_ROOT}/git/trees/{main_sha}?recursive=1", MAX_API_BYTES)
    if tree_payload.get("truncated") is True:
        raise MainKnowledgeUnavailable("main Git tree is truncated; refusing an incomplete knowledge scan")
    raw_entries = tree_payload.get("tree")
    if not isinstance(raw_entries, list):
        raise MainKnowledgeUnavailable("GitHub main tree has no valid tree list")
    tree: dict[str, dict[str, Any]] = {}
    for entry in raw_entries:
        if not isinstance(entry, Mapping) or entry.get("type") != "blob":
            continue
        path = str(entry.get("path", "")).strip()
        sha = str(entry.get("sha", "")).strip()
        if path and re.fullmatch(r"[0-9a-f]{40}", sha):
            tree[path] = dict(entry)
    tree_sha = str(tree_payload.get("sha", "")).strip()

    def fetch_artifact(path: str) -> bytes:
        entry = tree.get(path)
        if entry is None:
            raise MainKnowledgeUnavailable(f"selected artifact is absent from pinned main: {path}")
        try:
            size = int(entry.get("size", 0))
        except (TypeError, ValueError):
            size = 0
        if size < 0 or size > MAX_ARTIFACT_BYTES:
            raise MainKnowledgeUnavailable(f"selected artifact exceeds size limit: {path}")
        url = f"{RAW_ROOT}/{main_sha}/{quote(path, safe='/')}"
        content = read(url, MAX_ARTIFACT_BYTES)
        expected_sha = str(entry["sha"])
        if _git_blob_sha(content) != expected_sha:
            raise MainKnowledgeUnavailable(f"Git blob SHA mismatch for pinned main artifact: {path}")
        return content

    def fetch_json_artifact(path: str) -> dict[str, Any]:
        try:
            value = json.loads(fetch_artifact(path).decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise MainKnowledgeUnavailable(f"invalid JSON artifact on main: {path}") from exc
        if not isinstance(value, dict):
            raise MainKnowledgeUnavailable(f"expected JSON object on main: {path}")
        return value

    registry_path = "src/product/natal_domain_registry.py"
    default_domains: set[str] = set()
    if registry_path in tree:
        registry_source = fetch_artifact(registry_path).decode("utf-8")
        default_domains = set(_default_runtime_domains(registry_source))
    else:
        registry_source = ""
    runtime_source_path = "src/product/natal_domain_providers.py"
    runtime_source = (
        fetch_artifact(runtime_source_path).decode("utf-8")
        if runtime_source_path in tree
        else ""
    )
    runtime_parts = [
        f"{path}:{entry['sha']}"
        for path, entry in tree.items()
        if path.startswith("src/product/") and path.endswith(".py")
    ]
    runtime_version = "PRODUCT_RUNTIME_SHA256:" + _sha256_digest(runtime_parts)[:20]
    local_runtime_matches_main = False
    if repository_root is not None:
        root = Path(repository_root).resolve()
        local_runtime_matches_main = _default_checkout_matches_main(root, main_sha)

    requested_domains = {_normalize_domain(slot.domain) for slot in request.requested_slots}
    provider_paths, superseded_provider_paths = _provider_paths(tree, requested_domains)
    provider_objects: dict[str, tuple[str, dict[str, Any]]] = {}
    provider_summaries: list[ProviderDiscovery] = []
    for path in provider_paths:
        artifact = fetch_json_artifact(path)
        domain_id = _normalize_domain(str(artifact.get("domain_id", "")))
        if domain_id not in requested_domains:
            continue
        summary = _provider_summary(path, artifact, str(tree[path]["sha"]), default_domains)
        # If duplicate provider files exist, do not silently choose a version.
        if domain_id in provider_objects:
            raise MainKnowledgeUnavailable(f"multiple Product providers found for domain {domain_id}")
        provider_objects[domain_id] = (path, artifact)
        provider_summaries.append(summary)

    # Source-first ledgers are read only for the requested palace(s). Other
    # Knowledge formats are intentionally not guessed or auto-promoted.
    ledger_paths = _source_ledger_paths(tree, requested_domains)
    all_candidates: dict[str, list[tuple[QuickReadEvidenceItem, int]]] = {
        slot.slot_id: [] for slot in request.requested_slots
    }
    aggregate = {
        "ledger_files_discovered": len(ledger_paths),
        "ledger_files_accepted": 0,
        "records_seen": 0,
        "records_eligible_pre_batch": 0,
        "excluded_not_promoted": 0,
        "excluded_case_only": 0,
        "excluded_uncertain_or_unverified": 0,
        "excluded_layer_mismatch": 0,
        "excluded_missing_provenance": 0,
    }
    loaded_paths: list[str] = []
    for path in ledger_paths:
        artifact = fetch_json_artifact(path)
        if _supported_source_ledger(artifact):
            aggregate["ledger_files_accepted"] += 1
            loaded_paths.append(path)
        candidates, counts = _parse_source_ledger(
            artifact,
            path=path,
            main_sha=main_sha,
            requested_slots=request.requested_slots,
            question=request.question,
        )
        for slot_id, items in candidates.items():
            all_candidates[slot_id].extend(items)
        for key, value in counts.items():
            aggregate[key] += value

    selected_items: list[QuickReadEvidenceItem] = []
    source_refs_by_slot: dict[str, tuple[EvidenceSourceRef, ...]] = {}
    selected_count_by_slot: dict[str, int] = {}
    total_eligible_by_slot: dict[str, int] = {}
    already_seen_by_slot: dict[str, int] = {}
    remaining_after_batch_by_slot: dict[str, int] = {}
    next_seen_evidence_ids = set(seen_evidence_ids)
    for slot in request.requested_slots:
        unique: dict[str, tuple[QuickReadEvidenceItem, int]] = {}
        for item, score in all_candidates[slot.slot_id]:
            unique[item.evidence_id] = (item, score)
        ordered = sorted(unique.values(), key=lambda pair: (-pair[1], pair[0].evidence_id))
        ordered_items = [item for item, _ in ordered]
        unread = [
            item for item in ordered_items
            if item.evidence_id not in seen_evidence_ids
        ]
        selected = unread[:source_items_per_slot]
        next_seen_evidence_ids.update(item.evidence_id for item in selected)
        selected_items.extend(selected)
        refs_by_identity = {
            ref.identity(): ref
            for item in selected
            for ref in item.source_refs
        }
        source_refs_by_slot[slot.slot_id] = tuple(
            refs_by_identity[key] for key in sorted(refs_by_identity)
        )
        selected_count_by_slot[slot.slot_id] = len(selected)
        total_eligible_by_slot[slot.slot_id] = len(ordered_items)
        already_seen_by_slot[slot.slot_id] = sum(
            1 for item in ordered_items if item.evidence_id in seen_evidence_ids
        )
        remaining_after_batch_by_slot[slot.slot_id] = max(
            0, len(unread) - len(selected)
        )

    # Build the actual runtime-capability manifest. A provider counts as
    # executable only if the current-main runtime registry activates it and
    # the accepted runtime input files reconcile to reviewed, non-case rows.
    runtime_rules_by_domain: dict[str, tuple[tuple[str, ...], tuple[EvidenceSourceRef, ...]]] = {}
    runtime_input_paths_by_domain: dict[str, tuple[str, ...]] = {}
    runtime_blockers: dict[str, str] = {}
    for domain in requested_domains.intersection(default_domains):
        provider_entry = provider_objects.get(domain)
        if provider_entry is None:
            runtime_blockers[domain] = "Default runtime domain has no matching discovered Product provider file."
            continue
        provider_path, provider_artifact = provider_entry
        try:
            if domain == "wealth":
                rules, refs, input_paths = _wealth_runtime_rules(
                    provider=provider_artifact,
                    tree=tree,
                    main_sha=main_sha,
                    fetch_artifact=fetch_artifact,
                    runtime_source=runtime_source,
                )
                runtime_rules_by_domain[domain] = (rules, refs)
                runtime_input_paths_by_domain[domain] = tuple(sorted({provider_path, *input_paths}))
            else:
                runtime_blockers[domain] = (
                    f"No domain-specific runtime manifest adapter is implemented for {provider_path}; "
                    "provider discovery is not enough to assert executable capability."
                )
        except (MainKnowledgeUnavailable, ValueError, TypeError) as exc:
            runtime_blockers[domain] = str(exc)

    runtime_inputs_match_main: dict[str, bool] = {}
    if repository_root is not None and local_runtime_matches_main:
        root = Path(repository_root).resolve()
        for domain, paths in runtime_input_paths_by_domain.items():
            matches = True
            for path in paths:
                entry = tree.get(path)
                local_path = root / path
                try:
                    if entry is None or not local_path.is_file() or _git_blob_sha(local_path.read_bytes()) != str(entry["sha"]):
                        matches = False
                        break
                except OSError:
                    matches = False
                    break
            runtime_inputs_match_main[domain] = matches
    else:
        runtime_inputs_match_main = {domain: False for domain in runtime_input_paths_by_domain}

    records: list[CapabilityRecord] = []
    for slot in request.requested_slots:
        domain = _normalize_domain(slot.domain)
        runtime_rules, runtime_refs = runtime_rules_by_domain.get(domain, ((), ()))
        runtime_available = (
            local_runtime_matches_main
            and runtime_inputs_match_main.get(domain, False)
            and slot.temporal_layer.upper() == "NATAL"
            and domain in default_domains
            and bool(runtime_rules)
            and bool(runtime_refs)
        )
        if runtime_available:
            runtime_status = "AVAILABLE"
            rule_ids = runtime_rules
            executable_refs = runtime_refs
        else:
            runtime_status = "NOT_AVAILABLE"
            rule_ids = ()
            executable_refs = ()
        source_refs = source_refs_by_slot[slot.slot_id]
        source_status = "AVAILABLE" if source_refs else "NOT_AVAILABLE"
        if runtime_available:
            reason = "Current main and the local runtime source files match, and main declares a default NATAL provider; this reader has not executed chart-specific rules."
        elif domain in default_domains and domain in runtime_rules_by_domain and not local_runtime_matches_main:
            reason = "Main declares this default provider, but the local checkout is absent, dirty, or not at the exact main SHA; executable capability is not asserted."
        elif domain in default_domains and domain in runtime_rules_by_domain and not runtime_inputs_match_main.get(domain, False):
            reason = "The local runtime checkout is at main, but one or more provider/source input files do not match the pinned main snapshot; executable capability is not asserted."
        elif domain in provider_objects and domain not in default_domains:
            reason = "A Product provider exists on main but is opt-in/not in the default runtime; it was not auto-enabled."
        elif slot.temporal_layer.upper() != "NATAL":
            reason = "No accepted temporal runtime provider is declared by the current default runtime registry."
        elif domain in runtime_blockers:
            reason = runtime_blockers[domain]
        elif source_refs:
            reason = "Reviewed source-only evidence is available; no matching default runtime provider was activated."
        else:
            reason = "No supported source ledger or default runtime provider was found for this requested scope."
        records.append(
            CapabilityRecord(
                slot=slot,
                runtime_status=runtime_status,
                source_status=source_status,
                runtime_rule_ids=rule_ids,
                runtime_source_refs=executable_refs,
                source_refs=source_refs,
                reason=reason,
            )
        )

    knowledge_paths = {
        path for path in tree
        if path.startswith("knowledge/")
        or (path.startswith("product/PL3N_") and "_DOMAIN_PROVIDER_v" in path)
    }
    for provider_path, provider_artifact in provider_objects.values():
        for path_key in ("projection_source", "palace_ontology"):
            value = provider_artifact.get(path_key)
            if isinstance(value, str) and value in tree:
                knowledge_paths.add(value)
        for path_key in ("batch_paths",):
            values = provider_artifact.get(path_key)
            if isinstance(values, list):
                knowledge_paths.update(value for value in values if isinstance(value, str) and value in tree)
        for meta in [provider_artifact.get("source_mapping"), *(provider_artifact.get("additional_source_mappings") or [])]:
            if isinstance(meta, Mapping):
                value = meta.get("path")
                if isinstance(value, str) and value in tree:
                    knowledge_paths.add(value)
    knowledge_paths.update(
        path for paths in runtime_input_paths_by_domain.values() for path in paths if path in tree
    )
    knowledge_parts = [f"{path}:{tree[path]['sha']}" for path in knowledge_paths]
    knowledge_version = "MAIN_KNOWLEDGE_SHA256:" + _sha256_digest(knowledge_parts)[:20]

    manifest = CapabilityManifest(
        main_sha=main_sha,
        knowledge_version=knowledge_version,
        runtime_version=runtime_version,
        records=tuple(records),
    )
    slot_report = []
    for slot in request.requested_slots:
        record = next(item for item in records if item.slot.slot_id == slot.slot_id)
        provider = next(
            (item for item in provider_summaries if item.domain_id == _normalize_domain(slot.domain)),
            None,
        )
        slot_report.append(
            {
                "slot_id": slot.slot_id,
                "domain": slot.domain,
                "temporal_layer": slot.temporal_layer,
                "runtime_status": record.runtime_status,
                "runtime_rule_count": len(record.runtime_rule_ids),
                "source_status": record.source_status,
                "source_evidence_total_eligible": total_eligible_by_slot[slot.slot_id],
                "source_evidence_already_seen": already_seen_by_slot[slot.slot_id],
                "source_evidence_selected_this_batch": selected_count_by_slot[slot.slot_id],
                "source_evidence_remaining_after_batch": remaining_after_batch_by_slot[slot.slot_id],
                "provider_discovery": provider.to_dict() if provider else None,
                "reason": record.reason,
            }
        )
    report = {
        "source_of_truth": "GitHub main only",
        "repository": REPOSITORY,
        "main_sha": main_sha,
        "main_commit_url": f"https://github.com/{REPOSITORY}/commit/{main_sha}",
        "tree_sha": tree_sha,
        "knowledge_version": knowledge_version,
        "runtime_version": runtime_version,
        "local_runtime_matches_main": local_runtime_matches_main,
        "runtime_inputs_match_main": runtime_inputs_match_main,
        "runtime_execution_performed": False,
        "default_runtime_domains": sorted(default_domains),
        "loaded_source_ledger_paths": loaded_paths,
        "superseded_provider_paths": superseded_provider_paths,
        "aggregate_source_ledger_counts": aggregate,
        "source_adapter": "SOURCE_READJUDICATION_LEDGER_V0_1",
        "source_batch_limit_per_slot": source_items_per_slot,
        "source_items_total_eligible_by_slot": total_eligible_by_slot,
        "source_items_already_seen_by_slot": already_seen_by_slot,
        "source_items_selected_this_batch_by_slot": selected_count_by_slot,
        "source_items_remaining_after_batch_by_slot": remaining_after_batch_by_slot,
        "continuation": {
            "main_sha": main_sha,
            "requested_slot_ids": sorted(
                slot.slot_id for slot in request.requested_slots
            ),
            "seen_evidence_ids": sorted(next_seen_evidence_ids),
            "has_more": any(remaining_after_batch_by_slot.values()),
        },
        "slots": slot_report,
        "limitations": [
            "No LLM/model API call is made; this reader does make read-only GitHub API requests for the pinned main snapshot and returns a source-pinned payload for a caller.",
            "Source-review ledgers are retrieval/semantic support only, never proof of runtime execution.",
            "CASE_SUPPORT_ONLY, held, uncertain, unreviewed, and temporally mismatched records are excluded.",
            "Only the recognized source-first palace ledger format is ingested in v0.1; other Knowledge formats remain unavailable until an explicit adapter is accepted.",
            "A provider marked OPT_IN_OR_NOT_DEFAULT is reported but is not silently activated.",
            "The reader does not use unmerged branches, PR files, Issue text, archived drafts, or model memory as accepted knowledge.",
            "No source ledger by itself authorizes probabilities, empirical validity, or specific-period event claims.",
            "The per-slot source item limit is a per-call batch budget, not a session/global cap; callers may continue from the returned main-pinned cursor while has_more is true.",
        ],
        "bytes_fetched": total_bytes,
    }
    return MainKnowledgeBundle(
        request=request,
        manifest=manifest,
        evidence_items=tuple(selected_items),
        providers=tuple(sorted(provider_summaries, key=lambda item: item.domain_id)),
        reader_report=report,
    )


def _build_cli_request(args: argparse.Namespace) -> QuickReadRequest:
    domain = args.domain
    layer = args.layer.upper()
    kind = args.capability_kind
    namespaces = ("CANONICAL",) if layer == "NATAL" else (
        ("CANONICAL", "TEMPORAL")
        if any(token in kind.upper() for token in ("RESPONSE", "MANIFESTATION"))
        else ("TEMPORAL",)
    )
    slot = QuickReadScopeSlot(
        slot_id=f"{_normalize_domain(domain)}_{layer.lower()}",
        domain=domain,
        temporal_layer=layer,
        capability_kind=kind,
        required_namespaces=namespaces,
    )
    return QuickReadRequest(
        question=args.question,
        target_id="QUICKREAD-DISCOVERY-ONLY",
        requested_slots=(slot,),
        mode=args.mode,
        min_chars=args.min_chars,
        max_chars=args.max_chars,
    )


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Read the latest accepted QuickRead knowledge from GitHub main.")
    parser.add_argument("--domain", required=True, help="e.g. wealth, career, relationship")
    parser.add_argument("--layer", default="NATAL", choices=("NATAL", "DECADE", "YEAR", "MONTH", "DAY", "HOUR"))
    parser.add_argument("--capability-kind", default="NATAL_STRUCTURE")
    parser.add_argument("--question", required=True)
    parser.add_argument("--mode", default="SOURCE_FIRST", choices=("HYBRID", "AUDIT", "SOURCE_FIRST"))
    parser.add_argument("--min-chars", type=int, default=120)
    parser.add_argument("--max-chars", type=int, default=220)
    parser.add_argument(
        "--source-items-per-slot",
        type=int,
        default=DEFAULT_FIRST_PASS_SOURCE_ITEMS_PER_SLOT,
        help="Per-call source evidence batch size; continuation can fetch later batches.",
    )
    args = parser.parse_args(argv)
    try:
        bundle = load_latest_main_knowledge(
            _build_cli_request(args),
            source_items_per_slot=args.source_items_per_slot,
            repository_root=Path(__file__).resolve().parents[2],
        )
    except MainKnowledgeUnavailable as exc:
        parser.exit(2, f"QuickRead main read unavailable: {exc}\n")
    print(json.dumps(bundle.to_dict(), ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
