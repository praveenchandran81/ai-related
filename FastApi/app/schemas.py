from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class ProductCreate(BaseModel):
    name: str
    description: str
    price: Decimal

    model_config = ConfigDict(from_attributes=True)


class ProductRead(ProductCreate):
    id: int
