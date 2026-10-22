import json
import os
import shutil
import subprocess
from pathlib import Path

import pytest

from src.product.wang_full_chart_evidence import (
    EXPECTED_CASE_IDS,
    validate_wang_full_chart_evidence,
)


ROOT = Path(__file__).resolve().parents[1]
CASE_ROOT = ROOT / "product" / "expert_cases" / "wang_tingzhi"


def test_materializer_end_to_end_with_explicit_mock_engine_only(tmp_path):
    """Exercise materializer wiring; the mock output is test-only, never product evidence."""
    node = shutil.which("node")
    if node is None:
        pytest.skip("Node.js is not available in this test runtime")

    signatures_path = CASE_ROOT / "SOURCE_BIRTH_SIGNATURES_V0_1.json"
    blind_path = CASE_ROOT / "BLIND_EVIDENCE_V0_1.json"
    readiness_path = CASE_ROOT / "FULL_CHART_RECONSTRUCTION_READINESS_V0_1.json"
    signatures = json.loads(signatures_path.read_text(encoding="utf-8"))
    blind = json.loads(blind_path.read_text(encoding="utf-8"))
    readiness = json.loads(readiness_path.read_text(encoding="utf-8"))
    blind_by_id = {row["case_id"]: row for row in blind["cases"]}
    signature_by_id = {row["case_id"]: row for row in signatures["cases"]}
    readiness_by_id = {row["case_id"]: row for row in readiness["cases"]}

    mock_charts = {}
    for case_id in EXPECTED_CASE_IDS:
        source = signature_by_id[case_id]
        anchor = blind_by_id[case_id]
        ready = readiness_by_id[case_id]
        candidate_id = ready["matched_candidate_ids"][0]
        day = int(candidate_id.split(":D")[1].split(":")[0])
        time_index = int(candidate_id.split(":T")[1])
        lunar_date = f'{source["lunar_year"]}-{source["lunar_month"]}-{day}'
        mock_charts[f"{lunar_date}|{time_index}"] = {
            "target_palace": anchor["target_palace"],
            "target_palace_empty_main_star": anchor["target_palace_empty_main_star"],
            "target_palace_main_stars": anchor["target_palace_main_stars"],
            "borrowed_from_opposite_main_stars": anchor["borrowed_from_opposite_main_stars"],
        }

    temp_script = tmp_path / "product" / "tools" / "wang_full_chart_materializer.mjs"
    temp_script.parent.mkdir(parents=True)
    source_script = ROOT / "product" / "tools" / "wang_full_chart_materializer.mjs"
    temp_script.write_text(source_script.read_text(encoding="utf-8"), encoding="utf-8")

    module_dir = tmp_path / "node_modules" / "iztro"
    module_dir.mkdir(parents=True)
    (module_dir / "package.json").write_text(
        json.dumps({"name": "iztro", "version": "2.6.1", "type": "module", "exports": "./index.js"}),
        encoding="utf-8",
    )
    mock_module = r'''
import fs from "node:fs";
const mock = JSON.parse(fs.readFileSync(process.env.WANG_MOCK_CHARTS, "utf8"));
const branches = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"];
const standardNames = ["命宫", "兄弟宫", "夫妻宫", "子女宫", "财帛宫", "疾厄宫", "迁移宫", "奴仆宫", "官禄宫", "田宅宫", "福德宫", "父母宫"];
const normalise = (value) => String(value ?? "").trim().replace(/宫$/u, "");
const star = (name) => ({ name, type: "major", brightness: null, mutagen: null, scope: null });
export const astro = {
  config() {},
  byLunar(lunarDate, timeIndex) {
    const row = mock[String(lunarDate) + "|" + String(timeIndex)];
    if (!row) throw new Error("mock engine input not found");
    const names = [row.target_palace, ...standardNames.filter((name) => normalise(name) !== normalise(row.target_palace))].slice(0, 12);
    const palaces = branches.map((branch, index) => {
      let majorStars = [];
      if (branch === "子" && !row.target_palace_empty_main_star) majorStars = row.target_palace_main_stars.map(star);
      if (branch === "午" && row.target_palace_empty_main_star) majorStars = row.borrowed_from_opposite_main_stars.map(star);
      return {
        name: names[index],
        heavenlyStem: "甲",
        earthlyBranch: branch,
        isBodyPalace: false,
        majorStars,
        minorStars: [],
        adjectiveStars: [],
        decadal: null,
      };
    });
    return {
      toJSON() {
        return {
          solarDate: "1900-1-1",
          lunarDate: lunarDate,
          chineseDate: "甲子年",
          time: "子",
          timeRange: "23:00-00:59",
          soul: "示例星",
          body: "示例星",
          fiveElementsClass: "示例局",
          earthlyBranchOfSoulPalace: "子",
          earthlyBranchOfBodyPalace: "午",
          palaces,
        };
      },
    };
  },
};
'''
    (module_dir / "index.js").write_text(mock_module, encoding="utf-8")
    mock_path = tmp_path / "mock_charts.json"
    mock_path.write_text(json.dumps(mock_charts, ensure_ascii=False), encoding="utf-8")
    output_path = tmp_path / "full_chart_test_output.json"

    env = dict(os.environ)
    env["WANG_MOCK_CHARTS"] = str(mock_path)
    result = subprocess.run(
        [
            node,
            str(temp_script),
            str(signatures_path),
            str(blind_path),
            str(readiness_path),
            str(output_path),
        ],
        cwd=tmp_path,
        env=env,
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    generated = json.loads(output_path.read_text(encoding="utf-8"))
    assert tuple(row["case_id"] for row in generated["cases"]) == EXPECTED_CASE_IDS
    assert generated["summary"]["full_chart_materialized"] == 11
    assert all(len(row["chart"]["palaces"]) == 12 for row in generated["cases"])

    import hashlib

    source_hashes = {
        "source_signatures": hashlib.sha256(signatures_path.read_bytes()).hexdigest(),
        "blind_anchor": hashlib.sha256(blind_path.read_bytes()).hexdigest(),
        "reconstruction_readiness": hashlib.sha256(readiness_path.read_bytes()).hexdigest(),
    }
    validate_wang_full_chart_evidence(
        generated, signatures, blind, readiness, source_hashes=source_hashes
    )
