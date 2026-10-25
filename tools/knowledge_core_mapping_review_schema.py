"""Standard-library validator for the Mapping Review Envelope v0.1 contract."""

from __future__ import annotations

from functools import lru_cache
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "knowledge/core/wp06b/MAPPING_REVIEW_SCHEMA_v0.1.json"


@lru_cache(maxsize=1)
def load_mapping_review_schema() -> dict[str, Any]:
    """Load the authoritative machine-readable envelope schema."""
    return json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))


def _validate_value_state(value: Any, field: str, schema: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    definition = schema["$defs"][f"{field}_state"]
    if not isinstance(value, dict):
        return [f"{field} must be an object"]

    allowed_keys = set(definition["properties"])
    extra_keys = [key for key in value if key not in allowed_keys]
    if extra_keys:
        errors.append(f"{field} has unexpected properties: {', '.join(map(str, extra_keys))}")
    for required in definition["required"]:
        if required not in value:
            errors.append(f"{field} is missing required property: {required}")

    state = value.get("state")
    allowed_states = schema["$defs"]["review_value_state"]["enum"]
    if state not in allowed_states:
        errors.append(f"{field}.state must be one of {allowed_states}")
        return errors

    item_value = value.get("value")
    conflict_ref = value.get("conflict_ref")
    allowed_values = schema["$defs"][f"{field}_values"]["enum"]

    if state == "KNOWN":
        if item_value not in allowed_values:
            errors.append(f"{field}.value must be one of {allowed_values} when state is KNOWN")
        if conflict_ref is not None:
            errors.append(f"{field}.conflict_ref must be absent or null when state is KNOWN")
    elif state == "CONFLICT":
        if item_value is not None:
            errors.append(f"{field}.value must be null when state is CONFLICT")
        if not isinstance(conflict_ref, str) or len(conflict_ref) < 1:
            errors.append(f"{field}.conflict_ref must be a non-empty reference when state is CONFLICT")
    else:
        if item_value is not None:
            errors.append(f"{field}.value must be null when state is {state}")
        if conflict_ref is not None:
            errors.append(f"{field}.conflict_ref must be absent or null when state is {state}")
    return errors


def validate_mapping_review(record: Any) -> list[str]:
    """Return validation errors for one mapping_review object; an empty list means valid."""
    schema = load_mapping_review_schema()
    if not isinstance(record, dict):
        return ["mapping_review must be an object"]

    errors: list[str] = []
    for required in schema["required"]:
        if required not in record:
            errors.append(f"mapping_review is missing required field: {required}")

    allowed_fields = set(schema["properties"])
    extra_fields = [field for field in record if field not in allowed_fields]
    if extra_fields:
        errors.append(f"mapping_review has unexpected fields: {', '.join(map(str, extra_fields))}")

    version = schema["properties"]["schema_version"]["const"]
    if "schema_version" in record and record["schema_version"] != version:
        errors.append(f"schema_version must equal {version}")

    for field in ("review_record_id", "target_ref", "rationale"):
        if field not in record:
            continue
        spec = schema["properties"][field]
        value = record[field]
        if not isinstance(value, str) or len(value) < spec.get("minLength", 0):
            errors.append(f"{field} must be a non-empty string")

    if "source_refs" in record:
        refs = record["source_refs"]
        spec = schema["properties"]["source_refs"]
        if not isinstance(refs, list):
            errors.append("source_refs must be an array")
        else:
            if len(refs) < spec.get("minItems", 0):
                errors.append("source_refs must contain at least one reference")
            bad_items = [
                index for index, item in enumerate(refs)
                if not isinstance(item, str) or len(item) < spec["items"].get("minLength", 0)
            ]
            if bad_items:
                errors.append(f"source_refs contains invalid item(s) at indexes {bad_items}")
            if spec.get("uniqueItems") and not bad_items and len(set(refs)) != len(refs):
                errors.append("source_refs must not contain duplicate references")

    for field in ("evidence_role", "mapping_disposition"):
        if field in record:
            errors.extend(_validate_value_state(record[field], field, schema))
    return errors


def validate_mapping_review_collection(records: Any) -> list[str]:
    """Validate a list of records and ensure review_record_id is unique within it."""
    if not isinstance(records, list):
        return ["mapping-review collection must be an array"]

    errors: list[str] = []
    seen: dict[str, int] = {}
    for index, record in enumerate(records):
        errors.extend(
            f"records[{index}]: {error}"
            for error in validate_mapping_review(record)
        )
        if isinstance(record, dict):
            record_id = record.get("review_record_id")
            if isinstance(record_id, str) and len(record_id) > 0:
                if record_id in seen:
                    errors.append(
                        f"records[{index}].review_record_id duplicates records[{seen[record_id]}]"
                    )
                else:
                    seen[record_id] = index
    return errors
