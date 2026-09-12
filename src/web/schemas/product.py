from pydantic import BaseModel


class ProductResponse(BaseModel):
    id: str
    name: str
    description: str
    price: str
