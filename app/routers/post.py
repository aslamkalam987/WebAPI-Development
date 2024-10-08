from .. import models, schemas, oauth2
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import session
from ..database import engine,get_db
from typing import List, Optional
from sqlalchemy import func

router = APIRouter(
    prefix="/posts",
    tags = ["posts"]
)

# @router.get("/")
# def root():
#     return {"message": "This is root path"

@router.get("/", response_model=List[schemas.PostOut], )
# def get_posts():
#     cursor.execute("""SELECT * FROM posts """)
#     posts = cursor.fetchall()

#     return {"data":posts}
def get_posts(db:session= Depends(get_db), current_user : int = Depends(oauth2.get_current_user),
              limit:int = 10, skip:int= 0, search:Optional[str]= ''):
    
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts





@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
# def create_posts(post: Post):
#     cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s)  RETURNING * """,
#                    (post.title, post.content, post.published ))
#     new_post = cursor.fetchone()
#     conn.commit()
#     return {"data":new_post}

def create_posts(post:schemas.PostCreate, db:session= Depends(get_db),
                 current_user : int = Depends(oauth2.get_current_user)):
    #print(current_user.email)
    new_post = models.Post(owner_id =current_user.id,**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post



@router.get("/{id}",response_model=schemas.PostOut )
# def get_post(id: int):
#     cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id)))
#     post = cursor.fetchone()
#     if not post:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail= f'post with id {id} is not find'
#                             )
#         # response.status_code = status.HTTP_404_NOT_FOUND
#         # return f'post with id {id} is not find'
#     return {"post_detail": post}
def get_posts(id: int,db:session= Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()

    #print(db.query(models.Post).filter(models.Post.id == id))
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail= f'post with id {id} is not found'
                            )
    return  post


@router.delete("/{id}")
# def delete_post(id: int):
#     cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
#     delete_post = cursor.fetchone()
#     conn.commit()
#     if delete_post is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
#                             detail=f'Post with id {id} does not exist')
#     return Response(status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int, db: session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail= f'post with id {id} is not found')
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail ="Not Authorized to perform the action")
    post_query.delete(synchronize_session = False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)




@router.put("/{id}", response_model= schemas.Post)
# def update_post(id:int, post:Post):
#     cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
#                    (post.title, post.content, post.published, str(id)))
#     update_post = cursor.fetchone()
#     conn.commit()
#     if update_post is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
#                             detail=f'Post with id {id} does not exist')
    
#     return {"data":update_post}
def update_posts(id: int,updated_post:schemas.PostCreate, db: session = Depends(get_db),current_user : int = Depends(oauth2.get_current_user)):
     post_query= db.query(models.Post).filter(models.Post.id == id)

     post = post_query.first()
     
     if post == None:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail= f'post with id {id} is not found')
     
     if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail ="Not Authorized to perform the action")
     
     post_query.update(updated_post.dict(), synchronize_session = False)
     db.commit()
     return post_query.first()