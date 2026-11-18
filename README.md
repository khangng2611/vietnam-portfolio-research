# Vietnam Long-Only Multi-Asset Portfolio

This research package studies representative equity selection followed by capital allocation for Vietnamese long-only portfolios. Five dated correlation representatives from a static 30-stock basket are combined with a GOLD valuation proxy and VFF bond-fund NAV proxy. B1 uses a Black–Litterman equilibrium prior. B2 adds saved XGBoost views. C1 uses VFF 30% and equal shares of the remaining 70% across the other six instruments.

Version `0.2.0` packages the accepted research code and derived evidence. Author: **Nguyen Phuc Khang**. Original project software is available under the MIT license; [NOTICE.md](NOTICE.md) explains the separate data scope. The upstream development project is [portfolio-optimization](https://github.com/khangng2611/portfolio-optimization).

## Benchmark follow-up and advisor handoff

D01/D02/D04 calculations are complete privately with full 906/641 coverage. This release adds their evaluation code, source/coverage documentation and nine tests. New benchmark tables, daily series, figures and the full advisor report are not distributed here. See [scope and source conditions](docs/data_sharing_review.md) and [public handoff](docs/paper_handoff_vi.md). Version 0.2.0 is a code-and-portfolio-results release, not an open VN30TRI dataset.

## Main observed OOS results

The common anchor is 2023-09-29. There are 641 daily returns from 2023-10-02 to 2026-04-29.

| Strategy | Final NAV | CAGR | Annual vol | Sharpe | MDD | One-way TO/year |
| --- | --- | --- | --- | --- | --- | --- |
| C1 | 1.7164 | 23.66% | 13.97% | 1.172 | −10.18% | .760 |
| B1 | 1.7104 | 23.49% | 13.81% | 1.175 | −10.26% | .851 |
| B2 | 1.8244 | 26.66% | 13.71% | 1.367 | −9.51% | 7.975 |

C1 and B1 have close observed profiles. B2 has a higher gross Sharpe and greater hypothetical turnover costs. Paired uncertainty and the cost grid are preserved. The period was already observed during research development, so the evidence remains conditional on that sample and static basket.

## Repository map

```text
code/                     Portable reproduce.py and benchmark.py, original accounting helper
  frozen_baseline/        Original selected scientific source for selector, XGBoost, views, BL, optimizer
  frozen_experiments/     Original A/B runner for source reference and authorized historical reconstruction
results/
  reference/              Dated accepted strategy outputs and original selection/cost/uncertainty tables
  derived/                Regenerated metrics, episodes, class contributions and checks
figures/                  Manuscript PNG/PDF/SVG figures
data_public/             32-series dictionary, input schema and access instructions
 docs/                    Methodology, source status, result map and Vietnamese paper handoff
reproducibility/           Tests, extraction recipe, original configuration and source identities
CITATION.cff              Author and versioned software citation
LICENSE                   Current licensing status
```

## Reproduce the released tables and figures

Use Python 3.11+ and install the three pinned analysis dependencies from requirements.txt in your own virtual environment. From this directory, run

```sh
python -B -m unittest discover -s reproducibility -p 'test_*.py' -v
python -B code/reproduce.py --output /path/to/new/reproduced-results
```

The command regenerates 24 C1/B1/B2 scenario metrics and 128 accepted A/B scenario metrics, annual turnover,294 drawdown episodes, class-attribution summaries, reconciliation and four publication figures. It consumes distributed dated strategy outputs. The same command runs after extracting this package into a standalone directory.

[Setup and source versions](docs/reproducibility.md), [methodology](docs/methodology.md), [result/figure map](docs/results_guide.md), [data dictionary and rights](docs/data_dictionary.md).

## Twelve guide_5 items

D03 drawdowns, D05 class P&L, D06 figures, D07 dictionary, D08 predictor-to-BL documentation, D09 selection/accounting documentation, D11 consistency reproduction and D12 paper handoff are prepared. D01/D02 and D04 calculations are available locally; public source-data admission remains pending. D10 publication status and the version URL are recorded in [release_review.md](docs/release_review.md).

[Detailed progress](docs/deliverables.csv), [consolidated Vietnamese handoff and remaining tasks](docs/paper_handoff_vi.md), [VN30TRI source findings](docs/benchmark_source_status.md). The private advisor package contains the full benchmark tables, D04 summaries, figures and a LaTeX fragment. Manuscript integration/approval and any expanded data distribution remain with the authors; no additional strategy training is required by guide_5.

## Data and replication scope

The package contains code and derived research outputs. Raw vendor prices, private input ledgers and fitted model objects require authorized access. Readers can regenerate the distributed summaries/figures and verify class linking from released daily contributions. Recomputing those daily contributions from original asset returns or refitting historical models requires the frozen private inputs. Source-copy hashes distinguish original experimental code from newly organized analysis code.

Equity adjusted closes are retrospective provider snapshots. GOLD and VFF remain valuation proxies with assumed availability and next-close marking. Fees of0/10/25/50 bps per traded side are hypothetical. The code license does not license vendor data; future index inputs require their own access and sharing conditions.

## Citation and release

Use the versioned release rather than the moving default branch:

> Khang, Nguyen Phuc (2026). *Vietnam Long-Only Multi-Asset Portfolio — Research Code and Derived Results* (Version 0.2.0) [Software]. GitHub. https://github.com/khangng2611/vietnam-portfolio-research/releases/tag/v0.2.0

Machine-readable metadata are in [CITATION.cff](CITATION.cff). No DOI has been assigned. The original local author-review tag `v0.1.0-rc1` remains unchanged.
