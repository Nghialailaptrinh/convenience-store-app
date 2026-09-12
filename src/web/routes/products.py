from fastapi import APIRouter

router = APIRouter(prefix="/products", tags=["products"])


@router.get("")
def get_products() -> dict[str, str]:
    raise NotImplementedError("TODO: dispatch GetProducts query")


@router.get("/{product_id}")
def get_product_by_id(product_id: str) -> dict[str, str]:
    raise NotImplementedError("TODO: dispatch GetProductById query")
