#!/usr/bin/env node
/**
 * Build deterministic P1 B02 temporal boundary targets from pinned lunar-lite.
 *
 * The selector scan is deterministic. The generated target list is printed and
 * written as JSON so CI artifacts preserve the exact dates used.
 */
import fs from "node:fs";
import lunarLite from "lunar-lite";

const { solar2lunar } = lunarLite;
const [outputPath] = process.argv.slice(2);
if (!outputPath) throw new Error("Usage: node tools/build_p1_edge_targets.mjs output.json");

function pad(n) { return String(n).padStart(2, "0"); }
function fmt(date) {
  return `${date.getUTCFullYear()}-${pad(date.getUTCMonth()+1)}-${pad(date.getUTCDate())}`;
}
function parse(s) {
  const [y,m,d] = s.split("-").map(Number);
  return new Date(Date.UTC(y,m-1,d));
}
function addDays(s, delta) {
  const d=parse(s); d.setUTCDate(d.getUTCDate()+delta); return fmt(d);
}

const days=[];
for(let d=parse("2032-01-01"), end=parse("2035-12-31"); d<=end; d=new Date(d.getTime()+86400000)) {
  const solar=fmt(d);
  const l=solar2lunar(solar);
  days.push({solar,lunarYear:l.lunarYear,lunarMonth:l.lunarMonth,lunarDay:l.lunarDay,isLeap:Boolean(l.isLeap)});
}

const first=(fn,label)=>{
  const x=days.find(fn);
  if(!x) throw new Error("boundary selector not found: "+label);
  return x;
};

// Use the first complete examples in a fixed scan window.
const cny=first(x=>!x.isLeap && x.lunarMonth===1 && x.lunarDay===1 && x.solar>="2033-01-01","CNY");
const regularMonthStart=first(x=>!x.isLeap && x.lunarMonth===5 && x.lunarDay===1 && x.solar>cny.solar,"regular month start");
const leapStart=first(x=>x.isLeap && x.lunarDay===1,"leap month start");
const leap15=first(x=>x.isLeap && x.lunarYear===leapStart.lunarYear && x.lunarMonth===leapStart.lunarMonth && x.lunarDay===15,"leap day 15");
const leap16=first(x=>x.isLeap && x.lunarYear===leapStart.lunarYear && x.lunarMonth===leapStart.lunarMonth && x.lunarDay===16,"leap day 16");
const leapDays=days.filter(x=>x.isLeap && x.lunarYear===leapStart.lunarYear && x.lunarMonth===leapStart.lunarMonth);
const leapLast=leapDays[leapDays.length-1];

const targets=[
  {target_id:"B02_GREG_LEAP_H0",solar_date:"2032-02-29",time_index:0,edge:"gregorian_leap_day_early_zi"},
  {target_id:"B02_GREG_LEAP_H12",solar_date:"2032-02-29",time_index:12,edge:"gregorian_leap_day_late_zi"},

  {target_id:"B02_CNY_EVE_H11",solar_date:addDays(cny.solar,-1),time_index:11,edge:"lunar_year_end_hai"},
  {target_id:"B02_CNY_EVE_H12",solar_date:addDays(cny.solar,-1),time_index:12,edge:"lunar_year_end_late_zi_forward"},
  {target_id:"B02_CNY_DAY_H0",solar_date:cny.solar,time_index:0,edge:"lunar_new_year_early_zi"},
  {target_id:"B02_CNY_DAY_H1",solar_date:cny.solar,time_index:1,edge:"lunar_new_year_chou"},

  {target_id:"B02_NORMAL_MONTH_PREV_H12",solar_date:addDays(regularMonthStart.solar,-1),time_index:12,edge:"normal_month_end_late_zi"},
  {target_id:"B02_NORMAL_MONTH_DAY1_H0",solar_date:regularMonthStart.solar,time_index:0,edge:"normal_month_first_day"},

  {target_id:"B02_LEAP_ENTER_PREV_H12",solar_date:addDays(leapStart.solar,-1),time_index:12,edge:"before_leap_month_late_zi"},
  {target_id:"B02_LEAP_ENTER_DAY1_H0",solar_date:leapStart.solar,time_index:0,edge:"leap_month_first_day"},
  {target_id:"B02_LEAP_DAY15_H0",solar_date:leap15.solar,time_index:0,edge:"leap_month_first_half_day15"},
  {target_id:"B02_LEAP_DAY15_H12",solar_date:leap15.solar,time_index:12,edge:"leap_month_day15_late_zi"},
  {target_id:"B02_LEAP_DAY16_H0",solar_date:leap16.solar,time_index:0,edge:"leap_month_second_half_day16"},
  {target_id:"B02_LEAP_LAST_H12",solar_date:leapLast.solar,time_index:12,edge:"leap_month_last_day_late_zi"},
  {target_id:"B02_LEAP_EXIT_H0",solar_date:addDays(leapLast.solar,1),time_index:0,edge:"first_day_after_leap_month"},

  {target_id:"B02_GREG_YEAR_END_H12",solar_date:"2033-12-31",time_index:12,edge:"gregorian_year_end_late_zi"},
  {target_id:"B02_GREG_YEAR_START_H0",solar_date:"2034-01-01",time_index:0,edge:"gregorian_year_start_early_zi"},
  {target_id:"B02_BASELINE_DAYTIME",solar_date:"2034-08-03",time_index:6,edge:"ordinary_control"}
];

const unique=new Set(targets.map(x=>x.target_id));
if(unique.size!==targets.length) throw new Error("duplicate target_id");
if(targets.length!==18) throw new Error("expected 18 B02 targets");

const manifest={
  version:"0.3",
  generated_with:"lunar-lite@0.2.8",
  scan_window:["2032-01-01","2035-12-31"],
  selected_lunar_boundaries:{
    cny,
    regular_month_start:regularMonthStart,
    leap_month_start:leapStart,
    leap_month_day15:leap15,
    leap_month_day16:leap16,
    leap_month_last:leapLast
  },
  targets
};

fs.writeFileSync(outputPath,JSON.stringify(manifest,null,2)+"\n","utf8");
console.log(JSON.stringify(manifest,null,2));
