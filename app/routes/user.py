from fastapi import status,HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session 
from .. import models,schemas,untils
from ..database import get_db

routers = APIRouter()


@routers.post("/users", status_code=status.HTTP_201_CREATED,response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate,db:Session = Depends(get_db)):
    user.password = untils.hashPassword(user.password)
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@routers.get('/users/{id}',response_model=schemas.UserOut)
def get_user(id:int,db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == str(id)).first()
    if user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No user id {id} found")
    return user
