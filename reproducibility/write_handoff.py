"""Write the Vietnamese manuscript handoff from regenerated release tables."""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]


def markdown(headers, rows):
    lines = ['| ' + ' | '.join(headers) + ' |', '| ' + ' | '.join(['---'] * len(headers)) + ' |']
    lines.extend('| ' + ' | '.join(map(str, row)) + ' |' for row in rows)
    return '\n'.join(lines)


def main():
    derived = ROOT / 'results/derived'
    episodes = pd.read_csv(derived / 'drawdown_episodes.csv')
    deepest = episodes.sort_values('depth').groupby(['strategy', 'phase']).head(1).sort_values(['phase', 'strategy'])
    drawdowns = markdown(['Phase', 'Nhánh', 'Đỉnh', 'Đáy', 'Độ sâu %', 'Phiên dưới đỉnh', 'Hồi phục'],
                         [[r.phase, r.strategy, r.peak_date, r.trough_date, f'{100*r.depth:.2f}', r.underwater_sessions,
                           'Chưa hồi phục trong phase' if pd.isna(r.recovery_date) else r.recovery_date] for r in deepest.itertuples()])
    contribution = pd.read_csv(derived / 'class_contribution_summary.csv')
    pivot = contribution.pivot(index=['phase', 'strategy'], columns='asset_class', values='linked_contribution_percentage_points')
    attribution = markdown(['Phase', 'Nhánh', 'Equities', 'GOLD', 'VFF', 'Tổng tăng NAV'],
                           [[phase, strategy, f'{row.equities:.2f}', f'{row.GOLD:.2f}', f'{row.VFF:.2f}', f'{row.sum():.2f}']
                            for (phase, strategy), row in pivot.iterrows()])
    progress = pd.read_csv(ROOT / 'docs/deliverables.csv')
    status = markdown(['ID', 'Trạng thái', 'Đầu ra'], [[r.item, r.status, r.description] for r in progress.itertuples()])
    text = f'''# Bàn giao bằng chứng và research repository cho paper_5

Ngày 11/11/2026. Phiên bản local release candidate0.1.0-rc1.

Đã tổ chức source khoa học và kết quả cần cho paper trong paper5_research, với entry point tái tạo bảng/hình chạy độc lập từ thư mục này. Phần bổ sung trích lại dữ liệu quyết định/return/holdings đã lưu. Kết quả chính C1/B1/B2 và A/B được đối chiếu theo quy ước đã nghiệm thu. D01/D02 và D04 còn chờ daily VN30TRI hợp lệ. D10 đã có package để duyệt, cần xác nhận tác giả, license và phạm vi public trước khi có link release để cite.

## 1. Trạng thái D01–D12

{status}

## 2. D03 — Các drawdown sâu nhất

{drawdowns}

Toàn bộ294 episodes có trong results/derived/drawdown_episodes.csv. Bảng trên chọn episode sâu nhất trong từng cặp phase/nhánh. Phiên dưới đỉnh đếm đến hồi phục hoặc ngày cuối phase, loại phiên hồi phục. Một episode nông hơn có thể kéo dài hơn episode sâu nhất. Những đợt cuối kỳ chưa hồi phục được ghi right-censored.

OOS C1 và B1 có đáy sâu nhất tại23/03/2026 sau đỉnh24/02/2026, còn ở dưới đỉnh khi chốt mẫu29/04/2026. B2 có MDD OOS tại09/04/2025 sau đỉnh01/04/2025, hồi phục26/05/2025. IS của B2 có episode từ06/04/2022 chưa hồi phục ở cuối IS. Diễn giải gắn với từng cửa sổ riêng đã chuẩn hóa anchor.

Có thể chèn bảng các episode sâu nhất vào phần Results hoặc phụ lục. Đồ thị underwater giúp trình bày độ sâu và thời gian nắm giữ dưới đỉnh.

## 3. D05 — Đóng góp vào tăng NAV theo lớp tài sản

Đơn vị là điểm phần trăm của NAV đầu kỳ. Với NAV đầu kỳ1, ba phần cộng lại bằng100×(NAV cuối−1).

{attribution}

Công thức theo interval là c_class,t = tổng w_held,i,t × r_i,t. Đóng góp wealth cả kỳ là tổng NAV_(t−1) × c_class,t. Đây là phép phân rã theo đường NAV đã thực hiện. Cột tổng của OOS là71,64% cho C1,71,04% cho B1 và82,44% cho B2, khác đơn vị CAGR năm. Sum simple daily contributions được giữ ở cột riêng trong CSV.

Đối chiếu daily contributions với gross return cho sai số lớn nhất3,02e−16. Tổng linked wealth contributions khớp NAV cuối với sai số tối đa6,27e−14. Daily held weights được dùng đúng đầu return. Dữ liệu giá gốc chỉ tham gia extraction tại máy được cấp quyền.

Đoạn tiếng Anh có thể dùng trong Results, sau khi tác giả rà soát số làm tròn

> We decompose gross portfolio returns using the weights held at the start of each valuation interval. Daily class contributions are linked using prior portfolio wealth, so their phase totals reconcile with the change in NAV. In the observed OOS period, the C1 equity, GOLD and VFF components contribute45.67,19.62 and6.35 percentage points of initial wealth. The corresponding B1 contributions are46.90,17.80 and6.34 points, and B2 contributions are56.60,18.06 and7.78 points.

## 4. D06 — Hình đưa vào manuscript

Ba tên file đang được guide ghi nhận đã có trong figures/, mỗi hình có PNG300dpi, PDF và SVG.

- C1_OOS_wealth dùng641 gross return với anchor29/09/2023.
- C1_class_weights dùng tỷ trọng đang nắm giữ tại đầu return cho cả ba nhánh.
- C1_cost_sensitivity dùng lưới phí giả định0/10/25/50bps cho mỗi phía mua hoặc bán.
- portfolio_underwater trình bày drawdown IS/OOS với anchor riêng.

Mapping chi tiết nằm trong docs/results_guide.md. paper_5.tex và project_5.md chưa được cung cấp trong thư mục làm việc này, nên bản bàn giao đưa ra vị trí chèn và filenames để nhóm viết paper tích hợp.

## 5. D01/D02 và D04 — Phần còn chờ

Đã đọc Ground Rules HOSE v4.0/Decision747 được guide dẫn và tài liệu FiinQuant cho daily historical close. Chưa nhận được gói daily VN30TRI có nghiên cứu/nguồn/vintage phù hợp. Factsheet và phương pháp xác nhận danh tính chỉ số. Chúng chưa cung cấp chuỗi mức chỉ số để tính906/641 return. Kết quả benchmark hiện để trống có trạng thái rõ ràng. Ngày thị trường giảm theo drawdown10% sẽ được xác định khi có dữ liệu này.

code/benchmark.py đã được chuẩn bị và kiểm thử trên fixture tổng hợp tạm thời. Quy tắc căn chỉnh giữ nguyên hai đầu mỗi interval của cả index và portfolio. Nếu chỉ có mẫu ngắn hơn, bảng ghi COMMON_CONTIGUOUS và tính lại các danh mục trên chính tập ngày đó. D04 full-history chỉ xuất khi hai phase đều đủ. Quyền nghiên cứu và quyền tái phân phối cần được xác nhận từ dữ liệu thực nhận. Chi tiết nguồn và bước tiếp theo nằm ở docs/benchmark_source_status.md.

## 6. D08/D09 — Source khoa học và phân biệt phiên bản

code/frozen_baseline chứa các module gốc cho selector, features, labels, ensemble, views, BL, optimizer và accounting/timing. code/frozen_experiments/run.py là runner A/B trong layout gốc. code/accounting.py sao nguyên byte helper gốc. code/fixed_rule.py trích nguyên hàm chia tỷ trọng C1 và import numpy.

code/reproduce.py là entry point tái tạo bảng/hình cho người đọc từ outputs đã phát hành. Nó tính lại24 dòng metrics C1/B1/B2 và128 dòng A/B/chi phí, annual turnover từ event ledger, episodes và class linking. Source-map chỉ rõ source/hash gốc so với source được tổ chức để công bố. Tài liệu methodology mô tả8 features, label5phiên, training cutoff/purge/scaler, seeds42–46, ánh xạ annual views sang daily Q, Omega và matched controls của B1/B2.

## 7. D10/D12 — Release và citation

Đã chuẩn bị README, CITATION.cff ở mức dự thảo, trạng thái LICENSE, requirements tối giản, source-map, dữ liệu dẫn xuất, tests và manifest. Candidate có Git commit/tag local riêng và gói ZIP để rà soát. Repository phần mềm hiện hữu ở upstream khangng2611/portfolio-optimization. Chưa tạo public release cho candidate này, chưa có DOI được cấp.

Trước khi đưa link vào paper, nhóm tác giả cần xác nhận danh sách tác giả/contributors, license cho code và quyền chia sẻ derived outputs, rồi chọn publish dưới upstream hiện tại hoặc repository nghiên cứu riêng. Khi release đã tồn tại, kiểm tra URL theo version/tag hoặc DOI thực tế và cập nhật CITATION.cff. guide_5 mục8.6 đặt bước này sau khi nội dung được tác giả duyệt.

Đề xuất Data/Code Availability để nhóm tác giả hoàn thiện sau khi có public link thực

> The versioned research repository contains the portfolio methodology, original scientific source snapshots, dated strategy outputs, and scripts for regenerating the reported tables and figures. Vendor price histories and restricted historical records are available through their respective providers under applicable access conditions. The release documents which analyses can be reproduced from the shared outputs and which require authorized source data.

Cần thêm public version permalink đã kiểm tra vào câu trên trước submission. Metadata tác giả hiện dùng Nguyen Phuc Khang ở mức contributor đã biết và chờ xác nhận đồng tác giả. LICENSE chưa cấp giấy phép mở mới cho code hoặc quyền vendor data.

## 8. Đối chiếu và giới hạn

24 metrics C1/B1/B2 cùng128 metrics A/B được tính lại từ dated returns và event trades, dung sai1e−10.6 tests nhỏ kiểm tra drawdown/recovery/anchor, wealth linking và index interval alignment. Replay/QA chạy từ một output folder ngoài repository. Source-map ghi41 file khoa học gốc được sao/trích có hash.

Hồ sơ C cũ có câu ghi48 dòng metrics trong khi CSV có24. Package hiện tại ghi và kiểm tra đúng24 dòng. Đây là sửa mô tả đóng gói. Các con số NAV/CAGR/Sharpe/MDD/TO được nghiệm thu vẫn khớp. Những scripts cũ cần workstation paths/inputs không được dùng làm entry point public.

Universe30mã cố định, publication/revision vintages chưa đầy đủ, GOLD/VFF là proxy định giá và phí là kịch bản giả định. Holdout đã được quan sát trong dự án. Những kết quả này mô tả cách một kiến trúc chọn đại diện và phân bổ vốn hoạt động trên mẫu hiện tại. Diễn giải cho paper cần giữ phạm vi đó cùng khoảng bất định đã báo cáo.
'''
    (ROOT / 'docs/paper_handoff_vi.md').write_text(text)
    for source in (derived / 'figures').iterdir():
        if source.suffix in ['.png', '.pdf', '.svg']:
            import shutil
            shutil.copy2(source, ROOT / 'figures' / source.name)
    print('Wrote Vietnamese handoff and finalized figure exports')


if __name__ == '__main__':
    main()
