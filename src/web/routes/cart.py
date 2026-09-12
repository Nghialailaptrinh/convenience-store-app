from fastapi import APIRouter

router = APIRouter(prefix="/cart", tags=["cart"])


@router.get("")
def get_cart() -> dict[str, str]:
    raise NotImplementedError("TODO: dispatch GetCart query")


@router.post("/items")
def add_product_to_cart() -> dict[str, str]:
    raise NotImplementedError("TODO: dispatch AddProductToCart command")
