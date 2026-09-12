from uuid import UUID

from fastapi import APIRouter, HTTPException

from application.products.queries.get_product_by_id import query as get_product_slice
from application.products.queries.get_products import query as get_products_slice
from web.schemas.product import ProductResponse

router = APIRouter(prefix="/products", tags=["products"])


@router.get("", response_model=list[ProductResponse])
def get_products(include_inactive: bool = False):
    return get_products_slice.handle(get_products_slice.GetProductsQuery(include_inactive))


@router.get("/{product_id}", response_model=ProductResponse)
def get_product_by_id(product_id: UUID):
    result = get_product_slice.handle(get_product_slice.GetProductByIdQuery(product_id))
    if result is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return result
