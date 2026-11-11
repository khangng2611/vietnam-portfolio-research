# VN30TRI source and coverage status

Reviewed 2026-11-11. D01(OOS), D02(IS) and dependent D04 remain PENDING_SOURCE. No daily VN30TRI level file has been admitted. The expected anchors are2020-02-18 for 906 IS returns and 2023-09-29 for 641 OOS returns. There are 0 admitted index observations. The calendar file enumerates planned portfolio dates and does not assert that market data are absent on those dates.

The updated official rules supplied in guide_5 are HOSE Ground Rules v4.0, Decision 747/QĐ-SGDHCM dated 2024-12-30. The retrieved document identifies price/total-return variants, the EOD total-return calculation and dividend reinvestment. It also describes revisions/corrections and source intellectual-property terms. Its full methodology is available from HOSE. [Official rules](https://staticfile.hsx.vn/Uploads/LocalFiles/ef15ff11e799483abd11677ad0443887/20250114_20241230_QD%20747%20HOSE%20Index%20Ground%20Rules.pdf).

The HOSE index factsheet supplied by guide_5 is a metadata reference. A factsheet does not supply the dated sequence needed to calculate 1547 portfolio-aligned daily returns. [Factsheet reference](https://staticfile.hsx.vn/Uploads/UploadDocuments/2452173/Form_Factsheet_MCIndices_Eng_T04.2026.pdf).

The publicly retrieved HOSE end-of-day page exposed its application shell and no accepted export. The previously examined TradingView symbol identifies VN30TRI but supplied no accepted daily export/vintage/right-to-use pack. This records the retrieval outcome, not a claim about every access channel on those platforms. [HOSE end-of-day page](https://www.hsx.vn/vi/du-lieu-giao-dich/thong-ke/du-lieu-cuoi-ngay), [VN30TRI symbol](https://www.tradingview.com/symbols/HOSE-VN30TRI/).

FiinQuant's historical-data documentation specifies authenticated Fetch_Trading_Data, daily granularity and close fields. It documents a possible vendor route, but its examples do not establish a VN30TRI entitlement or provide the required file to this task. An authenticated, licensed export still needs to be obtained and identified. [Historical-data documentation](https://docs.fiinquant.vn/ham-va-cong-thuc/2.-du-lieu-giao-dich/2.2.-ham-du-lieu-lich-su).

Previous C2 source findings also identified CEIC's displayed monthly VN30 total-return dataset. That retrieved monthly series cannot supply daily IS/OOS intervals. Public search results for CafeF VNINDEX and Investing VN30 describe price-index routes. They are outside D01/D02's specified total-return identity. [CEIC monthly series](https://www.ceicdata.com/en/vietnam/ho-chi-minh-stock-exchange-monthly/ho-chi-minh-stock-exchange-index-total-return-vn30).

## Input needed to finish

Obtain a lawful HOSE VN30TRI daily EOD level file including both anchors and all 1547 return intervals, plus canonical identifier, source/provider URL, retrieval time, dividend methodology, historical coverage, version/backfill information and research-use evidence. Retain vendor-record dates if provided. Confirm raw and derived redistribution rights separately. The input can remain private.

`code/benchmark.py` is prepared and tested on explicitly synthetic temporary fixtures. It computes full641/906 windows when covered, reports unmatched intervals, and recomputes all portfolios on a shorter contiguous common sample when necessary. A date gap is never bridged into a single-session return. It exports continuous-peak D04 labels only when both complete phases are covered. Benchmark metrics and states have not been computed on live VN30TRI observations.

The current coverage/status tables are `results/reference/benchmark_status.csv`, `benchmark_expected_calendar.csv` and `market_state_status.csv`. Market-state summary cells remain unavailable until admitted index data arrive. No market-outperformance claim follows from this release candidate.
