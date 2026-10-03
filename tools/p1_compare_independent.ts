import fs from "node:fs";
import path from "node:path";
import { pathToFileURL } from "node:url";
import { astro } from "iztro";

const inputsPath = process.argv[2] || "validation/product_chart_regression/regression_inputs_v0.1.csv";
const independentRoot = process.env.INDEPENDENT_ENGINE_ROOT || "/tmp/ziwei-independent";

function parseCsv(text: string): Record<string,string>[] {
  const lines = text.trim().split(/\r?\n/);
  const header = lines[0].split(",");
  return lines.slice(1).map(line => {
    const vals = line.split(",");
    return Object.fromEntries(header.map((h,i)=>[h,vals[i]]));
  });
}

function addDays(dateStr: string, n: number): string {
  const [y,m,d] = dateStr.split("-").map(Number);
  const dt = new Date(Date.UTC(y,m-1,d+n));
  return dt.toISOString().slice(0,10);
}

function birthClock(row: Record<string,string>) {
  const ti = Number(row.time_index);
  if (ti === 12) return { date: addDays(row.solar_date, 1), hour: 0, minute: 30 };
  if (ti === 0) return { date: row.solar_date, hour: 0, minute: 30 };
  return { date: row.solar_date, hour: ti * 2, minute: 0 };
}

const chartMod = await import(pathToFileURL(path.join(independentRoot, "src/core/chart.ts")).href);
const annualMod = await import(pathToFileURL(path.join(independentRoot, "src/core/fortune/annual.ts")).href);
const { createChart } = chartMod;
const { getYearStem, getYearBranch, getFlowMonthPalace, getFlowDayPalace } = annualMod;

const rows = parseCsv(fs.readFileSync(inputsPath, "utf8"));
const targetDates = ["2025-01-29","2025-06-21","2026-02-17","2026-09-23"];
const branchFromOneBased = ["","子","丑","寅","卯","辰","巳","午","未","申","酉","戌","亥"];

let checks = 0;
let mismatches:any[] = [];
const categoryCount:Record<string,number> = {};

function check(caseId:string, category:string, field:string, a:any, b:any, context:any={}) {
  checks++;
  if (a !== b) {
    mismatches.push({case_id:caseId, category, field, iztro:a, independent:b, ...context});
    categoryCount[category] = (categoryCount[category]||0)+1;
  }
}

for (const row of rows) {
  const ti=Number(row.time_index);
  const cfg = {algorithm:"zhongzhou", dayDivide:"forward", yearDivide:"normal", horoscopeDivide:"normal", ageDivide:"normal"} as const;
  const iz = astro.withOptions({
    type:"solar", dateStr:row.solar_date, timeIndex:ti, gender:row.gender,
    fixLeap:true, language:"zh-CN", config:cfg,
  });
  const izJson:any = iz.toJSON();

  const bc = birthClock(row);
  const [y,m,d] = bc.date.split("-").map(Number);
  const ind:any = createChart({
    year:y, month:m, day:d, hour:bc.hour, minute:bc.minute,
    gender:row.gender==="male"?"男":"女", school:"sanhe", isLunar:false,
  });

  check(row.case_id,"natal","soul_palace_branch",izJson.earthlyBranchOfSoulPalace,branchFromOneBased[ind.mingPalace],{time_index:ti});
  check(row.case_id,"natal","body_palace_branch",izJson.earthlyBranchOfBodyPalace,branchFromOneBased[ind.shenPalace],{time_index:ti});
  check(row.case_id,"natal","five_elements_class",izJson.fiveElementsClass,ind.elementPhase,{time_index:ti});
  check(row.case_id,"natal","soul_star",izJson.soul,ind.mingMaster,{time_index:ti});
  check(row.case_id,"natal","body_star",izJson.body,ind.shenMaster,{time_index:ti});

  const izMajor = new Map<string,string>();
  for (const p of izJson.palaces) for (const s of p.majorStars||[]) izMajor.set(s.name,p.earthlyBranch);
  const indMajor = new Map<string,string>();
  for (const p of ind.palaces) for (const s of p.mainStars||[]) indMajor.set(s,p.branch);
  for (const star of ["紫微","天机","太阳","武曲","天同","廉贞","天府","太阴","贪狼","巨门","天相","天梁","七杀","破军"]) {
    check(row.case_id,"major_star",star,izMajor.get(star),indMajor.get(star),{time_index:ti});
  }

  for (const target of targetDates) {
    const h:any=iz.horoscope(target,0).toJSON();
    const [ty,tm,td]=target.split("-").map(Number);
    check(row.case_id,"yearly","stem",h.yearly.heavenlyStem,getYearStem(ty),{target});
    check(row.case_id,"yearly","branch",h.yearly.earthlyBranch,getYearBranch(ty),{target});

    // Independent core exposes branch/palace progression for flow month/day.
    // We compare only on the target solar month/day as an independent structural sanity check.
    const monthBranch=branchFromOneBased[getFlowMonthPalace(ty,tm)];
    const dayBranch=branchFromOneBased[getFlowDayPalace(ty,tm,td)];
    check(row.case_id,"monthly_oracle","earthly_branch",h.monthly.earthlyBranch,monthBranch,{target,oracle:"independent_core_simplified"});
    check(row.case_id,"daily_oracle","earthly_branch",h.daily.earthlyBranch,dayBranch,{target,oracle:"independent_core_simplified"});
  }
}

const out={
  engine:"yzhi1065-bot/ziwei-dou-shu self core",
  engine_revision:"master@runtime-clone",
  cases:rows.length,
  checks,
  mismatch_count:mismatches.length,
  mismatch_by_category:categoryCount,
  first_mismatches:mismatches.slice(0,200),
  note:"monthly/day oracle is explicitly simplified in upstream independent core; disagreements there are diagnostic, not automatic iztro failures."
};
console.log("P1_INDEPENDENT_SUMMARY="+JSON.stringify(out));
fs.writeFileSync("/tmp/p1_independent_mismatches.jsonl",mismatches.map(x=>JSON.stringify(x)).join("\n")+(mismatches.length?"\n":""));
