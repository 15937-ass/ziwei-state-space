"""Bounded ZQX native PL1/PL2/PL3 diagnostic. Temporary PR only; do not merge."""
from __future__ import annotations
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import warnings

ROOT = Path(__file__).resolve().parents[1]
CASE = {"case_id":"zqx_anonymized","solar_date":"2004-02-25",
        "time_index":10,"gender":"女","algorithm":"zhongzhou",
        "day_divide":"forward","year_divide":"normal","horoscope_divide":"normal",
        "fix_leap":True}
ORACLE = [
    ("命","巳","己","天相","左辅 天马 天厨 天月 劫煞 天德"),
    ("兄弟","辰","戊","巨门","八座 恩光 台辅 蜚廉 华盖"),
    ("夫妻","卯","丁","紫微 贪狼","擎羊 大耗 龙德"),
    ("子女","寅","丙","天机 太阴","文曲 禄存 天姚 凤阁 天虚 年解"),
    ("财帛","丑","丁","天府","天魁 陀罗 地空 天喜 天才 月德"),
    ("疾厄","子","丙","太阳","文昌 火星 龙池 天伤 封诰 阴煞"),
    ("迁移","亥","乙","武曲 破军","孤辰"),
    ("交友","戌","甲","天同","天刑 三台 天使 天哭"),
    ("官禄","酉","癸","","右弼 地劫 天寿 天福 副截 天空 咸池 破碎"),
    ("田宅","申","壬","","铃星 解神 天巫 截空"),
    ("福德","未","辛","廉贞 七杀","天钺 红鸾 天官 副旬 寡宿"),
    ("父母","午","庚","天梁","天贵 旬空"),
]
BIRTH_MUTAGEN={"太阳":"忌","廉贞":"禄","破军":"权","武曲":"科"}


def chart_oracle():
    palaces={}
    for name,branch,stem,maj,other in ORACLE:
        def st(s):
            return {"name":s,"brightness":None,"mutagen":BIRTH_MUTAGEN.get(s),
                    "type":None,"scope":None}
        palaces[name]={
            "name":name,"branch":branch,"stem":stem,
            "is_body_palace":name=="财帛",
            "major_stars":[st(x) for x in maj.split() if x],
            "minor_stars":[st(x) for x in other.split() if x],
            "adjective_stars":[],
        }
    return {
        "schema_version":"0.1",
        "engine":{"name":"wenmo-input","version":"2.5.16","adapter_version":"manual-comparison"},
        "input":CASE, "chart":{"palaces":palaces},
    }


def notice(label,payload):
    # Pytest emits its warnings summary even under the existing CI's '-q'.
    compact=json.dumps(payload,ensure_ascii=False,sort_keys=True,separators=(",",":"))
    warnings.warn("ZQX_NATIVE_"+label+"="+compact[:7000],UserWarning,stacklevel=2)


def native_wealth(snapshot):
    from src.product.natal_domain_registry import load_default_natal_domain_registry
    registry=load_default_natal_domain_registry(ROOT)
    profile=registry.build_profile(snapshot)
    ids=[x.rule_id for x in profile.domains[0].active_rules]
    assert "W01-031" in ids, "wealth: 天府 W01-031 should trigger"
    assert len(registry.providers)==1
    assert not profile.feedback_used and not profile.empirical_calibration_used
    return profile,ids


def test_zqx_native_pl2_pl3_natal():
    profile,ids=native_wealth(chart_oracle())
    notice("PL2_PL3N_ORACLE",{
        "engine":"real repository WealthNatalDomainProvider / RuleRuntime / NatalStateProfile",
        "active_rule_count":len(ids),"active_rule_ids":ids,
        "profile_id":profile.profile_id,"canonical_fact_count":len(profile.canonical_facts),
        "named_structure_count":len(profile.named_structure_facts),
        "confidence_band":profile.domains[0].confidence_band,
    })


def run_command(args,timeout,**kwargs):
    try:
        p=subprocess.run(args,cwd=ROOT,text=True,capture_output=True,timeout=timeout,**kwargs)
        return {"ok":p.returncode==0,"returncode":p.returncode,
                "stdout":p.stdout[-2200:],"stderr":p.stderr[-2200:]}
    except Exception as e:
        return {"ok":False,"error":str(e)[:500]}


def test_zqx_native_p1_through_pl3_temporal():
    # CI runner can access package registries; current ChatGPT container cannot.
    p=run_command(["npm","install","--no-save","--no-package-lock","iztro@2.6.1"],150)
    if not p["ok"]:
        notice("P1_BLOCKED",{"step":"install iztro@2.6.1","result":p})
        return
    with tempfile.TemporaryDirectory() as td:
        inp=Path(td)/"input.jsonl"; manifest=Path(td)/"targets.json"; out=Path(td)/"iztro.jsonl"
        inp.write_text(json.dumps(CASE,ensure_ascii=False)+"\n",encoding="utf-8")
        targets=[{"target_id":str(y),"solar_date":f"{y}-06-15","time_index":6}
                 for y in (2026,2031,2034)]
        manifest.write_text(json.dumps({"targets":targets},ensure_ascii=False),encoding="utf-8")
        e=run_command(["node","tools/iztro_full_export.mjs",str(inp),str(manifest),str(out)],100)
        if not e["ok"]:
            notice("P1_BLOCKED",{"step":"native iztro_full_export.mjs","result":e})
            return
        full=json.loads(out.read_text(encoding="utf-8").splitlines()[0])
        native_p=full["natal"]["palaces"]
        bybranch={str(v["branch"]):v for v in native_p.values()}
        diffs=[]
        for name,branch,stem,maj,other in ORACLE:
            v=bybranch.get(branch)
            got=sorted(x["name"] for x in v["major_stars"]) if v else []
            expect=sorted(maj.split())
            if got!=expect: diffs.append({"palace":name,"branch":branch,"expected":expect,"p1":got})
        notice("PL1",{"engine":full["engine"],"natal_palaces":len(native_p),
                      "targets":len(full["temporal"]),"major_star_differences":diffs,
                      "soul_palace":full["natal"].get("soul_palace_branch"),
                      "body_palace":full["natal"].get("body_palace_branch")})
        # Explicit PL1 -> WP05 legacy name compatibility. Keep the original
        # PL1 snapshot unchanged so temporal adapter still sees engine output.
        # This is a boundary adapter in the diagnostic, not a rule rewrite.
        normalized=json.loads(json.dumps(full,ensure_ascii=False))
        aliases={"仆役":"交友"}
        conversions=[]
        for branch_key,palace in normalized["natal"]["palaces"].items():
            if palace["name"] in aliases:
                conversions.append({"branch":branch_key,"before":palace["name"],"after":aliases[palace["name"]]})
                palace["name"]=aliases[palace["name"]]
        notice("PL1_PL2_ALIASES",conversions)
        profile,ids=native_wealth(normalized)
        notice("PL2_PL3N_PL1_NATIVE",{"active_count":len(ids),"active_ids":ids,
                    "profile_id":profile.profile_id,
                    "knowledge_version":profile.knowledge_version})
        from src.product.temporal_asset_adapter import (
            adapt_target_from_full_snapshot, build_temporal_environment_from_assets)
        from src.product.temporal_reaction_compiler import (
            compile_temporal_reaction_registry, match_temporal_reactions)
        reaction_registry=json.loads((ROOT/"product/PL3T_TEMPORAL_REACTION_REGISTRY_v0.1.json").read_text(encoding="utf-8"))
        native_rules=compile_temporal_reaction_registry(reaction_registry)
        temporal=[]
        for year in (2026,2031,2034):
            b=adapt_target_from_full_snapshot(full,target_id=str(year))
            m=match_temporal_reactions(profile,b,native_rules)
            env=build_temporal_environment_from_assets(profile,b,reactions=m.matched)
            temporal.append({"year":year,"layers":env.active_layers,
                             "temporal_facts":len(env.temporal_facts),
                             "condition_facts":len(b.condition_facts),
                             "actual_reactions":len(env.reactions),
                             "profile_id":env.profile_id})
        notice("PL3T",{"compiled_production_reactions":len(native_rules),
                       "targets":temporal})
        # Independent x-iztro adapter is installed only after PL1+PL2+PL3 success.
        q=run_command([sys.executable,"-m","pip","install","--disable-pip-version-check",
                       "x-iztro==0.6.1"],150)
        if not q["ok"]:
            notice("P1_XIZTRO_BLOCKED",{"step":"pip install","result":q})
            return
        other=Path(td)/"xiztro.jsonl"
        # Independent x-iztro Rust adapter requires ASCII gender labels;
        # the JS engine accepts the Chinese upstream label instead.
        xinput=Path(td)/"xinput.jsonl"
        xcase=dict(CASE,gender="female")
        xinput.write_text(json.dumps(xcase,ensure_ascii=False)+"\n",encoding="utf-8")
        z=run_command([sys.executable,"tools/x_iztro_full_export.py",
                       str(xinput),str(manifest),str(other)],100)
        if not z["ok"]:
            notice("P1_XIZTRO_BLOCKED",{"step":"x_iztro_full_export","result":z})
            return
        compare=Path(td)/"diff.json"
        diff=run_command([sys.executable,"tools/p1_compare_full.py",
                          str(out),str(other),"--report",str(compare)],100)
        comp=json.loads(compare.read_text(encoding="utf-8")) if compare.exists() else {}
        notice("PL1_DUAL_ENGINE",{"comparison":comp,"command":diff})


def test_zqx_native_all_80_years_dual_engine_and_temporal():
    """80 annual targets, each manifest bounded to 8 targets per project guardrails."""
    from src.product.temporal_asset_adapter import adapt_target_from_full_snapshot
    if not (ROOT/"node_modules"/"iztro").exists():
        notice("80Y_BLOCKED",{"reason":"prior iztro installation unavailable"})
        return
    try:
        import x_iztro
    except ImportError as exc:
        notice("80Y_BLOCKED",{"reason":"x-iztro unavailable","detail":str(exc)})
        return
    summaries=[]
    total_target_count=0
    total_both_engine_diffs=0
    total_temporal_facts=0
    with tempfile.TemporaryDirectory() as td:
        base=Path(td)
        inp=base/"js.jsonl"; xp=base/"rust.jsonl"
        inp.write_text(json.dumps(CASE,ensure_ascii=False)+"\n",encoding="utf-8")
        xp.write_text(json.dumps(dict(CASE,gender="female"),ensure_ascii=False)+"\n",encoding="utf-8")
        for block in range(10):
            years=tuple(range(2006+block*8,2014+block*8))
            assert len(years)==8
            mf=base/f"targets_{block}.json"
            targets=[{"target_id":str(y),"solar_date":f"{y}-06-15","time_index":6}
                     for y in years]
            mf.write_text(json.dumps({"targets":targets}),encoding="utf-8")
            a=base/f"js_{block}.jsonl"; b=base/f"rust_{block}.jsonl"
            ra=run_command(["node","tools/iztro_full_export.mjs",str(inp),str(mf),str(a)],130)
            rb=run_command([sys.executable,"tools/x_iztro_full_export.py",str(xp),str(mf),str(b)],130)
            assert ra["ok"],f"JS PL1 block {block} failed: {ra}"
            assert rb["ok"],f"Rust PL1 block {block} failed: {rb}"
            js=json.loads(a.read_text(encoding="utf-8").splitlines()[0])
            rust=json.loads(b.read_text(encoding="utf-8").splitlines()[0])
            assert len(js["temporal"])==8==len(rust["temporal"])
            # Normalize only input metadata label, never computed natal/time results.
            raw_label=(js["input"]["gender"],rust["input"]["gender"])
            rust["input"]["gender"]=js["input"]["gender"]
            bb=base/f"rust_canonical_{block}.jsonl"
            bb.write_text(json.dumps(rust,ensure_ascii=False)+"\n",encoding="utf-8")
            report=base/f"diff_{block}.json"
            rd=run_command([sys.executable,"tools/p1_compare_full.py",
                            str(a),str(bb),"--report",str(report),"--fail-on-diff"],130)
            results=json.loads(report.read_text(encoding="utf-8")) if report.exists() else {}
            assert rd["ok"],f"PL1 dual engine chart diff at block {block}: {results}, {rd}"
            differences=results.get("total_differences",-1)
            total_both_engine_diffs+=differences
            total_target_count+=len(js["temporal"])
            c=0
            for yr in years:
                bundle=adapt_target_from_full_snapshot(js,target_id=str(yr))
                assert len(bundle.condition_facts)>0 and len(bundle.temporal_facts)>0
                c+=len(bundle.temporal_facts)
            total_temporal_facts+=c
            summaries.append({"from":years[0],"to":years[-1],
                "horoscope_snapshots":len(js["temporal"]),
                "computed_diff":differences,"scope_layers":6,
                "temporal_facts":c,"raw_gender_labels":raw_label})
    assert total_target_count==80
    assert total_both_engine_diffs==0
    notice("80Y_NATIVE_COMPLETE",{"batches":summaries,"targets":total_target_count,
                                   "computed_differences":total_both_engine_diffs,
                                   "total_temporal_facts":total_temporal_facts,
                                   "comparison_policy":"input.gender metadata only normalized, computed natal and horoscope unchanged"})
