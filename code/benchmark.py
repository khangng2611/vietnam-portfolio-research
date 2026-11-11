"""Evaluate a permitted daily VN30TRI file and descriptive market-drawdown labels."""
import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from accounting import return_stats
from reproduce import ROOT, PHASES, STRATEGIES, save_figure


def align_levels(levels, calendar):
    """Require index return boundaries to equal the portfolio's adjacent sessions."""
    levels = levels.copy()
    levels['index_date'] = pd.to_datetime(levels.index_date)
    if levels.index_date.duplicated().any() or not levels.index_date.is_monotonic_increasing:
        raise ValueError('Index dates must be sorted and unique')
    if not np.isfinite(levels.index_level).all() or (levels.index_level <= 0).any():
        raise ValueError('Index levels must be finite and positive')
    levels = levels.set_index('index_date')
    returns = levels.index_level.pct_change(fill_method=None).reindex(calendar)
    source_previous = pd.Series(levels.index, index=levels.index).shift().reindex(calendar)
    expected_previous = pd.Series(calendar, index=calendar).shift()
    valid = returns.notna() & source_previous.eq(expected_previous)
    return returns.where(valid), levels.index_level.reindex(calendar)


def longest_block(valid):
    blocks = valid.ne(valid.shift()).cumsum()
    runs = [group.index for _, group in valid.groupby(blocks) if group.all()]
    return max(runs, key=len) if runs else valid.index[:0]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--levels', type=Path, required=True)
    parser.add_argument('--metadata', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    metadata = json.loads(args.metadata.read_text())
    required = ['provider', 'source_url', 'retrieved_at', 'dividend_method', 'vintage', 'rights_evidence']
    if metadata.get('identifier') != 'VN30TRI' or metadata.get('return_type') != 'total_return':
        raise ValueError('Requires documented HOSE VN30TRI total-return series')
    if metadata.get('currency') != 'VND' or metadata.get('research_use_permitted') is not True:
        raise ValueError('VND and research-use evidence required')
    if any(not metadata.get(key) for key in required):
        raise ValueError('Incomplete source metadata')
    if args.output.exists() and any(args.output.iterdir()):
        raise ValueError('Choose a new empty output folder')
    args.output.mkdir(parents=True, exist_ok=True)
    import hashlib
    hashes = {'levels_sha256': hashlib.sha256(args.levels.read_bytes()).hexdigest(),
              'metadata_sha256': hashlib.sha256(args.metadata.read_bytes()).hexdigest(),
              'status': 'started', 'raw_redistribution_permitted': metadata.get('raw_redistribution_permitted', False)}
    (args.output / 'input_manifest.json').write_text(json.dumps(hashes, indent=2) + '\n')
    levels = pd.read_csv(args.levels)
    daily = pd.read_csv(ROOT / 'results/reference/strategy_daily.csv', parse_dates=['date'])
    panel = daily.pivot(index='date', columns='strategy', values='gross_return')
    aligned, index_levels = align_levels(levels, panel.index)
    metrics, coverage = [], []
    for phase, (start, end, expected) in PHASES.items():
        dates = panel.loc[start:end].index
        eligible = aligned.loc[dates[1:]].notna()
        used = longest_block(eligible)
        full = len(used) == expected
        coverage.append({'phase': phase, 'expected_returns': expected, 'matched_returns': int(eligible.sum()),
                         'longest_common_returns': len(used), 'full_sample': full})
        if len(used) < 2:
            continue
        sample = pd.DataFrame({'VN30TRI': aligned.loc[used], **{s: panel.loc[used, s] for s in STRATEGIES}})
        for name in sample:
            metrics.append({'phase': phase, 'strategy': name, 'N': len(used),
                            'first_return': used[0], 'last_return': used[-1],
                            'sample_kind': 'FULL_SAMPLE' if full else 'COMMON_CONTIGUOUS',
                            **return_stats(sample[name]), 'turnover': None})
        anchor = panel.index[panel.index.get_loc(used[0]) - 1]
        wealth = pd.concat([pd.DataFrame(1., index=[anchor], columns=sample.columns), (1 + sample).cumprod()])
        ax = wealth.plot(figsize=(8, 3.7), ylabel='Gross wealth (common anchor = 1)')
        save_figure(ax.figure, args.output, f'VN30TRI_context_{phase}')
    pd.DataFrame(coverage).to_csv(args.output / 'coverage.csv', index=False)
    pd.DataFrame(metrics).to_csv(args.output / 'metrics.csv', index=False)
    alignment = pd.DataFrame({'return_date': panel.index, 'index_level_available': index_levels.notna(),
                              'aligned_return': aligned})
    alignment.to_csv(args.output / 'alignment.csv', index=False)
    if all(row['full_sample'] for row in coverage):
        market = index_levels.loc['2020-02-18':'2026-04-29']
        dd = market / market.cummax() - 1
        states = pd.DataFrame({'date': market.index, 'market_drawdown': dd,
                               'market_state': np.where(dd <= -.1, 'MARKET_DRAWDOWN_10', 'OTHER_OBSERVED_DAYS')})
        states.to_csv(args.output / 'market_states.csv', index=False)
        rows = []
        for phase, (start, end, _) in PHASES.items():
            for label in ['MARKET_DRAWDOWN_10', 'OTHER_OBSERVED_DAYS']:
                selected = states[(states.date > start) & (states.date <= end) & (states.market_state == label)].date
                for strategy in STRATEGIES:
                    returns = panel.loc[selected, strategy]
                    rows.append({'phase': phase, 'market_state': label, 'strategy': strategy, 'N': len(returns),
                                 'mean_daily_return': returns.mean(), 'fraction_negative': (returns < 0).mean(),
                                 'worst_day': returns.min(), 'annualized_volatility': returns.std(ddof=1) * np.sqrt(252),
                                 'compounded_subset_return': (1 + returns).prod() - 1 if len(returns) else np.nan})
        pd.DataFrame(rows).to_csv(args.output / 'market_state_summary.csv', index=False)
    hashes['status'] = 'completed'
    (args.output / 'input_manifest.json').write_text(json.dumps(hashes, indent=2) + '\n')
    print(json.dumps(coverage))


if __name__ == '__main__':
    main()
