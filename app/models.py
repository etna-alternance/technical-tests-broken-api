from pydantic import BaseModel, NonNegativeInt

from .db import ProductType


class Product(BaseModel):
    id: int
    name: str
    type: ProductType
    price: NonNegativeInt


class ProductCreate(BaseModel):
    name: str
    type: ProductType
    price: int
