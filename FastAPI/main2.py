from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    valor: float
    is_oferta: Union[bool, None] = None

item_db = {}

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.put("/items/{item_id}")
def atualiza_item(item_id: int, item: Item):
    if item_id in item_db:
        item_db[item_id] = item
        return {"item_id": item_id, "item": item}
    else:
        return {"error": "Item not found"}
    
@app.get("items/")
def le_item(): 
    return item_db