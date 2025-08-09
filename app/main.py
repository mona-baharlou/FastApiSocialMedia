from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from typing import List
from sqlalchemy.orm import Session
from . import models, schemas, utils
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)


app = FastAPI()


while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi',
                                user='postgres', password='Nima1234',
                                cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("DB connection was ok")
        break
    except Exception as error:
        print('DB connectin failed')
        print("Error", error)
        time.sleep(2)


my_posts = [{"title": "Title 1", "content": "Content1", "id": 1},
            {"title": "Title 2", "content": "Content2", "id": 2}
            ]


@app.get("/")
def root():
    return {"message": "Hello !"}


# @app.get("/sqlalchemy")
# def test(db: Session = Depends(get_db)):
#     posts = db.query(models.Post).all()
#     return {"data": posts}


