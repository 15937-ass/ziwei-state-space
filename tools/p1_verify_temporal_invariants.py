#!/usr/bin/env python3
"""Semantic invariants for P1 B02 temporal boundaries.

These checks are deliberately independent of cross-engine equality: they verify
the relationships expected at lunar-year/month and early/late-Zi boundaries.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def load(path: Path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def signature(scope):
    return {
        "stem": scope["stem"],
        "branch": scope["branch"],
        "mutagen": scope["mutagen"],
        "stars": scope["stars"],
    }


def main() -> int:
    ap=argparse.ArgumentParser()
    ap.add_argument("jsonl")
    args=ap.parse_args()

    rows=load(Path(args.jsonl))
    assert len(rows)==100, f"expected 100 cases, got {len(rows)}"

    same_day_pairs=[
        ("B02_CNY_EVE_H12","B02_CNY_DAY_H0"),
        ("B02_NORMAL_MONTH_PREV_H12","B02_NORMAL_MONTH_DAY1_H0"),
        ("B02_LEAP_ENTER_PREV_H12","B02_LEAP_ENTER_DAY1_H0"),
        ("B02_LEAP_DAY15_H12","B02_LEAP_DAY16_H0"),
        ("B02_LEAP_LAST_H12","B02_LEAP_EXIT_H0"),
        ("B02_GREG_YEAR_END_H12","B02_GREG_YEAR_START_H0"),
    ]

    for row in rows:
        by_id={t["target"]["target_id"]:t for t in row["temporal"]}
        assert len(by_id)==18

        for t in by_id.values():
            for name in ("decadal","age","yearly","monthly","daily","hourly"):
                s=t["scopes"][name]
                assert 0 <= s["index"] <= 11
                assert len(s["palace_names"]) == 12
                assert len(s["mutagen"]) == 4
                if name != "age":
                    assert len(s["stars"]) == 12

        # 晚子时采用 forward：日干支/日四化/流日星、时干支/时四化/流时星
        # 应与下一公历日早子时相同。
        for late_id,next_id in same_day_pairs:
            late=by_id[late_id]; nxt=by_id[next_id]
            assert signature(late["scopes"]["daily"]) == signature(nxt["scopes"]["daily"]), (row["case_id"],late_id,"daily")
            assert signature(late["scopes"]["hourly"]) == signature(nxt["scopes"]["hourly"]), (row["case_id"],late_id,"hourly")

        # 农历换年：除夕晚子与正月初一早子属于同一日/时干支，
        # 但流年、流月层必须随农历年/月切换。
        eve=by_id["B02_CNY_EVE_H12"]; cny=by_id["B02_CNY_DAY_H0"]
        assert signature(eve["scopes"]["yearly"]) != signature(cny["scopes"]["yearly"])
        assert signature(eve["scopes"]["monthly"]) != signature(cny["scopes"]["monthly"])

        # 公历 12/31 -> 1/1 不是本配置的农历换年边界。
        yend=by_id["B02_GREG_YEAR_END_H12"]; ystart=by_id["B02_GREG_YEAR_START_H0"]
        assert signature(yend["scopes"]["yearly"]) == signature(ystart["scopes"]["yearly"])
        assert signature(yend["scopes"]["monthly"]) == signature(ystart["scopes"]["monthly"])

        # 普通农历初一：流月切换，流年不切。
        mend=by_id["B02_NORMAL_MONTH_PREV_H12"]; mstart=by_id["B02_NORMAL_MONTH_DAY1_H0"]
        assert signature(mend["scopes"]["yearly"]) == signature(mstart["scopes"]["yearly"])
        assert signature(mend["scopes"]["monthly"]) != signature(mstart["scopes"]["monthly"])

        # fixLeap=true：闰月前半沿用原月；进入闰月初一不立即切换流月。
        before_leap=by_id["B02_LEAP_ENTER_PREV_H12"]; leap1=by_id["B02_LEAP_ENTER_DAY1_H0"]
        assert signature(before_leap["scopes"]["monthly"]) == signature(leap1["scopes"]["monthly"])

        # 闰月 15/16 分界：16 日开始按下月处理。
        leap15h0=by_id["B02_LEAP_DAY15_H0"]; leap15h12=by_id["B02_LEAP_DAY15_H12"]; leap16=by_id["B02_LEAP_DAY16_H0"]
        assert signature(leap15h0["scopes"]["monthly"]) == signature(leap15h12["scopes"]["monthly"])
        assert signature(leap15h12["scopes"]["monthly"]) != signature(leap16["scopes"]["monthly"])

        # 闰月后半已经按下月处理，退出闰月时流月保持连续。
        leap_last=by_id["B02_LEAP_LAST_H12"]; leap_exit=by_id["B02_LEAP_EXIT_H0"]
        assert signature(leap_last["scopes"]["monthly"]) == signature(leap_exit["scopes"]["monthly"])

        # 同一公历闰日早子与晚子：年/月不变，但 forward 晚子进入下一日。
        leap_h0=by_id["B02_GREG_LEAP_H0"]; leap_h12=by_id["B02_GREG_LEAP_H12"]
        assert signature(leap_h0["scopes"]["yearly"]) == signature(leap_h12["scopes"]["yearly"])
        assert signature(leap_h0["scopes"]["monthly"]) == signature(leap_h12["scopes"]["monthly"])
        assert signature(leap_h0["scopes"]["daily"]) != signature(leap_h12["scopes"]["daily"])
        assert signature(leap_h0["scopes"]["hourly"]) != signature(leap_h12["scopes"]["hourly"])

    print("P1 B02 TEMPORAL INVARIANTS: PASS")
    print("cases=100 targets_per_case=18")
    print("verified=lunar_year_boundary,normal_month_boundary,leap_month_entry,leap_15_16_split,leap_exit,late_zi_forward,gregorian_year_nonboundary")
    return 0


if __name__=="__main__":
    raise SystemExit(main())
