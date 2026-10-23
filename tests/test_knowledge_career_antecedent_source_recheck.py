import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RECHECK = ROOT / "knowledge/wp07c/CAREER_ANTECEDENT_SOURCE_RECHECK_16_v0.1.json"
B1 = ROOT / "knowledge/wp07c/CAREER_CONTEXTUAL_ACTIVATION_01_v0.2.json"
B2 = ROOT / "knowledge/wp07c/CAREER_CONTEXTUAL_ACTIVATION_02_v0.1.json"
B3 = ROOT / "knowledge/wp07c/CAREER_CONTEXTUAL_ACTIVATION_03_v0.1.json"
CLOSURE = ROOT / "knowledge/wp07c/CAREER_CONTEXTUAL_ACTIVATION_CLOSURE_251_v0.2.json"

def load(p):
    return json.loads(p.read_text(encoding="utf-8"))

def test_all_16_rechecked_with_no_human_gate():
    r=load(RECHECK)
    assert r["summary"]["reviewed"] == 16
    assert r["summary"]["still_ambiguous"] == 0
    assert r["summary"]["human_gate_required"] is False
    assert len({x["source_rule_id"] for x in r["records"]}) == 16

def test_no_adjacency_guessing():
    r=load(RECHECK)
    assert r["guardrails"]["adjacency_guess_used"] is False
    assert all(x["source_span_ids"] for x in r["records"])
    assert all(x["reasoning"] for x in r["records"])

def test_ca01080_uses_base_078_not_baiguan_079():
    r={x["source_rule_id"]:x for x in load(RECHECK)["records"]}
    x=r["CA01-080"]
    assert x["antecedent_rule_ids"] == ["CA01-078"]
    assert x["prior_historical_hint"] == "CA01-079"
    b={x["source_rule_id"]:x for x in load(B1)["records"]}["CA01-080"]
    assert b["antecedent_mode"] == "EXPLICIT_RULE_REFERENCE"
    assert b["antecedent_rule_ids"] == ["CA01-078"]

def test_ca01098_repairs_contradictory_inheritance():
    r={x["source_rule_id"]:x for x in load(RECHECK)["records"]}["CA01-098"]
    assert r["disposition"] == "SOURCE_CONDITION_REPAIR"
    assert r["antecedent_rule_ids"] == []
    assert "无刑煞" not in r["repaired_source_condition_text"]
    assert "见煞刑耗曜" in r["repaired_source_condition_text"]
    b={x["source_rule_id"]:x for x in load(B1)["records"]}["CA01-098"]
    assert b["antecedent_mode"] == "NONE"
    assert b["antecedent_rule_ids"] == []
    assert b["source_condition_repaired"] is True
    assert "ANTECEDENT_DEPENDENCY" not in b["unresolved_blockers"]

def test_expected_dependency_edges():
    expected={
      "CA01-058":["CA01-057"], "CA01-060":["CA01-059"], "CA01-080":["CA01-078"],
      "CA02-108":["CA02-107"], "CA02-117":["CA02-116"], "CA02-134":["CA02-133"],
      "CA02-152":["CA02-151"], "CA02-157":["CA02-156"], "CA02-167":["CA02-166"],
      "CA02-168":["CA02-166"], "CA02-170":["CA02-169"], "CA02-171":["CA02-170"],
      "CA02-184":["CA02-183"], "CA02-199":["CA02-198"], "CA03-235":["CA03-234"],
    }
    by={x["source_rule_id"]:x for x in load(B1)["records"]}
    for rid,parents in expected.items():
        assert by[rid]["antecedent_mode"] == "EXPLICIT_RULE_REFERENCE"
        assert by[rid]["antecedent_rule_ids"] == parents

def test_cumulative_251_has_zero_unresolved_antecedents():
    c=load(CLOSURE)
    assert c["coverage"]["complete"] is True
    assert c["summary"]["unresolved_antecedent_reference_rows"] == 0
    assert c["summary"]["explicit_antecedent_dependency_rows"] == 64
    assert c["summary"]["source_resolution_changes"] == 16
    assert c["summary"]["source_condition_repairs"] == 1
    assert c["summary"]["dependency_scope_corrections"] == 1

def test_all_251_unique_after_recheck():
    rows=load(B1)["records"]+load(B2)["records"]+load(B3)["records"]
    assert len(rows) == 251
    assert len({r["source_rule_id"] for r in rows}) == 251
    assert not [r for r in rows if r["antecedent_mode"] == "ANTECEDENT_SURFACE_UNRESOLVED"]

def test_no_execution_or_numeric_unlock():
    b=load(B1)
    c=load(CLOSURE)
    assert b["summary"]["conditions_compiled"] == 0
    assert b["summary"]["execution_unlocked"] == 0
    assert c["summary"]["conditions_compiled"] == 0
    assert c["summary"]["execution_unlocked"] == 0
    assert c["guardrails"]["product_runtime_modified"] is False
    assert c["guardrails"]["numeric_weights_added"] is False
    assert c["guardrails"]["probabilities_added"] is False
    assert c["guardrails"]["unknown_forced_to_executable"] is False
