# Đăng ký API để kiểm tra VN30TRI

Cập nhật sau kiểm tra: đã tìm được chuỗi VN30TR Index miễn phí trên website Dragon Capital, không cần bốn API key bên dưới, và hoàn tất tính toán tại máy. Xem [kết quả và giới hạn nguồn](VN30TRI_completion_20261118_vi.md). Các hướng dẫn dưới đây vẫn mô tả những lựa chọn nguồn khác, chưa xác nhận coverage của từng nguồn.

Kiểm tra ngày 18/11/2026. Chưa xác nhận được nguồn nào trong DNSE, FHSC, SSI và TCBS cung cấp **đúng VN30TRI hằng ngày, đủ 18/02/2020–29/04/2026** qua quyền miễn phí. Các lần chạy Vnstock 6.0.1 hiện bị chặn vì thiếu khóa trước khi nhận dữ liệu. Xem reproducibility/vn30tri_acquisition_20261118.json.

## Nguồn nên thử trước

Nếu đã có tài khoản tại một nguồn, ưu tiên nguồn đó. Nếu chưa có, **TCBS là lựa chọn thử đầu tiên xét riêng tiêu chí đăng ký API miễn phí**, vì tài liệu iFlash xác nhận miễn phí. Đây chưa phải xác nhận có VN30TRI. Nên hỏi hỗ trợ về series/coverage trước khi mở thêm tài khoản hoặc mua gói. [Workflow TCBS](https://developers.tcbs.com.vn/docs/v1.0.0/workflow/).

| Nguồn | Bằng chứng đã xác minh | Đúng VN30TRI, đủ 2020–2026? | Phí |
| --- | --- | --- | --- |
| TCBS | bars-long-term nhận type=index, khung D/W/M | Chưa xác nhận | Đăng ký iFlash miễn phí; chưa xác nhận riêng entitlement VN30TRI |
| FHSC/Finhay | Có catalog chỉ số và lịch sử 1D theo mã | Catalog thực tế cần API key | Chưa xác minh cam kết miễn phí cho nhu cầu này |
| SSI | Có indexList và OHLCV daily; mô tả daily từ khi mã bắt đầu giao dịch | Chưa xác nhận VN30TRI trong catalog và độ phủ | Cần SSI xác nhận |
| DNSE | price/ohlc hỗ trợ nhóm chỉ số | Chưa xác nhận mã và độ phủ | Chưa xác nhận riêng daily VN30TRI miễn phí |

API chỉ số tổng quát hoặc VN30 price index không xác nhận quyền lấy VN30TRI total-return.

## TCBS

1. Đăng nhập TCInvest bằng tài khoản TCBS của bạn. Nếu chưa có, bạn tự hoàn tất quy trình mở tài khoản/xác thực tại đơn vị.
2. Mở [iFlash Open API](https://tcinvest.tcbs.com.vn/iflash-open-api), hoặc **Tiện ích → iFlash Open API**.
3. Tự đọc điều khoản hiện hành và đăng ký API; lưu API Key trên máy.
4. Dùng API Key cùng iOTP để cấp token. Theo tài liệu, token có hiệu lực tối đa 8 giờ; cần mở lại khi hết phiên.
5. Kiểm tra đúng mã VN30TRI qua lịch sử index, identity và coverage trước khi đưa vào luận văn.

[Workflow/đăng ký miễn phí](https://developers.tcbs.com.vn/docs/v1.0.0/workflow/), [lịch sử dài hạn](https://developers.tcbs.com.vn/docs/v1.0.0/stock/bars-long-term/).

## FHSC/Finhay

1. Đăng nhập [Finhay Invest](https://invest.fhsc.com.vn/), mở [Quản lý API](https://invest.fhsc.com.vn/quan-ly-api) và tạo khóa theo quy trình hiện hành.
2. Dữ liệu thị trường Tier 1 chỉ cần API key qua header X-FH-APIKEY; không cần secret của nhóm tài khoản/giao dịch Tier 2.
3. Kiểm tra `GET /market/quotes/indices` tìm VN30TRI hoặc alias được nhà cung cấp xác nhận. Nếu có, kiểm tra `/market/quotes/indices/{symbol}/history` với resolution=1D và khoảng thời gian yêu cầu.

[Quickstart](https://developers.fhsc.com.vn/quickstart), [catalog chỉ số](https://developers.fhsc.com.vn/api-reference/bang-gia-thi-truong/danh-muc-chi-so), [lịch sử chỉ số](https://developers.fhsc.com.vn/api-reference/bang-gia-thi-truong/lich-su-gia-chi-so). Tài liệu Finhay dùng tên FINHAY_API_KEY; Vnstock dùng FHSC_API_KEY hoặc keyring cho cùng khóa nguồn. Giá/phạm vi truy cập cần xác nhận tại nguồn.

## SSI

1. Có tài khoản chứng khoán SSI rồi đăng ký FastConnect theo [quy trình chính thức](https://developers.ssi.com.vn/docs/getting-started/registration). Hướng dẫn hiện yêu cầu liên hệ SSI để kích hoạt dịch vụ và tự hoàn tất hợp đồng/OTP.
2. Khi được duyệt, đăng nhập Developer Portal → **Bảng điều khiển → Quản lý API Key → Tạo Key mới**. Lưu API Key và API Secret.
3. Kiểm tra [indexList](https://developers.ssi.com.vn/docs/api-reference/data-indexList), sau đó [OHLCV daily](https://developers.ssi.com.vn/docs/api-reference/data-ohlc) của đúng mã. Daily từ khi mã bắt đầu giao dịch không bảo đảm mọi chỉ số đều có từ 2020.

[Cách lấy khóa](https://developers.ssi.com.vn/docs/getting-started/api-keys). Phí và quyền xuất lịch sử VN30TRI cần SSI xác nhận.

## DNSE

1. Đăng nhập hoặc tự mở tài khoản tại [Entrade X](https://entradex.dnse.com.vn/).
2. Chọn họ tên → **Thông tin tài khoản → Lightspeed API**; tự đăng ký và xác thực OTP theo hướng dẫn.
3. Lưu API Key và API Secret; theo tài liệu secret chỉ hiển thị một lần sau khi đăng ký.
4. Kiểm tra đúng mã VN30TRI qua price/ohlc và độ phủ lịch sử.

[Đăng ký](https://developers.dnse.com.vn/docs/guide/intro/register_guide/), [lịch sử OHLC](https://developers.dnse.com.vn/docs/dnse/get-ohlc-history/). Miễn phí giao dịch hoặc Ami X không đủ để kết luận daily VN30TRI qua API là miễn phí.

## Phần mềm và cấu hình trên máy

`vnstock-oapi` là connector Cộng đồng có thể dùng độc lập cho học tập/nghiên cứu trong phạm vi giấy phép phần mềm; lớp chuẩn hóa `vnstock` thế hệ 6 thuộc bản Mở rộng. Có thể dùng connector hoặc API chính thức trực tiếp để ưu tiên miễn phí. Quyền của nguồn dữ liệu là điều kiện riêng. [Phạm vi và liên kết nguồn](https://vnstocks.com/docs/vnstock-oapi/gioi-thieu).

Sau khi có khóa, dùng `vnstock-oapi keys set tcbs` trong môi trường đã cài connector; thay tcbs bằng fhsc, ssi hoặc dnse tương ứng. Công cụ hỏi khóa trên máy, không cần truyền trong câu lệnh. Sau khi cấu hình chỉ cần báo nguồn đã sẵn sàng; không gửi khóa, secret hoặc OTP qua chat/GitHub. Khi mở phiên, bạn tự nhập OTP nếu nguồn yêu cầu.

## Câu hỏi gửi hỗ trợ trước khi đăng ký

> Tôi cần HOSE VN30 Total Return Index, mã VN30TRI, mức đóng cửa hằng ngày từ 18/02/2020 đến 29/04/2026, gồm 29/09/2023, phục vụ luận văn. Open API của quý đơn vị có đúng series này không, mã truy vấn là gì, lịch sử bắt đầu ngày nào và tài khoản miễn phí có xuất đủ khoảng này không? Tôi có được công bố bảng/hình thống kê dẫn xuất trong luận văn/paper, giữ dữ liệu gốc private, không?

Phí đăng ký API không quyết định quyền công bố dữ liệu. Cần xác nhận phạm vi nghiên cứu và quyền chia sẻ kết quả riêng. Chưa gửi tin nhắn hoặc đăng ký tài khoản thay người dùng. Khi có file hợp lệ, code/benchmark.py kiểm tra 1548 mức tại các phiên yêu cầu, tạo 906 IS và 641 OOS return, rồi tính D01/D02/D04 theo quy tắc đã khóa.
