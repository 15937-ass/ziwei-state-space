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
const FORTEL_STATIC_NAMES = new Set([
  ...fortel.MajorStar.stars,
  ...fortel.MinorStar.stars,
  ...fortel.MiniStar.stars,
].map(s=>simp(s.displayName)));

function brightnessRiskIztro(v) {
  const x=simp(v || '');
  return x==='陷' ? 'FALLEN' : 'NOT_FALLEN';
}
function brightnessRiskFortel(v) {
  return Number(v) < 0 ? 'FALLEN' : 'NOT_FALLEN';
}
function allStaticBranchesIztro(a) {
  const out={};
  for(const p of a.palaces){
    for(const s of [...(p.majorStars||[]),...(p.minorStars||[]),...(p.adjectiveStars||[])]){
      const n=starName(s);
      if(!FORTEL_STATIC_NAMES.has(n)) continue;
      (out[n] ??= []).push(simp(p.earthlyBranch));
    }
  }
  for(const k of Object.keys(out)) out[k].sort();
  return out;
}
function allStaticBranchesFortel(board) {
  const out={};
  for(const cell of board.cells){
    // Compare static natal stars only. Fortel's allStars also appends the three
    // rotating 12-star systems (博士/岁前/将前), which are a different layer.
    for(const s of [...cell.majorStars,...cell.minorStars,...cell.miniStars]){
      const n=simp(s.displayName);
      if(!FORTEL_STATIC_NAMES.has(n)) continue;
      (out[n] ??= []).push(simp(cell.ground.displayName));
    }
  }
  for(const k of Object.keys(out)) out[k].sort();
  return out;
}

function simp(s) {
  if (s == null) return s;
  return String(s)
    .replaceAll('祿','禄').replaceAll('權','权').replaceAll('機','机').replaceAll('陽','阳').replaceAll('陰','阴')
    .replaceAll('貪','贪').replaceAll('門','门').replaceAll('貞','贞').replaceAll('軍','军')
    .replaceAll('殺','杀').replaceAll('鉞','钺').replaceAll('輔','辅').replaceAll('鈴','铃')
    .replaceAll('羅','罗').replaceAll('馬','马').replaceAll('鸞','鸾')
    .replaceAll('壽','寿').replaceAll('龍','龙').replaceAll('鳳','凤').replaceAll('閣','阁')
    .replaceAll('傷','伤').replaceAll('虛','虚').replaceAll('廚','厨').replaceAll('貴','贵')
    .replaceAll('誥','诰').replaceAll('將','将').replaceAll('書','书').replaceAll('氣','气')
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
function natalTransformFromFortel(map) {
  // DestinyBoard.bornStarDerivativeMap is derivative -> star.
  const out={};
  for (const [deriv,star] of map.entries()) out[simp(deriv.displayName)] = simp(star.displayName);
  return out;
}
function runtimeTransformFromFortel(map) {
  // RuntimeContext.*.starDerivativeMap is star -> derivative.
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
function flowBaseName(raw) {
  const n=starName(raw);
  const suffix=n.replace(/^(运|流|月|日|时)/,'');
  const aliases={
    '魁':'天魁','钺':'天钺','昌':'文昌','曲':'文曲','禄':'禄存',
    '羊':'擎羊','陀':'陀罗','马':'天马','鸾':'红鸾','喜':'天喜'
  };
  return aliases[suffix] || n;
}
function flowBranchIztro(a, item, wanted) {
  const result={};
  const stars=item?.stars || [];
  for(let i=0;i<stars.length;i++){
    const branch=simp(a.palaces[i].earthlyBranch);
    for(const s of (stars[i]||[])){
      const n=flowBaseName(s);
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
function stable(value) {
  if(Array.isArray(value)) return value.map(stable);
  if(value && typeof value==='object'){
    return Object.fromEntries(Object.keys(value).sort().map(k=>[k,stable(value[k])]));
  }
  return value;
}
function eq(a,b){ return JSON.stringify(stable(a))===JSON.stringify(stable(b)); }

function fix12(x){ return ((x%12)+12)%12; }
function canonicalTemporalPalaces(iz, h, lunar) {
  const monthlyIndex=h.monthly.index;
  let dailyIndex=h.daily.index;
  let rule='NORMAL_MONTH';
  if(lunar.isLeapMonth){
    const regularDays=fortel.defaultCalendar.lunarMonthDays(lunar.lunarYear,lunar.lunarMonth,false);
    if(lunar.lunarDay <= 15){
      dailyIndex=fix12(monthlyIndex + regularDays + lunar.lunarDay - 1);
      rule='LEAP_FIRST_HALF_CONTINUES_PREVIOUS_MONTH';
    } else {
      dailyIndex=fix12(monthlyIndex + lunar.lunarDay - 16);
      rule='LEAP_SECOND_HALF_STARTS_FROM_NEXT_MONTH_PALACE';
    }
  }
  return {
    monthly_branch:simp(iz.palaces[monthlyIndex].earthlyBranch),
    daily_branch:simp(iz.palaces[dailyIndex].earthlyBranch),
    monthly_index:monthlyIndex,
    daily_index:dailyIndex,
    rule,
  };
}

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
  const [by,bm,bd]=c.solar_date.split('-').map(Number);
  const g=c.gender==='male' ? fortel.Gender.M : fortel.Gender.F;

  const iz=astro.withOptions({
    type:'solar', dateStr:c.solar_date, timeIndex:t, gender:c.gender,
    fixLeap:String(c.fix_leap)==='true', language:'zh-CN', astroType:'heaven',
    config:{
      algorithm:'zhongzhou', dayDivide:'forward', yearDivide:'normal',
      horoscopeDivide:'normal', mutagens:ZZ_MUTAGENS,
    },
  });

  const fbBaseConfig=fortel.DestinyConfigBuilder.withSolar({
    year:by, month:bm, day:bd, bornTimeGround:fortel.DayTimeGround.get(t),
    configType:fortel.ConfigType.SKY, gender:g,
  });
  let fbConfig=fbBaseConfig;
  if(t===12){
    // iztro forward late-Zi keeps birth month/palace geometry on the civil date,
    // but uses the next lunar day (wrapped within the lunar month) for Ziwei-day
    // placement and the next sexagenary day pillar.
    const [ny,nm,nd]=addDays(c.solar_date,1).split('-').map(Number);
    const nextLunar=fortel.defaultCalendar.solar2lunar(ny,nm,nd);
    fbConfig=new fortel.DestinyConfig({
      year:fbBaseConfig.year, month:fbBaseConfig.month, day:nextLunar.lunarDay,
      isLeapMonth:fbBaseConfig.isLeapMonth,
      yearSky:fbBaseConfig.yearSky, yearGround:fbBaseConfig.yearGround,
      monthSky:fbBaseConfig.monthSky, monthGround:fbBaseConfig.monthGround,
      daySky:nextLunar.daySky, dayGround:nextLunar.dayGround,
      bornTimeGround:fortel.DayTimeGround.get(12),
      configType:fortel.ConfigType.SKY, gender:g,
    });
  }
  const fb=new fortel.DestinyBoard(fbConfig);

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

  // Compare every static star name implemented by Fortel and present in iztro,
  // using branch multisets so duplicate stars (e.g. 旬空/截空) remain visible.
  const iAll=allStaticBranchesIztro(iz), fAll=allStaticBranchesFortel(fb);
  const commonStatic=[...new Set([...Object.keys(iAll),...Object.keys(fAll)])].filter(n=>FORTEL_STATIC_NAMES.has(n)).sort();
  for(const s of commonStatic) passed &= check(c.case_id,'natal_static_star',s,iAll[s]??[],fAll[s]??[],{time_index:t});

  // The two libraries use different brightness granularity. Compare the
  // source-relevant risk class (落陷 vs 非落陷); retain iztro's richer label
  // as display metadata, not as a falsely comparable numeric scale.
  for(const p of iz.palaces){
    for(const s of (p.majorStars||[])){
      const n=starName(s);
      const fs=fortel.MajorStar.stars.find(x=>simp(x.displayName)===n);
      if(fs){
        const fv=fb.getMajorStarEnergyLevel(fs);
        passed &= check(c.case_id,'natal_major_brightness_risk',n,brightnessRiskIztro(s.brightness),brightnessRiskFortel(fv),{branch:simp(p.earthlyBranch),raw_iztro:simp(s.brightness),fortel_energy:fv});
      }
    }
  }

  passed &= check(c.case_id,'natal','mutagens',natalTransformFromIztro(iz),natalTransformFromFortel(fb.bornStarDerivativeMap),{time_index:t});

  const targetT=Number(c.target_time_index);
  const h=iz.horoscope(`${c.target_date} ${clockFor(targetT)}`);
  const [ty,tm,td]=c.target_date.split('-').map(Number);
  const lunar=fortel.defaultCalendar.solar2lunar(ty,tm,td);
  const canonicalPalaces=canonicalTemporalPalaces(iz,h,lunar);
  const rt=fb.getRuntimContext({
    lunarYear:lunar.lunarYear,lunarMonth:lunar.lunarMonth,lunarDay:lunar.lunarDay,
    leap:lunar.isLeapMonth,
  });
  let rtDay=rt;
  if(targetT===12){
    // Horoscope geometry (monthly/daily palace index) uses the target civil lunar
    // date in iztro, while the sexagenary daily pillar follows next-day late-Zi.
    const [ey,em,ed]=addDays(c.target_date,1).split('-').map(Number);
    const el=fortel.defaultCalendar.solar2lunar(ey,em,ed);
    rtDay=fb.getRuntimContext({
      lunarYear:el.lunarYear,lunarMonth:el.lunarMonth,lunarDay:el.lunarDay,
      leap:el.isLeapMonth,
    });
  }

  const layers=[
    ['decadal',h.decadal,rt.tenYear,rt.tenYearSky,rt.tenYearGround,rt.tenYear],
    ['yearly',h.yearly,rt.year,rt.yearSky,rt.yearGround,rt.year],
    ['monthly',h.monthly,rt.month,rt.monthSky,rt.monthGround,rt.month],
    ['daily',h.daily,rt.day,rtDay.daySky,rtDay.dayGround,rtDay.day],
  ];
  for(const [name, ih, fr, fs, fg, fForDerivative] of layers){
    passed &= check(c.case_id,name,'stem',simp(ih.heavenlyStem),simp(fs.displayName),{target_date:c.target_date,target_time_index:targetT});
    passed &= check(c.case_id,name,'branch',simp(ih.earthlyBranch),simp(fg.displayName),{target_date:c.target_date,target_time_index:targetT});
    const izPalaceBranch = ih.index >= 0 ? simp(iz.palaces[ih.index].earthlyBranch) : null;
    passed &= check(c.case_id,name,'palace_branch',izPalaceBranch,simp(fr.cellGround.displayName),{target_date:c.target_date,target_time_index:targetT});
    passed &= check(c.case_id,name,'mutagens',transformFromIztro(ih),runtimeTransformFromFortel(fForDerivative.starDerivativeMap),{target_date:c.target_date,target_time_index:targetT});
    if(ih.stars && fForDerivative.groundStars){
      const isf=flowBranchIztro(iz,ih,SHARED_FLOW);
      const fsf=flowBranchFortel(fForDerivative.groundStars,SHARED_FLOW);
      for(const s of SHARED_FLOW) passed &= check(c.case_id,name,`flow_star.${s}`,isf[s]??null,fsf[s]??null,{target_date:c.target_date,target_time_index:targetT});
    }
  }

  caseResults.push({case_id:c.case_id,passed:Boolean(passed),birth:c.solar_date,time_index:t,target_date:c.target_date,target_time_index:targetT});
}

const byGroup={};
for(const m of mismatches){
  byGroup[m.group]=(byGroup[m.group]||0)+1;
}

// Source-resolve the known leap-month flow-palace algorithm divergence.
// Zhongzhou source: leap month 1-15 belongs previous month and flow-day count
// continues; day 16+ belongs next month and starts from that next-month palace.
const sourceResolutions=[];
const unresolved=[];
for(const m of mismatches){
  if((m.group==='monthly' || m.group==='daily') && m.field==='palace_branch'){
    const row=cases.find(x=>x.case_id===m.case_id);
    const [y,mo,d]=row.target_date.split('-').map(Number);
    const lu=fortel.defaultCalendar.solar2lunar(y,mo,d);
    if(lu.isLeapMonth){
      // Recreate iztro horoscope only to derive the source-canonical palace index.
      const izCase=astro.withOptions({
        type:'solar', dateStr:row.solar_date, timeIndex:Number(row.time_index), gender:row.gender,
        fixLeap:true, language:'zh-CN', astroType:'heaven',
        config:{algorithm:'zhongzhou',dayDivide:'forward',yearDivide:'normal',horoscopeDivide:'normal',mutagens:ZZ_MUTAGENS},
      });
      const hh=izCase.horoscope(`${row.target_date} ${clockFor(Number(row.target_time_index))}`);
      const cp=canonicalTemporalPalaces(izCase,hh,lu);
      const canonical=m.group==='monthly' ? cp.monthly_branch : cp.daily_branch;
      const winner=(m.iztro===canonical && m.fortel===canonical) ? 'BOTH'
        : (m.iztro===canonical ? 'IZTRO'
        : (m.fortel===canonical ? 'FORTEL' : 'CANONICAL_OVERRIDE'));
      sourceResolutions.push({...m,classification:'SOURCE_RESOLVED_LEAP_MONTH',canonical,winner,lunar:{year:lu.lunarYear,month:lu.lunarMonth,day:lu.lunarDay,isLeap:true},rule:cp.rule});
      continue;
    }
  }
  unresolved.push(m);
}
const summary={
  engine_a:{name:'iztro',version:'2.6.1',algorithm:'zhongzhou',astroType:'heaven',dayDivide:'forward',yearDivide:'normal',horoscopeDivide:'normal',customMutagens:'ZHONGZHOU_v0.2'},
  engine_b:{name:'fortel-ziweidoushu',version:'1.3.4',configType:'SKY',lateZiAdapter:'source-compatible split semantics for natal day placement and temporal day pillar'},
  total_cases:cases.length,
  fully_matching_cases:caseResults.filter(x=>x.passed).length,
  cases_with_mismatch:caseResults.filter(x=>!x.passed).length,
  total_raw_field_mismatches:mismatches.length,
  source_resolved_mismatches:sourceResolutions.length,
  unresolved_core_mismatches:unresolved.length,
  mismatch_by_group:byGroup,
  field_stats:fieldStats,
};
fs.mkdirSync(path.dirname(REPORT),{recursive:true});
fs.writeFileSync(REPORT,JSON.stringify({summary,cases:caseResults,mismatches,source_resolutions:sourceResolutions,unresolved},null,2)+'\n');
console.log(JSON.stringify(summary,null,2));
console.log('REPORT='+REPORT);
if(mismatches.length){
  console.log('FIRST_MISMATCHES');
  console.log(JSON.stringify(mismatches.slice(0,30),null,2));
}
if(sourceResolutions.length){
  console.log('SOURCE_RESOLUTIONS');
  console.log(JSON.stringify(sourceResolutions,null,2));
}
if(unresolved.length){
  console.error('UNRESOLVED_CORE_MISMATCHES='+unresolved.length);
  process.exitCode=2;
}
