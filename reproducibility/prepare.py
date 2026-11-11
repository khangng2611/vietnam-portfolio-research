"""Curate the local release candidate from immutable research runs in the parent checkout."""
import ast
import hashlib
import json
from pathlib import Path
import shutil

import numpy as np
import pandas as pd

RELEASE = Path(__file__).resolve().parents[1]
REPO = RELEASE.parent
C_RUN = REPO / 'extensions_C_v1/runs/extensions-C-20261104T210906'
B_RUN = REPO / 'experiments_core/runs/core-evidence-20261023T211011'
BASE = REPO / 'outputs/step1/readiness_20261012/runs/availability-observed-contract-20261012T233110'
NAMES = {'C1-FixedRule-K5-7': 'C1', 'B1_BLnoML': 'B1', 'B2_BLML': 'B2'}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def copy_source(source, destination, manifest):
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)
    manifest.append({'source': str(source.relative_to(REPO)), 'released_path': str(destination.relative_to(RELEASE)),
                     'source_sha256': digest(source), 'released_sha256': digest(destination), 'transformation': 'byte-identical copy'})


def main():
    for run in [B_RUN, C_RUN]:
        original = json.loads((run / 'manifest.json').read_text())
        artifacts = original.get('result_artifacts', original.get('artifacts', []))
        for artifact in artifacts:
            if digest(run / artifact['path']) != artifact['sha256']:
                raise ValueError(f'Frozen result artifact changed: {artifact["path"]}')
    record = json.loads((RELEASE / 'reproducibility/pre_analysis_manifest.json').read_text())
    for item in record['inputs']:
        source = REPO / item['path']
        if item['path'] == 'guide_5.md':
            source = REPO.parent / 'phase2-journal-plan/guide_5.md'
        if digest(source) != item['sha256']:
            raise ValueError(f'Input hash changed: {item["path"]}')
    reference = RELEASE / 'results/reference'
    daily = pd.read_csv(C_RUN / 'outputs/C1_daily.csv', parse_dates=['date'])
    daily['strategy'] = daily.strategy.map(NAMES)
    if daily.strategy.isna().any():
        raise ValueError('Unknown strategy')
    daily.to_csv(reference / 'strategy_daily.csv', index=False)
    accepted = pd.read_csv(C_RUN / 'outputs/C1_results.csv')
    accepted['strategy'] = accepted.strategy.map(NAMES)
    accepted.to_csv(reference / 'accepted_metrics.csv', index=False)
    prices = pd.read_csv(BASE / 'aligned_prices.csv', index_col=0, parse_dates=True)
    asset_returns = prices.pct_change(fill_method=None)
    class_contributions, class_weights, errors = [], [], []
    for original, strategy in NAMES.items():
        held = pd.read_csv(C_RUN / 'outputs' / f'{original}_holdings_weights.csv', index_col=0, parse_dates=True)
        if set(held.columns) != set(prices.columns):
            raise ValueError('Unexpected instrument set')
        asset_contribution = held * asset_returns.loc[held.index, held.columns]
        equity_columns = [name for name in held if name not in ['GOLD', 'VFF']]
        contributions = pd.DataFrame({'equities': asset_contribution[equity_columns].sum(axis=1),
                                      'GOLD': asset_contribution.GOLD, 'VFF': asset_contribution.VFF})
        gross = daily[daily.strategy == strategy].set_index('date').gross_return.loc[held.index]
        error = float((contributions.sum(axis=1) - gross).abs().max())
        if error > 1e-10:
            raise ValueError(f'Attribution mismatch {strategy}')
        errors.append({'strategy': strategy, 'max_daily_error_from_frozen_asset_prices': error})
        contributions['strategy'] = strategy
        class_contributions.append(contributions.reset_index(names='date'))
        grouped = pd.DataFrame({'equities': held[equity_columns].sum(axis=1), 'GOLD': held.GOLD, 'VFF': held.VFF})
        grouped['strategy'] = strategy
        class_weights.append(grouped.reset_index(names='date'))
        held.to_csv(reference / f'{strategy}_held_instrument_weights.csv', index_label='return_date')
    pd.concat(class_contributions, ignore_index=True).to_csv(reference / 'class_contributions.csv', index=False)
    pd.concat(class_weights, ignore_index=True).to_csv(reference / 'held_class_weights.csv', index=False)
    trades = pd.read_csv(C_RUN / 'outputs/C1_trades.csv')
    trades['strategy'] = trades.strategy.map(NAMES)
    trades.to_csv(reference / 'instrument_trades.csv', index=False)
    event_columns = ['strategy', 'decision_date', 'execution_date', 'first_return_date', 'turnover', 'traded_notional', 'initial_allocation']
    event_columns += [name for name in trades if name.startswith('event_cost_fraction_')]
    trades.drop_duplicates(['strategy', 'execution_date'])[event_columns].to_csv(reference / 'event_trades.csv', index=False)
    for filename in ['selection_structure.csv', 'selection_history_comparison.csv', 'selection_portfolio_metrics.csv', 'selection_portfolio_returns.csv',
                     'optimizer_ladder_metrics.csv', 'cost_sensitivity.csv', 'uncertainty_intervals.csv', 'experiment_registry.csv']:
        shutil.copy2(B_RUN / 'outputs' / filename, reference / filename)
    for folder in sorted((B_RUN / 'outputs/variants').iterdir()):
        destination = reference / 'variants' / folder.name
        destination.mkdir(parents=True, exist_ok=True)
        for filename in ['daily_returns.csv', 'weights.csv', 'trades.csv']:
            shutil.copy2(folder / filename, destination / filename)
        if folder.name.startswith('B'):
            shutil.copy2(folder / 'posterior_audit.csv', destination / 'posterior_audit.csv')
    shutil.copy2(C_RUN / 'outputs/selected_k5_events.csv', reference / 'selected_k5_events.csv')
    shutil.copy2(C_RUN / 'outputs/paired_uncertainty.csv', reference / 'C1_paired_uncertainty.csv')
    dictionary = pd.read_csv(REPO / 'extensions_C_v1/input_dictionary.csv')
    dictionary.to_csv(RELEASE / 'data_public/series_dictionary.csv', index=False)
    sources = []
    frozen = B_RUN / 'source_snapshot/outputs/step1/readiness_20261012/candidate_workspace'
    for directory in ['backtest', 'gen_view', 'utils']:
        for source in sorted((frozen / directory).rglob('*.py')):
            destination = RELEASE / 'code/frozen_baseline' / source.relative_to(frozen)
            copy_source(source, destination, sources)
    copy_source(frozen / 'config.py', RELEASE / 'code/frozen_baseline/config.py', sources)
    copy_source(frozen / 'assets_1.json', RELEASE / 'code/frozen_baseline/assets_1.json', sources)
    copy_source(B_RUN / 'source_snapshot/experiments_core/src/run.py', RELEASE / 'code/frozen_experiments/run.py', sources)
    copy_source(B_RUN / 'source_snapshot/experiments_core/src/core.py', RELEASE / 'code/accounting.py', sources)
    # Keep the prescribed C1 rule verbatim while dropping the workstation-specific runner wrapper.
    original_c1 = C_RUN / 'source_snapshot/extensions_C_v1/C1_fixed_rule.py'
    original_text = original_c1.read_text()
    node = next(n for n in ast.parse(original_text).body if isinstance(n, ast.FunctionDef) and n.name == 'fixed_targets')
    destination = RELEASE / 'code/fixed_rule.py'
    destination.write_text('import numpy as np\n\n\n' + ast.get_source_segment(original_text, node) + '\n')
    sources.append({'source': str(original_c1.relative_to(REPO)), 'source_sha256': digest(original_c1),
                    'released_path': str(destination.relative_to(RELEASE)), 'released_sha256': digest(destination),
                    'transformation': 'verbatim fixed_targets function with numpy import; runner wrapper omitted'})
    shutil.copy2(BASE / 'run_config.json', RELEASE / 'reproducibility/frozen_run_config.json')
    shutil.copy2(B_RUN / 'experiment_plan.json', RELEASE / 'reproducibility/frozen_experiment_plan.json')
    shutil.copy2(B_RUN / 'requirements_frozen.txt', RELEASE / 'reproducibility/original_environment.txt')
    (RELEASE / 'reproducibility/source_map.json').write_text(json.dumps(sources, indent=2) + '\n')
    (RELEASE / 'reproducibility/attribution_input_check.json').write_text(json.dumps(errors, indent=2) + '\n')
    print(f'Curated {len(sources)} source files and derived dated research results')


if __name__ == '__main__':
    main()
