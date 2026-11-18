# VN30TRI source and coverage status

Latest update, 2026-11-18: full 906/641 private calculations are now available from Dragon Capital’s publicly displayed VN30TR Index, with a separately documented three-session reconstruction sensitivity. See [completion findings](VN30TRI_completion_20261118_vi.md). Raw-series and derived-data redistribution rights have not been established; zero observations have been admitted to the public data payload. The earlier access checks below are retained as history.

Earlier review on 2026-11-18: D01(OOS), D02(IS) were PENDING_SOURCE and D04 was PENDING_D01_D02. No daily VN30TRI level file has been admitted. The expected anchors are2020-02-18 for 906 IS returns and 2023-09-29 for 641 OOS returns. There are 0 admitted index observations. The calendar file enumerates planned portfolio dates and does not assert that market data are absent on those dates.

## Latest Vnstock runtime check, 2026-11-18

Installed the latest available stable Vnstock 6.0.1 with vnstock-oapi 0.1.2 from the official package index into an isolated temporary environment. The original research environment retains Vnstock 4.0.4. Installation completed and pip check reported no broken requirements. The official release history dates 6.0.1 to 2026-11-15. [Release history](https://vnstocks.com/docs/vnstock/lich-su-phien-ban).

Executed `Market(source).index("VN30TRI").ohlcv(start="2020-01-14", end="2026-04-29", interval="1D", floating=None)` for each of the four sources documented for index OHLCV: dnse, fhsc, ssi and tcbs. Every call raised CredentialError with code VNSTOCK_CREDENTIAL_MISSING before retrieving index data. Missing credentials were DNSE_API_KEY/DNSE_API_SECRET, FHSC_API_KEY, SSI_API_KEY/SSI_API_SECRET and TCBS_API_KEY respectively. No index CSV was produced. The runtime record and evidence hashes are in [the acquisition record](../reproducibility/vn30tri_acquisition_20261118.json); installation log, environment and exact probe are retained locally under ignored reproducibility/artifacts/vnstock-probe-20261118/.

This verifies the current access barrier, not whether those vendors carry VN30TRI or cover 2020–2026. Generation 6 uses the user's own Open API credentials. vnstock-oapi is the Community connector; the vnstock normalization layer belongs to the extended software offering. Broker/source access and software licensing are separate prerequisites; neither establishes a right to publish raw or derived data. [Index history API](https://vnstocks.com/docs/vnstock/v6/thi-truong-market), [Generation 6 architecture and access](https://vnstocks.com/docs/vnstock/v6/gioi-thieu).

No benchmark experiment was run. Existing C1/B1/B2 outputs and D01/D02/D04 status tables remain unchanged. An authorized source key configured locally, followed by symbol/coverage/rights checks, or a permitted daily index export is still needed.

## Earlier source findings

The updated official rules supplied in guide_5 are HOSE Ground Rules v4.0, Decision 747/QĐ-SGDHCM dated 2024-12-30. The retrieved document identifies price/total-return variants, the EOD total-return calculation and dividend reinvestment. It also describes revisions/corrections and source intellectual-property terms. Its full methodology is available from HOSE. [Official rules](https://staticfile.hsx.vn/Uploads/LocalFiles/ef15ff11e799483abd11677ad0443887/20250114_20241230_QD%20747%20HOSE%20Index%20Ground%20Rules.pdf).

The HOSE index factsheet supplied by guide_5 is a metadata reference. A factsheet does not supply the dated sequence needed to calculate 1547 portfolio-aligned daily returns. [Factsheet reference](https://staticfile.hsx.vn/Uploads/UploadDocuments/2452173/Form_Factsheet_MCIndices_Eng_T04.2026.pdf).

The publicly retrieved HOSE end-of-day page exposed its application shell and no accepted export. The previously examined TradingView symbol identifies VN30TRI but supplied no accepted daily export/vintage/right-to-use pack. This records the retrieval outcome, not a claim about every access channel on those platforms. [HOSE end-of-day page](https://www.hsx.vn/vi/du-lieu-giao-dich/thong-ke/du-lieu-cuoi-ngay), [VN30TRI symbol](https://www.tradingview.com/symbols/HOSE-VN30TRI/).

FiinQuant's historical-data documentation specifies authenticated Fetch_Trading_Data, daily granularity and close fields. It documents a possible vendor route, but its examples do not establish a VN30TRI entitlement or provide the required file to this task. An authenticated, licensed export still needs to be obtained and identified. [Historical-data documentation](https://docs.fiinquant.vn/ham-va-cong-thuc/2.-du-lieu-giao-dich/2.2.-ham-du-lieu-lich-su).

Previous C2 source findings also identified CEIC's displayed monthly VN30 total-return dataset. That retrieved monthly series cannot supply daily IS/OOS intervals. Public search results for CafeF VNINDEX and Investing VN30 describe price-index routes. They are outside D01/D02's specified total-return identity. [CEIC monthly series](https://www.ceicdata.com/en/vietnam/ho-chi-minh-stock-exchange-monthly/ho-chi-minh-stock-exchange-index-total-return-vn30).

## Earlier input requirements (superseded by the private calculation above)

Obtain a lawful HOSE VN30TRI daily EOD level file including both anchors and all 1547 return intervals, plus canonical identifier, source/provider URL, retrieval time, dividend methodology, historical coverage, version/backfill information and research-use evidence. Retain vendor-record dates if provided. Confirm raw and derived redistribution rights separately. The input can remain private.

`code/benchmark.py` is prepared and tested on explicitly synthetic temporary fixtures. It computes full641/906 windows when covered, reports unmatched intervals, and recomputes all portfolios on a shorter contiguous common sample when necessary. A date gap is never bridged into a single-session return. It exports continuous-peak D04 labels only when both complete phases are covered. Benchmark metrics and states have not been computed on live VN30TRI observations.

At that earlier stage, coverage/status were recorded in `results/reference/benchmark_status.csv`, `benchmark_expected_calendar.csv` and `market_state_status.csv`, with no computed market-state summaries. The status tables now distinguish computed private observations from zero publicly admitted observations. The consolidated [handoff](paper_handoff_vi.md) includes the completed D01/D02/D04 results and remaining publication tasks. No general market-outperformance claim follows from these descriptive comparisons.
