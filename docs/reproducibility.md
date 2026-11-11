# Reproduction and source versions

Use Python 3.11 or later. The verified research interpreter is Python 3.13 with numpy 2.2.6, pandas 2.2.3 and matplotlib 3.10.8. A minimal environment is recorded in requirements.txt. The complete original research environment is retained as a reference in reproducibility/original_environment.txt.

From the release root, run

```sh
python -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -B -m unittest discover -s reproducibility -p 'test_*.py' -v
.venv/bin/python -B code/reproduce.py --output /path/to/new/reproduced-results
```

The main command regenerates 24 C1/B1/B2 metric records, 128 A/B strategy-phase-cost records, phase NAV/drawdown paths, all episodes, deepest episodes, class-attribution summaries/reconciliation and four figures in PNG/PDF/SVG. It verifies accepted metric values and event-based annual turnover to 1e-10. File format rounding is handled at numerical precision. Rendering output can differ by fonts/backend without changing the dated values.

`code/accounting.py` is a byte-identical copy of the original experiment helper. `code/frozen_baseline/` contains the accepted selection, XGBoost feature/training/views, BL and optimizer source snapshot. `code/frozen_experiments/run.py` is the archived A/B runner and requires its original package layout, data and saved precursor artifacts. `code/fixed_rule.py` extracts the prescribed C1 allocation function verbatim. `reproducibility/source_map.json` identifies every original source and published copy/extraction. Original source versions and release-analysis code have distinct roles.

`reproducibility/prepare.py` was executed inside the parent portfolio-optimization checkout to curate the reference outputs and compute daily class contributions using private prices. It expects that original sibling directory layout. It is an extraction recipe for authorized authors. `code/reproduce.py` is the portable reader entry point and needs only files distributed in this release candidate. No old packaging scripts or external workstation paths are required by that entry point.

The three immutable source identities are availability-observed-contract-20261012T233110, core-evidence-20261023T211011 and extensions-C-20261104T210906. Their input/source hashes and source-map are recorded. This release extracts existing results. Historical fitting, price acquisition and original first-publication vintages require authorized inputs. The previous C package had a prose count of48 metrics although its CSV contains 24. The new package reproduces24 and records the packaging correction without changing accepted numeric results.

## VN30TRI when admitted data become available

Use a new output folder and provide a lawful daily-level CSV with index_date/index_level. Metadata must contain identifier=VN30TRI, return_type=total_return, currency=VND, provider, source_url, retrieved_at, dividend_method, vintage, rights_evidence and research_use_permitted=true. Vendor-record dates can be retained as additional evidence. Actual source rights must be checked by the authors.

```sh
.venv/bin/python -B code/benchmark.py --levels /authorized/VN30TRI.csv --metadata /authorized/VN30TRI.metadata.json --output /path/to/new/benchmark-results
```

The script handles IS/OOS independently, includes each phase anchor and checks that the index return interval has the same two session endpoints as its portfolio counterpart. Missing and extra source sessions remain visible. Full-sample rows are distinguished from a longest contiguous common sample with all portfolio metrics recomputed there. It exports coverage, alignment and descriptive metrics, and three-path-plus-C1 wealth context. When both phases have full history, it exports continuous-peak market states and state-specific descriptive return statistics. Index turnover remains N/A. No empirical benchmark file has been admitted in this release candidate.
