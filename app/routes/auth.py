from fastapi import APIRouter,Depends,HTTPException,status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .. import database,models,untils,oauth2

routers = APIRouter(tags=['Authentication'])

@routers.post('/login')
def login(user_credentials: OAuth2PasswordRequestForm = Depends(),db:Session = Depends(database.get_db)):
    # OAuth2 password return username and email
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"No user found with email {user_credentials.username}")
    if not untils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail=f"wrong password")
    # create token
    # return token
    
    access_token = oauth2.create_access_token(data={"user_id":user.id})
    return {"token":access_token,"token_type":"bearer"}
