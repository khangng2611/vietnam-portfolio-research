# Bàn giao nghiên cứu cho guide 5

Ngày 18/11/2026. Code release v0.2.0.

D01–D12 đã có đầu ra bàn giao. D01/D02 dùng chuỗi VN30TR Index do Dragon Capital công bố, đủ 906 IS và 641 OOS return, đúng hai anchor và lịch interval. D04 dùng peak liên tục, ngưỡng drawdown 10% cố định, có 12 dòng thống kê theo nhánh/phase/state. Một sensitivity riêng cho ba phiên đứng giá không làm đổi nhãn D04. Chuỗi nhà cung cấp và nhánh sensitivity được phân biệt rõ; không coi nhánh tái tạo là chỉ số chính thức.

Bản public này chứa phương pháp, code, kiểm tra và coverage. Bảng số, hình benchmark và báo cáo đầy đủ ở gói bàn giao riêng cho tác giả/giảng viên, không đính kèm trên GitHub vì chưa xác lập quyền phân phối lại. Không có file vendor gốc, daily index levels, index returns hoặc daily market-state sequence mới trong release này. Đây là giới hạn phạm vi công bố, không phải phân tích chưa chạy.

D03 có 294 drawdown episodes; D05 có daily class contributions và linked wealth reconciliation; D06 có các hình NAV, held weights, cost sensitivity và underwater từ outputs đã public. D07 có dictionary 32 series. D08/D09 mô tả selection, XGBoost → BL, training/label timing, constraints và accounting. D11 tái tạo 24 main và 128 A/B records. Chín unit tests kiểm tra các quy ước quan trọng. Không thay đổi các kết quả C1/B1/B2 đã nghiệm thu, không retrain/retune.

Giữ gross 0 bps làm đối chiếu chính và toàn bộ lưới phí giả định 0/10/25/50 bps cho mỗi phía. Không gọi phí giả định là phí giao dịch thực tế. Benchmark là market context của danh mục đa tài sản, không phải chứng minh superiority. Nhãn D04 là ex-post và có cả ngày hồi phục.

Repository: https://github.com/khangng2611/vietnam-portfolio-research

Version: https://github.com/khangng2611/vietnam-portfolio-research/releases/tag/v0.2.0

Citation: Khang, Nguyen Phuc (2026). Vietnam Long-Only Multi-Asset Portfolio — Research Code and Derived Results (Version 0.2.0) [Software]. GitHub.

MIT áp dụng cho mã gốc; không cấp quyền đối với dữ liệu bên thứ ba. Chưa có DOI. Gói nộp riêng có báo cáo Word/PDF/Markdown, bảng/hình và fragment LaTeX. Manuscript gốc paper_5.tex chưa được cung cấp, nên tích hợp cuối cùng và duyệt nội dung thuộc nhóm tác giả.

Xem [kết quả và hình đã public](results_guide.md), [phương án bàn giao](submission_decisions_vi.md), [reproducibility](reproducibility.md), và [nguồn/quyền dữ liệu](data_sharing_review.md).
