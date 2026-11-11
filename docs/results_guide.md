# Paper table and figure map

| Paper content | Released source | Regenerated output |
| --- | --- | --- |
| Main C1/B1/B2 IS/OOS gross and cost metrics | reference/strategy_daily.csv, accepted_metrics.csv, event_trades.csv | derived/performance_metrics.csv |
| A selector and matched B0/B1/B2 results | reference/variants/, original cost_sensitivity.csv | derived/AB_reproduced_metrics.csv |
| Selector coverage/stability and seed controls | reference/selection_history_comparison.csv, selection_structure.csv, selection_portfolio_metrics.csv | original accepted dated tables |
| Paired uncertainty | reference/C1_paired_uncertainty.csv, uncertainty_intervals.csv | original accepted intervals, no new resampling |
| D03 drawdown chronology | reference/strategy_daily.csv | derived/drawdown_episodes.csv, deepest_drawdowns.csv, phase_nav_drawdown.csv |
| D05 class P&L | reference/class_contributions.csv and start-held weights | derived/class_contribution_summary.csv, contribution_reconciliation.csv |
| D06 OOS NAV | dated gross returns | figures/C1_OOS_wealth.png/pdf/svg |
| D06 held class weights | reference/held_class_weights.csv | figures/C1_class_weights.png/pdf/svg |
| D06 hypothetical costs | accepted scenario daily returns | figures/C1_cost_sensitivity.png/pdf/svg |
| Drawdown figure | phase NAV including anchors | figures/portfolio_underwater.png/pdf/svg |
| D01/D02 VN30TRI | source acquisition pending | reference/benchmark_status.csv and expected calendar only |
| D04 market drawdown labels | depends on admitted VN30TRI | reference/market_state_status.csv |

Paths in the table are relative to results/ except figures/. `code/reproduce.py` creates figure files under its output/figures. The top-level figures/ folder contains the corresponding finalized manuscript exports.

The three filenames already referenced by the manuscript are preserved. Vector PDF and SVG exports accompany 300dpi PNGs. All paths use the full dated outputs. The handoff does not edit paper_5.tex because that manuscript was not supplied in the current filesystem.

Linked class contributions are in percentage points of initial phase wealth. Their sum equals 100×(terminal NAV−1). A CAGR contribution is not inferred. The daily contributions and a sum of their simple values remain separately named. Recovery date is empty for right-censored drawdowns. Underwater duration counts observed sessions below the episode peak and excludes recovery.
