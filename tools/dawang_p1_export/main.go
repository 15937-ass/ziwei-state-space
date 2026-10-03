package main

import (
	"bufio"
	"encoding/json"
	"fmt"
	"os"
	"sort"
	"strconv"
	"strings"

	"github.com/dawang20250107/ziweidoushu/internal/ziwei"
)

var branches = []string{"子","丑","寅","卯","辰","巳","午","未","申","酉","戌","亥"}

var keyStars = map[string]bool{
	"紫微":true,"天机":true,"太阳":true,"武曲":true,"天同":true,"廉贞":true,
	"天府":true,"太阴":true,"贪狼":true,"巨门":true,"天相":true,"天梁":true,"七杀":true,"破军":true,
	"文昌":true,"文曲":true,"左辅":true,"右弼":true,"天魁":true,"天钺":true,
	"擎羊":true,"陀罗":true,"火星":true,"铃星":true,"地空":true,"地劫":true,
	"禄存":true,"天马":true,
}

type Input struct {
	CaseID string `json:"case_id"`
	SolarDate string `json:"solar_date"`
	TimeIndex int `json:"time_index"`
	Gender string `json:"gender"`
}

type Target struct {
	TargetID string `json:"target_id"`
	SolarDate string `json:"solar_date"`
	TimeIndex int `json:"time_index"`
}
type TargetManifest struct { Targets []Target `json:"targets"` }

type EngineMeta struct {
	Name string `json:"name"`
	Version string `json:"version"`
	SourceRevision string `json:"source_revision"`
	AdapterVersion string `json:"adapter_version"`
}
type DX struct {
	Range [2]int `json:"range"`
	Branch string `json:"branch"`
}
type Natal struct {
	LunarYear int `json:"lunar_year"`
	LunarMonth int `json:"lunar_month"`
	LunarDay int `json:"lunar_day"`
	IsLeap bool `json:"is_leap"`
	SoulBranch string `json:"soul_palace_branch"`
	BodyBranch string `json:"body_palace_branch"`
	FiveElements string `json:"five_elements_class"`
	KeyStarPositions map[string]string `json:"key_star_positions"`
	BirthMutagen map[string]string `json:"birth_mutagen"`
	Decadal []DX `json:"decadal"`
}
type Scope struct {
	PalaceBranch string `json:"palace_branch"`
	Stem string `json:"stem"`
	Branch string `json:"branch"`
	PalaceNames []string `json:"palace_names"`
	Mutagen []string `json:"mutagen"`
	Stars [][]string `json:"stars"`
	NominalAge int `json:"nominal_age,omitempty"`
}
type Temporal struct {
	Target Target `json:"target"`
	SolarDate string `json:"solar_date"`
	Scopes map[string]Scope `json:"scopes"`
	Suiqian12 []string `json:"suiqian12"`
	Jiangqian12 []string `json:"jiangqian12"`
}
type Output struct {
	CaseID string `json:"case_id"`
	Engine EngineMeta `json:"engine"`
	Natal Natal `json:"natal"`
	Temporal []Temporal `json:"temporal"`
}

func parseDate(s string) (int,int,int,error) {
	p:=strings.Split(s,"-")
	if len(p)!=3 { return 0,0,0,fmt.Errorf("bad date %s",s) }
	y,e:=strconv.Atoi(p[0]); if e!=nil{return 0,0,0,e}
	m,e:=strconv.Atoi(p[1]); if e!=nil{return 0,0,0,e}
	d,e:=strconv.Atoi(p[2]); if e!=nil{return 0,0,0,e}
	return y,m,d,nil
}
func dateFmt(y,m,d int) string { return fmt.Sprintf("%04d-%02d-%02d",y,m,d) }

func iztroOrder(values [12]string) []string {
	out:=make([]string,12)
	for i:=0;i<12;i++ { b:=(i+2)%12; out[i]=values[b] }
	return out
}
func starGroupsIztroOrder(groups [][]ziwei.Star) [][]string {
	out:=make([][]string,12)
	for i:=0;i<12;i++ {
		b:=(i+2)%12
		names:=[]string{}
		if b < len(groups) {
			for _,s:=range groups[b] { names=append(names,s.Name) }
		}
		sort.Strings(names)
		out[i]=names
	}
	return out
}
func scope(s ziwei.HoroscopeScope) Scope {
	return Scope{
		PalaceBranch: branches[s.PalaceBranch],
		Stem:s.Stem,
		Branch:s.Branch,
		PalaceNames:iztroOrder(s.PalaceNames),
		Mutagen:[]string{s.Mutagen[0],s.Mutagen[1],s.Mutagen[2],s.Mutagen[3]},
		Stars:starGroupsIztroOrder(s.Stars),
		NominalAge:s.NominalAge,
	}
}

func render(in Input, targets []Target) (Output,error) {
	y,m,d,err:=parseDate(in.SolarDate); if err!=nil{return Output{},err}
	chart,err:=ziwei.Generate(ziwei.BirthInfo{
		Year:y,Month:m,Day:d,Hour:in.TimeIndex,Gender:ziwei.Gender(in.Gender),
	},ziwei.Options{ReferenceYear:2034})
	if err!=nil{return Output{},err}

	keyPos:=map[string]string{}
	birthMutagen:=map[string]string{}
	for _,p:=range chart.Palaces {
		for _,s:=range p.Stars {
			if keyStars[s.Name] { keyPos[s.Name]=branches[p.Branch] }
			if s.SiHua!="" { birthMutagen[s.Name]=string(s.SiHua) }
		}
	}
	dx:=make([]DX,0,len(chart.DaXians))
	for _,v:=range chart.DaXians {
		dx=append(dx,DX{Range:[2]int{v.StartAge,v.EndAge},Branch:branches[v.PalaceBranch]})
	}
	sort.Slice(dx,func(i,j int)bool{return dx[i].Range[0]<dx[j].Range[0]})

	temporal:=make([]Temporal,0,len(targets))
	for _,t:=range targets {
		ty,tm,td,e:=parseDate(t.SolarDate); if e!=nil{return Output{},e}
		h,e:=ziwei.GenerateHoroscope(chart,ty,tm,td,t.TimeIndex); if e!=nil{return Output{},e}
		scopes:=map[string]Scope{
			"decadal":scope(h.Decadal),"age":scope(h.Age),"yearly":scope(h.Yearly),
			"monthly":scope(h.Monthly),"daily":scope(h.Daily),"hourly":scope(h.Hourly),
		}
		temporal=append(temporal,Temporal{
			Target:t,SolarDate:dateFmt(ty,tm,td),Scopes:scopes,
			Suiqian12:iztroOrder(h.Suiqian12),Jiangqian12:iztroOrder(h.Jiangqian12),
		})
	}

	return Output{
		CaseID:in.CaseID,
		Engine:EngineMeta{Name:"dawang-go",Version:"pinned",SourceRevision:"947166fc45cd7c8c0849da1bd870f570972a7172",AdapterVersion:"0.1"},
		Natal:Natal{
			LunarYear:chart.LunarInfo.LunarYear,LunarMonth:chart.LunarInfo.LunarMonth,LunarDay:chart.LunarInfo.LunarDay,IsLeap:chart.LunarInfo.IsLeapMonth,
			SoulBranch:branches[chart.MingGongBranch],BodyBranch:branches[chart.ShenGongBranch],FiveElements:chart.WuxingJuName,
			KeyStarPositions:keyPos,BirthMutagen:birthMutagen,Decadal:dx,
		},
		Temporal:temporal,
	},nil
}

func main(){
	if len(os.Args)!=4 { panic("usage: p1export input.jsonl targets.json output.jsonl") }
	targetBytes,err:=os.ReadFile(os.Args[2]); if err!=nil{panic(err)}
	var manifest TargetManifest
	if err=json.Unmarshal(targetBytes,&manifest); err!=nil{panic(err)}
	inFile,err:=os.Open(os.Args[1]); if err!=nil{panic(err)}; defer inFile.Close()
	outFile,err:=os.Create(os.Args[3]); if err!=nil{panic(err)}; defer outFile.Close()
	w:=bufio.NewWriter(outFile); defer w.Flush()
	s:=bufio.NewScanner(inFile)
	count:=0
	for s.Scan(){
		if strings.TrimSpace(s.Text())=="" {continue}
		var in Input
		if err=json.Unmarshal([]byte(s.Text()),&in); err!=nil{panic(err)}
		row,err:=render(in,manifest.Targets); if err!=nil{panic(fmt.Sprintf("%s: %v",in.CaseID,err))}
		b,err:=json.Marshal(row); if err!=nil{panic(err)}
		fmt.Fprintln(w,string(b)); count++
	}
	if err=s.Err(); err!=nil{panic(err)}
	fmt.Printf("P1 dawang-go: wrote %d natal records and %d horoscope snapshots\n",count,count*len(manifest.Targets))
}
