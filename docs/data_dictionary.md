# Data, sources and access

`data_public/series_dictionary.csv` lists all 32 instruments, units, sample endpoints, source identity, original raw-source hashes and publication limitations. The 30 names form a static study basket. The source files are vendor-native retrospective snapshots. Historical constituent membership and every first-public/revision vintage are incomplete.

| Group | Frozen valuation field and unit | Decision-information convention | Source access |
| --- | --- | --- | --- |
| 30 equities | KBS adjusted close c/1000, thousand VND/share | adjusted close available by 18:00 under inherited assumption | KBS provider-native daily records, with exact source hashes per ticker |
| GOLD | SJC-HCM archived selling close, thousand VND/luong, about 100,000 VND source resolution | next calendar day eligibility | GiaVang.TV history, historical GiaVang.org archive |
| VFF | FMarket product21 NAV/unit divided by 1000, thousand VND/fund unit | five observed-session buffer plus later provider record metadata | FMarket product21 historical NAV records |

The KBS historical route in the acquisition record is `kbbuddywts.kbsec.com.vn/iis-server/investment/stocks/{ticker}/data_day`. The original `c` field and per-file hashes identify the series. GOLD acquisition uses the archived historical selling side, with the raw archive hash in the dictionary. VFF original `nav_per_unit_vnd` is scaled once. Equity cash dividends are not added separately. Independent total-return/corporate-action certification of all adjusted prices remains incomplete.

Source portals and methodology references are provided for lawful access. [KBS](https://kbbuddywts.kbsec.com.vn/), [gold history](https://giavang.tv/lich-su?range=all), [FMarket](https://fmarket.vn/), [VFF fund provider](https://wm.vinacapital.com/vi/investment-solutions/onshore-funds/vff/).

The observed exchange calendar was inherited from the frozen VNINDEX session record. VNINDEX is a calendar/market proxy in that archive. D01/D02 specifically require VN30TRI daily total-return levels. Its source and coverage status are described in `benchmark_source_status.md`.

## Released result fields

`results/reference/strategy_daily.csv` has one row per strategy/date, continuous gross NAV/return and net return/NAV at 0/10/25/50 bps. The first row is an anchor with an empty return. `accepted_metrics.csv` contains 24 accepted C1/B1/B2 strategy × phase × cost records. Reference group labels C1, B1 and B2 map to C1-FixedRule-K5-7, B1_BLnoML and B2_BLML.

`held_class_weights.csv` and `*_held_instrument_weights.csv` contain start-of-return held weights at the indexed date. `class_contributions.csv` contains equities/GOLD/VFF daily gross contribution calculated from exact private asset prices and saved held weights. The extraction error is recorded in `reproducibility/attribution_input_check.json`. Reproducing this extraction needs the authorized frozen valuation matrix. The released contribution file suffices to reproduce linking, phase summaries and portfolio-return reconciliation.

`instrument_trades.csv` has all 32 instruments per strategy/event. Asset-specific fields are pre_trade_weight, target_weight and weight_change. Event totals repeat across those asset rows. `event_trades.csv` contains one row per event and is the appropriate file for summing turnover, traded_notional and cost fractions. Initial deployment is flagged. Annual turnover units are portfolio-equivalent one-way trades/year.

`results/reference/variants/` preserves saved A/B return streams, targets and trades, plus B-arm posterior records with asset ordering, mu, pi, covariance, P/Q/confidence. No new optimization is needed to reproduce its performance and cost summaries. `selection_structure.csv`, `selection_history_comparison.csv`, the A metrics, original cost grid and uncertainty tables preserve accepted selection evidence. Random median return-path statistics and medians of seed-level metrics describe different aggregates.

`results/derived/` holds regenerated phase metrics, drawdown episodes, NAV/drawdown records, linked class-attribution summaries and reconciliation. All dates are observed sessions. Percentage-like metrics in CSV are fractions unless a field explicitly ends in percentage_points. `docs/results_guide.md` maps outputs to paper content.

## Access and distribution

Raw vendor prices, index history, private input ledgers and fitted pickle objects are held in authorized local storage. The user authorized publication of this curated code and derived research package on 2026-11-18 and confirmed Khang Phuc Nguyen as author and MIT for project software. `LICENSE` and `NOTICE.md` distinguish that software license from source-data rights. Provider datasets are not relicensed by this release. New raw index inputs and restricted derived outputs require their own access/sharing conditions.

Full historical reconstruction requires the input identities in `reproducibility/pre_analysis_manifest.json`, source-policy/availability ledger, original selected-set records, historical training/prediction records and the original execution layout. Obtain these through the data owner under applicable terms. The complete local source remains in the parent working repository. Public-level reproduction uses only admitted dated results. Small synthetic test cases are explicitly confined to reproducibility tests.
