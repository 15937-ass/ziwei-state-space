import csv
from collections import Counter
from pathlib import Path

INDEX = Path("training_data/CASEBOOK_CASE_INDEX_v0.1.csv")

EXPECTED = {
    "LIAORAN_UPPER_01": {"count": 15, "first": 1, "last": 15, "pdf_pages": 250},
    "LIAORAN_MIDDLE_02": {"count": 41, "first": 16, "last": 56, "pdf_pages": 298},
    "LIAORAN_LOWER_03": {"count": 44, "first": 57, "last": 100, "pdf_pages": 270},
}


def load_rows():
    with INDEX.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def test_casebook_index_has_all_100_cases():
    rows = load_rows()
    ids = [int(r["case_id"]) for r in rows]
    assert len(rows) == 100
    assert ids == list(range(1, 101))


def test_casebook_source_counts_and_ranges():
    rows = load_rows()
    counts = Counter(r["source_id"] for r in rows)
    assert counts == Counter({k: v["count"] for k, v in EXPECTED.items()})

    for source_id, exp in EXPECTED.items():
        source_rows = [r for r in rows if r["source_id"] == source_id]
        ids = [int(r["case_id"]) for r in source_rows]
        assert ids[0] == exp["first"]
        assert ids[-1] == exp["last"]
        assert int(source_rows[-1]["pdf_end_page"]) == exp["pdf_pages"]


def test_page_ranges_are_monotonic_nonoverlapping_and_offset_is_explicit():
    rows = load_rows()

    for source_id in EXPECTED:
        source_rows = [r for r in rows if r["source_id"] == source_id]
        previous_end = None

        for row in source_rows:
            printed = int(row["printed_start_page"])
            start = int(row["pdf_start_page"])
            end = int(row["pdf_end_page"])

            assert start == printed + 2
            assert start <= end
            assert row["index_status"] == "TOC_INDEXED"

            if previous_end is not None:
                assert start == previous_end + 1
            previous_end = end
