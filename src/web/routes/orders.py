from fastapi import APIRouter

router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("/checkout")
def checkout() -> dict[str, str]:
    raise NotImplementedError("TODO: dispatch Checkout command")


@router.get("/{order_id}")
def get_order(order_id: str) -> dict[str, str]:
    raise NotImplementedError("TODO: dispatch GetOrder query")
