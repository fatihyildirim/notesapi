import os
from fastapi import FastAPI

app = FastAPI(title="Notes")

@app.get("/")
def root():
    return {
        "version": "0.1",
        "title": "Notes",
        "description": "A simple notes API"
    }