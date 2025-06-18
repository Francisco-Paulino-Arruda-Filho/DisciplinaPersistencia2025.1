from pydantic import BaseModel
from typing import Optional

class ItemModel(BaseModel):
    id: Optional[str]
    name: str
    description: Optional[str] = None
    price: float
    in_stock: bool = True

