from dataclasses import dataclass
from uuid import UUID

from application.common.interfaces.application_db_context import IApplicationDbContext
from application.common.interfaces.request import Request
from application.common.interfaces.request_handler import RequestHandler
from application.products.queries.get_products.product_dto import ProductDto


@dataclass(frozen=True)
class GetProductByIdQuery(Request[ProductDto | None]):
    product_id: UUID


class GetProductByIdQueryHandler(
    RequestHandler[GetProductByIdQuery, ProductDto | None]
):
    def __init__(self, context: IApplicationDbContext) -> None:
        self._context = context

    def handle(self, request: GetProductByIdQuery) -> ProductDto | None:
        with self._context:
            product = self._context.products.get_by_id(request.product_id)
            return ProductDto.from_domain(product) if product else None
