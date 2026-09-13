from collections.abc import Callable

from application.carts.commands.add_product_to_cart.add_product_to_cart import (
    AddProductToCartCommand,
    AddProductToCartCommandHandler,
)
from application.carts.commands.add_product_to_cart.add_product_to_cart_command_validator import (
    AddProductToCartCommandValidator,
)
from application.carts.commands.remove_product_from_cart.remove_product_from_cart import (
    RemoveProductFromCartCommand,
    RemoveProductFromCartCommandHandler,
)
from application.carts.commands.remove_product_from_cart.remove_product_from_cart_command_validator import (
    RemoveProductFromCartCommandValidator,
)
from application.carts.commands.update_cart_item_quantity.update_cart_item_quantity import (
    UpdateCartItemQuantityCommand,
    UpdateCartItemQuantityCommandHandler,
)
from application.carts.commands.update_cart_item_quantity.update_cart_item_quantity_command_validator import (
    UpdateCartItemQuantityCommandValidator,
)
from application.carts.queries.get_cart.get_cart import (
    GetCartQuery,
    GetCartQueryHandler,
)
from application.common.dispatching.dispatcher import Dispatcher
from application.common.interfaces.application_db_context import IApplicationDbContext
from application.common.interfaces.current_user import ICurrentUser
from application.common.interfaces.identity_service import IIdentityService
from application.common.interfaces.payment_gateway import IPaymentGateway
from application.common.interfaces.sender import Sender
from application.common.interfaces.token_service import ITokenService
from application.identity.commands.login_user.login_user import (
    LoginUserCommand,
    LoginUserCommandHandler,
)
from application.identity.commands.login_user.login_user_command_validator import (
    LoginUserCommandValidator,
)
from application.identity.commands.register_user.register_user import (
    RegisterUserCommand,
    RegisterUserCommandHandler,
)
from application.identity.commands.register_user.register_user_command_validator import (
    RegisterUserCommandValidator,
)
from application.identity.queries.get_current_user.get_current_user import (
    GetCurrentUserQuery,
    GetCurrentUserQueryHandler,
)
from application.orders.commands.cancel_order.cancel_order import (
    CancelOrderCommand,
    CancelOrderCommandHandler,
)
from application.orders.commands.cancel_order.cancel_order_command_validator import (
    CancelOrderCommandValidator,
)
from application.orders.commands.checkout.checkout import (
    CheckoutCommand,
    CheckoutCommandHandler,
)
from application.orders.commands.checkout.checkout_command_validator import (
    CheckoutCommandValidator,
)
from application.orders.commands.create_order.create_order import (
    CreateOrderCommand,
    CreateOrderCommandHandler,
)
from application.orders.commands.create_order.create_order_command_validator import (
    CreateOrderCommandValidator,
)
from application.orders.queries.get_order.get_order import (
    GetOrderQuery,
    GetOrderQueryHandler,
)
from application.products.queries.get_product_by_id.get_product_by_id import (
    GetProductByIdQuery,
    GetProductByIdQueryHandler,
)
from application.products.queries.get_products.get_products import (
    GetProductsQuery,
    GetProductsQueryHandler,
)


def create_sender(
    context_factory: Callable[[], IApplicationDbContext],
    payment: IPaymentGateway,
    identity: IIdentityService | None = None,
    tokens: ITokenService | None = None,
    current_user: ICurrentUser | None = None,
) -> Sender:
    """Register use cases, injecting fresh transaction dependencies per send."""
    sender = Dispatcher()
    if identity is not None:
        sender.register(
            RegisterUserCommand,
            lambda: RegisterUserCommandHandler(identity),
            RegisterUserCommandValidator(),
        )
        if tokens is not None:
            sender.register(
                LoginUserCommand,
                lambda: LoginUserCommandHandler(identity, tokens),
                LoginUserCommandValidator(),
            )
        if current_user is not None:
            sender.register(
                GetCurrentUserQuery, lambda: GetCurrentUserQueryHandler(current_user, identity)
            )
    sender.register(
        AddProductToCartCommand,
        lambda: AddProductToCartCommandHandler(context_factory()),
        AddProductToCartCommandValidator(),
    )
    sender.register(
        RemoveProductFromCartCommand,
        lambda: RemoveProductFromCartCommandHandler(context_factory()),
        RemoveProductFromCartCommandValidator(),
    )
    sender.register(
        UpdateCartItemQuantityCommand,
        lambda: UpdateCartItemQuantityCommandHandler(context_factory()),
        UpdateCartItemQuantityCommandValidator(),
    )
    sender.register(GetCartQuery, lambda: GetCartQueryHandler(context_factory()))
    sender.register(
        CancelOrderCommand,
        lambda: CancelOrderCommandHandler(context_factory()),
        CancelOrderCommandValidator(),
    )
    sender.register(
        CheckoutCommand,
        lambda: CheckoutCommandHandler(context_factory(), payment),
        CheckoutCommandValidator(),
    )
    sender.register(
        CreateOrderCommand,
        lambda: CreateOrderCommandHandler(context_factory()),
        CreateOrderCommandValidator(),
    )
    sender.register(GetOrderQuery, lambda: GetOrderQueryHandler(context_factory()))
    sender.register(GetProductByIdQuery, lambda: GetProductByIdQueryHandler(context_factory()))
    sender.register(GetProductsQuery, lambda: GetProductsQueryHandler(context_factory()))
    return sender
