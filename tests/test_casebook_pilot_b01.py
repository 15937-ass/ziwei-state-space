import json
from pathlib import Path

PATH = Path("training_data/case_records/PILOT_B01_cases_16_17_20_22_23.jsonl")
EXPECTED_IDS = [16, 17, 20, 22, 23]


def load():
    return [json.loads(line) for line in PATH.read_text(encoding="utf-8").splitlines() if line.strip()]


def test_pilot_b01_ids_and_minimum_contract():
    rows = load()
    assert [r["case_id"] for r in rows] == EXPECTED_IDS
    for r in rows:
        assert r["source_id"] == "LIAORAN_MIDDLE_02"
        assert r["source_pages"]["pdf_start"] <= r["source_pages"]["pdf_end"]
        assert r["question"]["domains"]
        assert r["author_reasoning"]
        assert r["grades"]["provenance"].startswith("P")
        assert r["grades"]["outcome"].startswith("O")
        assert r["review"]["status"]


def test_no_reality_ground_truth_is_invented():
    rows = load()
    for r in rows:
        assert r["grades"]["outcome"] in {"O0_NONE", "O1_SUBJECTIVE", "O2_STATED_EVENT", "O3_EXTERNALLY_VERIFIED"}
        if r["grades"]["outcome"] == "O0_NONE":
            assert r["feedback"]["later_outcomes"] == []
