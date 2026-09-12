from pydantic import BaseModel


class AddProductToCartRequest(BaseModel):
    product_id: str
    quantity: int
