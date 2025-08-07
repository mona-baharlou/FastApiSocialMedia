from fastapi import FastAPI, Response, status
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time


app = FastAPI()


class PostModel(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


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


@app.get("/posts")
def get_posts(response: Response):
    response.headers["Cache-Control"] = "no-store"
    cursor.execute("""SELECT * FROM posts """)
    posts = cursor.fetchall()
    print(posts)
    return {"data": posts}


@app.get("/posts/{id}")
def get_post(id: int):
    return {"data": f"post id is {id}"}


@app.post("/posts")
def create_post(post: PostModel, status_code=status.HTTP_201_CREATED):
    cursor.execute("""INSERT INTO posts (title,content,published)
                    VALUES (%s,%s,%s) RETURNING *;""",
                   (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()

    return {"data": new_post}


