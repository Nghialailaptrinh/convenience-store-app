from uuid import UUID

from fastapi import APIRouter, HTTPException

from application.products.queries.get_product_by_id.get_product_by_id import GetProductByIdQuery
from application.products.queries.get_products.get_products import GetProductsQuery
from application.products.queries.get_products.product_dto import ProductDto
from web.dependency_injection import SenderDependency

router = APIRouter(prefix="/products", tags=["products"])


@router.get("", response_model=list[ProductDto])
def get_products(sender: SenderDependency, include_inactive: bool = False):
    return sender.send(GetProductsQuery(include_inactive))


@router.get("/{product_id}", response_model=ProductDto)
def get_product_by_id(product_id: UUID, sender: SenderDependency):
    result = sender.send(GetProductByIdQuery(product_id))
    if result is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return result
