"""Write a local Vietnamese report from the completed, private benchmark evaluation."""
import argparse
import hashlib
import json
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
import pandas as pd

from run_dragon_benchmark import ROOT
from reproduce import save_figure
from write_handoff import markdown


def performance_table(frame):
    names = {'VN30TRI_reported': 'VN30TRI — Dragon Capital'}
    return markdown(['Nhánh', 'N', 'NAV', 'CAGR %', 'Vol %', 'Sharpe', 'MDD %'],
                    [[names.get(r.strategy, r.strategy), r.N, f'{r.final_nav:.4f}',
                      f'{100*r.ann_return:.2f}', f'{100*r.ann_volatility:.2f}',
                      f'{r.sharpe:.3f}', f'{100*r.max_drawdown:.2f}'] for r in frame.itertuples()])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run', type=Path, required=True)
    parser.add_argument('--source-dir', type=Path, required=True)
    args = parser.parse_args()
    run, source = args.run.resolve(), args.source_dir.resolve()
    manifest = json.loads((run / 'manifest.json').read_text())
    if manifest['status'] != 'completed' or manifest['scope'] != 'PRIVATE_RESEARCH_ANALYSIS':
        raise ValueError('Requires a completed private analysis')
    metrics = pd.read_csv(run / 'reported/metrics.csv')
    alternative = pd.read_csv(run / 'three_day_sensitivity/metrics.csv')
    states = pd.read_csv(run / 'reported/market_states.csv', parse_dates=['date'])
    other_states = pd.read_csv(run / 'three_day_sensitivity/market_states.csv', parse_dates=['date'])
    pd.testing.assert_series_equal(states.date, other_states.date)
    changed = int(states.market_state.ne(other_states.market_state).sum())
    summary = pd.read_csv(run / 'reported/market_state_summary.csv')
    other_summary = pd.read_csv(run / 'three_day_sensitivity/market_state_summary.csv')
    if changed == 0:
        pd.testing.assert_frame_equal(summary, other_summary)
    sensitivity = pd.read_csv(run / 'three_session_sensitivity.csv')
    left = metrics[metrics.strategy.str.startswith('VN30TRI_')].set_index('phase')
    right = alternative[alternative.strategy.str.startswith('VN30TRI_')].set_index('phase')
    effects = pd.DataFrame([{'phase': phase, 'metric': metric, 'reported': left.loc[phase, metric],
                             'sensitivity': right.loc[phase, metric],
                             'difference': right.loc[phase, metric] - left.loc[phase, metric]}
                            for phase in left.index for metric in
                            ['final_nav', 'ann_return', 'ann_volatility', 'sharpe', 'max_drawdown']])
    effects.to_csv(run / 'sensitivity_effects.csv', index=False)
    fig, ax = plt.subplots(figsize=(10, 3.5))
    ax.plot(states.date, states.market_drawdown, color='#244D70', linewidth=1)
    ax.fill_between(states.date, states.market_drawdown, -.1,
                    where=states.market_drawdown.le(-.1), color='#C45C4C', alpha=.25,
                    label='Market drawdown at least 10% (ex-post)')
    ax.axhline(-.1, color='#666666', linestyle='--', linewidth=.8)
    ax.axvline(pd.Timestamp('2023-09-29'), color='#777777', linestyle=':', linewidth=1, label='IS/OOS boundary')
    ax.yaxis.set_major_formatter(PercentFormatter(1))
    ax.set(title='VN30TRI drawdown — continuous peak across IS/OOS', ylabel='Drawdown')
    ax.legend(loc='lower left', fontsize=8)
    save_figure(fig, run, 'D04_market_drawdown_timeline')
    state_tables = {}
    for phase in ['IS', 'OOS']:
        part = summary[summary.phase.eq(phase)]
        state_tables[phase] = markdown(
            ['Trạng thái', 'Nhánh', 'N', 'Mean/ngày %', 'Phiên âm %', 'Ngày xấu nhất %', 'Vol năm %', 'Lãi kép tập con %'],
            [['DD ≥ 10%' if r.market_state == 'MARKET_DRAWDOWN_10' else 'Còn lại', r.strategy, r.N,
              f'{100*r.mean_daily_return:.4f}', f'{100*r.fraction_negative:.2f}', f'{100*r.worst_day:.2f}',
              f'{100*r.annualized_volatility:.2f}', f'{100*r.compounded_subset_return:.2f}'] for r in part.itertuples()])
    audit_table = markdown(['Ngày', 'Mức nguồn', 'Mức nhánh nhạy cảm'],
                           [[r.date, f'{r.reported_level:.2f}', f'{r.sensitivity_level:.2f}']
                            for r in sensitivity.itertuples()])
    report = f'''# D01, D02 và D04 — VN30 total-return benchmark

Ngày 18/11/2026. Đã hoàn tất tính toán trên máy cho cả hai phase. Kết quả chính dùng chuỗi VN30TR Index do Dragon Capital công bố; một nhánh riêng tái tạo ba phiên có dấu hiệu giữ nguyên mức để kiểm tra độ nhạy. C1/B1/B2 được tái tính trên cùng ngày và khớp toàn bộ kết quả gross đã nghiệm thu.

## 1. Nguồn và thay đổi hướng thực hiện

Trong khi tìm lịch sử thành phần/tỷ trọng VN30, đã tải báo cáo VFMVN30 bán niên 2020 và trích bảng 30 mã tại 30/06/2020. Các tỷ trọng in trong bảng cộng thành 102,38%, vượt sai số làm tròn thông thường; bảng này không được chuẩn hóa cưỡng bức hoặc dùng làm đầu vào chỉ số. Một ảnh chụp cũng chưa thiết lập lịch sử đầy đủ.

Đồng thời tìm được chuỗi tham chiếu trên [trang quỹ Dragon Capital](https://www.dragoncapital.com.vn/institution/vi/product/a0eJ2000001X9zhIAC/vn30). Dữ liệu website tách VN30 Index, VN30TR Index và NAV quỹ. Request chọn benchmarkFundReportCode=VN30TR Index; lấy fundBenchmarkData.navPrice, không lấy fundData của ETF.

Mức VN30TRI mới nhất ngày 18/11/2026 của Dragon Capital là 2225,72, khớp mức trên [TradingView HOSE:VN30TRI](https://www.tradingview.com/symbols/HOSE-VN30TRI/) tại lần kiểm tra. Đây là đối chiếu danh tính/một điểm quan sát, không chứng nhận mọi mức lịch sử.

Nguồn cung cấp 1576 mức có giá trị từ 02/01/2020 đến 29/04/2026. Các hàng trống trên lịch hợp nhất của quỹ/chỉ số được bỏ khỏi chuỗi nguồn, không forward-fill. Mức neo 18/02/2020: 950,50; 29/09/2023: 1346,62; mức cuối 29/04/2026: 2442,52. Dữ liệu được lấy miễn phí qua chức năng công khai, không cần API key hoặc tài khoản trả phí.

## 2. Coverage và quy ước

| Phase | Anchor | Return đầu | Return cuối | N yêu cầu | N khớp |
| --- | --- | --- | --- | --- | --- |
| IS | 18/02/2020 | 19/02/2020 | 29/09/2023 | 906 | 906 |
| OOS | 29/09/2023 | 02/10/2023 | 29/04/2026 | 641 | 641 |

Hai phase dùng anchor riêng. Mỗi return yêu cầu hai đầu ngày khớp đúng interval của portfolio. Không có phiên thiếu hoặc extra-index interval trong hai mẫu này. CAGR/vol/Sharpe dùng 252 phiên/năm, risk-free ngày 1,06^(1/252)−1 và std(ddof=1). MDD bao gồm NAV anchor=1. Index turnover và chi phí giao dịch của người nắm giữ index là N/A; các danh mục ở đây là gross, 0 bps.

## 3. D02 — IS

{performance_table(metrics[metrics.phase.eq('IS')])}

Trong IS, ba danh mục có CAGR/Sharpe cao hơn và MDD ít âm hơn benchmark quan sát. Đây là mô tả giai đoạn phát triển, không phải bằng chứng tổng quát hoặc một holdout mới.

![IS](reported/VN30TRI_reported_context_IS.png)

## 4. D01 — OOS

{performance_table(metrics[metrics.phase.eq('OOS')])}

VN30TRI có CAGR khoảng 26,38%. C1 và B1 thấp hơn về CAGR, nhưng có volatility/MDD thấp hơn và Sharpe cao hơn trên mẫu này. B2 có CAGR khoảng 26,66%, cao hơn benchmark khoảng 0,29 điểm phần trăm, đồng thời có volatility/MDD thấp hơn và Sharpe cao hơn. Đây chưa phải kiểm định chênh lệch có ý nghĩa thống kê. Benchmark là 100% cổ phiếu lớn; C1/B1/B2 có GOLD/VFF và các ràng buộc khác, nên diễn giải là market context.

![OOS](reported/VN30TRI_reported_context_OOS.png)

## 5. Kiểm tra ba phiên và nhánh tái tạo

Nguồn giữ mức 1552,85 ở 05–07/05/2025 trong khi VN30 price index biến động. Bảng chính giữ nguyên các mức nguồn. Nhánh nhạy cảm dùng hệ số TRI/price ở 29/04/2025 và giả định dividend yield bằng 0 trong khoảng này. Đối chiếu với mức nguồn 08/05/2025 có sai lệch 0,00935 điểm, nằm trong ngưỡng kiểm tra 0,02 điểm đã đặt trước khi tính metrics. Điều này hỗ trợ giả định để kiểm tra độ nhạy; chưa phải xác minh chính thức cổ tức/nguyên nhân thiếu cập nhật.

{audit_table}

Nhánh nhạy cảm giữ nguyên terminal NAV, CAGR và MDD. Sharpe OOS của benchmark thay từ {left.loc['OOS', 'sharpe']:.6f} thành {right.loc['OOS', 'sharpe']:.6f}; volatility từ {100*left.loc['OOS', 'ann_volatility']:.4f}% thành {100*right.loc['OOS', 'ann_volatility']:.4f}%. Có {changed} ngày đổi nhãn thị trường; bảng D04 của ba danh mục giữ nguyên. Không chọn nhánh theo kết quả có lợi cho mô hình.

So sánh TRI/price còn ghi nhận một số ngày price index giữa VCI và Dragon Capital không trùng nhau. Chúng được giữ trong quality_flags.csv tại thư mục nguồn để thẩm định tiếp; không tự sửa TRI bằng một nguồn price khác. Snapshot nguồn là dữ liệu truy xuất hồi cứu ngày 18/11/2026, chưa xác minh đầy đủ lịch sử revisions.

## 6. D04 — Danh mục trong trạng thái thị trường dưới đỉnh ít nhất 10%

Nhãn MARKET_DRAWDOWN_10 khi VN30TRI / running peak − 1 ≤ −10%. Running peak liên tục từ 18/02/2020 qua ranh giới IS/OOS. Đây là nhãn ex-post tại close, không phải tín hiệu giao dịch hoặc định nghĩa mọi phiên giảm giá.

### IS

{state_tables['IS']}

### OOS

{state_tables['OOS']}

IS có 420 phiên DD ≥ 10% và 486 phiên còn lại; OOS có 366 và 275 phiên. Trong nhóm OOS DD ≥ 10%, mean daily return lần lượt xấp xỉ 0,0058% (C1), 0,0057% (B1), 0,0362% (B2). Nhóm này bao gồm cả phiên hồi phục khi thị trường vẫn dưới đỉnh; không suy ra mô hình dự báo hoặc né tránh được thị trường giảm.

Lãi kép tập con nhân các return của những ngày được gán nhãn; tập ngày có thể không liên tục, không phải lợi nhuận của một chiến lược giao dịch thực thi. Hai mức lãi kép ở hai nhóm cũng không cộng trực tiếp thành lợi nhuận toàn phase.

![Nhãn thị trường](D04_market_drawdown_timeline.png)

## 7. Bằng chứng và tái lập

- reported/metrics.csv: 8 dòng D01/D02; reported/coverage.csv: 2 dòng coverage.
- reported/market_states.csv và market_state_summary.csv: nhãn ngày và 12 dòng D04.
- three_day_sensitivity/: cùng bộ kết quả cho nhánh tái tạo ba phiên; three_session_sensitivity.csv ghi từng mức thay thế.
- sensitivity_effects.csv: hiệu ứng trên 5 metrics của index, riêng IS/OOS.
- manifest.json và source_snapshots/: input/code hashes, môi trường, phương án định trước và kết quả kiểm tra. 9 unit tests đã qua; NAV/CAGR/vol/Sharpe/MDD của cả 6 cặp phase/danh mục khớp kết quả đã nghiệm thu, dung sai 1e−10.

Script: reproducibility/run_dragon_benchmark.py; dùng --source-dir trỏ tới thư mục nguồn đã lưu request/response, --output trỏ tới một thư mục private mới. Việc parse/evaluate dùng cùng accounting và interval-alignment với code/benchmark.py. Không refit XGBoost hoặc tối ưu lại danh mục.

## 8. Phạm vi sử dụng

Đây là kết quả tính toán nghiên cứu riêng theo yêu cầu của tác giả. Dữ liệu gốc và artifacts nằm trong thư mục Git ignore. Chưa có văn bản cấp phép tái phân phối dữ liệu Dragon Capital hoặc một xác nhận rằng chính sách bảo mật của website là giấy phép dữ liệu. Không gán research_use_permitted=true hoặc quyền chia sẻ mới để đi qua điều kiện của CLI công bố. Trước khi đưa raw data, chuỗi ngày, hình hoặc gói kết quả lên kho công khai, cần xác nhận điều kiện nguồn phù hợp. Kết quả ở đây không phải toàn bộ VN30TRI được tái dựng từ rổ cố định; nó dùng chuỗi nhà cung cấp cùng một nhánh nhạy cảm ba phiên được ghi rõ.
'''
    (run / 'report_vi.md').write_text(report)
    checks = {'market_state_label_changes': changed, 'full_sample_coverage': manifest['coverage'],
              'unit_tests_passed': 9, 'portfolio_metric_cross_checks': 6,
              'primary_series': 'Dragon Capital VN30TR Index as reported',
              'source_notes': 'Provider snapshot; three flat sessions retained in primary case',
              'scope': 'Private research; public redistribution rights unconfirmed'}
    (run / 'completion_checks.json').write_text(json.dumps(checks, indent=2) + '\n')
    artifacts = [p for p in run.rglob('*') if p.is_file() and p.name != 'postprocessing_manifest.json']
    post = {'generator_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'artifacts': {str(p.relative_to(run)): hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(artifacts)}}
    (run / 'postprocessing_manifest.json').write_text(json.dumps(post, indent=2) + '\n')
    print(run / 'report_vi.md')


if __name__ == '__main__':
    main()
