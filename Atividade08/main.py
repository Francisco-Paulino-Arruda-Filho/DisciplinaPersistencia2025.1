from fastapi import FastAPI
from crud import create_document, get_all_items, get_item_by_id, update_item, delete_item
from schemas import ItemCreate, Item

app = FastAPI()

@app.post("/items/", response_model=Item)
def create_item(item: ItemCreate):
    """Create a new item."""
    item_data = item.dict()
    item_id = create_document(item_data)
    return {**item_data, "id": item_id}

@app.get("/items/", response_model=list[Item])
def read_items():
    """Retrieve all items."""
    items = get_all_items()
    return items

@app.get("/items/{item_id}", response_model=Item)   
def read_item(item_id: str):
    """Retrieve a single item by its ID."""
    item = get_item_by_id(item_id)
    if item:
        return item
    return {"error": "Item not found"}

@app.put("/items/{item_id}", response_model=Item)
def update_item_endpoint(item_id: str, item: ItemCreate):
    """Update an existing item by its ID."""
    updated_item = update_item(item_id, item.dict())
    if updated_item:
        return updated_item
    return {"error": "Item not found or not updated"}

@app.delete("/items/{item_id}", response_model=dict)
def delete_item_endpoint(item_id: str):
    """Delete an item by its ID."""
    if delete_item(item_id):
        return {"message": "Item deleted successfully"}
    return {"error": "Item not found or not deleted"}