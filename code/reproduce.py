"""Recreate paper tables and figures from admitted dated strategy outputs."""
import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from accounting import return_stats, cost_returns

ROOT = Path(__file__).resolve().parents[1]
PHASES = {'IS': ('2020-02-18', '2023-09-29', 906), 'OOS': ('2023-09-29', '2026-04-29', 641)}
STRATEGIES = ['C1', 'B1', 'B2']
CLASSES = ['equities', 'GOLD', 'VFF']
COLORS = {'C1': '#555555', 'B1': '#2377AD', 'B2': '#D46C20'}
EPISODE_COLUMNS = ['peak_date', 'first_decline_date', 'trough_date', 'depth', 'peak_to_trough_sessions',
                   'underwater_sessions', 'recovery_date', 'peak_to_recovery_sessions', 'observed_end_date', 'status']


def drawdown_episodes(nav):
    """Use the last tied peak, first tied trough and explicit right censoring."""
    if nav.empty or nav.index.has_duplicates or not nav.index.is_monotonic_increasing:
        raise ValueError('NAV needs unique sorted dates')
    if not np.isfinite(nav).all() or (nav <= 0).any():
        raise ValueError('NAV must be positive and finite')
    values = nav.to_numpy()
    peak = 0
    start = None
    trough = None
    rows = []
    for i in range(1, len(nav)):
        if values[i] >= values[peak] - 1e-12:
            if start is not None:
                rows.append([nav.index[peak], nav.index[start], nav.index[trough],
                             values[trough] / values[peak] - 1, trough - peak, i - start,
                             nav.index[i], i - peak, nav.index[i], 'recovered'])
            peak, start, trough = i, None, None
        else:
            if start is None:
                start = trough = i
            if values[i] < values[trough]:
                trough = i
    if start is not None:
        rows.append([nav.index[peak], nav.index[start], nav.index[trough],
                     values[trough] / values[peak] - 1, trough - peak, len(nav) - start,
                     pd.NaT, np.nan, nav.index[-1], 'unrecovered_right_censored'])
    return pd.DataFrame(rows, columns=EPISODE_COLUMNS)


def attribution(contributions, returns):
    """Link daily contributions to total phase wealth using prior phase NAV."""
    if not contributions.index.equals(returns.index):
        raise ValueError('Contribution/return dates differ')
    if not np.isfinite(contributions).all().all() or not np.isfinite(returns).all():
        raise ValueError('Nonfinite contributions/returns')
    residual = contributions.sum(axis=1) - returns
    if residual.abs().max() > 1e-10:
        raise ValueError('Class contributions do not reconcile with portfolio return')
    nav = (1 + returns).cumprod()
    previous_nav = nav.shift(1, fill_value=1)
    linked = contributions.mul(previous_nav, axis=0)
    if abs(linked.to_numpy().sum() - (nav.iloc[-1] - 1)) > 1e-10:
        raise ValueError('Class wealth increments do not reconcile with terminal NAV')
    return linked, float(residual.abs().max())


def save_figure(fig, folder, name):
    fig.tight_layout()
    for extension in ['png', 'pdf', 'svg']:
        fig.savefig(folder / f'{name}.{extension}', dpi=300, bbox_inches='tight')
    plt.close(fig)


def reproduce(output):
    reference = ROOT / 'results/reference'
    output.mkdir(parents=True, exist_ok=True)
    figures = output / 'figures'
    figures.mkdir(exist_ok=True)
    daily = pd.read_csv(reference / 'strategy_daily.csv', parse_dates=['date'])
    contributions = pd.read_csv(reference / 'class_contributions.csv', parse_dates=['date'])
    weights = pd.read_csv(reference / 'held_class_weights.csv', parse_dates=['date'])
    accepted = pd.read_csv(reference / 'accepted_metrics.csv')
    event_trades = pd.read_csv(reference / 'event_trades.csv', parse_dates=['execution_date'])
    all_metrics, all_navs, episodes, summaries, reconciliation = [], [], [], [], []
    for strategy in STRATEGIES:
        saved = daily[daily.strategy == strategy].set_index('date')
        class_daily = contributions[contributions.strategy == strategy].set_index('date')
        for phase, (start, end, expected_count) in PHASES.items():
            part = saved.loc[start:end]
            if len(part) != expected_count + 1 or str(part.index[0].date()) != start:
                raise ValueError(f'Unexpected calendar for {strategy}/{phase}')
            phase_events = event_trades[(event_trades.strategy == strategy) & (event_trades.execution_date > start)
                                        & (event_trades.execution_date <= end) & ~event_trades.initial_allocation]
            turnover = phase_events.turnover.sum() * 252 / expected_count
            for bps in [0, 10, 25, 50]:
                returns = part[f'net_return_{bps}bps'].iloc[1:]
                metrics = return_stats(returns)
                original = accepted[(accepted.strategy == strategy) & (accepted.phase == phase)
                                    & (accepted.bps_per_side == bps)].iloc[0]
                for name, value in metrics.items():
                    if abs(value - original[name]) > 1e-10:
                        raise ValueError(f'Accepted metric mismatch {strategy}/{phase}/{bps}/{name}')
                if abs(turnover - original.annualized_turnover) > 1e-10:
                    raise ValueError(f'Turnover mismatch {strategy}/{phase}')
                all_metrics.append({'strategy': strategy, 'phase': phase, 'bps_per_side': bps,
                                    'anchor': start, 'first_return': part.index[1], 'last_return': end,
                                    'N': expected_count, **metrics,
                                    'annualized_turnover': turnover})
            gross = part.gross_return.iloc[1:]
            nav = pd.Series(np.r_[1., (1 + gross).cumprod()], index=part.index)
            dd = nav / nav.cummax() - 1
            all_navs.append(pd.DataFrame({'date': part.index, 'strategy': strategy, 'phase': phase,
                                         'gross_nav': nav.values, 'drawdown': dd.values}))
            events = drawdown_episodes(nav)
            events.insert(0, 'strategy', strategy)
            events.insert(1, 'phase', phase)
            episodes.append(events)
            episode_mdd = min(0., events.depth.min()) if len(events) else 0.
            if abs(episode_mdd - dd.min()) > 1e-10:
                raise ValueError('Episode MDD does not match daily MDD')
            linked, error = attribution(class_daily.loc[gross.index, CLASSES], gross)
            reconciliation.append({'strategy': strategy, 'phase': phase, 'N': expected_count,
                                   'max_daily_return_error': error,
                                   'terminal_wealth_error': linked.to_numpy().sum() - (nav.iloc[-1] - 1),
                                   'terminal_nav': nav.iloc[-1]})
            for asset_class in CLASSES:
                summaries.append({'strategy': strategy, 'phase': phase, 'asset_class': asset_class,
                                  'N': expected_count,
                                  'sum_simple_daily_contribution': class_daily.loc[gross.index, asset_class].sum(),
                                  'linked_wealth_contribution': linked[asset_class].sum(),
                                  'linked_contribution_percentage_points': 100 * linked[asset_class].sum(),
                                  'portfolio_total_return': nav.iloc[-1] - 1})
    metrics = pd.DataFrame(all_metrics)
    navs = pd.concat(all_navs, ignore_index=True)
    events = pd.concat(episodes, ignore_index=True)
    metrics.to_csv(output / 'performance_metrics.csv', index=False)
    navs.to_csv(output / 'phase_nav_drawdown.csv', index=False)
    events.to_csv(output / 'drawdown_episodes.csv', index=False)
    deepest = events.sort_values('depth').groupby(['strategy', 'phase'], sort=False).head(3)
    deepest.sort_values(['phase', 'strategy', 'depth']).to_csv(output / 'deepest_drawdowns.csv', index=False)
    pd.DataFrame(summaries).to_csv(output / 'class_contribution_summary.csv', index=False)
    pd.DataFrame(reconciliation).to_csv(output / 'contribution_reconciliation.csv', index=False)
    plot_results(navs, weights, metrics, figures)
    ab_rows = reproduce_ab(reference, output)
    return {'accepted_metric_rows_reproduced': len(metrics), 'AB_metric_rows_reproduced': ab_rows, 'phase_strategy_pairs': 6,
            'episodes': len(events), 'attribution_max_daily_error': max(r['max_daily_return_error'] for r in reconciliation),
            'attribution_max_terminal_error': max(abs(r['terminal_wealth_error']) for r in reconciliation)}


def reproduce_ab(reference, output):
    accepted = pd.read_csv(reference / 'cost_sensitivity.csv')
    gross_reference = pd.concat([pd.read_csv(reference / 'selection_portfolio_metrics.csv'),
                                 pd.read_csv(reference / 'optimizer_ladder_metrics.csv')], ignore_index=True)
    rows = []
    for folder in sorted((reference / 'variants').iterdir()):
        gross = pd.read_csv(folder / 'daily_returns.csv', index_col=0, parse_dates=True)['return']
        trades = pd.read_csv(folder / 'trades.csv', parse_dates=['execution_date'])
        for bps in [0, 10, 25, 50]:
            net = cost_returns(gross, trades, bps)
            for phase, (start, end, count) in PHASES.items():
                returns = net.loc[(net.index > start) & (net.index <= end)]
                if len(returns) != count:
                    raise ValueError('A/B sample count mismatch')
                stats = return_stats(returns)
                original = accepted[(accepted.experiment_id == folder.name) & (accepted.phase == phase)
                                    & (accepted.bps_per_side == bps)].iloc[0]
                for metric, value in stats.items():
                    if abs(value - original[metric]) > 1e-10:
                        raise ValueError(f'A/B metric mismatch {folder.name}/{phase}/{bps}/{metric}')
                events = trades[(trades.execution_date > start) & (trades.execution_date <= end)
                                & ~trades.initial_allocation]
                turnover = events.turnover.sum() * 252 / count
                original_turnover = gross_reference[(gross_reference.experiment_id == folder.name)
                                                    & (gross_reference.phase == phase)].iloc[0].annualized_turnover
                if abs(turnover - original_turnover) > 1e-10:
                    raise ValueError('A/B turnover mismatch')
                rows.append({'experiment_id': folder.name, 'phase': phase, 'bps_per_side': bps,
                             'N': count, **stats, 'annualized_turnover': turnover})
    pd.DataFrame(rows).to_csv(output / 'AB_reproduced_metrics.csv', index=False)
    return len(rows)


def plot_results(navs, weights, metrics, folder):
    plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 10,
                         'axes.spines.top': False, 'axes.spines.right': False})
    fig, ax = plt.subplots(figsize=(8, 3.7))
    for strategy in STRATEGIES:
        part = navs[(navs.strategy == strategy) & (navs.phase == 'OOS')]
        ax.plot(part.date, part.gross_nav, label=strategy, color=COLORS[strategy], lw=1.5)
    ax.set(ylabel='Gross wealth (anchor = 1)', xlabel='Date')
    ax.legend(ncol=3)
    ax.grid(alpha=.15)
    save_figure(fig, folder, 'C1_OOS_wealth')
    fig, axes = plt.subplots(3, 1, figsize=(8, 5.5), sharex=True)
    for ax, strategy in zip(axes, STRATEGIES):
        part = weights[(weights.strategy == strategy) & (weights.date > '2023-09-29')]
        ax.stackplot(part.date, *[part[c] for c in CLASSES], labels=CLASSES,
                     colors=['#2377AD', '#D6AE32', '#78A87D'])
        ax.set(ylim=(0, 1), ylabel=strategy)
    axes[0].legend(ncol=3, loc='upper left', fontsize=8)
    axes[-1].set_xlabel('Return date, weights held at interval start')
    save_figure(fig, folder, 'C1_class_weights')
    fig, ax = plt.subplots(figsize=(8, 3.5))
    for strategy in STRATEGIES:
        part = metrics[(metrics.strategy == strategy) & (metrics.phase == 'OOS')]
        ax.plot(part.bps_per_side, part.sharpe, 'o-', color=COLORS[strategy], label=strategy)
    ax.set(xlabel='Hypothetical cost, bps per traded side', ylabel='OOS net Sharpe', xticks=[0, 10, 25, 50])
    ax.legend(ncol=3)
    ax.grid(alpha=.15)
    save_figure(fig, folder, 'C1_cost_sensitivity')
    fig, axes = plt.subplots(2, 1, figsize=(8, 5.4))
    for ax, phase in zip(axes, PHASES):
        for strategy in STRATEGIES:
            part = navs[(navs.strategy == strategy) & (navs.phase == phase)]
            ax.plot(part.date, 100 * part.drawdown, label=strategy, color=COLORS[strategy], lw=1.1)
        ax.set(ylabel=f'{phase} drawdown (%)')
        ax.grid(alpha=.15)
    axes[0].legend(ncol=3)
    save_figure(fig, folder, 'portfolio_underwater')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=ROOT / 'results/derived')
    args = parser.parse_args()
    report = reproduce(args.output)
    (args.output / 'reproduction_summary.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report))


if __name__ == '__main__':
    main()
