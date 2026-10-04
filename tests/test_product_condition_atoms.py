import pytest

from src.product.condition_atoms import (
    compile_condition_registry,
    compile_condition_spec,
    fact_from_atom,
)


def test_atom_canonicalization_is_order_independent():
    a = fact_from_atom("PALACE_HAS_STAR", palace="P05", star="武曲")
    b = fact_from_atom("PALACE_HAS_STAR", star="武曲", palace="P05")
    assert a == b


def test_registry_rejects_unknown_atom_type():
    with pytest.raises(ValueError):
        compile_condition_registry(
            {
                "schema_version": "0.1",
                "rules": {
                    "R1": {
                        "all_of": [
                            {"atom_type": "MAGIC_GUESS", "args": {"x": "y"}}
                        ]
                    }
                },
            }
        )


def test_boolean_condition_all_any_none():
    condition = compile_condition_spec(
        {
            "all_of": [
                {"atom_type": "PALACE_PRESENT", "args": {"palace": "P05"}}
            ],
            "any_of": [
                [
                    {"atom_type": "STAR_PRESENT", "args": {"star": "武曲"}},
                    {"atom_type": "STAR_PRESENT", "args": {"star": "天府"}},
                ]
            ],
            "none_of": [
                {"atom_type": "TAG_PRESENT", "args": {"tag": "QUARANTINED"}}
            ],
        }
    )

    good = frozenset(
        {
            fact_from_atom("PALACE_PRESENT", palace="P05"),
            fact_from_atom("STAR_PRESENT", star="武曲"),
        }
    )
    assert condition.matches(good)

    missing_any = frozenset({fact_from_atom("PALACE_PRESENT", palace="P05")})
    assert not condition.matches(missing_any)

    forbidden = frozenset(
        set(good) | {fact_from_atom("TAG_PRESENT", tag="QUARANTINED")}
    )
    assert not condition.matches(forbidden)


def test_registry_requires_v01():
    with pytest.raises(ValueError):
        compile_condition_registry({"schema_version": "0.2", "rules": {}})
