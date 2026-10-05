from pathlib import Path

from src.product.palace_structure import load_palace_ontology
from src.product.wealth_normalization_review import load_normalization_review
from src.product.wealth_pilot import (
    build_w01_coverage_ledger,
    compose_wealth_registries,
    compile_wealth_pilot,
    load_pilot_registry,
    load_projection_rows,
    run_wealth_pilot,
    summarize_ledger,
)

ROOT=Path(__file__).resolve().parents[1]
W01=ROOT/"validation/wp05/W01_wealth_projection_review_001_100.csv"
ONTOLOGY=ROOT/"knowledge/wp05/palace_ontology_v0.1.csv"
REVIEW=ROOT/"product/PL2O_WEALTH_NORMALIZATION_REVIEW_v0.1.csv"
BATCHES=[
    ROOT/"product/PL2C_WEALTH_PILOT_v0.1.json",
    ROOT/"product/PL2F_WEALTH_NORMALIZATION_BATCH2_v0.1.json",
    ROOT/"product/PL2H_WEALTH_CROSS_PALACE_BATCH_v0.1.json",
    ROOT/"product/PL2J_WEALTH_READY_BATCH1_v0.1.json",
    ROOT/"product/PL2J2_WEALTH_READY_BATCH2_v0.1.json",
    ROOT/"product/PL2M_WEALTH_ANTECEDENT_EXECUTABLE_BATCH_v0.1.json",
    ROOT/"product/PL2L_WEALTH_SOURCE_BACKED_BATCH_v0.1.json",
    ROOT/"product/PL2O2_WEALTH_NORMALIZATION_SAFE_BATCH_v0.1.json",
]

BRANCH={
    "命宫":"酉","兄弟宫":"戌","夫妻宫":"未","子女宫":"申",
    "财帛宫":"巳","疾厄宫":"午","迁移宫":"卯","交友宫":"辰",
    "事业宫":"丑","田宅宫":"寅","福德宫":"亥","父母宫":"子",
}


def star(name,mutagen=None):
    return {"name":name,"brightness":None,"mutagen":mutagen,"type":None,"scope":None}


def snapshot(wealth_stars):
    palaces={}
    for name,branch in BRANCH.items():
        palaces[branch]={
            "name":name[:-1],"stem":"甲","branch":branch,"is_body_palace":False,
            "major_stars":list(wealth_stars if name=="财帛宫" else []),
            "minor_stars":[],"adjective_stars":[],
        }
    return {"schema_version":"0.2","engine":{"name":"test","version":"1","adapter_version":"0.2"},"input":{},"natal":{"palaces":palaces}}


def load_all():
    rows=load_projection_rows(W01)
    registry=compose_wealth_registries(*(load_pilot_registry(p) for p in BATCHES))
    return rows,registry,load_palace_ontology(ONTOLOGY)


def test_b08_consumes_exact_pl2o_ready_subset():
    ready={r.projection_rule_id for r in load_normalization_review(REVIEW) if r.review_disposition=="EXECUTABLE_NORMALIZATION_READY"}
    b08=set(load_pilot_registry(BATCHES[-1])["rules"])
    assert ready=={"W01-067","W01-071"}
    assert b08==ready


def test_b08_expands_coverage_to_59():
    rows,registry,_=load_all()
    report=compile_wealth_pilot(rows,registry)
    assert report.issues==()
    assert len(report.executable)==59
    assert summarize_ledger(build_w01_coverage_ledger(rows,registry))=={
        "EXECUTABLE":59,
        "NORMALIZATION_PENDING":41,
        "PATH_DEPENDENT_HOLD":0,
        "EXCLUDED":0,
    }


def test_w01_067_requires_fire_or_bell_plus_ji_plus_kongjie():
    rows,registry,ontology=load_all()
    ok=run_wealth_pilot(snapshot([star("火星"),star("地空"),star("武曲","忌")]),rows,registry,palace_ontology=ontology)
    assert "W01-067" in {n.rule_id for n in ok.nodes}
    missing_ji=run_wealth_pilot(snapshot([star("火星"),star("地空")]),rows,registry,palace_ontology=ontology)
    assert "W01-067" not in {n.rule_id for n in missing_ji.nodes}


def test_w01_071_preserves_source_disjunction_without_false_fire_dikong():
    rows,registry,ontology=load_all()
    fire_dikong=run_wealth_pilot(snapshot([star("火星"),star("地空")]),rows,registry,palace_ontology=ontology)
    assert "W01-071" not in {n.rule_id for n in fire_dikong.nodes}
    bell_dikong=run_wealth_pilot(snapshot([star("铃星"),star("地空")]),rows,registry,palace_ontology=ontology)
    assert "W01-071" in {n.rule_id for n in bell_dikong.nodes}
    fire_dijie=run_wealth_pilot(snapshot([star("火星"),star("地劫")]),rows,registry,palace_ontology=ontology)
    assert "W01-071" in {n.rule_id for n in fire_dijie.nodes}
