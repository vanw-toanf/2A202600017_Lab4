from langchain_core.tools import tool

#========================
#   MOCK DATA
#   Gia ca co logic (gia cuoi tuan dat hon, gia hang cao hon dat hon) 
#   Doc hieu data de debug test case
#========================
FLIGHTS_DB = {
    ("Hà Nội", "Đà Nẵng"): [
        {"airline": "Vietnam Airlines", "departure": "06:00", "arrival": "07:20", "price": 1_450_000, "class": "economy"},
        {"airline": "Vietnam Airlines", "departure": "14:00", "arrival": "15:20", "price": 2_800_000, "class": "business"},
        {"airline": "VietJet Air", "departure": "08:30", "arrival": "09:50", "price": 890_000, "class": "economy"},
        {"airline": "Bamboo Airways", "departure": "11:00", "arrival": "12:20", "price": 1_200_000, "class": "economy"},
    ],
    ("Hà Nội", "Phú Quốc"): [
        {"airline": "Vietnam Airlines", "departure": "07:00", "arrival": "09:15", "price": 2_100_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "10:00", "arrival": "12:15", "price": 1_350_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "16:00", "arrival": "18:15", "price": 1_100_000, "class": "economy"},
    ],
    ("Hà Nội", "Hồ Chí Minh"): [
        {"airline": "Vietnam Airlines", "departure": "06:00", "arrival": "08:10", "price": 1_600_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "07:30", "arrival": "09:40", "price": 950_000, "class": "economy"},
        {"airline": "Bamboo Airways", "departure": "12:00", "arrival": "14:10", "price": 1_300_000, "class": "economy"},
        {"airline": "Vietnam Airlines", "departure": "18:00", "arrival": "20:10", "price": 3_200_000, "class": "business"},
    ],
    ("Hồ Chí Minh", "Đà Nẵng"): [
        {"airline": "Vietnam Airlines", "departure": "09:00", "arrival": "10:20", "price": 1_300_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "13:00", "arrival": "14:20", "price": 780_000, "class": "economy"},
    ],
    ("Hồ Chí Minh", "Phú Quốc"): [
        {"airline": "Vietnam Airlines", "departure": "08:00", "arrival": "09:00", "price": 1_100_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "15:00", "arrival": "16:00", "price": 650_000, "class": "economy"},
    ],
}

HOTELS_DB = {
    "Đà Nẵng": [
        {"name": "Mường Thanh Luxury", "stars": 5, "price_per_night": 1_800_000, "area": "Mỹ Khê", "rating": 4.5},
        {"name": "Sala Danang Beach", "stars": 4, "price_per_night": 1_200_000, "area": "Mỹ Khê", "rating": 4.3},
        {"name": "Fivitel Danang", "stars": 3, "price_per_night": 650_000, "area": "Sơn Trà", "rating": 4.1},
        {"name": "Memory Hostel", "stars": 2, "price_per_night": 250_000, "area": "Hải Châu", "rating": 4.6},
        {"name": "Christina's Homestay", "stars": 2, "price_per_night": 350_000, "area": "An Thượng", "rating": 4.7},
    ],
    "Phú Quốc": [
        {"name": "Vinpearl Resort", "stars": 5, "price_per_night": 3_500_000, "area": "Bãi Dài", "rating": 4.4},
        {"name": "Sol by Meliá", "stars": 4, "price_per_night": 1_500_000, "area": "Bãi Trường", "rating": 4.2},
        {"name": "Lahana Resort", "stars": 3, "price_per_night": 800_000, "area": "Dương Đông", "rating": 4.0},
        {"name": "9Station Hostel", "stars": 2, "price_per_night": 200_000, "area": "Dương Đông", "rating": 4.5},
    ],
    "Hồ Chí Minh": [
        {"name": "Rex Hotel", "stars": 5, "price_per_night": 2_800_000, "area": "Quận 1", "rating": 4.3},
        {"name": "Liberty Central", "stars": 4, "price_per_night": 1_400_000, "area": "Quận 1", "rating": 4.1},
        {"name": "Cochin Zen Hotel", "stars": 3, "price_per_night": 550_000, "area": "Quận 3", "rating": 4.4},
        {"name": "The Common Room", "stars": 2, "price_per_night": 180_000, "area": "Quận 1", "rating": 4.6},
    ],
}



def _format_vnd(amount: int) -> str:
    return f"{amount:,}".replace(",", ".") + "đ"


def _find_city_key(city: str, available_keys: list[str]) -> str | None:
    city_normalized = city.strip().lower()
    for key in available_keys:
        if key.lower() == city_normalized:
            return key
    return None


@tool
def search_flights(origin: str, destination: str) -> str:
    """
    Tìm kiếm các chuyến bay giữa hai thành phố.
    Tham số:
    - origin: thành phố khởi hành (VD: 'Hà Nội', 'Hồ Chí Minh')
    - destination: thành phố đến (VD: 'Đà Nẵng', 'Phú Quốc')
    Trả về danh sách chuyến bay với hãng, giờ bay, giá vé.
    Nếu không tìm thấy chuyến bay, trả về thông báo không có chuyến.
    """
    origin_input = origin.strip()
    destination_input = destination.strip()

    if not origin_input or not destination_input:
        return "Thiếu thông tin điểm đi hoặc điểm đến. Vui lòng nhập đầy đủ."

    matched_origin = _find_city_key(origin_input, list({k[0] for k in FLIGHTS_DB.keys()}))
    matched_destination = _find_city_key(destination_input, list({k[1] for k in FLIGHTS_DB.keys()}))

    if not matched_origin:
        matched_origin = origin_input
    if not matched_destination:
        matched_destination = destination_input

    direct_key = (matched_origin, matched_destination)
    reverse_key = (matched_destination, matched_origin)

    direct_flights = FLIGHTS_DB.get(direct_key, [])
    if direct_flights:
        lines = [f"Các chuyến bay từ {matched_origin} đến {matched_destination}:"]
        sorted_flights = sorted(direct_flights, key=lambda item: item["price"])
        for index, flight in enumerate(sorted_flights, start=1):
            lines.append(
                f"{index}. {flight['airline']} | {flight['departure']} - {flight['arrival']} | "
                f"{flight['class']} | {_format_vnd(flight['price'])}"
            )
        return "\n".join(lines)

    reverse_flights = FLIGHTS_DB.get(reverse_key, [])
    if reverse_flights:
        lines = [
            f"Không tìm thấy chuyến bay từ {matched_origin} đến {matched_destination}.",
            f"Bạn có thể tham khảo chiều ngược lại ({matched_destination} → {matched_origin}):",
        ]
        sorted_flights = sorted(reverse_flights, key=lambda item: item["price"])
        for index, flight in enumerate(sorted_flights, start=1):
            lines.append(
                f"{index}. {flight['airline']} | {flight['departure']} - {flight['arrival']} | "
                f"{flight['class']} | {_format_vnd(flight['price'])}"
            )
        return "\n".join(lines)

    return f"Không tìm thấy chuyến bay từ {matched_origin} đến {matched_destination}."

@tool
def search_hotels(city: str, max_price_per_night: int = 99999999) -> str:
    """
    Tìm kiếm khách sạn tại một thành phố, có thể lọc theo giá tối đa mỗi đêm.
    Tham số:
    - city: tên thành phố (VD: 'Đà Nẵng', 'Phú Quốc', 'Hồ Chí Minh')
    - max_price_per_night: giá tối đa mỗi đêm (VNĐ), mặc định không giới hạn
    Trả về danh sách khách sạn phù hợp với tên, số sao, giá, khu vực, rating.
    """
    city_input = city.strip()
    if not city_input:
        return "Thiếu thông tin thành phố. Vui lòng nhập tên thành phố cần tìm khách sạn."

    if max_price_per_night <= 0:
        return "max_price_per_night phải lớn hơn 0."

    matched_city = _find_city_key(city_input, list(HOTELS_DB.keys()))
    if not matched_city:
        return f"Không tìm thấy dữ liệu khách sạn tại {city_input}."

    hotels = HOTELS_DB.get(matched_city, [])
    filtered_hotels = [
        hotel for hotel in hotels if hotel["price_per_night"] <= int(max_price_per_night)
    ]
    filtered_hotels.sort(key=lambda item: (-item["rating"], item["price_per_night"]))

    if not filtered_hotels:
        return (
            f"Không tìm thấy khách sạn tại {matched_city} với giá dưới "
            f"{_format_vnd(int(max_price_per_night))}/đêm. Hãy thử tăng ngân sách."
        )

    lines = [
        f"Khách sạn tại {matched_city} (<= {_format_vnd(int(max_price_per_night))}/đêm):"
    ]
    for index, hotel in enumerate(filtered_hotels, start=1):
        lines.append(
            f"{index}. {hotel['name']} | {hotel['stars']}⭐ | {hotel['area']} | "
            f"Rating {hotel['rating']} | {_format_vnd(hotel['price_per_night'])}/đêm"
        )
    return "\n".join(lines)

@tool
def calculate_budget(total_budget: int, expenses: str) -> str:
    """
    Tính toán ngân sách còn lại sau khi trừ các khoản chi phí.
    Tham số:
    - total_budget: tổng ngân sách ban đầu (VNĐ)
    - expenses: chuỗi mô tả các khoản chi, mỗi khoản cách nhau bởi dấu phẩy, 
      định dạng 'tên_khoản:số_tiền' (VD: 'vé_máy_bay:890000,khách_sạn:650000')
    Trả về bảng chi tiết các khoản chi và số tiền còn lại.
    Nếu vượt ngân sách, cảnh báo rõ ràng số tiền thiếu.
    """
    if total_budget < 0:
        return "Tổng ngân sách phải là số không âm."

    expenses_input = expenses.strip()
    if not expenses_input:
        return "Chuỗi expenses đang rỗng. Vui lòng nhập theo dạng 've_may_bay:890000,khach_san:650000'."

    parsed_expenses: dict[str, int] = {}
    items = [item.strip() for item in expenses_input.split(",") if item.strip()]

    if not items:
        return "Không đọc được khoản chi nào từ expenses."

    for item in items:
        if ":" not in item:
            return (
                "Định dạng expenses không hợp lệ. Mỗi khoản phải theo dạng "
                "'ten_khoan:so_tien' và cách nhau bằng dấu phẩy."
            )

        name_part, amount_part = item.split(":", 1)
        expense_name = name_part.strip()
        amount_text = amount_part.strip().replace("_", "")

        if not expense_name:
            return "Tên khoản chi không được để trống."

        if not amount_text.lstrip("-").isdigit():
            return f"Số tiền không hợp lệ ở khoản '{expense_name}': '{amount_part.strip()}'."

        expense_amount = int(amount_text)
        if expense_amount < 0:
            return f"Số tiền ở khoản '{expense_name}' không được âm."

        parsed_expenses[expense_name] = parsed_expenses.get(expense_name, 0) + expense_amount

    total_expense = sum(parsed_expenses.values())
    remaining_budget = total_budget - total_expense

    lines = ["Bảng chi phí:"]
    for expense_name, expense_amount in parsed_expenses.items():
        display_name = expense_name.replace("_", " ").strip().title()
        lines.append(f"- {display_name}: {_format_vnd(expense_amount)}")

    lines.extend(
        [
            "---",
            f"Tổng chi: {_format_vnd(total_expense)}",
            f"Ngân sách: {_format_vnd(total_budget)}",
            f"Còn lại: {_format_vnd(remaining_budget)}",
        ]
    )

    if remaining_budget < 0:
        lines.append(f"Vượt ngân sách {_format_vnd(abs(remaining_budget))}! Cần điều chỉnh.")

    return "\n".join(lines)
