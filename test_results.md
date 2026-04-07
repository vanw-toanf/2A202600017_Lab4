# Test Results – TravelBuddy Agent

## Command

```bash
cp .env.example .env  # Thay keY OPENAI_API_KEY 
pip install -r requirements.txt
python agent/agent.py
```

## Tổng quan

- 5 phiên hội thoại mẫu.
- Agent gọi đúng tool trong các bài toán du lịch.
- Agent từ chối đúng yêu cầu ngoài phạm vi.

---

## Case 1 – Chào hỏi, thu thập nhu cầu

**Mục tiêu:** Kiểm tra phản hồi mở đầu và hỏi thêm thông tin.

```text
============================================================
TravelBuddy – Trợ lý Du lịch Thông minh
      Gõ 'quit' để thoát
============================================================

Bạn: xin chào, tôi đang muốn đi du lịch nhưng chưa biết đi đâu.

TravelBuddy đang suy nghĩ...
Trả lời trực tiếp

TravelBuddy: Chào bạn! Thật vui khi bạn muốn đi du lịch. Bạn có ý tưởng về địa điểm nào chưa? Hoặc bạn muốn mình gợi ý vài nơi đẹp ở Việt Nam? Bên cạnh đó, bạn có thể cho mình biết thêm về ngân sách, thời gian dự kiến đi và số người đi cùng để mình có thể tư vấn tốt hơn nhé!

Bạn: quit
```

---

## Case 2 – Tìm chuyến bay Hà Nội → Đà Nẵng

**Mục tiêu:** Kiểm tra gọi `search_flights` và trình bày kết quả.

```text
============================================================
TravelBuddy – Trợ lý Du lịch Thông minh
      Gõ 'quit' để thoát
============================================================

Bạn: Tìm giúp tôi chuyến bay từ Hà Nội đi Đà Nẵng.

TravelBuddy đang suy nghĩ...
Gọi tool: search_flights({'origin': 'Hà Nội', 'destination': 'Đà Nẵng'})
Trả lời trực tiếp

TravelBuddy: Dưới đây là các chuyến bay từ Hà Nội đi Đà Nẵng mà bạn có thể tham khảo:

1. **VietJet Air** | 08:30 - 09:50 | Economy | **890.000 VND**
2. **Bamboo Airways** | 11:00 - 12:20 | Economy | **1.200.000 VND**
3. **Vietnam Airlines** | 06:00 - 07:20 | Economy | **1.450.000 VND**
4. **Vietnam Airlines** | 14:00 - 15:20 | Business | **2.800.000 VND**

Bạn muốn đặt vé cho chuyến bay nào hoặc cần thêm thông tin gì không?

Bạn: quit
```

---

## Case 3 – Tư vấn trọn gói theo ngân sách

**Mục tiêu:** Kiểm tra gọi nhiều tool (`search_flights` + `search_hotels`) và tổng hợp phương án.

```text
============================================================
TravelBuddy – Trợ lý Du lịch Thông minh
      Gõ 'quit' để thoát
============================================================

Bạn: Tôi ở Hà Nội , muốn đi Phú Quốc 2 đêm, buget 5 triệu. Tư vấn giúp!

TravelBuddy đang suy nghĩ...
Gọi tool: search_flights({'origin': 'Hà Nội', 'destination': 'Phú Quốc'})
Gọi tool: search_hotels({'city': 'Phú Quốc', 'max_price_per_night': 2500000})
Trả lời trực tiếp

TravelBuddy: Dưới đây là phương án chuyến đi cho bạn từ Hà Nội đến Phú Quốc trong 2 đêm, với ngân sách 5 triệu:

**Chuyến bay:**
1. **VietJet Air** | 16:00 - 18:15 | economy | **1.100.000đ**
2. **VietJet Air** | 10:00 - 12:15 | economy | **1.350.000đ**
3. **Vietnam Airlines** | 07:00 - 09:15 | economy | **2.100.000đ**

**Khách sạn (cho 2 đêm):**
1. **9Station Hostel** | 2⭐ | Dương Đông | Rating 4.5 | **200.000đ/đêm** → Tổng 400.000đ cho 2 đêm.
2. **Sol by Meliá** | 4⭐ | Bãi Trường | Rating 4.2 | **1.500.000đ/đêm** → Tổng 3.000.000đ cho 2 đêm.
3. **Lahana Resort** | 3⭐ | Dương Đông | Rating 4.0 | **800.000đ/đêm** → Tổng 1.600.000đ cho 2 đêm.

**Tổng chi phí ước tính:**
- **Chọn chuyến bay VietJet Air (1.100.000đ):**
  - Vé máy bay: 1.100.000đ
  - Khách sạn 9Station Hostel: 400.000đ
  - **Tổng: 1.500.000đ**

- **Chọn chuyến bay VietJet Air (1.350.000đ):**
  - Vé máy bay: 1.350.000đ
  - Khách sạn 9Station Hostel: 400.000đ
  - **Tổng: 1.750.000đ**

- **Chọn chuyến bay Vietnam Airlines (2.100.000đ):**
  - Vé máy bay: 2.100.000đ
  - Khách sạn 9Station Hostel: 400.000đ
  - **Tổng: 2.500.000đ**

**Gợi ý thêm:**
Bạn có thể chọn chuyến bay với giá rẻ hơn và lưu trú tại khách sạn rẻ để tiết kiệm chi phí, hoặc nếu muốn thoải mái hơn, bạn có thể chọn các khách sạn 4⭐ như Sol by Meliá nhưng sẽ làm bạn vượt ngân sách. Hãy cho mình biết bạn thấy phương án nào phù hợp nhé!

Bạn: quit
```

---

## Case 4 – Thiếu thông tin đầu vào khách sạn

**Mục tiêu:** Kiểm tra agent hỏi bổ sung dữ kiện.

```text
============================================================
TravelBuddy – Trợ lý Du lịch Thông minh
      Gõ 'quit' để thoát
============================================================

Bạn: Tôi muốn đặt khách sạn

TravelBuddy đang suy nghĩ...
Trả lời trực tiếp

TravelBuddy: Bạn có thể cho mình biết thành phố bạn muốn đặt khách sạn là ở đâu và ngân sách tối đa mỗi đêm của bạn là bao nhiêu không?

Bạn: quit
```

---

## Case 5 – Từ chối yêu cầu ngoài phạm vi

**Mục tiêu:** Kiểm tra constraint từ chối bài tập không liên quan du lịch.

```text
============================================================
TravelBuddy – Trợ lý Du lịch Thông minh
      Gõ 'quit' để thoát
============================================================

Bạn: Giải giúp tôi bài tập Python về linked list.

TravelBuddy đang suy nghĩ...
Trả lời trực tiếp

TravelBuddy: Xin lỗi, mình không thể giúp bạn với bài tập Python về linked list. Tuy nhiên, nếu bạn cần tư vấn về du lịch, đặt vé máy bay hoặc khách sạn, hãy cho mình biết nhé!

Bạn: quit
```
