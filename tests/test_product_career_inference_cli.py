import json
from pathlib import Path

from tools.run_career_inference import main

ROOT = Path(__file__).resolve().parents[1]
ASSET_PATH = ROOT / "product/PL3T_TEMPORAL_ASSET_FIXTURE_v0.1.json"

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
    assert report["natal"]["active_rules"][0]["rule_id"] == "CA04-347"
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
    assert "must not overwrite the input snapshot" in error.err
