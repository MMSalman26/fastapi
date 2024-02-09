from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str = None

@app.get("/items")
async def read_item():
    cursor.execute("SELECT * FROM students")
    item = cursor.fetchall()

    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    
    return {"item": item}

@app.get("/items/{itemid1}/{itemid2}")
async def read_item(itemid1 : int, itemid2 : int):
    cursor.execute("SELECT * FROM items")
    item = cursor.fetchone()

    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    
    return {"new file": itemid1 + itemid2}

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




