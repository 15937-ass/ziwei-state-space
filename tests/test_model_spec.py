from src.model_spec import (
    ModelGraph,
    PalaceNode,
    Paper1Model,
    StarSystemMode,
    TemporalInput,
    ObservabilityStatus,
    classify_observability,
)


def make_model():
    graph = ModelGraph(
        palaces={
            "P-MING": PalaceNode("P-MING", "命宫", "整体自我与人生基态", ("P-FUDE",)),
            "P-FUDE": PalaceNode("P-FUDE", "福德宫", "思想与内在活动", ("P-MING",)),
        },
        edges={
            "P-MING": ("P-FUDE",),
            "P-FUDE": ("P-MING",),
        },
    )
    return Paper1Model(graph)


def test_reaction_keeps_natal_essence_separate_from_temporal_input():
    model = make_model()
    mode = StarSystemMode(11, "紫微破军", "mode_switch", "安定", "动荡")
    essence = model.build_natal_essence(
        "P-MING",
        {"QI-03": "变动端"},
        {"QR-02": "主导端"},
        [mode],
    )
    temporal = TemporalInput(
        time_label="大限A",
        astrological_layer="decade",
        transformations=("巨门化忌",),
    )
    reaction = model.react(essence, temporal)

    assert reaction.natal_essence is essence
    assert reaction.temporal_input is temporal
    assert essence.intrinsic_state["QI-03"] == "变动端"


def test_projection_is_semantic_not_fixed_event_mapping():
    model = make_model()
    essence = model.build_natal_essence("P-MING", {}, {}, [])
    temporal = TemporalInput("流年A", "year")
    reaction = model.react(essence, temporal)
    result = model.project(
        reaction,
        semantic_classes=["关系压力增加", "决策扰动"],
        provenance=["RULE-001"],
    )

    assert "离婚" not in result.semantic_classes
    assert result.provenance == ("RULE-001",)


def test_observability_classification():
    assert classify_observability(3) == ObservabilityStatus.STRUCTURALLY_OBSERVABLE
    assert classify_observability(1) == ObservabilityStatus.PARTIALLY_OBSERVABLE
    assert classify_observability(0) == ObservabilityStatus.STRUCTURALLY_AT_RISK
    assert classify_observability(5, derived_from_existing=True) == ObservabilityStatus.DERIVED_ONLY
