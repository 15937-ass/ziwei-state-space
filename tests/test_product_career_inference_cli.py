import json
from pathlib import Path

from src.product.career_inference_cli import main

ROOT = Path(__file__).resolve().parents[1]
ASSET_PATH = ROOT / "product/PL3T_TEMPORAL_ASSET_FIXTURE_v0.2.json"

BRANCH = {
    "命宫": "酉",
    "兄弟宫": "戌",
    "夫妻宫": "未",
    "子女宫": "申",
    "财帛宫": "巳",
    "疾厄宫": "午",
    "迁移宫": "卯",
    "交友宫": "辰",
    "事业宫": "丑",
    "田宅宫": "寅",
    "福德宫": "亥",
    "父母宫": "子",
}


def _snapshot(star_name="武曲", mutagen="科"):
    snapshot = json.loads(ASSET_PATH.read_text(encoding="utf-8"))
    palaces = {}
    for palace_name, branch in BRANCH.items():
        palaces[branch] = {
            "name": palace_name[:-1],
            "stem": "甲",
            "branch": branch,
            "is_body_palace": False,
            "major_stars": [],
            "minor_stars": [],
            "adjective_stars": [],
        }
    palaces[BRANCH["事业宫"]]["major_stars"] = [
        {
            "name": star_name,
            "brightness": None,
            "mutagen": mutagen,
            "type": None,
            "scope": None,
        }
    ]
    snapshot["natal"] = {"palaces": palaces}
    return snapshot


def test_cli_writes_utf8_report_to_output_file(tmp_path):
    snapshot_path = tmp_path / "snapshot.json"
    output_path = tmp_path / "career-report.json"
    snapshot_path.write_text(
        json.dumps(_snapshot(), ensure_ascii=False),
        encoding="utf-8",
    )

    result = main(
        [
            "--snapshot",
            str(snapshot_path),
            "--target-id",
            "T-DEMO",
            "--question",
            "事业本命结构及大限、流年环境",
            "--output",
            str(output_path),
        ]
    )

    report = json.loads(output_path.read_text(encoding="utf-8"))
    assert result == 0
    assert report["status"] == "PARTIAL_TEMPORAL_REGISTRY_EMPTY"
    assert report["selected_temporal_layers"] == ["DECADE", "YEAR"]
    active_ids = {item["rule_id"] for item in report["natal"]["active_rules"]}
    assert {"CA04-336", "CA04-338", "CA04-341", "CA04-347"} <= active_ids
    assert report["temporal"]["matched_reaction_rule_ids"] == []
    assert report["real_world_event_prediction_supported"] is False


def test_cli_stdout_is_deterministic_for_same_snapshot_and_arguments(capsys, tmp_path):
    snapshot_path = tmp_path / "snapshot.json"
    snapshot_path.write_text(
        json.dumps(_snapshot("破军", "禄"), ensure_ascii=False),
        encoding="utf-8",
    )
    args = [
        "--snapshot",
        str(snapshot_path),
        "--target-id",
        "T-DEMO",
        "--question",
        "事业推理接口稳定性测试",
    ]

    first_result = main(args)
    first = capsys.readouterr()
    second_result = main(args)
    second = capsys.readouterr()

    assert first_result == second_result == 0
    assert first.err == second.err == ""
    assert first.out == second.out
    payload = json.loads(first.out)
    assert payload["status"] == "PARTIAL_TEMPORAL_REGISTRY_EMPTY"


def test_cli_accepts_only_explicit_migration_window_input_and_reports_overlay(tmp_path, capsys):
    snapshot_path = tmp_path / "snapshot.json"
    window_path = tmp_path / "migration-window.json"
    output_path = tmp_path / "report.json"
    snapshot_path.write_text(
        json.dumps(_snapshot(), ensure_ascii=False),
        encoding="utf-8",
    )
    window_path.write_text(
        json.dumps(
            {
                "confirmed_distant_settlement": True,
                "years_since_distant_relocation": 2,
                "travel_only": False,
                "trigger_provenance": "OBS-CLI-RELOCATION-001",
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    result = main(
        [
            "--snapshot",
            str(snapshot_path),
            "--target-id",
            "T-DEMO",
            "--question",
            "事业推理与迁移事件相对窗口",
            "--migration-window",
            str(window_path),
            "--output",
            str(output_path),
        ]
    )

    report = json.loads(output_path.read_text(encoding="utf-8"))
    assert result == 0
    context = report["temporal"]["event_relative_context"]
    assert len(context) == 1
    assert context[0]["context_id"] == "MIGRATION_FIRST_THREE_YEARS"
    assert context[0]["status"] == "ACTIVE"
    assert context[0]["trigger_provenance"] == "OBS-CLI-RELOCATION-001"
    assert report["status"] == "PARTIAL_TEMPORAL_REGISTRY_EMPTY"
    assert report["temporal"]["matched_reaction_rule_ids"] == []
    assert report["real_world_event_prediction_supported"] is False


def test_cli_rejects_migration_window_without_required_trigger_provenance(tmp_path, capsys):
    snapshot_path = tmp_path / "snapshot.json"
    window_path = tmp_path / "migration-window.json"
    snapshot_path.write_text(
        json.dumps(_snapshot(), ensure_ascii=False),
        encoding="utf-8",
    )
    window_path.write_text(
        json.dumps(
            {
                "confirmed_distant_settlement": True,
                "years_since_distant_relocation": 1,
                "travel_only": False,
            }
        ),
        encoding="utf-8",
    )

    result = main(
        [
            "--snapshot",
            str(snapshot_path),
            "--target-id",
            "T-DEMO",
            "--question",
            "missing trigger provenance",
            "--migration-window",
            str(window_path),
        ]
    )
    error = capsys.readouterr()

    assert result == 2
    assert "trigger_provenance" in error.err


def test_cli_fails_closed_on_missing_target_and_refuses_input_overwrite(tmp_path, capsys):
    snapshot_path = tmp_path / "snapshot.json"
    snapshot_path.write_text(
        json.dumps(_snapshot(), ensure_ascii=False),
        encoding="utf-8",
    )

    missing_target = main(
        [
            "--snapshot",
            str(snapshot_path),
            "--target-id",
            "T-NOT-PRESENT",
            "--question",
            "missing target",
        ]
    )
    error = capsys.readouterr()
    assert missing_target == 2
    assert "target_id not found" in error.err

    overwrite = main(
        [
            "--snapshot",
            str(snapshot_path),
            "--target-id",
            "T-DEMO",
            "--question",
            "overwrite guard",
            "--output",
            str(snapshot_path),
        ]
    )
    error = capsys.readouterr()
    assert overwrite == 2
    assert "must not overwrite any input file" in error.err
