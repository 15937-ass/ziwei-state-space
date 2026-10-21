"""Content-addressed Product Knowledge Input Bundle and active lock v0.1.

This module implements Proposal #491 without changing canonical Ziwei semantics.

Important boundaries:
- Knowledge/main is research truth, not an implicit mutable Product dependency.
- The active Product lock is explicit and never auto-refreshes.
- Artifact bytes and semantic projections are verified separately.
- Unknown semantic contracts fail closed.
- Historical Product artifacts are not rewritten by this module.

v0.1 deliberately uses a conservative production contract: every populated
active-bundle artifact treats exact bytes as semantic. This may over-invalidate
but cannot silently under-invalidate. Narrower canonical-JSON contracts exist
only as tested primitives for the subsequent impact work; they are not used to
promote the active baseline in this work unit.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping, Sequence


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_BUNDLE_PATH = ROOT / "product" / "PRODUCT_KNOWLEDGE_BUNDLE_V0_1.json"
DEFAULT_LOCK_PATH = ROOT / "product" / "PRODUCT_KNOWLEDGE.lock.json"

SCHEMA_VERSION = "0.1"
LOCK_SCHEMA_VERSION = "0.1"

SUPPORTED_COMPONENTS = frozenset(
    {"K_signal", "K_response", "K_manifest", "K_method"}
)
SUPPORTED_SEMANTIC_CONTRACTS = frozenset(
    {
        "JSON_CANONICAL_FULL_V0_1",
        "JSON_RESPONSE_SEMANTICS_NO_PROVENANCE_V0_1",
        "RAW_CONTENT_FULL_V0_1",
    }
)


class KnowledgeLockError(ValueError):
    """Base error for Product Knowledge lock failures."""


class KnowledgeLockMismatchError(KnowledgeLockError):
    """Raised when a governed Product consumer sees lock drift."""


def _sha256_bytes(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def _canonical_json_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def _strip_provenance(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {
            str(key): _strip_provenance(child)
            for key, child in value.items()
            if key != "provenance"
        }
    if isinstance(value, list):
        return [_strip_provenance(child) for child in value]
    return value


def compute_artifact_digest(path: str | Path) -> str:
    """Return the Git blob content address for exact on-disk bytes.

    GitHub's contents API exposes this same blob SHA, so the checked-in lock can
    be generated and independently verified without a second artifact store.
    """

    data = Path(path).read_bytes()
    header = f"blob {len(data)}\0".encode("ascii")
    return "git-sha1:" + hashlib.sha1(header + data).hexdigest()


def compute_semantic_digest(
    path: str | Path,
    semantic_contract: str,
) -> str:
    """Compute the versioned semantic projection digest for one artifact."""

    path = Path(path)
    if semantic_contract not in SUPPORTED_SEMANTIC_CONTRACTS:
        raise KnowledgeLockError(
            f"unsupported semantic contract: {semantic_contract}"
        )

    if semantic_contract == "RAW_CONTENT_FULL_V0_1":
        return compute_artifact_digest(path)

    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise KnowledgeLockError(
            f"{path}: JSON semantic contract requires valid JSON"
        ) from exc

    if semantic_contract == "JSON_RESPONSE_SEMANTICS_NO_PROVENANCE_V0_1":
        payload = _strip_provenance(payload)

    return _sha256_bytes(_canonical_json_bytes(payload))


def _component_projection(
    artifacts: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    projection = []
    for artifact in sorted(
        artifacts,
        key=lambda item: str(item.get("path", "")),
    ):
        projection.append(
            {
                "path": str(artifact.get("path", "")),
                "semantic_contract": str(
                    artifact.get("semantic_contract", "")
                ),
                "semantic_digest": artifact.get("semantic_digest"),
            }
        )
    return projection


def compute_component_semantic_digest(
    artifacts: Sequence[Mapping[str, Any]],
) -> str:
    return _sha256_bytes(_canonical_json_bytes(_component_projection(artifacts)))


def compute_bundle_semantic_digest(
    components: Sequence[Mapping[str, Any]],
) -> str:
    projection = [
        {
            "component_id": str(component.get("component_id", "")),
            "coverage_status": str(component.get("coverage_status", "")),
            "component_semantic_digest": str(
                component.get("component_semantic_digest", "")
            ),
        }
        for component in sorted(
            components,
            key=lambda item: str(item.get("component_id", "")),
        )
    ]
    return _sha256_bytes(_canonical_json_bytes(projection))


def _required_text(value: Any, field: str) -> str:
    text = str(value or "").strip()
    if not text:
        raise KnowledgeLockError(f"{field} is required")
    return text


def _safe_repo_path(root: Path, relative: str) -> Path:
    if Path(relative).is_absolute():
        raise KnowledgeLockError(f"absolute artifact path forbidden: {relative}")
    candidate = (root / relative).resolve()
    resolved_root = root.resolve()
    if not candidate.is_relative_to(resolved_root):
        raise KnowledgeLockError(f"artifact path escapes repository: {relative}")
    return candidate


def load_bundle(path: str | Path = DEFAULT_BUNDLE_PATH) -> dict[str, Any]:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise KnowledgeLockError("Knowledge Input Bundle must be a JSON object")
    return payload


def load_lock(path: str | Path = DEFAULT_LOCK_PATH) -> dict[str, Any]:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise KnowledgeLockError("Product Knowledge Lock must be a JSON object")
    return payload


def validate_bundle_structure(bundle: Mapping[str, Any]) -> None:
    if str(bundle.get("schema_version", "")) != SCHEMA_VERSION:
        raise KnowledgeLockError("Knowledge Input Bundle schema_version must be 0.1")
    _required_text(bundle.get("bundle_id"), "bundle_id")
    _required_text(bundle.get("source_commit"), "source_commit")
    _required_text(bundle.get("bundle_semantic_digest"), "bundle_semantic_digest")

    components = bundle.get("components")
    if not isinstance(components, list):
        raise KnowledgeLockError("bundle.components must be an array")

    ids = [
        str(item.get("component_id", ""))
        for item in components
        if isinstance(item, Mapping)
    ]
    if set(ids) != SUPPORTED_COMPONENTS or len(ids) != len(SUPPORTED_COMPONENTS):
        raise KnowledgeLockError(
            "bundle must contain exactly K_signal/K_response/K_manifest/K_method"
        )

    seen_paths: set[str] = set()
    for component in components:
        if not isinstance(component, Mapping):
            raise KnowledgeLockError("bundle component must be an object")
        component_id = _required_text(
            component.get("component_id"), "component.component_id"
        )
        _required_text(
            component.get("contract_version"),
            f"{component_id}.contract_version",
        )
        _required_text(
            component.get("coverage_status"),
            f"{component_id}.coverage_status",
        )
        _required_text(
            component.get("component_semantic_digest"),
            f"{component_id}.component_semantic_digest",
        )
        artifacts = component.get("artifacts")
        if not isinstance(artifacts, list):
            raise KnowledgeLockError(f"{component_id}.artifacts must be an array")

        for artifact in artifacts:
            if not isinstance(artifact, Mapping):
                raise KnowledgeLockError(
                    f"{component_id}: artifact must be an object"
                )
            relative = _required_text(
                artifact.get("path"), f"{component_id}.artifact.path"
            )
            if relative in seen_paths:
                raise KnowledgeLockError(
                    f"duplicate artifact path across components: {relative}"
                )
            seen_paths.add(relative)
            _required_text(
                artifact.get("artifact_digest"),
                f"{component_id}.{relative}.artifact_digest",
            )
            contract = _required_text(
                artifact.get("semantic_contract"),
                f"{component_id}.{relative}.semantic_contract",
            )
            if contract not in SUPPORTED_SEMANTIC_CONTRACTS:
                raise KnowledgeLockError(
                    f"{component_id}.{relative}: unsupported semantic contract {contract}"
                )
            _required_text(
                artifact.get("semantic_digest"),
                f"{component_id}.{relative}.semantic_digest",
            )

    expected_bundle_semantic = compute_bundle_semantic_digest(components)
    if bundle.get("bundle_semantic_digest") != expected_bundle_semantic:
        raise KnowledgeLockError(
            "bundle semantic digest does not match component projection"
        )


def validate_lock_structure(lock: Mapping[str, Any]) -> None:
    if str(lock.get("schema_version", "")) != LOCK_SCHEMA_VERSION:
        raise KnowledgeLockError("Product Knowledge Lock schema_version must be 0.1")
    _required_text(lock.get("lock_id"), "lock_id")
    _required_text(lock.get("active_bundle_path"), "active_bundle_path")
    _required_text(lock.get("active_bundle_id"), "active_bundle_id")
    _required_text(lock.get("bundle_artifact_digest"), "bundle_artifact_digest")
    _required_text(lock.get("bundle_semantic_digest"), "bundle_semantic_digest")
    _required_text(lock.get("source_commit"), "source_commit")
    if lock.get("auto_refresh") is not False:
        raise KnowledgeLockError("Product Knowledge Lock auto_refresh must be false")


@dataclass(frozen=True)
class LockFinding:
    code: str
    path: str
    expected: str | None
    actual: str | None

    def to_dict(self) -> dict[str, Any]:
        return {
            "code": self.code,
            "path": self.path,
            "expected": self.expected,
            "actual": self.actual,
        }


def verify_bundle(
    repository_root: str | Path,
    bundle: Mapping[str, Any],
) -> dict[str, Any]:
    root = Path(repository_root).resolve()
    findings: list[LockFinding] = []

    try:
        validate_bundle_structure(bundle)
    except (KnowledgeLockError, TypeError, ValueError) as exc:
        return {
            "status": "FAIL",
            "bundle_id": str(bundle.get("bundle_id", "")),
            "findings": [
                LockFinding(
                    "BUNDLE_STRUCTURE_INVALID",
                    "",
                    None,
                    str(exc),
                ).to_dict()
            ],
        }

    for component in bundle["components"]:
        component_id = str(component["component_id"])
        for artifact in component["artifacts"]:
            relative = str(artifact["path"])
            try:
                path = _safe_repo_path(root, relative)
            except KnowledgeLockError as exc:
                findings.append(
                    LockFinding(
                        "ARTIFACT_PATH_INVALID",
                        relative,
                        None,
                        str(exc),
                    )
                )
                continue

            if not path.is_file():
                findings.append(
                    LockFinding(
                        "ARTIFACT_MISSING",
                        relative,
                        str(artifact["artifact_digest"]),
                        None,
                    )
                )
                continue

            artifact_digest = compute_artifact_digest(path)
            if artifact_digest != artifact["artifact_digest"]:
                findings.append(
                    LockFinding(
                        "ARTIFACT_DIGEST_MISMATCH",
                        relative,
                        str(artifact["artifact_digest"]),
                        artifact_digest,
                    )
                )

            try:
                semantic_digest = compute_semantic_digest(
                    path,
                    str(artifact["semantic_contract"]),
                )
            except KnowledgeLockError as exc:
                findings.append(
                    LockFinding(
                        "SEMANTIC_CONTRACT_FAILURE",
                        relative,
                        str(artifact["semantic_digest"]),
                        str(exc),
                    )
                )
                continue

            if semantic_digest != artifact["semantic_digest"]:
                findings.append(
                    LockFinding(
                        "SEMANTIC_DIGEST_MISMATCH",
                        relative,
                        str(artifact["semantic_digest"]),
                        semantic_digest,
                    )
                )

        actual_component_digest = compute_component_semantic_digest(
            component["artifacts"]
        )
        if actual_component_digest != component["component_semantic_digest"]:
            findings.append(
                LockFinding(
                    "COMPONENT_SEMANTIC_DIGEST_MISMATCH",
                    component_id,
                    str(component["component_semantic_digest"]),
                    actual_component_digest,
                )
            )

    return {
        "status": "PASS" if not findings else "FAIL",
        "bundle_id": str(bundle["bundle_id"]),
        "bundle_semantic_digest": str(bundle["bundle_semantic_digest"]),
        "verified_artifact_count": sum(
            len(component["artifacts"])
            for component in bundle["components"]
        ),
        "findings": [item.to_dict() for item in findings],
    }


def verify_active_lock(
    repository_root: str | Path = ROOT,
    lock_path: str | Path | None = None,
) -> dict[str, Any]:
    root = Path(repository_root).resolve()
    lock_file = (
        Path(lock_path)
        if lock_path is not None
        else root / "product" / "PRODUCT_KNOWLEDGE.lock.json"
    )

    try:
        lock = load_lock(lock_file)
        validate_lock_structure(lock)
        bundle_path = _safe_repo_path(root, str(lock["active_bundle_path"]))
        if not bundle_path.is_file():
            raise KnowledgeLockError("active bundle artifact is missing")

        actual_bundle_artifact_digest = compute_artifact_digest(bundle_path)
        if actual_bundle_artifact_digest != lock["bundle_artifact_digest"]:
            return {
                "status": "FAIL",
                "lock_id": str(lock["lock_id"]),
                "bundle_id": str(lock["active_bundle_id"]),
                "findings": [
                    LockFinding(
                        "BUNDLE_ARTIFACT_DIGEST_MISMATCH",
                        str(lock["active_bundle_path"]),
                        str(lock["bundle_artifact_digest"]),
                        actual_bundle_artifact_digest,
                    ).to_dict()
                ],
            }

        bundle = load_bundle(bundle_path)
        if bundle.get("bundle_id") != lock["active_bundle_id"]:
            raise KnowledgeLockError("lock/bundle id mismatch")
        if bundle.get("bundle_semantic_digest") != lock["bundle_semantic_digest"]:
            raise KnowledgeLockError("lock/bundle semantic digest mismatch")
        if bundle.get("source_commit") != lock["source_commit"]:
            raise KnowledgeLockError("lock/bundle source_commit mismatch")

        report = verify_bundle(root, bundle)
        return {
            "status": report["status"],
            "lock_id": str(lock["lock_id"]),
            "bundle_id": str(lock["active_bundle_id"]),
            "bundle_semantic_digest": str(lock["bundle_semantic_digest"]),
            "source_commit": str(lock["source_commit"]),
            "verified_artifact_count": report.get("verified_artifact_count", 0),
            "findings": report["findings"],
        }
    except (
        OSError,
        json.JSONDecodeError,
        KnowledgeLockError,
        TypeError,
        ValueError,
    ) as exc:
        return {
            "status": "FAIL",
            "lock_id": "",
            "bundle_id": "",
            "findings": [
                LockFinding(
                    "ACTIVE_LOCK_INVALID",
                    str(lock_file),
                    None,
                    str(exc),
                ).to_dict()
            ],
        }


def verify_active_component_lock(
    repository_root: str | Path,
    component_id: str,
) -> dict[str, Any]:
    """Verify one active component without invalidating unrelated components.

    The bundle/lock identity is still checked globally, but artifact verification
    is limited to the requested component. This is the key selective-invalidation
    boundary from Proposal #491: K_response drift must not make an unchanged
    K_signal consumer unusable.
    """

    root = Path(repository_root).resolve()
    findings: list[LockFinding] = []

    try:
        if component_id not in SUPPORTED_COMPONENTS:
            raise KnowledgeLockError(
                f"unknown Product Knowledge component: {component_id}"
            )

        lock = load_lock(root / "product" / "PRODUCT_KNOWLEDGE.lock.json")
        validate_lock_structure(lock)
        bundle_path = _safe_repo_path(root, str(lock["active_bundle_path"]))
        if not bundle_path.is_file():
            raise KnowledgeLockError("active bundle artifact is missing")
        if compute_artifact_digest(bundle_path) != lock["bundle_artifact_digest"]:
            raise KnowledgeLockError("active bundle artifact digest mismatch")

        bundle = load_bundle(bundle_path)
        validate_bundle_structure(bundle)
        if bundle.get("bundle_id") != lock["active_bundle_id"]:
            raise KnowledgeLockError("active lock/bundle id mismatch")
        if bundle.get("bundle_semantic_digest") != lock["bundle_semantic_digest"]:
            raise KnowledgeLockError("active lock/bundle semantic digest mismatch")
        if bundle.get("source_commit") != lock["source_commit"]:
            raise KnowledgeLockError("active lock/bundle source_commit mismatch")

        component = next(
            (
                item
                for item in bundle["components"]
                if item["component_id"] == component_id
            ),
            None,
        )
        if component is None:
            raise KnowledgeLockError(
                f"active bundle does not contain {component_id}"
            )

        expected_component_digest = compute_component_semantic_digest(
            component["artifacts"]
        )
        if expected_component_digest != component["component_semantic_digest"]:
            raise KnowledgeLockError(
                f"{component_id}: component semantic digest metadata mismatch"
            )

        for artifact in component["artifacts"]:
            relative = str(artifact["path"])
            path = _safe_repo_path(root, relative)
            if not path.is_file():
                findings.append(
                    LockFinding(
                        "ARTIFACT_MISSING",
                        relative,
                        str(artifact["artifact_digest"]),
                        None,
                    )
                )
                continue

            exact = compute_artifact_digest(path)
            if exact != artifact["artifact_digest"]:
                findings.append(
                    LockFinding(
                        "ARTIFACT_DIGEST_MISMATCH",
                        relative,
                        str(artifact["artifact_digest"]),
                        exact,
                    )
                )

            semantic = compute_semantic_digest(
                path,
                str(artifact["semantic_contract"]),
            )
            if semantic != artifact["semantic_digest"]:
                findings.append(
                    LockFinding(
                        "SEMANTIC_DIGEST_MISMATCH",
                        relative,
                        str(artifact["semantic_digest"]),
                        semantic,
                    )
                )

        return {
            "status": "PASS" if not findings else "FAIL",
            "component_id": component_id,
            "verified_artifact_count": len(component["artifacts"]),
            "findings": [item.to_dict() for item in findings],
        }
    except (
        OSError,
        json.JSONDecodeError,
        KnowledgeLockError,
        TypeError,
        ValueError,
    ) as exc:
        return {
            "status": "FAIL",
            "component_id": component_id,
            "verified_artifact_count": 0,
            "findings": [
                LockFinding(
                    "ACTIVE_COMPONENT_LOCK_INVALID",
                    component_id,
                    None,
                    str(exc),
                ).to_dict()
            ],
        }


def require_active_component_lock(
    repository_root: str | Path,
    component_id: str,
) -> None:
    """Fail closed for the requested component only."""

    report = verify_active_component_lock(repository_root, component_id)
    if report["status"] != "PASS":
        raise KnowledgeLockMismatchError(
            f"active Product Knowledge component lock failed: {report['findings']}"
        )


def require_artifact_locked(
    repository_root: str | Path,
    artifact_path: str | Path,
    component_id: str,
) -> None:
    """Verify one governed in-repository artifact before Product reads it.

    External temporary fixture paths are intentionally allowed so unit tests can
    exercise parsers/adapters without pretending fixture data are production
    Knowledge. Any path inside the repository is fail-closed: it must appear in
    the requested active component and its exact/semantic digests must match.
    """

    root = Path(repository_root).resolve()
    path = Path(artifact_path).resolve()
    if not path.is_relative_to(root):
        return

    if component_id not in SUPPORTED_COMPONENTS:
        raise KnowledgeLockMismatchError(
            f"unknown Product Knowledge component: {component_id}"
        )

    lock = load_lock(root / "product" / "PRODUCT_KNOWLEDGE.lock.json")
    validate_lock_structure(lock)
    bundle_path = _safe_repo_path(root, str(lock["active_bundle_path"]))
    if compute_artifact_digest(bundle_path) != lock["bundle_artifact_digest"]:
        raise KnowledgeLockMismatchError("active bundle artifact digest mismatch")
    bundle = load_bundle(bundle_path)
    validate_bundle_structure(bundle)
    if bundle.get("bundle_id") != lock["active_bundle_id"]:
        raise KnowledgeLockMismatchError("active lock/bundle id mismatch")
    if bundle.get("bundle_semantic_digest") != lock["bundle_semantic_digest"]:
        raise KnowledgeLockMismatchError("active lock/bundle semantic digest mismatch")
    if bundle.get("source_commit") != lock["source_commit"]:
        raise KnowledgeLockMismatchError("active lock/bundle source_commit mismatch")

    component = next(
        (
            item
            for item in bundle["components"]
            if item["component_id"] == component_id
        ),
        None,
    )
    if component is None:
        raise KnowledgeLockMismatchError(
            f"active bundle does not contain {component_id}"
        )
    actual_component_digest = compute_component_semantic_digest(
        component["artifacts"]
    )
    if actual_component_digest != component["component_semantic_digest"]:
        raise KnowledgeLockMismatchError(
            f"{component_id}: component semantic digest mismatch"
        )

    relative = path.relative_to(root).as_posix()
    artifact = next(
        (
            item
            for item in component["artifacts"]
            if item["path"] == relative
        ),
        None,
    )
    if artifact is None:
        raise KnowledgeLockMismatchError(
            f"{relative} is not registered in active {component_id} lock"
        )

    actual_artifact = compute_artifact_digest(path)
    if actual_artifact != artifact["artifact_digest"]:
        raise KnowledgeLockMismatchError(
            f"{relative}: artifact digest mismatch"
        )
    actual_semantic = compute_semantic_digest(
        path,
        str(artifact["semantic_contract"]),
    )
    if actual_semantic != artifact["semantic_digest"]:
        raise KnowledgeLockMismatchError(
            f"{relative}: semantic digest mismatch"
        )
