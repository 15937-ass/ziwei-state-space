import pytest

from apps.social_quickread_pilot.temporal_4h import (
    InteractionType,
    Mutagen,
    TemporalInputSource,
    TemporalLayer,
    TEN_STEM_TRANSFORMATIONS,
    build_temporal_4h_series,
    build_temporal_4h_snapshot,
    quickread_temporal_payload,
    stem_for_gregorian_year,
    transformations_for_stem,
)


def test_ten_stem_table_is_complete_and_ordered():
    assert set(TEN_STEM_TRANSFORMATIONS) == set("甲乙丙丁戊己庚辛壬癸")
    assert TEN_STEM_TRANSFORMATIONS["甲"] == ("廉贞", "破军", "武曲", "太阳")
    assert TEN_STEM_TRANSFORMATIONS["乙"] == ("天机", "天梁", "紫微", "太阴")
    assert TEN_STEM_TRANSFORMATIONS["丙"] == ("天同", "天机", "文昌", "廉贞")
    assert TEN_STEM_TRANSFORMATIONS["丁"] == ("太阴", "天同", "天机", "巨门")
    assert TEN_STEM_TRANSFORMATIONS["戊"] == ("贪狼", "太阴", "右弼", "天机")
    assert TEN_STEM_TRANSFORMATIONS["己"] == ("武曲", "贪狼", "天梁", "文曲")
    assert TEN_STEM_TRANSFORMATIONS["庚"] == ("太阳", "武曲", "太阴", "天同")
    assert TEN_STEM_TRANSFORMATIONS["辛"] == ("巨门", "太阳", "文曲", "文昌")
    assert TEN_STEM_TRANSFORMATIONS["壬"] == ("天梁", "紫微", "左辅", "武曲")
    assert TEN_STEM_TRANSFORMATIONS["癸"] == ("破军", "巨门", "太阴", "贪狼")


def test_transformations_for_stem_resolves_palaces_without_semantics():
    marks = transformations_for_stem(
        "甲",
        layer=TemporalLayer.DECADE,
        star_to_palace={
            "廉贞": "夫妻",
            "破军": "迁移",
            "武曲": "官禄",
            "太阳": "父母",
        },
    )
    assert [(x.star, x.mutagen, x.palace) for x in marks] == [
        ("廉贞", Mutagen.LU, "夫妻"),
        ("破军", Mutagen.QUAN, "迁移"),
        ("武曲", Mutagen.KE, "官禄"),
        ("太阳", Mutagen.JI, "父母"),
    ]


def test_cross_layer_same_star_and_natal_reactivation_are_detected():
    snapshot = build_temporal_4h_snapshot(
        decade_stem="丁",
        year_stem="丙",
        star_to_palace={
            "太阴": "财帛",
            "天同": "迁移",
            "天机": "官禄",
            "巨门": "夫妻",
            "文昌": "命宫",
            "廉贞": "福德",
        },
        natal_transformations={"天机": "化权"},
    )
    interactions = {
        (x.interaction_type, x.star, x.palace, x.mutagens)
        for x in snapshot.interactions
    }
    assert (
        InteractionType.SAME_STAR_CROSS_MUTAGEN,
        "天机",
        "官禄",
        ("权", "科"),
    ) in interactions or (
        InteractionType.SAME_STAR_CROSS_MUTAGEN,
        "天机",
        "官禄",
        ("权", "科", "权"),
    ) in interactions
    assert any(
        x.interaction_type is InteractionType.NATAL_STAR_REACTIVATED
        and x.star == "天机"
        for x in snapshot.interactions
    )
    assert any(
        x.interaction_type is InteractionType.SAME_STAR_CROSS_MUTAGEN
        and x.star == "天同"
        for x in snapshot.interactions
    )


def test_same_mutagen_stack_is_detected():
    snapshot = build_temporal_4h_snapshot(
        decade_stem="甲",
        year_stem="甲",
        star_to_palace={
            "廉贞": "命宫",
            "破军": "迁移",
            "武曲": "财帛",
            "太阳": "官禄",
        },
    )
    assert any(
        x.interaction_type is InteractionType.SAME_STAR_SAME_MUTAGEN
        and x.star == "廉贞"
        and x.mutagens == ("禄",)
        for x in snapshot.interactions
    )


def test_manual_snapshot_is_not_runtime_and_payload_is_fail_narrow():
    snapshot = build_temporal_4h_snapshot(
        decade_stem="乙",
        year_stem="丙",
        star_to_palace={
            "天机": "官禄",
            "天梁": "迁移",
            "紫微": "命宫",
            "太阴": "财帛",
            "天同": "夫妻",
            "文昌": "父母",
            "廉贞": "福德",
        },
        input_source=TemporalInputSource.MANUAL_SCREENSHOT,
    )
    payload = quickread_temporal_payload(snapshot)
    assert payload["input_source"] == "MANUAL_SCREENSHOT"
    assert payload["runtime_run_id"] is None
    assert payload["interpretation_contract"]["event_inference_forbidden_without_source_backed_rule"] is True
    assert "事业变好" not in str(payload)


def test_validated_runtime_source_requires_run_id():
    with pytest.raises(ValueError, match="runtime_run_id"):
        build_temporal_4h_snapshot(
            decade_stem="乙",
            year_stem="丙",
            star_to_palace={},
            input_source=TemporalInputSource.VALIDATED_P1_RUNTIME,
        )


def test_invalid_stem_fails_closed():
    with pytest.raises(ValueError, match="unsupported heavenly stem"):
        transformations_for_stem(
            "A",
            layer=TemporalLayer.YEAR,
            star_to_palace={},
        )


def test_gregorian_year_stem_and_multi_year_series():
    assert stem_for_gregorian_year(2024) == "甲"
    assert stem_for_gregorian_year(2025) == "乙"
    assert stem_for_gregorian_year(2026) == "丙"
    assert stem_for_gregorian_year(2027) == "丁"

    rows = build_temporal_4h_series(
        decade_stem="丁",
        years=(2025, 2026, 2027),
        star_to_palace={
            "太阴": "财帛",
            "天同": "迁移",
            "天机": "官禄",
            "巨门": "夫妻",
            "天梁": "父母",
            "紫微": "命宫",
            "文昌": "福德",
            "廉贞": "交友",
        },
    )
    assert [year for year, _ in rows] == [2025, 2026, 2027]
    assert [snapshot.year_stem for _, snapshot in rows] == ["乙", "丙", "丁"]
