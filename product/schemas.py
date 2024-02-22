#This is for pydantic model

from pydantic import BaseModel


class Product(BaseModel):
    name: str
    description: str
    price: int



#There are some case you did not want the response return all of the data so we have to build a class for the dispaly
class DisplayProduct(BaseModel):
    name: str
    description: str

    class Config:
        from_attributes = True


class Seller(BaseModel):
    name: str
    email: str
    password: str