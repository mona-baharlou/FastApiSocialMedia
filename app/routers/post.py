from fastapi import Response, status, HTTPException, Depends, APIRouter
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from .. import models, schemas, oauth2
from ..database import get_db


router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)


@router.get("/", response_model=List[schemas.PostOut])
def get_posts(response: Response, db: Session = Depends(get_db),
              current_user: models.User = Depends(oauth2.get_current_user),
              limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    
    response.headers["Cache-Control"] = "no-store"
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id,
                                                                    isouter=True).group_by(models.Post.id).filter(
                                                                        models.Post.title.contains(search)
                                                                        ).limit(limit).offset(skip).all()



    # cursor.execute("""SELECT * FROM posts """)
    # posts = cursor.fetchall()
    return results


# @router.get("/{id}", response_model=schemas.PostOut)
# def get_post(id: int, db: Session = Depends(get_db),
#              current_user: models.User = Depends(oauth2.get_current_user)):
    
#     # post_query = db.query(models.Post).filter(models.Post.id == id)

#     result = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id,
#                                                                     isouter=True).group_by(models.Post.id).filter(models.Post.id == id)
    
#     print(result)
#     post = result.first()
#     print(**post.model_dump())

#     # post, votes = results


#     if post is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"post with id: {id} does not exist")
#     # if not hasattr(post, "owner_id"):
#     #     raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#     #                         detail="Post object missing owner_id")

#     if str(post.owner_id) != str(current_user.id):
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
#                             detail="Not authorized to perform requested action")

#     # cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id)))
#     # result = cursor.fetchone()

#     return post  # schemas.PostOut(Post=post, votes=votes)


@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db),
             current_user: models.User = Depends(oauth2.get_current_user)):

    result = db.query(
        models.Post,
        func.count(models.Vote.post_id).label("votes")
    ).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True
    ).group_by(
        models.Post.id
    ).filter(
        models.Post.id == id
    )

    post = result.first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")

    post_obj, votes_count = post

    if not hasattr(post_obj, "owner_id"):
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Post object missing owner_id")


    if str(post_obj.owner_id) != str(current_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    return schemas.PostOut(Post=post_obj, votes=votes_count)



@router.post("/", status_code=status.HTTP_201_CREATED,
             response_model=schemas.PostResponse
             )
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db),
                current_user: models.User = Depends(oauth2.get_current_user)):
    
    print(current_user)

    new_post = models.Post(owner_id=current_user.id, **post.model_dump())

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
def delete_post(id: int, db: Session = Depends(get_db),
                current_user: models.User = Depends(oauth2.get_current_user)):
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} not found!")
    
    if not hasattr(post, "owner_id"):
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Post object missing owner_id")


    # print(f"Comparing: post.owner_id={post.owner_id} ({type(post.owner_id)})
    #       with current_user.id={current_user.id} ({type(current_user.id)})")

    if str(post.owner_id) != str(current_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")
    
    post_query.delete(synchronize_session=False)
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
           db: Session = Depends(get_db),
           current_user: models.User = Depends(oauth2.get_current_user)):
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} not found!")
    
    if not hasattr(post, "owner_id"):
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Post object missing owner_id")

    if str(post.owner_id) != str(current_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")
    
    post_query.update(**updated_post.model_dump(), synchronize_session=False)

    db.commit()

    return post_query.first()