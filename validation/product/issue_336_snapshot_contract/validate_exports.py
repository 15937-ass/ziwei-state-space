"""Reproduce Issue #336's real-export compatibility gate (never repair input)."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path

from src.product.full_chart_snapshot_contract import validate_normalized_full_chart_snapshot


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('snapshots', nargs='+', type=Path)
    parser.add_argument('--report', required=True, type=Path)
    args = parser.parse_args()
    reports = []
    for path in args.snapshots:
        raw = path.read_bytes()
        records = [json.loads(line) for line in raw.splitlines() if line.strip()]
        checked = failed = 0
        shapes = Counter()
        errors = Counter()
        for snapshot in records:
            for target in snapshot['temporal']:
                scope = target['scopes']['age']
                shapes[(len(scope['palace_names']), len(scope['stars']))] += 1
                result = validate_normalized_full_chart_snapshot(
                    snapshot, target_id=target['target']['target_id'],
                )
                checked += 1
                failed += not result.ok
                errors.update(result.errors)
        reports.append({
            'file': path.name,
            'sha256': hashlib.sha256(raw).hexdigest(),
            'engine': records[0]['engine'],
            'natal_records': len(records),
            'selected_target_checks': checked,
            'passed': checked - failed,
            'failed': failed,
            'age_shapes': [
                {'palace_names': key[0], 'star_groups': key[1], 'count': count}
                for key, count in sorted(shapes.items())
            ],
            'error_counts': dict(sorted(errors.items())),
        })
    args.report.write_text(json.dumps({'exports': reports}, ensure_ascii=False, indent=2) + '\n')
    for report in reports:
        print(report['file'], 'checked=', report['selected_target_checks'],
              'passed=', report['passed'], 'failed=', report['failed'])
    return int(any(report['failed'] for report in reports))


if __name__ == '__main__':
    raise SystemExit(main())
