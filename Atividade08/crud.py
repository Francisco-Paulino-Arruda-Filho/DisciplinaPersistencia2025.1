from database import db
from bson.objectid import ObjectId

def create_document(data):
    """Create a new document in the collection."""
    result = db.items.insert_one(data)
    return str(result.inserted_id)

def get_all_items():
    """Retrieve all items from the collection."""
    items = db.items.find()
    result = []
    for item in items:
        print(item)
        item['_id'] = str(item['_id'])  # Convert ObjectId to string
        result.append(item)
    return result

def get_item_by_id(item_id):
    """Retrieve a single item by its ID."""
    item = db.items.find_one({"_id": ObjectId(item_id)})
    if item:
        item['_id'] = str(item['_id'])  # Convert ObjectId to string
        return item
    return None    

def update_item(item_id, data):
    """Update an existing item by its ID."""
    result = db.items.update_one({"_id": ObjectId(item_id)}, {"$set": data})
    if result.modified_count > 0:
        return get_item_by_id(item_id)
    return None

def delete_item(item_id):
    """Delete an item by its ID."""
    result = db.items.delete_one({"_id": ObjectId(item_id)})
    if result.deleted_count > 0:
        return True
    return False                                     