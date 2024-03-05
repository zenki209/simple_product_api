from fastapi import APIRouter, Depends, status, HTTPException
import schemas
import models
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from database import get_db
from datetime import datetime, timedelta
from jose import jwt

# FOR JWT
SECRET_KEY = "f9037d2829bb8ae55a34f42b5969e8a1d23fb732e86bcaf18be6a8543c941fe8e4847d199f8b6b035452d6c2f733407dbafbffab4884e27b09c579027a1f2b1699554ed512e87c80ef94a940fd455d19"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 20


router = APIRouter()

# create password context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def generate_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # SET THE EXPIRED TIME FOR THE TOKEN
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@router.post('/login')
def login(request: schemas.Login, db: Session = Depends(get_db)):
    user = db.query(models.Seller).filter(
        models.Seller.username == request.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='user name not found')

    if not pwd_context.verify(request.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Invalid Password')

    # Gen JWT Token
    access_token = generate_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}
