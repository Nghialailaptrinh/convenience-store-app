# Convenience Store — Clean Architecture

Bản Python theo cấu trúc [Jason Taylor CleanArchitecture](https://github.com/jasontaylordev/CleanArchitecture),
thay nghiệp vụ Todo bằng **Products, Carts, Orders**. Web demo dùng SQLite và payment giả lập.

## Kiến trúc

```text
Web → Application → Domain
Infrastructure → Application (interfaces) + Domain (mapping)
```

Application khong phu thuoc truc tiep vao mot repository implementation. Handler nhan
`IApplicationDbContext`; context contract nay gom cac port `IProductRepository`,
`ICartRepository` va `IOrderRepository` cung `save_changes()`. Infrastructure trien khai
contract do bang `ApplicationDbContext`; cac adapter trong `infrastructure/repositories/`
chi la implementation detail duoc context tao va quan ly.

Day la adaptation theo Python, khong phai ban sao EF Core:

```text
Handler
    |
    v
IApplicationDbContext
    |
    v
ApplicationDbContext
    |
    +--> IProductRepository  -> SqlAlchemyProductRepository -> SQLAlchemy
    +--> ICartRepository     -> SqlAlchemyCartRepository    -> SQLAlchemy
    `--> IOrderRepository    -> SqlAlchemyOrderRepository   -> SQLAlchemy
```

Handler khong import `IProductRepository`, `ICartRepository` hay `IOrderRepository`.
Chung chi xuat hien trong contract cua context va lop adapter Infrastructure, gan voi
vai tro `DbSet`/query access trong ban .NET.

| Layer | Vai trò |
| --- | --- |
| **Domain** | Entity, value object, quy tắc nghiệp vụ; không phụ thuộc ORM/framework. |
| **Application** | Command/query, handler, validator, DTO và interfaces. |
| **Infrastructure** | Database context, cấu hình entity, repository và payment adapter. |
| **Web** | Endpoint, HTTP request/response và composition root; không chứa business logic. |

## Cấu trúc

```text
src/
├── domain/          # common, entities, enums, events, exceptions, value_objects
├── application/
│   ├── common/      # behaviours, exceptions, interfaces, models, security
│   ├── products/queries/get_products/
│   │   ├── get_products.py
│   │   └── product_dto.py
│   ├── carts/       # commands, queries
│   ├── orders/commands/create_order/
│   │   ├── create_order.py
│   │   └── create_order_command_validator.py
│   └── dependency_injection.py
├── infrastructure/
│   ├── data/        # application_db_context.py, application_db_context_initialiser.py
│   │   └── configurations/  # product/cart/order_configuration.py
│   ├── identity/, repositories/, payment/
│   └── dependency_injection.py
└── web/             # endpoints, infrastructure, services, wwwroot
    ├── appsettings.json
    ├── dependency_injection.py
    └── program.py
tests/               # domain_unit_tests, application_unit_tests,
                     # application_functional_tests, infrastructure_integration_tests,
                     # web_acceptance_tests, architecture
```

Mỗi slice đặt **tên file trùng use case**, chứa request bất biến và handler riêng.
Handler nhận `IApplicationDbContext` qua constructor, xử lý bằng `handle(request)`;
endpoint gọi `sender.send(...)`. Validator chạy trước handler; query trả DTO.
[Bảng đối chiếu file với mẫu](docs/template_structure.md).

## Chạy demo

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e ".[dev]"
.\.venv\Scripts\python.exe -m uvicorn web.program:app --host 127.0.0.1 --port 8000
```

Mở **<http://127.0.0.1:8000>**; API docs: `/docs`. Dữ liệu lưu ở `shop.db`.
Tạo đơn chờ để thử hủy; checkout mô phỏng thanh toán, không thu tiền thật.
Demo chưa có đăng nhập, payment thật hoặc migrations; các phần Identity/auditing/events vẫn là khung mở rộng.

Kiểm tra: `.\.venv\Scripts\python.exe -m pytest -q`.
