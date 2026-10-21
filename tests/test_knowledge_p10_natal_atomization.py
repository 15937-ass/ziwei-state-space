import csv
import json
from pathlib import Path

from src.product.condition_atoms import ALLOWED_ATOM_TYPES, fact_from_atom
from src.product.palace_structure import load_palace_ontology, resolve_palace_structure

ROOT=Path(__file__).resolve().parents[1]
MAPPING=ROOT/"knowledge/palaces/P10_property/wp07a/PROPERTY_NATAL_ATOMIZATION_MAP_v0.1.json"
ONTOLOGY=ROOT/"knowledge/wp05/palace_ontology_v0.1.csv"

CANONICAL_PALACES=[
 ("P01","命宫"),("P02","兄弟宫"),("P03","夫妻宫"),("P04","子女宫"),
 ("P05","财帛宫"),("P06","疾厄宫"),("P07","迁移宫"),("P08","交友宫"),
 ("P09","事业宫"),("P10","田宅宫"),("P11","福德宫"),("P12","父母宫"),
]
BRANCHES=list("子丑寅卯辰巳午未申酉戌亥")
EXPECTED={
 "TP02-141":{"star":"天同","mutagen":"忌","projection_domain":"effort","projection_target":"self_acquired_property_can_coexist_with_persistent_property_related_worry_and_effort","projection_mode":"FUNCTIONAL_PROJECTION","source_location":"田宅宫printed_p160"},
 "TP03-262":{"star":"巨门","mutagen":"禄","projection_domain":"property_acquisition","projection_target":"midlife_or_later_self_acquisition_tendency_strengthens","projection_mode":"STRUCTURAL_CONSTRAINT","source_location":"田宅宫printed_p163"},
 "TP04-314":{"star":"天梁","mutagen":"禄","projection_domain":"relation","projection_target":"social_or_interpersonal_friction_can_strengthen","projection_mode":"FUNCTIONAL_PROJECTION","source_location":"田宅宫printed_p164"},
}

def load_doc():
    return json.loads(MAPPING.read_text(encoding="utf-8"))

def source_rows():
    paths=[
      ROOT/"validation/wp05/TP02_property_projection_review_101_200.csv",
      ROOT/"validation/wp05/TP03_property_projection_review_201_300.csv",
      ROOT/"validation/wp05/TP04_property_projection_review_301_358.csv",
    ]
    out={}
    for path in paths:
        with path.open("r",encoding="utf-8-sig",newline="") as f:
            for row in csv.DictReader(f):
                if row["projection_rule_id"] in EXPECTED:
                    out[row["projection_rule_id"]]=row
    return out

def snapshot(star_name,mutagen):
    palaces={}
    for idx,(_,name) in enumerate(CANONICAL_PALACES):
        branch=BRANCHES[idx]
        stars=[]
        if name=="田宅宫":
            stars=[{"name":star_name,"brightness":None,"mutagen":mutagen,"type":None,"scope":None}]
        palaces[branch]={"name":name,"stem":"甲","branch":branch,"is_body_palace":False,"major_stars":stars,"minor_stars":[],"adjective_stars":[]}
    return {"schema_version":"0.2","engine":{"name":"knowledge-p10-atomization-test","version":"1","adapter_version":"0.2"},"input":{},"natal":{"palaces":palaces}}

def test_exactly_three_property_rows_mapped_without_source_drift():
    d=load_doc(); src=source_rows(); maps={x["source_rule_id"]:x for x in d["mappings"]}
    assert set(maps)==set(EXPECTED)==set(src)
    assert d["validation"]["nominated_rows"]==3
    assert d["validation"]["mapped_rows"]==3
    assert d["validation"]["blocked_nominated_rows"]==0
    for rid,e in EXPECTED.items():
        row=src[rid]; item=maps[rid]; p=item["source_provenance"]; proj=item["expected_projection"]
        assert row["source_id"]==p["source_id"]=="SRC-ZZ-003"
        assert row["source_location"]==p["source_location"]==e["source_location"]
        assert row["review_status"]==p["review_status"]=="SOURCE_SPAN_VERIFIED"
        assert row["source_span_verified"]=="true" and p["source_span_verified"] is True
        assert row["time_layer"]==p["time_layer"]=="NATAL"
        assert row["case_support_only"]=="false" and p["case_support_only"] is False
        assert row["condition"]==item["source_condition_text"]
        assert row["projection_domain"]==proj["projection_domain"]==e["projection_domain"]
        assert row["projection_target"]==proj["projection_target"]==e["projection_target"]
        assert row["projection_mode"]==proj["projection_mode"]==e["projection_mode"]
        assert item["executable_registry_entry"] is False

def test_atoms_match_real_natal_runtime_fact_shape():
    d=load_doc(); ontology=load_palace_ontology(ONTOLOGY)
    for item in d["mappings"]:
        atoms=item["condition"]["all_of"]
        assert len(atoms)==1
        atom=atoms[0]
        assert atom["atom_type"]=="TRANSFORMATION_PRESENT"
        assert atom["atom_type"] in ALLOWED_ATOM_TYPES
        assert atom==item["expected_runtime_fact"]
        assert atom["args"]["palace"]=="P10"
        facts=resolve_palace_structure(snapshot(atom["args"]["star"],atom["args"]["mutagen"]),ontology).runtime_facts()
        assert fact_from_atom(atom["atom_type"],**atom["args"]) in facts

def test_nearby_compound_and_case_rows_are_explicitly_excluded():
    d=load_doc(); ex={x["source_rule_id"]:x for x in d["exclusions"]}
    required={"TP02-142","TP02-143","TP02-144","TP03-263","TP04-315","TP04-316","TP04-317"}
    assert required.issubset(ex)
    assert ex["TP02-144"]["reason_code"]=="PATH_DEPENDENT_PARENT_REQUIRED"
    assert ex["TP03-263"]["reason_code"]=="CASE_SUPPORT_ONLY_EVENT_CANDIDATE"
    assert ex["TP04-315"]["reason_code"]=="COMPOUND_OPPOSITE_BRIGHTNESS_MALEFIC_CONTEXT"
    assert d["validation"]["source_rows_modified"] is False
    assert d["validation"]["executable_rule_created"] is False
    assert d["validation"]["product_runtime_modified"] is False
    assert d["validation"]["production_registry_modified"] is False

def test_midlife_language_is_not_numericized():
    d=load_doc(); x=next(i for i in d["mappings"] if i["source_rule_id"]=="TP03-262")
    assert "midlife_or_later" in x["expected_projection"]["projection_target"]
    assert d["validation"]["numeric_age_threshold_created"] is False
