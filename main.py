from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, conlist
import sqlite3

conn = sqlite3.connect('test.db')  # Updated to use test.db
cursor = conn.cursor()

# Ensure the database table for users exists
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        user_name TEXT NOT NULL,
        balance INTEGER
    )
''')
conn.commit()

app = FastAPI()

class User(BaseModel):
    user_id: int
    user_name: str
    balance: int

@app.post("/api/users", status_code=status.HTTP_201_CREATED)
async def create_user(user: User):
    cursor.execute("INSERT INTO users (user_id, user_name, balance) VALUES (?, ?, ?)", (user.user_id, user.user_name, user.balance))
    conn.commit()
    
    return user.dict()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS stations (
        station_id INTEGER PRIMARY KEY,
        station_name TEXT NOT NULL,
        longitude FLOAT,
        latitude FLOAT
    )
''')
conn.commit()

class Station(BaseModel):
    station_id: int
    station_name: str
    longitude: float
    latitude: float

@app.post("/api/stations", status_code=status.HTTP_201_CREATED)
async def create_station(station: Station):
    cursor.execute("INSERT INTO stations (station_id, station_name, longitude, latitude) VALUES (?, ?, ?, ?)",
                   (station.station_id, station.station_name, station.longitude, station.latitude))
    conn.commit()
    
    return station.dict()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS trains (
        train_id INTEGER PRIMARY KEY,
        train_name TEXT NOT NULL,
        capacity INTEGER,
        service_start TEXT,
        service_ends TEXT,
        num_stations INTEGER
    )
''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS train_stops (
        train_id INTEGER,
        station_id INTEGER,
        arrival_time TEXT,
        departure_time TEXT,
        fare INTEGER,
        FOREIGN KEY(train_id) REFERENCES trains(train_id)
    )
''')

conn.commit()

class Stop(BaseModel):
    station_id: int
    arrival_time: str = None
    departure_time: str
    fare: int

class Train(BaseModel):
    train_id: int
    train_name: str
    capacity: int
    stops: conlist(Stop, min_items=2)

@app.post("/api/trains", status_code=status.HTTP_201_CREATED)
async def create_train(train: Train):
    num_stations = len(train.stops)
    service_start = train.stops[0].departure_time
    service_ends = train.stops[-1].arrival_time

    train.stops[0].arrival_time = None
    train.stops[-1].departure_time = None
    cursor.execute("INSERT INTO trains (train_id, train_name, capacity, service_start, service_ends, num_stations) VALUES (?, ?, ?, ?, ?, ?)",
                   (train.train_id, train.train_name, train.capacity, service_start, service_ends, num_stations))
    for stop in train.stops:
        cursor.execute("INSERT INTO train_stops (train_id, station_id, arrival_time, departure_time, fare) VALUES (?, ?, ?, ?, ?)",
                       (train.train_id, stop.station_id, stop.arrival_time, stop.departure_time, stop.fare))
    conn.commit()
    
    return {
        "train_id": train.train_id,
        "train_name": train.train_name,
        "capacity": train.capacity,
        "service_start": service_start,
        "service_ends": service_ends,
        "num_stations": num_stations
    }