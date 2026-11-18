"""Evaluate publicly displayed Dragon Capital index observations for private research."""
import argparse
import hashlib
import importlib.metadata
import json
import platform
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'code'))
from benchmark import evaluate_levels


def normalize_history(payload):
    data = payload['returnValue']
    dates = data['fundDates']
    rows = data['fundBenchmarkData']
    if len(rows) != len(dates) or [r.get('navDate') for r in rows] != dates:
        raise ValueError('Benchmark observations do not match source date vector')
    if len(dates) != len(set(dates)):
        raise ValueError('Duplicate source dates')
    available = [r for r in rows if r.get('navPrice') is not None]
    if not available or any(r.get('navCurrency') != 'VND' for r in available):
        raise ValueError('Requires nonempty VND index levels')
    frame = pd.DataFrame(available).rename(columns={'navDate': 'index_date', 'navPrice': 'index_level'})
    frame['index_date'] = pd.to_datetime(frame.index_date, errors='raise')
    frame['index_level'] = pd.to_numeric(frame.index_level, errors='raise')
    if not np.isfinite(frame.index_level).all() or (frame.index_level <= 0).any():
        raise ValueError('Index levels must be finite and positive')
    return frame[['index_date', 'index_level']].sort_values('index_date').reset_index(drop=True)


def reconstruct_three_sessions(levels, price_levels):
    """Sensitivity only: assume no dividend yield during the three observed flat sessions."""
    tri = levels.set_index('index_date').index_level.copy()
    price = price_levels.set_index('index_date').index_level
    dates = pd.to_datetime(['2025-05-05', '2025-05-06', '2025-05-07'])
    left, right = pd.Timestamp('2025-04-29'), pd.Timestamp('2025-05-08')
    if not tri.loc[dates].eq(tri.loc[left]).all():
        raise ValueError('Expected three flat source observations')
    scale = tri.loc[left] / price.loc[left]
    bracket_error = float(scale * price.loc[right] - tri.loc[right])
    if abs(bracket_error) > .02:
        raise ValueError('No-dividend factor fails the right-end rounding check')
    replacement = (price.loc[dates] * scale).round(2)
    audit = pd.DataFrame({'date': dates, 'reported_level': tri.loc[dates].to_numpy(),
                          'sensitivity_level': replacement.to_numpy(),
                          'method': 'constant_TRI_price_factor_from_2025-04-29',
                          'right_bracket_error_points': bracket_error})
    tri.loc[dates] = replacement
    return tri.rename('index_level').reset_index(), audit


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-dir', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    output = args.output.resolve()
    private_roots = [ROOT / 'private_inputs', ROOT / 'reproducibility/artifacts']
    if not any(output.is_relative_to(p) for p in private_roots):
        raise ValueError('Private analysis outputs must stay in an ignored private folder')
    if output.exists():
        raise ValueError('Use a new run directory')
    output.mkdir(parents=True)
    source = args.source_dir.resolve()
    inputs = ['dragon_benchmark_full_response.json', 'dragon_benchmark_full_request.json',
              'dragon_price_history_response.json', 'dragon_price_history_request.json',
              'dragon_public_fund_data.json', 'dragon_public_fund_request.json']
    sources = [Path(__file__).resolve(), ROOT / 'code/benchmark.py', ROOT / 'code/accounting.py',
               ROOT / 'code/reproduce.py']
    manifest = {'status': 'started', 'started_at': datetime.now(timezone.utc).isoformat(),
                'source_commit': subprocess.check_output(['git', '-C', str(ROOT), 'rev-parse', 'HEAD'], text=True).strip(),
                'source_files': {str(p.relative_to(ROOT)): sha(p) for p in sources},
                'input_files': {name: sha(source / name) for name in inputs},
                'strategy_daily_sha256': sha(ROOT / 'results/reference/strategy_daily.csv'),
                'scope': 'PRIVATE_RESEARCH_ANALYSIS', 'public_redistribution_permission': 'not_established',
                'source_access': 'anonymous published website chart; no credentials or subscription',
                'source_url': 'https://www.dragoncapital.com.vn/institution/vi/product/a0eJ2000001X9zhIAC/vn30',
                'series': 'VN30TR Index (Dragon Capital reported)',
                'plan': {'phases': {'IS': ['2020-02-18', '2023-09-29', 906],
                                    'OOS': ['2023-09-29', '2026-04-29', 641]},
                         'primary': 'Provider levels as reported, without filling or repairing',
                         'sensitivity': 'Reconstruct 2025-05-05/06/07 using the pre-gap TRI/price factor; assumes zero dividend yield',
                         'market_state': 'continuous peak from 2020-02-18; drawdown <= -10%; ex-post',
                         'statistics': '252 sessions/year; rf=(1.06**(1/252)-1); sample std; anchor included in drawdown'},
                'environment': {'python': sys.version, 'platform': platform.platform(),
                                **{p: importlib.metadata.version(p) for p in ['numpy', 'pandas', 'matplotlib']}}}
    manifest_path = output / 'manifest.json'
    manifest_path.write_text(json.dumps(manifest, indent=2) + '\n')
    snapshots = output / 'source_snapshots'
    snapshots.mkdir()
    for path in sources:
        shutil.copy2(path, snapshots / path.name)
    identity = json.loads((source / 'dragon_public_fund_data.json').read_text())['returnValue']
    if identity['specificBenchmarkFundData']['fundReportCode__c'] != 'VN30TR Index':
        raise ValueError('Source benchmark identity does not match VN30 total return')
    request = json.loads((source / 'dragon_benchmark_full_request.json').read_text())
    params = json.loads(request['params']['params'])
    if params['benchmarkFundReportCode'] != 'VN30TR Index' or params['includingBenchmark'] is not True:
        raise ValueError('Historical request did not select the total-return benchmark')
    reported = normalize_history(json.loads((source / 'dragon_benchmark_full_response.json').read_text()))
    prices = normalize_history(json.loads((source / 'dragon_price_history_response.json').read_text()))
    sensitivity, audit = reconstruct_three_sessions(reported, prices)
    audit.to_csv(output / 'three_session_sensitivity.csv', index=False)
    daily = pd.read_csv(ROOT / 'results/reference/strategy_daily.csv', parse_dates=['date'])
    coverage = {}
    for name, levels in [('reported', reported), ('three_day_sensitivity', sensitivity)]:
        folder = output / name
        folder.mkdir()
        levels.to_csv(folder / 'index_levels_private.csv', index=False)
        coverage[name] = evaluate_levels(levels, daily, folder, f'VN30TRI_{name}')
        if not all(row['full_sample'] for row in coverage[name]):
            raise ValueError(f'Incomplete IS/OOS coverage in {name}')
    first = pd.read_csv(output / 'reported/metrics.csv')
    second = pd.read_csv(output / 'three_day_sensitivity/metrics.csv')
    a = first[first.strategy.str.startswith('VN30TRI_')].set_index('phase')
    b = second[second.strategy.str.startswith('VN30TRI_')].set_index('phase')
    np.testing.assert_allclose(a[['final_nav', 'ann_return']], b[['final_nav', 'ann_return']], atol=1e-12, rtol=1e-12)
    for name in ['reported', 'three_day_sensitivity']:
        metrics = pd.read_csv(output / name / 'metrics.csv')
        accepted = pd.read_csv(ROOT / 'results/derived/performance_metrics.csv')
        accepted = accepted[accepted.bps_per_side.eq(0)]
        merged = metrics[metrics.strategy.isin(['C1', 'B1', 'B2'])].merge(accepted, on=['phase', 'strategy'], suffixes=('_new', '_old'))
        if len(merged) != 6:
            raise ValueError('Missing portfolio cross-check rows')
        for column in ['final_nav', 'ann_return', 'ann_volatility', 'sharpe', 'max_drawdown']:
            np.testing.assert_allclose(merged[f'{column}_new'], merged[f'{column}_old'], rtol=1e-10, atol=1e-10)
    manifest.update(status='completed', completed_at=datetime.now(timezone.utc).isoformat(), coverage=coverage,
                    artifact_hashes={str(p.relative_to(output)): sha(p) for p in sorted(output.rglob('*'))
                                     if p.is_file() and p != manifest_path})
    manifest_path.write_text(json.dumps(manifest, indent=2) + '\n')
    print(json.dumps({'output': str(output), 'coverage': coverage}))


if __name__ == '__main__':
    main()
