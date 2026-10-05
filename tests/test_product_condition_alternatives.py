from src.product.condition_atoms import compile_condition_spec, fact_from_atom


def atom(star):
    return {"atom_type": "PALACE_HAS_STAR", "args": {"palace": "P05", "star": star}}


def test_alternatives_are_or_of_complete_conjunctions():
    condition=compile_condition_spec({
        "alternatives":[
            [atom("铃星"),atom("地空")],
            [atom("火星"),atom("地劫")],
        ]
    })
    bell_void=frozenset({
        fact_from_atom("PALACE_HAS_STAR",palace="P05",star="铃星"),
        fact_from_atom("PALACE_HAS_STAR",palace="P05",star="地空"),
    })
    fire_void=frozenset({
        fact_from_atom("PALACE_HAS_STAR",palace="P05",star="火星"),
        fact_from_atom("PALACE_HAS_STAR",palace="P05",star="地空"),
    })
    fire_robbery=frozenset({
        fact_from_atom("PALACE_HAS_STAR",palace="P05",star="火星"),
        fact_from_atom("PALACE_HAS_STAR",palace="P05",star="地劫"),
    })
    assert condition.matches(bell_void)
    assert not condition.matches(fire_void)
    assert condition.matches(fire_robbery)


def test_alternative_branch_cannot_require_forbidden_atom():
    try:
        compile_condition_spec({
            "none_of":[atom("地空")],
            "alternatives":[[atom("铃星"),atom("地空")]],
        })
    except ValueError as exc:
        assert "forbidden atom" in str(exc)
    else:
        raise AssertionError("expected ValueError")
