import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CSV = ROOT / "validation/knowledge/palaces/P01_life/LP01_life_projection_review_001_100.csv"
READJ = ROOT / "knowledge/palaces/P01_life/LIFE_LP01_SOURCE_READJUDICATION_100_v0.1.json"
TIME = ROOT / "knowledge/palaces/P01_life/LIFE_LP01_SOURCE_TIME_SCOPE_v0.1.json"

def load(path):
    return json.loads(path.read_text(encoding="utf-8"))

def rows():
    with CSV.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))

def test_lp01_exact_100_unique_and_provenance():
    r = rows()
    assert len(r) == 100
    assert len({x["projection_rule_id"] for x in r}) == 100
    assert r[0]["projection_rule_id"] == "P01-001"
    assert r[-1]["projection_rule_id"] == "P01-100"
    assert all(x["source_id"] == "SRC-ZZ-003" for x in r)
    assert all(x["palace_id"] == "P01" for x in r)
    assert all(x["source_span_verified"] == "true" for x in r)

def test_case_and_history_counts_reconfirmed():
    r = rows()
    assert sum(x["case_support_only"] == "true" for x in r) == 21
    ids = {x["projection_rule_id"] for x in r if x["history_feedback"]}
    assert ids == {"P01-022", "P01-041", "P01-056"}

def test_readjudication_summary():
    d = load(READJ)
    s = d["summary"]
    assert s["reviewed"] == 100
    assert s["canonical_promoted"] == 100
    assert s["reusable_projection_rules"] == 79
    assert s["case_support_only"] == 21
    assert s["history_feedback"] == 3
    assert s["source_resolution_changed_rows"] == ["P01-044", "P01-045", "P01-054", "P01-055", "P01-073"]
    assert d["source_basis"]["historical_candidate_status"] == "NONCANONICAL_ACCELERATION_INPUT_ONLY"

def test_source_time_scope_not_silently_narrowed():
    d = load(TIME)
    m = {x["projection_rule_id"]: x for x in d["records"]}
    assert m["P01-007"]["source_time_layers"] == ["DECADE", "YEAR"]
    assert m["P01-010"]["scope_status"] == "SOURCE_GENERIC_NIANXIAN"
    assert m["P01-049"]["source_time_layers"] == ["DECADE", "YEAR"]
    assert m["P01-057"]["source_time_layers"] == ["DECADE", "YEAR"]
    assert m["P01-074"]["source_time_layers"] == ["UNSPECIFIED_PERIOD"]
    assert m["P01-032"]["additional_source_time_scope"] == ["DECADE", "YEAR"]
    assert "年限" in m["P01-032"]["source_timing_note"]

def test_history_fail_closed():
    d = load(TIME)
    m = {x["projection_rule_id"]: x for x in d["records"]}
    assert m["P01-022"]["dependencies"] == ["CHECK_EXISTING_A2_R1"]
    assert m["P01-041"]["dependencies"] == ["CHECK_EXISTING_A2_R1"]
    assert m["P01-056"]["dependencies"] == ["CHECK_EXISTING_A2_R1"]

def test_no_new_quantitative_or_time_primitive():
    s = load(READJ)["summary"]
    for key in [
        "new_primitive_qi",
        "new_memory_type",
        "new_independent_time_scale",
        "numeric_weight",
        "probability",
        "decay",
    ]:
        assert s[key] == 0


def test_cross_palace_dependency_critic_repairs():
    m = {x["projection_rule_id"]: x for x in rows()}
    assert m["P01-044"]["cross_palace_dependency"] == "夫妻宫"
    assert m["P01-045"]["cross_palace_dependency"] == "夫妻宫"
    assert m["P01-054"]["cross_palace_dependency"] == ""
    assert m["P01-055"]["cross_palace_dependency"] == ""
    assert m["P01-073"]["cross_palace_dependency"] == ""
