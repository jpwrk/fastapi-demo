#!/usr/bin/python3
from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel
import mysql.connector
from mysql.connector import Error
import json
import os


DBHOST = "ds2022.cqee4iwdcaph.us-east-1.rds.amazonaws.com"
DBUSER = "admin"
DBPASS = os.getenv('DBPASS')
DB = "cqb3tc"

db = mysql.connector.connect(user=DBUSER, host=DBHOST, password=DBPASS, database=DB)
cur=db.cursor()


app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.get("/")
def zone_apex():
    return {"message": "Welcome to the API!"}


@app.get('/genres')
def get_genres():
    query = "SELECT * FROM genres ORDER BY genreid;"
    try:    
        cur.execute(query)
        headers=[x[0] for x in cur.description]
        results = cur.fetchall()
        json_data=[]
        for result in results:
            json_data.append(dict(zip(headers,result)))
        return(json_data)
    except Error as e:
        return {"Error": "MySQL Error: " + str(e)}


@app.get("/songs")
def get_songs():
    query = """
    SELECT
        songs.title,
        songs.album,
        songs.artist,
        songs.year,
        songs.file,
        songs.image,
        genres.genre
    FROM songs
    JOIN genres WHERE songs.genre = genres.genreid
    ORDER BY songs.id;
    """

    try:
        cur = db.cursor(dictionary=True)
        cur.execute(query)
        results = cur.fetchall()

        json_data = []
        
        for result in results:
            json_data.append(result)
        
        return json_data

    except Error as e:
        return {"Error": f"MySQL Error: {str(e)}"}
