package ziwei

import (
	"bufio"
	"encoding/json"
	"fmt"
	"os"
	"reflect"
	"sort"
	"strings"
	"testing"
	"time"

	"liki-engine/internal/engine/ganzhi"
	"liki-engine/internal/engine/tianwen"
)

type p1Star struct { Name string `json:"name"` }
type p1Palace struct {
	EarthlyBranch string `json:"earthlyBranch"`
	MajorStars []p1Star `json:"majorStars"`
}
type p1RawLunar struct {
	LunarYear int `json:"lunarYear"`
	LunarMonth int `json:"lunarMonth"`
	LunarDay int `json:"lunarDay"`
	IsLeap bool `json:"isLeap"`
}
type p1Scope struct {
	EarthlyBranch string `json:"earthlyBranch"`
	PalaceNames []string `json:"palaceNames"`
	Mutagen []string `json:"mutagen"`
}
type p1Payload struct {
	FiveElementsClass string `json:"fiveElementsClass"`
	Soul string `json:"soul"`
	Body string `json:"body"`
	RawDates struct { LunarDate p1RawLunar `json:"lunarDate"` } `json:"rawDates"`
	Palaces []p1Palace `json:"palaces"`
	Yearly p1Scope `json:"yearly"`
	Monthly p1Scope `json:"monthly"`
	Daily p1Scope `json:"daily"`
	Hourly p1Scope `json:"hourly"`
}
type p1Record struct {
	Kind string `json:"kind"`
	CaseID string `json:"case_id"`
	TargetDate string `json:"target_date"`
	TargetTimeIndex int `json:"target_time_index"`
	Input map[string]string `json:"input"`
	Payload p1Payload `json:"payload"`
}

func p1ZhiName(z Zhi) string {
	names := []string{"", "子","丑","寅","卯","辰","巳","午","未","申","酉","戌","亥"}
	if int(z) < 1 || int(z) > 12 { return "" }
	return names[int(z)]
}

func p1Gender(s string) ganzhi.Gender {
	if s == "male" { return ganzhi.Male }
	return ganzhi.Female
}

func p1SiHuaOrdered(m siHuaResult) []string {
	out := []string{"","","",""}
	idx := map[siHuaType]int{HuaLu:0,HuaQuan:1,HuaKe:2,HuaJi:3}
	for star, typ := range m {
		if i, ok := idx[typ]; ok { out[i] = starName(star) }
	}
	return out
}

func p1MajorByBranch(c Chart) map[string][]string {
	out := map[string][]string{}
	for _, p := range c.GongWei {
		b := p.Zhi.String()
		for _, s := range p.Stars {
			if s.IsMajor { out[b] = append(out[b], s.Name) }
		}
		sort.Strings(out[b])
	}
	return out
}
func p1ExpectedMajor(ps []p1Palace) map[string][]string {
	out := map[string][]string{}
	for _, p := range ps {
		for _, s := range p.MajorStars { out[p.EarthlyBranch] = append(out[p.EarthlyBranch], s.Name) }
		sort.Strings(out[p.EarthlyBranch])
	}
	return out
}

func p1FlowNames(g [12]flowPalace) []string {
	out:=make([]string,12)
	for i:=range g { out[i]=g[i].Name }
	return out
}

func p1ParseDate(s string) time.Time {
	var y,m,d int
	fmt.Sscanf(s,"%d-%d-%d",&y,&m,&d)
	return time.Date(y,time.Month(m),d,0,0,0,0,time.FixedZone("CST",8*3600))
}

func TestP1ExternalCrossCheck(t *testing.T) {
	path := os.Getenv("P1_IZTRO_JSONL")
	if path == "" { t.Fatal("P1_IZTRO_JSONL missing") }
	f, err := os.Open(path)
	if err != nil { t.Fatal(err) }
	defer f.Close()

	charts := map[string]Chart{}
	var natal, temporal, checks, mismatches int
	byScope := map[string]int{}
	byField := map[string]int{}
	var samples []string

	mismatch := func(scope, caseID, field string, got, want any) {
		checks++
		if !reflect.DeepEqual(got,want) {
			mismatches++
			byScope[scope]++
			byField[scope+"."+field]++
			if len(samples)<30 { samples=append(samples,fmt.Sprintf("%s %s %s got=%v want=%v",caseID,scope,field,got,want)) }
		}
	}
	equal := func(scope,caseID,field string,got,want any){ mismatch(scope,caseID,field,got,want) }

	sc := bufio.NewScanner(f)
	buf:=make([]byte,64*1024)
	sc.Buffer(buf,16*1024*1024)
	for sc.Scan() {
		var r p1Record
		if err:=json.Unmarshal(sc.Bytes(),&r); err!=nil { t.Fatal(err) }
		if r.Kind=="natal" {
			natal++
			rl:=r.Payload.RawDates.LunarDate
			ti:=0
			fmt.Sscanf(r.Input["time_index"],"%d",&ti)
			shichen:=ti+1
			if ti==12 { shichen=1 }
			lt:=tianwen.LunarTime{Year:rl.LunarYear,Month:rl.LunarMonth,Day:rl.LunarDay,Leap:rl.IsLeap,Shichen:ganzhi.Zhi(shichen)}
			c,err:=ComputeChart(lt,p1Gender(r.Input["gender"]))
			if err!=nil { t.Fatalf("%s ComputeChart: %v",r.CaseID,err) }
			fc:=ComputeFullChart(c,0,0)
			charts[r.CaseID]=fc
			equal("natal",r.CaseID,"five_elements_class",fc.JuShuName,r.Payload.FiveElementsClass)
			equal("natal",r.CaseID,"soul",fc.MingZhu,r.Payload.Soul)
			equal("natal",r.CaseID,"body",fc.ShenZhu,r.Payload.Body)
			gotMajor:=p1MajorByBranch(fc)
			wantMajor:=p1ExpectedMajor(r.Payload.Palaces)
			for _,b:=range []string{"子","丑","寅","卯","辰","巳","午","未","申","酉","戌","亥"} {
				equal("natal",r.CaseID,"major@"+b,gotMajor[b],wantMajor[b])
			}
			continue
		}

		temporal++
		fc,ok:=charts[r.CaseID]
		if !ok { t.Fatalf("%s temporal before natal",r.CaseID) }

		target:=p1ParseDate(r.TargetDate)
		// 晚子时在 forward 口径下使用次日的历法日。
		if r.TargetTimeIndex==12 { target=target.Add(24*time.Hour) }
		lunar:=tianwen.SolarToLunar(tianwen.GregorianTime(target))
		td:=tianwen.LunarDate{Year:lunar.Year,Month:lunar.Month,Day:lunar.Day,Leap:lunar.Leap}

		ln:=ComputeLiuNian(fc,lunar.Year)
		equal("yearly",r.CaseID,"branch",p1ZhiName(ln.Zhi),r.Payload.Yearly.EarthlyBranch)
		equal("yearly",r.CaseID,"mutagen",p1SiHuaOrdered(ln.SiHua),r.Payload.Yearly.Mutagen)
		equal("yearly",r.CaseID,"palace_names",p1FlowNames(ln.GongWei),r.Payload.Yearly.PalaceNames)

		ly,err:=ComputeLiuYue(fc,td)
		if err!=nil { t.Fatalf("%s month: %v",r.CaseID,err) }
		equal("monthly",r.CaseID,"branch",p1ZhiName(ly.Zhi),r.Payload.Monthly.EarthlyBranch)
		equal("monthly",r.CaseID,"mutagen",p1SiHuaOrdered(ly.SiHua),r.Payload.Monthly.Mutagen)
		equal("monthly",r.CaseID,"palace_names",p1FlowNames(ly.GongWei),r.Payload.Monthly.PalaceNames)

		lr,err:=ComputeLiuRi(fc,td)
		if err!=nil { t.Fatalf("%s day: %v",r.CaseID,err) }
		equal("daily",r.CaseID,"branch",p1ZhiName(lr.Zhi),r.Payload.Daily.EarthlyBranch)
		equal("daily",r.CaseID,"mutagen",p1SiHuaOrdered(lr.SiHua),r.Payload.Daily.Mutagen)
		equal("daily",r.CaseID,"palace_names",p1FlowNames(lr.GongWei),r.Payload.Daily.PalaceNames)

		hz:=r.TargetTimeIndex+1
		if r.TargetTimeIndex==12 { hz=1 }
		lh,err:=ComputeLiuShi(fc,td,ganzhi.Zhi(hz))
		if err!=nil { t.Fatalf("%s hour: %v",r.CaseID,err) }
		equal("hourly",r.CaseID,"branch",p1ZhiName(lh.Zhi),r.Payload.Hourly.EarthlyBranch)
		equal("hourly",r.CaseID,"mutagen",p1SiHuaOrdered(lh.SiHua),r.Payload.Hourly.Mutagen)
		equal("hourly",r.CaseID,"palace_names",p1FlowNames(lh.GongWei),r.Payload.Hourly.PalaceNames)
	}
	if err:=sc.Err();err!=nil { t.Fatal(err) }
	fmt.Printf("P1_LIKI_SUMMARY natal=%d temporal=%d checks=%d mismatches=%d by_scope=%v by_field=%v\n",natal,temporal,checks,mismatches,byScope,byField)
	if len(samples)>0 { fmt.Printf("P1_LIKI_SAMPLES %s\n",strings.Join(samples," | ")) }
	if mismatches>0 { t.Logf("P1 third-engine diagnostic differences=%d; see mismatch ledger/report",mismatches) }
}
