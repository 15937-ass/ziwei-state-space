"""Compare current and canonical-main Career service behavior for Issue #336."""
import argparse
import json
from pathlib import Path
import runpy
import subprocess
import types

from src.product.career_inference_service import run_career_inference


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--base-ref', required=True)
    parser.add_argument('--raw-snapshot', type=Path, required=True)
    parser.add_argument('--target-id', required=True)
    parser.add_argument('--report', type=Path, required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[3]
    source = subprocess.check_output(
        ['git', 'show', f'{args.base_ref}:src/product/career_inference_service.py'],
        cwd=root, text=True,
    )
    baseline = types.ModuleType('src.product._baseline_career_service')
    baseline.__package__ = 'src.product'
    exec(compile(source, 'baseline:career_inference_service.py', 'exec'), baseline.__dict__)
    fixtures = runpy.run_path(str(root / 'tests/test_product_career_natal_domain_provider.py'))
    checks = []
    for star, mutagen in [(None, None), ('武曲', '科'), ('武曲', '忌'), ('破军', '禄')]:
        for empty_age in (False, True):
            stars = {'事业宫': [fixtures['_star'](star, mutagen)]} if star else {}
            snapshot = fixtures['_full_snapshot'](stars)
            if empty_age:
                snapshot['temporal'][0]['scopes']['age']['stars'] = []
            kwargs = dict(target_id='T-DEMO', question='Issue #336 behavior invariance')
            old = baseline.run_career_inference(root, snapshot, **kwargs)
            new = run_career_inference(root, snapshot, **kwargs)
            checks.append({'star': star, 'mutagen': mutagen, 'empty_age': empty_age,
                           'identical': old.to_dict() == new.to_dict(), 'status': new.status})
    raw = json.loads(args.raw_snapshot.read_text())
    results = {}
    for label, fn in [('canonical_main', baseline.run_career_inference), ('candidate', run_career_inference)]:
        try:
            run = fn(root, raw, target_id=args.target_id, question='raw exporter compatibility')
            results[label] = {'status': run.status}
        except ValueError as error:
            results[label] = {'error_type': type(error).__name__, 'error': str(error)}
    report = {
        'baseline_commit': subprocess.check_output(['git', 'rev-parse', args.base_ref], cwd=root, text=True).strip(),
        'normalized_fixture_comparisons': checks,
        'raw_export_service_comparison': results,
        'raw_behavior_unchanged': results['canonical_main'] == results['candidate'],
        'known_limitation': 'PREEXISTING_PALACE_ALIAS_LIMITATION' if 'error' in results['candidate'] else None,
    }
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print('normalized fixture equality:', sum(x['identical'] for x in checks), '/', len(checks))
    print('raw exporter baseline parity:', report['raw_behavior_unchanged'])
    print('raw exporter limitation:', report['known_limitation'])
    return int(not all(x['identical'] for x in checks) or not report['raw_behavior_unchanged'])


if __name__ == '__main__':
    raise SystemExit(main())
