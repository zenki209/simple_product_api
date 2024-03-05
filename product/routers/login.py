from fastapi import APIRouter, Depends, status, HTTPException
import schemas,models
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from database import get_db

router = APIRouter()

#create password context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post('/login')
def login(request: schemas.Login, db: Session = Depends(get_db)):
    user = db.query(models.Seller).filter(models.Seller.username == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='user name not found')
    

    if not pwd_context.verify(request.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail= 'Invalid Password')
    
    #Gen JWT Token

    return request
