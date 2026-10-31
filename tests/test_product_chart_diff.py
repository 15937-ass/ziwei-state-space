from src.product.chart_diff import compare_chart_snapshots, summarize_differences


def _base_chart():
    return {
        "meta": {"engine": "a", "version": "1"},
        "palaces": {
            "命宫": {
                "stem": "甲",
                "branch": "子",
                "major_stars": ["紫微", "天府"],
                "minor_stars": ["左辅", "右弼"],
                "transformations": [
                    {"star": "紫微", "type": "权", "layer": "natal"},
                    {"star": "天府", "type": "科", "layer": "natal"},
                ],
                "brightness": {"紫微": "庙", "天府": "旺"},
            }
        },
        "limits": {"decades": [{"start_age": 2, "end_age": 11}]},
    }


def test_set_like_fields_ignore_serialization_order():
    left = _base_chart()
    right = _base_chart()
    right["palaces"]["命宫"]["major_stars"] = ["天府", "紫微"]
    right["palaces"]["命宫"]["minor_stars"] = ["右弼", "左辅"]
    right["palaces"]["命宫"]["transformations"] = list(
        reversed(right["palaces"]["命宫"]["transformations"])
    )

    diffs = compare_chart_snapshots(left, right, ignore_paths=("meta",))
    assert diffs == []


def test_major_star_difference_is_critical():
    left = _base_chart()
    right = _base_chart()
    right["palaces"]["命宫"]["major_stars"] = ["紫微"]

    diffs = compare_chart_snapshots(left, right, ignore_paths=("meta",))
    assert len(diffs) == 1
    assert diffs[0].path == "palaces.命宫.major_stars"
    assert diffs[0].severity == "CRITICAL"
    assert diffs[0].category == "stars"


def test_metadata_can_be_ignored_without_hiding_chart_difference():
    left = _base_chart()
    right = _base_chart()
    right["meta"]["engine"] = "external"
    right["palaces"]["命宫"]["branch"] = "丑"

    diffs = compare_chart_snapshots(left, right, ignore_paths=("meta",))
    assert len(diffs) == 1
    assert diffs[0].path == "palaces.命宫.branch"


def test_summary_counts_severity_and_category():
    left = _base_chart()
    right = _base_chart()
    right["palaces"]["命宫"]["stem"] = "乙"
    right["palaces"]["命宫"]["brightness"]["紫微"] = "陷"

    summary = summarize_differences(
        compare_chart_snapshots(left, right, ignore_paths=("meta",))
    )
    assert summary["exact_match"] is False
    assert summary["total_differences"] == 2
    assert summary["severity_counts"]["CRITICAL"] == 1
    assert summary["severity_counts"]["HIGH"] == 1


def test_provenance_metadata_is_ignored_but_canonical_chart_config_is_compared():
    left = {
        "chart_contract_id": "ZHONGZHOU_IZTRO_JS_2_6_1_V1",
        "engine": {"name": "iztro-js", "version": "2.6.1"},
        "input": {
            "entrypoint": "astro.withOptions",
            "chart_config": {"algorithm": "zhongzhou", "day_divide": "forward"},
        },
    }
    right = {
        "engine": {"name": "x-iztro-rust", "version": "0.6.1"},
        "input": {
            "entrypoint": "x-iztro-rust.by_solar",
            "chart_config": {"algorithm": "zhongzhou", "day_divide": "forward"},
        },
    }
    ignored = ("engine", "chart_contract_id", "input.entrypoint")
    assert compare_chart_snapshots(left, right, ignore_paths=ignored) == []

    right["input"]["chart_config"]["algorithm"] = "default"
    diffs = compare_chart_snapshots(left, right, ignore_paths=ignored)
    assert len(diffs) == 1
    assert diffs[0].path == "input.chart_config.algorithm"
