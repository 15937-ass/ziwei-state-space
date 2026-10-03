from src.product.chart_schema import validate_normalized_chart


def _palace():
    return {
        "stem": "甲",
        "branch": "子",
        "is_body_palace": False,
        "major_stars": [],
        "minor_stars": [],
        "adjective_stars": [],
    }


def _snapshot():
    palaces = {f"宫{i}": _palace() for i in range(12)}
    return {
        "schema_version": "0.1",
        "engine": {
            "name": "test",
            "version": "1",
            "adapter_version": "0.1",
        },
        "input": {"solar_date": "2000-02-29"},
        "chart": {"palaces": palaces},
    }


def test_valid_snapshot_passes():
    result = validate_normalized_chart(_snapshot())
    assert result.ok is True
    assert result.errors == ()


def test_requires_twelve_palaces():
    snapshot = _snapshot()
    snapshot["chart"]["palaces"].pop("宫0")
    result = validate_normalized_chart(snapshot)
    assert result.ok is False
    assert any("12 palaces" in e for e in result.errors)


def test_requires_engine_metadata():
    snapshot = _snapshot()
    snapshot["engine"]["version"] = ""
    result = validate_normalized_chart(snapshot)
    assert result.ok is False
    assert "engine.version is required" in result.errors
