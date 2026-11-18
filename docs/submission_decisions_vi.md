# Phương án bàn giao guide 5

Ngày 18/11/2026. Tác giả: Nguyen Phuc Khang; citation: Khang, Nguyen Phuc.

Các lựa chọn dưới đây chốt cách đóng gói và trình bày hồ sơ, không thay đổi mô hình hoặc kết quả đã nghiệm thu. Giảng viên/nhóm tác giả vẫn là bên duyệt nội dung manuscript.

1. Dùng chuỗi VN30TR Index do Dragon Capital công bố làm benchmark chính. Giữ nguyên mức nguồn, hai anchor riêng cho bảng IS/OOS, không forward-fill. Nhánh tái tạo 05–07/05/2025 chỉ là sensitivity và được ghi rõ giả định không có dividend yield trong khoảng.
2. Dùng bảng gross 0 bps làm đối chiếu phương pháp chính; trình bày đầy đủ 0/10/25/50 bps mỗi phía mua/bán để thấy độ nhạy. Không gọi một mức phí giả định là phí thực tế tại Việt Nam. Không chọn phí theo chiến lược nào thắng.
3. D04 dùng drawdown VN30TRI ≤−10%, peak liên tục qua IS/OOS. Nhãn là ex-post; không kết luận khả năng dự báo hoặc bảo vệ nhân quả trong bear market.
4. Giữ nguyên các số C1/B1/B2, thiết kế selection và allocation, seeds, training và constraints. Không thêm backtest, ablation hoặc retune để cải thiện kết quả.
5. Hồ sơ nộp giảng viên chứa báo cáo đầy đủ, bảng tổng hợp, hình và đoạn LaTeX. Không gửi kèm file vendor gốc hoặc chuỗi mức/return VN30TRI hằng ngày. Hồ sơ này chưa phải quyền cho phép public lại dữ liệu.
6. Bản public mới chứa code, phương pháp, hồ sơ coverage và hướng dẫn lấy input hợp pháp. Các bảng/hình benchmark và toàn bộ báo cáo riêng ở gói bàn giao, chưa phân phối trên GitHub. Giữ nguyên các tag cũ; phiên bản code mới dùng v0.2.0, không cấp DOI chưa tồn tại.
7. Do chưa có paper_5.tex, cung cấp fragment LaTeX và bản preview tự chứa để nhóm tác giả tích hợp. Không khẳng định đã sửa hoặc biên dịch manuscript gốc.

## Nguồn và phạm vi quyền

[Trang quỹ Dragon Capital](https://www.dragoncapital.com.vn/institution/vi/product/a0eJ2000001X9zhIAC/vn30) xác định benchmark VN30 TRI. [Điều khoản sử dụng](https://www.dragoncapital.com.vn/terms), kiểm tra 18/11/2026, xác lập quyền sở hữu của DCVFM/các bên liên quan, nêu điều kiện đối với việc dùng thông tin cho mục đích thương mại và không bảo đảm tính đầy đủ/chính xác/kịp thời. Không tìm thấy trên trang này một giấy phép mở cho chuỗi chỉ số. Việc nguồn công khai không được mô tả là chứng cứ cấp quyền tái phân phối. Đây là ghi nhận nội dung nguồn, không phải xác nhận pháp lý của nhà cung cấp.

Phương án hiện tại là code-and-results repository với giới hạn truy cập được mô tả theo guide_5 mục 8.4 và 10. Người đọc tái tạo các bảng danh mục đã public từ outputs của release; phần benchmark cần có dữ liệu nguồn phù hợp. Chưa có văn bản xác nhận quyền phân phối lại raw hoặc chuỗi dẫn xuất. Nếu sau này cần mở các tệp này, nhóm tác giả xác nhận riêng với chủ nguồn; điều đó không được giả lập như một việc đã hoàn thành trong hồ sơ nộp.

## Những việc thuộc bước sau bàn giao

- Giảng viên/nhóm tác giả duyệt cách diễn giải và chèn nội dung vào manuscript thật.
- Trước khi mở dữ liệu/hình benchmark ngoài gói bàn giao, xác nhận điều kiện nguồn; nếu không có, tiếp tục giữ riêng và nêu giới hạn reproducibility.
- Archive DOI là tùy chọn. Permalink phiên bản GitHub được dùng khi chưa có DOI.

Không còn phép tính nào đang chờ trong phạm vi D01–D12. Việc công bố một bộ dữ liệu mở hoặc nộp paper thay nhóm tác giả không phải kết quả được khẳng định ở đây.
