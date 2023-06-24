from fastapi import Response,status,HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session 
from .. import schemas, oauth2,database,models

routers = APIRouter(    
    prefix="/vote",
    tags=['Vote'])

@routers.post('/',status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote,db: Session = Depends(database.get_db) ,current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"Post id {vote.post_id} not found")
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id,models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()
    if (vote.dir == 1):
        if found_vote:
            raise HTTPException(status.HTTP_409_CONFLICT,detail="Vote already exists")
        new_vote = models.Vote(post_id = vote.post_id,user_id = current_user.id)
        db.add(new_vote)
        db.commit()
        db.refresh(new_vote)
        return {"message":"Voted successfully"}
    else:
        if not found_vote:
            raise HTTPException(status.HTTP_404_NOT_FOUND,detail="vote not exists")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message":"Unvoted sucessfully"}
