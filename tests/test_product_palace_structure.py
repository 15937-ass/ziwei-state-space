from pathlib import Path

import pytest

from src.product.condition_atoms import fact_from_atom
from src.product.palace_structure import (
    compile_palace_ontology,
    load_palace_ontology,
    resolve_palace_structure,
)

ROOT = Path(__file__).resolve().parents[1]
ONTOLOGY = ROOT / "knowledge/wp05/palace_ontology_v0.1.csv"

CANONICAL = [
    ("P01", "命宫"),
    ("P02", "兄弟宫"),
    ("P03", "夫妻宫"),
    ("P04", "子女宫"),
    ("P05", "财帛宫"),
    ("P06", "疾厄宫"),
    ("P07", "迁移宫"),
    ("P08", "交友宫"),
    ("P09", "事业宫"),
    ("P10", "田宅宫"),
    ("P11", "福德宫"),
    ("P12", "父母宫"),
]
BRANCHES = list("子丑寅卯辰巳午未申酉戌亥")


def _star(name, mutagen=None):
    return {
        "name": name,
        "brightness": None,
        "mutagen": mutagen,
        "type": None,
        "scope": None,
    }


def _snapshot(*, aliases=False):
    palaces = {}
    for index, (_, name) in enumerate(CANONICAL):
        observed = name[:-1]
        if aliases and name == "事业宫":
            observed = "官禄"
        if aliases and name == "交友宫":
            observed = "奴仆"

        stars = []
        if name == "财帛宫":
            stars = [_star("武曲", "忌")]
        if name == "福德宫":
            stars = [_star("天府", "科")]
        if name == "事业宫":
            stars = [_star("七杀")]

        branch = BRANCHES[index]
        palaces[branch] = {
            "name": observed,
            "stem": "甲",
            "branch": branch,
            "is_body_palace": False,
            "major_stars": stars,
            "minor_stars": [],
            "adjective_stars": [],
        }

    return {
        "schema_version": "0.2",
        "engine": {
            "name": "test",
            "version": "1",
            "adapter_version": "0.2",
        },
        "input": {},
        "natal": {"palaces": palaces},
    }


def test_ontology_has_symmetric_opposite_and_closed_triads():
    ontology = load_palace_ontology(ONTOLOGY)
    assert len(ontology.entries) == 12

    wealth = ontology.entry("P05")
    assert wealth.opposite_palace_id == "P11"
    assert set(wealth.triad_palace_ids) == {"P01", "P09"}

    for palace_id, entry in ontology.entries.items():
        assert ontology.entry(entry.opposite_palace_id).opposite_palace_id == palace_id
        expected = {palace_id, *entry.triad_palace_ids}
        for triad_id in entry.triad_palace_ids:
            actual = {triad_id, *ontology.entry(triad_id).triad_palace_ids}
            assert actual == expected


def test_resolver_accepts_canonical_short_names_and_legacy_aliases():
    ontology = load_palace_ontology(ONTOLOGY)
    structure = resolve_palace_structure(_snapshot(aliases=True), ontology)

    assert structure.palace("P05").canonical_name == "财帛宫"
    assert structure.palace("P09").observed_name == "官禄"
    assert structure.palace("P08").observed_name == "奴仆"


def test_wealth_structure_relations_are_explicit_and_deterministic():
    ontology = load_palace_ontology(ONTOLOGY)
    structure = resolve_palace_structure(_snapshot(), ontology)

    assert structure.opposite_of("P05") == "P11"
    assert set(structure.triads_of("P05")) == {"P01", "P09"}
    assert set(structure.sanfang_sizheng_of("P05")) == {
        "P05",
        "P01",
        "P09",
        "P11",
    }
    assert structure.relation_between("P05", "P11") == "OPPOSITE"
    assert structure.relation_between("P05", "P09") == "TRIAD"
    assert structure.relation_between("P05", "P05") == "SELF"
    assert structure.relation_between("P05", "P02") is None


def test_runtime_facts_include_cross_palace_stars_and_relations():
    ontology = load_palace_ontology(ONTOLOGY)
    structure = resolve_palace_structure(_snapshot(), ontology)
    facts = structure.runtime_facts()

    assert fact_from_atom(
        "PALACE_RELATION",
        source="P05",
        target="P11",
        relation="OPPOSITE",
    ) in facts
    assert fact_from_atom(
        "PALACE_RELATION",
        source="P05",
        target="P09",
        relation="TRIAD",
    ) in facts
    assert fact_from_atom(
        "TRANSFORMATION_PRESENT",
        palace="P05",
        star="武曲",
        mutagen="忌",
    ) in facts
    assert fact_from_atom(
        "TRANSFORMATION_PRESENT",
        palace="P11",
        star="天府",
        mutagen="科",
    ) in facts
    assert fact_from_atom(
        "PALACE_HAS_STAR",
        palace="P09",
        star="七杀",
    ) in facts


def test_snapshot_order_does_not_change_resolved_facts():
    ontology = load_palace_ontology(ONTOLOGY)
    snapshot = _snapshot()
    palaces = snapshot["natal"]["palaces"]
    reversed_snapshot = dict(snapshot)
    reversed_snapshot["natal"] = {
        "palaces": dict(reversed(list(palaces.items())))
    }

    a = resolve_palace_structure(snapshot, ontology).runtime_facts()
    b = resolve_palace_structure(reversed_snapshot, ontology).runtime_facts()
    assert a == b


def test_unknown_label_fails_closed_without_explicit_alias():
    ontology = load_palace_ontology(ONTOLOGY)
    snapshot = _snapshot()
    first = next(iter(snapshot["natal"]["palaces"].values()))
    first["name"] = "未知宫名"

    with pytest.raises(ValueError, match="cannot map snapshot palace"):
        resolve_palace_structure(snapshot, ontology)


def test_explicit_adapter_alias_can_be_supplied_without_mutating_ontology():
    ontology = load_palace_ontology(ONTOLOGY)
    snapshot = _snapshot()
    for palace in snapshot["natal"]["palaces"].values():
        if palace["name"] == "交友":
            palace["name"] = "引擎自定义仆役标签"
            break

    structure = resolve_palace_structure(
        snapshot,
        ontology,
        extra_aliases={"引擎自定义仆役标签": "P08"},
    )
    assert structure.palace("P08").canonical_name == "交友宫"


def test_broken_ontology_symmetry_is_rejected():
    ontology = load_palace_ontology(ONTOLOGY)
    rows = []
    for entry in ontology.entries.values():
        rows.append(
            {
                "palace_id": entry.palace_id,
                "canonical_name": entry.canonical_name,
                "legacy_alias": ";".join(entry.aliases),
                "opposite_palace": ontology.entry(entry.opposite_palace_id).canonical_name,
                "triad_palace_1": ontology.entry(entry.triad_palace_ids[0]).canonical_name,
                "triad_palace_2": ontology.entry(entry.triad_palace_ids[1]).canonical_name,
                "source_basis": entry.source_basis,
                "status": "ACTIVE",
            }
        )
    row = next(item for item in rows if item["palace_id"] == "P05")
    row["opposite_palace"] = "兄弟宫"

    with pytest.raises(ValueError):
        compile_palace_ontology(rows)


@pytest.mark.parametrize("engine,version", [("iztro-js", "2.6.1"), ("x-iztro-rust", "0.6.1")])
@pytest.mark.parametrize("label", ["仆役", "仆役宫"])
def test_pinned_engine_transport_alias_preserves_raw_and_matches_canonical_facts(engine, version, label):
    import copy
    ontology = load_palace_ontology(ONTOLOGY)
    snapshot = _snapshot()
    snapshot['engine'].update(name=engine, version=version)
    expected = resolve_palace_structure(snapshot, ontology).runtime_facts()
    snapshot['natal']['palaces'][BRANCHES[7]]['name'] = label
    before = copy.deepcopy(snapshot)
    labels = dict(ontology.label_to_id)
    structure = resolve_palace_structure(snapshot, ontology)
    assert structure.palace('P08').observed_name == label
    assert structure.palace('P08').raw is snapshot['natal']['palaces'][BRANCHES[7]]
    assert structure.runtime_facts() == expected
    assert snapshot == before
    assert dict(ontology.label_to_id) == labels
    assert ontology.resolve_label('仆役') is None


@pytest.mark.parametrize('field,bad', [('name', 'other-engine'), ('version', 'future'), ('adapter_version', 'future'), ('version', [])])
def test_unrecognized_engine_metadata_cannot_activate_transport_alias(field, bad):
    ontology = load_palace_ontology(ONTOLOGY)
    snapshot = _snapshot()
    snapshot['engine'].update(name='iztro-js', version='2.6.1')
    snapshot['engine'][field] = bad
    snapshot['natal']['palaces'][BRANCHES[7]]['name'] = '仆役'
    with pytest.raises(ValueError, match='cannot map snapshot palace'):
        resolve_palace_structure(snapshot, ontology)


@pytest.mark.parametrize('engine', ['iztro-js', 'x-iztro-rust'])
def test_pinned_engine_still_rejects_unknown_names_and_duplicate_palaces(engine):
    ontology = load_palace_ontology(ONTOLOGY)
    snapshot = _snapshot()
    snapshot['engine'].update(name=engine, version='2.6.1' if engine=='iztro-js' else '0.6.1')
    snapshot['natal']['palaces'][BRANCHES[7]]['name'] = '未知仆役'
    with pytest.raises(ValueError, match='cannot map snapshot palace'):
        resolve_palace_structure(snapshot, ontology)
    snapshot['natal']['palaces'][BRANCHES[7]]['name'] = '仆役'
    snapshot['natal']['palaces'][BRANCHES[0]]['name'] = '交友'
    with pytest.raises(ValueError, match='multiple palaces to P08'):
        resolve_palace_structure(snapshot, ontology)


def test_explicit_alias_cannot_override_pinned_transport_or_canonical_mapping():
    ontology = load_palace_ontology(ONTOLOGY)
    snapshot = _snapshot()
    snapshot['engine'].update(name='iztro-js', version='2.6.1')
    for aliases in ({'仆役': 'P05'}, {'交友': 'P05'}):
        with pytest.raises(ValueError, match='conflicts with palace mapping'):
            resolve_palace_structure(snapshot, ontology, extra_aliases=aliases)


def test_pinned_alias_cannot_override_conflicting_ontology_label():
    import csv
    with ONTOLOGY.open(encoding='utf-8') as stream:
        rows = list(csv.DictReader(stream))
    # Model a future ontology conflict without touching canonical Knowledge.
    for row in rows:
        if row['palace_id'] == 'P09':
            row['legacy_alias'] = '仆役'
    ontology = compile_palace_ontology(rows)
    snapshot = _snapshot()
    snapshot['engine'].update(name='iztro-js', version='2.6.1')
    with pytest.raises(ValueError, match='conflicts with palace mapping'):
        resolve_palace_structure(snapshot, ontology)
