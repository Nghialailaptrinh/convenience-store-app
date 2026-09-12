# Đối chiếu cấu trúc mẫu

Nguồn: [jasontaylordev/CleanArchitecture](https://github.com/jasontaylordev/CleanArchitecture/tree/97663a0c6f0eb75a40df7b837708ee24dc74f61f),
commit `97663a0c6f0eb75a40df7b837708ee24dc74f61f`.
Giữ Python theo lựa chọn của project: PascalCase → snake_case, `.cs` → `.py`.
Đây là chuyển thể cấu trúc và mẫu triển khai, không phải bản sao chạy được của toàn bộ .NET template.

## File tương ứng

| Mẫu .NET | Project cửa hàng |
| --- | --- |
| `Application/TodoLists/Commands/CreateTodoList/CreateTodoList.cs` | `application/orders/commands/create_order/create_order.py` |
| `CreateTodoListCommandValidator.cs` | `create_order_command_validator.py` cùng slice |
| `Application/TodoItems/Commands/CreateTodoItem/CreateTodoItem.cs` | `application/carts/commands/add_product_to_cart/add_product_to_cart.py` |
| `Application/TodoItems/Commands/UpdateTodoItem/UpdateTodoItem.cs` | `application/carts/commands/update_cart_item_quantity/update_cart_item_quantity.py` |
| `Application/TodoItems/Commands/DeleteTodoItem/DeleteTodoItem.cs` | `application/carts/commands/remove_product_from_cart/remove_product_from_cart.py` |
| `Application/TodoLists/Queries/GetTodos/GetTodos.cs` | `application/products/queries/get_products/get_products.py` |
| `TodoItemDto.cs`, `TodoListDto.cs`, `TodosVm.cs` cạnh query | `product_dto.py`, `cart_dto.py`, `cart_item_dto.py`, `order_dto.py`, `order_item_dto.py` cạnh query tương ứng |
| `Common/Interfaces/IApplicationDbContext.cs` | `common/interfaces/application_db_context.py`: protocol, repository ports và `save_changes()` |
| `Common/Interfaces/IIdentityService.cs`, `IUser.cs` | `common/interfaces/identity_service.py`, `user.py` |
| `Common/Behaviours/*Behaviour.cs` | `common/behaviours/*_behaviour.py` |
| `Common/Models/LookupDto.cs`, `Result.cs` | `common/models/lookup_dto.py`, `result.py` |
| `Common/Security/AuthorizeAttribute.cs` | `common/security/authorize.py` |
| `Common/Exceptions/ValidationException.cs`, `ForbiddenAccessException.cs` | `common/exceptions/validation_exception.py`, `forbidden_access_exception.py` |
| `TodoItems/EventHandlers/LogTodoItemCompleted.cs` | `orders/event_handlers/log_order_created.py` |
| `Domain/Common/BaseEntity.cs`, `BaseAuditableEntity.cs`, `BaseEvent.cs`, `ValueObject.cs` | `domain/common/base_entity.py`, `base_auditable_entity.py`, `base_event.py`, `value_object.py` |
| `Domain/Entities/TodoList.cs`, `TodoItem.cs` | `domain/entities/product.py`, `category.py`, `customer.py`, `cart.py`, `cart_item.py`, `order.py`, `order_item.py` |
| `Domain/Enums/PriorityLevel.cs` | `domain/enums/order_status.py` |
| `Domain/ValueObjects/Colour.cs` | `domain/value_objects/money.py` |
| `Domain/Events/TodoItemCompletedEvent.cs` | `domain/events/order_created_event.py` |
| `Domain/Constants/Roles.cs` | `domain/constants/roles.py` |
| `Infrastructure/Data/ApplicationDbContext.cs` | `infrastructure/data/application_db_context.py` |
| `Infrastructure/Data/ApplicationDbContextInitialiser.cs` | `infrastructure/data/application_db_context_initialiser.py` |
| `Data/Configurations/TodoListConfiguration.cs`, `TodoItemConfiguration.cs` | `data/configurations/product_configuration.py`, `cart_configuration.py`, `order_configuration.py` |
| `Data/Interceptors/AuditableEntityInterceptor.cs`, `DispatchDomainEventsInterceptor.cs` | `data/interceptors/auditable_entity_interceptor.py`, `dispatch_domain_events_interceptor.py` |
| `Infrastructure/Identity/ApplicationUser.cs`, `IdentityService.cs`, `IdentityResultExtensions.cs` | `infrastructure/identity/application_user.py`, `identity_service.py`, `identity_result_extensions.py` |
| `Web/Endpoints/TodoLists.cs`, `TodoItems.cs` | `web/endpoints/products.py`, `carts.py`, `orders.py` |
| `Web/Endpoints/Users.cs`, `Services/CurrentUser.cs` | `web/endpoints/users.py`, `services/current_user.py` |
| `Web/Infrastructure/ProblemDetailsExceptionHandler.cs` | `web/infrastructure/problem_details_exception_handler.py` |
| `Web/Infrastructure/IEndpointGroup.cs` | `web/infrastructure/endpoint_group.py` |
| `Web/Infrastructure/EndpointRouteBuilderExtensions.cs`, `WebApplicationExtensions.cs` | `web/infrastructure/endpoint_route_builder_extensions.py`, `web_application_extensions.py` |
| `Web/Program.cs`, `appsettings.json`, `Web.http`, `wwwroot/` | `web/program.py`, `appsettings.json`, `web.http`, `wwwroot/` |
| `DependencyInjection.cs` tại mỗi outer layer | `dependency_injection.py` tại Application, Infrastructure, Web |
| `tests/Domain.UnitTests`, `Application.UnitTests`, `Application.FunctionalTests`, `Infrastructure.IntegrationTests`, `Web.AcceptanceTests` | Các thư mục tương ứng dạng `snake_case`, test nghiệp vụ đặt tiếp theo feature/commands/queries hoặc entities/value_objects |

## Phạm vi chuyển thể

- Giữ đủ 10 use case cửa hàng; không thay bằng CRUD Todo hoặc thêm chức năng thời tiết/counter của mẫu.
- Validator, DTO, handler, context, cấu hình ORM và Web đang nối vào demo. Các module Identity,
  authorization, auditing và domain-event dispatch có chú thích chưa cấu hình; không giả lập đăng nhập thành công.
- Base domain và event là khung mở rộng, chưa đổi entity đang chạy sang audited entity hoặc tự phát event.
  Logging/performance/unhandled-exception behaviours có mẫu xử lý nhưng chưa đăng ký vào dispatcher.
- Query DTO giữ response JSON hiện tại; không thêm `*Vm` chỉ để bọc lại một danh sách.
- `repositories/` là adapter nội bộ do `ApplicationDbContext` sở hữu; handler không phụ thuộc trực tiếp
  vào các repository này. `payment/`, `common/dispatching/` và các Python request/handler/sender protocols
  bổ sung phần cần cho demo, thay EF Core/MediatR bằng adapter Python. Context vẫn quản lý transaction nguyên tử.
- Không đưa `.csproj`, `.slnx`, `GlobalUsings.cs`, NuGet/MSBuild, Aspire/AppHost/TestAppHost,
  Angular/React client, ASP.NET Identity/OpenAPI transformers, launchSettings và .NET reflection extensions vào Python.
  `pyproject.toml`, FastAPI và `wwwroot` đảm nhiệm phần tương ứng. SQLite là provider demo hiện hành.
- Không đổi tên bảng hoặc xóa/reset dữ liệu `shop.db` khi chuyển cấu trúc.
