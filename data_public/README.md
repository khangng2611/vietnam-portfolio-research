# Data access and admitted inputs

series_dictionary.csv contains metadata for the32 frozen study series. Raw vendor prices and private historical eligibility/model records require authorized access. Derived research results are curated under results/reference/ for author review of sharing rights.

For VN30TRI, supply an authorized CSV with index_date,index_level and retain vendor_record_date where supplied. Include both phase anchors 2020-02-18 and 2023-09-29 plus every aligned return endpoint through2026-04-29. Metadata must identify HOSE VN30TRI, VND total-return variant, provider, actual data source URL, dividend methodology, retrieval timestamp, historical vintage/coverage, research-use evidence and redistribution conditions.

See docs/benchmark_source_status.md and code/benchmark.py. External input files are kept in private_inputs/ or an authorized directory outside the public package. No example index price series is distributed here.
