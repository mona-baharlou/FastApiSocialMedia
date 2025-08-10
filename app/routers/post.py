from fastapi import Response, status, HTTPException, Depends, APIRouter
from typing import List
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db


router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)


@router.get("/", response_model=List[schemas.PostResponse])
def get_posts(response: Response, db: Session = Depends(get_db)):
    response.headers["Cache-Control"] = "no-store"
    posts = db.query(models.Post).all()
    # cursor.execute("""SELECT * FROM posts """)
    # posts = cursor.fetchall()
    return posts


@router.get("/{id}", response_model=schemas.PostResponse)
def get_post(id: int, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    
    # cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id)))
    # result = cursor.fetchone()

    return post


@router.post("/", status_code=status.HTTP_201_CREATED,
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


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
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


@router.put("/{id}",
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