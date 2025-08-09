from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from typing import List
from sqlalchemy.orm import Session
from . import models, schemas
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


@app.get("/posts", response_model=List[schemas.PostResponse])
def get_posts(response: Response, db: Session = Depends(get_db)):
    response.headers["Cache-Control"] = "no-store"
    posts = db.query(models.Post).all()
    # cursor.execute("""SELECT * FROM posts """)
    # posts = cursor.fetchall()
    return posts


@app.get("/posts/{id}", response_model=schemas.PostResponse)
def get_post(id: int, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    
    # cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id)))
    # result = cursor.fetchone()

    return post


@app.post("/posts", status_code=status.HTTP_201_CREATED,
          response_model=schemas.PostResponse
          )
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):

    new_post = models.Post(**post.model_dump())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    # cursor.execute("""INSERT INTO posts (title,content,published)
    #                 VALUES (%s,%s,%s) RETURNING *;""",
    #                (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()

    return new_post


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


@app.put("/posts/{id}",
         status_code=status.HTTP_200_OK,
         response_model=schemas.PostResponse
         )
def update(id: int, updated_post: schemas.PostCreate,
           db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    if post_query.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} not found!")
    
    post_query.update(**updated_post.model_dump(), synchronize_session=False)

    db.commit()

    return post_query.first()


@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_user(user: schemas.User, db: Session = Depends(get_db)):
    new_user = models.User(**user.model_dump())

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

