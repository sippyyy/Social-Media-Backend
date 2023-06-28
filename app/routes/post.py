from fastapi import Response,status,HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from .. import models,schemas,oauth2
from ..database import get_db
from typing import List,Optional

routers = APIRouter(
    prefix="/posts",
    tags=['Posts']
)


@routers.get("/",response_model=List[schemas.PostOut])
async def getPost(db:Session = Depends(get_db),
                  current_user: int=Depends(oauth2.get_current_user),
                  limit: int= 10,
                  search:Optional[str]="",
                  skip:int= 0):
    result = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(
            models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    return result

@routers.get("/myposts",response_model=List[schemas.PostOut])
async def getYourPosts(db:Session = Depends(get_db),
                       current_user: int=Depends(oauth2.get_current_user),
                       limit: int= 10,
                       search:Optional[str]="",
                       skip:int= 0):
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
            models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(
            models.Post.id).filter(models.Post.title.contains(search)).filter(models.Post.owner_id == current_user.id).limit(limit).offset(skip).all()
    return posts

@routers.get("/myposts/{id}",response_model=schemas.PostOut)
async def myposts(id: int, db:Session = Depends(get_db),current_user: int=Depends(oauth2.get_current_user)):
    result= db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(
            models.Post.id).filter(models.Post.id == id).filter(models.Post.owner_id == current_user.id).first()
    if not result:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, 
                            detail=f"No post found with id {id}")
    if result.Post.owner_id != current_user.id:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN,detail="Not authorized to see this post")
    return result


@routers.post("/", status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def create_posts(post: schemas.PostCreate,db:Session = Depends(get_db),current_user: int=Depends(oauth2.get_current_user)):
    new_post = models.Post(owner_id = current_user.id,**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@routers.get("/{id}",response_model=schemas.PostOut)
def get_post(id: int,db: Session = Depends(get_db),current_user: int=Depends(oauth2.get_current_user)):
    result= db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(
            models.Post.id).filter(models.Post.id == id).first()
    if not result:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, 
                            detail=f"No post found with id {id}")
    if result.Post.owner_id != current_user.id:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN,detail="Not authorized to see this post")
    return result

@routers.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int,db:Session = Depends(get_db),current_user: int=Depends(oauth2.get_current_user)):
    post_delete = db.query(models.Post).filter(models.Post.id == id)
    post = post_delete.first()
    # cursor.execute("""DELETE FROM posts WHERE id = %s returning *""",(str(id),))
    # post_delete = cursor.fetchone()
    # index = find_index_post(id)
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"No post found with id {id} to delete")
    # my_posts.pop(index)
    # conn.commit()
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to delete")
    post_delete.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@routers.put("/{id}",response_model=schemas.Post)
def update_post(id: int, post: schemas.PostCreate,db:Session = Depends(get_db),current_user: int=Depends(oauth2.get_current_user)):
    # cursor.execute("""UPDATE posts SET title=%s,content=%s,published=%s WHERE id = %s  RETURNING *""",(post.title,post.content,post.published,str(id)))
    # post_updated = cursor.fetchone()
    # conn.commit()
    post_updated = db.query(models.Post).filter(models.Post.id == id)
    post_query = post_updated.first()
    # index = find_index_post(id)
    if post_query == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"No post found with id {id} to update")
    if post_query.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to update")

    post_updated.update(post.dict(),synchronize_session=False)
    db.commit()
    # post_result = post.dict()    
    # post_result['id'] = id
    # my_posts[index] = post_result
    return post_updated.first()
