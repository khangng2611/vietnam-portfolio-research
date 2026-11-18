# Bàn giao bằng chứng và research repository cho paper_5

Ngày 18/11/2026. Phiên bản 0.1.0.

Đã tổ chức source khoa học và kết quả cần cho paper trong paper5_research, với entry point tái tạo bảng/hình chạy độc lập từ thư mục này. Phần bổ sung trích lại dữ liệu quyết định/return/holdings đã lưu. Kết quả chính C1/B1/B2 và A/B được đối chiếu theo quy ước đã nghiệm thu. D01/D02 và D04 còn chờ daily VN30TRI hợp lệ. D10 có metadata tác giả và MIT đã xác nhận; trạng thái public/version được ghi riêng trong hồ sơ phát hành.

## 1. Trạng thái D01–D12

| ID | Trạng thái | Đầu ra |
| --- | --- | --- |
| D01 | PENDING_SOURCE | VN30TRI OOS641 |
| D02 | PENDING_SOURCE | VN30TRI IS906 |
| D03 | COMPLETE | 294 dated portfolio drawdown episodes |
| D04 | PENDING_D01_D02 | Objective VN30TRI decline labels |
| D05 | COMPLETE | Daily class contributions and linked wealth |
| D06 | COMPLETE | Three manuscript figures plus underwater, PNG/PDF/SVG |
| D07 | COMPLETE | 32-series source and units dictionary |
| D08 | COMPLETE | Finalized XGBoost to BL source and timing documentation |
| D09 | COMPLETE | Selection, constraints and accounting code/source map |
| D10 | COMPLETE | Public research repository and versioned v0.1.1 software citation |
| D11 | COMPLETE | 24 main + 128 AB metrics and event turnover reproduced |
| D12 | COMPLETE_LOCAL_HANDOFF | Vietnamese results/paper integration handoff |

## 2. D03 — Các drawdown sâu nhất

| Phase | Nhánh | Đỉnh | Đáy | Độ sâu % | Phiên dưới đỉnh | Hồi phục |
| --- | --- | --- | --- | --- | --- | --- |
| IS | B1 | 2020-02-20 | 2020-03-30 | -17.98 | 132 | 2020-08-28 |
| IS | B2 | 2022-04-06 | 2022-11-15 | -18.12 | 371 | Chưa hồi phục trong phase |
| IS | C1 | 2020-02-20 | 2020-03-30 | -17.66 | 131 | 2020-08-27 |
| OOS | B1 | 2026-02-24 | 2026-03-23 | -10.26 | 45 | Chưa hồi phục trong phase |
| OOS | B2 | 2025-04-01 | 2025-04-09 | -9.51 | 34 | 2025-05-26 |
| OOS | C1 | 2026-02-24 | 2026-03-23 | -10.18 | 45 | Chưa hồi phục trong phase |

Toàn bộ294 episodes có trong results/derived/drawdown_episodes.csv. Bảng trên chọn episode sâu nhất trong từng cặp phase/nhánh. Phiên dưới đỉnh đếm đến hồi phục hoặc ngày cuối phase, loại phiên hồi phục. Một episode nông hơn có thể kéo dài hơn episode sâu nhất. Những đợt cuối kỳ chưa hồi phục được ghi right-censored.

OOS C1 và B1 có đáy sâu nhất tại 23/03/2026 sau đỉnh 24/02/2026, còn ở dưới đỉnh khi chốt mẫu 29/04/2026. B2 có MDD OOS tại 09/04/2025 sau đỉnh 01/04/2025, hồi phục 26/05/2025. IS của B2 có episode từ 06/04/2022 chưa hồi phục ở cuối IS. Diễn giải gắn với từng cửa sổ riêng đã chuẩn hóa anchor.

Có thể chèn bảng các episode sâu nhất vào phần Results hoặc phụ lục. Đồ thị underwater giúp trình bày độ sâu và thời gian nắm giữ dưới đỉnh.

## 3. D05 — Đóng góp vào tăng NAV theo lớp tài sản

Đơn vị là điểm phần trăm của NAV đầu kỳ. Với NAV đầu kỳ1, ba phần cộng lại bằng100×(NAV cuối−1).

| Phase | Nhánh | Equities | GOLD | VFF | Tổng tăng NAV |
| --- | --- | --- | --- | --- | --- |
| IS | B1 | 60.67 | 6.45 | 11.98 | 79.10 |
| IS | B2 | 50.31 | 2.79 | 12.92 | 66.03 |
| IS | C1 | 58.85 | 6.74 | 11.92 | 77.51 |
| OOS | B1 | 46.90 | 17.80 | 6.34 | 71.04 |
| OOS | B2 | 56.60 | 18.06 | 7.78 | 82.44 |
| OOS | C1 | 45.67 | 19.62 | 6.35 | 71.64 |

Công thức theo interval là c_class,t = tổng w_held,i,t × r_i,t. Đóng góp wealth cả kỳ là tổng NAV_(t−1) × c_class,t. Đây là phép phân rã theo đường NAV đã thực hiện. Cột tổng của OOS là 71,64% cho C1, 71,04% cho B1 và 82,44% cho B2, khác đơn vị CAGR năm. Sum simple daily contributions được giữ ở cột riêng trong CSV.

Đối chiếu daily contributions với gross return cho sai số lớn nhất 3,02e−16. Tổng linked wealth contributions khớp NAV cuối với sai số tối đa 6,27e−14. Daily held weights được dùng đúng đầu return. Dữ liệu giá gốc chỉ tham gia extraction tại máy được cấp quyền.

Đoạn tiếng Anh có thể dùng trong Results, sau khi tác giả rà soát số làm tròn

> We decompose gross portfolio returns using the weights held at the start of each valuation interval. Daily class contributions are linked using prior portfolio wealth, so their phase totals reconcile with the change in NAV. In the observed OOS period, the C1 equity, GOLD and VFF components contribute 45.67, 19.62 and 6.35 percentage points of initial wealth. The corresponding B1 contributions are 46.90, 17.80 and 6.34 points, and B2 contributions are 56.60, 18.06 and 7.78 points.

## 4. D06 — Hình đưa vào manuscript

Ba tên file đang được guide ghi nhận đã có trong figures/, mỗi hình có PNG 300 dpi, PDF và SVG.

- C1_OOS_wealth dùng 641 gross return với anchor 29/09/2023.
- C1_class_weights dùng tỷ trọng đang nắm giữ tại đầu return cho cả ba nhánh.
- C1_cost_sensitivity dùng lưới phí giả định 0/10/25/50 bps cho mỗi phía mua hoặc bán.
- portfolio_underwater trình bày drawdown IS/OOS với anchor riêng.

Mapping chi tiết nằm trong docs/results_guide.md. paper_5.tex và project_5.md chưa được cung cấp trong thư mục làm việc này, nên bản bàn giao đưa ra vị trí chèn và filenames để nhóm viết paper tích hợp.

## 5. D01/D02 và D04 — Phần còn chờ

Đã đọc Ground Rules HOSE v4.0/Decision 747 được guide dẫn và tài liệu FiinQuant cho daily historical close. Chưa nhận được gói daily VN30TRI có nghiên cứu/nguồn/vintage phù hợp. Factsheet và phương pháp xác nhận danh tính chỉ số. Chúng chưa cung cấp chuỗi mức chỉ số để tính 906/641 return. Kết quả benchmark hiện để trống có trạng thái rõ ràng. Ngày thị trường giảm theo drawdown 10% sẽ được xác định khi có dữ liệu này.

code/benchmark.py đã được chuẩn bị và kiểm thử trên fixture tổng hợp tạm thời. Quy tắc căn chỉnh giữ nguyên hai đầu mỗi interval của cả index và portfolio. Nếu chỉ có mẫu ngắn hơn, bảng ghi COMMON_CONTIGUOUS và tính lại các danh mục trên chính tập ngày đó. D04 full-history chỉ xuất khi hai phase đều đủ. Quyền nghiên cứu và quyền tái phân phối cần được xác nhận từ dữ liệu thực nhận. Chi tiết nguồn và bước tiếp theo nằm ở docs/benchmark_source_status.md.

## 6. D08/D09 — Source khoa học và phân biệt phiên bản

code/frozen_baseline chứa các module gốc cho selector, features, labels, ensemble, views, BL, optimizer và accounting/timing. code/frozen_experiments/run.py là runner A/B trong layout gốc. code/accounting.py sao nguyên byte helper gốc. code/fixed_rule.py trích nguyên hàm chia tỷ trọng C1 và import numpy.

code/reproduce.py là entry point tái tạo bảng/hình cho người đọc từ outputs đã phát hành. Nó tính lại 24 dòng metrics C1/B1/B2 và128 dòng A/B/chi phí, annual turnover từ event ledger, episodes và class linking. Source-map chỉ rõ source/hash gốc so với source được tổ chức để công bố. Tài liệu methodology mô tả 8 features, label 5 phiên, training cutoff/purge/scaler, seeds 42–46, ánh xạ annual views sang daily Q, Omega và matched controls của B1/B2.

## 7. D10/D12 — Release và citation

Tác giả đã xác nhận tên **Nguyen Phuc Khang** và chọn **MIT** cho mã nguồn do nhóm sở hữu ngày 18/11/2026. Bản v0.1.1 được chuẩn bị tại repository nghiên cứu riêng. Trạng thái phát hành được ghi trong docs/release_review.md và docs/deliverables.csv; CITATION.cff ghi metadata trích dẫn.

Đường dẫn phiên bản: https://github.com/khangng2611/vietnam-portfolio-research/releases/tag/v0.1.1

> Khang, Nguyen Phuc (2026). Vietnam Long-Only Multi-Asset Portfolio — Research Code and Derived Results (Version 0.1.1) [Software]. GitHub.

Đề xuất Data/Code Availability:

> The versioned research repository contains the portfolio methodology, original scientific source snapshots, dated strategy outputs, and scripts for regenerating the reported tables and figures. Vendor price histories and restricted historical records require access through their respective providers. The release documents which analyses can be reproduced from the shared outputs and which require authorized source data.

NOTICE.md phân biệt license phần mềm với quyền dữ liệu. Dữ liệu giá gốc và fitted objects không nằm trong repository. Chưa có DOI được cấp. Tag local v0.1.0-rc1 ban đầu được giữ nguyên. D01/D02/D04 còn chờ dữ liệu VN30TRI hợp lệ.

## 8. Đối chiếu và giới hạn

24 metrics C1/B1/B2 cùng 128 metrics A/B được tính lại từ dated returns và event trades, dung sai 1e−10. 6 tests nhỏ kiểm tra drawdown/recovery/anchor, wealth linking và index interval alignment. Replay/QA chạy từ một output folder ngoài repository. Source-map ghi 41 file khoa học gốc được sao/trích có hash.

Hồ sơ C cũ có câu ghi 48 dòng metrics trong khi CSV có 24. Package hiện tại ghi và kiểm tra đúng 24 dòng. Đây là sửa mô tả đóng gói. Các con số NAV/CAGR/Sharpe/MDD/TO được nghiệm thu vẫn khớp. Những scripts cũ cần workstation paths/inputs không được dùng làm entry point public.

Universe30 mã cố định, publication/revision vintages chưa đầy đủ, GOLD/VFF là proxy định giá và phí là kịch bản giả định. Holdout đã được quan sát trong dự án. Những kết quả này mô tả cách một kiến trúc chọn đại diện và phân bổ vốn hoạt động trên mẫu hiện tại. Diễn giải cho paper cần giữ phạm vi đó cùng khoảng bất định đã báo cáo.
