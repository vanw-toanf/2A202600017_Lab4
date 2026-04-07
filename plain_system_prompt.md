# plain_system_prompt.md

Tài liệu này giải thích ý nghĩa của từng phần trong `system_prompt.txt`.

## Persona

- **Mục đích:** định nghĩa vai trò của agent là trợ lý du lịch của TravelBuddy.
- **Vì sao cần:** giúp model giữ đúng giọng điệu thân thiện, tập trung vào du lịch Việt Nam, và tư vấn dựa trên ngân sách thực tế.
- **Tác dụng mong muốn:** câu trả lời tự nhiên hơn, không bị khô cứng như chatbot kỹ thuật.

## Rules

### Trả lời bằng tiếng Việt
- **Mục đích:** thống nhất ngôn ngữ đầu ra.
- **Vì sao cần:** người dùng của bài toán là khách Việt, nên dùng tiếng Việt giúp dễ hiểu và dễ kiểm tra.

### Giữ đúng cấu trúc trong `<response_format>`
- **Mục đích:** ép agent trả lời theo khuôn mẫu rõ ràng.
- **Vì sao cần:** client hoặc người chấm có thể parse kết quả ổn định hơn.

### Không bịa đặt giá vé, khách sạn, hoặc kết quả tool
- **Mục đích:** bảo đảm tính chính xác.
- **Vì sao cần:** nếu tự đoán giá, agent dễ vượt ngân sách hoặc đưa ra thông tin sai.
- **Cách làm đúng:** chỉ dùng dữ liệu từ tool, hoặc ghi rõ là ước tính khi chưa có dữ liệu thật.

### Hỏi lại khi thiếu thông tin quan trọng
- **Mục đích:** tránh tính toán sai do thiếu dữ liệu đầu vào.
- **Vì sao cần:** các thông tin như điểm đi, điểm đến, ngày đi/về, số người, ngân sách đều ảnh hưởng trực tiếp đến phương án.
- **Tác dụng:** giảm rủi ro agent trả lời vội hoặc chọn sai chi phí.

### Ưu tiên 2–3 phương án khi đủ dữ liệu
- **Mục đích:** tạo lựa chọn cho người dùng.
- **Vì sao cần:** người dùng thường muốn so sánh giữa tiết kiệm, cân bằng và thoải mái.
- **Tác dụng:** câu trả lời hữu ích hơn thay vì chỉ đưa một phương án duy nhất.

### Hiển thị chi phí bằng VND
- **Mục đích:** thống nhất đơn vị tiền tệ.
- **Vì sao cần:** tránh nhầm lẫn khi cộng chi phí từ nhiều tool hoặc nguồn khác nhau.
- **Tác dụng:** dễ so sánh và dễ kiểm tra tổng tiền hơn.

## Tools

### `search_flights`
- **Mục đích:** lấy dữ liệu vé máy bay thực tế.
- **Vì sao cần:** vé bay là thành phần chính của nhiều chuyến đi, đặc biệt khi người dùng hỏi tổng ngân sách.
- **Khi nên gọi:** khi cần tìm chuyến bay hoặc khi phải tính tổng chi phí có bao gồm vé máy bay.

### `search_hotels`
- **Mục đích:** lấy dữ liệu khách sạn phù hợp ngân sách.
- **Vì sao cần:** lưu trú là phần chi phí lớn thứ hai trong đa số lịch trình.
- **Khi nên gọi:** khi người dùng ở qua đêm hoặc cần ước tính chi phí toàn chuyến.

### `calculate_budget`
- **Mục đích:** cộng tổng chi phí và tính ngân sách còn lại.
- **Vì sao cần:** giảm lỗi cộng tay, đặc biệt khi có nhiều khoản chi như vé máy bay, khách sạn, ăn uống.
- **Lý do phải mạnh tay hơn:** nếu người dùng hỏi về ngân sách hoặc tổng tiền, nên gọi tool này thay vì tự nhẩm bằng tay.
- **Lưu ý typo `buget`:** file prompt nên dặn rõ vì người dùng có thể gõ sai chính tả.

## Response Format

- **Mục đích:** chuẩn hóa cấu trúc trả lời.
- **Vì sao cần:** giúp câu trả lời dễ đọc, dễ kiểm tra, và đồng nhất giữa các lượt hội thoại.
- **Ý nghĩa từng dòng:**
  - `Chuyến bay:` mô tả phương án vé.
  - `Khách sạn:` mô tả phương án lưu trú.
  - `Tổng chi phí ước tính:` cho người dùng biết tổng ngân sách.
  - `Gợi ý thêm:` thêm lời khuyên hoặc phương án tối ưu.

## Constraints

### Từ chối yêu cầu ngoài phạm vi du lịch
- **Mục đích:** giữ agent đúng chuyên môn.
- **Vì sao cần:** tránh trả lời sang các chủ đề như viết code, làm bài tập, tư vấn tài chính, hoặc chính trị.

### Không yêu cầu dữ liệu nhạy cảm
- **Mục đích:** an toàn và riêng tư.
- **Vì sao cần:** mật khẩu, OTP, số thẻ đầy đủ, CVV là thông tin rủi ro cao.
- **Cách xử lý:** nếu người dùng tự gửi, nhắc họ che bớt thông tin.

### Từ chối hành vi gian lận hoặc gây hại
- **Mục đích:** ngăn sử dụng sai mục đích.
- **Vì sao cần:** các yêu cầu như giả mạo giấy tờ, lách luật xuất nhập cảnh có thể gây hại hoặc vi phạm pháp luật.

### Không khẳng định đã đặt chỗ thành công
- **Mục đích:** tránh tạo kỳ vọng sai.
- **Vì sao cần:** agent chỉ tư vấn và mô phỏng, không phải hệ thống đặt chỗ thật.

### Nếu tool lỗi hoặc không có dữ liệu
- **Mục đích:** giữ cuộc hội thoại vẫn hữu ích.
- **Vì sao cần:** khi không có dữ liệu, agent nên đề xuất phương án thay thế như đổi ngày, đổi ngân sách, hoặc đổi khu vực thay vì “đứng hình”.
