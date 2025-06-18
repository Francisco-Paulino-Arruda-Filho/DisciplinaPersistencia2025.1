from pydantic import BaseModel

class ItemCreate(BaseModel):
    name: str
    description: str | None = None
    price: float
    in_stock: bool = True        

class Item(ItemCreate):
    id: str

                  