# Paper table and figure map

| Content | Distributed output |
| --- | --- |
| C1/B1/B2 IS/OOS gross and cost metrics | results/derived/performance_metrics.csv |
| A/B accepted controls and cost records | results/derived/AB_reproduced_metrics.csv |
| D03 drawdown chronology | results/derived/drawdown_episodes.csv and deepest_drawdowns.csv |
| D05 linked class contribution | results/derived/class_contribution_summary.csv and reconciliation |
| D06 dated NAV | figures/C1_OOS_wealth.png/pdf/svg |
| D06 held class weights | figures/C1_class_weights.png/pdf/svg |
| D06 hypothetical costs | figures/C1_cost_sensitivity.png/pdf/svg |
| Underwater figure | figures/portfolio_underwater.png/pdf/svg |
| D01/D02 benchmark | Source/coverage status only; numerical evidence delivered privately |
| D04 market drawdown | Status and method only; dated states and summaries delivered privately |

code/reproduce.py regenerates the public tables/figures. code/benchmark.py and reproducibility/run_dragon_benchmark.py implement benchmark analysis; independently obtained source inputs are required. The advisor handoff includes the full benchmark report, figures, sensitivity and LaTeX fragment; these are not public release assets. See data_sharing_review.md and paper_handoff_vi.md.
