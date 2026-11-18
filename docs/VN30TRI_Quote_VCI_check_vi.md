# Kiểm tra script Quote/VCI cho VN30TRI

Ngày 18/11/2026. Đã chạy mẫu người dùng cung cấp trên Vnstock 4.0.4 đang cài trong môi trường nghiên cứu. Không thay đổi package, source khoa học hoặc kết quả đã phát hành.

Yêu cầu: `Quote(symbol=..., source="VCI").history(start="2020-01-01", end="2026-04-29", interval="1d")`. Ngày kết thúc giữ ở mốc đóng mẫu luận văn, không lấy đến ngày hiện tại rồi trộn với mẫu đã khóa.

| Kiểm tra thực tế | Kết quả |
| --- | --- |
| Quote với VN30 | Thành công: trả 1653 dòng OHLCV đến 29/04/2026, không trùng timestamp |
| VN30 sau khi lọc đúng khoảng yêu cầu | 1576 dòng, từ 02/01/2020 đến 29/04/2026 |
| Quote với VN30TRI | ValueError trong nhận diện mã, trước khi gọi lịch sử |
| Danh mục index tĩnh của adapter VCI 4.0.4 | Có VN30, không có VN30TRI |
| POST trực tiếp cùng endpoint VCI với symbols=[VN30TRI] | HTTP 200, response `[]`, 0 dòng |

Lỗi Quote cụ thể là `Invalid derivative or bond symbol...`: parser không nhận VN30TRI là chỉ số và đi vào nhánh kiểm tra mã 7 ký tự. Đây là lỗi nhận diện của bản thư viện, không mô tả bản chất tài sản VN30TRI.

Để kiểm tra riêng phía nguồn, đã gửi một request thông thường tới endpoint mà adapter sử dụng: `https://trading.vietcap.com.vn/api/chart/OHLCChart/gap-chart`, với timeFrame=ONE_DAY, symbols=[VN30TRI], countBack=1800, to=1777507200 (30/04/2026 00:00 UTC). Server trả danh sách rỗng. Không sửa mapping, ép VN30 thành VN30TRI hoặc thay đổi cơ chế xác thực. Kết quả chỉ áp dụng cho mã và endpoint đã truy vấn; chưa xác minh alias khác hay một dịch vụ dữ liệu khác của Vietcap.

VN30 trong script là price index. D01/D02 yêu cầu đúng chỉ số tổng thu nhập VN30TRI; vì vậy dữ liệu control VN30 không được đưa vào benchmark này. Đáng chú ý, API qua thư viện trả 77 dòng sớm hơn ngày bắt đầu yêu cầu; mọi dữ liệu nhận được cần lọc và kiểm tra lịch thực tế trước khi sử dụng.

File VN30 control và phản hồi gốc được lưu trong private_inputs/ đã Git ignore. Script kiểm tra và hồ sơ từng lần gọi nằm trong reproducibility/artifacts/vci-quote-20261118T100717Z/; nhật ký tóm tắt máy đọc được ở [vn30tri_vci_quote_20261118.json](../reproducibility/vn30tri_vci_quote_20261118.json).

Chưa tải được mức VN30TRI nào, chưa chạy benchmark hoặc phân loại thị trường giảm. D01/D02 vẫn PENDING_SOURCE, D04 vẫn PENDING_D01_D02. Cần export đúng VN30TRI hoặc nguồn/API xác nhận đúng series, đủ lịch sử và điều kiện nghiên cứu.
