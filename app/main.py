from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)


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


@app.get("/sqlalchemy")
def test(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"data": posts}


@app.get("/posts")
def get_posts(response: Response, db: Session = Depends(get_db)):
    response.headers["Cache-Control"] = "no-store"
    posts = db.query(models.Post).all()
    # cursor.execute("""SELECT * FROM posts """)
    # posts = cursor.fetchall()
    print(posts)
    return {"data": posts}


@app.get("/posts/{id}")
def get_post(id: int, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    
    # cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id)))
    # result = cursor.fetchone()

    return {"data": f"post : {post}"}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: models.Post, db: Session = Depends(get_db)):

    post = models.Post(
        title=post.title, content=post.content, published=post.published
    )

    db.add(post)
    db.commit()
    db.refresh(post)
    # cursor.execute("""INSERT INTO posts (title,content,published)
    #                 VALUES (%s,%s,%s) RETURNING *;""",
    #                (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()

    return {"data": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} not found!")
    
    post.delete(synchronize_session=False)
    db.commit()

    # cursor.execute(""" DELETE FROM posts WHERE id = %s returning *""", (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()
        
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def update(id: int, updated_post: models.Post, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} not found!")
    
    post.update(updated_post.model_dump(), synchronize_session=False)

    db.commit()

    return {"data": "successful"}


