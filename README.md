# Convenience Store API

Skeleton app mua hàng cho cửa hàng tiện lợi, dùng **Python 3.12+, FastAPI, SQLite và SQLAlchemy**.

## Kiến trúc phần mềm

Áp dụng **Clean Architecture**: dependency hướng vào trong, tách nghiệp vụ khỏi HTTP và database.

```text
Web/API ──────────> Application ──────────> Domain
                         ↑
                  Infrastructure
```

| Layer | Vai trò |
| --- | --- |
| **Domain** | Entity, value object và quy tắc nghiệp vụ cốt lõi. Không phụ thuộc framework, ORM hay layer khác. |
| **Application** | Điều phối use case qua Domain và các interface repository/payment. **Command** thay đổi dữ liệu; **Query** chỉ đọc. |
| **Infrastructure** | Triển khai interface của Application: database, repository, payment và dịch vụ ngoài. Mapping ORM sang Domain tại đây. |
| **Web/API** | Nhận HTTP request, gọi use case, trả response. Không chứa business logic. |

## Tổ chức code

```text
src/
├── domain/          # entities, value_objects, enums
├── application/     # products, cart, orders: mỗi use case một slice
│   └── interfaces/  # repository và payment contracts
├── infrastructure/  # database, repositories, payment
└── web/             # routes, schemas, main.py
tests/               # kiểm tra kiến trúc và API
```

**Domain:** Product, Category, Customer, Cart, CartItem, Order, OrderItem, Money, OrderStatus.

**Vertical slice:** mỗi use case có thư mục riêng, chứa command/query và hàm `handle`.
Ví dụ: `application/cart/add_product/command.py`.
Các use case bao gồm xem sản phẩm, quản lý giỏ hàng, checkout, tạo/xem/hủy đơn.

**Trạng thái:** mới là skeleton; business logic, persistence và payment chưa triển khai.
`GET /health` trả 200; 10 endpoint nghiệp vụ đã nối vào Application và trả 501.

## Chạy dự án

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e ".[dev]"
.\.venv\Scripts\python.exe -m uvicorn web.main:app --reload
```

Swagger: http://127.0.0.1:8000/docs

```powershell
.\.venv\Scripts\python.exe -m pytest
.\.venv\Scripts\python.exe -m ruff check src tests
```
