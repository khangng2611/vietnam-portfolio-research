"""Check the portable package, admitted inputs and standalone table reproduction."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    tests = subprocess.run([sys.executable, '-B', '-m', 'unittest', 'discover', '-s', 'reproducibility',
                            '-p', 'test_*.py', '-v'], cwd=ROOT, text=True, capture_output=True)
    if tests.returncode:
        raise RuntimeError(tests.stdout + tests.stderr)
    artifacts = ROOT / 'reproducibility/artifacts'
    artifacts.mkdir(exist_ok=True)
    (artifacts / 'tests.log').write_text(tests.stdout + tests.stderr)
    with tempfile.TemporaryDirectory(prefix='paper5-reproduce-') as temporary:
        command = [sys.executable, '-B', str(ROOT / 'code/reproduce.py'), '--output', temporary]
        process = subprocess.run(command, cwd=temporary, text=True, capture_output=True)
        if process.returncode:
            raise RuntimeError(process.stdout + process.stderr)
        summary = json.loads(process.stdout.strip().splitlines()[-1])
        for name in ['performance_metrics.csv', 'AB_reproduced_metrics.csv', 'drawdown_episodes.csv',
                     'class_contribution_summary.csv', 'contribution_reconciliation.csv']:
            actual = pd.read_csv(Path(temporary) / name)
            expected = pd.read_csv(ROOT / 'results/derived' / name)
            pd.testing.assert_frame_equal(actual, expected, check_exact=False, rtol=1e-12, atol=1e-12)
    source_map = json.loads((ROOT / 'reproducibility/source_map.json').read_text())
    for item in source_map:
        if sha(ROOT / item['released_path']) != item['released_sha256']:
            raise ValueError(f'Source-copy hash mismatch {item["released_path"]}')
    reference = ROOT / 'results/reference'
    metrics = pd.read_csv(ROOT / 'results/derived/performance_metrics.csv')
    if len(metrics) != 24 or summary['AB_metric_rows_reproduced'] != 128:
        raise ValueError('Unexpected metric row counts')
    if len(pd.read_csv(ROOT / 'data_public/series_dictionary.csv')) != 32:
        raise ValueError('Unexpected instrument count')
    contributions = pd.read_csv(reference / 'class_contributions.csv')
    if not np.isfinite(contributions[['equities', 'GOLD', 'VFF']]).all().all():
        raise ValueError('Nonfinite class contribution')
    statuses = pd.read_csv(ROOT / 'docs/deliverables.csv')
    if statuses.item.nunique() != 12:
        raise ValueError('Expected D01–D12')
    for name in ['prices_valuation.csv', 'aligned_prices.csv', 'result.pkl', '.env']:
        if list(ROOT.rglob(name)):
            raise ValueError(f'Restricted file in release candidate {name}')
    if pd.read_csv(reference / 'benchmark_status.csv').accepted_level_rows.sum() != 0:
        raise ValueError('Update benchmark status after admitting real data')
    summary.update(status='VERIFIED_RESEARCH_PACKAGE', tests_passed=9, original_source_mappings=len(source_map),
                   publication=statuses.loc[statuses.item.eq('D10'), 'status'].item(),
                   VN30TRI=statuses.loc[statuses.item.eq('D01'), 'status'].item())
    (ROOT / 'reproducibility/verification.json').write_text(json.dumps(summary, indent=2) + '\n')
    print(json.dumps(summary))


if __name__ == '__main__':
    main()
