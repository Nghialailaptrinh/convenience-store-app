# Convenience Store — Clean Architecture

Demo cấu trúc **Python** theo [Jason Taylor CleanArchitecture](https://github.com/jasontaylordev/CleanArchitecture).
Mục tiêu là minh họa tổ chức code; nghiệp vụ, lưu dữ liệu và thanh toán vẫn là TODO.

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

Khi triển khai DI, host là nơi ghép Application với Infrastructure; nghiệp vụ không phụ thuộc cách ghép này.

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
    ├── endpoints/, infrastructure/, services/, schemas/
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

Đây là bản mô phỏng cấu trúc, không phải bản port toàn bộ template .NET.
`dependency_injection.py`, behaviours, identity và event handlers hiện chỉ là vị trí dự kiến;
không cần chạy server hay database để xem demo.
