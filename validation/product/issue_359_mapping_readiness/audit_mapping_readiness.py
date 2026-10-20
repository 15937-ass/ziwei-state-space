"""Bounded, read-only reconciliation of merged Career mappings and Product rules."""
import argparse
from collections import Counter
import csv
import hashlib
import json
from pathlib import Path

from src.product.career_natal_domain_provider import load_career_source_mappings
from src.product.palace_structure import load_palace_ontology
from src.product.registry_driven_natal_provider import RegistryDrivenNatalDomainProvider
from src.product.condition_atoms import compile_condition_spec

REGISTRY_PATH = 'product/PL3N_CAREER_DOMAIN_PROVIDER_v0.1.json'
MAPPING_PATHS = tuple('knowledge/wp07a/' + name for name in (
    'CAREER_NATAL_ATOMIZATION_MAP_v0.1.json',
    'CAREER_NATAL_TRANSFORMATION_MAP_CA01_CA03_v0.1.json',
    'CAREER_DIRECT_TRANSFORM_MAP_CA04_CA09_v0.1.json',
    'CAREER_CROSS_PALACE_MAP_CA01_066_CA02_188_CA03_255_v0.1.json',
    'CAREER_CONTEXT_MAP_CA01_020_v0.1.json',
    'CAREER_SPOUSE_KONGJIE_CA01_023_v0.1.json',
    'CAREER_STAR_PRESENCE_MAP_CA01_026_044_v0.1.json',
    'CAREER_CONTEXT_MAP_CA01_035_043_045_v0.1.json',
    'CAREER_ZIWEI_ZIPO_STATIC_8_MAP_v0.1.json',
    'CAREER_100_REVIEW_01_v0.1.json',
    'CAREER_100_REVIEW_02_v0.1.json',
    'CAREER_100_REVIEW_03_v0.1.json',
    'CAREER_100_REVIEW_04_v0.1.json',
))
SOURCE_PATHS = tuple(
    f'validation/wp05/CA{i:02d}_career_projection_review_{(i-1)*100+1:03d}_{i*100:03d}.csv'
    for i in range(1,9)
) + ('validation/wp05/CA09_career_projection_review_801_888.csv',)
STATIC = {
    'STATIC_PROJECTION_CANDIDATE_NOT_EXECUTABLE',
    'STATIC_CROSS_PALACE_CANDIDATE_NOT_EXECUTABLE',
    'STATIC_STAR_PRESENCE_CANDIDATE_NOT_EXECUTABLE',
}
NEXT_STEPS = {
    'BLOCKED_ILLUSTRATIVE_EXAMPLE_SCOPE_AND_CONTEXT_INHERITANCE_UNRESOLVED': '补足示例适用范围与前文继承的来源依据；不得直接泛化。',
    'BLOCKED_FIRE_BELL_AND_OR_UNRESOLVED': '取得适用于本句的量词证据；既有火铃证据审查尚未定解，不移植别段AND/OR。',
    'BLOCKED_METHODOLOGICAL_CONSTRAINT_NOT_OUTCOME_RULE': '保留为推断方法限制；不转成贫富结果或新增结果规则。',
    'BLOCKED_NON_CHART_ACTION_PREREQUISITE': '需获准表达并核实“勉强求变”行为前提；仅凭星曜上下文不足。',
    'BLOCKED_PATH_DEPENDENT_TARGET': '需明确历史次序、变化与定局的来源语义及运行契约；不得压成静态结果。',
    'BLOCKED_EVENT_LIKE_TARGET_REQUIRES_MANIFESTATION_REVIEW': '先完成显象语义审查；不由条件匹配直接推出人身攻击事件。',
    'BLOCKED_TIMING_TRIGGER_REQUIRES_TEMPORAL_SPEC': '需来源忠实的时间触发契约；不由本命单条件推年龄或时间窗口。',
}


def read_json(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def read_rows(path):
    with Path(path).open(encoding='utf-8-sig',newline='') as handle:
        return list(csv.DictReader(handle))


def audit(root, *, mapping_paths=MAPPING_PATHS, registry_document=None):
    root=Path(root)
    registry=registry_document if registry_document is not None else read_json(root/REGISTRY_PATH)
    selected=load_career_source_mappings(root,registry)
    provider=RegistryDrivenNatalDomainProvider(
        projection_rows=[r for p in registry['projection_sources'] for r in read_rows(root/p)],
        registry=registry,
        palace_ontology=load_palace_ontology(root/registry['palace_ontology']),
    )
    canonical={}
    for path in SOURCE_PATHS:
        for row in read_rows(root/path):
            rid=row['projection_rule_id']
            if rid in canonical:raise ValueError(f'duplicate canonical ID: {rid}')
            canonical[rid]=row
    mapped={};manifest=[]
    for path in mapping_paths:
        doc=read_json(root/path)
        entries=doc['mappings']
        ids=[m['source_rule_id'] for m in entries]
        if len(ids)!=len(set(ids)) or set(ids)!=set(doc['scope']['nominated_source_rule_ids']):
            raise ValueError(f'mapping nomination/duplicate mismatch: {path}')
        manifest.append({'path':path,'audit_id':doc['audit_id'],'sha256':hashlib.sha256((root/path).read_bytes()).hexdigest()})
        for item in entries:
            rid=item['source_rule_id']
            if rid in mapped:raise ValueError(f'duplicate mapping ID: {rid}')
            if rid not in canonical:raise ValueError(f'mapping missing canonical row: {rid}')
            row=canonical[rid];provenance=item['source_provenance']
            for field in ('source_id','source_location','review_status','time_layer'):
                if provenance[field]!=row[field]:raise ValueError(f'{rid}: canonical drift in {field}')
            if provenance.get('history_feedback','')!=row['history_feedback']:
                raise ValueError(f'{rid}: canonical drift in history_feedback')
            for field in ('source_span_verified','case_support_only'):
                if provenance[field] is not (row[field].lower()=='true'):
                    raise ValueError(f'{rid}: canonical drift in {field}')
            if item['source_condition_text']!=row['condition']:
                raise ValueError(f'{rid}: canonical drift in condition')
            for field,value in item['expected_projection'].items():
                if row[field]!=value:raise ValueError(f'{rid}: canonical drift in {field}')
            if item['executable_registry_entry'] is not False:
                raise ValueError(f'{rid}: Knowledge mapping must remain non-executable')
            readiness=item.get('execution_readiness')
            if rid in selected:
                status='COMPILED_IN_PRODUCT'
                if readiness and readiness.startswith('BLOCKED_'):
                    raise ValueError(f'{rid}: blocked mapping selected')
            elif readiness in NEXT_STEPS or (isinstance(readiness,str) and readiness.startswith('BLOCKED_')):
                status='BLOCKED'
            elif readiness in STATIC:
                condition=item.get('condition')
                if not isinstance(condition,dict) or not any(condition.values()):
                    raise ValueError(f'{rid}: incomplete static condition')
                compile_condition_spec(condition)
                status='STATIC_CANDIDATE_NOT_SELECTED'
            else:raise ValueError(f'{rid}: unreviewed mapping readiness')
            mapped[rid]={
                'source_rule_id':rid,'mapping_path':path,'classification':status,
                'execution_readiness':readiness,'mapping_status':item['mapping_status'],
                'source_condition_text':item['source_condition_text'],
                'source_provenance':provenance,'expected_projection':item['expected_projection'],
                'history_feedback_field_present_in_mapping':'history_feedback' in provenance,
                'canonical_history_feedback':row['history_feedback'],
                'condition_is_null':item.get('condition') is None,
                'next_requirement_zh':NEXT_STEPS.get(readiness,item.get('review_reason_zh','')),
                'automatic_activation_allowed':False,
            }
    if not set(selected)<=set(mapped):raise ValueError('Product selections missing from mapping inventory')
    counts=Counter(m['classification'] for m in mapped.values())
    if counts['COMPILED_IN_PRODUCT']!=provider.executable_rule_count:
        raise ValueError('compiled provider count mismatch')
    unmapped=[r for rid,r in canonical.items() if rid not in mapped]
    groups=Counter('CASE_SUPPORT_ONLY' if r['case_support_only'].lower()=='true'
                   else 'NON_NATAL_SOURCE_ONLY' if r['time_layer']!='NATAL'
                   else 'NATAL_WITHOUT_SCOPED_MAPPING' for r in unmapped)
    return {
        'audit_id':'PRODUCT_CAREER_MAPPING_READINESS_ISSUE_359',
        'scope':'Twelve explicitly listed merged mapping/context artifacts through Knowledge Review-03; no unmerged branch discovery',
        'counts':{'canonical_source_rows':len(canonical),'scoped_mapping_artifacts':len(manifest),
                  'unique_mapping_ids':len(mapped),'compiled_product_rules':provider.executable_rule_count,
                  'blocked_mapping_ids':counts['BLOCKED'],
                  'static_candidates_not_selected':counts['STATIC_CANDIDATE_NOT_SELECTED'],
                  'legacy_mapping_history_field_omissions':sum(not m['history_feedback_field_present_in_mapping'] for m in mapped.values()),
                  'source_rows_without_scoped_mapping':len(unmapped),
                  'unmapped_source_groups':dict(sorted(groups.items()))},
        'new_executable_rules_this_audit':0,'automatic_activation_allowed':False,
        'registry_document_sha256':hashlib.sha256(json.dumps(registry,sort_keys=True,ensure_ascii=False).encode()).hexdigest(),
        'source_manifest':manifest,
        'canonical_source_manifest':[{'path':p,'sha256':hashlib.sha256((root/p).read_bytes()).hexdigest()} for p in SOURCE_PATHS],
        'entries':[mapped[rid] for rid in sorted(mapped)],
        'limits':['Source-review counts are not executable-rule counts.',
                  'Static candidate readiness is not automatic Product approval.',
                  'Exclusion mentions and evidence spans are not additional mapped rule IDs.',
                  'Unmapped rows have not received executable-readiness review by this audit.',
                  'No empirical validation or temporal registry activation is established.'],
    }


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[3])
    parser.add_argument('--report',type=Path,required=True)
    args=parser.parse_args();report=audit(args.root)
    args.report.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report['counts'],ensure_ascii=False))


if __name__=='__main__':main()
