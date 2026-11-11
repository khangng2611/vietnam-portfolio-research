# Research design and finalized implementation

The research studies representative equity selection followed by capital allocation for Vietnamese long-only portfolios. The static study basket contains 30 equities, GOLD and VFF. A dated correlation-coverage selector supplies five equities every 20 sessions. B1, B2 and C1 invest on that common menu with targets every five sessions.

## Samples and accounting

The inherited valuation panel has 1,568 sessions and 32 instruments, from 2020-01-14 through 2026-04-29. IS starts with NAV 1 at 2020-02-18 and contains 906 returns through 2023-09-29. OOS restarts reported phase NAV at 1 on 2023-09-29 and contains 641 returns from 2023-10-02 through 2026-04-29. Holdings carry continuously across that boundary in the simulation.

Selection at decision t uses eligible information through t−1. After-close targets execute at the assumed next session close. Old holdings earn the return to that close. New holdings first earn the subsequent interval. Held weights in the released dated files refer to the start of the indexed return. Targets can differ from held weights after drift. The complete 32-instrument union records incoming and outgoing positions.

Targets sum to one, are long-only and cap every instrument at 50%. Non-VFF weight is capped at 70%, producing an effective VFF floor of 30%. Drift can move holdings outside target bounds between executions. Initial capital is held in cash until the first modeled execution.

One-way turnover is half the sum of absolute target-minus-pretrade weight changes. Annual turnover is 252 times the sum of event turnover divided by phase return count. Initial funding is excluded from turnover. Initial purchase costs are charged once in IS. OOS carries existing holdings. Terminal trades incur costs within the last observed interval.

Hypothetical cost c is 0, 10, 25 or 50 bps per traded side. On an execution date, net growth equals gross growth times (1 − c × full traded notional). Full traded notional is twice one-way turnover. This is the accepted approximate event-cost convention. Actual fund dealing calendars, gold spreads, taxes and settlement remain outside the valuation-proxy study.

Annualization uses 252 sessions, sample standard deviation with ddof=1 and daily rf = 1.06^(1/252)−1. MDD includes the phase anchor NAV of one. CSV CAGR/volatility/drawdown are fractions. CAGR differences in paired-effect tables are percentage points.

## Selection

`code/frozen_baseline/gen_view/ranking/stock_selection.py` computes distance = 1 − correlation of historical returns and minimizes the sum of nearest-representative distances over all C(30,5) combinations. The original routine retains ticker ordering for deterministic ties. The saved A experiment controls include Full30, low-volatility K5 over 20 prior returns, and ten RandomK5 seeds 7,11,19,23,31,43,59,71,83,97. All comparisons inherit the same information and execution policies.

The accepted implementation is identified by source-map hashes. `results/reference/selected_k5_events.csv` preserves dated decisions, history endpoints and original selection-state IDs. `selection_history_comparison.csv` records all A memberships, coverage, correlations and switches. A/B source code and results are retained alongside C1.

## Allocation

C1 sets VFF to .30 and each of the five selected equities plus GOLD to .70/6. It is conditional on the active selector. Its target HHI is .1716667. B1 uses the BL equilibrium prior pi = delta × Sigma × equal_weight, with delta 2.5, tau .05 and the same dated seven-instrument menu. B2 uses the saved ML views with the same covariance, prior and optimizer constraints. B0_MVOmatched uses sample mean returns as context.

B1's no-view posterior equals pi. B2 covariance is estimated on 20 eligible return intervals. Covariance is regularized by the accepted eigenvalue floor. With ordered view matrix P, daily view Q and confidence, Omega has diagonal max(diag(P tau Sigma Pᵀ),1e-10) / clipped_confidence. Posterior and constraints are implemented in `code/accounting.py` and the archived experiment runner. The matched A/B experiment fixes risk aversion at 1.5 and excludes defensive regime views and regime-dependent risk-aversion changes. B2 retains the frozen volatility confidence dampener.

## XGBoost into BL

The frozen precursor run used `ranking_absolute`, an absolute-return XGBoost ensemble path. The class is `XGBoostEnsembleModel` in `code/frozen_baseline/gen_view/xgboost/xgboost_core.py`. Input features are momentum_5, momentum_10, momentum_20, rsi_14, ma_ratio_10_30, volatility_20, macd_hist and price_std_20. Minimum feature history is 30 prices. EMA/MACD state is computed on the supplied expanding prefix. The label is the native forward five-observed-price return.

Historical training was walk-forward on the selected equities. The executed retrain control is the top-level configuration's 10 sessions. `gen_view/xgboost/config.py` also contains a legacy 20-session constant, so reproducing the executed path requires the imports in `_ranking_helpers.py` and `reproducibility/frozen_run_config.json`. The outer training slice ends at t−5 exclusive. Prediction uses the eligible prefix ending before t. Exact historical fitted-label endpoints are identified by the saved training-audit hash in the provenance record.

The model uses a temporal 80/20 training/validation split, purges fitting labels whose endpoints reach validation, fits StandardScaler only on fitting rows, and uses validation for early stopping. Ensemble members use seeds 42–46, max_depth 4, learning_rate .05, n_estimators up to 200, early stopping 10 rounds, subsample .8 and colsample_bytree .70/.75/.80/.85/.90. Exact parameters remain in the archived code and configuration.

Prediction confidence is based on ensemble disagreement, clipped to .25–.70, with a directional-accuracy penalty below .40 using only matured predictions. The saved confidence additionally includes volatility dampening when the ratio exceeds 1.3. `generate_ml_views` filters absolute predicted returns below .001. When volatility is usable, annual view magnitude is .5 × tanh(predicted_5day_return / (daily_volatility × sqrt(5))). Its coded fallback uses capped linear annualization. `build_views_matrix` divides the annual magnitude by 252 to obtain daily Q. P is aligned to the active menu and each absolute view selects its corresponding equity. Saved records determine actual use and absence of views.

The source snapshot also contains historical regime and alternative-model branches. The accepted B2 experiment filters saved view names for `_ml_` and fixes its matched controls in `code/frozen_experiments/run.py`. Reading another branch in the snapshot does not identify the B2 strategy. Full fitting requires authorized price/eligibility data and historical records. Public replay regenerates summaries from dated outputs and preserves the original learned decisions.

## Additional descriptive analyses

A drawdown episode starts on the first NAV below the most recent tied peak. The first tied trough determines depth and peak-to-trough duration. Recovery is the first NAV reaching the peak within 1e-12. Underwater sessions count rows strictly below that peak, excluding the recovery row. Episodes outstanding at the phase end are right-censored. IS and OOS use separate anchors. Maximum observed underwater duration can belong to a different episode from maximum depth.

Daily class contribution is sum of start-of-interval instrument weight times instrument return within each class. For phase-level attribution, multiply each daily class contribution by previous phase NAV and sum the wealth increments. The three class wealth contributions add to terminal NAV−1. A sum of daily simple contributions is also saved as a separately labelled quantity. Linked contributions are path-dependent attribution, measured against initial phase wealth.

Market-state analysis requires the admitted VN30TRI series. The fixed ex-post label is MARKET_DRAWDOWN_10 when the index is at least 10% below its continuous running peak, and OTHER_OBSERVED_DAYS otherwise. Full-history labels continue across the IS/OOS boundary. Compounded subset returns may span discontinuous days. The label is a descriptive close-based classification.
