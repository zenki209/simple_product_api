from fastapi import APIRouter, status, Response, HTTPException
from sqlalchemy.orm import Session
from fastapi.params import Depends
import models
from schemas import *
from database import get_db
from typing import List

router = APIRouter()

@router.post('/seller', response_model=DisplaySeller, tags=['Sellers'])
def add_seller(request: Seller, db: Session = Depends(get_db)):
    hashed_pwd = pwd_context.hash(request.password)

    new_Seller = models.Seller(
        username=request.name, email=request.email, password=hashed_pwd
    )
    db.add(new_Seller)
    db.commit()
    db.refresh(new_Seller)
    return request