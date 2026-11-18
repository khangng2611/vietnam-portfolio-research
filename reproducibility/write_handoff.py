"""Write the Vietnamese manuscript handoff, including an explicit private benchmark run."""
import argparse
import json
import os
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]


def markdown(headers, rows):
    lines = ['| ' + ' | '.join(headers) + ' |', '| ' + ' | '.join(['---'] * len(headers)) + ' |']
    lines.extend('| ' + ' | '.join(map(str, row)) + ' |' for row in rows)
    return '\n'.join(lines)


def benchmark_section(run):
    checks = json.loads((run / 'completion_checks.json').read_text())
    metrics = pd.read_csv(run / 'reported/metrics.csv')
    coverage = pd.read_csv(run / 'reported/coverage.csv')
    states = pd.read_csv(run / 'reported/market_state_summary.csv')
    effects = pd.read_csv(run / 'sensitivity_effects.csv')
    if (coverage.set_index('phase').matched_returns.to_dict() != {'IS': 906, 'OOS': 641}
            or not coverage.full_sample.all() or len(metrics) != 8 or len(states) != 12
            or checks['market_state_label_changes'] != 0):
        raise ValueError('Benchmark handoff requires the verified full-sample two-case run')
    link = Path(os.path.relpath(run, ROOT / 'docs')).as_posix()
    sections = []
    for phase, item in [('IS', 'D02'), ('OOS', 'D01')]:
        rows = metrics.loc[metrics.phase.eq(phase)]
        table = markdown(['Nhánh', 'N', 'NAV', 'CAGR %', 'Vol %', 'Sharpe', 'MDD %'],
                         [['VN30TRI — Dragon Capital' if r.strategy == 'VN30TRI_reported' else r.strategy,
                           r.N, f'{r.final_nav:.4f}', f'{100*r.ann_return:.2f}',
                           f'{100*r.ann_volatility:.2f}', f'{r.sharpe:.3f}', f'{100*r.max_drawdown:.2f}']
                          for r in rows.itertuples()])
        sections.append(f'### {item} — {phase}\n\n{table}\n\n'
                        f'![Market context {phase}]({link}/reported/VN30TRI_reported_context_{phase}.png)')
    for phase in ['IS', 'OOS']:
        table = markdown(['Trạng thái', 'Nhánh', 'N', 'Mean/ngày %', 'Phiên âm %',
                          'Ngày xấu nhất %', 'Vol năm %', 'Lãi kép tập con %'],
                         [['DD ≥ 10%' if r.market_state == 'MARKET_DRAWDOWN_10' else 'Còn lại',
                           r.strategy, r.N, f'{100*r.mean_daily_return:.4f}',
                           f'{100*r.fraction_negative:.2f}', f'{100*r.worst_day:.2f}',
                           f'{100*r.annualized_volatility:.2f}', f'{100*r.compounded_subset_return:.2f}']
                          for r in states.loc[states.phase.eq(phase)].itertuples()])
        sections.append(f'### D04 — {phase}\n\n{table}')
    sharpe = effects.loc[effects.phase.eq('OOS') & effects.metric.eq('sharpe')].iloc[0]
    return f'''Nguồn chính là [VN30TR Index do Dragon Capital công bố](https://www.dragoncapital.com.vn/institution/vi/product/a0eJ2000001X9zhIAC/vn30), truy xuất ngày 18/11/2026. Trường fundBenchmarkData.navPrice được lấy riêng với benchmarkFundReportCode=VN30TR Index; không dùng NAV ETF hoặc VN30 price index. Đây là chuỗi nhà cung cấp, không phải toàn bộ chỉ số tự dựng từ rổ cổ phiếu cố định.

Chuỗi nguồn có 1.576 mức từ 02/01/2020 đến 29/04/2026. IS neo 18/02/2020 tại 950,50, gồm 906 return từ 19/02/2020 đến 29/09/2023. OOS neo 29/09/2023 tại 1.346,62, gồm 641 return từ 02/10/2023 đến 29/04/2026; mức cuối 2.442,52. Đủ hai đầu từng interval, không thiếu phiên trong lịch yêu cầu, không forward-fill. Hai phase có anchor riêng; NAV anchor=1 được tính vào MDD. Dùng 252 phiên/năm, risk-free ngày 1,06^(1/252)−1, sample std(ddof=1). Bảng danh mục là gross 0 bps; index turnover/chi phí giao dịch của người nắm giữ là N/A.

{(chr(10) * 2).join(sections[:2])}

Trong IS, ba danh mục có CAGR/Sharpe cao hơn và MDD ít âm hơn benchmark quan sát; IS là giai đoạn phát triển, không phải holdout mới. Trong OOS, C1/B1 có CAGR thấp hơn VN30TRI nhưng volatility/MDD thấp hơn và Sharpe cao hơn. B2 có CAGR cao hơn khoảng 0,29 điểm phần trăm và rủi ro quan sát thấp hơn. Đây là market context: benchmark 100% cổ phiếu, còn danh mục có GOLD/VFF và ràng buộc khác. Chưa kiểm định ý nghĩa thống kê của chênh lệch với benchmark; không kết luận alpha hoặc superiority tổng quát.

### D04 — Quy tắc và kết quả

market_drawdown(t)=VN30TRI(t)/running_peak(t)−1; nhãn MARKET_DRAWDOWN_10 khi ≤−10%, còn lại OTHER_OBSERVED_DAYS. Peak liên tục từ 18/02/2020 qua ranh giới IS/OOS. Nhãn ex-post tại close có cả phiên hồi phục khi index vẫn dưới đỉnh, không phải tín hiệu biết trước phiên hoặc tập mọi ngày có return âm.

{(chr(10) * 2).join(sections[2:])}

IS có 420 phiên DD ≥ 10% và 486 phiên còn lại; OOS có 366 và 275 phiên. Trong nhóm OOS DD ≥ 10%, mean daily return C1/B1/B2 lần lượt khoảng 0,0058%/0,0057%/0,0362%. Lãi kép tập con nhân return các ngày được gán nhãn, có thể không liên tục; không phải lợi nhuận của chiến lược giao dịch thực thi, không annualize và không cộng trực tiếp hai nhóm. Không suy ra mô hình dự báo hoặc né tránh được thị trường giảm.

![D04 — Drawdown thị trường và hai phase]({link}/D04_market_drawdown_timeline.png)

### Chất lượng nguồn và độ nhạy

Nguồn giữ mức 1.552,85 trong 05–07/05/2025 dù price index biến động. Bảng chính giữ nguyên mức nguồn. Nhánh riêng tái tạo ba phiên bằng hệ số TRI/price ngày 29/04/2025, giả định dividend yield bằng 0 trong khoảng; sai lệch kiểm tra đầu mút 08/05/2025 là 0,00935 điểm, dưới ngưỡng 0,02 đã đặt trước tính metrics. Giả định này chưa phải xác minh chính thức cổ tức hoặc nguyên nhân đứng giá. Sharpe benchmark OOS đổi {sharpe.reported:.6f} → {sharpe.sensitivity:.6f}; NAV/CAGR/MDD không đổi và 0 ngày đổi nhãn D04. Không chọn nhánh theo kết quả thuận lợi cho mô hình.

Một điểm mới nhất được đối chiếu với TradingView để kiểm tra danh tính; chưa đối chiếu độc lập mọi mức lịch sử hoặc revisions. Một số sai khác giữa hai nguồn price index được lưu trong quality flags, không dùng để sửa im lặng chuỗi TRI. Báo cáo phương pháp cổ tức tham chiếu HOSE Ground Rules: total return tái đầu tư cổ tức tiền mặt theo quy tắc chỉ số; chuỗi vendor là snapshot hồi cứu. Điều kiện chia sẻ raw/chuỗi ngày/hình chưa được xác nhận, nên artifacts giữ riêng, chưa nằm trong tag v0.1.1.

[Báo cáo nguồn và phân tích chi tiết]({link}/report_vi.md), [coverage]({link}/reported/coverage.csv), [metrics]({link}/reported/metrics.csv), [D04]({link}/reported/market_state_summary.csv), [manifest]({link}/manifest.json). Liên kết artifacts chỉ dùng tại checkout có dữ liệu riêng. Chạy lại phần bàn giao bằng `python reproducibility/write_handoff.py --benchmark-run <thư-mục-run-đã-xác-minh>`.

Đoạn đề xuất đưa vào Results, sau khi nhóm tác giả duyệt:

> Over the 641 OOS returns, the provider-reported VN30 total-return benchmark has a CAGR of 26.38%, annualized volatility of 19.84%, Sharpe ratio of 0.986 and maximum drawdown of −16.95%. C1 and B1 exhibit lower returns and lower observed risk, whereas B2 has a slightly higher CAGR of 26.66% with a Sharpe ratio of 1.367. These comparisons provide market context for multi-asset portfolios with different constraints; they do not establish statistically significant outperformance.

> Using a continuous benchmark peak, 366 OOS observations fall at least 10% below the previous peak. Mean daily portfolio returns in this subset are 0.0058%, 0.0057% and 0.0362% for C1, B1 and B2. This ex-post classification includes recovery days and is descriptive rather than a tradable regime signal.
'''


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--benchmark-run', type=Path, required=True)
    args = parser.parse_args()
    benchmark = benchmark_section(args.benchmark_run.resolve())
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

Ngày 18/11/2026. Bản bàn giao hoàn thiện cho giảng viên; code release v0.2.0 có phạm vi công bố riêng với báo cáo benchmark đầy đủ.

Đã có đầu ra tại máy cho toàn bộ 12 mục guide_5: D01–D06 có số liệu/hình, D07–D11 có source/data documentation, kiểm tra nhất quán và repository public, D12 là bản bàn giao này. D01/D02/D04 đã khớp đủ 906 IS và 641 OOS return; điều kiện chia sẻ nguồn VN30TRI còn chờ xác nhận. Các con số C1/B1/B2 và A/B đã nghiệm thu giữ nguyên. Code release v0.2.0 bổ sung pipeline benchmark, coverage và hướng dẫn tái lập. Báo cáo benchmark đầy đủ dùng trong gói bàn giao riêng; raw/chuỗi ngày không được public. Đây là hồ sơ sẵn sàng nộp giảng viên, không phải xác nhận manuscript đã được nhóm tác giả duyệt.

## 1. Trạng thái D01–D12

{status}

## 2. D03 — Các drawdown sâu nhất

{drawdowns}

Toàn bộ 294 episodes có trong results/derived/drawdown_episodes.csv. Bảng trên chọn episode sâu nhất trong từng cặp phase/nhánh. Phiên dưới đỉnh đếm đến hồi phục hoặc ngày cuối phase, loại phiên hồi phục. Một episode nông hơn có thể kéo dài hơn episode sâu nhất. Những đợt cuối kỳ chưa hồi phục được ghi right-censored.

OOS C1 và B1 có đáy sâu nhất tại 23/03/2026 sau đỉnh 24/02/2026, còn ở dưới đỉnh khi chốt mẫu 29/04/2026. B2 có MDD OOS tại 09/04/2025 sau đỉnh 01/04/2025, hồi phục 26/05/2025. IS của B2 có episode từ 06/04/2022 chưa hồi phục ở cuối IS. Diễn giải gắn với từng cửa sổ riêng đã chuẩn hóa anchor.

Có thể chèn bảng các episode sâu nhất vào phần Results hoặc phụ lục. Đồ thị underwater giúp trình bày độ sâu và thời gian nắm giữ dưới đỉnh.

## 3. D05 — Đóng góp vào tăng NAV theo lớp tài sản

Đơn vị là điểm phần trăm của NAV đầu kỳ. Với NAV đầu kỳ 1, ba phần cộng lại bằng 100×(NAV cuối−1).

{attribution}

Đóng góp mỗi lớp tài sản trong interval là c_class,t = tổng w_held,i,t × r_i,t. Đóng góp wealth cả kỳ là tổng NAV_(t−1) × c_class,t. Đây là phép phân rã theo đường NAV đã thực hiện. Cột tổng của OOS là 71,64% cho C1, 71,04% cho B1 và 82,44% cho B2, khác đơn vị CAGR năm. Sum simple daily contributions được giữ ở cột riêng trong CSV.

Đối chiếu daily contributions với gross return cho sai số lớn nhất 3,02e−16. Tổng linked wealth contributions khớp NAV cuối với sai số tối đa 6,27e−14. Daily held weights được dùng đúng đầu return. Dữ liệu giá gốc chỉ tham gia extraction tại máy, không nằm trong repository public.

Đoạn tiếng Anh có thể dùng trong Results, sau khi tác giả rà soát số làm tròn

> We decompose gross portfolio returns using the weights held at the start of each valuation interval. Daily class contributions are linked using prior portfolio wealth, so their phase totals reconcile with the change in NAV. In the observed OOS period, the C1 equity, GOLD and VFF components contribute 45.67, 19.62 and 6.35 percentage points of initial wealth. The corresponding B1 contributions are 46.90, 17.80 and 6.34 points, and B2 contributions are 56.60, 18.06 and 7.78 points.

## 4. D06 — Hình đưa vào manuscript

Ba tên file đang được guide ghi nhận đã có trong figures/, mỗi hình có PNG 300 dpi, PDF và SVG.

- C1_OOS_wealth dùng 641 gross return với anchor 29/09/2023.
- C1_class_weights dùng tỷ trọng đang nắm giữ tại đầu return cho cả ba nhánh.
- C1_cost_sensitivity dùng lưới phí giả định 0/10/25/50 bps cho mỗi phía mua hoặc bán.
- portfolio_underwater trình bày drawdown IS/OOS với anchor riêng.

Mapping chi tiết nằm trong docs/results_guide.md. paper_5.tex và project_5.md chưa được cung cấp trong thư mục làm việc này, nên bản bàn giao đưa ra vị trí chèn và filenames để nhóm viết paper tích hợp.

## 5. D01/D02 và D04 — Benchmark total return và trạng thái thị trường

{benchmark}

## 6. D08/D09 — Source khoa học và phân biệt phiên bản

code/frozen_baseline chứa các module gốc cho selector, features, labels, ensemble, views, BL, optimizer và accounting/timing. code/frozen_experiments/run.py là runner A/B trong layout gốc. code/accounting.py sao nguyên byte helper gốc. code/fixed_rule.py trích nguyên hàm chia tỷ trọng C1 và import numpy.

code/reproduce.py là entry point tái tạo bảng/hình cho người đọc từ outputs đã phát hành. Nó tính lại 24 dòng metrics C1/B1/B2 và 128 dòng A/B/chi phí, annual turnover từ event ledger, episodes và class linking. Source-map chỉ rõ source/hash gốc so với source được tổ chức để công bố. Tài liệu methodology mô tả 8 features, label 5 phiên, training cutoff/purge/scaler, seeds 42–46, ánh xạ annual views sang daily Q, Omega và matched controls của B1/B2.

## 7. D10/D12 — Release và citation

Tác giả đã xác nhận tên **Nguyen Phuc Khang**, citation **Khang, Nguyen Phuc**, và chọn **MIT** cho mã nguồn do nhóm sở hữu ngày 18/11/2026. Repository public: https://github.com/khangng2611/vietnam-portfolio-research. Phiên bản code để cite là v0.2.0. Release công khai không chứa chuỗi, bảng số hoặc hình VN30TRI mới; các đầu ra này được bàn giao riêng cùng giới hạn quyền chia sẻ. Các tag trước được giữ nguyên. Trạng thái phát hành được ghi trong docs/release_review.md; CITATION.cff ghi metadata trích dẫn.

Đường dẫn phiên bản: https://github.com/khangng2611/vietnam-portfolio-research/releases/tag/v0.2.0

> Khang, Nguyen Phuc (2026). Vietnam Long-Only Multi-Asset Portfolio — Research Code and Derived Results (Version 0.2.0) [Software]. GitHub.

Đề xuất Data/Code Availability:

> The versioned research repository contains the portfolio methodology, original scientific source snapshots, dated strategy outputs, and scripts for regenerating the reported tables and figures. Vendor price histories and restricted historical records require access through their respective providers. The release documents which analyses can be reproduced from the shared outputs and which require authorized source data.

NOTICE.md phân biệt license phần mềm với quyền dữ liệu. Dữ liệu giá gốc và fitted objects không nằm trong repository. Chưa có DOI được cấp. Tag local v0.1.0-rc1 ban đầu được giữ nguyên. D01/D02/D04 đã tính riêng tại máy; xem hồ sơ bổ sung và điều kiện chia sẻ nguồn.

## 8. Đối chiếu và giới hạn

24 metrics C1/B1/B2 cùng 128 metrics A/B được tính lại từ dated returns và event trades, dung sai 1e−10. 9 tests nhỏ kiểm tra drawdown/recovery/anchor, wealth linking, index interval alignment, parser và nhánh nhạy cảm ba phiên. Sáu cặp phase/strategy của phần benchmark khớp NAV/CAGR/vol/Sharpe/MDD đã nghiệm thu. Replay/QA chạy từ một output folder ngoài repository. Source-map ghi 41 file khoa học gốc được sao/trích có hash.

Hồ sơ C cũ có câu ghi 48 dòng metrics trong khi CSV có 24. Package hiện tại ghi và kiểm tra đúng 24 dòng. Đây là sửa mô tả đóng gói. Các con số NAV/CAGR/Sharpe/MDD/TO được nghiệm thu vẫn khớp. Những scripts cũ cần workstation paths/inputs không được dùng làm entry point public.

Universe 30 mã cố định, publication/revision vintages chưa đầy đủ, GOLD/VFF là proxy định giá và phí là kịch bản giả định. Holdout đã được quan sát trong dự án. Những kết quả này mô tả cách một kiến trúc chọn đại diện và phân bổ vốn hoạt động trên mẫu hiện tại. Diễn giải cho paper cần giữ phạm vi đó cùng khoảng bất định đã báo cáo.

## 9. Kết luận bàn giao và những bước sau khi nộp

Đã có đầu ra cho toàn bộ D01–D12, theo đúng phạm vi công bố: số liệu đầy đủ trong gói nộp, code và các outputs được phép trong repository, dữ liệu nguồn/chuỗi ngày benchmark giữ riêng. Xem [phương án bàn giao](submission_decisions_vi.md) và [mapping kết quả](results_guide.md). Không còn yêu cầu tính toán đang chờ; không cần retrain, retune hoặc thêm chiến lược.

Chốt cách trình bày: bảng gross 0 bps làm đối chiếu chính, giữ đầy đủ lưới phí giả định 0/10/25/50 bps. Chuỗi benchmark nguồn làm kết quả chính, nhánh tái tạo ba phiên chỉ làm sensitivity. D04 giữ quy tắc drawdown ≤−10% đã định, ex-post, peak liên tục. Đây là phương án đề xuất cho nhóm tác giả duyệt, không phải quyết định đã được giảng viên chấp thuận.

| Bước sau bàn giao | Tình trạng |
| --- | --- |
| Duyệt diễn giải | Báo cáo và các đoạn Results/Data Availability đã soạn; giảng viên/nhóm tác giả duyệt trước dùng trong paper. |
| Tích hợp manuscript gốc | Chưa có paper_5.tex; đã chuẩn bị đoạn LaTeX và hình/tables trong gói nộp để chèn vào Results, Data, Discussion và phụ lục. Không khẳng định đã sửa manuscript thật. |
| Mở thêm dữ liệu benchmark | Chưa có xác nhận quyền tái phân phối. Tiếp tục giữ riêng; nếu muốn public chuỗi/bảng/hình, xác nhận với chủ nguồn trước. Giới hạn này đã được công khai trong hướng dẫn reproducibility. |
| DOI | Chưa có, là tùy chọn; sử dụng URL phiên bản GitHub thay vì điền DOI chưa được cấp. |

[Điều khoản sử dụng Dragon Capital](https://www.dragoncapital.com.vn/terms), đọc ngày 18/11/2026, không được coi là giấy phép dữ liệu mở. Việc ghi nhận điều kiện nguồn và giữ dữ liệu riêng đáp ứng phương án code-and-results repository của guide_5; không thể thay cho xác nhận riêng từ chủ dữ liệu nếu cần mở dataset.

Gói nộp gồm báo cáo Word/PDF/Markdown, bảng tổng hợp, hình và đoạn LaTeX, cùng bảng tiến độ và manifest kiểm tra. File vendor gốc và chuỗi VN30TRI hằng ngày không được đính kèm. Người đọc có quyền truy cập phù hợp có thể tái chạy bằng pipeline đã công bố.
'''
    (ROOT / 'docs/paper_handoff_vi.md').write_text(text)
    for source in (derived / 'figures').iterdir():
        if source.suffix in ['.png', '.pdf', '.svg']:
            import shutil
            shutil.copy2(source, ROOT / 'figures' / source.name)
    print('Wrote Vietnamese handoff and finalized figure exports')


if __name__ == '__main__':
    main()
