from fastapi import FastAPI
from fastapi import Body, Response, status, HTTPException
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor


app = FastAPI()

my_posts = [
            {"title": "title of first post", "content":"content of first post", "id": 1},
            {"title": "title of second post", "content":"content of second post", "id": 2}
            ] 


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p
        
def find_index(id):
    for index, post in enumerate(my_posts):
        if post['id'] == id:
            return index
    return None  # If no post is found with the given id


@app.get("/")
def root():
    return {"message": "This is root path"}

@app.get("/posts")
def get_posts():
    return {"data":my_posts}

# @app.post("/createposts")
# def create_posts(payload: dict = Body(...)):
#     print(payload)
#     return {"mesage":"Successfully Created Post here",
#             "new_post": f"title is {payload['title']} and content is {payload['content']}"
#             }

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    post_dict = post.dict()
    post_dict["id"]= randrange(0,10000000)
    my_posts.append(post_dict)
    
    return {"data":my_posts}

@app.get("/posts/latest")
def latest_post():
    latest_post = my_posts[-1]
    return {"latest_post": latest_post}

@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail= f'post with id {id} is not find'
                            )
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return f'post with id {id} is not find'
    return {"post_detail": post}


@app.delete("/posts/{id}")
def delete_post(id: int):
    index = find_index(id)
    
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f'Post with id {id} does not exist')
    
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id:int, post:Post):
    index = find_index(id)
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f'Post with id {id} does not exist')
    post_dict = post.dict()
    print(post_dict)
    post_dict['id']= id
    my_posts[index]= post_dict
    return {"data":post_dict}


