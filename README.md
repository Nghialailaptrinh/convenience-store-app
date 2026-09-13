# Convenience Store — Clean Architecture

Ứng dụng mô phỏng hệ thống mua hàng tại cửa hàng tiện lợi, được xây dựng nhằm học và thực hành **Clean Architecture**.

Kiến trúc project được tham khảo từ [Jason Taylor CleanArchitecture](https://github.com/jasontaylordev/CleanArchitecture) và điều chỉnh để phù hợp với Python.

Identity có đăng ký, đăng nhập cấp Bearer token và `/identity/me`, thử tại `/docs`.
Xem [hướng dẫn Bước 3](docs/identity_step_3.md). Cart/Order chưa kiểm tra quyền sở hữu.

Mục tiêu:

* Tách biệt business logic khỏi framework và database.
* Tổ chức hệ thống thành các layer có trách nhiệm rõ ràng.
* Áp dụng Dependency Inversion và Dependency Injection.
* Tổ chức use case theo Command / Query và Vertical Slice.
* Dễ dàng thêm tính năng, business rule hoặc thay đổi công nghệ.

---

# 1. Architecture

Project gồm bốn layer chính:

```text id="5m3j0j"
src/
├── domain/
├── application/
├── infrastructure/
└── web/
```

Dependency hướng vào trong:

```text id="48ejxe"
                 Domain
                   ↑
                   │
              Application
               ↑        ↑
               │        │
             Web   Infrastructure
```

Nguyên tắc:

```text id="hh05ll"
Domain
└── không phụ thuộc layer khác

Application
└── phụ thuộc Domain

Infrastructure
└── implement các abstraction của Application

Web
└── nhận request và gọi Application
```

---

# 2. Domain

```text id="v7gk5m"
src/domain/
```

Domain chứa các đối tượng và business rules cốt lõi.

```text id="z8cbqg"
domain/
├── common/
├── constants/
├── entities/
├── enums/
├── events/
├── exceptions/
└── value_objects/
```

Các domain object chính:

```text id="m8vm09"
Product
Category
Customer
Cart
CartItem
Order
OrderItem
Money
OrderStatus
```

### Entities

Các đối tượng có identity riêng:

```text id="s5h8oj"
Product
Cart
Order
```

Business rules liên quan trực tiếp đến trạng thái của Entity nên được đặt tại đây.

Ví dụ:

```text id="xctm49"
Order đã COMPLETED
→ không được cancel
```

### Value Objects

Các object được xác định bởi giá trị thay vì identity.

Ví dụ:

```text id="r3gk28"
Money(
    amount=10000,
    currency="VND"
)
```

### Enums

Biểu diễn các tập trạng thái cố định.

Ví dụ:

```text id="k8x4n1"
OrderStatus

PENDING
PAID
COMPLETED
CANCELLED
```

### Events

Biểu diễn các sự kiện có ý nghĩa trong Domain.

Ví dụ:

```text id="u0sqgj"
OrderCreated
OrderCancelled
```

Domain không phụ thuộc vào Web, database hoặc framework.

---

# 3. Application

```text id="sk80s3"
src/application/
```

Application chứa các **use case** của hệ thống.

Ví dụ:

```text id="8vd7ku"
GetProducts
GetProductById

AddProductToCart
RemoveProductFromCart
UpdateCartItemQuantity
GetCart

Checkout
CreateOrder
GetOrder
CancelOrder
```

Application được tổ chức theo feature và Vertical Slice:

```text id="5q7z3g"
application/
├── common/
│   ├── behaviours/
│   ├── exceptions/
│   ├── interfaces/
│   ├── models/
│   └── security/
│
├── products/
│   └── queries/
│
├── cart/
│   ├── commands/
│   └── queries/
│
├── orders/
│   ├── commands/
│   ├── queries/
│   └── event_handlers/
│
└── dependency_injection.py
```

---

# 4. Command / Query

Use case được chia thành hai loại chính:

```text id="68a1sk"
Command
→ thay đổi trạng thái hệ thống

Query
→ đọc dữ liệu
```

Ví dụ Command:

```text id="rvxsb8"
AddProductToCart
RemoveProductFromCart
UpdateCartItemQuantity
CreateOrder
CancelOrder
```

Ví dụ Query:

```text id="gytsr7"
GetProducts
GetProductById
GetCart
GetOrder
```

Mỗi use case có thể chứa:

```text id="6oj2vb"
Command / Query
Handler
Validator
DTO / Result
```

---

# 5. Handler

Handler thực hiện và điều phối một use case.

Flow cơ bản:

```text id="9u5gnx"
LOAD
 ↓
EXECUTE DOMAIN
 ↓
SAVE
```

Ví dụ:

```text id="5xsv58"
AddProductToCartHandler

Load Product
     ↓
Load Cart
     ↓
cart.add_product(...)
     ↓
Save changes
```

Handler điều phối workflow.

Business rules cốt lõi được giữ trong Domain.

---

# 6. Application Interfaces

Các abstraction mà Application cần được định nghĩa tại:

```text id="iwhd32"
application/common/interfaces/
```

Ví dụ:

```text id="6kptkg"
IApplicationDbContext
IPaymentGateway
ICurrentUser
```

Application chỉ phụ thuộc vào abstraction:

```text id="uh0ewj"
Handler
   ↓
IApplicationDbContext
```

Implementation cụ thể nằm bên ngoài Application.

---

# 7. Infrastructure

```text id="vjzw1k"
src/infrastructure/
```

Infrastructure chứa các implementation kỹ thuật.

```text id="j6s1pd"
infrastructure/
├── data/
│   ├── application_db_context.py
│   ├── configurations/
│   ├── interceptors/
│   └── migrations/
│
├── identity/
└── dependency_injection.py
```

Ví dụ quan hệ giữa Application và Infrastructure:

```text id="1o34mj"
APPLICATION

IApplicationDbContext
        ↑
        │ implements
        │
INFRASTRUCTURE

ApplicationDbContext
```

ApplicationDbContext chịu trách nhiệm làm việc với persistence/database.

Flow:

```text id="qpl1my"
Handler
   ↓
IApplicationDbContext
   ↓
ApplicationDbContext
   ↓
Database
```

---

# 8. Web

```text id="6z3i7p"
src/web/
```

Web là entry point của hệ thống.

```text id="4zn74u"
web/
├── endpoints/
├── infrastructure/
├── services/
├── schemas/
├── dependency_injection.py
└── main.py
```

Web chịu trách nhiệm:

```text id="r2i60i"
HTTP Request
      ↓
Endpoint
      ↓
Command / Query
      ↓
Application
```

Kết quả được chuyển ngược thành:

```text id="0r2t7n"
Application Result
      ↓
Web
      ↓
HTTP Response
```

Business logic không được đặt trong endpoint.

---

# 9. Request Flow

Ví dụ thêm Product vào Cart:

```text id="x8zd3c"
POST /cart/items
```

Flow:

```text id="1m2rkp"
WEB

Endpoint
   │
   │ tạo Command
   ↓

APPLICATION

AddProductToCartCommand
   ↓
Sender / Dispatcher
   ↓
AddProductToCartHandler
   │
   ├──────────────→ DOMAIN
   │                 Cart
   │                 Product
   │                 CartItem
   │
   ↓
IApplicationDbContext
   │
   │ implemented by
   ↓

INFRASTRUCTURE

ApplicationDbContext
   ↓
Database
```

Sau khi hoàn thành:

```text id="8vm63p"
Database
   ↑
ApplicationDbContext
   ↑
Handler
   ↑
Web
   ↑
HTTP Response
```

---

# 10. Extending the System

Kiến trúc được thiết kế để việc mở rộng ít ảnh hưởng đến các thành phần không liên quan.

## Thêm Entity

Ví dụ thêm:

```text id="dnz25w"
Supplier
```

thêm Domain Entity:

```text id="ir9yox"
domain/entities/supplier.py
```

và các use case:

```text id="r36jme"
application/suppliers/
├── commands/
└── queries/
```

---

## Thêm Business Rule

Ví dụ:

```text id="r2rfgf"
Order đã COMPLETED không được cancel.
```

Rule được đặt trong:

```text id="7bc47d"
Order.cancel()
```

Các layer bên ngoài chỉ sử dụng Domain rule đó.

---

## Thêm Use Case

Ví dụ:

```text id="u13ryv"
ApplyDiscount
```

có thể thêm thành Vertical Slice:

```text id="1p1gzy"
application/orders/commands/apply_discount/
```

mà không cần thay đổi các use case khác.

---

## Thay Persistence Implementation

Application tiếp tục phụ thuộc:

```text id="a2vtyn"
IApplicationDbContext
```

Infrastructure có thể thay đổi implementation mà Domain và phần lớn Application không cần thay đổi.

```text id="67e6h5"
Application
     ↓
IApplicationDbContext
     ↑
     │
Infrastructure implementation
```

---

## Thay External Service

External services được truy cập thông qua abstraction.

Ví dụ:

```text id="z0qwhd"
Application
     ↓
IPaymentGateway
     ↑
     │
Infrastructure
```

Implementation có thể được thay đổi mà use case không cần phụ thuộc trực tiếp vào provider.

---

# 11. Testing

Tests được chia theo layer và mục đích:

```text id="hs58pm"
tests/
├── domain_unit/
├── application_unit/
├── application_functional/
├── infrastructure_integration/
├── web_acceptance/
└── architecture/
```

Trong đó:

```text id="a4j3tc"
domain_unit
→ business rules

application_unit
→ Handler / use case

application_functional
→ Application workflows

infrastructure_integration
→ database và Infrastructure

web_acceptance
→ API

architecture
→ dependency giữa các layer
```

---

# 12. Development Rules

Khi thêm code mới:

1. Business rules thuộc **Domain**.
2. Use cases thuộc **Application**.
3. Database, framework và external services thuộc **Infrastructure**.
4. HTTP/API thuộc **Web**.
5. Dependency hướng vào trong.
6. Application phụ thuộc abstraction thay vì implementation cụ thể.
7. Command dùng cho thay đổi trạng thái.
8. Query dùng cho đọc dữ liệu.
9. Mỗi use case nên được tổ chức thành một Vertical Slice.
10. Tránh thêm abstraction hoặc pattern khi chưa có nhu cầu rõ ràng.

---

# 13. Development Strategy

Project được phát triển từng Vertical Slice:

```text id="t15v3v"
GetProducts
     ↓
GetProductById
     ↓
AddProductToCart
     ↓
GetCart
     ↓
UpdateCartItemQuantity
     ↓
Checkout
     ↓
CreateOrder
     ↓
GetOrder
     ↓
CancelOrder
```

Với mỗi feature, kiểm tra flow:

```text id="1bym7h"
Web
 ↓
Command / Query
 ↓
Handler
 ↓
Domain
 ↓
IApplicationDbContext
 ↓
ApplicationDbContext
 ↓
Database
```

---

# Architecture Summary

```text id="t5gsxd"
                    WEB
                     │
                     │ Command / Query
                     ↓
                APPLICATION
                Handler / Use Case
                 │          │
                 ↓          ↓
              DOMAIN    INTERFACE
                            ↑
                            │ implements
                            │
                    INFRASTRUCTURE
                            │
                         Database
```

> **Business logic nằm ở trung tâm; Web, database, framework và external services là các chi tiết bên ngoài có thể thay đổi.**
