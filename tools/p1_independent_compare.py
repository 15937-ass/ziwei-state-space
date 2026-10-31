#!/usr/bin/env python3
"""Independent-core audit: iztro zhongzhou projection vs pinned Go engine.

The Go engine is a separate implementation and is not configured as the canonical
Zhongzhou late-Zi oracle. This audit intentionally compares school-neutral/core
fields. A manifest identifies late-Zi targets as cross-school diagnostic targets;
those temporal targets are excluded from the hard equality gate rather than being
mislabeled as engine bugs. The canonical Zhongzhou production contract itself
uses day_divide=current and does not retain a next-day alternative.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

IZTRO_INDEX_BRANCH = ["寅","卯","辰","巳","午","未","申","酉","戌","亥","子","丑"]
KEY_STARS = {
    "紫微","天机","太阳","武曲","天同","廉贞","天府","太阴","贪狼","巨门","天相","天梁","七杀","破军",
    "文昌","文曲","左辅","右弼","天魁","天钺","擎羊","陀罗","火星","铃星","地空","地劫","禄存","天马",
}


def load(path):
    out={}
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        if line.strip():
            row=json.loads(line); out[row["case_id"]]=row
    return out


def target_core(target):
    return {key: target.get(key) for key in ("target_id", "solar_date", "time_index")}


def is_late_zi_birth(row):
    """Whether the canonical birth input uses late Zi (23:00-23:59)."""
    birth_input = row.get("input") or {}
    return birth_input.get("time_index") == 12


def iztro_projection(row, excluded_target_ids=None):
    excluded_target_ids = excluded_target_ids or set()
    natal=row["natal"]
    positions={}
    birth_mutagen={}
    dx=[]
    for branch,p in natal["palaces"].items():
        for group in ("major_stars","minor_stars","adjective_stars"):
            for s in p[group]:
                if s["name"] in KEY_STARS:
                    positions[s["name"]]=branch
                if s.get("mutagen"):
                    birth_mutagen[s["name"]]=s["mutagen"]
        if p.get("decadal"):
            dx.append({"range":p["decadal"]["range"],"branch":p["decadal"]["branch"]})
    dx.sort(key=lambda x:x["range"][0])

    temporal=[]
    for t in row["temporal"]:
        if t.get("target", {}).get("target_id") in excluded_target_ids:
            continue
        scopes={}
        for name,s in t["scopes"].items():
            scopes[name]={
                "palace_branch": IZTRO_INDEX_BRANCH[s["index"]],
                "stem":s["stem"],
                "branch":s["branch"],
                "palace_names":s["palace_names"],
                "mutagen":s["mutagen"],
                **({"stars":[sorted(x["name"] for x in group) for group in s["stars"]]} if name != "age" else {}),
                **({"nominal_age":s["nominal_age"]} if s.get("nominal_age") is not None else {}),
            }
        yd=t.get("yearly_dec_stars") or {}
        temporal.append({
            "target":target_core(t["target"]),
            "solar_date":t["solar_date"],
            "scopes":scopes,
            "suiqian12":[("大耗" if x == "岁破" else x) for x in yd.get("suiqian12",[])],
            "jiangqian12":yd.get("jiangqian12",[]),
        })
    return {
        "natal":{
            "soul_palace_branch":natal["soul_palace_branch"],
            "body_palace_branch":natal["body_palace_branch"],
            "five_elements_class":natal["five_elements_class"],
            "key_star_positions":positions,
            "birth_mutagen":birth_mutagen,
            "decadal":dx,
        },
        "temporal":temporal,
    }


def go_projection(row, excluded_target_ids=None):
    excluded_target_ids = excluded_target_ids or set()
    natal = dict(row["natal"])
    for key in ("lunar_year", "lunar_month", "lunar_day", "is_leap"):
        natal.pop(key, None)

    temporal = []
    for t in row["temporal"]:
        if t.get("target", {}).get("target_id") in excluded_target_ids:
            continue
        scopes = {}
        for name, s0 in t["scopes"].items():
            s = dict(s0)
            if name == "age":
                s.pop("stars", None)
            scopes[name] = s
        temporal.append({
            "target": target_core(t["target"]),
            "solar_date": t["solar_date"],
            "scopes": scopes,
            "suiqian12": [("大耗" if x == "岁破" else x) for x in t.get("suiqian12", [])],
            "jiangqian12": t.get("jiangqian12", []),
        })
    return {"natal": natal, "temporal": temporal}


def walk(a,b,path="",out=None):
    if out is None: out=[]
    if isinstance(a,dict) and isinstance(b,dict):
        for k in sorted(set(a)|set(b)):
            p=f"{path}.{k}" if path else k
            if k not in a or k not in b: out.append({"path":p,"left":a.get(k),"right":b.get(k)}); continue
            walk(a[k],b[k],p,out)
    elif isinstance(a,list) and isinstance(b,list):
        if len(a)!=len(b): out.append({"path":path+".length","left":len(a),"right":len(b)})
        for i,(x,y) in enumerate(zip(a,b)): walk(x,y,f"{path}[{i}]",out)
    elif a!=b:
        out.append({"path":path,"left":a,"right":b})
    return out


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("iztro")
    ap.add_argument("go")
    ap.add_argument("--report",required=True)
    ap.add_argument("--fail-on-core-diff",action="store_true")
    ap.add_argument("--school-sensitive-manifest")
    ap.add_argument("--max-total-diffs",type=int,default=500)
    ap.add_argument("--max-detail-per-case",type=int,default=100)
    args=ap.parse_args()

    excluded_target_ids=set()
    if args.school_sensitive_manifest:
        manifest=json.loads(Path(args.school_sensitive_manifest).read_text(encoding="utf-8"))
        excluded_target_ids=set(manifest.get("school_sensitive_target_ids", []))

    left=load(args.iztro); right=load(args.go)
    details=[]; total=0; cases=0; truncated=False
    late_zi_birth_cases=[]
    for cid in sorted(set(left)|set(right)):
        if cid not in left or cid not in right:
            d=[{"path":"record","left":cid in left,"right":cid in right}]
        elif is_late_zi_birth(left[cid]):
            # The pinned Go core is not configured with the canonical Zhongzhou
            # late-Zi same-day rule. Keep these records visible as diagnostics,
            # but do not let a cross-policy difference fail the hard gate.
            late_zi_birth_cases.append(cid)
            d=[]
        else:
            d=walk(
                iztro_projection(left[cid], excluded_target_ids),
                go_projection(right[cid], excluded_target_ids),
            )
        if d:
            cases+=1; total+=len(d); details.append({"case_id":cid,"difference_count":len(d),"differences":d[:args.max_detail_per_case]})
            if total >= args.max_total_diffs:
                truncated=True
                break
    hard_case_count=max(0,len(set(left)|set(right))-len(late_zi_birth_cases))
    report={
        "case_count":len(set(left)|set(right)),
        "hard_gate_case_count":hard_case_count,
        "excluded_late_zi_birth_case_ids":late_zi_birth_cases,
        "excluded_late_zi_birth_case_count":len(late_zi_birth_cases),
        "cases_with_differences":cases,
        "total_differences":total,
        "exact_case_agreement_rate":(hard_case_count-cases)/hard_case_count if hard_case_count else 0,
        "comparison_scope":"school-neutral natal core + temporal structural fields, excluding late-Zi birth cases because the Go core is not the canonical Zhongzhou day_divide=current oracle",
        "school_sensitive_target_ids_excluded_from_hard_gate":sorted(excluded_target_ids),
        "go_source_revision":"947166fc45cd7c8c0849da1bd870f570972a7172",
        "details":details,
        "truncated_at_difference_cap":truncated,
        "max_total_diffs":args.max_total_diffs,
        "max_detail_per_case":args.max_detail_per_case,
    }
    Path(args.report).write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print("P1 INDEPENDENT GO CORE AUDIT")
    print(f"cases={report['case_count']}")
    print(f"late_zi_birth_cases_excluded_from_hard_gate={len(late_zi_birth_cases)}")
    print(f"cases_with_differences={cases}")
    print(f"total_differences={total}")
    print(f"exact_case_agreement_rate={report['exact_case_agreement_rate']:.6f}")
    print(f"school_sensitive_target_ids_excluded={sorted(excluded_target_ids)}")
    if details:
        for item in details[:5]:
            print("CASE",item["case_id"],"diffs",item["difference_count"])
            for d in item["differences"][:15]:
                print(" ",d["path"],"LEFT=",d["left"],"RIGHT=",d["right"])
    if truncated:
        print(f"FAIL-FAST: difference cap reached ({args.max_total_diffs}); report is intentionally truncated")
        return 2
    return 1 if args.fail_on_core_diff and total else 0

if __name__=="__main__":
    raise SystemExit(main())
