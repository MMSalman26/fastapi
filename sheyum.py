from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()
app = FastAPI()

class Item(BaseModel):
    name: str
    description: str = None

def convert(books):
    my_dict={}
    book_list=[]

    for value in books:
        my_dict["id"]=value[0]
        my_dict["title"]=value[1]
        my_dict["author"]=value[2]
        my_dict["genre"]=value[3]
        book_list.append(my_dict)
        my_dict={}

    return book_list

@app.get("/items")
async def read_item():
    cursor.execute("SELECT * FROM students")
    item = cursor.fetchall()
    book_list=convert(item) # Calling Function


    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    
    return {"items": book_list}

@app.get("/items/{itemid1}/{itemid2}")
async def read_item(itemid1 : int, itemid2 : int):
    cursor.execute("SELECT * FROM students")
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




