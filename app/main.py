#!/usr/bin/env python3

from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel
import json
import os

app = FastAPI()

@app.get("/")  # zone apex
def zone_apex():
    return {"Hey": "Shawty"}

@app.get("/square/{a}")
def square(a: int, b: int):
    return {"square": a**2}
@app.get("/multiply/{c}/{d}")
def multiply(c:int,d:int):
    return{"product":c*d}
