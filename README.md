# Vietnam Long-Only Multi-Asset Portfolio

This research package studies representative equity selection followed by capital allocation for Vietnamese long-only portfolios. Five dated correlation representatives from a static 30-stock basket are combined with a GOLD valuation proxy and VFF bond-fund NAV proxy. B1 uses a Black–Litterman equilibrium prior. B2 adds saved XGBoost views. C1 uses VFF 30% and equal shares of the remaining 70% across the other six instruments.

This is the local `0.1.0-rc1` release candidate prepared for author review under guide_5.md. Public release, full paper authorship and project licensing are pending approval. CITATION.cff records the known contributor provisionally. A verified public version permalink/DOI will be added after actual publication. The upstream development project is [portfolio-optimization](https://github.com/khangng2611/portfolio-optimization).

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
CITATION.cff              Provisional citation metadata awaiting author/release approval
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

D03 drawdowns, D05 class P&L, D06 figures, D07 dictionary, D08 predictor-to-BL documentation, D09 selection/accounting documentation, D11 consistency reproduction and D12 paper handoff are prepared. D01/D02 VN30TRI data acquisition and dependent D04 market labels remain pending. D10 has a curated, locally versioned candidate and awaits author approval for the public repository/release.

[Detailed progress](docs/deliverables.csv), [Vietnamese handoff](docs/paper_handoff_vi.md), [VN30TRI source findings](docs/benchmark_source_status.md).

## Data and replication scope

The package contains code and derived research outputs for author review. Raw vendor prices, private input ledgers and fitted model objects require authorized access. Public readers can regenerate the distributed summaries/figures and verify class linking from released daily contributions. Recomputing those daily contributions from original asset returns or refitting historical models requires the frozen private inputs. Source-copy hashes distinguish original experimental code from newly organized analysis code.

Equity adjusted closes are retrospective provider snapshots. GOLD and VFF remain valuation proxies with assumed availability and next-close marking. Fees of0/10/25/50 bps per traded side are hypothetical. Index source data and dated derived-output sharing rights need author clearance before public distribution.

## Citation and release

The local candidate is tagged `v0.1.0-rc1`. Before manuscript citation, approve the full author list, license and sharing scope, publish a stable release to an accessible repository, and verify its version permalink. Record a DOI only after an archive service has assigned one. The current upstream development URL identifies the development project, while this candidate's public release link is still pending.
