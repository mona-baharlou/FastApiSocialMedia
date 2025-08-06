from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel

app = FastAPI()


class PostModel(BaseModel):
    title: str
    content: str
    published: bool = True


@app.get("/")
def root():
    return {"message": "Hello !"}


@app.get("/posts")
def get_posts():
    return {"data": "Your Posts"}


@app.post("/createpost")
def create_post(new_post: PostModel):
    print(new_post)
    return {"data": "New post is created!"}
