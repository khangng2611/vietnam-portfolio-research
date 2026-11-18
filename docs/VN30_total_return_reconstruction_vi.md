# Khả năng tái tạo benchmark total return của VN30

Kiểm tra ngày 18/11/2026 theo đề xuất tự tính benchmark. Chưa tạo chuỗi chỉ số hoặc chạy D01/D02/D04. Chưa có bằng chứng chuỗi tự tính tương đương VN30TRI chính thức.

## Đầu vào đã thu thập

- VN30 price index qua VCI: 1576 mức trong khoảng 02/01/2020–29/04/2026 sau khi lọc ngày, lưu private từ lần kiểm tra Quote.
- VCI corporate events: truy vấn thành công eventCode=DIV cho cả 30 mã trong rổ nghiên cứu hiện có, khoảng nguồn 20200101–20260429. Mỗi phản hồi chỉ có một trang. Thu được 134 sự kiện tiền mặt có ex-date trong khoảng, có số tiền/cổ phiếu và ngày không hưởng quyền.
- Các sự kiện ACB có trường valuePerShare=1000 VND và ex-date rõ ràng. Sự kiện 31/05/2024 khớp mẫu thông báo chính thức đã lưu ở Step 1. Chưa xác minh độc lập đầy đủ mọi sự kiện hoặc ngữ nghĩa bộ lọc ngày của nhà cung cấp.

Raw responses, manifest từng request và cash_dividend_candidates.csv được giữ trong private_inputs/vn30-reconstruction-20261118T111855Z/. Tóm tắt số lượng, kiểm tra thiếu/trùng và hash nằm trong [hồ sơ khả thi](../reproducibility/vn30_reconstruction_feasibility_20261118.json). Dữ liệu này là đầu vào ứng viên, chưa phải lịch sử chỉ số được nghiệm thu.

Các file KBS sự kiện từng thu thập ở Step 1 phần lớn là phản hồi lỗi tham số s=500, vượt giới hạn 20. Không tính những file đó là các bảng corporate actions hợp lệ. Lần thử lại ACB với s=20, eID=2 trả mảng rỗng. Không dùng mảng rỗng làm bằng chứng rằng ACB không chia cổ tức.

## Đầu vào còn thiếu để tái tạo đúng đối tượng

1. Danh sách thành phần VN30 và ngày hiệu lực của mọi thay đổi trong giai đoạn nghiên cứu. Rổ 30 mã cố định của dự án không thiết lập được lịch sử này.
2. Tỷ trọng chỉ số theo lịch sử, hoặc đầy đủ số lượng cổ phiếu tính chỉ số, free-float/capping factors và điều chỉnh số chia để tái tạo tỷ trọng. Tổng hợp cổ tức của 30 mã với tỷ trọng tùy chọn không tái tạo VN30.
3. Giá và xử lý corporate actions nhất quán với phương pháp chỉ số. Giá điều chỉnh KBS hiện chưa được chứng nhận độc lập về xử lý cash dividend; tránh cộng cổ tức hai lần.
4. Quy tắc HOSE tương ứng từng thời kỳ và các mức VN30TRI chính thức trên mẫu chung để đối chiếu. Sự trùng khớp định nghĩa total return không tự xác lập sự trùng khớp chuỗi số liệu.

Tìm kiếm công khai có báo cáo ETF chứa danh mục/tỷ trọng ở một số ngày, ví dụ báo cáo bán niên VFMVN30 tại 30/06/2020. Một ảnh chụp theo kỳ chưa xác lập trọng số/ngày hiệu lực của toàn bộ lịch sử. Chưa nhập các tỷ trọng từ tài liệu này vào tính toán; lần trích PDF chưa hoàn tất. [Nguồn HOSE](https://staticfile.hsx.vn/Uploads/FinancialReport/578/20200811_20200811%20-%20E1VFVN30%20-%20Bao%20cao%20tong%20ket%20HD%20QLQ%20ban%20nien%202020.pdf).

## Cách trình bày khi có kết quả đủ kiểm tra

Có thể ghi ngắn ở phương pháp/phụ lục: “Benchmark total return của VN30 được tính theo quy tắc HOSE từ dữ liệu thành phần, tỷ trọng và cổ tức tiền mặt; nguồn dữ liệu và kiểm tra đối chiếu được cung cấp trong repository.” Chỉ dùng câu này sau khi các đầu vào và phép tính thực sự đáp ứng mô tả đó.

Nếu chỉ dùng rổ cố định, giả định tỷ trọng hoặc cổ tức ước lượng, tên và phương pháp phải thể hiện đây là proxy cho đối tượng tương ứng. Khi chưa đối chiếu, không gán chuỗi thành VN30TRI chính thức hoặc mô tả sai nguồn. Điều này ảnh hưởng cả kết quả benchmark lẫn nhãn thị trường giảm D04.

Các kết quả C1/B1/B2, báo cáo đã công bố và release v0.1.1 được giữ nguyên trong lần kiểm tra khả thi này. D01/D02 và D04 tiếp tục chờ đầu vào đáp ứng yêu cầu. Chưa upload dữ liệu của nhà cung cấp hoặc cấp quyền chia sẻ mới cho dữ liệu này.
