from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import session
from .. import database, schemas, models, utils

router = APIRouter(tags= ["Authentication"])

@router.post("/login")
def login(user_credentials:schemas.UserLogin,db:session = Depends(database.get_db)):

   user = db.query(models.Users).filter(models.Users.email == user_credentials.email).first()

   if not user:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail ="Invalid Credentials")
   
   print(user_credentials.password,user.password)
   if not utils.verify(user_credentials.password, user.password):
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail ="Invalid Credentials")

   return {"token":"token"}