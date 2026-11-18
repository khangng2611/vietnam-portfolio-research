# Yêu cầu dữ liệu để hoàn tất D01, D02 và D04

Cập nhật 18/11/2026. Chưa nhận được chuỗi daily VN30TRI đủ điều kiện để chạy các phân tích. Đã chạy thử Vnstock mới nhất, ngoài kiểm tra chức năng xuất TradingView và các nguồn trước đó.

## Kiểm tra Vnstock mới nhất

Đã cài và chạy Vnstock 6.0.1 cùng vnstock-oapi 0.1.2 trong môi trường tạm riêng. Bản 4.0.4 trong môi trường nghiên cứu được giữ nguyên. Đã gọi lịch sử ngày của đúng mã VN30TRI từ 14/01/2020 đến 29/04/2026 qua cả bốn nguồn hỗ trợ index OHLCV theo tài liệu hiện hành:

| Nguồn | Kết quả chạy thực tế |
| --- | --- |
| DNSE | Thiếu DNSE_API_KEY và DNSE_API_SECRET |
| FHSC | Thiếu FHSC_API_KEY |
| SSI | Thiếu SSI_API_KEY và SSI_API_SECRET |
| TCBS | Thiếu TCBS_API_KEY |

Cả bốn trả CredentialError, mã VNSTOCK_CREDENTIAL_MISSING, trước khi lấy dữ liệu; tổng cộng tải được 0 dòng. Vì vậy chưa xác minh được vendor nào có đúng VN30TRI, mức độ phủ lịch sử hoặc quyền nghiên cứu. Không thể kết luận VN30TRI được hoặc không được hỗ trợ chỉ từ lỗi thiếu khóa. [Nhật ký máy đọc được](../reproducibility/vn30tri_acquisition_20261118.json), [tài liệu lịch sử chỉ số](https://vnstocks.com/docs/vnstock/v6/thi-truong-market).

Thế hệ 6 yêu cầu khóa Open API do người dùng đăng ký tại nguồn. Nếu đã có tài khoản được phép truy cập, cấu hình khóa ngay trên máy bằng `vnstock keys set <nguồn>` trong môi trường Vnstock 6 và mở phiên theo yêu cầu của nguồn. Không gửi API secret hoặc OTP qua chat. Sau khi có quyền truy cập vẫn cần xác nhận đúng series, kiểm tra coverage và điều kiện sử dụng trước khi chạy benchmark. Ngoài quyền của nguồn, lớp chuẩn hóa vnstock 6 thuộc bản Mở rộng; cần xác nhận quyền phần mềm nếu tiếp tục dùng lớp này. [Giới thiệu thế hệ 6](https://vnstocks.com/docs/vnstock/v6/gioi-thieu).

Một bản export được phép sử dụng vẫn đủ để hoàn tất công việc, không bắt buộc phải dùng API. D01, D02 và D04 chưa có kết quả VN30TRI thực nghiệm; các kết quả danh mục hiện có được giữ nguyên.

## Kết quả kiểm tra truy cập

- TradingView có đúng HOSE:VN30TRI, tên VN30 Total Return Index. Đã mở biểu đồ 1D và thử Manage layouts → Download chart data → Download. Phiên hiện tại hiện thông báo nâng cấp gói để xuất dữ liệu. Không có CSV tải xuống. Danh tính công khai được xác nhận tại trang chỉ số. [VN30TRI](https://www.tradingview.com/symbols/HOSE-VN30TRI/).
- Hướng dẫn TradingView cho biết CSV xuất theo phần lịch sử đã nạp vào biểu đồ. Khi xuất qua một tài khoản được phép, cần nạp đủ lịch sử rồi kiểm tra ngày bắt đầu/kết thúc trong file. [Hướng dẫn xuất CSV](https://www.tradingview.com/support/solutions/43000537255-how-to-export-chart-data/).
- Truy vấn EODHD symbols/search với VN30TRI, type=index trả HTTP 200 và 0 kết quả. Chưa xác minh được một mã thay thế tại nhà cung cấp này. Request identity và tham số được ghi trong reproducibility/vn30tri_acquisition_20261112.json.
- FiinQuant có tài liệu lấy historical close theo ngày qua phiên đăng nhập. Chưa có tài khoản/entitlement được cung cấp cho tác vụ, và tài liệu tổng quát chưa xác nhận khả năng xuất đủ lịch sử đúng VN30TRI. Cần nhà cung cấp xác nhận coverage trước khi chọn gói truy cập. [Historical API](https://docs.fiinquant.vn/ham-va-cong-thuc/2.-du-lieu-giao-dich/2.2.-ham-du-lieu-lich-su.md).

## Bộ dữ liệu cần cung cấp

Một file CSV hoặc Excel xuất từ HOSE, vendor hoặc tài khoản được phép sử dụng, với mức đóng cửa hằng ngày của đúng VN30 Total Return Index.

| Nội dung | Yêu cầu |
| --- | --- |
| Series | HOSE VN30TRI, total-return, chỉ số cuối ngày |
| Khoảng ngày tối thiểu | 18/02/2020–29/04/2026, có ngày 29/09/2023 |
| Khoảng ngày nên xin nếu thuận tiện | 14/01/2020–29/04/2026 hoặc lịch sử đầy đủ |
| Trường bắt buộc trong file | ngày và mức chỉ số đóng cửa, tương ứng index_date/index_level |
| Các cột xuất phổ biến có thể xử lý | Date/Close hoặc time/close từ TradingView, giữ nguyên file gốc |
| Thông tin nguồn kèm theo | Nhà cung cấp, URL/màn hình xuất, mã và tên series, tần suất 1D, thời điểm xuất, phiên bản/vintage hoặc thông tin điều chỉnh lịch sử nếu có |
| Quyền sử dụng | Điều khoản hoặc xác nhận cho phép nghiên cứu và trình bày bảng/hình dẫn xuất trong luận văn/paper |
| Phân phối dữ liệu | Xác nhận riêng raw data có được chia sẻ công khai hay chỉ lưu private |

Để đủ cả hai phase, kỳ vọng 1548 mức chỉ số tại các session cần thiết, tạo 1547 return, gồm 906 IS và 641 OOS. Ngày29/09/2023 là điểm chung giữa hai phase. Không yêu cầu bên cung cấp điền thêm ngày cuối tuần/ngày nghỉ. Giữ các điểm thiếu nguyên trạng để kiểm tra coverage. Những trường vendor_record_date hoặc thông tin sửa đổi nên giữ lại nếu có, không tự gán ngày lịch sử chưa biết.

File raw có thể giữ trong thư mục private_inputs/ đã được Git ignore. Mật khẩu hoặc API secret không cần gửi trong chat. Một bản export từ người có quyền truy cập thường đã đủ để làm việc.

## Nội dung có thể gửi cho giảng viên, thư viện hoặc nhà cung cấp

Em đang hoàn thiện nghiên cứu danh mục đầu tư tại Việt Nam và cần lịch sử chỉ số HOSE VN30 Total Return Index, mã VN30TRI, theo ngày từ 18/02/2020 đến 29/04/2026, tốt hơn nếu có từ 14/01/2020. Em cần ngày và mức đóng cửa của chỉ số tổng thu nhập, bao gồm ngày 29/09/2023.

Nhờ Thầy/Cô hoặc bộ phận dữ liệu cho biết trường/đơn vị có thể hỗ trợ xuất đúng series này không, hoặc có kênh truy cập học thuật phù hợp nào. Em cũng cần thông tin nguồn, thời điểm xuất và điều kiện sử dụng cho luận văn/paper, đặc biệt quyền công bố bảng/hình phân tích dẫn xuất. Dữ liệu raw có thể giữ private theo điều khoản nhà cung cấp. Nếu nguồn chỉ có một phần lịch sử, nhờ cung cấp khoảng thời gian sẵn có để em kiểm tra mẫu chung.

Kênh hỗ trợ chính thức của FiinQuant được liệt kê trên trang liên hệ để xác nhận series/coverage và quyền truy cập trước khi đăng ký. [Liên hệ FiinQuant](https://docs.fiinquant.vn/thong-tin-lien-he.md).

## Khi nhận được file

Kiểm tra identifier, tần suất, ngày, trùng/mất phiên, mức chỉ số và điều khoản sử dụng. Chuẩn hóa hai trường dữ liệu rồi dùng code/benchmark.py với một thư mục output mới. Pipeline xử lý 906/641 return riêng, tính lại metric trên cùng mẫu nếu thiếu lịch sử và xuất D04 khi đủ cả hai phase. Chưa có kết quả thực nghiệm VN30TRI được tạo trong lần kiểm tra này.
