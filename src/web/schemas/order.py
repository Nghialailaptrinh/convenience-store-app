from pydantic import BaseModel


class CheckoutRequest(BaseModel):
    customer_id: str
