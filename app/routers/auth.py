from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import session
from .. import database, schemas, models, utils, oauth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter(tags= ["Authentication"])

@router.post("/login")
#def login(user_credentials:schemas.UserLogin,db:session = Depends(database.get_db)):
def login(user_credentials:OAuth2PasswordRequestForm = Depends() , db:session = Depends(database.get_db)):

   #{"username": "sdfghjkl@gamil.com", "password":"fkjj9290"}

   #user = db.query(models.Users).filter(models.Users.email == user_credentials.email).first()

   user = db.query(models.Users).filter(models.Users.email == user_credentials.username).first()
   if not user:
    raise HTTPException(status_code=status.HTTP_403,detail ="Invalid Credentials")
   
   #print(user_credentials.password,user.password)
   if not utils.verify(user_credentials.password, user.password):
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail ="Invalid Credentials")

   access_token = oauth2.create_access_token(data={"user_id":user.id})

   return {"access_token":access_token,"token_type":"bearer"}