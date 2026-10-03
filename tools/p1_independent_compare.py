#!/usr/bin/env python3
"""Independent-core audit: iztro zhongzhou projection vs pinned Go engine.

The Go engine is a separate implementation. It targets iztro/default historically,
so this audit intentionally compares only school-neutral/core fields.
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


def iztro_projection(row):
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
            "target":t["target"],
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


def go_projection(row):
    """Drop representation-only fields and normalize known school aliases."""
    natal = dict(row["natal"])
    for key in ("lunar_year", "lunar_month", "lunar_day", "is_leap"):
        natal.pop(key, None)

    temporal = []
    for t in row["temporal"]:
        scopes = {}
        for name, s0 in t["scopes"].items():
            s = dict(s0)
            if name == "age":
                s.pop("stars", None)
            scopes[name] = s
        temporal.append({
            "target": t["target"],
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
    args=ap.parse_args()
    left=load(args.iztro); right=load(args.go)
    details=[]; total=0; cases=0
    for cid in sorted(set(left)|set(right)):
        if cid not in left or cid not in right:
            d=[{"path":"record","left":cid in left,"right":cid in right}]
        else:
            d=walk(iztro_projection(left[cid]),go_projection(right[cid]))
        if d:
            cases+=1; total+=len(d); details.append({"case_id":cid,"difference_count":len(d),"differences":d[:300]})
    report={
        "case_count":len(set(left)|set(right)),
        "cases_with_differences":cases,
        "total_differences":total,
        "exact_case_agreement_rate":(len(left)-cases)/len(left) if left else 0,
        "comparison_scope":"school-neutral natal core + decadal/year/month/day/hour structural fields",
        "go_source_revision":"947166fc45cd7c8c0849da1bd870f570972a7172",
        "details":details,
    }
    Path(args.report).write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print("P1 INDEPENDENT GO CORE AUDIT")
    print(f"cases={report['case_count']}")
    print(f"cases_with_differences={cases}")
    print(f"total_differences={total}")
    print(f"exact_case_agreement_rate={report['exact_case_agreement_rate']:.6f}")
    if details:
        for item in details[:5]:
            print("CASE",item["case_id"],"diffs",item["difference_count"])
            for d in item["differences"][:15]:
                print(" ",d["path"],"LEFT=",d["left"],"RIGHT=",d["right"])
    return 1 if args.fail_on_core_diff and total else 0

if __name__=="__main__":
    raise SystemExit(main())
