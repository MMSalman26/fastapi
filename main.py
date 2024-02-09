from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# cursor.execute('''
#     CREATE TABLE IF NOT EXISTS items (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         name TEXT NOT NULL,
#         description TEXT
#     )
# ''')
# conn.commit()

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str = None

@app.get("/items")
async def read_item():
    cursor.execute("SELECT * FROM items")
    item = cursor.fetchall()

    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    
    return {"items": item}

@app.get("/items/{itemid1}/{itemid2}")
async def read_item(itemid1 : int, itemid2 : int):
    cursor.execute("SELECT * FROM items")
    item = cursor.fetchone()

    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    
    return {"items": itemid1 + itemid2}

@app.get("/items/")
async def read_item(itemid1 : str = None, itemid2 : str = None):
    cursor.execute("SELECT * FROM items")
    item = cursor.fetchone()
    value = ""
    if itemid1 :
        value = itemid1
    if itemid2 : 
        value = itemid2 
    if itemid1 and itemid2 : 
        value = itemid1 + itemid2
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    
    return {"items": value}

@app.post("/items")
async def create_item(item: Item):
    cursor.execute("INSERT INTO items (name, description) VALUES (?, ?)", (item.name, item.description))
    conn.commit()
    
    return {"message": "Item created successfully"}

# @app.put("/items/{item_id}")
# async def update_item(item_id: int, item: Item):
#     cursor.execute("UPDATE items SET name=?, description=? WHERE id=?", (item.name, item.description, item_id))
#     conn.commit()
    
#     return {"message": "Item updated successfully"}

# @app.delete("/items/{item_id}")
# async def delete_item(item_id: int):
#     cursor.execute("DELETE FROM items WHERE id=?", (item_id,))
#     conn.commit()
    
#     return {"message": "Item deleted successfully"}
