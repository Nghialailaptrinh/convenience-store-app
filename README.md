# Convenience Store — Clean Architecture

Demo cấu trúc **Python** theo [Jason Taylor CleanArchitecture](https://github.com/jasontaylordev/CleanArchitecture).
Bản demo chạy được: 10 use case, web mua sắm tiếng Việt, SQLite và thanh toán giả lập.

## Chạy demo

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e ".[dev]"
.\.venv\Scripts\python.exe -m uvicorn web.main:app --host 127.0.0.1 --port 8000
```

Mở **http://127.0.0.1:8000**; API docs tại `/docs`.
SQLite tự tạo `shop.db` và thêm 9 sản phẩm mẫu khi khởi động, giữ dữ liệu khi chạy lại.

- Thêm/sửa/xóa sản phẩm trong giỏ → **Tạo đơn chờ thanh toán** → có thể hủy.
- **Thanh toán demo** tạo đơn đã thanh toán, không thu tiền thật; không hỗ trợ hủy/hoàn tiền đơn này.
- Giỏ được xóa khi tạo đơn thành công; payment thất bại sẽ rollback, giữ nguyên giỏ.
- Demo chưa có đăng nhập: customer ID và danh sách mã đơn được giữ trên trình duyệt.

## Kiến trúc

```text
Web → Application → Domain
Infrastructure → Application (interfaces) và Domain (mapping)
```

| Layer | Trách nhiệm |
| --- | --- |
| **Domain** | Entity, value object và quy tắc nghiệp vụ; không phụ thuộc ORM/framework. |
| **Application** | Điều phối use case. Command thay đổi dữ liệu, Query chỉ đọc; phụ thuộc các interface. |
| **Infrastructure** | Triển khai database, repository, payment và dịch vụ ngoài. |
| **Web** | Nhận request, gọi Application, trả response; không chứa business logic. |

`web/main.py` là composition root ghép các layer; handler nhận repository qua Unit of Work.
Mỗi command commit một transaction; query không ghi dữ liệu.

## Cấu trúc theo mẫu

```text
src/
├── domain/
│   ├── entities/             # Product, Category, Customer, Cart, CartItem, Order, OrderItem
│   ├── value_objects/        # Money
│   ├── enums/                # OrderStatus
│   └── common/, constants/, events/, exceptions/
├── application/
│   ├── common/               # interfaces, behaviours, exceptions, models, security
│   ├── products/queries/     # get_products, get_product_by_id
│   ├── cart/
│   │   ├── commands/         # add_product_to_cart, remove_product_from_cart, update_cart_item_quantity
│   │   └── queries/          # get_cart
│   ├── orders/
│   │   ├── commands/         # checkout, create_order, cancel_order
│   │   ├── queries/          # get_order
│   │   └── event_handlers/
│   └── dependency_injection.py
├── infrastructure/
│   ├── data/                 # connection, models, configurations, interceptors
│   ├── identity/, repositories/, payment/
│   └── dependency_injection.py
└── web/
    ├── endpoints/, infrastructure/, services/, schemas/, static/
    ├── dependency_injection.py
    └── main.py
tests/                        # domain_unit, application_unit, application_functional,
                              # infrastructure_integration, web_acceptance, architecture
```

Mỗi use case là một **vertical slice**, ví dụ:
`application/cart/commands/add_product_to_cart/command.py` chứa command và handler;
validator hoặc DTO riêng sẽ đặt cùng slice. Các thư mục chưa dùng có placeholder giải thích vai trò.

## So với mẫu Jason Taylor

| Mẫu gốc | Bản Python này |
| --- | --- |
| `Application/Feature/Commands hoặc Queries/UseCase` | Cùng cách phân nhóm, dùng tên `snake_case`. |
| `Application/Common`, `Infrastructure/Data`, `Web/Endpoints` | Giữ cách tổ chức tương ứng. |
| `IApplicationDbContext` và EF Core | Giữ repository interfaces theo yêu cầu cửa hàng; SQLAlchemy nằm ở Infrastructure. |
| Các project test riêng theo layer | Các thư mục test tương ứng trong Python. |

Giữ cấu trúc mẫu, dùng repository + SQLAlchemy và JSON cho các dòng giỏ/đơn để hạ tầng demo gọn.
Behaviours, identity và event handlers vẫn là placeholder. Payment thật, đăng nhập và migrations
chưa triển khai; bản demo chỉ chạy local. SQLite tuần tự hóa transaction để tránh checkout trùng.

Kiểm tra: `.\.venv\Scripts\python.exe -m pytest -q` và
`.\.venv\Scripts\python.exe -m ruff check src tests`.
