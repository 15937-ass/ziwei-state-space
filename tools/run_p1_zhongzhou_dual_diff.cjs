#!/usr/bin/env node
'use strict';

const fs = require('node:fs');
const path = require('node:path');
const { astro } = require('iztro');
const fortel = require('fortel-ziweidoushu');

const INPUT = process.argv[2] || 'validation/product_chart_regression/regression_temporal_inputs_v0.2.csv';
const REPORT = process.argv[3] || 'validation/product_chart_regression/p1_zhongzhou_dual_diff_report.json';

const ZZ_MUTAGENS = {
  '甲': ['廉贞','破军','武曲','太阳'],
  '乙': ['天机','天梁','紫微','太阴'],
  '丙': ['天同','天机','文昌','廉贞'],
  '丁': ['太阴','天同','天机','巨门'],
  '戊': ['贪狼','太阴','太阳','天机'],
  '己': ['武曲','贪狼','天梁','文曲'],
  '庚': ['太阳','武曲','天府','天同'],
  '辛': ['巨门','太阳','文曲','文昌'],
  '壬': ['天梁','紫微','天府','武曲'],
  '癸': ['破军','巨门','太阴','贪狼'],
};

const MAJOR = ['紫微','天机','太阳','武曲','天同','廉贞','天府','太阴','贪狼','巨门','天相','天梁','七杀','破军'];
const SHARED_MINOR = ['禄存','天魁','天钺','文昌','文曲','左辅','右弼','地空','地劫','火星','铃星','擎羊','陀罗','天马'];
const SHARED_FLOW = ['禄存','天魁','天钺','文昌','文曲','擎羊','陀罗'];
const MUT_NAMES = ['禄','权','科','忌'];

function simp(s) {
  if (s == null) return s;
  return String(s)
    .replaceAll('祿','禄').replaceAll('機','机').replaceAll('陽','阳').replaceAll('陰','阴')
    .replaceAll('貪','贪').replaceAll('門','门').replaceAll('貞','贞').replaceAll('軍','军')
    .replaceAll('殺','杀').replaceAll('鉞','钺').replaceAll('輔','辅').replaceAll('鈴','铃')
    .replaceAll('遷','迁').replaceAll('財','财').replaceAll('僕','仆').replaceAll('業','业')
    .replaceAll('宮','宫').replaceAll('歲','岁').replaceAll('鸞','鸾');
}
function palaceName(s) {
  const x=simp(s);
  if (x==='事业' || x==='官禄') return '官禄';
  if (x==='交友' || x==='仆役' || x==='奴仆') return '交友';
  return x;
}
function starName(x) {
  if (x == null) return x;
  if (typeof x === 'string') return simp(x);
  return simp(x.name ?? x.displayName ?? x.toString?.());
}
function parseCSV(text) {
  const lines=text.trim().split(/\r?\n/);
  const head=lines[0].split(',');
  return lines.slice(1).filter(Boolean).map(line=>{
    const vals=line.split(',');
    return Object.fromEntries(head.map((h,i)=>[h,vals[i]]));
  });
}
function addDays(ymd, n) {
  const [y,m,d]=ymd.split('-').map(Number);
  const dt=new Date(Date.UTC(y,m-1,d)+n*86400000);
  return `${dt.getUTCFullYear()}-${String(dt.getUTCMonth()+1).padStart(2,'0')}-${String(dt.getUTCDate()).padStart(2,'0')}`;
}
function clockFor(t) {
  t=Number(t);
  if(t===0) return '00:30';
  if(t===12) return '23:30';
  return `${String(t*2-1).padStart(2,'0')}:30`;
}
function fortelTime(t) {
  // Product convention: late-Zi belongs to next civil date; after shifting date,
  // it is structurally the same Zi branch, so use early-Zi on the effective date.
  return Number(t)===12 ? 0 : Number(t);
}
function entriesTransformFromFortel(map) {
  const out={};
  for (const [star,deriv] of map.entries()) out[simp(deriv.displayName)] = simp(star.displayName);
  return out;
}
function transformFromIztro(item) {
  const arr=(item?.mutagen || []).map(starName);
  const out={};
  MUT_NAMES.forEach((m,i)=>{ out[m]=arr[i] ?? null; });
  return out;
}
function natalTransformFromIztro(a) {
  const out={};
  for(const p of a.palaces){
    for(const s of [...(p.majorStars||[]),...(p.minorStars||[]),...(p.adjectiveStars||[])]){
      if(s.mutagen) out[simp(s.mutagen)] = starName(s);
    }
  }
  return out;
}
function starBranchIztro(a, wanted) {
  const result={};
  for(const p of a.palaces){
    for(const s of [...(p.majorStars||[]),...(p.minorStars||[]),...(p.adjectiveStars||[])]){
      const n=starName(s);
      if(wanted.includes(n)) result[n]=simp(p.earthlyBranch);
    }
  }
  return result;
}
function starBranchFortel(board, wanted) {
  const result={};
  for(const c of board.cells){
    for(const s of [...c.majorStars,...c.minorStars,...c.miniStars]){
      const n=simp(s.displayName);
      if(wanted.includes(n)) result[n]=simp(c.ground.displayName);
    }
  }
  return result;
}
function flowBranchIztro(a, item, wanted) {
  const result={};
  const stars=item?.stars || [];
  for(let i=0;i<stars.length;i++){
    const branch=simp(a.palaces[i].earthlyBranch);
    for(const s of (stars[i]||[])){
      const n=starName(s);
      if(wanted.includes(n)) result[n]=branch;
    }
  }
  return result;
}
function flowBranchFortel(map, wanted) {
  const result={};
  for(const [g,stars] of map.entries()){
    for(const s of stars){
      const n=simp(s.displayName);
      if(wanted.includes(n)) result[n]=simp(g.displayName);
    }
  }
  return result;
}
function fortelPalaceByBranch(board) {
  const out={};
  for(const c of board.cells){
    const main=c.temples.find(t=>simp(t.displayName)!=='身宫');
    out[simp(c.ground.displayName)]={
      stem:simp(c.sky.displayName),
      branch:simp(c.ground.displayName),
      name:palaceName(main?.displayName),
      body:c.temples.some(t=>simp(t.displayName)==='身宫'),
      range:[c.ageStart,c.ageEnd],
    };
  }
  return out;
}
function iztroPalaceByBranch(a) {
  const out={};
  for(const p of a.palaces){
    out[simp(p.earthlyBranch)]={
      stem:simp(p.heavenlyStem), branch:simp(p.earthlyBranch), name:palaceName(p.name),
      body:Boolean(p.isBodyPalace), range:p.decadal?.range ?? null,
    };
  }
  return out;
}
function eq(a,b){ return JSON.stringify(a)===JSON.stringify(b); }

const cases=parseCSV(fs.readFileSync(INPUT,'utf8'));
const mismatches=[];
const caseResults=[];
const fieldStats={};
function check(caseId, group, field, a, b, meta={}) {
  const key=`${group}.${field}`;
  fieldStats[key] ??= {checks:0,mismatches:0};
  fieldStats[key].checks++;
  if(!eq(a,b)){
    fieldStats[key].mismatches++;
    mismatches.push({case_id:caseId,group,field,iztro:a,fortel:b,...meta});
    return false;
  }
  return true;
}

for(const c of cases){
  const t=Number(c.time_index);
  const effectiveBirth=t===12 ? addDays(c.solar_date,1) : c.solar_date;
  const [by,bm,bd]=effectiveBirth.split('-').map(Number);
  const g=c.gender==='male' ? fortel.Gender.M : fortel.Gender.F;

  const iz=astro.withOptions({
    type:'solar', dateStr:c.solar_date, timeIndex:t, gender:c.gender,
    fixLeap:String(c.fix_leap)==='true', language:'zh-CN', astroType:'heaven',
    config:{
      algorithm:'zhongzhou', dayDivide:'forward', yearDivide:'normal',
      horoscopeDivide:'normal', mutagens:ZZ_MUTAGENS,
    },
  });

  const fb=new fortel.DestinyBoard(fortel.DestinyConfigBuilder.withSolar({
    year:by, month:bm, day:bd, bornTimeGround:fortel.DayTimeGround.get(fortelTime(t)),
    configType:fortel.ConfigType.SKY, gender:g,
  }));

  let passed=true;
  passed &= check(c.case_id,'natal','five_elements',simp(iz.fiveElementsClass),simp(fb.element.displayName),{time_index:t});
  passed &= check(c.case_id,'natal','soul_star',starName(iz.soul),simp(fb.destinyMaster.displayName),{time_index:t});
  passed &= check(c.case_id,'natal','body_star',starName(iz.body),simp(fb.bodyMaster.displayName),{time_index:t});
  passed &= check(c.case_id,'natal','soul_palace_branch',simp(iz.earthlyBranchOfSoulPalace),simp(fb.destinyTempleCellGround.displayName),{time_index:t});

  const ip=iztroPalaceByBranch(iz), fp=fortelPalaceByBranch(fb);
  for(const br of Object.keys(ip).sort()){
    passed &= check(c.case_id,'natal_palace',`${br}.stem`,ip[br].stem,fp[br]?.stem,{time_index:t});
    passed &= check(c.case_id,'natal_palace',`${br}.name`,ip[br].name,fp[br]?.name,{time_index:t});
    passed &= check(c.case_id,'natal_palace',`${br}.body`,ip[br].body,fp[br]?.body,{time_index:t});
    passed &= check(c.case_id,'natal_palace',`${br}.decadal_range`,ip[br].range,fp[br]?.range,{time_index:t});
  }
  const imaj=starBranchIztro(iz,MAJOR), fmaj=starBranchFortel(fb,MAJOR);
  for(const s of MAJOR) passed &= check(c.case_id,'natal_major_star',s,imaj[s]??null,fmaj[s]??null,{time_index:t});
  const imin=starBranchIztro(iz,SHARED_MINOR), fmin=starBranchFortel(fb,SHARED_MINOR);
  for(const s of SHARED_MINOR) passed &= check(c.case_id,'natal_shared_minor_star',s,imin[s]??null,fmin[s]??null,{time_index:t});
  passed &= check(c.case_id,'natal','mutagens',natalTransformFromIztro(iz),entriesTransformFromFortel(fb.bornStarDerivativeMap),{time_index:t});

  const targetT=Number(c.target_time_index);
  const h=iz.horoscope(`${c.target_date} ${clockFor(targetT)}`);
  const effectiveTarget=targetT===12 ? addDays(c.target_date,1) : c.target_date;
  const [ty,tm,td]=effectiveTarget.split('-').map(Number);
  const lunar=fortel.defaultCalendar.solar2lunar(ty,tm,td);
  const rt=fb.getRuntimContext({
    lunarYear:lunar.lunarYear,lunarMonth:lunar.lunarMonth,lunarDay:lunar.lunarDay,
    leap:lunar.isLeapMonth,
  });

  const layers=[
    ['decadal',h.decadal,rt.tenYear,rt.tenYearSky,rt.tenYearGround],
    ['yearly',h.yearly,rt.year,rt.yearSky,rt.yearGround],
    ['monthly',h.monthly,rt.month,rt.monthSky,rt.monthGround],
    ['daily',h.daily,rt.day,rt.daySky,rt.dayGround],
  ];
  for(const [name, ih, fr, fs, fg] of layers){
    passed &= check(c.case_id,name,'stem',simp(ih.heavenlyStem),simp(fs.displayName),{target_date:c.target_date,target_time_index:targetT});
    passed &= check(c.case_id,name,'branch',simp(ih.earthlyBranch),simp(fg.displayName),{target_date:c.target_date,target_time_index:targetT});
    passed &= check(c.case_id,name,'palace_branch',simp(ih.earthlyBranch),simp(fr.cellGround.displayName),{target_date:c.target_date,target_time_index:targetT});
    passed &= check(c.case_id,name,'mutagens',transformFromIztro(ih),entriesTransformFromFortel(fr.starDerivativeMap),{target_date:c.target_date,target_time_index:targetT});
    if(ih.stars && fr.groundStars){
      const isf=flowBranchIztro(iz,ih,SHARED_FLOW);
      const fsf=flowBranchFortel(fr.groundStars,SHARED_FLOW);
      for(const s of SHARED_FLOW) passed &= check(c.case_id,name,`flow_star.${s}`,isf[s]??null,fsf[s]??null,{target_date:c.target_date,target_time_index:targetT});
    }
  }

  caseResults.push({case_id:c.case_id,passed:Boolean(passed),birth:c.solar_date,time_index:t,target_date:c.target_date,target_time_index:targetT});
}

const byGroup={};
for(const m of mismatches){
  byGroup[m.group]=(byGroup[m.group]||0)+1;
}
const summary={
  engine_a:{name:'iztro',version:'2.6.1',algorithm:'zhongzhou',astroType:'heaven',dayDivide:'forward',yearDivide:'normal',horoscopeDivide:'normal',customMutagens:'ZHONGZHOU_v0.2'},
  engine_b:{name:'fortel-ziweidoushu',version:'1.3.4',configType:'SKY',lateZiAdapter:'shift_to_next_date_then_early_Zi'},
  total_cases:cases.length,
  fully_matching_cases:caseResults.filter(x=>x.passed).length,
  cases_with_mismatch:caseResults.filter(x=>!x.passed).length,
  total_field_mismatches:mismatches.length,
  mismatch_by_group:byGroup,
  field_stats:fieldStats,
};
fs.mkdirSync(path.dirname(REPORT),{recursive:true});
fs.writeFileSync(REPORT,JSON.stringify({summary,cases:caseResults,mismatches},null,2)+'\n');
console.log(JSON.stringify(summary,null,2));
console.log('REPORT='+REPORT);
if(mismatches.length){
  console.log('FIRST_MISMATCHES');
  console.log(JSON.stringify(mismatches.slice(0,30),null,2));
}
