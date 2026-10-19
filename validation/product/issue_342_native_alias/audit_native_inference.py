"""Audit raw pinned exports through the real Career API; never repair input."""
import argparse
from collections import Counter
import copy
import hashlib
import json
from pathlib import Path

from src.product.career_inference_service import run_career_inference
from src.product.career_inference_report import build_career_inference_report
from src.product.palace_structure import load_palace_ontology, resolve_palace_structure


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('exports', nargs='+', type=Path)
    parser.add_argument('--report', type=Path, required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[3]
    ontology = load_palace_ontology(root / 'knowledge/wp05/palace_ontology_v0.1.csv')
    reports = []
    for path in args.exports:
        raw = path.read_bytes()
        snapshots = [json.loads(line) for line in raw.splitlines() if line.strip()]
        statuses, active_rules = Counter(), Counter()
        runs = facts_equal = natal_equal = preserved = 0
        for snapshot in snapshots:
            before = copy.deepcopy(snapshot)
            structure = resolve_palace_structure(snapshot, ontology)
            assert structure.palace('P08').observed_name == '仆役'
            # Comparison fixture only: not passed back to the raw caller or saved
            # as repaired input. Production never changes a snapshot name.
            comparison = copy.deepcopy(snapshot)
            comparison['natal']['palaces'][structure.palace('P08').branch]['name'] = '交友'
            expected = resolve_palace_structure(comparison, ontology)
            assert structure.runtime_facts() == expected.runtime_facts()
            facts_equal += 1
            for index, target in enumerate(snapshot['temporal']):
                target_id = target['target']['target_id']
                run = run_career_inference(root, snapshot, target_id=target_id, question='原始引擎事业路径内部验收')
                report = build_career_inference_report(root, run)
                assert run.status == 'PARTIAL_TEMPORAL_REGISTRY_EMPTY'
                assert run.blockers == ('PRODUCTION_TEMPORAL_REACTION_REGISTRY_EMPTY',)
                assert run.selected_temporal_layers == ('DECADE', 'YEAR')
                assert run.reaction_rule_count == 0
                assert run.reaction_report.matched == ()
                assert report['real_world_event_prediction_supported'] is False
                assert report['temporal']['matched_reaction_rule_ids'] == []
                for rule in report['natal']['active_rules']:
                    assert rule['rule_id'] in {'CA04-347', 'CA04-349', 'CA09-852'}
                    assert rule['source']['source_id'] == 'SRC-ZZ-003'
                    assert rule['source']['source_location']
                    active_rules[rule['rule_id']] += 1
                if index == 0:
                    control = run_career_inference(root, comparison, target_id=target_id, question=run.question)
                    assert run.natal_profile.to_dict() == control.natal_profile.to_dict()
                    natal_equal += 1
                statuses[run.status] += 1
                runs += 1
            assert snapshot == before
            preserved += 1
        reports.append({
            'file': path.name,
            'sha256': hashlib.sha256(raw).hexdigest(),
            'engine': snapshots[0]['engine'],
            'raw_natal_records': len(snapshots),
            'target_runs': runs,
            'status_counts': dict(statuses),
            'active_rule_counts': dict(active_rules),
            'source_trace_integrity': 'PASS',
            'canonical_fact_equivalence': facts_equal,
            'natal_profile_equivalence': natal_equal,
            'unchanged_raw_snapshots': preserved,
            'empirical_prediction_validated': False,
        })
        print(path.name, 'natal=', len(snapshots), 'runs=', runs, 'all PASS', flush=True)
    args.report.write_text(json.dumps({'exports': reports}, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    main()
