from src.model_spec import (
    ModelGraph,
    PalaceNode,
    Paper1Model,
    StarSystemMode,
    TemporalInput,
    ObservationPathSupport,
    HistoryMemory,
    HistoryMemoryKind,
    PersistenceScope,
    SourceGatedHistoryTransition,
    EpistemicType,
    classify_observation_path_support,
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


def test_observation_path_support_classification():
    assert classify_observation_path_support(3) == ObservationPathSupport.MULTI_PATH_SUPPORTED
    assert classify_observation_path_support(1) == ObservationPathSupport.SINGLE_PATH_SUPPORTED
    assert classify_observation_path_support(0) == ObservationPathSupport.NO_DIRECT_PATH
    assert classify_observation_path_support(5, derived_from_existing=True) == ObservationPathSupport.DERIVED_ONLY


def test_legacy_observability_alias_returns_path_support_not_control_claim():
    assert classify_observability(2) == ObservationPathSupport.MULTI_PATH_SUPPORTED


def test_a2_history_memory_is_separate_from_natal_essence():
    model = make_model()
    essence = model.build_natal_essence("P-MING", {"QI-16": "goal-directed"}, {}, [])
    temporal = TemporalInput("大限A", "decade")
    memory = HistoryMemory(acquired_dispositions={"timidity": "reinforced"})
    reaction = model.react(essence, temporal, history_memory=memory)
    assert reaction.natal_essence is essence
    assert reaction.history_memory.acquired_dispositions["timidity"] == "reinforced"
    assert "timidity" not in essence.intrinsic_state


def test_a2_typed_history_updates_do_not_conflate_disposition_and_gate():
    model = make_model()
    memory = HistoryMemory()
    disposition = SourceGatedHistoryTransition(
        "HU-TEST", ("ZZ-SYS-31-033",), HistoryMemoryKind.ACQUIRED_DISPOSITION,
        "reckless_disposition", "entrench", PersistenceScope.LATER_PERIODS,
    )
    gate = SourceGatedHistoryTransition(
        "HG-TEST", ("ZZ-SYS-31-020",), HistoryMemoryKind.PATH_DEPENDENT_GATE,
        "key_period_utilization", "set_gate", PersistenceScope.LATER_PERIODS,
    )
    memory = model.apply_history_transition(memory, disposition, "entrenched")
    memory = model.apply_history_transition(memory, gate, "used")
    assert memory.acquired_dispositions == {"reckless_disposition": "entrenched"}
    assert memory.path_gates == {"key_period_utilization": "used"}
    assert memory.provenance == ["ZZ-SYS-31-033", "ZZ-SYS-31-020"]


def test_a2_history_transition_rejects_nonexplicit_source():
    model = make_model()
    transition = SourceGatedHistoryTransition(
        "HU-HYP", ("HYP-1",), HistoryMemoryKind.ACQUIRED_DISPOSITION,
        "x", "reinforce", PersistenceScope.UNSPECIFIED, EpistemicType.HYPOTHESIS,
    )
    try:
        model.apply_history_transition(HistoryMemory(), transition, "stronger")
    except ValueError as exc:
        assert "EXPLICIT" in str(exc)
    else:
        raise AssertionError("non-explicit history transition must be rejected")
