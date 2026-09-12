# Convenience Store Shopping App

Ung dung mua hang cho cua hang tien loi, duoc to chuc theo tu tuong **Clean Architecture**.

Muc tieu cua project khong chi la tao mot ung dung hoat dong duoc, ma con xay dung cau truc phan mem ro rang, de mo rong, de kiem thu va han che business logic phu thuoc vao database, framework hoac giao dien nguoi dung.

> README nay dung tieng Viet khong dau de de doc trong moi terminal va moi moi truong phat trien.

---

## 1. Architecture

Project su dung 4 layer chinh:

```text
Web
  |
  v
Application
  |
  v
Domain

Infrastructure ---> Application
```

Quy tac quan trong nhat:

```text
Dependencies point inward.
```

Dieu do co nghia la:

- `Domain` khong phu thuoc layer nao khac.
- `Application` co the phu thuoc `Domain`.
- `Infrastructure` trien khai cac interface cua `Application` va su dung `Domain`.
- `Web` goi `Application` de thuc hien use case.
- Business logic khong phu thuoc truc tiep vao database, HTTP hay framework.

---

## 2. Responsibilities

### Domain

Domain mo ta cac doi tuong va quy tac cot loi cua bai toan cua hang tien loi:

```text
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

Domain khong duoc biet ve:

```text
HTTP
FastAPI / Django
SQLAlchemy
PostgreSQL / SQLite
Redis
Stripe
HTML / React
```

Vi du, `Order` co the quan ly:

```text
Order
 |- OrderItem
 |- Money
 |- OrderStatus
 `- business rules
```

### Application

Application chua cac use case cua he thong va tra loi cau hoi:

```text
He thong co the lam gi?
```

Use case ban dau:

```text
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

Application su dung Domain, nhung chi phu thuoc vao abstraction. Repository va payment gateway duoc khai bao tai `src/application/interfaces`, khong goi database hay framework truc tiep.

### Infrastructure

Infrastructure chiu trach nhiem cho cac chi tiet ky thuat:

```text
Database
Repository implementations
SQLAlchemy
PostgreSQL / SQLite
Payment gateway
External services
```

Application chi biet interface, vi du:

```text
ProductRepository
CartRepository
OrderRepository
PaymentGateway
```

Infrastructure se cung cap implementation tuong ung, vi du:

```text
SqlAlchemyProductRepository
PostgreSQLOrderRepository
FakePaymentGateway
StripePaymentGateway
```

### Web

Web la cong giao tiep giua client va Application:

```text
HTTP Request
  |
  v
convert request
  |
  v
Application use case
  |
  v
HTTP Response
```

Web khong nen chua business logic. Route chi nen parse request, tao command/query, goi handler va chuyen ket qua thanh response.

---

## 3. Project Structure

Cau truc hien tai:

```text
convenience-store/
|
|- src/
|  |- domain/
|  |  |- entities/
|  |  |  |- product.py
|  |  |  |- category.py
|  |  |  |- customer.py
|  |  |  |- cart.py
|  |  |  |- cart_item.py
|  |  |  |- order.py
|  |  |  `- order_item.py
|  |  |- value_objects/
|  |  |  `- money.py
|  |  `- enums/
|  |     `- order_status.py
|  |
|  |- application/
|  |  |- products/
|  |  |  |- get_products/query.py
|  |  |  `- get_product_by_id/query.py
|  |  |- cart/
|  |  |  |- add_product/command.py
|  |  |  |- remove_product/command.py
|  |  |  |- update_item_quantity/command.py
|  |  |  `- get_cart/query.py
|  |  |- orders/
|  |  |  |- checkout/command.py
|  |  |  |- create_order/command.py
|  |  |  |- get_order/query.py
|  |  |  `- cancel_order/command.py
|  |  `- interfaces/
|  |     |- product_repository.py
|  |     |- cart_repository.py
|  |     |- order_repository.py
|  |     `- payment_gateway.py
|  |
|  |- infrastructure/
|  |  |- database/connection.py
|  |  |- repositories/sqlalchemy_product_repository.py
|  |  `- payment/fake_payment_gateway.py
|  |
|  `- web/
|     |- routes/
|     |  |- health.py
|     |  |- products.py
|     |  |- cart.py
|     |  `- orders.py
|     |- schemas/
|     |  |- product.py
|     |  |- cart.py
|     |  `- order.py
|     `- main.py
|
|- tests/
|  |- unit/
|  |- integration/
|  `- functional/
|
|- pyproject.toml
|- .gitignore
`- README.md
```

`tests/` la cau truc du kien cho cac buoc tiep theo; skeleton hien tai chua implement day du business logic va test.

---

## 4. Vertical Slice

Application duoc to chuc theo tung use case thay vi gom tat ca logic vao mot service lon.

Vi du:

```text
application/
`- cart/
 `- add_product/
  `- command.py
```

Moi slice chi chua nhung gi lien quan truc tiep den use case do. Khi use case phat trien, co the bo sung:

```text
command.py      # Mo ta yeu cau thay doi he thong
validator.py    # Kiem tra input va invariant o application boundary
handler.py      # Orchestrate use case
```

Trong skeleton hien tai, command/query va ham `handle` dang duoc dat cung file de giu pham vi nho. Khi bat dau implement business logic, co the tach `handler.py` va `validator.py` theo nhu cau.

---

## 5. Command and Query

Project su dung tu tuong CQRS o muc don gian.

### Command

Command lam thay doi trang thai he thong:

```text
AddProductToCart
RemoveProductFromCart
UpdateCartItemQuantity
Checkout
CreateOrder
CancelOrder
```

Flow du kien:

```text
Command
 |
 v
Validator
 |
 v
Handler
 |
 v
Domain
 |
 v
Repository Interface
```

### Query

Query chi doc du lieu va khong nen thay doi trang thai he thong:

```text
GetProducts
GetProductById
GetCart
GetOrder
```

---

## 6. Dependency Inversion

Application khong phu thuoc truc tiep vao database implementation.

```text
Application
  |
  v
OrderRepository (interface)
  ^
  |
Infrastructure implementation
```

Application chi can biet cac thao tac can thiet, vi du:

```text
save(order)
get_by_id(id)
```

No khong can biet phia duoi dang dung SQLite, PostgreSQL hay he quan tri co so du lieu khac.

---

## 7. API Status

Endpoint da co:

```text
GET /health
```

Cac route feature da duoc tao de lam boundary, nhung dang la TODO va chua dispatch handler:

```text
GET  /products
GET  /products/{product_id}
GET  /cart
POST /cart/items
POST /orders/checkout
GET  /orders/{order_id}
```

Khong nen xem cac route TODO la business implementation. Business logic se duoc them o Application truoc, sau do Web moi duoc noi vao handler.

---

## 8. Example Request Flow

Vi du checkout gio hang:

```text
Client
 |
 v
POST /orders/checkout
 |
 v
Web route
 |
 v
CheckoutCommand
 |
 v
Checkout handler
 |
 v
Cart / Product / Order / Money
 |
 v
OrderRepository + PaymentGateway
 |
 v
Infrastructure
 |
 v
Database / Payment provider
```

Ket qua di nguoc lai qua Infrastructure, Application va Web ve client.

---

## 9. Initial Core Flow

Version dau tien tap trung vao flow:

```text
View Products
  |
  v
Add Product To Cart
  |
  v
Update Quantity
  |
  v
View Cart
  |
  v
Checkout
  |
  v
Create Order
  |
  v
Payment
  |
  v
Complete Order
```

Chua nen dua qua nhieu chuc nang vao ngay tu dau. Cac chuc nang co the bo sung sau:

```text
Promotion
Voucher
Loyalty points
Inventory management
Multiple stores
Delivery
Recommendation system
AI assistant
Analytics
```

---

## 10. Development Principles

Khi them mot chuc nang moi:

1. Xac dinh business object va business rule trong `Domain`.
2. Xac dinh use case trong `Application`.
3. Tao `Command` hoac `Query`.
4. Tao `Validator` neu can.
5. Tao handler va viet unit test cho use case.
6. Neu can external dependency, tao interface trong `Application`.
7. Implement interface trong `Infrastructure`.
8. Cuoi cung tao hoac cap nhat Web/API endpoint.

Khong dat business logic truc tiep trong:

```text
route
controller
database model
SQL query
```

---

## 11. Local Development

Tao moi truong va cai dependencies:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
py -m pip install -e ".[dev]"
```

Chay API:

```powershell
uvicorn src.web.main:app --reload
```

Sau do mo Swagger tai `http://127.0.0.1:8000/docs` va kiem tra `GET /health`.

Dependencies va cau hinh lint/test nam trong [pyproject.toml](pyproject.toml).

The domain has no dependency on FastAPI, SQLAlchemy, or any other framework.

## Run locally

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
py -m pip install -e ".[dev]"
uvicorn src.web.main:app --reload
```

The API currently exposes `GET /health`. Feature endpoints and handlers are intentionally TODOs.

## Structure

- `src/domain`: entities, value objects, enums, and business rules
- `src/application`: vertical slices with commands, queries, and ports
- `src/infrastructure`: database, repository, and payment adapters
- `src/web`: HTTP routes, schemas, and dependency wiring
