from dataclasses import dataclass

from application.common.interfaces.application_db_context import ApplicationDbContext
from application.common.interfaces.request import Request
from application.common.interfaces.request_handler import RequestHandler
from application.products.queries.get_products.product_dto import ProductDto


@dataclass(frozen=True)
class GetProductsQuery(Request[list[ProductDto]]):
    include_inactive: bool = False


class GetProductsQueryHandler(RequestHandler[GetProductsQuery, list[ProductDto]]):
    def __init__(self, context: ApplicationDbContext) -> None:
        self._context = context

    def handle(self, request: GetProductsQuery) -> list[ProductDto]:
        with self._context:
            return [
                ProductDto.from_domain(p)
                for p in self._context.products.get_all()
                if request.include_inactive or p.is_active
            ]
