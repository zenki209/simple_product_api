#This is for pydantic model

from pydantic import BaseModel


class Product(BaseModel):
    name: str
    description: str
    price: int
